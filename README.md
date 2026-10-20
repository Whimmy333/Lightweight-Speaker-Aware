# When Does Context Help? — Speaker-Aware Context Fusion for Conversational Emotion Recognition

EE6405 group project. Text-only emotion recognition on MELD and EmoryNLP (original text release).
We compare a TF-IDF baseline, single-utterance DistilBERT, context concatenation, fixed fusion and
adaptive speaker-aware fusion, plus ablations and a context-length study.

**Running the experiments on a GPU machine?** Follow sections 1–4 in order. Everything is one
command per step, and every step can be rerun safely.

## 1. Install

Python 3.9–3.12 (developed on 3.12.4). From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"   # expect: 2.5.1 True
```

`torch==2.5.1` from PyPI ships with CUDA 12.x on Linux. If `nvidia-smi` shows a driver that only
supports CUDA 11.8, install torch first with
`pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu118`, then run
`pip install -r requirements.txt`.

## 2. Prepare data and the encoder (needs internet once)

```bash
python prepare_data.py
```

This downloads:

| what | where it goes | source (pinned) |
|---|---|---|
| MELD `train/dev/test_sent_emo.csv` | `data/raw/meld/` | `declare-lab/MELD`, commit `ca3e126`, SHA-256 checked |
| EmoryNLP `emotion-detection-trn/dev/tst.json` | `data/raw/emorynlp/` | `emorynlp/emotion-detection`, commit `28df4a2`, SHA-256 checked |
| DistilBERT (`distilbert-base-uncased`) | `data/pretrained/distilbert-base-uncased/` | Hugging Face revision `12040ac` |

It then writes the unified records to `data/processed/<dataset>/<split>.jsonl` and the data audit to
`outputs/data_audit.md`.

**Cluster compute nodes without internet:** run `python prepare_data.py` once on a login node (or any
machine with internet, then copy `data/` over). After that, nothing downloads anything; the training
jobs read only local files.

**Downloads blocked entirely?** Put the six dataset files into `data/raw/meld/` and `data/raw/emorynlp/`
(official file names), and `config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json`,
`vocab.txt` from the Hugging Face revision above into `data/pretrained/distilbert-base-uncased/`, then run
`python prepare_data.py --no-download`.

## 3. Pre-flight check (about 20 min on CPU)

```bash
bash run_all.sh --smoke
```

Runs every config with 50 utterances per split, 1 epoch, on CPU, writing to `outputs/smoke/` (no
checkpoints kept). It should end with `all selected runs finished`. This catches environment problems
before you spend GPU hours. To check just one model: `python train.py --config configs/meld/adaptive_k3_s42.yaml --smoke`.

## 4. Run all experiments (GPU)

```bash
bash run_all.sh 2>&1 | tee run_all.log
```

- Runs 44 configs in priority order: TF-IDF, MELD main comparison, EmoryNLP replication, the
  speaker-merge ablation, then the 1- and 5-turn context study.
- Each neural config trains with lr 2e-5 and 5e-5 (5 epochs each) and keeps the best (lr, epoch) on
  dev Macro-F1. That is 84 training runs in total.
- **Rerunnable:** a finished run (`outputs/runs/<run>/DONE`) is skipped; an interrupted one resumes from
  its last finished epoch. If the job is killed or times out, submit the same command again.
- A failed run is logged and the script continues; it exits with code 1 and lists the failures at the end.
  Progress is appended to `outputs/run_all_status.log` (`OK`/`FAIL`, config, seconds).
- **Split across several jobs/GPUs** by passing path patterns, e.g. `bash run_all.sh emorynlp/`,
  `bash run_all.sh _s42`, `bash run_all.sh meld/adaptive meld/fixed`. Do not run the same config in two
  jobs at once.
- Disk: about 0.25 GB per finished run for its selected checkpoint (≈11 GB in total), plus one
  temporary 0.8 GB resume file per running job.
- Mixed precision is used automatically on CUDA (bf16 if supported, otherwise fp16).

Example SLURM job (adjust partition, time and paths to the cluster):

```bash
#!/bin/bash
#SBATCH --job-name=ee6405
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=run_all_%j.log
cd /path/to/Lightweight-Speaker-Aware
source .venv/bin/activate
bash run_all.sh
```

## 5. Where the results are

| path | content |
|---|---|
| `outputs/results_summary.md` | mean ± std over seeds 42/43/44: main comparison, per-class F1, context length, ablations |
| `outputs/results_summary.csv`, `outputs/results_runs.csv` | the same numbers per group and per run |
| `outputs/run_all_status.log` | one line per config: OK/FAIL and duration |
| `outputs/data_audit.md` | split sizes, label distribution, duplicate and leakage checks |
| `outputs/runs/<run_name>/` | everything for one run (below) |

Inside `outputs/runs/<run_name>/`:

| file | content |
|---|---|
| `config.yaml` | exact config used |
| `train.log` | full log (appended on resume) |
| `lr_<lr>/epoch_metrics.jsonl` | dev Macro-F1, Weighted-F1, per-class F1 and train loss after every epoch |
| `best.json` | selected lr and epoch, dev Macro-F1, path of the best checkpoint |
| `lr_<lr>/checkpoints/best.pt` | best checkpoint (only for the selected lr) |
| `metrics_dev.json`, `metrics_test.json` | Macro-F1, Weighted-F1, accuracy, per-class P/R/F1, confusion matrix |
| `predictions_dev.csv`, `predictions_test.csv` | per utterance: ids, speakers, text, gold `label`, `pred`, `prob_<class>` |
| `fusion_weights_dev.csv`, `fusion_weights_test.csv` | fusion models: per-utterance source availability and weights |
| `metrics_*_equal_weights.json` | adaptive models: same checkpoint with the gate replaced by equal weights |
| `latency.json` | end-to-end inference latency (tokenisation + forward), hardware |
| `report.md` | readable summary of the run |

`fusion_weights_*.csv` columns: `dataset, split, dialogue_id, utterance_id, turn_index, label, pred,
source_mode, n_same, n_other, avail_current, avail_same, avail_other, avail_history, w_current, w_same,
w_other, w_history`. Speaker-split models fill current/same/other and leave `*_history` empty; the
merged ablation fills current/history and leaves `*_same`/`*_other` empty. `avail=0` with `w=0` means the
source was missing (e.g. the first turn) and was masked.

**Sending results back:** commit `outputs/` (checkpoints are git-ignored) or copy it. Keep the `best.pt`
files of the main MELD runs if the demo needs them.

To rebuild the summary at any time: `python -m eval.aggregate`.

## 6. Experiments

| configs | question | seeds |
|---|---|---|
| `{meld,emorynlp}/tfidf_lr.yaml` | traditional baseline (deterministic, one run) | – |
| `meld/{single,concat_k3,fixed_k3,adaptive_k3}_s*.yaml` | main MELD comparison | 42, 43, 44 |
| `emorynlp/{concat,fixed,adaptive}_k3_s*.yaml` | replication on EmoryNLP | 42, 43, 44 |
| `meld/adaptive_merged_k3_s*.yaml` | does separating same/other-speaker history help? | 42, 43, 44 |
| `meld/fixed_k3_s*.yaml` vs `adaptive_k3` | does learning the weights help? (equal-weights ablation) | 42, 43, 44 |
| `meld/{concat,fixed,adaptive}_k{1,3,5}_s*.yaml` | when does more history help or interfere? | 42, 43, 44 |

The equal-weights ablation needs no extra training: replacing the adaptive gate with equal weights while
keeping the rest of the architecture is exactly the `fixed` model. Each adaptive run additionally reports
its own checkpoint evaluated with equal weights (`metrics_*_equal_weights.json`).

## 7. How the models work

- **Data** (`data/loaders.py`): one record per utterance with `dataset, split, dialogue_id, utterance_id,
  turn_index, speaker_ids, text, label`. Official splits, original punctuation/casing/negation.
  `turn_index` is the position in the dialogue (MELD utterance ids have gaps).
- **Context** (`data/context.py`): the previous k utterances (k = 1, 3, 5) of the same dialogue, oldest
  first, split into same-speaker (speaker sets overlap) and other-speaker turns. The first turn has no
  history. Gold labels of history turns never enter the input.
- **Shared token budget** (`models/batching.py`): every utterance, current or history, is cut to its first
  80 word pieces, for every model, so all models see exactly the same text. Single:
  `[CLS] current [SEP]`. Concat: `[CLS] current [SEP] h_-k [SEP] … h_-1 [SEP]` (max 487 tokens at k=5).
  Fusion: each utterance encoded separately.
- **Models** (`models/neural.py`): all use the same pretrained DistilBERT encoder and take the `[CLS]`
  vector of each sequence, followed by a dropout + linear classifier.
  - *Fixed fusion*: mean-pool history vectors per group, then
    `z = w_current*h_current + w_same*h_same + w_other*h_other` with equal weights over the available sources.
  - *Adaptive fusion*: same, but a feed-forward gate (input: the three vectors and availability flags) with
    a masked softmax produces per-utterance weights that sum to 1 over available sources. Missing groups
    get weight 0, so the first turn uses the current utterance only. The gate's output layer starts at
    zero, i.e. training starts from the fixed-fusion weights.
  - *Merged ablation*: same- and other-speaker history pooled into one source (weights over 2 sources).
- **Training** (`models/trainer.py`): AdamW (weight decay 0.01), linear warm-up (10%) and decay, batch 16,
  cross-entropy, gradient clipping 1.0, up to 5 epochs, lr 2e-5 and 5e-5 each tried once from the same
  seed. The checkpoint with the best dev Macro-F1 is evaluated on test once.
- **Evaluation** (`eval/`): shared metrics, prediction/fusion-weight file formats, latency, aggregation.
  Latency is measured on 300 test utterances, batch size 1, after 10 warm-up batches, on the training device.
- **TF-IDF baseline** (`models/tfidf_lr.py`): fitted on train only; the grid in the config is scored on
  dev Macro-F1. Keeps negations and `!`/`?` as features.

## 8. Changing settings

All hyper-parameters are in the YAML configs, which are generated from one file:

```bash
# edit the constants in configs/generate_configs.py, then
python configs/generate_configs.py
```

For a one-off change use `--override`, e.g.
`python train.py --config configs/meld/concat_k3_s42.yaml --override train.batch_size=8`.
A run directory remembers its config: resuming with a different config is refused, so use a new
`run_name`/`output_dir` or delete the old run directory.

## 9. Repository layout

```
prepare_data.py      download + normalise data, fetch DistilBERT, write the data audit
train.py             single entry point: python train.py --config <yaml> [--smoke] [--override k=v ...]
run_all.sh           every experiment in priority order, then the summary
data/                loaders.py, context.py, audit.py (raw/, processed/, pretrained/ are not committed)
models/              tfidf_lr.py, batching.py, neural.py, trainer.py
eval/                metrics.py, predictions.py, latency.py, aggregate.py
configs/             generate_configs.py and the 44 generated YAML files
outputs/             data_audit.md, runs/<run_name>/, results_summary.*
app/                 Streamlit demo (later stage)
tests/               pytest suite
```

## 10. Tests

```bash
python -m pytest
```

Covers the loaders, context construction (first turn, window sizes, speaker split, no label leakage),
batching under the token budget, fusion masking and weights, every model type end to end on a tiny
randomly initialised encoder, crash/resume, and the aggregation. Needs no download; two tests that read
the real processed data are skipped if `prepare_data.py` has not been run.
