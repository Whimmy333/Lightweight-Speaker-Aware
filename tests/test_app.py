import json

import numpy as np
import pytest
import torch

from app import core
from data.loaders import LABELS
from models.neural import build_model
from tests.conftest import write_tiny_processed

DIALOGUE = [("Maya", "oh no"), ("Leo", "what ?"), ("Maya", "no !"), ("Leo", "yes"), ("Maya", "hello")]


def test_models_and_seeds_from_configs():
    meld = core.models_for("meld")
    assert meld["adaptive"] == [1, 3, 5]
    assert meld["tfidf_lr"] == [0] and meld["single"] == [0]
    assert meld["adaptive_merged"] == [3]
    assert list(meld)[:5] == ["tfidf_lr", "single", "concat", "fixed", "adaptive"]  # display order
    assert "fixed_merged" in core.models_for("dailydialog")
    assert core.seeds_for("meld") == [42, 43, 44]


def test_pick_spec():
    specs = core.config_specs("meld")
    assert core.pick_spec(specs, "concat", 5, 43).run_name == "meld_concat_k5_s43"
    assert core.pick_spec(specs, "single", 5, 42).run_name == "meld_single_s42"
    assert core.pick_spec(specs, "tfidf_lr", 1, 44).run_name == "meld_tfidf_lr"
    assert core.pick_spec(specs, "adaptive_merged", 1, 42).k == 3  # only configured at k=3
    assert core.pick_spec(core.config_specs("emorynlp"), "concat", 1, 42).k == 3  # EmoryNLP: k=3 only
    assert core.pick_spec(specs, "fixed_merged", 3, 42) is None  # DailyDialog-only ablation


def test_find_checkpoint_reroots_cluster_path(tmp_path):
    run = tmp_path / "meld_adaptive_k3_s42"
    ckpt = run / "lr_5e-05" / "checkpoints" / "best.pt"
    ckpt.parent.mkdir(parents=True)
    ckpt.write_bytes(b"x")
    (run / "best.json").write_text(json.dumps(
        {"checkpoint": "/ssd/proj/outputs/runs/meld_adaptive_k3_s42/lr_5e-05/checkpoints/best.pt"}))
    assert core.find_checkpoint(run) == ckpt


def test_find_checkpoint_without_best_json(tmp_path):
    run = tmp_path / "r"
    assert core.find_checkpoint(run) is None
    for lr, f1 in (("lr_2e-05", 0.5), ("lr_5e-05", 0.4)):
        d = run / lr
        (d / "checkpoints").mkdir(parents=True)
        (d / "checkpoints" / "best.pt").write_bytes(b"x")
        (d / "epoch_metrics.jsonl").write_text(json.dumps({"dev_macro_f1": f1}) + "\n")
    assert core.find_checkpoint(run).parts[-3] == "lr_2e-05"
    (run / "best.pt").write_bytes(b"x")  # a single file dropped in by hand wins over the scan
    assert core.find_checkpoint(run) == run / "best.pt"


def test_status_degrades_without_checkpoints_or_data(tmp_path):
    kw = dict(runs_dir=tmp_path / "runs", cache_dir=tmp_path / "cache", processed_dir=tmp_path / "proc")
    s = core.model_status("meld", "adaptive", 3, 42, **kw)
    assert s.state == "missing" and "checkpoint" in s.note
    assert core.model_status("meld", "tfidf_lr", 3, 42, **kw).state == "missing"
    assert core.model_status("emorynlp", "concat", 1, 42, **kw).state == "missing"
    write_tiny_processed(tmp_path / "proc")
    assert core.model_status("meld", "tfidf_lr", 3, 42, **kw).state == "trainable"


def test_parse_dialogue_and_records():
    turns = core.parse_dialogue("Joey and Chandler: Hey!\n\n  no speaker here  \nRachel: Hi: there")
    assert turns == [("Joey and Chandler", "Hey!"), ("", "no speaker here"), ("Rachel", "Hi: there")]
    recs = core.dialogue_records(turns, "meld", "c")
    assert recs[0]["speaker_ids"] == ["Joey", "Chandler"] and recs[1]["speaker_ids"] == []
    assert [r["turn_index"] for r in recs] == [0, 1, 2]
    assert len({r["utterance_id"] for r in recs}) == 3
    ctx = core.context_for(recs, 2, 3)
    assert [h.same_speaker for h in ctx.history] == [False, None]


def test_tfidf_trains_into_cache_and_predicts(tmp_path):
    proc = write_tiny_processed(tmp_path / "proc")
    spec = core.pick_spec(core.config_specs("meld"), "tfidf_lr", 0, 42)
    path = core.train_tfidf(spec, cache_dir=tmp_path / "cache", processed_dir=proc)
    assert path.exists()
    assert core.tfidf_model_path(spec.run_name, tmp_path / "runs", tmp_path / "cache") == path
    pred = core.TfidfPredictor.load(path).predict(core.dialogue_records(DIALOGUE, "meld"))
    assert pred.probs.shape == (5, 7) and np.allclose(pred.probs.sum(1), 1)
    assert pred.weights is None and set(pred.pred) <= set(LABELS["meld"])


def _save_checkpoint(path, tiny_encoder, model_cfg, k):
    cfg = {"run_name": "t", "data": {"dataset": "meld"}, "context": {"num_turns": k, "max_utt_tokens": 8},
           "model": {"pretrained": tiny_encoder, "dropout": 0.0, **model_cfg}}
    torch.manual_seed(0)
    model = build_model(cfg["model"], 7)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "labels": LABELS["meld"], "config": cfg}, path)
    return model


@pytest.mark.parametrize("speaker_split", [True, False])
def test_neural_fusion_predictor(tmp_path, tiny_encoder, speaker_split):
    ckpt = tmp_path / "best.pt"
    _save_checkpoint(ckpt, tiny_encoder, {"type": "fusion", "fusion": {
        "weighting": "learned", "speaker_split": speaker_split, "gate_hidden": 8}}, k=3)
    p = core.NeuralPredictor.load(ckpt)
    assert p.k == 3
    pred = p.predict(core.dialogue_records(DIALOGUE, "meld"))
    n_src = 3 if speaker_split else 2
    assert pred.probs.shape == (5, 7) and pred.weights.shape == (5, n_src)
    assert pred.source_names == core.SOURCE_NAMES[n_src]
    assert np.allclose(pred.weights.sum(1), 1, atol=1e-5)
    assert pred.weights[0].tolist()[0] == pytest.approx(1.0)  # first turn: current utterance only
    assert (pred.weights[~pred.avail] == 0).all()


def test_neural_single_predictor_matches_direct_forward(tmp_path, tiny_encoder):
    ckpt = tmp_path / "best.pt"
    model = _save_checkpoint(ckpt, tiny_encoder, {"type": "single"}, k=3).eval()
    p = core.NeuralPredictor.load(ckpt)
    assert p.k == 0  # single never sees history, whatever the config says
    recs = core.dialogue_records(DIALOGUE, "meld")
    pred = p.predict(recs)
    assert pred.weights is None
    batch = p.collator([(c, 0) for c in core.build_contexts(recs, 0)])
    with torch.no_grad():
        ref = torch.softmax(model(batch)["logits"], -1).numpy()
    assert np.allclose(pred.probs, ref, atol=1e-6)


def test_status_ready_when_checkpoint_dropped_in(tmp_path, tiny_encoder, monkeypatch):
    runs = tmp_path / "runs"
    kw = dict(runs_dir=runs, cache_dir=tmp_path / "cache", processed_dir=tmp_path / "proc")
    assert core.model_status("meld", "concat", 3, 42, **kw).state == "missing"
    _save_checkpoint(runs / "meld_concat_k3_s42" / "best.pt", tiny_encoder, {"type": "concat"}, k=3)
    monkeypatch.setattr(core, "ENCODER_DIR", core.Path(tiny_encoder))
    s = core.model_status("meld", "concat", 3, 42, **kw)
    assert s.state == "ready" and s.checkpoint.name == "best.pt"


def test_results_table_loads():
    df = core.load_results()
    assert {"meld", "emorynlp", "dailydialog"} <= set(df["dataset"])
    assert df.loc[df["model"] == "adaptive", "model_label"].iloc[0] == "Adaptive fusion"


def test_test_dialogues_fall_back_to_predictions_csv(tmp_path):
    from eval.predictions import predictions_frame, save_predictions
    from tests.conftest import make_record

    recs = [make_record("dia7", t, [s], text, label="joy", split="test")
            for t, (s, text) in enumerate([("Joey and Chandler", "None"), ("Ross", "NA"), ("Ross", "hi")])]
    run = tmp_path / "runs" / "meld_tfidf_lr"
    save_predictions(predictions_frame(recs, [0, 1, 2], LABELS["meld"]), run / "predictions_test.csv")
    assert core.load_test_dialogues("meld", tmp_path / "proc", tmp_path / "nothing") == {}
    got = core.load_test_dialogues("meld", tmp_path / "proc", tmp_path / "runs")
    assert got == {"dia7": recs}  # same records, "None"/"NA" stay text, joint speakers stay split


def test_committed_test_dialogues_load():
    dialogues = core.load_test_dialogues("meld", core.ROOT / "no_processed_here")
    assert sum(len(v) for v in dialogues.values()) == 2610  # MELD test utterances
