# When Does Context Help? Lightweight Speaker-Aware Context Fusion for Conversational Emotion Recognition

EE6405 Natural Language Processing, group project.

Each utterance in a dialogue gets one emotion label from its text, its speaker and the preceding turns.
We build a small **adaptive fusion module** that, for every utterance, decides how much to rely on the
utterance itself, on the **same speaker's** earlier turns and on **other speakers'** turns. We then test
it in controlled comparisons against a TF-IDF baseline, single-utterance DistilBERT, context
concatenation and fixed-weight fusion, on **MELD** and **EmoryNLP**.

> **Status.** Data pipeline, audit, TF-IDF baseline and all neural models are complete and tested:
> 47 unit tests pass, and all 44 experiment configurations ran end to end on CPU. **GPU training on NTU EEE
> Cluster 02 is the next step.** See [docs/HANDOVER.md](docs/HANDOVER.md).

| document | for |
|---|---|
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | how everything works: data, models, protocol, decisions, limitations |
| [docs/HANDOVER.md](docs/HANDOVER.md) | step-by-step guide to running the GPU experiments |
| [notebooks/data_cleaning.ipynb](notebooks/data_cleaning.ipynb) | every cleaning step and data check, with outputs |
| [outputs/data_audit.md](outputs/data_audit.md) | data audit: split sizes, labels, duplicates, leakage |

---

## Why this project is useful

**The problem is real.** Many replies are ambiguous on their own. Our single-utterance baseline reads
"Fine." as anger with probability 0.54 against neutral 0.40, and in MELD's training data "Hey!" is
labelled joy, neutral, surprise and anger in different scenes. Dialogue history resolves such cases, but
more history costs compute and can bring in turns that are irrelevant. Anyone building a conversational
system has to decide how much context a model should see and whose turns matter. Examples are chatbots,
dialogue analytics and the quality assurance of customer-service conversations.

**It answers that decision with evidence, not intuition.** Published models often change the encoder, the
input and the tuning budget at the same time, so it is unclear what caused an improvement. Here every
neural model uses the same encoder, sees exactly the same text and gets the same tuning budget and
selection rule, with three seeds. This isolates three questions:

1. Does more history help, or does it interfere? (1, 3 or 5 previous turns)
2. Does separating the speaker's own history from other speakers' history help? (speaker-merge ablation)
3. Does learning per-utterance weights beat simple concatenation or equal-weight fusion?

**It is interpretable.** The adaptive model outputs, for every utterance, the weight it gave to the
utterance itself, to the same speaker and to the others (`fusion_weights_test.csv`). Developers and
dialogue analysts can see *when* context changed a prediction, not only *whether* accuracy changed.

**It is cheap.** The fusion module adds 0.6M parameters (0.9%) to a 66M-parameter DistilBERT, and
end-to-end latency (tokenisation included) is measured for every model. The results can therefore say
whether any gain is worth its cost.

**It checks itself across benchmarks.** The key comparisons are repeated on a second dataset with a
different label set. The data audit also documents flaws in both datasets that affect how results
should be read.

Speaker-aware modelling is an established direction (for example CoMPM, Lee & Lee 2022). Our
contribution is a simplified, documented shared-encoder design, a controlled study and its analysis.
Performance improvements will be claimed only where the results support them.

## What we built and what we improved

**The method.** A shared DistilBERT encodes the current utterance and each history utterance. History
vectors are mean-pooled per speaker group. A small gate with a masked softmax produces weights that sum
to 1 over the sources that exist:

```
z = w_current · h_current + w_same · h_same + w_other · h_other
```

A missing group gets weight 0, so the first turn of a dialogue uses the utterance alone. The gate starts
at equal weights, which makes the adaptive model a strict extension of the fixed-fusion control.

**Improvements over a naive setup:**

- **Fair by construction.** One encoder, one per-utterance token budget (80 word pieces) for every model,
  identical optimiser and schedule, and the same rule for choosing the learning rate and epoch (dev
  Macro-F1 only). Differences between models therefore come from how they use context.
- **No duplicate training for the equal-weights ablation.** Removing the learned gate gives exactly the
  fixed-fusion model, so that comparison needs no extra run. Every adaptive model is also re-evaluated
  with equal weights at inference, to test whether it relies on what it learned.
- **A data audit that found real dataset flaws.** It matches rare word sequences, so it still works when
  a scene is re-segmented or its metadata is wrong. It found that:
  - two MELD test dialogues replay a training scene, under wrong episode metadata and with different gold
    labels;
  - a clip-show episode in EmoryNLP dev replays four training scenes;
  - one EmoryNLP dev scene is an exact duplicate.

  The official splits are kept, and these dialogues are listed in `outputs/flagged_dialogues.csv` for a
  sensitivity check.
- **No label leakage.** Gold emotions of history turns can never reach a model input; a unit test checks
  this.
- **Reproducible and hand-over ready.**
  - Inputs are pinned: datasets to fixed commits with SHA-256 checks, DistilBERT to a fixed revision, and
    every package version.
  - Training needs no network.
  - One command runs everything in priority order, resumes after interruptions and refuses to mix
    settings.
  - 47 tests run in seconds without downloads.

## Results so far

Only the TF-IDF + logistic regression baseline has been run. Neural results will appear in
`outputs/results_summary.md` after GPU training.

| dataset | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | latency (CPU, batch 1) |
|---|---:|---:|---:|---:|
| MELD | 0.411 | **0.360** | 0.545 | 0.67 ms |
| EmoryNLP | 0.294 | **0.286** | 0.322 | 0.41 ms |

Its weakest classes are the rare ones: fear 0.07 and disgust 0.15 F1 on MELD, powerful 0.13 and
peaceful 0.19 on EmoryNLP.

## Quick start

**On NTU EEE Cluster 02** (A40 GPUs, Slurm), use the ready-made job scripts from the repository folder in an
SSD project directory. Never run installs or training on the login node.
[docs/HANDOVER.md](docs/HANDOVER.md) has every step and the cluster rules:

```bash
sbatch cluster/setup.sbatch       # CPU: conda env, packages, data + DistilBERT, tests
sbatch cluster/smoke.sbatch       # CPU: every config on 50 utterances
sbatch cluster/gpu_check.sbatch   # A40: short mixed-precision check
sbatch cluster/train.sbatch       # A40: all experiments (resubmit to resume)
```

**Anywhere else** (Python 3.9–3.12):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python prepare_data.py            # data + DistilBERT (needs internet once), audit, flagged list
python -m pytest                  # 47 tests, ~10 s
bash run_all.sh --smoke           # every config on 50 utterances, CPU, ~20 min
bash run_all.sh                   # all experiments (GPU), then outputs/results_summary.md
```

One run: `python train.py --config configs/meld/adaptive_k3_s42.yaml`. All hyper-parameters are in the
YAML configs, which are generated by `configs/generate_configs.py`.

## Experiments

| configs | question | seeds |
|---|---|---|
| `{meld,emorynlp}/tfidf_lr.yaml` | traditional baseline (deterministic) | – |
| `meld/{single,concat_k3,fixed_k3,adaptive_k3}_s*.yaml` | main comparison on MELD | 42, 43, 44 |
| `emorynlp/{concat,fixed,adaptive}_k3_s*.yaml` | replication on EmoryNLP | 42, 43, 44 |
| `meld/adaptive_merged_k3_s*.yaml` | does speaker separation help? | 42, 43, 44 |
| `meld/fixed_k3` vs `meld/adaptive_k3` | do learned weights help? | 42, 43, 44 |
| `meld/{concat,fixed,adaptive}_k{1,3,5}_s*.yaml` | when does more history help or interfere? | 42, 43, 44 |

44 configurations, 84 training runs (each neural config tries learning rates 2e-5 and 5e-5, up to 5 epochs,
and keeps the best dev Macro-F1).

## Data

| dataset | splits (train / dev / test utterances) | labels | licence |
|---|---|---|---|
| MELD | 9,989 / 1,109 / 2,610 | anger, disgust, fear, joy, neutral, sadness, surprise | GPL-3.0 |
| EmoryNLP (original text release) | 9,934 / 1,344 / 1,328 | joyful, mad, neutral, peaceful, powerful, sad, scared | Apache-2.0 |

Records: `dataset, split, dialogue_id, utterance_id, turn_index, speaker_ids, text, label`
(`data/processed/<dataset>/<split>.jsonl`). Text keeps the original punctuation, casing and negation.
Raw data, processed data and the encoder weights are downloaded by `prepare_data.py` and are not
committed.

## Where results go

| path | content |
|---|---|
| `outputs/results_summary.md` | mean ± std over seeds: main comparison, per-class F1, context length, ablations |
| `outputs/runs/<run_name>/metrics_{dev,test}.json` | Macro-F1, Weighted-F1, accuracy, per-class F1, confusion matrix |
| `outputs/runs/<run_name>/predictions_{dev,test}.csv` | per utterance: ids, text, gold label, prediction, class probabilities |
| `outputs/runs/<run_name>/fusion_weights_{dev,test}.csv` | fusion models: per-utterance source availability and weights |
| `outputs/runs/<run_name>/` (other files) | config, log, per-epoch dev metrics, selected checkpoint, latency |
| `outputs/flagged_dialogues.csv` | dialogues to drop in a sensitivity analysis |

## Repository layout

```
prepare_data.py      download + clean data, fetch DistilBERT, write the audit and flagged list
train.py             one entry point: python train.py --config <yaml> [--smoke] [--override k=v ...]
run_all.sh           every experiment in priority order, then the summary
data/                loaders.py (records), context.py (history windows), audit.py (checks)
models/              tfidf_lr.py, batching.py (token budget), neural.py (models), trainer.py
eval/                metrics.py, predictions.py, latency.py, aggregate.py
configs/             generate_configs.py and the 44 generated YAML files
cluster/             Slurm job scripts for NTU EEE Cluster 02 (setup, smoke, gpu_check, train, aggregate)
notebooks/           data_cleaning.ipynb
docs/                TECHNICAL.md, HANDOVER.md
outputs/             data_audit.md, flagged_dialogues.csv, runs/<run_name>/, results_summary.*
app/                 Streamlit demo (next stage)
tests/               pytest suite
```

## References

- Poria et al. (2019). MELD: A Multimodal Multi-Party Dataset for Emotion Recognition in Conversations. ACL.
- Zahiri & Choi (2018). Emotion Detection on TV Show Transcripts with Sequence-based CNNs. AAAI Workshops.
- Lee & Lee (2022). CoMPM: Context Modeling with Speaker's Pre-trained Memory Tracking for Emotion
  Recognition in Conversation. NAACL.
- Sanh et al. (2019). DistilBERT, a distilled version of BERT. NeurIPS EMC² Workshop.
