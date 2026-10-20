"""Single entry point for every experiment.

    python train.py --config configs/meld/adaptive_k3_s42.yaml
    python train.py --config configs/meld/adaptive_k3_s42.yaml --smoke     # 50 samples, 1 epoch, CPU
    python train.py --config ... --override train.batch_size=8 train.device=cuda:1

All hyper-parameters live in the YAML config. ``model.type`` selects the pipeline:
tfidf_lr (models/tfidf_lr.py) or single / concat / fusion (models/trainer.py).
A finished run (``<output_dir>/DONE``) is skipped; an interrupted run resumes.
"""

from __future__ import annotations

import argparse
import copy
import os

import yaml

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

SMOKE_SAMPLES = 50


def apply_override(config: dict, item: str) -> None:
    key, sep, raw = item.partition("=")
    if not sep:
        raise ValueError(f"override {item!r} must look like a.b.c=value")
    node = config
    *parents, leaf = key.split(".")
    for p in parents:
        node = node.setdefault(p, {})
    node[leaf] = yaml.safe_load(raw)


def smoke_config(config: dict) -> dict:
    """Same pipeline on a tiny CPU budget; results go to outputs/smoke/ and no checkpoint is kept."""
    cfg = copy.deepcopy(config)
    cfg["data"]["max_samples"] = SMOKE_SAMPLES
    cfg["output_dir"] = os.path.join("outputs", "smoke", cfg["run_name"])
    cfg["latency"] = {**cfg.get("latency", {}), "max_samples": 20, "warmup": 2}
    if cfg["model"]["type"] != "tfidf_lr":
        cfg["train"].update({"epochs": 1, "device": "cpu", "amp": False, "log_every": 1})
        cfg["save"] = {**cfg.get("save", {}), "keep_best_checkpoint": False}
    return cfg


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--smoke", action="store_true", help=f"{SMOKE_SAMPLES} samples per split, 1 epoch, CPU")
    ap.add_argument("--override", nargs="*", default=[], metavar="KEY=VALUE")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    for item in args.override:
        apply_override(config, item)
    if args.smoke:
        config = smoke_config(config)

    if config["model"]["type"] == "tfidf_lr":
        from models.tfidf_lr import run
    else:
        from models.trainer import run
    run(config)


if __name__ == "__main__":
    main()
