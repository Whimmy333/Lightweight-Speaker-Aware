"""Training loop shared by every neural model (single, concat, fixed and adaptive fusion).

One config = one run = (dataset, model, context window, seed). The run trains once with
every learning rate in ``train.lrs`` (each from the same seed), keeps the (lr, epoch) with
the best dev Macro-F1, and evaluates that checkpoint on dev and test.

Layout of ``output_dir``:
  config.yaml, train.log
  lr_<lr>/epoch_metrics.jsonl          dev metrics after every epoch
  lr_<lr>/checkpoints/best.pt          best epoch of this lr (removed for the lr not selected)
  lr_<lr>/checkpoints/last.pt          resume state; deleted when the lr finishes
  best.json                            selected lr, epoch, dev Macro-F1, checkpoint path
  metrics_{dev,test}.json              shared metrics (eval/metrics.py)
  predictions_{dev,test}.csv           shared prediction format (eval/predictions.py)
  fusion_weights_{dev,test}.csv        fusion models only, fixed column layout
  metrics_{dev,test}_equal_weights.json  learned-gate models evaluated with equal weights
  latency.json, report.md, DONE
Rerunning a finished run is a no-op; an interrupted run resumes from the last finished epoch.
"""

from __future__ import annotations

import contextlib
import json
import logging
import math
import os
import random
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
import torch.nn.functional as F
import yaml
from torch.utils.data import DataLoader
from transformers import AutoConfig, AutoTokenizer, get_linear_schedule_with_warmup

from data.context import build_contexts
from data.loaders import LABELS, SPLITS, label_to_id, load_split
from eval.latency import measure_latency
from eval.metrics import compute_metrics, metrics_to_markdown, save_metrics
from eval.predictions import fusion_weights_frame, predictions_frame, save_predictions
from models.batching import Collator, build_token_cache, max_sequence_length
from models.neural import build_model, input_mode

log = logging.getLogger("train")


# ---------------------------------------------------------------- setup helpers

def setup_logging(out_dir: Path) -> None:
    log.handlers.clear()
    log.setLevel(logging.INFO)
    log.propagate = False
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    for h in (logging.StreamHandler(sys.stdout), logging.FileHandler(out_dir / "train.log", encoding="utf-8")):
        h.setFormatter(fmt)
        log.addHandler(h)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def resolve_device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


def amp_dtype(device: torch.device, enabled: bool) -> Optional[torch.dtype]:
    if device.type != "cuda" or not enabled:
        return None
    return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16


def autocast(device: torch.device, dtype: Optional[torch.dtype]):
    if dtype is None:
        return contextlib.nullcontext()
    return torch.autocast(device_type=device.type, dtype=dtype)


def to_device(batch: dict, device: torch.device) -> dict:
    return {k: v.to(device, non_blocking=True) if torch.is_tensor(v) else v for k, v in batch.items()}


def atomic_save(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    torch.save(obj, tmp)
    os.replace(tmp, path)


def lr_tag(lr: float) -> str:
    return f"lr_{lr:g}"


def write_config(config: dict, out_dir: Path) -> None:
    """Save the config; refuse to resume a run directory created with a different config."""
    path = out_dir / "config.yaml"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            saved = yaml.safe_load(f)
        if saved != config:
            raise RuntimeError(
                f"{path} differs from the requested config. Use a new run_name/output_dir, "
                f"or delete {out_dir} to start this run again."
            )
        return
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)


# ---------------------------------------------------------------- data

class RunData:
    """Records, contexts, label ids and token caches for train/dev/test."""

    def __init__(self, config: dict, tokenizer):
        dcfg, ccfg = config["data"], config["context"]
        self.dataset = dcfg["dataset"]
        self.labels = LABELS[self.dataset]
        l2i = label_to_id(self.dataset)
        num_turns = 0 if config["model"]["type"] == "single" else ccfg["num_turns"]
        self.records, self.contexts, self.items, self.cache = {}, {}, {}, {}
        for sp in SPLITS:
            recs = load_split(Path(dcfg.get("processed_dir", "data/processed")), self.dataset, sp)
            if dcfg.get("max_samples"):
                recs = recs[: dcfg["max_samples"]]
            ctx = build_contexts(recs, num_turns)  # labels of history turns are never copied
            self.records[sp] = recs
            self.contexts[sp] = ctx
            self.items[sp] = [(c, l2i[r["label"]]) for c, r in zip(ctx, recs)]
            self.cache[sp] = build_token_cache(tokenizer, recs, ccfg["max_utt_tokens"])


def make_loader(items, collator, batch_size: int, shuffle_seed: Optional[int] = None) -> DataLoader:
    generator = None
    if shuffle_seed is not None:
        generator = torch.Generator()
        generator.manual_seed(shuffle_seed)
    return DataLoader(items, batch_size=batch_size, shuffle=shuffle_seed is not None, generator=generator,
                      collate_fn=collator, num_workers=0)


@torch.no_grad()
def evaluate(model, loader, device, dtype, weighting_override: Optional[str] = None) -> dict:
    model.eval()
    probs, weights, avail = [], [], []
    for batch in loader:
        batch = to_device(batch, device)
        with autocast(device, dtype):
            out = model(batch, weighting_override=weighting_override)
        probs.append(torch.softmax(out["logits"].float(), -1).cpu())
        if "weights" in out:
            weights.append(out["weights"].float().cpu())
            avail.append(batch["avail"].cpu())
    probs = torch.cat(probs).numpy()
    res = {"probs": probs, "preds": probs.argmax(1)}
    if weights:
        res["weights"] = torch.cat(weights).numpy()
        res["avail"] = torch.cat(avail).numpy().astype(int)
    return res


# ---------------------------------------------------------------- training for one learning rate

def _optimizer(model, lr: float, weight_decay: float):
    decay, no_decay = [], []
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        (no_decay if name.endswith("bias") or "LayerNorm" in name or "layer_norm" in name else decay).append(p)
    return torch.optim.AdamW([{"params": decay, "weight_decay": weight_decay},
                              {"params": no_decay, "weight_decay": 0.0}], lr=lr)


def train_one_lr(config: dict, lr: float, data: RunData, collator: Collator, device, dtype, out_dir: Path) -> List[dict]:
    tcfg = config["train"]
    sub = out_dir / lr_tag(lr)
    ckpt_dir = sub / "checkpoints"
    metrics_path = sub / "epoch_metrics.jsonl"
    if (sub / "DONE").exists():
        log.info("%s already finished, skipping", sub.name)
        return [json.loads(line) for line in metrics_path.read_text(encoding="utf-8").splitlines() if line]

    seed = config["seed"]
    set_seed(seed)
    model = build_model(config["model"], len(data.labels)).to(device)
    optimizer = _optimizer(model, lr, tcfg.get("weight_decay", 0.01))
    steps_per_epoch = math.ceil(len(data.items["train"]) / tcfg["batch_size"])
    total_steps = steps_per_epoch * tcfg["epochs"]
    scheduler = get_linear_schedule_with_warmup(optimizer, int(tcfg.get("warmup_ratio", 0.1) * total_steps), total_steps)
    scaler = torch.amp.GradScaler("cuda", enabled=dtype == torch.float16)

    history: List[dict] = []
    best_f1, bad_epochs, start_epoch = -1.0, 0, 1
    last_path = ckpt_dir / "last.pt"
    if tcfg.get("resume", True) and last_path.exists():
        # Load on CPU: RNG states must stay CPU tensors; load_state_dict moves weights/optimizer to the device.
        state = torch.load(last_path, map_location="cpu", weights_only=False)
        model.load_state_dict(state["model"])
        optimizer.load_state_dict(state["optimizer"])
        scheduler.load_state_dict(state["scheduler"])
        scaler.load_state_dict(state["scaler"])
        history, best_f1, bad_epochs = state["history"], state["best_f1"], state["bad_epochs"]
        start_epoch = state["epoch"] + 1
        random.setstate(state["rng"]["python"])
        np.random.set_state(state["rng"]["numpy"])
        torch.set_rng_state(state["rng"]["torch"])
        if torch.cuda.is_available() and state["rng"].get("cuda") is not None:
            torch.cuda.set_rng_state_all(state["rng"]["cuda"])
        log.info("%s: resuming after epoch %d (best dev Macro-F1 so far %.4f)", sub.name, state["epoch"], best_f1)

    dev_loader = make_loader(data.items["dev"], collator, tcfg.get("eval_batch_size", 64))
    log_every = tcfg.get("log_every", 100)
    for epoch in range(start_epoch, tcfg["epochs"] + 1):
        model.train()
        t0, loss_sum, n_seen = time.time(), 0.0, 0
        loader = make_loader(data.items["train"], collator, tcfg["batch_size"], shuffle_seed=seed * 1000 + epoch)
        for step, batch in enumerate(loader, 1):
            batch = to_device(batch, device)
            with autocast(device, dtype):
                out = model(batch)
            loss = F.cross_entropy(out["logits"].float(), batch["labels"])
            optimizer.zero_grad(set_to_none=True)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), tcfg.get("max_grad_norm", 1.0))
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            loss_sum += loss.item() * len(batch["labels"])
            n_seen += len(batch["labels"])
            if step % log_every == 0:
                log.info("%s epoch %d step %d/%d loss %.4f", sub.name, epoch, step, steps_per_epoch, loss_sum / n_seen)

        res = evaluate(model, dev_loader, device, dtype)
        dev_y = [y for _, y in data.items["dev"]]
        m = compute_metrics(dev_y, res["preds"], data.labels)
        entry = {
            "lr": lr,
            "epoch": epoch,
            "train_loss": loss_sum / max(n_seen, 1),
            "dev_macro_f1": m["macro_f1"],
            "dev_weighted_f1": m["weighted_f1"],
            "dev_accuracy": m["accuracy"],
            "dev_per_class_f1": {k: v["f1"] for k, v in m["per_class"].items()},
            "epoch_seconds": round(time.time() - t0, 1),
        }
        history.append(entry)
        sub.mkdir(parents=True, exist_ok=True)
        metrics_path.write_text("".join(json.dumps(h) + "\n" for h in history), encoding="utf-8")
        improved = m["macro_f1"] > best_f1
        log.info("%s epoch %d: train loss %.4f, dev Macro-F1 %.4f, Weighted-F1 %.4f%s (%.0fs)", sub.name, epoch,
                 entry["train_loss"], m["macro_f1"], m["weighted_f1"], " *best*" if improved else "",
                 entry["epoch_seconds"])
        if improved:
            best_f1, bad_epochs = m["macro_f1"], 0
            atomic_save({"model": model.state_dict(), "lr": lr, "epoch": epoch, "dev_macro_f1": best_f1,
                         "labels": data.labels, "config": config}, ckpt_dir / "best.pt")
        else:
            bad_epochs += 1
        atomic_save({
            "model": model.state_dict(), "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
            "scaler": scaler.state_dict(), "epoch": epoch, "history": history, "best_f1": best_f1,
            "bad_epochs": bad_epochs,
            "rng": {"python": random.getstate(), "numpy": np.random.get_state(), "torch": torch.get_rng_state(),
                    "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None},
        }, last_path)
        patience = tcfg.get("patience")
        if patience and bad_epochs >= patience:
            log.info("%s: no dev improvement for %d epochs, stopping early", sub.name, patience)
            break

    (sub / "DONE").write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")
    last_path.unlink(missing_ok=True)
    del model, optimizer
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return history


# ---------------------------------------------------------------- full run

def _report(config, best, histories, metrics, eq_metrics, latency) -> str:
    lines = [f"# {config['run_name']}", "",
             f"Selected lr={best['lr']:g}, epoch {best['epoch']} (dev Macro-F1 {best['dev_macro_f1']:.4f}).", "",
             "| lr | epoch | train loss | dev Macro-F1 | dev Weighted-F1 | seconds |", "|---|---:|---:|---:|---:|---:|"]
    for hist in histories.values():
        for h in hist:
            lines.append(f"| {h['lr']:g} | {h['epoch']} | {h['train_loss']:.4f} | {h['dev_macro_f1']:.4f} "
                         f"| {h['dev_weighted_f1']:.4f} | {h['epoch_seconds']} |")
    lines.append("")
    for sp in ("dev", "test"):
        lines.append(metrics_to_markdown(metrics[sp], f"{sp} split (selected checkpoint)"))
    for sp, m in eq_metrics.items():
        lines.append(f"- {sp} with the learned gate replaced by equal weights at inference: Macro-F1 "
                     f"{m['macro_f1']:.4f}, Weighted-F1 {m['weighted_f1']:.4f}")
    if latency.get("n_samples"):
        lines += ["", f"Latency: {latency['ms_per_utterance']:.2f} ms/utterance end to end "
                      f"(batch size {latency['batch_size']}, {latency['n_samples']} test utterances, "
                      f"{latency['hardware']})."]
    return "\n".join(lines) + "\n"


def run(config: dict) -> Optional[dict]:
    out_dir = Path(config["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(out_dir)
    if (out_dir / "DONE").exists():
        log.info("%s is already complete (%s/DONE); delete the directory to rerun", config["run_name"], out_dir)
        return None
    config["train"]["lrs"] = [float(lr) for lr in config["train"]["lrs"]]  # YAML reads "1e-4" as a string
    write_config(config, out_dir)

    mcfg, ccfg, tcfg = config["model"], config["context"], config["train"]
    mode = input_mode(mcfg)
    num_turns = 0 if mode == "single" else ccfg["num_turns"]
    max_positions = AutoConfig.from_pretrained(mcfg["pretrained"]).max_position_embeddings
    need = max_sequence_length(mode, num_turns, ccfg["max_utt_tokens"])
    if need > max_positions:
        raise ValueError(f"token budget needs {need} positions but the encoder supports {max_positions}; "
                         f"lower context.max_utt_tokens")

    device = resolve_device(tcfg.get("device", "auto"))
    dtype = amp_dtype(device, tcfg.get("amp", True))
    log.info("run %s on %s (amp=%s), model=%s, k=%d, lrs=%s", config["run_name"], device, dtype, mcfg["name"],
             num_turns, tcfg["lrs"])

    tokenizer = AutoTokenizer.from_pretrained(mcfg["pretrained"])
    data = RunData(config, tokenizer)
    speaker_split = mcfg.get("fusion", {}).get("speaker_split", True)
    collators = {sp: Collator(mode, tokenizer, ccfg["max_utt_tokens"], speaker_split, data.cache[sp]) for sp in SPLITS}
    log.info("utterances: %s", {sp: len(v) for sp, v in data.records.items()})

    histories = {}
    for lr in tcfg["lrs"]:
        histories[lr] = train_one_lr(config, lr, data, collators["train"], device, dtype, out_dir)

    # Select (lr, epoch) on dev Macro-F1 only; ties keep the earlier lr in the list.
    best = None
    for lr, hist in histories.items():
        for h in hist:
            if best is None or h["dev_macro_f1"] > best["dev_macro_f1"]:
                best = {"lr": lr, "epoch": h["epoch"], "dev_macro_f1": h["dev_macro_f1"]}
    best["checkpoint"] = str(out_dir / lr_tag(best["lr"]) / "checkpoints" / "best.pt")
    (out_dir / "best.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
    log.info("selected lr=%g epoch=%d dev Macro-F1=%.4f", best["lr"], best["epoch"], best["dev_macro_f1"])

    model = build_model(mcfg, len(data.labels)).to(device)
    state = torch.load(best["checkpoint"], map_location="cpu", weights_only=False)
    model.load_state_dict(state["model"])
    eval_bs = tcfg.get("eval_batch_size", 64)
    metrics, eq_metrics = {}, {}
    for sp in ("dev", "test"):
        loader = make_loader(data.items[sp], collators[sp], eval_bs)
        res = evaluate(model, loader, device, dtype)
        y = [lab for _, lab in data.items[sp]]
        metrics[sp] = compute_metrics(y, res["preds"], data.labels)
        save_metrics(metrics[sp], out_dir / f"metrics_{sp}.json")
        save_predictions(predictions_frame(data.records[sp], res["preds"], data.labels, res["probs"]),
                         out_dir / f"predictions_{sp}.csv")
        if "weights" in res:
            save_predictions(fusion_weights_frame(data.records[sp], data.contexts[sp], res["preds"], data.labels,
                                                  res["weights"], res["avail"], speaker_split),
                             out_dir / f"fusion_weights_{sp}.csv")
        if mode == "fusion" and mcfg["fusion"]["weighting"] == "learned":
            eq = evaluate(model, loader, device, dtype, weighting_override="equal")
            eq_metrics[sp] = compute_metrics(y, eq["preds"], data.labels)
            save_metrics(eq_metrics[sp], out_dir / f"metrics_{sp}_equal_weights.json")
        log.info("[%s] Macro-F1 %.4f Weighted-F1 %.4f", sp, metrics[sp]["macro_f1"], metrics[sp]["weighted_f1"])

    lcfg = config.get("latency", {})
    live = Collator(mode, tokenizer, ccfg["max_utt_tokens"], speaker_split, token_cache=None)  # tokenises inside

    @torch.no_grad()
    def predict(batch_items):
        batch = to_device(live(batch_items), device)
        with autocast(device, dtype):
            return model(batch)["logits"].argmax(-1).cpu()

    model.eval()
    latency = measure_latency(predict, data.items["test"], lcfg.get("batch_size", 1), lcfg.get("warmup", 10),
                              lcfg.get("max_samples", 300), str(device))
    (out_dir / "latency.json").write_text(json.dumps(latency, indent=2), encoding="utf-8")
    if latency.get("n_samples"):
        log.info("latency %.2f ms/utterance (batch %d)", latency["ms_per_utterance"], latency["batch_size"])

    (out_dir / "report.md").write_text(_report(config, best, histories, metrics, eq_metrics, latency), encoding="utf-8")

    scfg = config.get("save", {})
    for lr in tcfg["lrs"]:
        ckpt = out_dir / lr_tag(lr) / "checkpoints" / "best.pt"
        if not scfg.get("keep_best_checkpoint", True) or (lr != best["lr"] and scfg.get("prune_unselected", True)):
            ckpt.unlink(missing_ok=True)
        if not any((out_dir / lr_tag(lr) / "checkpoints").glob("*")):
            shutil.rmtree(out_dir / lr_tag(lr) / "checkpoints", ignore_errors=True)
    best["checkpoint_kept"] = Path(best["checkpoint"]).exists()
    (out_dir / "best.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
    (out_dir / "DONE").write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")
    log.info("run complete: %s", out_dir)
    return {"best": best, "metrics": metrics, "latency": latency}
