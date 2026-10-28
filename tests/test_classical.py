"""Traditional baselines: term weighting schemes, classifiers and their run outputs."""

import json

import numpy as np
import pandas as pd
import pytest
from scipy.sparse import csr_matrix

from configs.generate_configs import CLASSIFIER_GRIDS, WEIGHTINGS, classical_config
from models.classical import BM25Transformer, make_features, run
from tests.conftest import write_tiny_processed


def test_bm25_weights():
    counts = csr_matrix(np.array([[2, 0, 1], [0, 1, 1]], dtype=float))
    bm25 = BM25Transformer(k1=1.2, b=0.75).fit(counts)
    w = bm25.transform(counts).toarray()
    idf = np.log1p((2 - np.array([1, 1, 2]) + 0.5) / (np.array([1, 1, 2]) + 0.5))
    norm0 = 1.2 * (1 - 0.75 + 0.75 * 3 / 2.5)  # document 0 has 3 tokens, average length 2.5
    assert w[0, 0] == pytest.approx(2 * 2.2 / (2 + norm0) * idf[0])
    assert w[0, 1] == 0
    assert (w[:, 2] > 0).all() and w[0, 2] < w[0, 0]  # a term in every document weighs less


@pytest.mark.parametrize("weighting", WEIGHTINGS)
def test_weightings_share_the_vocabulary(weighting):
    texts = ["oh no!", "what? no", "yes yes yes"]
    x = make_features(weighting, (1, 1), 1, {}).fit_transform(texts)
    assert x.shape == (3, 6)  # oh, no, !, what, ?, yes: punctuation "!" and "?" are tokens
    if weighting == "binary":
        assert x.max() == 1


@pytest.fixture
def data_dir(tmp_path):
    write_tiny_processed(tmp_path / "processed")
    return tmp_path


@pytest.mark.parametrize("classifier", list(CLASSIFIER_GRIDS))
def test_every_classifier_runs(data_dir, classifier):
    _, cfg = classical_config("meld", "bm25", classifier)
    cfg["data"]["processed_dir"] = str(data_dir / "processed")
    cfg["data"]["max_samples"] = 8  # only some of the 7 classes appear in train
    cfg["classical"]["feature_grid"] = {"ngram_range": [[1, 1]], "min_df": [1]}
    grid = cfg["classical"]["classifier_grid"][classifier]
    cfg["classical"]["classifier_grid"][classifier] = {k: v[:1] for k, v in grid.items()}
    cfg["latency"] = {"batch_size": 1, "max_samples": 5, "warmup": 1}
    cfg["output_dir"] = str(data_dir / "runs" / classifier)
    res = run(cfg)
    assert 0.0 <= res["test"]["macro_f1"] <= 1.0
    out = data_dir / "runs" / classifier
    preds = pd.read_csv(out / "predictions_test.csv")
    probs = preds[[c for c in preds.columns if c.startswith("prob_")]]
    assert probs.shape[1] == 7 and ((probs.sum(1) - 1).abs() < 1e-6).all()
    params = json.loads((out / "params.json").read_text())
    assert params["parameters"] > 0 and params["n_features"] > 0
    assert run(cfg) == {}  # finished runs are skipped
