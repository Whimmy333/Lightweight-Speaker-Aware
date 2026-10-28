"""Parameter counts and hyper-parameter tables for every model in the experiment plan.

    python -m eval.model_details                     # -> outputs/model_details.md

Neural parameter counts come from building each configured model (no training needed; the
pretrained encoders must be in data/pretrained/). Traditional models have no fixed size: their
counts come from the params.json of finished runs. Hyper-parameters are read from the generated
configs; the values each run selected on dev come from <runs csv> and the run directories.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import yaml

from configs.generate_configs import CLASSICAL, CLASSIFIER_GRIDS, all_configs
from eval.aggregate import ARCH_ORDER, BACKBONE_ORDER, _count

NUM_LABELS = 7  # every dataset uses seven emotion classes


def neural_configs() -> list:
    """One MELD config (seed 42, main k) per backbone x architecture, in table order."""
    seen = {}
    for _, cfg in all_configs():
        mcfg = cfg["model"]
        if mcfg["type"] in ("tfidf_lr", "classical") or cfg["seed"] != 42 or cfg["data"]["dataset"] != "meld":
            continue
        key = (mcfg.get("backbone", "distilbert"), mcfg.get("arch", mcfg["name"]))
        if key[1] in ARCH_ORDER and cfg["context"]["num_turns"] in (0, 3):
            seen.setdefault(key, cfg)
    order = lambda k: (BACKBONE_ORDER.index(k[0]), ARCH_ORDER.index(k[1]))  # noqa: E731
    return [seen[k] for k in sorted(seen, key=order)]


def parameter_table(configs: list) -> list:
    from models.neural import build_model, count_parameters

    lines = ["## Parameter counts (neural models)", "",
             "Concatenation and fixed fusion add no parameters to the single-utterance model; adaptive fusion adds "
             "the gate. Recurrent encoders keep DistilBERT's word-piece embedding table frozen, so most of their "
             "parameters are not trained.", "",
             "| backbone | architecture | total | trainable | encoder | gate | head |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for cfg in configs:
        mcfg = cfg["model"]
        backbone, arch = mcfg.get("backbone", "distilbert"), mcfg.get("arch", mcfg["name"])
        if not Path(mcfg["pretrained"]).exists():
            lines.append(f"| {backbone} | {arch} | missing {mcfg['pretrained']} | | | | |")
            continue
        p = count_parameters(build_model(mcfg, NUM_LABELS))
        lines.append(f"| {backbone} | {arch} | {p['total']:,} | {p['trainable']:,} | {p['encoder']:,} "
                     f"| {p['gate']:,} | {p['head']:,} |")
    return lines + [""]


def classical_parameter_table(runs_dir: Path) -> list:
    rows = []
    for d in sorted(runs_dir.glob("*/params.json")):
        cfg_path = d.parent / "config.yaml"
        p = json.loads(d.read_text(encoding="utf-8"))
        if "unit" not in p or not cfg_path.exists():
            continue
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        rows.append((cfg["data"]["dataset"], cfg["model"]["name"], p))
    if not rows:
        return []
    lines = ["## Parameter counts (traditional models)", "",
             "Learned values of the selected model: one weight per feature and class (plus intercepts or class "
             "priors); tree nodes for the random forest.", "",
             "| dataset | model | features | parameters | unit | selected setting |",
             "|---|---|---:|---:|---|---|"]
    for ds, name, p in rows:
        lines.append(f"| {ds} | {name} | {p['n_features']:,} | {p['parameters']:,} ({_count(p['parameters'])}) "
                     f"| {p['unit']} | `{json.dumps(p.get('selected', {}))}` |")
    return lines + [""]


def hyperparameter_table(configs: list) -> list:
    by_family = {}
    for cfg in configs:
        family = "recurrent" if "rnn" in cfg["model"] else "transformer"
        if cfg["model"].get("arch", cfg["model"]["name"]) == "adaptive":
            by_family.setdefault(family, cfg)
    t, r = by_family["transformer"], by_family["recurrent"]

    def row(name, fn):
        return f"| {name} | {fn(t)} | {fn(r)} |"

    lrs = lambda c: ", ".join(f"{lr:g}" for lr in c["train"]["lrs"])  # noqa: E731
    rnn = r["model"]["rnn"]
    lines = ["## Hyper-parameters (neural models)", "",
             "Every run trains once per learning rate and keeps the (learning rate, epoch) with the best dev "
             "Macro-F1; test data are never used for selection.", "",
             "| setting | Transformers (DistilBERT, BERT, RoBERTa) | recurrent (RNN, LSTM, GRU) |", "|---|---|---|",
             row("optimiser", lambda c: "AdamW, linear warm-up then linear decay"),
             row("learning-rate grid", lrs),
             row("epochs", lambda c: c["train"]["epochs"]),
             row("batch size", lambda c: c["train"]["batch_size"]),
             row("warm-up ratio", lambda c: c["train"]["warmup_ratio"]),
             row("weight decay", lambda c: c["train"]["weight_decay"]),
             row("gradient clipping (max norm)", lambda c: c["train"]["max_grad_norm"]),
             row("dropout", lambda c: c["model"]["dropout"]),
             row("mixed precision (GPU)", lambda c: "bf16" if c["train"]["amp"] else "off (fp32)"),
             row("word pieces kept per utterance", lambda c: c["context"]["max_utt_tokens"]),
             row("context turns k (main study)", lambda c: c["context"]["num_turns"]),
             row("fusion gate hidden units", lambda c: c["model"]["fusion"]["gate_hidden"]),
             row("utterance vector", lambda c: f"{c['model'].get('utterance_pooling', 'cls')} token"
                 if "rnn" not in c["model"] else f"{c['model']['rnn']['pooling']}-pooling over time"),
             f"| recurrent encoder | - | {rnn['num_layers']} layer, {rnn['hidden_size']} units per direction |",
             f"| embeddings | - | DistilBERT word-piece table ({rnn['embedding_init']}, "
             f"{'frozen' if rnn['freeze_embeddings'] else 'trained'}) |",
             ""]
    feats = CLASSICAL["classical"]["feature_grid"]
    lines += ["## Hyper-parameter grids (traditional models)", "",
              "Each weighting x classifier pair searches its feature grid x classifier grid on dev Macro-F1. "
              f"Feature grid: n-gram range {feats['ngram_range']}, min_df {feats['min_df']}; "
              f"BM25 k1={CLASSICAL['classical']['bm25']['k1']}, b={CLASSICAL['classical']['bm25']['b']}. "
              "TF-IDF + LR uses the same feature grid with C in [0.1, 0.3, 1, 3, 10] and class_weight in "
              "[None, balanced].", "",
              "| classifier | grid |", "|---|---|"]
    lines += [f"| {name} | " + "; ".join(f"{k} {v}" for k, v in grid.items()) + " |"
              for name, grid in CLASSIFIER_GRIDS.items()]
    return lines + [""]


def selected_table(runs_csv: Path) -> list:
    if not runs_csv.exists():
        return []
    runs = pd.read_csv(runs_csv)
    runs = runs[runs.selected_lr.notna()]
    if runs.empty:
        return []
    lines = ["## Selected learning rate and epoch (per seed)", "",
             "| dataset | model | k | learning rate | epoch |", "|---|---|---:|---|---|"]
    for (ds, model, k), g in runs.sort_values("seed").groupby(["dataset", "model", "k"], sort=False):
        lrs = ", ".join(f"{lr:g}" for lr in g.selected_lr)
        epochs = ", ".join(str(int(e)) for e in g.selected_epoch)
        lines.append(f"| {ds} | {model} | {k} | {lrs} | {epochs} |")
    return lines + ["", "Values are listed in seed order (42, 43, 44)."]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-dir", default="outputs/runs")
    ap.add_argument("--runs-csv", default="outputs/results_runs.csv")
    ap.add_argument("--out", default="outputs/model_details.md")
    args = ap.parse_args()
    configs = neural_configs()
    lines = ["# Model details", ""]
    lines += parameter_table(configs)
    lines += classical_parameter_table(Path(args.runs_dir))
    lines += hyperparameter_table(configs)
    lines += selected_table(Path(args.runs_csv))
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
