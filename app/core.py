"""Everything the Streamlit demo needs that is not UI: run discovery, model loading, live inference.

Models are found from the generated configs (``configs/<dataset>/*.yaml``) and their run directories
(``outputs/runs/<run_name>/``). Discovery is a cheap file scan, so a checkpoint copied into
``outputs/runs/`` switches its model on at the next page interaction without restarting the app.

TF-IDF + LR is always live: it loads ``model.joblib`` from the run directory if one exists, otherwise
``models/tfidf_lr.run`` re-trains it from ``data/processed`` (same grid, same dev selection as the
reported baseline) into ``outputs/demo_cache/``.

Neural models load ``best.pt`` on CPU, rebuild the architecture with ``models.neural.build_model`` and
batch a dialogue with ``models.batching.Collator`` on contexts from ``data.context.build_contexts``,
exactly as in training.
"""

from __future__ import annotations

import copy
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
import yaml

from data.context import build_contexts
from data.loaders import LABELS, load_split, parse_meld_speakers, processed_path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS_DIR = ROOT / "configs"
RUNS_DIR = ROOT / "outputs" / "runs"
CACHE_DIR = ROOT / "outputs" / "demo_cache"
PROCESSED_DIR = ROOT / "data" / "processed"
ENCODER_DIR = ROOT / "data" / "pretrained" / "distilbert-base-uncased"
RESULTS_CSV = ROOT / "outputs" / "results_summary.csv"

# The live demo uses the main comparison setting only (team decision, 27 Oct 2026).
DEMO_K = 3
DEMO_SEED = 42

DATASET_NAMES = {"meld": "MELD", "emorynlp": "EmoryNLP", "dailydialog": "DailyDialog"}


@dataclass(frozen=True)
class ModelInfo:
    label: str
    short: str
    blurb: str


# Display order is also the comparison order in every table.
MODEL_INFO: Dict[str, ModelInfo] = {
    "tfidf_lr": ModelInfo("TF-IDF + LR", "TF-IDF", "Bag of n-grams of the current utterance; no context."),
    "single": ModelInfo("DistilBERT (single)", "Single", "Current utterance only."),
    "concat": ModelInfo("Concat", "Concat", "Current utterance and the previous k turns in one sequence."),
    "fixed": ModelInfo("Fixed fusion", "Fixed", "Equal weights over current / same-speaker / other-speaker."),
    "adaptive": ModelInfo("Adaptive fusion", "Adaptive",
                          "Learned per-utterance weights over current / same-speaker / other-speaker."),
    "fixed_merged": ModelInfo("Fixed fusion (merged)", "Fixed-merged",
                              "Equal weights over current / all history (no speaker split)."),
    "adaptive_merged": ModelInfo("Adaptive fusion (merged)", "Adaptive-merged",
                                 "Learned weights over current / all history (no speaker split)."),
}
MODEL_ORDER = list(MODEL_INFO)

SOURCE_NAMES = {3: ["current", "same speaker", "other speaker"], 2: ["current", "history"]}

_CONFIG_NAME = re.compile(r"^(?P<model>[a-z_]+?)(?:_k(?P<k>\d+))?(?:_s(?P<seed>\d+))?$")


# ---------------------------------------------------------------- discovery

@dataclass(frozen=True)
class RunSpec:
    dataset: str
    model: str  # key of MODEL_INFO
    k: int  # history turns; 0 for tfidf_lr and single
    seed: Optional[int]  # None for tfidf_lr (deterministic)
    run_name: str
    config_path: Path

    @property
    def label(self) -> str:
        return MODEL_INFO[self.model].label


def config_specs(dataset: str, configs_dir: Path = CONFIGS_DIR) -> List[RunSpec]:
    """Every configured run for a dataset, parsed from the generated YAML file names."""
    specs = []
    for path in sorted((configs_dir / dataset).glob("*.yaml")):
        m = _CONFIG_NAME.match(path.stem)
        if not m or m["model"] not in MODEL_INFO:
            continue
        with open(path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        specs.append(RunSpec(dataset, m["model"], int(m["k"] or 0), int(m["seed"]) if m["seed"] else None,
                             cfg["run_name"], path))
    return specs


def models_for(dataset: str, configs_dir: Path = CONFIGS_DIR) -> Dict[str, List[int]]:
    """{model: sorted k values} configured for a dataset, in display order."""
    ks: Dict[str, set] = {}
    for s in config_specs(dataset, configs_dir):
        ks.setdefault(s.model, set()).add(s.k)
    return {m: sorted(ks[m]) for m in MODEL_ORDER if m in ks}


def seeds_for(dataset: str, configs_dir: Path = CONFIGS_DIR) -> List[int]:
    return sorted({s.seed for s in config_specs(dataset, configs_dir) if s.seed is not None})


def pick_spec(specs: Sequence[RunSpec], model: str, k: int, seed: int) -> Optional[RunSpec]:
    """The run for (model, k, seed). Models configured for one k only (e.g. ablations) use that k."""
    cands = [s for s in specs if s.model == model and (s.seed is None or s.seed == seed)]
    if not cands:
        return None
    exact = [s for s in cands if s.k == k]
    if exact:
        return exact[0]
    if len({s.k for s in cands}) == 1:  # tfidf_lr, single and k=3-only ablations
        return cands[0]
    return None


def find_checkpoint(run_dir: Path) -> Optional[Path]:
    """Locate the selected checkpoint of a neural run.

    Order: the path recorded in ``best.json`` (re-rooted onto this machine if it was written on the
    cluster), ``<run>/best.pt`` (a single file dropped in by hand), then ``lr_*/checkpoints/best.pt``
    (if several learning rates kept one, the one with the best dev Macro-F1 in ``epoch_metrics.jsonl``).
    """
    best_json = run_dir / "best.json"
    if best_json.exists():
        try:
            recorded = Path(json.loads(best_json.read_text(encoding="utf-8"))["checkpoint"])
        except (ValueError, KeyError):
            recorded = None
        if recorded is not None:
            parts = recorded.parts
            candidates = [recorded, ROOT / recorded]
            if run_dir.name in parts:  # cluster path -> same relative path under the local run dir
                candidates.append(run_dir.joinpath(*parts[parts.index(run_dir.name) + 1:]))
            for c in candidates:
                if c.is_file():
                    return c
    if (run_dir / "best.pt").is_file():
        return run_dir / "best.pt"
    found = sorted(run_dir.glob("lr_*/checkpoints/best.pt"))
    if len(found) <= 1:
        return found[0] if found else None

    def best_dev(ckpt: Path) -> float:
        metrics = ckpt.parents[1] / "epoch_metrics.jsonl"
        if not metrics.exists():
            return float("-inf")
        rows = [json.loads(line) for line in metrics.read_text(encoding="utf-8").splitlines() if line.strip()]
        return max((r.get("dev_macro_f1", float("-inf")) for r in rows), default=float("-inf"))

    return max(found, key=best_dev)


def encoder_dir_for(config: dict) -> Optional[Path]:
    """Local DistilBERT directory for a run: the configured path if present, else the default one."""
    configured = Path(config.get("model", {}).get("pretrained", ""))
    for c in (configured, ROOT / configured, ENCODER_DIR):
        if str(c) and (c / "config.json").exists() and (c / "vocab.txt").exists():
            return c
    return None


@dataclass
class ModelStatus:
    spec: Optional[RunSpec]
    model: str
    k: int
    state: str  # "ready" | "trainable" | "saved" (test-set CSVs only) | "missing"
    note: str
    checkpoint: Optional[Path] = None

    @property
    def usable(self) -> bool:
        return self.state in ("ready", "trainable")


def saved_predictions_path(run_dir: Path) -> Optional[Path]:
    p = run_dir / "predictions_test.csv"
    return p if p.exists() else None


def tfidf_model_path(run_name: str, runs_dir: Path = RUNS_DIR, cache_dir: Path = CACHE_DIR) -> Optional[Path]:
    for d in (runs_dir, cache_dir):
        p = d / run_name / "model.joblib"
        if p.exists():
            return p
    return None


def model_status(dataset: str, model: str, k: int, seed: int, *, configs_dir: Path = CONFIGS_DIR,
                 runs_dir: Path = RUNS_DIR, cache_dir: Path = CACHE_DIR,
                 processed_dir: Path = PROCESSED_DIR) -> ModelStatus:
    spec = pick_spec(config_specs(dataset, configs_dir), model, k, seed)
    if spec is None:
        return ModelStatus(None, model, k, "missing", f"not part of the {DATASET_NAMES[dataset]} experiments at k={k}")
    if model == "tfidf_lr":
        path = tfidf_model_path(spec.run_name, runs_dir, cache_dir)
        if path:
            return ModelStatus(spec, model, 0, "ready", f"loaded from {_rel(path)}", path)
        if processed_path(processed_dir, dataset, "train").exists():
            return ModelStatus(spec, model, 0, "trainable", "trains on first use (CPU, cached afterwards)")
        return ModelStatus(spec, model, 0, "missing", "no processed data; run `python prepare_data.py`")
    run_dir = runs_dir / spec.run_name
    ckpt = find_checkpoint(run_dir)
    saved = saved_predictions_path(run_dir)
    with open(spec.config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if ckpt is not None and encoder_dir_for(cfg) is not None:
        return ModelStatus(spec, model, spec.k, "ready", f"checkpoint {_rel(ckpt)}", ckpt)
    if saved is not None:  # no live model, but the cluster's test-set outputs are here
        return ModelStatus(spec, model, spec.k, "saved",
                           "saved test-set predictions only (no checkpoint): test-set dialogues only")
    if ckpt is None:
        return ModelStatus(spec, model, spec.k, "missing",
                           f"no checkpoint in {_rel(run_dir)}/ (copy it from the cluster)")
    return ModelStatus(spec, model, spec.k, "missing",
                       f"DistilBERT not found in {_rel(ENCODER_DIR)}; run `python prepare_data.py`", ckpt)


def _rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- predictors

@dataclass
class Prediction:
    labels: List[str]
    probs: np.ndarray  # (N, L)
    ms: float  # wall time for the whole dialogue, including tokenisation
    weights: Optional[np.ndarray] = None  # (N, S) fusion weights; 0 where unavailable
    avail: Optional[np.ndarray] = None  # (N, S) bool
    source_names: List[str] = field(default_factory=list)

    @property
    def pred(self) -> List[str]:
        return [self.labels[i] for i in self.probs.argmax(1)]

    @property
    def confidence(self) -> np.ndarray:
        return self.probs.max(1)


class TfidfPredictor:
    k = 0

    def __init__(self, bundle: dict):
        self.vectorizer = bundle["vectorizer"]
        self.classifier = bundle["classifier"]
        self.labels = list(bundle["labels"])

    @classmethod
    def load(cls, path: Path) -> "TfidfPredictor":
        import joblib

        return cls(joblib.load(path))

    def predict(self, records: Sequence[dict]) -> Prediction:
        from models.tfidf_lr import full_proba

        t0 = time.perf_counter()
        probs = full_proba(self.classifier, self.vectorizer.transform([r["text"] for r in records]),
                           len(self.labels))
        return Prediction(self.labels, probs, (time.perf_counter() - t0) * 1000)


def train_tfidf(spec: RunSpec, cache_dir: Path = CACHE_DIR, processed_dir: Path = PROCESSED_DIR) -> Path:
    """Re-run the configured TF-IDF grid (models/tfidf_lr.py) into the demo cache; return model.joblib."""
    from models.tfidf_lr import run

    with open(spec.config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    out_dir = cache_dir / spec.run_name
    config["output_dir"] = str(out_dir)
    config["data"]["processed_dir"] = str(processed_dir)
    if (out_dir / "DONE").exists() and not (out_dir / "model.joblib").exists():
        (out_dir / "DONE").unlink()  # half-cleaned cache: train again
    run(config)
    return out_dir / "model.joblib"


class NeuralPredictor:
    def __init__(self, model, collator, config: dict, labels: List[str]):
        self.model = model
        self.collator = collator
        self.config = config
        self.labels = labels
        mode = config["model"]["type"]
        self.k = 0 if mode == "single" else int(config["context"]["num_turns"])

    @classmethod
    def load(cls, checkpoint: Path, config_path: Optional[Path] = None) -> "NeuralPredictor":
        import torch
        from transformers import AutoTokenizer

        from models.batching import Collator
        from models.neural import build_model, input_mode

        state = torch.load(checkpoint, map_location="cpu", weights_only=False)
        config = state.get("config")
        if config is None:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)
        config = copy.deepcopy(config)
        encoder = encoder_dir_for(config)
        if encoder is None:
            raise FileNotFoundError(f"DistilBERT not found in {ENCODER_DIR}; run `python prepare_data.py`")
        mcfg = config["model"]
        mcfg["pretrained"] = str(encoder)
        labels = list(state.get("labels") or LABELS[config["data"]["dataset"]])

        model = build_model(mcfg, len(labels))
        model.load_state_dict(state["model"])
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(str(encoder))
        speaker_split = mcfg.get("fusion", {}).get("speaker_split", True)
        collator = Collator(input_mode(mcfg), tokenizer, config["context"]["max_utt_tokens"], speaker_split)
        return cls(model, collator, config, labels)

    def predict(self, records: Sequence[dict]) -> Prediction:
        import torch

        t0 = time.perf_counter()
        contexts = build_contexts(records, self.k)
        batch = self.collator([(c, 0) for c in contexts])
        with torch.no_grad():
            out = self.model(batch)
        probs = torch.softmax(out["logits"].float(), -1).numpy()
        ms = (time.perf_counter() - t0) * 1000
        if "weights" not in out:
            return Prediction(self.labels, probs, ms)
        w = out["weights"].float().numpy()
        return Prediction(self.labels, probs, ms, w, batch["avail"].numpy().astype(bool), SOURCE_NAMES[w.shape[1]])


class SavedPredictor:
    """Replays a run's saved test-set outputs (predictions_test.csv, fusion_weights_test.csv).

    Used when a neural run's CSVs are available but its checkpoint is not. It can only answer for
    utterances of the official test split, looked up by utterance_id; probabilities and fusion weights are
    exactly what the trained model produced on the cluster.
    """

    def __init__(self, probs: pd.DataFrame, labels: List[str], k: int, weights: Optional[pd.DataFrame] = None):
        self.probs = probs  # index utterance_id, columns = labels
        self.labels = labels
        self.k = k
        self.weights = weights  # index utterance_id, columns = sources, plus avail_<source>

    @classmethod
    def load(cls, run_dir: Path, labels: List[str], k: int) -> "SavedPredictor":
        pred = pd.read_csv(run_dir / "predictions_test.csv", dtype={"utterance_id": str})
        prob_cols = [f"prob_{lab}" for lab in labels]
        missing = [c for c in prob_cols if c not in pred.columns]
        if missing:
            raise ValueError(f"{run_dir}/predictions_test.csv lacks {missing}")
        probs = pred.set_index("utterance_id")[prob_cols]
        probs.columns = labels
        weights = None
        fw = run_dir / "fusion_weights_test.csv"
        if fw.exists():
            df = pd.read_csv(fw, dtype={"utterance_id": str}).set_index("utterance_id")
            keys = ["current", "same", "other"] if df["source_mode"].iloc[0] == "speaker_split" else ["current", "history"]
            weights = pd.DataFrame({name: df[f"w_{key}"] for key, name in zip(keys, SOURCE_NAMES[len(keys)])})
            for key, name in zip(keys, SOURCE_NAMES[len(keys)]):
                weights[f"avail_{name}"] = df[f"avail_{key}"].astype(bool)
        return cls(probs, labels, k, weights)

    def covers(self, records: Sequence[dict]) -> bool:
        return all(r["utterance_id"] in self.probs.index for r in records)

    def predict(self, records: Sequence[dict]) -> Prediction:
        ids = [r["utterance_id"] for r in records]
        pred = Prediction(self.labels, self.probs.loc[ids].to_numpy(dtype=float), float("nan"))
        if self.weights is not None and all(i in self.weights.index for i in ids):
            names = [c for c in self.weights.columns if not c.startswith("avail_")]
            rows = self.weights.loc[ids]
            pred.weights = rows[names].fillna(0.0).to_numpy(dtype=float)
            pred.avail = rows[[f"avail_{n}" for n in names]].to_numpy(dtype=bool)
            pred.source_names = names
        return pred


# ---------------------------------------------------------------- model size

DISTILBERT_BASE_PARAMS = 66_362_880  # distilbert-base-uncased, checked against the local copy in tests
DISTILBERT_HIDDEN = 768


def added_parameters(model_cfg: dict, num_labels: int, hidden: int = DISTILBERT_HIDDEN) -> int:
    """Trainable parameters a model adds on top of the shared encoder (mirrors models/neural.py)."""
    head = hidden * num_labels + num_labels
    if model_cfg["type"] != "fusion" or model_cfg["fusion"]["weighting"] != "learned":
        return head
    s = 3 if model_cfg["fusion"].get("speaker_split", True) else 2
    g = model_cfg["fusion"].get("gate_hidden", 256)
    return head + (s * hidden + s) * g + g + g * s + s


def model_sizes(dataset: str, k: int = 3, configs_dir: Path = CONFIGS_DIR) -> pd.DataFrame:
    """Per neural model: parameters added on top of the encoder, for the seed-42 run at k (or its only k)."""
    specs = config_specs(dataset, configs_dir)
    rows = []
    for m in MODEL_ORDER:
        spec = pick_spec(specs, m, k, 42)
        if spec is None or m == "tfidf_lr":
            continue
        with open(spec.config_path, encoding="utf-8") as f:
            mcfg = yaml.safe_load(f)["model"]
        added = added_parameters(mcfg, len(LABELS[dataset]))
        rows.append({"model": m, "k": spec.k, "added_params": added,
                     "added_pct": added / DISTILBERT_BASE_PARAMS,
                     "total_params": DISTILBERT_BASE_PARAMS + added})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- dialogues

def dialogue_records(turns: Sequence[tuple], dataset: str, dialogue_id: str = "demo") -> List[dict]:
    """Unified records from (speaker, text[, gold label]) tuples, in order."""
    out = []
    for i, turn in enumerate(turns):
        speaker, text = turn[0], turn[1]
        out.append({
            "dataset": dataset,
            "split": "demo",
            "dialogue_id": dialogue_id,
            "utterance_id": f"{dialogue_id}_u{i}",
            "turn_index": i,
            "speaker_ids": parse_meld_speakers(speaker) if speaker else [],
            "text": text.strip(),
            "label": turn[2] if len(turn) > 2 else None,
        })
    return out


def parse_dialogue(text: str) -> List[tuple]:
    """Parse ``Speaker: utterance`` lines. A line without a speaker prefix gets an unknown speaker."""
    turns = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        speaker, sep, utt = line.partition(":")
        if sep and utt.strip() and 0 < len(speaker.strip()) <= 40:
            turns.append((speaker.strip(), utt.strip()))
        else:
            turns.append(("", line))
    return turns


def _records_from_predictions(path: Path) -> List[dict]:
    """Test records rebuilt from a committed predictions CSV (eval/predictions.py layout)."""
    df = pd.read_csv(path, dtype={"dialogue_id": str, "utterance_id": str, "text": str, "label": str},
                     keep_default_na=False)
    return [{"dataset": r.dataset, "split": r.split, "dialogue_id": r.dialogue_id, "utterance_id": r.utterance_id,
             "turn_index": int(r.turn_index), "speaker_ids": json.loads(r.speaker_ids), "text": r.text,
             "label": r.label} for r in df.itertuples(index=False)]


def load_test_dialogues(dataset: str, processed_dir: Path = PROCESSED_DIR,
                        runs_dir: Path = RUNS_DIR) -> Dict[str, List[dict]]:
    """{dialogue_id: records in turn order} for the official test split.

    Reads data/processed if prepared, otherwise the TF-IDF run's committed predictions_test.csv
    (same records, same gold labels); {} if neither exists.
    """
    fallback = runs_dir / f"{dataset}_tfidf_lr" / "predictions_test.csv"
    if processed_path(processed_dir, dataset, "test").exists():
        records = load_split(processed_dir, dataset, "test")
    elif fallback.exists():
        records = _records_from_predictions(fallback)
    else:
        return {}
    dialogues: Dict[str, List[dict]] = {}
    for r in records:
        dialogues.setdefault(r["dialogue_id"], []).append(r)
    for recs in dialogues.values():
        recs.sort(key=lambda r: r["turn_index"])
    return dialogues


def context_for(records: Sequence[dict], index: int, k: int):
    """The UtteranceContext a k-turn model sees for one utterance (for display)."""
    return build_contexts(records, k)[index]


# ---------------------------------------------------------------- results

def load_results(path: Path = RESULTS_CSV) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["model_label"] = df["model"].map(lambda m: MODEL_INFO[m].label if m in MODEL_INFO else m)
    df["order"] = df["model"].map(lambda m: MODEL_ORDER.index(m) if m in MODEL_ORDER else len(MODEL_ORDER))
    return df.sort_values(["dataset", "order", "k"]).reset_index(drop=True)
