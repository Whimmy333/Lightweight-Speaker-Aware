"""Traditional baselines: term-weighting scheme x classifier on the current utterance only.

    python train.py --config configs/meld/bm25_svm.yaml

Same protocol as models/tfidf_lr.py (the reference TF-IDF + LR baseline, kept unchanged): features
and classifier are fitted on the training split only, every grid point is scored on dev Macro-F1,
and the selected model is evaluated once on dev and test.

Weighting schemes, all over the tokens of models/tfidf_lr.py:
  binary   1 if the term occurs in the utterance, else 0
  tf       raw term counts
  tfidf    sublinear tf x idf, L2-normalised (the features of tfidf_lr)
  bm25     Okapi BM25: idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len / avg_len))

Classifiers: logistic regression (lr), linear SVM (svm), multinomial naive Bayes (mnb),
complement naive Bayes (cnb), random forest (rf). The linear SVM has no probabilities; its
prediction file stores a softmax over the decision scores instead.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from data.loaders import LABELS, label_to_id, load_split
from eval.latency import measure_latency
from eval.metrics import compute_metrics, metrics_to_markdown, save_metrics
from eval.predictions import predictions_frame, save_predictions
from models.tfidf_lr import TOKEN_PATTERN, preprocess


class BM25Transformer(TransformerMixin, BaseEstimator):
    """Okapi BM25 weights for a term-count matrix; idf and average length come from the fit data."""

    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def fit(self, x, y=None):
        x = x.tocsr()
        n_docs = x.shape[0]
        df = np.bincount(x.indices, minlength=x.shape[1])
        self.idf_ = np.log1p((n_docs - df + 0.5) / (df + 0.5))
        self.avg_len_ = max(float(x.sum()) / max(n_docs, 1), 1e-9)
        return self

    def transform(self, x):
        x = x.tocsr().astype(np.float64, copy=True)
        doc_len = np.asarray(x.sum(axis=1)).ravel()
        norm = self.k1 * (1 - self.b + self.b * doc_len / self.avg_len_)
        rows = np.repeat(np.arange(x.shape[0]), np.diff(x.indptr))
        tf = x.data
        x.data = tf * (self.k1 + 1) / (tf + norm[rows]) * self.idf_[x.indices]
        return x


def make_features(weighting: str, ngram_range, min_df: int, cfg: dict):
    common = dict(preprocessor=preprocess, token_pattern=TOKEN_PATTERN, ngram_range=tuple(ngram_range),
                  min_df=min_df, stop_words=None)  # stop lists drop negations such as "not"/"no"
    if weighting == "binary":
        return CountVectorizer(binary=True, **common)
    if weighting == "tf":
        return CountVectorizer(**common)
    if weighting == "tfidf":
        return TfidfVectorizer(sublinear_tf=True, **common)
    if weighting == "bm25":
        bm25 = cfg.get("bm25", {})
        return Pipeline([("counts", CountVectorizer(**common)),
                         ("bm25", BM25Transformer(bm25.get("k1", 1.2), bm25.get("b", 0.75)))])
    raise ValueError(f"unknown weighting {weighting!r}")


def make_classifier(name: str, params: dict, seed: int, cfg: dict):
    if name == "lr":
        return LogisticRegression(C=params["C"], class_weight=params["class_weight"],
                                  max_iter=cfg.get("max_iter", 2000), random_state=seed)
    if name == "svm":
        return LinearSVC(C=params["C"], class_weight=params["class_weight"], max_iter=cfg.get("max_iter", 2000),
                         random_state=seed)
    if name == "mnb":
        return MultinomialNB(alpha=params["alpha"], fit_prior=params["fit_prior"])
    if name == "cnb":
        return ComplementNB(alpha=params["alpha"])
    if name == "rf":
        return RandomForestClassifier(n_estimators=params["n_estimators"], min_samples_leaf=params["min_samples_leaf"],
                                      class_weight=params["class_weight"], max_features="sqrt", n_jobs=-1,
                                      random_state=seed)
    raise ValueError(f"unknown classifier {name!r}")


def full_scores(clf, x, n_labels: int) -> np.ndarray:
    """Class probabilities (softmax of decision scores for the SVM), one column per label id."""
    if hasattr(clf, "predict_proba"):
        scores = clf.predict_proba(x)
    else:
        d = clf.decision_function(x)
        d = np.column_stack([-d, d]) if d.ndim == 1 else d
        e = np.exp(d - d.max(axis=1, keepdims=True))
        scores = e / e.sum(axis=1, keepdims=True)
    probs = np.zeros((x.shape[0], n_labels))
    probs[:, clf.classes_] = scores
    return probs


def count_parameters(clf, n_features: int) -> dict:
    """Learned values of the fitted classifier. A random forest has no weight vector, so it reports tree nodes."""
    if isinstance(clf, RandomForestClassifier):
        return {"n_features": n_features, "parameters": int(sum(t.tree_.node_count for t in clf.estimators_)),
                "unit": "tree nodes"}
    if hasattr(clf, "coef_"):
        n = clf.coef_.size + np.size(clf.intercept_)
    else:  # naive Bayes: per-class feature log-probabilities and class priors
        n = clf.feature_log_prob_.size + clf.class_log_prior_.size
    return {"n_features": n_features, "parameters": int(n), "unit": "weights"}


def _grid(values: dict):
    keys = list(values)
    for combo in itertools.product(*(values[k] for k in keys)):
        yield dict(zip(keys, combo))


def run(config: dict) -> dict:
    dataset = config["data"]["dataset"]
    processed_dir = Path(config["data"].get("processed_dir", "data/processed"))
    out_dir = Path(config["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    if (out_dir / "DONE").exists():
        print(f"{config['run_name']} is already complete ({out_dir}/DONE); delete the directory to rerun")
        return {}
    with open(out_dir / "config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    labels = LABELS[dataset]
    l2i = label_to_id(dataset)
    splits = {sp: load_split(processed_dir, dataset, sp) for sp in ("train", "dev", "test")}
    limit = config["data"].get("max_samples")
    if limit:  # smoke tests only
        splits = {sp: recs[:limit] for sp, recs in splits.items()}
    text = {sp: [r["text"] for r in recs] for sp, recs in splits.items()}
    y = {sp: np.array([l2i[r["label"]] for r in recs]) for sp, recs in splits.items()}

    mcfg, cfg = config["model"], config["classical"]
    weighting, clf_name = mcfg["weighting"], mcfg["classifier"]
    seed = config.get("seed", 42)
    rows, best = [], None
    for fparams in _grid(cfg["feature_grid"]):
        features = make_features(weighting, fparams["ngram_range"], fparams["min_df"], cfg)
        x_train = features.fit_transform(text["train"])  # fitted on train only
        x_dev = features.transform(text["dev"])
        for cparams in _grid(cfg["classifier_grid"][clf_name]):
            clf = make_classifier(clf_name, cparams, seed, cfg)
            t0 = time.time()
            clf.fit(x_train, y["train"])
            m = compute_metrics(y["dev"], clf.predict(x_dev), labels)
            params = {**fparams, **cparams}
            rows.append({**{k: str(v) for k, v in params.items()}, "dev_macro_f1": m["macro_f1"],
                         "dev_weighted_f1": m["weighted_f1"], "n_features": x_train.shape[1],
                         "fit_seconds": round(time.time() - t0, 2)})
            print(f"{params} dev macro-F1={m['macro_f1']:.4f}")
            if best is None or m["macro_f1"] > best[0]:
                best = (m["macro_f1"], params, features, clf, x_train.shape[1])

    pd.DataFrame(rows).to_csv(out_dir / "grid_search.csv", index=False)
    _, best_params, features, clf, n_features = best
    joblib.dump({"features": features, "classifier": clf, "labels": labels}, out_dir / "model.joblib")
    params = {**count_parameters(clf, n_features), "selected": best_params}
    (out_dir / "params.json").write_text(json.dumps(params, indent=2), encoding="utf-8")

    title = f"{weighting} + {clf_name}"
    results = {"best_params": best_params}
    report = [f"# {title} on {dataset}", "", f"Selected on dev Macro-F1: `{json.dumps(best_params)}`", "",
              f"Parameters: {params['parameters']:,} {params['unit']} over {n_features:,} features.", ""]
    for sp in ("dev", "test"):
        probs = full_scores(clf, features.transform(text[sp]), len(labels))
        pred = probs.argmax(axis=1)
        m = compute_metrics(y[sp], pred, labels)
        save_metrics(m, out_dir / f"metrics_{sp}.json")
        save_predictions(predictions_frame(splits[sp], pred, labels, probs), out_dir / f"predictions_{sp}.csv")
        report.append(metrics_to_markdown(m, f"{sp} split"))
        results[sp] = m
        print(f"[{sp}] macro-F1={m['macro_f1']:.4f} weighted-F1={m['weighted_f1']:.4f}")
    lcfg = config.get("latency", {})
    latency = measure_latency(lambda recs: clf.predict(features.transform([r["text"] for r in recs])),
                              splits["test"], lcfg.get("batch_size", 1), lcfg.get("warmup", 10),
                              lcfg.get("max_samples", 300), "cpu")
    (out_dir / "latency.json").write_text(json.dumps(latency, indent=2), encoding="utf-8")
    report.append(f"Latency: {latency['ms_per_utterance']:.3f} ms/utterance end to end "
                  f"(batch size {latency['batch_size']}, {latency['n_samples']} test utterances, CPU).")
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out_dir / "DONE").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")
    results["latency"] = latency
    return results
