import csv
import json
from pathlib import Path

import pytest

MELD_HEADER = ["Sr No.", "Utterance", "Speaker", "Emotion", "Sentiment", "Dialogue_ID", "Utterance_ID",
               "Season", "Episode", "StartTime", "EndTime"]


def write_meld_csv(path: Path, rows):
    """rows: (utterance, speaker, emotion, dialogue_id, utterance_id)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(MELD_HEADER)
        for i, (utt, spk, emo, dia, uid) in enumerate(rows, 1):
            w.writerow([i, utt, spk, emo, "neutral", dia, uid, 1, 1, "00:00:01,000", "00:00:02,000"])
    return path


def write_emorynlp_json(path: Path, scenes):
    """scenes: {scene_id: [(speakers, transcript, emotion), ...]}; one episode per scene prefix."""
    episodes = {}
    for scene_id, utts in scenes.items():
        ep = episodes.setdefault(scene_id[:7], {"episode_id": scene_id[:7], "scenes": []})
        ep["scenes"].append({
            "scene_id": scene_id,
            "utterances": [
                {"utterance_id": f"{scene_id}_u{i + 1:03d}", "speakers": spk, "transcript": text,
                 "tokens": [text.split()], "emotion": emo}
                for i, (spk, text, emo) in enumerate(utts)
            ],
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"season_id": "x", "episodes": list(episodes.values())}, f)
    return path


def make_record(dialogue_id, turn, speakers, text, label="neutral", split="train", dataset="meld"):
    return {
        "dataset": dataset,
        "split": split,
        "dialogue_id": dialogue_id,
        "utterance_id": f"{dialogue_id}_utt{turn}",
        "turn_index": turn,
        "speaker_ids": list(speakers),
        "text": text,
        "label": label,
    }


@pytest.fixture
def processed_dir():
    """Real processed data, if prepare_data.py has been run."""
    path = Path(__file__).resolve().parents[1] / "data" / "processed"
    if not (path / "meld" / "train.jsonl").exists():
        pytest.skip("data/processed not found; run prepare_data.py")
    return path
