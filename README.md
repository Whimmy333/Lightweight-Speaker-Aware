
# When Does Context Help? Lightweight Speaker-Aware Context Fusion for Conversational Emotion Recognition

EE6405 Natural Language Processing, group project.

Each utterance in a dialogue receives one emotion label from its text, its speaker and the preceding turns. We build a lightweight adaptive fusion module that decides how much to rely on the current utterance, the same speaker's earlier turns and other speakers' turns.

The main controlled comparisons use **MELD** and **EmoryNLP**. We add **DailyDialog** as a third, supplementary benchmark to examine how context methods behave on a different dialogue corpus.

DailyDialog does not provide explicit speaker IDs in the standard text release. Its experiments therefore use speaker-independent history fusion and do not test whether separating same-speaker history from other-speaker history helps.

> **Status.** The original study (57 configurations on MELD, EmoryNLP and DailyDialog) has finished on the cluster; its results are in [outputs/results_summary.md](outputs/results_summary.md) and summarised under [Results so far](#results-so-far). A second GPU batch (other encoders, the EmoryNLP single-utterance baseline and a hyper-parameter sweep) and the traditional term-weighting × classifier baselines are in progress. Everything is on `main`; `feature/dailydialog-support` has been merged. **Preparing the video?** See [For the presentation: where to find things](#for-the-presentation-where-to-find-things).

| Document | Purpose |
|---|---|
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | Data, models, protocol, decisions and limitations |
| [docs/HANDOVER2.md](docs/HANDOVER2.md) | Analysis of the first GPU batch (main results, ablations, latency) |
| [docs/HYPERPARAMETERS.md](docs/HYPERPARAMETERS.md) | Hyper-parameter effects: data files and plotting examples |
| [app/README.md](app/README.md) | Streamlit demo |
| [docs/HANDOVER.md](docs/HANDOVER.md), [docs/HANDOVER3.md](docs/HANDOVER3.md) | Running the first and second GPU batches on NTU EEE Cluster 02 |
| [notebooks/data_cleaning.ipynb](notebooks/data_cleaning.ipynb) | Data cleaning and checks |
| [outputs/data_audit.md](outputs/data_audit.md) | Split sizes, labels, duplicates and overlap checks |

---

## Why this project is useful

**The problem is real.** Many conversational replies are ambiguous on their own. A short response such as "Fine." may express different emotions depending on the preceding dialogue. History can help resolve the ambiguity, but more history costs compute and can introduce irrelevant information.

**The experiments isolate the source of improvement.** Neural models share the same encoder, per-utterance token budget and tuning protocol. We compare:

1. **Context length:** does more history help, or does it interfere? The main study compares 1, 3 and 5 previous turns.
2. **Speaker separation:** does distinguishing a speaker's own history from other speakers' history help? This ablation is conducted on datasets with speaker IDs.
3. **Fusion strategy:** does learning per-utterance source weights outperform context concatenation or equal-weight fusion?

**The model is interpretable.** Speaker-aware fusion records the availability and weight of the current, same-speaker and other-speaker sources. Speaker-independent fusion uses the current utterance and the combined history as its two sources.

**The method is lightweight.** The fusion module uses a shared DistilBERT encoder and a small fusion head. End-to-end latency, including tokenisation, is measured for the evaluated models.

**The benchmarks serve different purposes.** MELD and EmoryNLP are based on *Friends* and provide speaker annotations. DailyDialog provides a third corpus with a different label set and no explicit speaker IDs in its standard text release. DailyDialog can test cross-dataset behaviour of context methods, but it cannot establish the value of speaker-identity separation.

## What we built

### Method

A shared DistilBERT encodes the current utterance and each retained history utterance. The fusion model mean-pools history vectors by source group, then uses masked source weights to combine the resulting representations.

For speaker-aware fusion:

\[
z = w_{\mathrm{current}}h_{\mathrm{current}}
  + w_{\mathrm{same}}h_{\mathrm{same}}
  + w_{\mathrm{other}}h_{\mathrm{other}}
\]

A source that is unavailable receives zero weight. Therefore, the first turn of a dialogue uses the current utterance alone.

For speaker-independent fusion, the two sources are:

- the current utterance;
- all available history turns, pooled together.

The latter is the intended fusion design for DailyDialog. Missing speaker IDs are treated as unknown, not as evidence that two utterances belong to different speakers.

### Experimental controls

- One shared encoder for the neural models.
- A per-utterance token limit of 80 word pieces.
- The same optimiser and training schedule across comparable neural models.
- Learning-rate and epoch selection using dev Macro-F1.
- Three seeds (42, 43 and 44) for the main neural comparisons.
- Gold emotion labels from history turns are never passed into model inputs.
- Original text casing, punctuation and negation are preserved; only outer whitespace is stripped.
- Official train/dev/test splits are retained.

### Data audit

The audit checks split sizes, label distributions, duplicate dialogues, repeated text and cross-split overlap. The original MELD/EmoryNLP checks also investigate repeated *Friends* scene content.

DailyDialog has no *Friends* scene metadata, so repeated text is reported as textual overlap rather than being described as a reused scene. Flagged items are documented for interpretation and sensitivity analysis; the official splits are not silently modified.

### Reproducibility

MELD and EmoryNLP downloads use pinned revisions and SHA-256 checks. DailyDialog is downloaded from the dataset archive linked by the original paper; the script records the extracted files' SHA-256 digests, but those digests must not be interpreted as verification against a pinned expected checksum unless such a checksum has been configured.

DistilBERT uses a pinned Hugging Face revision. Training should use the prepared local encoder rather than requiring network access during model training.

---

## Results so far

Test Macro-F1 of the original study, k = 3, mean ± std over seeds 42, 43 and 44 (TF-IDF + LR is one deterministic run). Checkpoints were selected on dev Macro-F1. Source: [outputs/results_summary.md](outputs/results_summary.md); analysis: [docs/HANDOVER2.md](docs/HANDOVER2.md).

| Model | MELD | EmoryNLP | DailyDialog |
|---|---:|---:|---:|
| Always predicting the most frequent class | 0.093 | 0.059 | 0.128 |
| TF-IDF + LR | 0.360 | 0.286 | 0.437 |
| Single-utterance DistilBERT | 0.437 ± 0.007 | in progress | 0.478 ± 0.028 |
| Concatenation | 0.428 ± 0.012 | 0.292 ± 0.011 | 0.488 ± 0.022 |
| Fixed fusion (equal weights) | 0.361 ± 0.008 | 0.248 ± 0.004 | 0.480 ± 0.012 |
| Adaptive fusion (ours) | 0.438 ± 0.006 | 0.282 ± 0.007 | 0.489 ± 0.006 |

DailyDialog has no speaker IDs, so its fusion models pool all history into one source (`fixed_merged`, `adaptive_merged`).

- **The learned gate matters.** Adaptive fusion clearly beats fixed fusion. Replacing the trained gate with equal weights at inference drops MELD from 0.438 to 0.349.
- **Context adds little.** Adaptive fusion ties the single-utterance model on MELD (0.438 vs 0.437) and concatenation elsewhere; the differences are within the seed spread.
- **Speaker separation shows no clear gain** on MELD (0.438 separated vs 0.435 pooled).
- **Context length:** adaptive fusion rises slightly with k on MELD (0.434, 0.438, 0.443 for k = 1, 3, 5); concatenation stays flat.
- **Cost:** on MELD, adaptive fusion takes 4.9 ms per utterance on the cluster GPU vs 4.0 ms for concatenation and single-utterance models.

No significance test has been run yet, so small differences should not be called improvements.

---

## For the presentation: where to find things

Everything below is on `main`. "Now" means the file is already in the repository. "After batch 1" needs the per-run folders of the first GPU batch, which are still on the cluster. "After batch 2" needs the second GPU batch ([docs/HANDOVER3.md](docs/HANDOVER3.md)). Rebuild the tables after new runs arrive (see the end of this section).

**A: problem, audience and research questions (slides 1–4, 18–19)**

| Topic | Where | Status |
|---|---|---|
| Problem, audience, purpose | The group proposal (PDF, not in the repository); [Why this project is useful](#why-this-project-is-useful) | Now |
| Problem statement and the three research questions | [docs/TECHNICAL.md §1](docs/TECHNICAL.md#1-problem-and-research-questions) | Now |
| Answers to the research questions | [Results so far](#results-so-far), [docs/HANDOVER2.md §8](docs/HANDOVER2.md) | Now |

**B: idea, architecture, data and design choices (slides 5–9)**

| Topic | Where | Status |
|---|---|---|
| Related work, CoMPM comparison, fusion formula, gate size | [docs/TECHNICAL.md §4](docs/TECHNICAL.md#4-models), [Method](#method) | Now |
| Architecture code | [models/neural.py](models/neural.py) (`FusionClassifier`) | Now |
| Datasets, splits, labels, imbalance, duplicates | [docs/TECHNICAL.md §2](docs/TECHNICAL.md#2-data), [outputs/data_audit.md](outputs/data_audit.md) | Now |
| Training settings and why | [docs/TECHNICAL.md §5 and §9](docs/TECHNICAL.md#5-training-and-model-selection) | Now |
| Parameter counts per model, full hyper-parameter table, learning rate and epoch each run selected | `outputs/model_details.md` (`python -m eval.model_details`) | Being added |
| How hyper-parameters change results | [docs/HYPERPARAMETERS.md](docs/HYPERPARAMETERS.md), `outputs/hparams_summary.md` | Traditional models being added (run `python -m eval.hparams`); learning rate × epoch after batch 1; sweep after batch 2 |
| Engineering: pinned data, config generator, resumable runs, tests | [docs/TECHNICAL.md §10](docs/TECHNICAL.md#10-engineering-reproducibility-and-testing), [tests/](tests/) (`python -m pytest -q`: 114 tests) | Now |

**C: experiments and results (slides 10–14)**

| Topic | Where | Status |
|---|---|---|
| Baselines, metrics, seeds, selection protocol | [docs/TECHNICAL.md §6–7](docs/TECHNICAL.md#6-evaluation) | Now |
| Main comparison, per-class F1, latency | [outputs/results_summary.md](outputs/results_summary.md) "main comparison" | Now |
| Chart data (mean and std per model, dataset and k) | [outputs/results_summary.csv](outputs/results_summary.csv); per seed: [outputs/results_runs.csv](outputs/results_runs.csv) | Now |
| Context length (k = 1, 3, 5) and ablations | [outputs/results_summary.md](outputs/results_summary.md) "context length", "ablations" | Now |
| GPU time per configuration | [outputs/run_all_status.log](outputs/run_all_status.log) (7.75 h in total on one A40) | Now |
| Other encoders (BERT, RoBERTa, RNN/LSTM/GRU) and term weighting × classifier | `outputs/results_summary.md` "encoder comparison", "term weighting x classifier"; chart data in `outputs/results_comparison.csv` | Traditional models being added; encoders after batch 2 |

**D: interpretation and demo (slides 15–17)**

| Topic | Where | Status |
|---|---|---|
| What the results mean, what not to overstate | [docs/HANDOVER2.md](docs/HANDOVER2.md), [Results so far](#results-so-far) | Now |
| Gate weights per utterance (how much the model trusts each source) | [outputs/runs/meld_adaptive_k3_s42/fusion_weights_test.csv](outputs/runs/meld_adaptive_k3_s42/fusion_weights_test.csv) (seed 42) | Now; other seeds after batch 1 |
| Limitations | [docs/TECHNICAL.md §11](docs/TECHNICAL.md#11-limitations-and-risks) | Now |
| Live demo | [app/](app/) (`streamlit run app/streamlit_app.py`; setup in [app/README.md](app/README.md)) | Now |

**Rebuilding the tables.** Each command reads `outputs/runs/`, so run it after pulling new run folders:

```bash
python -m eval.aggregate        # results_summary.md / .csv, results_comparison.csv
python -m eval.model_details    # model_details.md
python -m eval.hparams          # hparams_summary.md and hparams_*.csv
```

Until the first batch's run folders are in the repository, `eval.aggregate` stops with an error instead of rebuilding `results_summary.*` from the few runs present locally; the committed cluster results stay as they are. `eval.model_details` and `eval.hparams` only write their own files.

---

## Quick start

### On NTU EEE Cluster 02

Use the repository's Slurm job scripts in the appropriate SSD project directory. Do not run package installations or long training jobs on the login node.

```bash
sbatch cluster/setup.sbatch
sbatch cluster/smoke.sbatch
sbatch cluster/gpu_check.sbatch
sbatch cluster/train.sbatch
```

Review [docs/HANDOVER.md](docs/HANDOVER.md) for the cluster-specific setup and execution instructions. Check that its scripts include the new DailyDialog configurations before using them for the full experiment matrix.

### In a local Python environment

Use a supported Python version from the project's environment documentation.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python prepare_data.py
python configs/generate_configs.py
python -m pytest
```

After the tests pass, run a smoke test for the DailyDialog configurations:

```bash
bash run_all.sh --smoke dailydialog/
```

This should be used as a short pre-flight check, not as the final experiment. Check the smoke-test logs and outputs before scheduling full GPU training.

To run all configured experiments:

```bash
bash run_all.sh
```

To use prepared data without having the script rewrite it, set `SKIP_PREPARE=1`:

```bash
SKIP_PREPARE=1 bash run_all.sh --smoke dailydialog/
```

Only use this option after confirming that the required processed data and encoder are already available.

To run one configuration:

```bash
python train.py --config configs/meld/adaptive_k3_s42.yaml
```

Hyperparameters are defined in the YAML files generated by `configs/generate_configs.py`; edit the generator rather than editing generated configurations by hand.

---

## Experiments

### Main experiments: MELD

| Configuration | Research question | Seeds |
|---|---|---|
| `meld/tfidf_lr.yaml` | Traditional text-classification baseline | Deterministic |
| `meld/single_s*.yaml` | Current utterance only | 42, 43, 44 |
| `meld/concat_k3_s*.yaml` | Context concatenation | 42, 43, 44 |
| `meld/fixed_k3_s*.yaml` | Equal-weight speaker-aware fusion | 42, 43, 44 |
| `meld/adaptive_k3_s*.yaml` | Learned speaker-aware fusion | 42, 43, 44 |
| `meld/adaptive_merged_k3_s*.yaml` | Ablation: merge same/other speaker history | 42, 43, 44 |
| `meld/{concat,fixed,adaptive}_k{1,3,5}_s*.yaml` | Effect of context length | 42, 43, 44 |

### Replication: EmoryNLP

| Configuration | Purpose | Seeds |
|---|---|---|
| `emorynlp/tfidf_lr.yaml` | Traditional baseline | Deterministic |
| `emorynlp/{concat,fixed,adaptive}_k3_s*.yaml` | Replicate the main context comparison | 42, 43, 44 |
| `emorynlp/single_s*.yaml` | Current utterance only | 42, 43, 44 |

### Supplementary benchmark: DailyDialog

| Configuration | Purpose | Seeds |
|---|---|---|
| `dailydialog/tfidf_lr.yaml` | Traditional baseline | Deterministic |
| `dailydialog/single_s*.yaml` | Current utterance only | 42, 43, 44 |
| `dailydialog/concat_k3_s*.yaml` | Concatenate the previous three turns | 42, 43, 44 |
| `dailydialog/fixed_merged_k3_s*.yaml` | Equal-weight current/history fusion | 42, 43, 44 |
| `dailydialog/adaptive_merged_k3_s*.yaml` | Learned current/history fusion | 42, 43, 44 |

DailyDialog uses the merged-history variants because speaker identities are not available. Its results should be reported separately from the MELD speaker-separation ablation.

### Model comparison: other encoders and traditional baselines

| Configuration | Purpose | Seeds |
|---|---|---|
| `meld/{bert,roberta}_single_s*.yaml`, `meld/{bert,roberta}_{concat,fixed,adaptive}_k3_s*.yaml` | Same architectures with BERT-base or RoBERTa-base instead of DistilBERT | 42, 43, 44 |
| `meld/{rnn,birnn,lstm,bilstm,gru,bigru}_single_s*.yaml`, `..._concat_k3_s*.yaml` | Recurrent encoders over DistilBERT's frozen word-piece embeddings | 42, 43, 44 |
| `meld/bilstm_{fixed,adaptive}_k3_s*.yaml` | Fusion on a recurrent encoder | 42, 43, 44 |
| `<dataset>/{binary,tf,tfidf,bm25}_{lr,svm,mnb,cnb,rf}.yaml` | Term weighting × classifier, current utterance only (CPU) | Deterministic |
| `meld/sweep_{single,adaptive_k3}_{lr*,bs*,do*}_s*.yaml` | Learning rate, batch size and dropout changed one at a time | 42, 43, 44 |

The original plan above has **57 configurations**: 3 TF-IDF configurations and 54 neural configurations. The model comparison adds 126 (3 EmoryNLP single, 66 encoder-comparison and 57 traditional) and the hyper-parameter sweep 54, for **237** in total. Neural configurations try the two configured learning rates and select the best dev Macro-F1 checkpoint. `python -m eval.model_details` writes parameter counts and hyper-parameter tables to `outputs/model_details.md`; `python -m eval.hparams` collects hyper-parameter effects for plots ([docs/HYPERPARAMETERS.md](docs/HYPERPARAMETERS.md)). The generated configuration files are the source of truth for the exact run settings.

---

## Data

| Dataset | Train / dev / test utterances | Labels | License |
|---|---:|---|---|
| MELD | 9,989 / 1,109 / 2,610 | anger, disgust, fear, joy, neutral, sadness, surprise | GPL-3.0 |
| EmoryNLP (original text release) | 9,934 / 1,344 / 1,328 | joyful, mad, neutral, peaceful, powerful, sad, scared | Apache-2.0 |
| DailyDialog | 87,170 / 8,069 / 7,740 | anger, disgust, fear, happiness, no_emotion, sadness, surprise | CC BY-NC-SA 4.0 |

DailyDialog split counts refer to utterances, not dialogues. Its published emotion IDs map as follows:

| Raw ID | Label |
|---:|---|
| 0 | `no_emotion` |
| 1 | `anger` |
| 2 | `disgust` |
| 3 | `fear` |
| 4 | `happiness` |
| 5 | `sadness` |
| 6 | `surprise` |

`no_emotion` remains a separate class; it is not mapped to `neutral`. DailyDialog does not supply explicit speaker IDs in the standard text release, so its `speaker_ids` values are empty lists.

Dataset references:

- [MELD project](https://github.com/declare-lab/MELD)
- [EmoryNLP emotion-detection repository](https://github.com/emorynlp/emotion-detection)
- [DailyDialog paper and dataset link](https://aclanthology.org/I17-1099/)
- [DailyDialog dataset card and licence](https://huggingface.co/datasets/ConvLab/dailydialog)

### Unified record format

Every processed utterance uses the same schema:

```text
dataset, split, dialogue_id, utterance_id, turn_index, speaker_ids, text, label
```

Files are written to:

```text
data/processed/<dataset>/<split>.jsonl
```

Raw and processed data, along with encoder weights, are not committed to the repository.

DailyDialog raw files are expected under `data/raw/dailydialog/`:

```text
data/raw/dailydialog/
├── dialogues_train.txt
├── dialogues_emotion_train.txt
├── dialogues_validation.txt
├── dialogues_emotion_validation.txt
├── dialogues_test.txt
└── dialogues_emotion_test.txt
```

The dataset preparation script downloads the archive and extracts the required dialogue and emotion files. If automatic download fails, the same six files can be placed in that directory manually.

---

## Where results go

| Path | Content |
|---|---|
| `outputs/results_summary.md` | Aggregated comparison across completed runs |
| `outputs/model_details.md` | Parameter counts and hyper-parameter tables (`python -m eval.model_details`) |
| `outputs/runs/<run_name>/params.json` | Parameter counts of the run's model |
| `outputs/runs/<run_name>/metrics_dev.json` | Dev metrics and per-class evaluation |
| `outputs/runs/<run_name>/metrics_test.json` | Test metrics and per-class evaluation |
| `outputs/runs/<run_name>/predictions_dev.csv` | Per-utterance dev predictions and probabilities |
| `outputs/runs/<run_name>/predictions_test.csv` | Per-utterance test predictions and probabilities |
| `outputs/runs/<run_name>/fusion_weights_*.csv` | Fusion source availability and weights |
| `outputs/runs/<run_name>/` | Configuration, logs, checkpoints and latency outputs |
| `outputs/flagged_dialogues.csv` | Dialogues flagged for overlap or duplication |
| `outputs/data_audit.md` | Dataset audit and preprocessing notes |

A run's result files are meaningful only after that run has completed successfully. Do not add pending results to tables as though they were measured.

---

## Repository layout

```text
prepare_data.py      Download/prepare datasets, fetch encoders and write audit
train.py             One entry point for configured experiments
run_all.sh           Run configured experiments and aggregate results
data/
  loaders.py         Unified loaders and record format
  context.py         History windows and speaker relations
  audit.py           Split, label, duplicate and overlap checks
models/
  tfidf_lr.py        TF-IDF + Logistic Regression
  classical.py       Term weighting x classifier baselines
  batching.py        Token budgets and neural batch construction
  neural.py          Neural models: Transformer and RNN/LSTM/GRU encoders, fusion
  trainer.py         Training, validation and checkpoints
eval/
  metrics.py         Classification metrics
  predictions.py     Per-utterance prediction export
  latency.py         Latency measurement
  aggregate.py       Aggregate experiment results
  model_details.py   Parameter counts and hyper-parameter tables
  hparams.py         Hyper-parameter effects (learning rate x epoch, grids, sweep)
configs/
  generate_configs.py
  meld/              MELD configurations
  emorynlp/          EmoryNLP configurations
  dailydialog/       DailyDialog configurations
cluster/             Slurm scripts for NTU EEE Cluster 02
notebooks/           Data-cleaning notebook
docs/                Technical notes and handover instructions
outputs/              Audits, run outputs and aggregate results
app/                  Streamlit demo
tests/                Unit and integration tests
```

---

## References

- Poria et al. (2019). *MELD: A Multimodal Multi-Party Dataset for Emotion Recognition in Conversations*. ACL.
- Zahiri & Choi (2018). *Emotion Detection on TV Show Transcripts with Sequence-based CNNs*. AAAI Workshops.
- Lee & Lee (2022). *CoMPM: Context Modeling with Speaker's Pre-trained Memory Tracking for Emotion Recognition in Conversation*. NAACL.
- Sanh et al. (2019). *DistilBERT, a distilled version of BERT*. NeurIPS EMC² Workshop.
- Li et al. (2017). *DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset*. IJCNLP.
