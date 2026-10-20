"""TF-IDF + Logistic Regression baseline on the current utterance only.

    python -m models.tfidf_lr --config configs/meld_tfidf_lr.yaml

The vectoriser and classifier are fitted on the training split only; the grid is
scored on the dev split (Macro-F1) and the selected model is then evaluated once
on dev and test. Outputs go to ``output_dir`` from the config.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from data.loaders import LABELS, label_to_id, load_split
from eval.latency import measure_latency
from eval.metrics import compute_metrics, metrics_to_markdown, save_metrics
from eval.predictions import predictions_frame, save_predictions

# Words (keeping in-word apostrophes so "don't"/"can't" survive as negations) plus "!" and "?".
TOKEN_PATTERN = r"(?u)\b\w[\w']*\b|[!?]"


def preprocess(text: str) -> str:
    # Model-side normalisation only; stored data keep the original characters.
    return text.lower().replace("’", "'").replace("‘", "'")


def full_proba(clf: LogisticRegression, x, n_labels: int) -> np.ndarray:
    """predict_proba has one column per class seen in training; map them to label ids."""
    probs = np.zeros((x.shape[0], n_labels))
    probs[:, clf.classes_] = clf.predict_proba(x)
    return probs


def _grid(cfg: dict):
    g = cfg["grid"]
    keys = ["ngram_range", "min_df", "C", "class_weight"]
    for values in itertools.product(*(g[k] for k in keys)):
        yield dict(zip(keys, values))


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

    cfg = config["tfidf_lr"]
    rows, vec_cache = [], {}
    best = None
    for params in _grid(cfg):
        vkey = (tuple(params["ngram_range"]), params["min_df"])
        if vkey not in vec_cache:
            vec = TfidfVectorizer(
                preprocessor=preprocess,
                token_pattern=TOKEN_PATTERN,
                ngram_range=vkey[0],
                min_df=vkey[1],
                sublinear_tf=cfg.get("sublinear_tf", True),
                stop_words=None,  # stop lists drop negations such as "not"/"no"
            )
            x_train = vec.fit_transform(text["train"])  # fitted on train only
            vec_cache[vkey] = (vec, x_train, vec.transform(text["dev"]))
        vec, x_train, x_dev = vec_cache[vkey]
        clf = LogisticRegression(
            C=params["C"],
            class_weight=params["class_weight"],
            max_iter=cfg.get("max_iter", 2000),
            random_state=config.get("seed", 42),
        )
        t0 = time.time()
        clf.fit(x_train, y["train"])
        m = compute_metrics(y["dev"], clf.predict(x_dev), labels)
        rows.append({**{k: str(v) for k, v in params.items()}, "dev_macro_f1": m["macro_f1"],
                     "dev_weighted_f1": m["weighted_f1"], "n_features": x_train.shape[1],
                     "fit_seconds": round(time.time() - t0, 2)})
        print(f"{params} dev macro-F1={m['macro_f1']:.4f}")
        if best is None or m["macro_f1"] > best[0]:
            best = (m["macro_f1"], params, vec, clf)

    pd.DataFrame(rows).to_csv(out_dir / "grid_search.csv", index=False)
    _, best_params, vec, clf = best
    joblib.dump({"vectorizer": vec, "classifier": clf, "labels": labels}, out_dir / "model.joblib")

    results = {"best_params": best_params}
    report = [f"# TF-IDF + LR on {dataset}", "", f"Selected on dev Macro-F1: `{json.dumps(best_params)}`", ""]
    for sp in ("dev", "test"):
        probs = full_proba(clf, vec.transform(text[sp]), len(labels))
        pred = probs.argmax(axis=1)
        m = compute_metrics(y[sp], pred, labels)
        save_metrics(m, out_dir / f"metrics_{sp}.json")
        save_predictions(predictions_frame(splits[sp], pred, labels, probs), out_dir / f"predictions_{sp}.csv")
        report.append(metrics_to_markdown(m, f"{sp} split"))
        results[sp] = m
        print(f"[{sp}] macro-F1={m['macro_f1']:.4f} weighted-F1={m['weighted_f1']:.4f}")
    lcfg = config.get("latency", {})
    latency = measure_latency(lambda recs: clf.predict(vec.transform([r["text"] for r in recs])), splits["test"],
                              lcfg.get("batch_size", 1), lcfg.get("warmup", 10), lcfg.get("max_samples", 300), "cpu")
    (out_dir / "latency.json").write_text(json.dumps(latency, indent=2), encoding="utf-8")
    report.append(f"Latency: {latency['ms_per_utterance']:.3f} ms/utterance end to end "
                  f"(batch size {latency['batch_size']}, {latency['n_samples']} test utterances, CPU).")
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out_dir / "DONE").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")
    results["latency"] = latency
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    run(config)


if __name__ == "__main__":
    main()
