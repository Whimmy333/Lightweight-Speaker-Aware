
"""Loaders that turn official MELD / EmoryNLP / DailyDialog files into one unified record format.

Every record is a dict with exactly the keys in ``RECORD_FIELDS``:

    dataset      "meld" | "emorynlp" | "dailydialog"
    split        "train" | "dev" | "test" (official splits, never re-drawn)
    dialogue_id  stable dialogue identifier within the dataset split
    utterance_id stable utterance identifier
    turn_index   0-based chronological position inside the dialogue
    speaker_ids  list[str]; multi-speaker utterances keep every known speaker
    text         transcript with only outer whitespace stripped
    label        lower-cased gold emotion (training/evaluation target only)

DailyDialog does not provide explicit speaker IDs in its standard text release,
so its records use an empty speaker_ids list rather than inventing speakers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

DATASETS = ("meld", "emorynlp", "dailydialog")
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
    "dailydialog": [
        "anger", "disgust", "fear", "happiness",
        "no_emotion", "sadness", "surprise",
    ],
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
    "dailydialog": {
        "train": "dialogues_train.txt",
        "dev": "dialogues_validation.txt",
        "test": "dialogues_test.txt",
    },
}

# Published utterance counts; checked during the data audit.
EXPECTED_COUNTS: Dict[str, Dict[str, int]] = {
    "meld": {"train": 9989, "dev": 1109, "test": 2610},
    "emorynlp": {"train": 9934, "dev": 1344, "test": 1328},
    "dailydialog": {"train": 87170, "dev": 8069, "test": 7740},
}

_MELD_COLUMNS = ("Utterance", "Speaker", "Emotion", "Dialogue_ID", "Utterance_ID")

# DailyDialog's published integer emotion IDs.
_DAILYDIALOG_EMOTION_LABELS = {
    0: "no_emotion",
    1: "anger",
    2: "disgust",
    3: "fear",
    4: "happiness",
    5: "sadness",
    6: "surprise",
}


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
                    "label": _check_label(
                        "meld",
                        row.Emotion.strip().lower(),
                        f"{path} dia{dia}_utt{row.utt_num}",
                    ),
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
                        "label": _check_label(
                            "emorynlp",
                            utt["emotion"].strip().lower(),
                            f"{path} {utt['utterance_id']}",
                        ),
                    }
                )
    return records


def load_dailydialog_split(path: Path, split: str) -> List[dict]:
    """Load DailyDialog text and its matching emotion-label file.

    The two files are expected in the same directory. For example:
        dialogues_train.txt
        dialogues_emotion_train.txt

    Each line represents one dialogue. Utterances are separated by "__eou__";
    the corresponding emotion line contains one integer label per utterance.
    """
    path = Path(path)
    emotion_path = path.with_name(
        path.name.replace("dialogues_", "dialogues_emotion_", 1)
    )

    if not path.exists():
        raise FileNotFoundError(path)
    if not emotion_path.exists():
        raise FileNotFoundError(emotion_path)

    dialogue_lines = path.read_text(encoding="utf-8").splitlines()
    emotion_lines = emotion_path.read_text(encoding="utf-8").splitlines()

    if len(dialogue_lines) != len(emotion_lines):
        raise ValueError(
            f"{path}: dialogue/emotion line-count mismatch "
            f"({len(dialogue_lines)} vs {len(emotion_lines)})"
        )

    records = []

    for dialogue_idx, (dialogue_line, emotion_line) in enumerate(
        zip(dialogue_lines, emotion_lines), start=1
    ):
        dialogue_id = f"dd_{split}_{dialogue_idx:05d}"

        # __eou__ separates utterances. Remove an optional trailing delimiter.
        utterances = [
            part.strip() for part in dialogue_line.strip().split("__eou__")
        ]
        if utterances and not utterances[-1]:
            utterances.pop()

        if not utterances or any(not text for text in utterances):
            raise ValueError(
                f"{path}: empty utterance in dialogue {dialogue_id}"
            )

        try:
            emotion_ids = [int(value) for value in emotion_line.split()]
        except ValueError as exc:
            raise ValueError(
                f"{emotion_path}: invalid emotion ID in dialogue {dialogue_id}"
            ) from exc

        if len(utterances) != len(emotion_ids):
            # Known anomaly in the original DailyDialog training split:
            # dialogue 7852 has 12 text utterances but only 11 labels.
            # The published training split contains 87,170 utterances.
            # Do not invent a label for the unmatched final text utterance.
            known_extra_turn = (
                split == "train"
                and dialogue_idx == 7852
                and len(utterances) == 12
                and len(emotion_ids) == 11
                and all(label_id == 0 for label_id in emotion_ids)
                and utterances[-1].strip() == "OK , let's go and ask ."
            )

            if known_extra_turn:
                print(
                    "WARNING: DailyDialog train dialogue 7852 has "
                    "12 utterances but 11 labels. Excluding the final "
                    "unlabelled utterance: "
                    f"{utterances[-1]!r}"
                )
                utterances = utterances[:len(emotion_ids)]
            else:
                raise ValueError(
                    f"{dialogue_id}: {len(utterances)} utterances but "
                    f"{len(emotion_ids)} emotion labels"
                )

        for turn_idx, (text, emotion_id) in enumerate(
            zip(utterances, emotion_ids)
        ):
            if emotion_id not in _DAILYDIALOG_EMOTION_LABELS:
                raise ValueError(
                    f"{emotion_path}: invalid emotion ID {emotion_id} in "
                    f"{dialogue_id}, turn {turn_idx}"
                )

            label = _DAILYDIALOG_EMOTION_LABELS[emotion_id]
            records.append(
                {
                    "dataset": "dailydialog",
                    "split": split,
                    "dialogue_id": dialogue_id,
                    "utterance_id": f"{dialogue_id}_utt{turn_idx}",
                    "turn_index": turn_idx,
                    "speaker_ids": [],
                    "text": text,
                    "label": _check_label(
                        "dailydialog",
                        label,
                        f"{dialogue_id}, turn {turn_idx}",
                    ),
                }
            )

    return records


_LOADERS = {
    "meld": load_meld_split,
    "emorynlp": load_emorynlp_split,
    "dailydialog": load_dailydialog_split,
}


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
