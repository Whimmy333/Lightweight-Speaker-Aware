
from collections import defaultdict

import pytest

from data.loaders import (
    DATASETS,
    EXPECTED_COUNTS,
    LABELS,
    RECORD_FIELDS,
    SPLITS,
    load_dailydialog_split,
    load_emorynlp_split,
    load_meld_split,
    load_split,
    parse_meld_speakers,
    processed_path,
    read_records,
    write_records,
)
from tests.conftest import write_emorynlp_json, write_meld_csv


@pytest.fixture
def meld_records(tmp_path):
    rows = [
        ("Second line.", "Monica", "joy", 0, 1),
        ("Dialogue one starts.", "Ross", "neutral", 1, 0),
        ("  Oh my God, he’s lost it. I don't know!  ", "Phoebe", "sadness", 0, 0),
        ("None", "Joey and Chandler", "surprise", 0, 3),
        ("NA", "All", "anger", 1, 1),
    ]
    return load_meld_split(
        write_meld_csv(tmp_path / "train_sent_emo.csv", rows), "train"
    )


def test_meld_record_fields(meld_records):
    assert len(meld_records) == 5
    for record in meld_records:
        assert tuple(record.keys()) == RECORD_FIELDS
        assert record["dataset"] == "meld"
        assert record["split"] == "train"
        assert isinstance(record["speaker_ids"], list)
        assert isinstance(record["turn_index"], int)
        assert record["label"] in LABELS["meld"]


def test_meld_chronological_order_and_gaps(meld_records):
    dia0 = [r for r in meld_records if r["dialogue_id"] == "dia0"]
    assert [r["utterance_id"] for r in dia0] == [
        "dia0_utt0", "dia0_utt1", "dia0_utt3"
    ]
    assert [r["turn_index"] for r in dia0] == [0, 1, 2]

    dia1 = [r for r in meld_records if r["dialogue_id"] == "dia1"]
    assert [r["turn_index"] for r in dia1] == [0, 1]


def test_meld_text_preserved(meld_records):
    first = meld_records[0]
    assert first["text"] == "Oh my God, he’s lost it. I don't know!"


def test_meld_na_like_text_stays_text(meld_records):
    texts = {r["utterance_id"]: r["text"] for r in meld_records}
    assert texts["dia0_utt3"] == "None"
    assert texts["dia1_utt1"] == "NA"


def test_meld_speakers(meld_records):
    speakers = {r["utterance_id"]: r["speaker_ids"] for r in meld_records}
    assert speakers["dia0_utt3"] == ["Joey", "Chandler"]
    assert speakers["dia1_utt1"] == ["All"]
    assert parse_meld_speakers(" Ross ") == ["Ross"]


def test_meld_rejects_unknown_label(tmp_path):
    path = write_meld_csv(
        tmp_path / "x.csv",
        [("Hi.", "Ross", "happy", 0, 0)],
    )
    with pytest.raises(ValueError, match="unknown meld label"):
        load_meld_split(path, "train")


def test_meld_rejects_duplicate_ids(tmp_path):
    path = write_meld_csv(
        tmp_path / "x.csv",
        [
            ("Hi.", "Ross", "joy", 0, 0),
            ("Hey.", "Rachel", "joy", 0, 0),
        ],
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_meld_split(path, "train")


@pytest.fixture
def emorynlp_records(tmp_path):
    scenes = {
        "s01_e02_c01": [
            (["Rachel Green"], "Coffee.", "Neutral"),
            (
                ["Monica Geller", "Phoebe Buffay", "Monica Geller"],
                "We're not going!",
                "Mad",
            ),
            (["Ross Geller"], " Oh... ", "Sad"),
        ],
        "s01_e02_c02": [
            (["Joey Tribbiani"], "How you doin'?", "Joyful")
        ],
    }
    path = write_emorynlp_json(
        tmp_path / "emotion-detection-dev.json", scenes
    )
    return load_emorynlp_split(path, "dev")


def test_emorynlp_records(emorynlp_records):
    assert [tuple(r.keys()) for r in emorynlp_records] == [RECORD_FIELDS] * 4
    assert [r["utterance_id"] for r in emorynlp_records] == [
        "s01_e02_c01_u001",
        "s01_e02_c01_u002",
        "s01_e02_c01_u003",
        "s01_e02_c02_u001",
    ]
    assert [r["turn_index"] for r in emorynlp_records] == [0, 1, 2, 0]
    assert [r["label"] for r in emorynlp_records] == [
        "neutral", "mad", "sad", "joyful"
    ]
    assert emorynlp_records[1]["speaker_ids"] == [
        "Monica Geller", "Phoebe Buffay"
    ]
    assert emorynlp_records[1]["text"] == "We're not going!"
    assert emorynlp_records[2]["text"] == "Oh..."
    assert {r["dialogue_id"] for r in emorynlp_records} == {
        "s01_e02_c01", "s01_e02_c02"
    }


def _write_dailydialog_files(directory, dialogues, emotions, filename="train"):
    """Write a tiny DailyDialog-style pair of aligned files."""
    directory.mkdir(parents=True, exist_ok=True)
    text_path = directory / f"dialogues_{filename}.txt"
    emotion_path = directory / f"dialogues_emotion_{filename}.txt"

    text_path.write_text(
        "\n".join(dialogues) + "\n",
        encoding="utf-8",
    )
    emotion_path.write_text(
        "\n".join(emotions) + "\n",
        encoding="utf-8",
    )
    return text_path


def test_dailydialog_record_fields_labels_and_order(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        [
            "Hello there.__eou__How are you?__eou__",
            "Really?__eou__That is bad.__eou__",
        ],
        [
            "4 0",
            "1 5",
        ],
    )

    records = load_dailydialog_split(path, "train")

    assert len(records) == 4
    assert all(tuple(r.keys()) == RECORD_FIELDS for r in records)
    assert all(r["dataset"] == "dailydialog" for r in records)
    assert all(r["split"] == "train" for r in records)

    assert [r["turn_index"] for r in records] == [0, 1, 0, 1]
    assert [r["dialogue_id"] for r in records] == [
        "dd_train_00001",
        "dd_train_00001",
        "dd_train_00002",
        "dd_train_00002",
    ]
    assert [r["text"] for r in records] == [
        "Hello there.",
        "How are you?",
        "Really?",
        "That is bad.",
    ]
    assert [r["label"] for r in records] == [
        "happiness",
        "no_emotion",
        "anger",
        "sadness",
    ]

    # The standard DailyDialog release does not provide explicit speaker IDs.
    assert all(r["speaker_ids"] == [] for r in records)
    assert all(r["label"] in LABELS["dailydialog"] for r in records)


def test_dailydialog_label_id_mapping(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        [
            "A.__eou__B.__eou__C.__eou__D.__eou__"
            "E.__eou__F.__eou__G.__eou__"
        ],
        ["0 1 2 3 4 5 6"],
    )

    records = load_dailydialog_split(path, "train")

    assert [r["label"] for r in records] == [
        "no_emotion",
        "anger",
        "disgust",
        "fear",
        "happiness",
        "sadness",
        "surprise",
    ]


def test_dailydialog_accepts_missing_trailing_delimiter(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        ["Hello.__eou__Goodbye."],
        ["4 0"],
    )

    records = load_dailydialog_split(path, "train")

    assert [r["text"] for r in records] == ["Hello.", "Goodbye."]
    assert len(records) == 2


def test_dailydialog_rejects_missing_emotion_file(tmp_path):
    path = tmp_path / "dialogues_train.txt"
    path.write_text("Hello.__eou__\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="dialogues_emotion_train"):
        load_dailydialog_split(path, "train")


def test_dailydialog_rejects_dialogue_emotion_line_mismatch(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        ["Hello.__eou__", "Goodbye.__eou__"],
        ["4"],
    )

    with pytest.raises(ValueError, match="line-count mismatch"):
        load_dailydialog_split(path, "train")


def test_dailydialog_rejects_utterance_emotion_mismatch(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        ["Hello.__eou__How are you?__eou__"],
        ["4"],
    )

    with pytest.raises(ValueError, match="utterances but"):
        load_dailydialog_split(path, "train")


def test_dailydialog_rejects_invalid_emotion_id(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        ["Hello.__eou__"],
        ["7"],
    )

    with pytest.raises(ValueError, match="invalid emotion ID"):
        load_dailydialog_split(path, "train")


def test_jsonl_roundtrip(tmp_path, emorynlp_records):
    path = tmp_path / "out" / "dev.jsonl"
    assert write_records(emorynlp_records, path) == len(emorynlp_records)
    assert read_records(path) == emorynlp_records


def test_dailydialog_jsonl_roundtrip(tmp_path):
    path = _write_dailydialog_files(
        tmp_path,
        ["Hello.__eou__Goodbye.__eou__"],
        ["4 0"],
    )
    records = load_dailydialog_split(path, "train")
    output_path = tmp_path / "processed" / "train.jsonl"

    assert write_records(records, output_path) == 2
    assert read_records(output_path) == records


def test_real_processed_data(processed_dir):
    # Keep the original real-data checks for the two existing datasets.
    # DailyDialog is tested separately so this test remains usable before
    # the new dataset has been downloaded and prepared.
    for dataset in ("meld", "emorynlp"):
        for split in SPLITS:
            records = load_split(processed_dir, dataset, split)
            assert len(records) == EXPECTED_COUNTS[dataset][split]
            assert len({r["utterance_id"] for r in records}) == len(records)
            assert all(
                r["label"] in LABELS[dataset] and r["split"] == split
                for r in records
            )

            turns = defaultdict(list)
            for record in records:
                turns[record["dialogue_id"]].append(record["turn_index"])

            assert all(
                sorted(indices) == list(range(len(indices)))
                for indices in turns.values()
            )


def test_real_dailydialog_processed_data(processed_dir):
    paths = [
        processed_path(processed_dir, "dailydialog", split)
        for split in SPLITS
    ]
    if not all(path.exists() for path in paths):
        pytest.skip("DailyDialog processed data not found yet")

    for split in SPLITS:
        records = load_split(processed_dir, "dailydialog", split)
        assert len(records) == EXPECTED_COUNTS["dailydialog"][split]
        assert len({r["utterance_id"] for r in records}) == len(records)
        assert all(
            r["dataset"] == "dailydialog"
            and r["split"] == split
            and r["label"] in LABELS["dailydialog"]
            and r["speaker_ids"] == []
            for r in records
        )

        turns = defaultdict(list)
        for record in records:
            turns[record["dialogue_id"]].append(record["turn_index"])

        assert all(
            sorted(indices) == list(range(len(indices)))
            for indices in turns.values()
        )
