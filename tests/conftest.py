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


TINY_VOCAB = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", "text", "hello", "oh", "no", "yes", "what", "!", "?", "."] + [
    str(i) for i in range(20)] + ["word"]


@pytest.fixture(scope="session")
def tiny_encoder(tmp_path_factory):
    """A randomly initialised 1-layer DistilBERT + tokenizer saved to disk (no download)."""
    import torch
    from transformers import DistilBertConfig, DistilBertModel, DistilBertTokenizerFast

    d = tmp_path_factory.mktemp("tiny_distilbert")
    (d / "vocab.txt").write_text("\n".join(TINY_VOCAB) + "\n", encoding="utf-8")
    DistilBertTokenizerFast(vocab_file=str(d / "vocab.txt")).save_pretrained(d)
    torch.manual_seed(0)
    cfg = DistilBertConfig(vocab_size=len(TINY_VOCAB), dim=32, n_layers=1, n_heads=2, hidden_dim=64,
                           max_position_embeddings=512)
    DistilBertModel(cfg).save_pretrained(d)
    return str(d)


def write_tiny_processed(root: Path, dataset="meld", dialogues=4, turns=5):
    """Small processed split files in the unified format."""
    from data.loaders import LABELS, processed_path, write_records

    labels = LABELS[dataset]
    speakers = ["A", "B", "A", "C", "B"]
    for split in ("train", "dev", "test"):
        recs = [make_record(f"dia{d}", t, [speakers[t % len(speakers)]], f"text {t} word {d} {'!' if t % 2 else '?'}",
                            label=labels[(d + t) % len(labels)], split=split, dataset=dataset)
                for d in range(dialogues) for t in range(turns)]
        write_records(recs, processed_path(root, dataset, split))
    return root


@pytest.fixture
def processed_dir():
    """Real processed data, if prepare_data.py has been run."""
    path = Path(__file__).resolve().parents[1] / "data" / "processed"
    if not (path / "meld" / "train.jsonl").exists():
        pytest.skip("data/processed not found; run prepare_data.py")
    return path
