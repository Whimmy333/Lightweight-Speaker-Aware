"""Shared classification metrics. Every model reports through ``compute_metrics``."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support


def compute_metrics(y_true: Sequence[int], y_pred: Sequence[int], labels: List[str]) -> Dict:
    """Macro-F1 (primary), Weighted-F1, accuracy, per-class P/R/F1/support and the
    confusion matrix (rows = gold, columns = predicted, in ``labels`` order)."""
    idx = list(range(len(labels)))
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=idx, zero_division=0)
    return {
        "n": int(len(y_true)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=idx, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=idx, average="weighted", zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "per_class": {
            lab: {"precision": float(p[i]), "recall": float(r[i]), "f1": float(f[i]), "support": int(s[i])}
            for i, lab in enumerate(labels)
        },
        "labels": list(labels),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=idx).tolist(),
    }


def save_metrics(metrics: Dict, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)


def metrics_to_markdown(metrics: Dict, title: str) -> str:
    labels = metrics["labels"]
    lines = [
        f"### {title}",
        "",
        f"- n = {metrics['n']}",
        f"- **Macro-F1 = {metrics['macro_f1']:.4f}**",
        f"- Weighted-F1 = {metrics['weighted_f1']:.4f}",
        f"- Accuracy = {metrics['accuracy']:.4f}",
        "",
        "| class | precision | recall | F1 | support |",
        "|---|---:|---:|---:|---:|",
    ]
    for lab in labels:
        c = metrics["per_class"][lab]
        lines.append(f"| {lab} | {c['precision']:.4f} | {c['recall']:.4f} | {c['f1']:.4f} | {c['support']} |")
    lines += ["", "Confusion matrix (rows = gold, columns = predicted):", ""]
    lines.append("| gold \\ pred | " + " | ".join(labels) + " |")
    lines.append("|---|" + "---:|" * len(labels))
    for lab, row in zip(labels, metrics["confusion_matrix"]):
        lines.append(f"| {lab} | " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines) + "\n"
