from collections import defaultdict

import pytest

from data.loaders import (
    DATASETS,
    EXPECTED_COUNTS,
    LABELS,
    RECORD_FIELDS,
    SPLITS,
    load_emorynlp_split,
    load_meld_split,
    load_split,
    parse_meld_speakers,
    read_records,
    write_records,
)
from tests.conftest import write_emorynlp_json, write_meld_csv


@pytest.fixture
def meld_records(tmp_path):
    rows = [  # deliberately out of order, with a gap (utt 2 missing) in dialogue 0
        ("Second line.", "Monica", "joy", 0, 1),
        ("Dialogue one starts.", "Ross", "neutral", 1, 0),
        ("  Oh my God, he’s lost it. I don't know!  ", "Phoebe", "sadness", 0, 0),
        ("None", "Joey and Chandler", "surprise", 0, 3),
        ("NA", "All", "anger", 1, 1),
    ]
    return load_meld_split(write_meld_csv(tmp_path / "train_sent_emo.csv", rows), "train")


def test_meld_record_fields(meld_records):
    assert len(meld_records) == 5
    for r in meld_records:
        assert tuple(r.keys()) == RECORD_FIELDS
        assert r["dataset"] == "meld" and r["split"] == "train"
        assert isinstance(r["speaker_ids"], list) and isinstance(r["turn_index"], int)
        assert r["label"] in LABELS["meld"]


def test_meld_chronological_order_and_gaps(meld_records):
    dia0 = [r for r in meld_records if r["dialogue_id"] == "dia0"]
    assert [r["utterance_id"] for r in dia0] == ["dia0_utt0", "dia0_utt1", "dia0_utt3"]
    assert [r["turn_index"] for r in dia0] == [0, 1, 2]
    dia1 = [r for r in meld_records if r["dialogue_id"] == "dia1"]
    assert [r["turn_index"] for r in dia1] == [0, 1]  # turn index restarts per dialogue


def test_meld_text_preserved(meld_records):
    first = meld_records[0]
    # Punctuation, negation, curly apostrophe and casing kept; only outer whitespace removed.
    assert first["text"] == "Oh my God, he’s lost it. I don't know!"


def test_meld_na_like_text_stays_text(meld_records):
    texts = {r["utterance_id"]: r["text"] for r in meld_records}
    assert texts["dia0_utt3"] == "None"
    assert texts["dia1_utt1"] == "NA"


def test_meld_speakers(meld_records):
    spk = {r["utterance_id"]: r["speaker_ids"] for r in meld_records}
    assert spk["dia0_utt3"] == ["Joey", "Chandler"]
    assert spk["dia1_utt1"] == ["All"]
    assert parse_meld_speakers(" Ross ") == ["Ross"]


def test_meld_rejects_unknown_label(tmp_path):
    path = write_meld_csv(tmp_path / "x.csv", [("Hi.", "Ross", "happy", 0, 0)])
    with pytest.raises(ValueError, match="unknown meld label"):
        load_meld_split(path, "train")


def test_meld_rejects_duplicate_ids(tmp_path):
    path = write_meld_csv(tmp_path / "x.csv", [("Hi.", "Ross", "joy", 0, 0), ("Hey.", "Rachel", "joy", 0, 0)])
    with pytest.raises(ValueError, match="duplicate"):
        load_meld_split(path, "train")


@pytest.fixture
def emorynlp_records(tmp_path):
    scenes = {
        "s01_e02_c01": [
            (["Rachel Green"], "Coffee.", "Neutral"),
            (["Monica Geller", "Phoebe Buffay", "Monica Geller"], "We're not going!", "Mad"),
            (["Ross Geller"], " Oh... ", "Sad"),
        ],
        "s01_e02_c02": [(["Joey Tribbiani"], "How you doin'?", "Joyful")],
    }
    return load_emorynlp_split(write_emorynlp_json(tmp_path / "emotion-detection-dev.json", scenes), "dev")


def test_emorynlp_records(emorynlp_records):
    assert [tuple(r.keys()) for r in emorynlp_records] == [RECORD_FIELDS] * 4
    assert [r["utterance_id"] for r in emorynlp_records] == [
        "s01_e02_c01_u001", "s01_e02_c01_u002", "s01_e02_c01_u003", "s01_e02_c02_u001"]
    assert [r["turn_index"] for r in emorynlp_records] == [0, 1, 2, 0]
    assert [r["label"] for r in emorynlp_records] == ["neutral", "mad", "sad", "joyful"]
    assert emorynlp_records[1]["speaker_ids"] == ["Monica Geller", "Phoebe Buffay"]  # de-duplicated, order kept
    assert emorynlp_records[1]["text"] == "We're not going!"
    assert emorynlp_records[2]["text"] == "Oh..."
    assert {r["dialogue_id"] for r in emorynlp_records} == {"s01_e02_c01", "s01_e02_c02"}


def test_jsonl_roundtrip(tmp_path, emorynlp_records):
    path = tmp_path / "out" / "dev.jsonl"
    assert write_records(emorynlp_records, path) == len(emorynlp_records)
    assert read_records(path) == emorynlp_records


def test_real_processed_data(processed_dir):
    for ds in DATASETS:
        for sp in SPLITS:
            recs = load_split(processed_dir, ds, sp)
            assert len(recs) == EXPECTED_COUNTS[ds][sp]
            assert len({r["utterance_id"] for r in recs}) == len(recs)
            assert all(r["label"] in LABELS[ds] and r["split"] == sp for r in recs)
            turns = defaultdict(list)
            for r in recs:
                turns[r["dialogue_id"]].append(r["turn_index"])
            assert all(sorted(t) == list(range(len(t))) for t in turns.values())
