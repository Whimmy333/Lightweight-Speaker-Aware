"""Fixed per-utterance prediction file format shared by all models.

Columns: dataset, split, dialogue_id, utterance_id, turn_index, speaker_ids (JSON list),
text, label (gold), pred, then one ``prob_<label>`` column per class in label order.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Sequence

import numpy as np
import pandas as pd

ID_COLUMNS = ["dataset", "split", "dialogue_id", "utterance_id", "turn_index", "speaker_ids", "text", "label", "pred"]


def predictions_frame(
    records: Sequence[dict],
    pred_ids: Sequence[int],
    labels: List[str],
    probs: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    if len(records) != len(pred_ids):
        raise ValueError(f"{len(records)} records but {len(pred_ids)} predictions")
    df = pd.DataFrame(
        {
            "dataset": [r["dataset"] for r in records],
            "split": [r["split"] for r in records],
            "dialogue_id": [r["dialogue_id"] for r in records],
            "utterance_id": [r["utterance_id"] for r in records],
            "turn_index": [r["turn_index"] for r in records],
            "speaker_ids": [json.dumps(r["speaker_ids"], ensure_ascii=False) for r in records],
            "text": [r["text"] for r in records],
            "label": [r["label"] for r in records],
            "pred": [labels[int(p)] for p in pred_ids],
        }
    )
    if probs is not None:
        probs = np.asarray(probs)
        for i, lab in enumerate(labels):
            df[f"prob_{lab}"] = probs[:, i]
    return df


FUSION_WEIGHT_COLUMNS = [
    "dataset", "split", "dialogue_id", "utterance_id", "turn_index", "label", "pred", "source_mode",
    "n_same", "n_other",
    "avail_current", "avail_same", "avail_other", "avail_history",
    "w_current", "w_same", "w_other", "w_history",
]


def fusion_weights_frame(records: Sequence[dict], contexts: Sequence, pred_ids: Sequence[int], labels: List[str],
                         weights: np.ndarray, avail: np.ndarray, speaker_split: bool) -> pd.DataFrame:
    """Per-utterance fusion weights in one fixed layout for every fusion model.

    speaker_split models fill current/same/other and leave *_history empty; merged
    models fill current/history and leave *_same/*_other empty. A weight of 0 with
    avail=0 means the source was missing and masked out.
    """
    n = len(records)
    nan = np.full(n, np.nan)
    if speaker_split:
        av = {"current": avail[:, 0], "same": avail[:, 1], "other": avail[:, 2], "history": nan}
        w = {"current": weights[:, 0], "same": weights[:, 1], "other": weights[:, 2], "history": nan}
    else:
        av = {"current": avail[:, 0], "same": nan, "other": nan, "history": avail[:, 1]}
        w = {"current": weights[:, 0], "same": nan, "other": nan, "history": weights[:, 1]}
    df = pd.DataFrame({
        "dataset": [r["dataset"] for r in records],
        "split": [r["split"] for r in records],
        "dialogue_id": [r["dialogue_id"] for r in records],
        "utterance_id": [r["utterance_id"] for r in records],
        "turn_index": [r["turn_index"] for r in records],
        "label": [r["label"] for r in records],
        "pred": [labels[int(p)] for p in pred_ids],
        "source_mode": "speaker_split" if speaker_split else "merged",
        "n_same": [len(c.same_speaker_texts) for c in contexts],
        "n_other": [len(c.other_speaker_texts) for c in contexts],
    })
    for k in ("current", "same", "other", "history"):
        df[f"avail_{k}"] = av[k]
    for k in ("current", "same", "other", "history"):
        df[f"w_{k}"] = w[k]
    return df[FUSION_WEIGHT_COLUMNS]


def save_predictions(df: pd.DataFrame, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
