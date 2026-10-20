"""End-to-end runs of train.py's pipelines on a tiny encoder and tiny dataset."""

import json

import pandas as pd
import pytest

import models.trainer as trainer
from configs.generate_configs import neural_config, tfidf_config
from eval.aggregate import collect, summarise, to_markdown
from eval.predictions import FUSION_WEIGHT_COLUMNS
from tests.conftest import write_tiny_processed


def tiny_config(tmp_path, tiny_encoder, model="adaptive", turns=3, run="run"):
    _, cfg = neural_config("meld", model, turns, 42)
    cfg["data"]["processed_dir"] = str(tmp_path / "processed")
    cfg["model"]["pretrained"] = tiny_encoder
    cfg["train"].update({"epochs": 2, "lrs": [1e-3, 2e-3], "batch_size": 4, "eval_batch_size": 8, "device": "cpu"})
    cfg["latency"] = {"batch_size": 1, "max_samples": 5, "warmup": 1}
    cfg["output_dir"] = str(tmp_path / "runs" / run)
    return cfg


@pytest.fixture
def data_dir(tmp_path):
    write_tiny_processed(tmp_path / "processed")
    return tmp_path


def test_adaptive_run_outputs(data_dir, tiny_encoder):
    cfg = tiny_config(data_dir, tiny_encoder)
    trainer.run(cfg)
    out = data_dir / "runs" / "run"
    for name in ("config.yaml", "train.log", "best.json", "metrics_dev.json", "metrics_test.json",
                 "predictions_dev.csv", "predictions_test.csv", "fusion_weights_dev.csv", "fusion_weights_test.csv",
                 "metrics_test_equal_weights.json", "latency.json", "report.md", "DONE"):
        assert (out / name).exists(), name
    best = json.loads((out / "best.json").read_text())
    assert best["lr"] in (1e-3, 2e-3) and best["checkpoint_kept"]
    kept = list(out.glob("lr_*/checkpoints/best.pt"))
    assert len(kept) == 1 and f"lr_{best['lr']:g}" in str(kept[0])  # unselected lr pruned, no last.pt left
    for lr in ("lr_0.001", "lr_0.002"):
        assert len((out / lr / "epoch_metrics.jsonl").read_text().splitlines()) == 2
    w = pd.read_csv(out / "fusion_weights_test.csv")
    assert list(w.columns) == FUSION_WEIGHT_COLUMNS and len(w) == 20
    assert ((w.w_current + w.w_same + w.w_other - 1).abs() < 1e-5).all()
    assert (w.loc[w.turn_index == 0, "w_current"] == 1).all()
    preds = pd.read_csv(out / "predictions_test.csv")
    assert len(preds) == 20 and {"label", "pred", "prob_joy"} <= set(preds.columns)
    assert trainer.run(cfg) is None  # finished runs are skipped


@pytest.mark.parametrize("model,turns", [("single", 3), ("concat", 5), ("fixed", 1), ("adaptive_merged", 3)])
def test_every_model_type_runs(data_dir, tiny_encoder, model, turns):
    cfg = tiny_config(data_dir, tiny_encoder, model, turns, run=model)
    cfg["train"].update({"epochs": 1, "lrs": [1e-3]})
    res = trainer.run(cfg)
    assert 0.0 <= res["metrics"]["test"]["macro_f1"] <= 1.0
    out = data_dir / "runs" / model
    assert (out / "fusion_weights_test.csv").exists() == (model in ("fixed", "adaptive_merged"))
    if model == "adaptive_merged":
        w = pd.read_csv(out / "fusion_weights_test.csv")
        assert w.w_same.isna().all() and ((w.w_current + w.w_history - 1).abs() < 1e-5).all()


def test_resume_after_crash(data_dir, tiny_encoder, monkeypatch):
    cfg = tiny_config(data_dir, tiny_encoder, run="crash")
    real_evaluate = trainer.evaluate
    calls = {"n": 0}

    def crash_on_second_dev_eval(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("simulated crash")
        return real_evaluate(*args, **kwargs)

    monkeypatch.setattr(trainer, "evaluate", crash_on_second_dev_eval)
    with pytest.raises(RuntimeError, match="simulated crash"):
        trainer.run(cfg)
    out = data_dir / "runs" / "crash"
    assert (out / "lr_0.001" / "checkpoints" / "last.pt").exists()
    assert len((out / "lr_0.001" / "epoch_metrics.jsonl").read_text().splitlines()) == 1

    changed = json.loads(json.dumps(cfg))
    changed["train"]["batch_size"] = 2
    with pytest.raises(RuntimeError, match="differs from the requested config"):
        trainer.run(changed)

    monkeypatch.setattr(trainer, "evaluate", real_evaluate)
    trainer.run(cfg)
    assert "resuming after epoch 1" in (out / "train.log").read_text()
    epochs = [json.loads(line)["epoch"] for line in (out / "lr_0.001" / "epoch_metrics.jsonl").read_text().splitlines()]
    assert epochs == [1, 2] and (out / "DONE").exists()
    assert not (out / "lr_0.001" / "checkpoints" / "last.pt").exists()


def test_tfidf_with_missing_classes_and_aggregate(data_dir, tiny_encoder):
    from models.tfidf_lr import run as run_tfidf

    _, cfg = tfidf_config("meld")
    cfg["data"]["processed_dir"] = str(data_dir / "processed")
    cfg["data"]["max_samples"] = 8  # only some of the 7 classes appear in train
    cfg["tfidf_lr"]["grid"] = {"ngram_range": [[1, 1]], "min_df": [1], "C": [1.0], "class_weight": [None]}
    cfg["latency"] = {"batch_size": 1, "max_samples": 5, "warmup": 1}
    cfg["output_dir"] = str(data_dir / "runs" / "tfidf")
    run_tfidf(cfg)
    preds = pd.read_csv(data_dir / "runs" / "tfidf" / "predictions_test.csv")
    probs = preds[[c for c in preds.columns if c.startswith("prob_")]]
    assert probs.shape[1] == 7 and ((probs.sum(1) - 1).abs() < 1e-6).all()

    runs = collect(data_dir / "runs")
    assert set(runs.model) == {"tfidf_lr"}
    assert "main comparison" in to_markdown(summarise(runs))
