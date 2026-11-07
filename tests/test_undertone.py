"""Undertone front end (app/undertone_app.py) and its helpers (app/insights.py)."""

import numpy as np
import pytest

from app import core
from app.insights import COUPLE_CHATS, MOOD, chat_summary, chat_text, is_mine, speakers_in
from data.loaders import LABELS

APP = "app/undertone_app.py"
L = LABELS["meld"]


def _probs(labels):
    p = np.full((len(labels), len(L)), 0.01)
    for i, (lab, conf) in enumerate(labels):
        p[i, L.index(lab)] = conf
    return p


def test_every_meld_label_has_a_mood():
    assert set(MOOD) == set(L)


def test_example_chats_round_trip_and_stay_unlabelled():
    for name, turns in COUPLE_CHATS.items():
        recs = core.dialogue_records(core.parse_dialogue(chat_text(turns)), "meld")
        assert [r["text"] for r in recs] == [t for _, t in turns], name
        assert all(r["label"] is None for r in recs)
        assert speakers_in(recs) and "Me" in speakers_in(recs), name


def test_speakers_and_ownership():
    recs = core.dialogue_records([("Joey and Chandler", "Hey!"), ("Monica", "Hi."), ("Joey", "So...")], "meld")
    assert speakers_in(recs) == ["Joey", "Chandler", "Monica"]
    assert is_mine(recs[0], "Chandler") and not is_mine(recs[1], "Chandler") and not is_mine(recs[0], None)


def test_chat_summary_reads_the_other_side():
    turns = [("Me", "a"), ("Sam", "b"), ("Me", "c"), ("Sam", "d"), ("Sam", "e")]
    recs = core.dialogue_records(turns, "meld")
    probs = _probs([("joy", .9), ("neutral", .8), ("sadness", .7), ("anger", .6), ("anger", .9)])
    w = np.array([[1, 0, 0], [.9, 0, .1], [.8, .1, .1], [.7, .1, .2], [1, 0, 0]], dtype=float)
    s = chat_summary(recs, L, probs, "Me", w, core.SOURCE_NAMES[3])
    assert s["their_lines"] == [1, 3, 4]
    assert s["counts"] == {"neutral": 1, "anger": 2}
    assert s["top_feeling"] == "anger"
    assert s["moment"] == 4 and s["moment_label"] == "anger" and s["moment_conf"] == pytest.approx(.9)
    assert s["your_share"] == pytest.approx((.1 + .2) / 2)  # line 4 has no history and is left out
    assert [lab for _, _, lab in s["journey"]] == ["neutral", "anger", "anger"]


def test_chat_summary_without_gate_or_hard_moments():
    recs = core.dialogue_records([("Me", "a"), ("Sam", "b")], "meld")
    s = chat_summary(recs, L, _probs([("neutral", .9), ("neutral", .9)]), "Me")
    assert s["top_feeling"] == "neutral" and s["moment"] is None and s["your_share"] is None


# ---------------------------------------------------------------- the page itself

def _app():
    from streamlit.testing.v1 import AppTest

    return AppTest.from_file(APP, default_timeout=180)


def _tfidf_ready():
    return core.model_status("meld", "tfidf_lr", core.DEMO_K, core.DEMO_SEED).state == "ready"


def test_page_runs_on_every_source():
    if not _tfidf_ready():
        pytest.skip("TF-IDF model not cached on this machine (python -m app.warm_cache meld)")
    at = _app().run()
    assert not at.exception, at.exception
    assert any("mood at a glance" in m.value for m in at.markdown)
    for source in ("Paste your own", "Scenes from Friends"):
        at.radio(key="u_source").set_value(source).run()
        assert not at.exception, (source, at.exception)
    assert any("labelled" in m.value for m in at.markdown)  # Friends scenes show the dataset's labels


def test_page_falls_back_to_keyword_engine_without_checkpoints(monkeypatch):
    if not _tfidf_ready():
        pytest.skip("TF-IDF model not cached on this machine (python -m app.warm_cache meld)")
    real = core.model_status

    def no_neural(dataset, model, k, seed, **kw):
        if model == "tfidf_lr":
            return real(dataset, model, k, seed, **kw)
        return core.ModelStatus(None, model, k, "missing", "no checkpoint (test)")

    monkeypatch.setattr(core, "model_status", no_neural)
    at = _app().run()
    assert not at.exception, at.exception
    page = " ".join(m.value for m in at.markdown)
    assert "lite mode" in page and "Keyword (TF-IDF)" in page
    assert "not installed" in page
