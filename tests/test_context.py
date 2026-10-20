import dataclasses
import random

import pytest

from data.context import build_contexts, is_same_speaker
from data.loaders import load_split
from tests.conftest import make_record

SPEAKERS = ["A", "B", "A", "C", "A", "B", "A"]


@pytest.fixture
def dialogue():
    return [make_record("dia0", t, [s], f"text {t}") for t, s in enumerate(SPEAKERS)]


def test_first_turn_has_no_history(dialogue):
    for k in (1, 3, 5):
        ctx = build_contexts(dialogue, k)[0]
        assert ctx.history == ()
        assert ctx.same_speaker_texts == [] and ctx.other_speaker_texts == []
        assert ctx.source_mask == (True, False, False)
        assert ctx.text == "text 0"


@pytest.mark.parametrize("k", [1, 3, 5])
def test_window_size_and_order(dialogue, k):
    for t, ctx in enumerate(build_contexts(dialogue, k)):
        expected = list(range(max(0, t - k), t))
        assert ctx.history_texts == [f"text {i}" for i in expected]  # oldest first
        assert [h.offset for h in ctx.history] == [t - i for i in expected]


def test_same_and_other_speaker_split(dialogue):
    ctx = build_contexts(dialogue, 5)[6]  # speaker A; window = turns 1..5 = B A C A B
    assert ctx.same_speaker_texts == ["text 2", "text 4"]
    assert ctx.other_speaker_texts == ["text 1", "text 3", "text 5"]
    assert ctx.source_mask == (True, True, True)
    ctx1 = build_contexts(dialogue, 1)[6]  # only turn 5 (B)
    assert ctx1.same_speaker_texts == [] and ctx1.other_speaker_texts == ["text 5"]
    assert ctx1.source_mask == (True, False, True)


def test_only_same_speaker_history():
    recs = [make_record("d", 0, ["A"], "x"), make_record("d", 1, ["A"], "y")]
    assert build_contexts(recs, 3)[1].source_mask == (True, True, False)


def test_multi_speaker_overlap():
    recs = [
        make_record("d", 0, ["Joey", "Chandler"], "both"),
        make_record("d", 1, ["Monica"], "m"),
        make_record("d", 2, ["Joey"], "j"),
        make_record("d", 3, ["Monica", "Phoebe"], "mp"),
    ]
    ctx = build_contexts(recs, 5)
    assert ctx[2].same_speaker_texts == ["both"] and ctx[2].other_speaker_texts == ["m"]
    assert ctx[3].same_speaker_texts == ["m"] and ctx[3].other_speaker_texts == ["both", "j"]
    assert is_same_speaker(["All"], ["Ross"]) is False
    assert is_same_speaker([], ["Ross"]) is False


def test_no_crossing_dialogue_or_split_boundaries():
    # MELD dialogue ids restart per split, so "dia0" exists in train and dev.
    recs = [
        make_record("dia0", 0, ["A"], "train a0"),
        make_record("dia0", 1, ["B"], "train a1"),
        make_record("dia1", 0, ["A"], "train b0"),
        make_record("dia0", 0, ["A"], "dev a0", split="dev"),
        make_record("dia0", 1, ["A"], "dev a1", split="dev"),
    ]
    ctx = build_contexts(recs, 5)
    assert ctx[2].history == ()
    assert ctx[3].history == ()
    assert ctx[4].history_texts == ["dev a0"]


def test_gold_labels_never_in_context(dialogue):
    for i, r in enumerate(dialogue):
        r["label"] = f"GOLD_LABEL_SENTINEL_{i}"
    for k in (1, 3, 5):
        for ctx in build_contexts(dialogue, k):
            assert "GOLD_LABEL_SENTINEL" not in repr(dataclasses.asdict(ctx))
            assert not hasattr(ctx, "label")
            assert all(not hasattr(h, "label") for h in ctx.history)


def test_input_order_does_not_matter(dialogue):
    shuffled = dialogue[:]
    random.Random(0).shuffle(shuffled)
    ref = {c.utterance_id: c for c in build_contexts(dialogue, 3)}
    out = build_contexts(shuffled, 3)
    assert [c.utterance_id for c in out] == [r["utterance_id"] for r in shuffled]  # aligned to input
    assert all(c == ref[c.utterance_id] for c in out)


def test_zero_turns_gives_empty_history(dialogue):
    assert all(c.history == () for c in build_contexts(dialogue, 0))


@pytest.mark.parametrize("bad", [-1, 2.5, "3"])
def test_invalid_num_turns(dialogue, bad):
    with pytest.raises(ValueError):
        build_contexts(dialogue, bad)


def test_duplicate_turn_index_raises():
    recs = [make_record("d", 0, ["A"], "x"), make_record("d", 0, ["B"], "y")]
    recs[1]["utterance_id"] = "other"
    with pytest.raises(ValueError, match="duplicate turn_index"):
        build_contexts(recs, 1)


def test_real_meld_contexts(processed_dir):
    recs = load_split(processed_dir, "meld", "train")
    by_id = {r["utterance_id"]: r for r in recs}
    for k in (1, 3, 5):
        for r, ctx in zip(recs, build_contexts(recs, k)):
            assert len(ctx.history) == min(k, r["turn_index"])
            for h in ctx.history:
                hr = by_id[h.utterance_id]
                assert hr["dialogue_id"] == r["dialogue_id"]
                assert hr["turn_index"] == r["turn_index"] - h.offset
