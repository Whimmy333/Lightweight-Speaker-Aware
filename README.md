# When Does Context Help? — Speaker-Aware Context Fusion for Conversational Emotion Recognition

EE6405 group project. Text-only emotion recognition on MELD and EmoryNLP (original text release),
comparing a TF-IDF baseline, single-utterance DistilBERT, context concatenation, fixed fusion and
adaptive speaker-aware fusion.

## Repository layout

```
prepare_data.py      download + normalise both datasets, write the data audit
data/                loaders.py (unified records), context.py (history windows), audit.py
  raw/               official files (created by prepare_data.py, not committed)
  processed/         unified JSONL records, one file per dataset/split (not committed)
models/              tfidf_lr.py (baseline); neural models are added in part 2
eval/                shared metrics (metrics.py) and prediction-file format (predictions.py)
configs/             one YAML file per run
outputs/             data_audit.md and runs/<run_name>/ for every experiment
app/                 Streamlit demo (later stage)
tests/               pytest suite for loaders and context construction
```

## 1. Install

Python 3.9–3.12 (developed on 3.12.4). From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`torch==2.5.1` from PyPI ships with CUDA 12.x on Linux. If the cluster driver only supports CUDA 11.8,
install torch first with
`pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu118`, then run the line above.

## 2. Prepare the data

```bash
python prepare_data.py
```

This downloads the six official files, pinned to a fixed commit of each repository and checked by SHA-256:

| dataset | files | source |
|---|---|---|
| MELD | `train_sent_emo.csv`, `dev_sent_emo.csv`, `test_sent_emo.csv` | `declare-lab/MELD`, `data/MELD/` |
| EmoryNLP (original text release) | `emotion-detection-trn.json`, `-dev.json`, `-tst.json` | `emorynlp/emotion-detection`, `json/` |

It then writes `data/processed/<dataset>/<split>.jsonl`, `data/processed/manifest.json`, and the audit
report `outputs/data_audit.md` (split sizes vs. the proposal, label distribution, duplicates, leakage checks,
context availability).

**No internet on the machine?** Copy the six files to `data/raw/meld/` and `data/raw/emorynlp/` with
the file names above and run `python prepare_data.py --no-download`. The script refuses files whose
checksum differs from the pinned version unless you pass `--allow-checksum-mismatch`.

### Record format

Each JSONL line has `dataset`, `split`, `dialogue_id`, `utterance_id`, `turn_index`, `speaker_ids`,
`text`, `label`. `turn_index` is the 0-based position inside the dialogue; it is needed because MELD
utterance ids have gaps. Text keeps the original punctuation, casing and negation. Official splits are
kept as released.

### Context construction (`data/context.py`)

`build_contexts(records, num_turns)` returns, for every utterance, the previous `num_turns` (1, 3 or 5)
utterances of the same dialogue, oldest first, each marked as same-speaker (speaker sets overlap) or
other-speaker. The first turn of a dialogue has an empty history. Gold labels of history turns are
never copied into a context.

## 3. TF-IDF + Logistic Regression baseline

```bash
python -m models.tfidf_lr --config configs/meld_tfidf_lr.yaml
python -m models.tfidf_lr --config configs/emorynlp_tfidf_lr.yaml
```

Fitted on the training split only. The grid in the config is scored on dev Macro-F1, and the selected
model is evaluated on dev and test. Each run writes to `outputs/runs/<run_name>/`:

| file | content |
|---|---|
| `config.yaml` | copy of the config used |
| `grid_search.csv` | dev scores for every grid point |
| `metrics_dev.json`, `metrics_test.json` | Macro-F1, Weighted-F1, accuracy, per-class P/R/F1, confusion matrix |
| `predictions_dev.csv`, `predictions_test.csv` | one row per utterance: ids, text, gold `label`, `pred`, `prob_<class>` |
| `report.md` | the same metrics as readable tables |
| `model.joblib` | fitted vectoriser + classifier (not committed) |

## 4. Tests

```bash
python -m pytest
```

The tests build small synthetic MELD/EmoryNLP files, so they need no download. Two extra tests check
the real processed data and are skipped if `prepare_data.py` has not been run.
