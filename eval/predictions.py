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


def save_predictions(df: pd.DataFrame, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
