"""Hyper-parameter effects, gathered from the logs every run already writes.

    python -m eval.hparams                  # outputs/runs -> outputs/hparams_*.csv, outputs/hparams_summary.md

Three tidy tables, one row per measurement, ready for plots (Streamlit, slides):

  hparams_epochs.csv  neural runs: dev metrics after every epoch for every learning rate tried
                      (lr_<lr>/epoch_metrics.jsonl). ``selected`` marks the (lr, epoch) kept on dev;
                      only that checkpoint has a test score, which is in results_runs.csv.
  hparams_sweep.csv   hyper-parameter sweep runs (config key ``sweep``): one setting changed at a
                      time on MELD, each with its own dev-selected epoch and test score.
  hparams_grid.csv    traditional models: dev Macro-F1 of every grid point (grid_search.csv).

hparams_summary.md shows the same data as tables. Dev scores describe the selection; only the sweep
reports test scores per setting, and none of these numbers changes a setting of the main study.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from eval.aggregate import CLASSIFIER_ORDER, WEIGHTING_ORDER, collect

RUN_INFO = ["run_name", "dataset", "model", "arch", "backbone", "k", "seed", "sweep_param", "sweep_value"]
EPOCH_COLUMNS = ["lr", "epoch", "train_loss", "dev_macro_f1", "dev_weighted_f1", "dev_accuracy", "epoch_seconds"]
CLASSIFIER_KNOB = {"lr": "C", "svm": "C", "mnb": "alpha", "cnb": "alpha", "rf": "min_samples_leaf"}


def _run_dirs(runs_dir: Path):
    for d in sorted(p for p in runs_dir.iterdir() if (p / "DONE").exists() and (p / "config.yaml").exists()):
        yield d, yaml.safe_load((d / "config.yaml").read_text(encoding="utf-8"))


def epoch_table(runs_dir: Path, runs: pd.DataFrame) -> pd.DataFrame:
    info = runs.set_index("run_name")[RUN_INFO[1:]] if not runs.empty else None
    rows = []
    for d, cfg in _run_dirs(runs_dir):
        if cfg["run_name"] not in getattr(info, "index", []):
            continue
        best = json.loads((d / "best.json").read_text(encoding="utf-8")) if (d / "best.json").exists() else {}
        for path in sorted(d.glob("lr_*/epoch_metrics.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line:
                    continue
                e = json.loads(line)
                row = {"run_name": cfg["run_name"], **info.loc[cfg["run_name"]].to_dict()}
                row.update({c: e.get(c) for c in EPOCH_COLUMNS})
                row["selected"] = e["lr"] == best.get("lr") and e["epoch"] == best.get("epoch")
                rows.append(row)
    return pd.DataFrame(rows)


def sweep_table(runs: pd.DataFrame) -> pd.DataFrame:
    if runs.empty or runs.sweep_param.isna().all():
        return pd.DataFrame()
    cols = RUN_INFO + ["selected_lr", "selected_epoch", "dev_macro_f1", "test_macro_f1", "test_weighted_f1",
                       "latency_ms"]
    return runs[runs.sweep_param.notna()][cols].reset_index(drop=True)


def grid_table(runs_dir: Path) -> pd.DataFrame:
    frames = []
    for d, cfg in _run_dirs(runs_dir):
        mcfg = cfg["model"]
        if mcfg["type"] not in ("tfidf_lr", "classical") or not (d / "grid_search.csv").exists():
            continue
        g = pd.read_csv(d / "grid_search.csv", dtype=str)
        for c in ("dev_macro_f1", "dev_weighted_f1", "n_features", "fit_seconds"):
            g[c] = pd.to_numeric(g[c])
        g.insert(0, "classifier", mcfg.get("classifier", "lr"))
        g.insert(0, "weighting", mcfg.get("weighting", "tfidf"))
        g.insert(0, "model", mcfg["name"])
        g.insert(0, "dataset", cfg["data"]["dataset"])
        g["selected"] = False
        g.loc[g.dev_macro_f1.idxmax(), "selected"] = True  # first maximum, as in the training scripts
        frames.append(g)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _ms(values) -> str:
    v = pd.to_numeric(pd.Series(values), errors="coerce").dropna()
    if v.empty:
        return "-"
    return f"{v.mean():.4f}" if len(v) == 1 else f"{v.mean():.4f} ± {v.std(ddof=1):.4f}"


def _sorted_values(values) -> list:
    def key(v):
        try:
            return (0, float(v))
        except (TypeError, ValueError):
            return (1, str(v))
    return sorted(set(values), key=key)


def epochs_markdown(epochs: pd.DataFrame) -> list:
    if epochs.empty:
        return []
    main = epochs[epochs.sweep_param.isna()]
    lines = ["## Learning rate x epoch (dev Macro-F1, mean ± std over seeds)", "",
             "Every run trains each learning rate from the same seed and keeps the (learning rate, epoch) with the "
             "best dev Macro-F1. `selected` counts how many seeds kept each learning rate.", ""]
    for (ds, model, k), g in main.groupby(["dataset", "model", "k"], sort=False):
        lrs = sorted(g.lr.unique())
        lines += [f"### {ds} / {model} (k={k})", "",
                  "| epoch | " + " | ".join(f"lr {lr:g}" for lr in lrs) + " |", "|---:|" + "---:|" * len(lrs)]
        for ep in sorted(g.epoch.unique()):
            lines.append(f"| {ep} | " + " | ".join(_ms(g[(g.lr == lr) & (g.epoch == ep)].dev_macro_f1)
                                                   for lr in lrs) + " |")
        picked = g[g.selected].groupby("lr").size()
        lines += ["| selected | " + " | ".join(f"{picked.get(lr, 0)}/{g.seed.nunique()}" for lr in lrs) + " |", ""]
    return lines


def sweep_markdown(sweep: pd.DataFrame, reference: dict) -> list:
    if sweep.empty:
        return []
    archs = [a for a in ("single", "adaptive") if a in set(sweep.arch)]
    lines = ["## One setting at a time (MELD, DistilBERT, k=3)", "",
             "Each setting trains one learning rate and selects its epoch on dev; test is evaluated once at that "
             f"epoch. Reference: {', '.join(f'{k} {v:g}' for k, v in reference.items())}.", ""]
    for param, g in sweep.groupby("sweep_param", sort=False):
        head = " | ".join(f"{a} dev | {a} test" for a in archs)
        lines += [f"### {param}", "", f"| {param} | {head} |", "|---:|" + "---:|---:|" * len(archs)]
        for value in _sorted_values(g.sweep_value):
            cells = []
            for a in archs:
                hit = g[(g.arch == a) & (g.sweep_value == value)]
                cells += [_ms(hit.dev_macro_f1), _ms(hit.test_macro_f1)]
            mark = " (reference)" if np.isclose(float(value), float(reference.get(param, np.nan))) else ""
            lines.append(f"| {value:g}{mark} | " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def grid_markdown(grid: pd.DataFrame) -> list:
    if grid.empty:
        return []
    lines = ["## Traditional models: main hyper-parameter (best dev Macro-F1 over the rest of the grid)", ""]
    for ds, gd in grid.groupby("dataset", sort=False):
        for clf in [c for c in CLASSIFIER_ORDER if c in set(gd.classifier)]:
            knob = CLASSIFIER_KNOB[clf]
            g = gd[gd.classifier == clf]
            ws = [w for w in WEIGHTING_ORDER if w in set(g.weighting)]
            lines += [f"### {ds} / {clf}: {knob}", "", f"| {knob} | " + " | ".join(ws) + " |",
                      "|---:|" + "---:|" * len(ws)]
            for value in _sorted_values(g[knob]):
                cells = [g[(g.weighting == w) & (g[knob] == value)].dev_macro_f1.max() for w in ws]
                lines.append(f"| {value} | " + " | ".join("-" if pd.isna(c) else f"{c:.4f}" for c in cells) + " |")
            lines.append("")
    return lines


def main() -> None:
    from configs.generate_configs import SWEEP_REFERENCE

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-dir", default="outputs/runs")
    ap.add_argument("--out-prefix", default="outputs/hparams")
    args = ap.parse_args()
    runs_dir, prefix = Path(args.runs_dir), Path(args.out_prefix)
    runs = collect(runs_dir)
    tables = {"epochs": epoch_table(runs_dir, runs), "sweep": sweep_table(runs), "grid": grid_table(runs_dir)}
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        if not df.empty:
            df.to_csv(f"{prefix}_{name}.csv", index=False)
        print(f"{name}: {len(df)} rows" + (f" -> {prefix}_{name}.csv" if not df.empty else ""))
    md = (["# Hyper-parameter effects", ""] + epochs_markdown(tables["epochs"])
          + sweep_markdown(tables["sweep"], SWEEP_REFERENCE) + grid_markdown(tables["grid"]))
    Path(f"{prefix}_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"summary -> {prefix}_summary.md")


if __name__ == "__main__":
    main()
