# Technical Report: Speaker-Aware Context Weighting for Conversational Emotion Recognition

EE6405 Natural Language Processing, group project. This report describes the data pipeline, the models,
the training and evaluation protocol, and the results of all 237 configurations (Section 8). Section 9 lists
the decisions that refine the original proposal.

## Contents

1. [Problem and research questions](#1-problem-and-research-questions)
2. [Data](#2-data)
3. [Context construction and the shared token budget](#3-context-construction-and-the-shared-token-budget)
4. [Models](#4-models)
5. [Training and model selection](#5-training-and-model-selection)
6. [Evaluation](#6-evaluation)
7. [Experiment matrix and compute](#7-experiment-matrix-and-compute)
8. [Results](#8-results)
9. [Decisions that refine the proposal](#9-decisions-that-refine-the-proposal)
10. [Engineering: reproducibility and testing](#10-engineering-reproducibility-and-testing)
11. [Limitations and risks](#11-limitations-and-risks)
12. [Next steps](#12-next-steps)
13. [References](#13-references)

---

## 1. Problem and research questions

Each utterance in a dialogue gets one emotion label. The inputs are its text, the speaker identities
(used only as "same speaker as the target or not") and a bounded window of preceding utterances from
the same dialogue. Short replies such as "Fine." or "What?" are ambiguous on their own, while long
context windows can bring in exchanges that are irrelevant to the target. The project asks:

1. How does using the previous 1, 3 or 5 turns affect performance?
2. Does separating the current speaker's own history from other speakers' history help?
3. Does learning per-utterance weights for these sources add value over concatenating the context or
   fusing it with fixed weights?

The working hypothesis is that adaptive weighting helps most on short utterances and where the context
sources differ in relevance. The experiments are designed to test this, and a gain is reported only if the
results show one.

## 2. Data

### 2.1 Datasets

Exactly two datasets are used, each with its official train/dev/test split.

| dataset | labels | train | dev | test | source (pinned) | licence |
|---|---|---:|---:|---:|---|---|
| MELD | anger, disgust, fear, joy, neutral, sadness, surprise | 9,989 | 1,109 | 2,610 | `declare-lab/MELD` @ `ca3e126`, `data/MELD/*_sent_emo.csv` | GPL-3.0 |
| EmoryNLP (original text release) | joyful, mad, neutral, peaceful, powerful, sad, scared | 9,934 | 1,344 | 1,328 | `emorynlp/emotion-detection` @ `28df4a2`, `json/emotion-detection-*.json` | Apache-2.0 |

All six split sizes match the counts published in the proposal. Both corpora are transcripts of the TV
series *Friends* but use different label sets (MELD: Ekman's six basic emotions plus neutral; EmoryNLP:
six emotions of Willcox's feeling wheel plus neutral). Models are trained on one dataset at a time, from
the same pretrained initialisation, with separate label maps and no cross-dataset training.

Both datasets are heavily imbalanced. For example, MELD train is 47.2% neutral while disgust and fear
are 2.7% each. Macro-F1 is therefore the primary metric.

### 2.2 Unified record format

`prepare_data.py` downloads the six files (verified by SHA-256), converts them, and writes
`data/processed/<dataset>/<split>.jsonl`. Each record has the same fields:

| field | MELD | EmoryNLP |
|---|---|---|
| `dataset`, `split` | `meld`, official split | `emorynlp`, official split |
| `dialogue_id` | `dia<Dialogue_ID>` | scene id, e.g. `s01_e15_c01` |
| `utterance_id` | `dia<D>_utt<U>` (original ids, gaps kept) | original id |
| `turn_index` | 0-based position in the dialogue | same |
| `speaker_ids` | list; "Joey and Chandler" → `["Joey", "Chandler"]` | list as released, duplicates removed |
| `text` | transcript, only outer whitespace stripped | same |
| `label` | lower-cased gold emotion | lower-cased (released capitalised) |

`turn_index` is an addition to the field list of the proposal. MELD skips utterance ids in 76 dialogues
(utterances removed by its authors), so an explicit position is needed for "the previous k turns" to be
well defined.

### 2.3 Cleaning decisions

The cleaning is deliberately minimal. Every step is counted against the raw files in
`notebooks/data_cleaning.ipynb`.

- Official splits are kept; no utterance is removed, merged or relabelled.
- Text keeps the original punctuation, casing and negation. The raw files contain no leading or
  trailing whitespace and no encoding damage (no mojibake); curly quotes and dashes are kept.
- MELD is read with `keep_default_na=False`, so an utterance such as "None" or "NA" would stay text
  instead of becoming a missing value.
- Chronological order: MELD rows are ordered by `(Dialogue_ID, Utterance_ID)`; EmoryNLP keeps the JSON
  order within a scene. Both files are already in this order, so no row moves.
- Joint MELD speakers (7 train, 4 dev, 3 test) are split into a speaker list so that the same-speaker
  relation can use overlap. Group names such as "All" and "Both" stay literal ids.
- The label map is fixed and alphabetical per dataset, never derived from the data.

### 2.4 Audit findings

The full report is in `outputs/data_audit.md`. The checks cover split sizes, label distribution,
utterance length, duplicates, cross-split overlap and context availability.

**Re-used scenes across splits.** Exact text matching misses scenes that a dataset cuts into different
utterances or annotates with wrong metadata. The audit therefore matches *rare word 6-grams*: sequences
of six words that occur in at most three dialogues of the dataset, ignoring spelled-out words such as
"C.H.E.E.S.E.". A dev/test dialogue counts as a re-used scene when at least two distinct texts match one
earlier-split dialogue, or when more than half of its utterances with five or more words match. The
result is stable for rarity thresholds of 3, 4 and 5 dialogues.

| dataset | split | flagged dialogues | utterances | finding |
|---|---|---|---:|---|
| MELD | test | `dia84`, `dia85` | 9 (0.34%) | Same scene as train `dia12` (season 6, episode 4), cut differently and partly re-segmented. `dia84` is labelled season 1, episode 5 in the metadata. Gold labels differ on 4 of the 6 matched utterances. |
| EmoryNLP | dev | `s04_e21_c06` – `c09` | 34 (2.5%) | A clip-show episode replaying training scenes (s01e05, s01e07, s02e07, s03e15/e16). Gold labels differ on 20 of 32 matched utterances. |
| EmoryNLP | dev | `s04_e01_c14` | 5 | Exact duplicate of `s04_e01_c13`. |

EmoryNLP test has no re-used scene. The flagged dialogues stay in the official splits and are listed in
`outputs/flagged_dialogues.csv`, so a sensitivity analysis can recompute dev/test metrics without them.

**Label ambiguity.** The same text carries different gold labels in many places: 105 distinct texts in
MELD train (877 rows) and 164 in EmoryNLP train (1,125 rows). For example, "Hey!" is joy 45 times,
neutral 19 and surprise 11 times in MELD train. These are kept: they reflect genuine dependence on
context, which is the phenomenon under study.

**Cross-dataset overlap.** 17–25% of long test utterances also appear in the other corpus (both come from
*Friends*). This is not leakage here, because no model is trained on one corpus and tested on the other.

### 2.5 Context availability

Train split; the window is the previous k utterances of the same dialogue.

| dataset | k | no history (first turn) | has same-speaker history | has other-speaker history |
|---|---:|---:|---:|---:|
| MELD | 1 | 10.4% | 20.1% | 69.5% |
| MELD | 3 | 10.4% | 64.5% | 80.1% |
| MELD | 5 | 10.4% | 69.0% | 83.9% |
| EmoryNLP | 1 | 7.2% | 2.0% | 90.8% |
| EmoryNLP | 3 | 7.2% | 65.2% | 92.5% |
| EmoryNLP | 5 | 7.2% | 70.5% | 92.5% |

At k=1 EmoryNLP almost never has same-speaker history, because speakers alternate. The speaker-separated
models therefore effectively reduce to two sources there.

## 3. Context construction and the shared token budget

`data/context.py` builds, for each target utterance at position t, the window t−k … t−1 of the same
dialogue (oldest first). Each history turn is marked *same-speaker* if its speaker set overlaps the
target's speaker set, otherwise *other-speaker*. The first turn of a dialogue has an empty history.
Only text, speaker ids and utterance ids are copied into a context object; gold labels of history turns
cannot reach the model, and a unit test checks this.

**Shared token budget.** Every utterance, whether current or history, keeps its first 80 DistilBERT word
pieces, in every model. Consequently all neural models see exactly the same retained text and differ only
in how they combine it. The limit truncates 1 of 13,708 MELD utterances and 98 of 12,606 EmoryNLP
utterances (0.78%). At k=5 the concatenated input is at most (5+1)·80+7 = 487 tokens, within DistilBERT's
512 positions.

| model | input sequence(s) |
|---|---|
| single | `[CLS] u_t [SEP]` |
| concat | `[CLS] u_t [SEP] u_{t-k} [SEP] … u_{t-1} [SEP]` |
| weighting | each utterance separately as `[CLS] u [SEP]` |

## 4. Models

All neural models load the same pretrained `distilbert-base-uncased` (66.4M parameters, pinned
revision `12040ac`). Each takes the `[CLS]` vector of a sequence (h ∈ ℝ⁷⁶⁸) and ends with the same
dropout(0.1) + linear classifier.

**Single-utterance DistilBERT** classifies `[CLS]` of the current utterance.

**Context concatenation** classifies `[CLS]` of the concatenated sequence above. It sees the history
but does not separate speakers.

**Fixed-weight weighting** encodes the current utterance and every history utterance with the shared
encoder. It mean-pools the history vectors within each speaker group:

- h_current = encoder(u_t)
- h_same = mean of encoder(u) over same-speaker history turns
- h_other = mean of encoder(u) over other-speaker history turns

and combines them as z = Σ_s w_s · h_s. Here w_s is equal (1/n) across the n available sources, and a
missing group gets weight 0.

**Adaptive weighting (proposed)** replaces the equal weights with a learned gate:

```
g     = [h_current ; h_same ; h_other ; m]            m = availability mask (3 flags)
w     = masked_softmax( W2 · tanh(W1 · g) , m )        w_s = 0 where m_s = 0,  Σ w_s = 1
z     = w_current·h_current + w_same·h_same + w_other·h_other
ŷ     = softmax( W_c · dropout(z) )
```

The gate has 592k parameters (W1: 2307→256, W2: 256→3), which is 0.9% of the model. The first turn of a
dialogue only has the current source, so w_current = 1. W2 starts at zero, so training begins exactly at
the fixed weights and the gate learns to move away from them only if that helps. The encoder,
gate and classifier are fine-tuned together.

**Ablations**

- *Speaker merge* (`adaptive_merged`): same- and other-speaker history pooled into one source; the gate
  weighs two sources (current, history).
- *Equal weights instead of learned weights*: removing the gate while keeping everything else fixed gives
  exactly the fixed-weighting model, so that comparison needs no extra training run. In addition, every
  trained adaptive model is evaluated a second time with its gate replaced by equal weights
  (`metrics_*_equal_weights.json`). This shows whether the trained model actually relies on the weights
  it learned.

**Encoder comparison.** On MELD (k = 3, three seeds), the same architectures run with other utterance
encoders (`model.backbone` in the config; `models/neural.py`):

- *Transformers*: `bert-base-uncased` (pinned `86b5e09`) and `roberta-base` (pinned `e2da8e2`) in all four
  architectures, with the training settings of Section 5.
- *Recurrent*: RNN, LSTM and GRU, each one- and bidirectional, as single-utterance and concatenation
  models; BiLSTM also with fixed and adaptive weighting. They read DistilBERT's word pieces through its frozen
  768-d input embedding table (static vectors, like GloVe), so they keep the token budget of every other
  model. One recurrent layer of 256 units per direction, max-pooling over time, dropout 0.3, learning rates
  1e-3 and 3e-3, 10 epochs, fp32.

Because every encoder sees the same word pieces of the same turns, differences come from the encoder.

**Traditional baselines.** Four term-weighting schemes (binary presence, raw term frequency, sublinear
TF-IDF, Okapi BM25 with k1 = 1.2 and b = 0.75) are crossed with five classifiers (logistic regression,
linear SVM, multinomial and complement naive Bayes, random forest with 300 trees) in `models/classical.py`.
They use the tokens of TF-IDF + LR, classify the current utterance only and select their own grid on dev
Macro-F1. They run once per pair and dataset on CPU. The random forest grid uses minimum leaf sizes 2 and 5:
a first grid with 1 and 2 always selected 2 on dev, and leaf size 1 took about 90% of the fit time (over an
hour per run on DailyDialog).

**Relation to CoMPM (Lee & Lee, 2022).** CoMPM is the methodological reference for the value of speaker
history. Our design is a simplified, shared-encoder adaptation. Its differences from the published method:

| aspect | CoMPM | this project |
|---|---|---|
| encoders | context model and speaker memory use separate pre-trained LMs (RoBERTa) | one shared DistilBERT for every utterance |
| context | the dialogue context with speaker tokens in one sequence | bounded window (k = 1, 3, 5); no speaker tokens |
| speaker history | the current speaker's previous utterances, tracked with a GRU | same- and other-speaker groups, mean-pooled |
| combination | memory output added to the context representation | per-utterance masked-softmax weights over the sources |
| cost | two large encoders | one 66M-parameter encoder plus a 0.6M-parameter gate |

The goal is not to reproduce CoMPM's scores. It is to isolate, under matched conditions, whether
speaker separation and adaptive weighting help.

## 5. Training and model selection

| setting | value |
|---|---|
| optimiser | AdamW, weight decay 0.01 (not on biases/LayerNorm) |
| learning rates | 2e-5 and 5e-5, each tried once per run from the same seed |
| schedule | linear warm-up over 10% of steps, then linear decay |
| epochs | up to 5 (no early stopping) |
| batch size | 16 target utterances (train), 64 (eval) |
| loss | cross-entropy, no class weights |
| regularisation | dropout 0.1, gradient clipping at norm 1.0 |
| precision | mixed precision on CUDA (bf16 if supported, otherwise fp16 with loss scaling) |
| seeds | 42, 43, 44 for every neural configuration |

**Selection.** After every epoch the model is scored on dev. The (learning rate, epoch) pair with the
highest dev Macro-F1 is kept, and only that checkpoint is evaluated on test, once. Test data never
influences any choice.

**TF-IDF + logistic regression.** The vectoriser and classifier are fitted on train only. Features are
word 1–2-grams that keep in-word apostrophes ("don't") and the tokens "!" and "?", without stop-word
removal so that negations survive. A 40-point grid (n-gram range, min_df, C, class weight) is scored on
dev Macro-F1. Logistic regression with lbfgs is deterministic, so this baseline runs once per dataset.

## 6. Evaluation

All models report through the same code in `eval/`:

- **Macro-F1** (primary), **Weighted-F1**, accuracy, per-class precision/recall/F1 and the confusion
  matrix (`eval/metrics.py`).
- **End-to-end inference latency** (`eval/latency.py`): from raw text to predicted label, including
  tokenisation, the forward pass and moving results back to the CPU. Measured on 300 test utterances,
  batch size 1, after 10 warm-up batches, on the training device.
- **Fixed output formats** (`eval/predictions.py`): one prediction row per utterance with gold label,
  predicted label and class probabilities; for weighting models, one row per utterance with source
  availability and the three weights.
- **Aggregation** (`eval/aggregate.py`): mean ± sample standard deviation over seeds, per dataset, model
  and context length, written to `outputs/results_summary.md`. The encoder comparison and the
  term-weighting × classifier matrix get their own tables there.
- **Model size and settings**: every run writes `params.json` (total and trainable parameters; learned
  values for traditional models). `python -m eval.model_details` writes `outputs/model_details.md` with
  parameter counts for every configured model, the hyper-parameter tables and the learning rate and epoch
  each run selected.
- **Hyper-parameter effects** (`python -m eval.hparams`, see `docs/HYPERPARAMETERS.md`): dev Macro-F1 per
  learning rate and epoch for every neural run, per grid point for traditional models, and the test
  scores of the one-setting-at-a-time sweep.
- **Sensitivity**: `outputs/flagged_dialogues.csv` lists the dialogues to drop from dev/test for a check
  that the conclusions do not depend on re-used scenes.

- **Significance**: paired bootstrap on the saved test predictions, resampling test utterances and
  pairing seeds (results in Section 8).

## 7. Experiment matrix and compute

237 configurations are generated from one file (`configs/generate_configs.py`):

| group | configurations | runs |
|---|---|---:|
| TF-IDF baseline | MELD, EmoryNLP, DailyDialog | 3 |
| MELD main comparison (k=3) | single, concat, fixed, adaptive × 3 seeds | 12 |
| EmoryNLP replication (k=3) | concat, fixed, adaptive × 3 seeds | 9 |
| MELD speaker-merge ablation (k=3) | adaptive_merged × 3 seeds | 3 |
| MELD context length (k=1, 5; k=3 reused) | concat, fixed, adaptive × 2 × 3 seeds | 18 |
| DailyDialog supplementary (k=3) | single, concat, fixed_merged, adaptive_merged × 3 seeds | 12 |
| EmoryNLP single-utterance baseline | single × 3 seeds | 3 |
| MELD Transformer encoders (k=3) | BERT, RoBERTa × single, concat, fixed, adaptive × 3 seeds | 24 |
| MELD recurrent encoders (k=3) | 6 RNN/LSTM/GRU variants × single, concat × 3 seeds; BiLSTM fixed, adaptive × 3 seeds | 42 |
| Traditional baselines (CPU) | 4 weightings × 5 classifiers − TF-IDF + LR, × 3 datasets | 57 |
| MELD hyper-parameter sweep (k=3) | single, adaptive × (5 learning rates, 2 batch sizes, 2 dropouts) × 3 seeds | 54 |

The first six groups (57 configurations) are the original study; all 237 configurations have finished.
Each neural configuration trains once per learning rate (two; one in the sweep), for up to 5 epochs (10 for
recurrent encoders). `run_all.sh` runs the groups in this priority order, so the main comparison finishes
first. All GPU runs used one NVIDIA A40 of NTU EEE Cluster 02 (`cluster/train.sbatch`), so latencies are
comparable: 7.75 h for the original study and 7.66 h for the second batch (Transformer encoders 2.96 h,
recurrent encoders 2.30 h, sweep 2.19 h, EmoryNLP single 0.22 h; per run in `outputs/run_all_status.log`). Disk use is about 0.25 GB per finished run (one checkpoint), about 11 GB in total.

## 8. Results

The original study (57 configurations) has finished on one A40. Test Macro-F1 at k = 3, mean ± std over
three seeds (full tables, per-class F1 and latency in `outputs/results_summary.md`):

| model | MELD | EmoryNLP | DailyDialog |
|---|---:|---:|---:|
| TF-IDF + LR | 0.360 | 0.286 | 0.437 |
| single-utterance DistilBERT | 0.437 ± 0.007 | 0.270 ± 0.006 | 0.478 ± 0.028 |
| concatenation | 0.428 ± 0.012 | 0.292 ± 0.011 | 0.488 ± 0.022 |
| fixed weighting | 0.361 ± 0.008 | 0.248 ± 0.004 | 0.480 ± 0.012 (merged) |
| adaptive weighting | 0.438 ± 0.006 | 0.282 ± 0.007 | 0.489 ± 0.006 (merged) |

The learned gate matters (fixed weighting is far below adaptive, and swapping equal weights into the trained
adaptive model drops MELD to 0.349), but context adds little over the single-utterance model on MELD and
DailyDialog, and speaker separation shows no clear gain (MELD 0.438 vs 0.435 merged). EmoryNLP is the
exception: concatenation beats the single-utterance model there, and the gate gives history 23% of the weight
when all three sources exist (16% on MELD).

Significance comes from a paired bootstrap on the saved test predictions: 10,000 resamples of test
utterances, each scoring both models on the same utterances for all three seeds and averaging the seed-wise
differences.

| comparison | MELD | EmoryNLP | DailyDialog |
|---|---|---|---|
| adaptive − single | +0.002 (p = 0.82) | +0.012 (p = 0.06) | +0.012 (p = 0.29) |
| adaptive − concat | +0.010 (p = 0.23) | −0.010 (p = 0.23) | +0.002 (p = 0.89) |
| adaptive − fixed | **+0.077** (+0.056 to +0.098) | **+0.035** (+0.017 to +0.053) | +0.009 (p = 0.51) |
| concat − single | −0.009 (p = 0.22) | **+0.022** (p = 0.009) | |
| adaptive − adaptive merged | +0.003 (p = 0.56) | | |

On MELD the gate is stable across seeds (current-utterance weight 0.84, 0.85, 0.84) and does not depend on
utterance length (correlation −0.01 to +0.01). Short replies (three words or fewer, 27% of the test set)
score 0.506 for single, concatenation and adaptive weighting alike; the seed-42 lead of concatenation on them
(+0.040) does not repeat on seeds 43 and 44.

The encoder comparison (MELD, k = 3) keeps the same ranking for BERT-base and RoBERTa-base: adaptive weighting
and concatenation are level (difference −0.002, p ≥ 0.76), both about 0.011–0.014 above the single-utterance
model (p = 0.07–0.16), and fixed weighting is 0.07 below (p < 0.001). RoBERTa-base concatenation is the best
model overall (0.470 ± 0.005); RoBERTa single beats DistilBERT single by 0.020 (p = 0.02) at about twice
the latency (8.6 vs 4.0 ms). Recurrent encoders reach at most 0.417 (GRU, concatenation) at about 1 ms per
utterance; the BiLSTM gate puts all of its weight on the current utterance. The sweep around the reference
setting changes no model by more than +0.011, and the adaptive − single difference ranges from −0.012 to
+0.017 across settings (README, "Hyper-parameter sweep").

The traditional baselines (Section 4) have finished. The pair selected on dev over all 19 reaches 0.382 on
MELD (TF-IDF + linear SVM), 0.279 on EmoryNLP (TF + LR) and 0.485 on DailyDialog (TF + linear SVM).
DistilBERT's lead over it is therefore 0.056, 0.013 and 0.004: on DailyDialog a linear model on term counts
is level with the pretrained encoder. The best linear model beats naive Bayes and random forest on every
dataset, though by only 0.001 over random forest on EmoryNLP.

The TF-IDF + LR details below are final for that model.

| dataset | dev Macro-F1 | test Macro-F1 | test Weighted-F1 | test accuracy | latency (CPU, batch 1) | selected settings |
|---|---:|---:|---:|---:|---:|---|
| MELD | 0.4108 | **0.3600** | 0.5454 | 0.5471 | 0.67 ms | 1–2-grams, min_df 1, C=10, balanced |
| EmoryNLP | 0.2942 | **0.2856** | 0.3224 | 0.3125 | 0.41 ms | unigrams, min_df 1, C=0.3, balanced |

Per-class test F1:

| MELD | anger | disgust | fear | joy | neutral | sadness | surprise |
|---|---:|---:|---:|---:|---:|---:|---:|
| TF-IDF + LR | 0.337 | 0.151 | 0.073 | 0.487 | 0.721 | 0.259 | 0.492 |

| EmoryNLP | joyful | mad | neutral | peaceful | powerful | sad | scared |
|---|---:|---:|---:|---:|---:|---:|---:|
| TF-IDF + LR | 0.435 | 0.283 | 0.421 | 0.194 | 0.132 | 0.246 | 0.288 |

The minority classes (MELD fear and disgust; EmoryNLP powerful and peaceful) are where a single-utterance
lexical model is weakest. The baseline is also uncertain on short replies: for "Fine." it predicts
anger 0.54 against neutral 0.40. These are the cases the context models are meant to address.

All neural pipelines have been verified end to end on CPU (50 utterances per split, 1 epoch, all 44
configurations); those smoke-test scores carry no information about model quality.

## 9. Decisions that refine the proposal

| topic | decision | reason |
|---|---|---|
| main context window | k = 3 for the main comparison and ablations; k = 1 and 5 in the context study | fixed before seeing results; k=3 is where same-speaker history becomes common (Section 2.5) |
| learning rates | each run tries 2e-5 and 5e-5 once and selects (lr, epoch) on dev Macro-F1 | one rule for every model; selection never uses test |
| token budget | 80 word pieces per utterance for all models | identical retained text for all models; fits k=5 into 512 positions |
| equal-weights ablation | identical to fixed weighting, plus an inference-time equal-weights evaluation of each adaptive run | avoids training a duplicate model |
| TF-IDF seeds | one run per dataset | deterministic solver |
| TF-IDF on EmoryNLP | added | gives the EmoryNLP comparison a non-neural reference |
| `turn_index` field | added to the record format | MELD utterance ids have gaps |
| re-used scenes | kept in official splits; listed for a sensitivity analysis | keeps results comparable with published work |
| gate initialisation | output layer starts at zero (= fixed weighting) | makes adaptive weighting a strict extension of the control |

## 10. Engineering: reproducibility and testing

- **Pinned inputs.** Dataset files are pinned to repository commits and checked by SHA-256; the encoder
  is pinned to a Hugging Face revision and saved locally, so training needs no network; all Python
  dependencies are pinned in `requirements.txt`.
- **One source of truth.** All configurations come from one generator. A run directory stores its config,
  and resuming with a different config is refused, so a run can never mix settings.
- **Fault tolerance.** Finished runs are skipped. An interrupted run resumes after its last finished epoch,
  restoring optimiser, scheduler, loss-scaler and random-number states. A failed run does not stop the
  batch.
- **Determinism.** Seeds fix initialisation and data order (the shuffle seed is derived from seed and
  epoch). GPU kernels are not forced to be deterministic, so repeated GPU runs can differ slightly;
  three seeds capture this variation.
- **Tests.** 114 pytest tests (one more is skipped without local data) run in about 20 seconds without
  downloads. They cover:
  - loaders and context construction: first turn, window sizes, speaker split, multi-speaker overlap,
    dialogue/split boundaries, label leakage;
  - the token budget, weighting masking and weights, and the gate's equal-weight initialisation;
  - every model type end to end on a tiny randomly initialised encoder, crash-and-resume, and refusal of
    changed configs;
  - TF-IDF with missing classes, the scene-overlap detector and aggregation.
  - RNN/LSTM/GRU encoders (padding never changes the output), parameter counts, BM25 and every
    traditional classifier, the hyper-parameter tables, and the Streamlit demo's core logic.

  Separate checks exercised the bf16 mixed-precision path on CPU and resume on a non-CPU device (Apple
  MPS). Those checks found and fixed a resume bug: random-number states had been loaded onto the GPU.
- **Smoke test.** `bash run_all.sh --smoke` ran all 44 configurations that existed before DailyDialog was
  added on CPU without errors in 16 minutes.
- **Cluster job scripts.** `cluster/*.sbatch` follow the NTU EEE Cluster 02 rules: environment and caches
  in the SSD project directory, a named GPU model, no CPU/memory flags on GPU jobs, CPU-only jobs for setup
  and smoke tests. They ran both GPU batches on the cluster: 7.75 h for the original study and 7.66 h for
  the model comparison, on one A40, with no failed run.

## 11. Limitations and risks

- **Domain.** Both corpora come from one TV series, so conclusions concern scripted sitcom dialogue.
  Transfer to customer-service conversations remains an open question.
- **Learning rate of the gate.** The gate trains with the same small learning rate as the encoder and
  starts from equal weights. It does move away from them (MELD: 0.84 on the current utterance when all three
  sources exist, on every seed), but it then varies little between utterances (10–90% range 0.79–0.88).
- **Label noise and ambiguity.** Many identical texts have different gold labels, and re-used scenes are
  labelled inconsistently (Section 2.4). This caps attainable scores and adds variance to minority classes.
- **Hardware.** Training ran on NTU EEE Cluster 02 with NVIDIA A40 GPUs (bf16). The fp16
  fallback for GPUs without bf16 is untested, but no allowed GPU on that cluster needs it. Its Blackwell
  GPUs (`pro6000`, `rtx5090`) are excluded: the pinned torch 2.5.1 has no kernels for them.
- **Seeds.** Three seeds give a rough spread, not a tight confidence interval. Differences smaller than
  the seed standard deviation should not be claimed.
- **Stakeholder evidence.** As noted in the proposal, user needs are design assumptions. The usability
  walkthrough is planned but not yet done.

## 12. Next steps

Done: all 237 runs, the results tables, the paired bootstrap for the key comparisons, the short-utterance
check and the Streamlit demo (`app/`). Still open:

1. Error analysis on minority classes and speaker emotion changes, using `predictions_test.csv` and
   `fusion_weights_test.csv`.
2. Repeat the key numbers without the flagged dialogues (`outputs/flagged_dialogues.csv`).

## 13. References

- Poria, S., Hazarika, D., Majumder, N., Naik, G., Cambria, E., Mihalcea, R. (2019). MELD: A Multimodal
  Multi-Party Dataset for Emotion Recognition in Conversations. ACL.
- Zahiri, S. M., Choi, J. D. (2018). Emotion Detection on TV Show Transcripts with Sequence-based
  Convolutional Neural Networks. AAAI Workshops.
- Lee, J., Lee, W. (2022). CoMPM: Context Modeling with Speaker's Pre-trained Memory Tracking for Emotion
  Recognition in Conversation. NAACL.
- Lu, X., Zhao, Y., Wu, Y., Tian, Y., Chen, H., Qin, B. (2020). An Iterative Emotion Interaction Network for
  Emotion Recognition in Conversations. COLING.
- Sanh, V., Debut, L., Chaumond, J., Wolf, T. (2019). DistilBERT, a distilled version of BERT: smaller,
  faster, cheaper and lighter. NeurIPS EMC² Workshop.
