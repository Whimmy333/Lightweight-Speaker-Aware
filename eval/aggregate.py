"""Collect finished runs into per-run and mean ± std (over seeds) tables.

    python -m eval.aggregate                       # outputs/runs -> outputs/results_*
    python -m eval.aggregate --runs-dir outputs/smoke --out-prefix outputs/smoke/results

Writes <prefix>_runs.csv (one row per run), <prefix>_summary.csv (grouped by dataset,
model, context turns) and <prefix>_summary.md (main comparison, context length, ablations,
encoder comparison, term weighting x classifier).

The main-study tables hold DistilBERT and TF-IDF + LR only. Runs whose config names another
backbone (``model.backbone``) or a traditional classifier (``model.arch: classical``) appear
in their own tables; hyper-parameter sweep runs (``sweep`` in the config) are summarised by
``python -m eval.hparams``. <prefix>_summary.csv keeps the main study only (the demo reads it);
every other configuration goes to <prefix>_comparison.csv.
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
# Descriptive columns: identical for every seed of a configuration.
INFO = ["arch", "backbone", "weighting", "classifier", "sweep_param", "sweep_value", "params_total",
        "params_trainable"]
BACKBONE_ORDER = ["distilbert", "bert", "roberta", "rnn", "birnn", "lstm", "bilstm", "gru", "bigru"]
ARCH_ORDER = ["single", "concat", "fixed", "adaptive"]
WEIGHTING_ORDER = ["binary", "tf", "tfidf", "bm25"]
CLASSIFIER_ORDER = ["lr", "svm", "mnb", "cnb", "rf"]
SKLEARN_TYPES = ("tfidf_lr", "classical")


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
        params = _read_json(d / "params.json") or {}
        mcfg, sweep = cfg["model"], cfg.get("sweep", {})
        sklearn_model = mcfg["type"] in SKLEARN_TYPES
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
            "arch": mcfg.get("arch", mcfg["name"]),
            "backbone": None if sklearn_model else mcfg.get("backbone", "distilbert"),
            "weighting": mcfg.get("weighting", "tfidf") if sklearn_model else None,
            "classifier": mcfg.get("classifier", "lr") if sklearn_model else None,
            "sweep_param": sweep.get("param"),
            "sweep_value": sweep.get("value"),
            "params_total": params.get("total", params.get("parameters")),
            "params_trainable": params.get("trainable"),
        }
        row.update({f"test_f1_{c}": v["f1"] for c, v in test["per_class"].items()})
        rows.append(row)
    return pd.DataFrame(rows)


def summarise(runs: pd.DataFrame) -> pd.DataFrame:
    value_cols = METRICS + sorted(c for c in runs.columns if c.startswith("test_f1_"))
    out = []
    for (ds, model, k), g in runs.groupby(["dataset", "model", "k"]):
        row = {"dataset": ds, "model": model, "k": k, "n_seeds": len(g), "seeds": " ".join(map(str, sorted(g.seed)))}
        row.update({c: g[c].iloc[0] for c in INFO if c in g})
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


def _count(v) -> str:
    if v is None or pd.isna(v):
        return "-"
    v = float(v)
    return f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}K" if v >= 1e3 else f"{v:.0f}"


def _ordered(values, order) -> list:
    present = set(values)
    return [v for v in order if v in present] + sorted(present - set(order))


def _matrix(df: pd.DataFrame, row_col: str, col_col: str, row_order, col_order, metric="test_macro_f1") -> list:
    """One cell per (row_col, col_col) pair, e.g. weighting x classifier."""
    cols = _ordered(df[col_col], col_order)
    lines = [f"| {row_col} | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
    for r in _ordered(df[row_col], row_order):
        cells = []
        for c in cols:
            hit = df[(df[row_col] == r) & (df[col_col] == c)]
            cells.append(_fmt(hit.iloc[0], metric) if len(hit) else "-")
        lines.append(f"| {r} | " + " | ".join(cells) + " |")
    return lines + [""]


def _encoder_section(s: pd.DataFrame, ds: str, main_k: int) -> list:
    enc = s[s.backbone.notna() & s.sweep_param.isna() & s.arch.isin(ARCH_ORDER)
            & ((s.k == main_k) | (s.arch == "single"))]
    if enc.backbone.nunique() < 2:
        return []
    enc = enc.assign(_b=enc.backbone.map({b: i for i, b in enumerate(BACKBONE_ORDER)}).fillna(99),
                     _a=enc.arch.map({a: i for i, a in enumerate(ARCH_ORDER)}))
    lines = [f"## {ds}: encoder comparison (k={main_k})", "",
             "Test Macro-F1. Every encoder sees the same word pieces under the same token budget and dev selection.",
             ""]
    lines += _matrix(enc, "backbone", "arch", BACKBONE_ORDER, ARCH_ORDER)
    lines += ["| model | k | seeds | test Macro-F1 | latency ms/utt | parameters | trainable |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for _, r in enc.sort_values(["_b", "_a"]).iterrows():
        lines.append(f"| {r.model} | {r.k} | {r.n_seeds} | {_fmt(r, 'test_macro_f1')} | {_fmt(r, 'latency_ms', 2)} "
                     f"| {_count(r.params_total)} | {_count(r.params_trainable)} |")
    return lines + [""]


def _classical_section(s: pd.DataFrame, ds: str) -> list:
    cl = s[s.weighting.notna()]
    if len(cl) < 2:
        return []
    return ([f"## {ds}: term weighting x classifier", "",
             "Test Macro-F1 of the setting selected on dev Macro-F1 (current utterance only; one run each).", ""]
            + _matrix(cl, "weighting", "classifier", WEIGHTING_ORDER, CLASSIFIER_ORDER))


def to_markdown(summary: pd.DataFrame, main_k: int = 3) -> str:
    cols = [("dev Macro-F1", "dev_macro_f1"), ("test Macro-F1", "test_macro_f1"),
            ("test Weighted-F1", "test_weighted_f1"), ("latency ms/utt", "latency_ms")]
    lines = ["# Results summary", "", "Mean ± sample std over seeds. Checkpoints were selected on dev Macro-F1.", ""]
    for ds in summary.dataset.unique():
        everything = summary[summary.dataset == ds]
        s = everything[everything.arch == everything.model]  # main study: DistilBERT and TF-IDF + LR
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
        lines += _encoder_section(everything, ds, main_k)
        lines += _classical_section(everything, ds)
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-dir", default="outputs/runs")
    ap.add_argument("--out-prefix", default="outputs/results")
    ap.add_argument("--allow-drop", action="store_true",
                    help="rewrite the tables even if runs listed in <prefix>_runs.csv are missing from --runs-dir")
    args = ap.parse_args()
    runs = collect(Path(args.runs_dir))
    if runs.empty:
        print(f"no finished runs under {args.runs_dir}")
        return
    previous = Path(f"{args.out_prefix}_runs.csv")
    if previous.exists() and not args.allow_drop:
        missing = sorted(set(pd.read_csv(previous).run_name) - set(runs.run_name))
        if missing:
            raise SystemExit(f"{len(missing)} runs in {previous} are not under {args.runs_dir} (e.g. {missing[0]}); "
                             f"rewriting would drop them. Pull their run folders first, or pass --allow-drop.")
    summary = summarise(runs)
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    runs.to_csv(f"{prefix}_runs.csv", index=False)
    main_study = summary.arch == summary.model
    summary[main_study].to_csv(f"{prefix}_summary.csv", index=False)
    if (~main_study).any():
        summary[~main_study].to_csv(f"{prefix}_comparison.csv", index=False)
    Path(f"{prefix}_summary.md").write_text(to_markdown(summary), encoding="utf-8")
    print(f"{len(runs)} runs -> {prefix}_runs.csv, {prefix}_summary.csv, {prefix}_comparison.csv, "
          f"{prefix}_summary.md")


if __name__ == "__main__":
    main()
