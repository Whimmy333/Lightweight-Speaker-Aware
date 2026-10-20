"""Loaders that turn the official MELD / EmoryNLP files into one unified record format.

Every record is a dict with exactly the keys in ``RECORD_FIELDS``:

    dataset      "meld" | "emorynlp"
    split        "train" | "dev" | "test"   (official splits, never re-drawn)
    dialogue_id  MELD: "dia<Dialogue_ID>"; EmoryNLP: scene id, e.g. "s01_e15_c01"
    utterance_id MELD: "dia<D>_utt<U>" (original ids, gaps kept); EmoryNLP: original id
    turn_index   0-based chronological position inside the dialogue
    speaker_ids  list[str]; multi-speaker utterances keep every speaker
    text         transcript with only outer whitespace stripped (punctuation,
                 casing and negation untouched)
    label        lower-cased gold emotion (training/evaluation target only)

``turn_index`` is an addition to the fields listed in the proposal: MELD utterance
ids have gaps where the authors dropped utterances, so an explicit position makes the
chronological order unambiguous for context construction.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

DATASETS = ("meld", "emorynlp")
SPLITS = ("train", "dev", "test")

RECORD_FIELDS = (
    "dataset",
    "split",
    "dialogue_id",
    "utterance_id",
    "turn_index",
    "speaker_ids",
    "text",
    "label",
)

# Fixed label order (alphabetical) -> class index. Never derived from data.
LABELS: Dict[str, List[str]] = {
    "meld": ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"],
    "emorynlp": ["joyful", "mad", "neutral", "peaceful", "powerful", "sad", "scared"],
}

RAW_FILES: Dict[str, Dict[str, str]] = {
    "meld": {
        "train": "train_sent_emo.csv",
        "dev": "dev_sent_emo.csv",
        "test": "test_sent_emo.csv",
    },
    "emorynlp": {
        "train": "emotion-detection-trn.json",
        "dev": "emotion-detection-dev.json",
        "test": "emotion-detection-tst.json",
    },
}

# Published utterance counts from the proposal; checked during the data audit.
EXPECTED_COUNTS: Dict[str, Dict[str, int]] = {
    "meld": {"train": 9989, "dev": 1109, "test": 2610},
    "emorynlp": {"train": 9934, "dev": 1344, "test": 1328},
}

_MELD_COLUMNS = ("Utterance", "Speaker", "Emotion", "Dialogue_ID", "Utterance_ID")


def label_to_id(dataset: str) -> Dict[str, int]:
    return {lab: i for i, lab in enumerate(LABELS[dataset])}


def parse_meld_speakers(raw: str) -> List[str]:
    """MELD writes joint turns as "Joey and Chandler"; split them so the
    same-speaker relation can use overlap. Group names such as "All" stay literal."""
    parts = [p.strip() for p in raw.strip().split(" and ")]
    return [p for p in parts if p]


def _check_label(dataset: str, label: str, where: str) -> str:
    if label not in LABELS[dataset]:
        raise ValueError(f"{where}: unknown {dataset} label {label!r}")
    return label


def load_meld_split(path: Path, split: str) -> List[dict]:
    # keep_default_na=False: utterances such as "None" or "NA" must stay text.
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")
    missing = [c for c in _MELD_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing MELD columns {missing}")
    df["dia_num"] = df["Dialogue_ID"].astype(int)
    df["utt_num"] = df["Utterance_ID"].astype(int)
    if df.duplicated(["dia_num", "utt_num"]).any():
        raise ValueError(f"{path}: duplicate (Dialogue_ID, Utterance_ID) pairs")
    df = df.sort_values(["dia_num", "utt_num"], kind="stable")

    records = []
    for dia, group in df.groupby("dia_num", sort=True):
        for turn, row in enumerate(group.itertuples(index=False)):
            records.append(
                {
                    "dataset": "meld",
                    "split": split,
                    "dialogue_id": f"dia{dia}",
                    "utterance_id": f"dia{dia}_utt{row.utt_num}",
                    "turn_index": turn,
                    "speaker_ids": parse_meld_speakers(row.Speaker),
                    "text": row.Utterance.strip(),
                    "label": _check_label("meld", row.Emotion.strip().lower(), f"{path} dia{dia}_utt{row.utt_num}"),
                }
            )
    return records


def load_emorynlp_split(path: Path, split: str) -> List[dict]:
    with open(path, encoding="utf-8") as f:
        season = json.load(f)
    records = []
    seen_scenes = set()
    for episode in season["episodes"]:
        for scene in episode["scenes"]:
            scene_id = scene["scene_id"]
            if scene_id in seen_scenes:
                raise ValueError(f"{path}: duplicate scene id {scene_id}")
            seen_scenes.add(scene_id)
            # Utterances are stored in broadcast order; keep it.
            for turn, utt in enumerate(scene["utterances"]):
                speakers = []
                for s in utt["speakers"]:
                    s = s.strip()
                    if s and s not in speakers:
                        speakers.append(s)
                records.append(
                    {
                        "dataset": "emorynlp",
                        "split": split,
                        "dialogue_id": scene_id,
                        "utterance_id": utt["utterance_id"],
                        "turn_index": turn,
                        "speaker_ids": speakers,
                        "text": utt["transcript"].strip(),
                        "label": _check_label("emorynlp", utt["emotion"].strip().lower(), f"{path} {utt['utterance_id']}"),
                    }
                )
    return records


_LOADERS = {"meld": load_meld_split, "emorynlp": load_emorynlp_split}


def raw_path(raw_dir: Path, dataset: str, split: str) -> Path:
    return Path(raw_dir) / dataset / RAW_FILES[dataset][split]


def load_raw_split(raw_dir: Path, dataset: str, split: str) -> List[dict]:
    return _LOADERS[dataset](raw_path(raw_dir, dataset, split), split)


def processed_path(processed_dir: Path, dataset: str, split: str) -> Path:
    return Path(processed_dir) / dataset / f"{split}.jsonl"


def write_records(records: Iterable[dict], path: Path) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps({k: rec[k] for k in RECORD_FIELDS}, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_records(path: Path) -> List[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_split(processed_dir: Path, dataset: str, split: str) -> List[dict]:
    """Read one processed split written by prepare_data.py."""
    path = processed_path(processed_dir, dataset, split)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found; run `python prepare_data.py` first")
    return read_records(path)


def records_to_frame(records: List[dict]) -> pd.DataFrame:
    return pd.DataFrame(records, columns=list(RECORD_FIELDS))
