"""Collect finished runs into per-run and mean ± std (over seeds) tables.

    python -m eval.aggregate                       # outputs/runs -> outputs/results_*
    python -m eval.aggregate --runs-dir outputs/smoke --out-prefix outputs/smoke/results

Writes <prefix>_runs.csv (one row per run), <prefix>_summary.csv (grouped by dataset,
model, context turns) and <prefix>_summary.md (main comparison, context length, ablations).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

MODEL_ORDER = ["tfidf_lr", "single", "concat", "fixed", "adaptive", "adaptive_merged"]
METRICS = ["dev_macro_f1", "test_macro_f1", "test_weighted_f1", "test_accuracy", "latency_ms",
           "test_macro_f1_equal_weights"]


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def collect(runs_dir: Path) -> pd.DataFrame:
    rows = []
    for d in sorted(p for p in runs_dir.iterdir() if (p / "DONE").exists() and (p / "config.yaml").exists()):
        cfg = yaml.safe_load((d / "config.yaml").read_text(encoding="utf-8"))
        dev, test = _read_json(d / "metrics_dev.json"), _read_json(d / "metrics_test.json")
        if dev is None or test is None:
            continue
        best = _read_json(d / "best.json") or {}
        lat = _read_json(d / "latency.json") or {}
        eq = _read_json(d / "metrics_test_equal_weights.json")
        row = {
            "run_name": cfg["run_name"],
            "dataset": cfg["data"]["dataset"],
            "model": cfg["model"]["name"],
            "k": cfg.get("context", {}).get("num_turns", 0),
            "seed": cfg.get("seed"),
            "selected_lr": best.get("lr"),
            "selected_epoch": best.get("epoch"),
            "dev_macro_f1": dev["macro_f1"],
            "test_macro_f1": test["macro_f1"],
            "test_weighted_f1": test["weighted_f1"],
            "test_accuracy": test["accuracy"],
            "latency_ms": lat.get("ms_per_utterance"),
            "test_macro_f1_equal_weights": eq["macro_f1"] if eq else None,
        }
        row.update({f"test_f1_{c}": v["f1"] for c, v in test["per_class"].items()})
        rows.append(row)
    return pd.DataFrame(rows)


def summarise(runs: pd.DataFrame) -> pd.DataFrame:
    value_cols = METRICS + sorted(c for c in runs.columns if c.startswith("test_f1_"))
    out = []
    for (ds, model, k), g in runs.groupby(["dataset", "model", "k"]):
        row = {"dataset": ds, "model": model, "k": k, "n_seeds": len(g), "seeds": " ".join(map(str, sorted(g.seed)))}
        for c in value_cols:
            vals = pd.to_numeric(g[c], errors="coerce").dropna()
            row[f"{c}_mean"] = vals.mean() if len(vals) else np.nan
            row[f"{c}_std"] = vals.std(ddof=1) if len(vals) > 1 else np.nan
        out.append(row)
    df = pd.DataFrame(out)
    if df.empty:
        return df
    df["_order"] = df.model.map({m: i for i, m in enumerate(MODEL_ORDER)}).fillna(99)
    return df.sort_values(["dataset", "_order", "k"]).drop(columns="_order")


def _fmt(row, col, digits=4) -> str:
    m, s = row.get(f"{col}_mean"), row.get(f"{col}_std")
    if m is None or pd.isna(m):
        return "-"
    return f"{m:.{digits}f}" if pd.isna(s) else f"{m:.{digits}f} ± {s:.{digits}f}"


def _table(df: pd.DataFrame, cols) -> list:
    lines = ["| model | k | seeds | " + " | ".join(h for h, _ in cols) + " |", "|---|---:|---:|" + "---:|" * len(cols)]
    for _, r in df.iterrows():
        lines.append(f"| {r.model} | {r.k} | {r.n_seeds} | " + " | ".join(_fmt(r, c, 2 if c == "latency_ms" else 4) for _, c in cols) + " |")
    return lines + [""]


def to_markdown(summary: pd.DataFrame, main_k: int = 3) -> str:
    cols = [("dev Macro-F1", "dev_macro_f1"), ("test Macro-F1", "test_macro_f1"),
            ("test Weighted-F1", "test_weighted_f1"), ("latency ms/utt", "latency_ms")]
    lines = ["# Results summary", "", "Mean ± sample std over seeds. Checkpoints were selected on dev Macro-F1.", ""]
    for ds in summary.dataset.unique():
        s = summary[summary.dataset == ds]
        main = s[(s.k == main_k) | s.model.isin(["tfidf_lr", "single"])]
        main = main[main.model != "adaptive_merged"]
        lines += [f"## {ds}: main comparison (k={main_k})", ""] + _table(main, cols)
        per_class = sorted(c[len("test_f1_"):-len("_mean")] for c in s.columns
                           if c.startswith("test_f1_") and c.endswith("_mean") and s[c].notna().any())
        if per_class:
            lines += [f"Per-class test F1 ({ds}):", ""]
            lines += _table(main, [(c, f"test_f1_{c}") for c in per_class])
        ctx = s[s.model.isin(["concat", "fixed", "adaptive"])]
        if ctx.k.nunique() > 1:
            lines += [f"## {ds}: context length", ""] + _table(ctx.sort_values(["model", "k"]), cols)
        abl = s[(s.k == main_k) & s.model.isin(["fixed", "adaptive", "adaptive_merged"])]
        if "adaptive_merged" in set(abl.model):
            lines += [f"## {ds}: ablations (k={main_k})", "",
                      "- `adaptive_merged`: same- and other-speaker history pooled into one source.",
                      "- `fixed`: equal weights instead of a learned gate, trained with the same architecture.",
                      "- equal weights at inference: the trained adaptive model with its gate replaced by equal weights.",
                      ""]
            lines += _table(abl, cols + [("test Macro-F1, equal weights at inference", "test_macro_f1_equal_weights")])
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-dir", default="outputs/runs")
    ap.add_argument("--out-prefix", default="outputs/results")
    args = ap.parse_args()
    runs = collect(Path(args.runs_dir))
    if runs.empty:
        print(f"no finished runs under {args.runs_dir}")
        return
    summary = summarise(runs)
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    runs.to_csv(f"{prefix}_runs.csv", index=False)
    summary.to_csv(f"{prefix}_summary.csv", index=False)
    Path(f"{prefix}_summary.md").write_text(to_markdown(summary), encoding="utf-8")
    print(f"{len(runs)} runs -> {prefix}_runs.csv, {prefix}_summary.csv, {prefix}_summary.md")


if __name__ == "__main__":
    main()
