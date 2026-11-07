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



def test_prediction_round_trips_as_plain_data(tmp_path, tiny_encoder):
    """The app caches vars(prediction), not the object (a hot-reloaded class would not pickle)."""
    import pickle

    ckpt = tmp_path / "best.pt"
    _save_checkpoint(ckpt, tiny_encoder, {"type": "fusion", "fusion": {
        "weighting": "learned", "speaker_split": True, "gate_hidden": 8}}, k=3)
    pred = core.NeuralPredictor.load(ckpt).predict(core.dialogue_records(DIALOGUE, "meld"))
    blob = pickle.dumps(vars(pred).copy())
    assert b"app.core" not in blob
    back = core.Prediction(**pickle.loads(blob))
    assert back.pred == pred.pred and np.allclose(back.weights, pred.weights)

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
    assert df.loc[df["model"] == "adaptive", "model_label"].iloc[0] == "Adaptive weighting"


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


@pytest.mark.parametrize("model_cfg", [
    {"type": "single"},
    {"type": "fusion", "fusion": {"weighting": "equal", "speaker_split": True, "gate_hidden": 8}},
    {"type": "fusion", "fusion": {"weighting": "learned", "speaker_split": True, "gate_hidden": 8}},
    {"type": "fusion", "fusion": {"weighting": "learned", "speaker_split": False, "gate_hidden": 8}},
])
def test_added_parameters_match_models(tiny_encoder, model_cfg):
    m = build_model({"pretrained": tiny_encoder, "dropout": 0.0, **model_cfg}, 7)
    added = sum(p.numel() for p in m.parameters()) - sum(p.numel() for p in m.encoder.parameters())
    assert core.added_parameters(model_cfg, 7, hidden=m.encoder.hidden_size) == added


def test_model_sizes_meld():
    sizes = core.model_sizes("meld", 3).set_index("model")["added_params"]
    assert sizes["adaptive"] == 597_002 and sizes["single"] == sizes["fixed"] == 5_383


def test_distilbert_size_constant():
    enc = core.ENCODER_DIR
    if not (enc / "model.safetensors").exists():
        pytest.skip("encoder not prepared")
    from transformers import AutoModel

    m = AutoModel.from_pretrained(str(enc))
    assert sum(p.numel() for p in m.parameters()) == core.DISTILBERT_BASE_PARAMS
    assert m.config.dim == core.DISTILBERT_HIDDEN


def _write_saved_run(run_dir, recs, speaker_split):
    from eval.predictions import fusion_weights_frame, predictions_frame, save_predictions

    rng = np.random.default_rng(0)
    probs = rng.dirichlet(np.ones(7), size=len(recs))
    ctx = core.build_contexts(recs, 3)
    s = 3 if speaker_split else 2
    avail = np.array([[True] + ([bool(c.same_speaker_texts), bool(c.other_speaker_texts)] if speaker_split
                                else [bool(c.history)]) for c in ctx])
    w = np.where(avail, rng.random((len(recs), s)), 0.0)
    w = w / w.sum(1, keepdims=True)
    save_predictions(predictions_frame(recs, probs.argmax(1), LABELS["meld"], probs), run_dir / "predictions_test.csv")
    save_predictions(fusion_weights_frame(recs, ctx, probs.argmax(1), LABELS["meld"], w, avail.astype(int),
                                          speaker_split), run_dir / "fusion_weights_test.csv")
    return probs, w, avail


@pytest.mark.parametrize("speaker_split", [True, False])
def test_saved_predictor_replays_cluster_outputs(tmp_path, speaker_split):
    from tests.conftest import make_record

    recs = [make_record("dia3", t, [s], f"line {t}", split="test") for t, s in enumerate("ABAAB")]
    run = tmp_path / "runs" / "meld_adaptive_k3_s42"
    probs, w, avail = _write_saved_run(run, recs, speaker_split)
    kw = dict(runs_dir=tmp_path / "runs", cache_dir=tmp_path / "cache", processed_dir=tmp_path / "proc")
    status = core.model_status("meld", "adaptive", 3, 42, **kw)
    assert status.state == "saved" and not status.usable

    sp = core.SavedPredictor.load(run, LABELS["meld"], 3)
    order = [recs[i] for i in (4, 0, 2)]  # lookup is by utterance_id, not position
    assert sp.covers(order) and not sp.covers(core.dialogue_records(DIALOGUE, "meld"))
    pred = sp.predict(order)
    assert np.allclose(pred.probs, probs[[4, 0, 2]])
    assert pred.source_names == core.SOURCE_NAMES[3 if speaker_split else 2]
    assert np.allclose(pred.weights, w[[4, 0, 2]]) and (pred.avail == avail[[4, 0, 2]]).all()



@pytest.mark.parametrize("speaker_split", [True, False])
def test_gate_summary_groups_and_averages_seeds(tmp_path, speaker_split):
    import pandas as pd
    from tests.conftest import make_record

    recs = [make_record("dia3", t, [s], f"line {t}", split="test") for t, s in enumerate("ABAAB")]
    runs = tmp_path / "runs"
    for seed in (42, 43):
        _write_saved_run(runs / f"meld_adaptive_k3_s{seed}", recs, speaker_split)
    model = "adaptive" if speaker_split else "adaptive_merged"
    if not speaker_split:  # the merged run is a different config: copy the files under its name
        for seed in (42, 43):
            (runs / f"meld_adaptive_k3_s{seed}").rename(runs / f"meld_adaptive_merged_k3_s{seed}")
    g = core.gate_summary("meld", model, 3, runs_dir=runs).set_index("group")
    d = pd.read_csv(runs / f"meld_{model}_k3_s42" / "fusion_weights_test.csv")
    assert g.loc["all test lines", "n"] == len(recs) and (g["n_seeds"] == 2).all()
    assert g.loc["first turn (no history)", "current"] == pytest.approx(1.0)
    assert g.drop("all test lines")["share"].sum() == pytest.approx(1.0)
    assert g.loc["all test lines", "current"] == pytest.approx(d["w_current"].mean())
    srcs = core.SOURCE_NAMES[3 if speaker_split else 2]
    assert np.allclose(g[srcs].sum(axis=1), 1.0)
    assert (g["spread"] == 0).all()  # both seeds wrote the same weights


def test_gate_summary_matches_reported_meld_numbers():
    """The README reports these: 84% on the current line when all three sources exist, own past 2x others'."""
    if not (core.RUNS_DIR / "meld_adaptive_k3_s44" / "fusion_weights_test.csv").is_file():
        pytest.skip("MELD adaptive fusion weights not in outputs/runs/")
    g = core.gate_summary("meld", "adaptive", 3).set_index("group")
    top = g.loc["all three sources"]
    assert (top["current"], top["same speaker"], top["other speaker"]) == pytest.approx((0.84, 0.11, 0.05), abs=0.006)
    assert top["same speaker"] / top["other speaker"] == pytest.approx(2, abs=0.2)
    assert int(top["n"]) == 1369 and int(g.loc["current + one history group", "n"]) == 961
    assert int(g.loc["first turn (no history)", "n"]) == 280 and g["spread"].max() < 0.01

def test_checkpoint_wins_over_saved_csvs(tmp_path, tiny_encoder, monkeypatch):
    from tests.conftest import make_record

    runs = tmp_path / "runs"
    recs = [make_record("d", t, ["A"], "x", split="test") for t in range(2)]
    _write_saved_run(runs / "meld_adaptive_k3_s42", recs, True)
    kw = dict(runs_dir=runs, cache_dir=tmp_path / "cache", processed_dir=tmp_path / "proc")
    assert core.model_status("meld", "adaptive", 3, 42, **kw).state == "saved"
    _save_checkpoint(runs / "meld_adaptive_k3_s42" / "best.pt", tiny_encoder, {"type": "fusion", "fusion": {
        "weighting": "learned", "speaker_split": True, "gate_hidden": 8}}, k=3)
    monkeypatch.setattr(core, "ENCODER_DIR", core.Path(tiny_encoder))
    assert core.model_status("meld", "adaptive", 3, 42, **kw).state == "ready"


def test_templates_are_unlabelled():
    from app.examples import TEMPLATES, template_text

    for name, turns in TEMPLATES.items():
        assert all(len(t) == 2 for t in turns), name  # never scored against our own readings
        recs = core.dialogue_records(core.parse_dialogue(template_text(name)), "meld")
        assert [r["text"] for r in recs] == [t for _, t in turns] and all(r["label"] is None for r in recs)


def test_featured_descriptions_hold():
    """The featured blurbs describe specific model behaviour; re-check it against the live checkpoints."""
    from app.examples import FEATURED

    dialogues = core.load_test_dialogues("meld")
    for feat in FEATURED["meld"]:
        recs = dialogues[feat["dialogue_id"]]
        line = feat["line"] - 1
        assert f"**{recs[line]['label']}**" in feat["blurb"]  # the gold label the blurb names
        for model, want in feat["expect"].items():
            status = core.model_status("meld", model, core.DEMO_K, core.DEMO_SEED)
            if status.state != "ready":
                pytest.skip(f"{model} checkpoint not on this machine")
            loader = core.TfidfPredictor.load if model == "tfidf_lr" else core.NeuralPredictor.load
            assert loader(status.checkpoint).predict(recs).pred[line] == want, (feat["dialogue_id"], model)
