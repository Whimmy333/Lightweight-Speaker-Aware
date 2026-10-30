
# When Does Context Help? Lightweight Speaker-Aware Context Fusion for Conversational Emotion Recognition

EE6405 Natural Language Processing, group project.

Each utterance in a dialogue receives one emotion label from its text, its speaker and the preceding turns. We build a lightweight adaptive fusion module that decides how much to rely on the current utterance, the same speaker's earlier turns and other speakers' turns.

The main controlled comparisons use **MELD** and **EmoryNLP**. We add **DailyDialog** as a third, supplementary benchmark to examine how context methods behave on a different dialogue corpus.

DailyDialog does not provide explicit speaker IDs in the standard text release. Its experiments therefore use speaker-independent history fusion and do not test whether separating same-speaker history from other-speaker history helps.

> **Status.** All 237 configurations have finished: the original study (57), the EmoryNLP single-utterance baseline, the other encoders, the traditional term-weighting × classifier baselines and the hyper-parameter sweep. Every run folder (without checkpoints) is in `outputs/runs/`; the results are in [outputs/results_summary.md](outputs/results_summary.md) and summarised under [Results so far](#results-so-far). Everything is on `main`; `feature/dailydialog-support` has been merged. **Preparing the video?** See [For the presentation: how to say it](#for-the-presentation-how-to-say-it) and [where to find things](#for-the-presentation-where-to-find-things).

| Document | Purpose |
|---|---|
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | Data, models, protocol, decisions and limitations |
| [docs/HANDOVER2.md](docs/HANDOVER2.md) | Analysis of the first GPU batch (main results, ablations, latency) |
| [docs/HYPERPARAMETERS.md](docs/HYPERPARAMETERS.md) | Hyper-parameter effects: data files and plotting examples |
| [app/README.md](app/README.md) | Streamlit demo |
| [docs/HANDOVER.md](docs/HANDOVER.md), [docs/HANDOVER3.md](docs/HANDOVER3.md) | Running the first and second GPU batches on NTU EEE Cluster 02 |
| [docs/DATA.md](docs/DATA.md) | Data sources, raw columns used, processed format and every cleaning step |
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

### Models compared

Every DistilBERT model uses the same pretrained encoder (66M parameters), the same first 80 word pieces of every utterance and the same classifier. They differ only in how they combine the current utterance with its history.

| Model | What it reads | How it combines the history | What it tests |
|---|---|---|---|
| TF-IDF + LR | current utterance, word 1–2-grams | none | traditional baseline |
| Single | current utterance | none | is context needed at all? |
| Concatenation | current + previous k turns as one sequence | the Transformer mixes everything | the simple way to add context |
| Fixed fusion | each turn encoded separately | equal weights over current, same-speaker and other-speaker vectors | is weighting needed? |
| Adaptive fusion (ours) | each turn encoded separately | a small gate learns per-utterance weights over the three sources | does learned weighting help? |
| Adaptive merged | each turn encoded separately | as adaptive, but all history in one source | does separating speakers help? |

The gate is a two-layer network with 0.59M parameters (0.9% of the model). It starts at equal weights and only moves away if that lowers the training loss. A missing source, such as same-speaker history on the first turns, gets weight 0. DailyDialog has no speaker IDs, so it only runs the merged versions of fixed and adaptive fusion.

Training is the same for every DistilBERT model: learning rates 2e-5 and 5e-5, up to 5 epochs, batch size 16, three seeds. The (learning rate, epoch) with the best dev Macro-F1 is kept and evaluated on test once. The other encoders use the same settings, recurrent ones for up to 10 epochs. Every setting is in [outputs/model_details.md](outputs/model_details.md).

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
| Single-utterance DistilBERT | 0.437 ± 0.007 | 0.270 ± 0.006 | 0.478 ± 0.028 |
| Concatenation | 0.428 ± 0.012 | 0.292 ± 0.011 | 0.488 ± 0.022 |
| Fixed fusion (equal weights) | 0.361 ± 0.008 | 0.248 ± 0.004 | 0.480 ± 0.012 |
| Adaptive fusion (ours) | 0.438 ± 0.006 | 0.282 ± 0.007 | 0.489 ± 0.006 |

DailyDialog has no speaker IDs, so its fusion models pool all history into one source (`fixed_merged`, `adaptive_merged`).

- **The learned gate matters.** Adaptive fusion beats fixed fusion by 0.077 on MELD (95% interval +0.056 to +0.098) and 0.035 on EmoryNLP (+0.017 to +0.053). Replacing the trained gate with equal weights at inference drops MELD from 0.438 to 0.349.
- **Context adds little on MELD and DailyDialog.** Adaptive fusion vs the single-utterance model: +0.002 on MELD (p = 0.82) and +0.012 on DailyDialog (p = 0.29); vs concatenation: +0.010 on MELD (p = 0.23).
- **On EmoryNLP, context helps.** Concatenation beats the single-utterance model by 0.022 (p = 0.009), adaptive fusion by 0.012 (p = 0.06). Its gate also gives history more weight than on MELD (23% vs 16% when all three sources exist). The single-utterance DistilBERT (0.270) is below TF-IDF + LR there.
- **Speaker separation shows no clear gain** on MELD (0.438 separated vs 0.435 pooled, p = 0.56).
- **Context length:** adaptive fusion rises slightly with k on MELD (0.434, 0.438, 0.443 for k = 1, 3, 5); concatenation stays flat.
- **Cost:** on MELD, adaptive fusion takes 4.9 ms per utterance on the cluster GPU vs 4.0 ms for concatenation and single-utterance models.
- **Per class (MELD):** fear (about 0.15 F1) and disgust (0.18–0.28) are the weakest classes for every model; adaptive fusion is best on disgust (0.277 vs 0.239 for single).

Weighted-F1 is much higher than Macro-F1 (MELD about 0.61, DailyDialog about 0.84) because the frequent classes are easy, so report Macro-F1 first. Per-class F1 for every model is in [outputs/results_summary.md](outputs/results_summary.md).

**Is any gap real?** Paired bootstrap on the saved test predictions: each of 10,000 resamples of test utterances scores both models on the same utterances for all three seeds and averages the three differences.

| Comparison (3 seeds) | MELD | EmoryNLP | DailyDialog |
|---|---|---|---|
| adaptive − single | +0.002 (p = 0.82) | +0.012 (p = 0.06) | +0.012 (p = 0.29) |
| adaptive − concatenation | +0.010 (p = 0.23) | −0.010 (p = 0.23) | +0.002 (p = 0.89) |
| adaptive − fixed | **+0.077** (95% interval +0.056 to +0.098, p < 0.001) | **+0.035** (+0.017 to +0.053, p < 0.001) | +0.009 (p = 0.51) |
| concatenation − single | −0.009 (p = 0.22) | **+0.022** (+0.006 to +0.038, p = 0.009) | +0.010 (p = 0.25) |
| adaptive − adaptive merged | +0.003 (p = 0.56) | | |

Only three gaps are significant at 0.05: adaptive over fixed fusion on MELD and EmoryNLP, and concatenation over the single-utterance model on EmoryNLP. On DailyDialog, which has no speaker IDs, no difference is significant.

### Context window

More history is not automatically better: adaptive fusion rises slightly with k, concatenation stays flat. MELD test Macro-F1:

| Model | k = 1 | k = 3 | k = 5 |
|---|---:|---:|---:|
| Adaptive fusion | 0.434 ± 0.016 | 0.438 ± 0.006 | **0.443 ± 0.005** |
| Concatenation | 0.426 ± 0.008 | **0.428 ± 0.012** | 0.424 ± 0.003 |
| Fixed fusion | 0.358 ± 0.008 | 0.361 ± 0.008 | **0.374 ± 0.007** |
| Single (no history) | 0.437 ± 0.007 | | |

- The rise for adaptive fusion (+0.009 from k = 1 to 5) is within the seed spread, so call it a trend, not a result. Its largest gain over Single is 0.006, at k = 5.
- k = 1 is a weak test of speaker separation: with one previous turn, only 20% of MELD training utterances have any same-speaker history, against 65% at k = 3 and 69% at k = 5. About 10% of utterances open a dialogue and have no history at all.

### Inside the adaptive gate

The gate learned to mostly ignore the history: it gives the current utterance 0.84 of the weight when all three sources exist, where fixed fusion gives 0.33. Mean weights on the MELD test set (adaptive fusion, k = 3, mean over seeds 42, 43 and 44; each seed within 0.01):

| Sources available | Test utterances | Current | Same speaker | Other speakers | Fixed fusion gives |
|---|---:|---:|---:|---:|---|
| current only (first turn) | 280 (11%) | 1.00 | – | – | 1.00 |
| current + one history group | 961 (37%) | 0.89 | 0.11 (whichever exists) | | 0.50 each |
| all three | 1,369 (52%) | 0.84 | 0.11 | 0.05 | 0.33 each |

- **This explains the main results.** Fixed fusion forces a third of the weight onto history and drops to 0.361. Forcing equal weights into the trained adaptive model drops it to 0.349. Adaptive fusion ties Single because it is mostly Single.
- **Same-speaker history gets twice the weight of other-speaker history** (0.11 vs 0.05). This is the one sign that the model uses the speaker split.
- **The weights barely change between utterances.** For 80% of utterances with all three sources, the current weight is between 0.79 and 0.88.
- **They do not depend on length.** The correlation between utterance length and current weight is between −0.01 and +0.01 on every seed, so the idea that the gate leans on context for short replies is not supported.
- **Short replies** (3 words or fewer, 27% of the MELD test set) are where context should matter most, yet Single, concatenation and adaptive fusion all score 0.506 on them over three seeds. The concatenation lead seen on seed 42 (+0.040) reverses on seeds 43 and 44 (−0.024 and −0.017).
- **EmoryNLP's gate leans more on history:** 0.77 on the current utterance when all three sources exist (MELD 0.84), consistent with context helping there. With BERT and RoBERTa on MELD the gate gives 0.84 and 0.80; with BiLSTM it gives 1.00.

Per-utterance weights: `outputs/runs/<dataset>_adaptive*_s<seed>/fusion_weights_test.csv`.

### Traditional baselines

Nineteen term weighting × classifier pairs per dataset, each reading the current utterance only, with every setting (n-grams, min_df, C or alpha, class weights, leaf size) chosen on dev Macro-F1; one deterministic run each. Test Macro-F1 of each classifier with the weighting that dev selected for it:

| Classifier | MELD | EmoryNLP | DailyDialog |
|---|---:|---:|---:|
| Logistic regression | 0.360 (TF-IDF) | **0.279** (TF) | 0.448 (binary) |
| Linear SVM | **0.382** (TF-IDF) | 0.272 (TF) | **0.485** (TF) |
| Multinomial naive Bayes | 0.352 (binary) | 0.251 (TF) | 0.432 (binary) |
| Complement naive Bayes | 0.328 (TF) | 0.251 (TF-IDF) | 0.431 (TF-IDF) |
| Random forest (300 trees) | 0.358 (BM25) | 0.278 (binary) | 0.437 (TF) |
| Best DistilBERT model (table above) | 0.438 | 0.292 | 0.489 |

Bold: the pair selected on dev over all 19.

<details>
<summary>Test Macro-F1 of every pair (bold: selected on dev)</summary>

| MELD | binary | TF | TF-IDF | BM25 |
|---|---:|---:|---:|---:|
| logistic regression | 0.385 | 0.385 | 0.360 | 0.342 |
| linear SVM | 0.376 | 0.373 | **0.382** | 0.355 |
| multinomial NB | 0.352 | 0.340 | 0.342 | 0.327 |
| complement NB | 0.332 | 0.328 | 0.325 | 0.314 |
| random forest | 0.355 | 0.368 | 0.338 | 0.358 |

| EmoryNLP | binary | TF | TF-IDF | BM25 |
|---|---:|---:|---:|---:|
| logistic regression | 0.270 | **0.279** | 0.286 | 0.254 |
| linear SVM | 0.253 | 0.272 | 0.269 | 0.250 |
| multinomial NB | 0.245 | 0.251 | 0.246 | 0.257 |
| complement NB | 0.252 | 0.247 | 0.251 | 0.256 |
| random forest | 0.278 | 0.278 | 0.268 | 0.277 |

| DailyDialog | binary | TF | TF-IDF | BM25 |
|---|---:|---:|---:|---:|
| logistic regression | 0.448 | 0.444 | 0.437 | 0.442 |
| linear SVM | 0.480 | **0.485** | 0.479 | 0.467 |
| multinomial NB | 0.432 | 0.433 | 0.401 | 0.411 |
| complement NB | 0.426 | 0.423 | 0.431 | 0.437 |
| random forest | 0.442 | 0.438 | 0.445 | 0.444 |

</details>

- **A linear model is the best traditional classifier on every dataset**, although random forest comes within 0.001 on EmoryNLP; naive Bayes is the weakest.
- **The pretrained encoder's lead depends on the dataset:** the best DistilBERT model is +0.056 on MELD, +0.013 on EmoryNLP and +0.004 on DailyDialog, where a linear SVM on term counts is level with DistilBERT. Without context, DistilBERT trails the selected pair on EmoryNLP (0.270 vs 0.279).
- **The classifier matters more than the weighting.** On MELD, plain word presence (binary) works as well as TF-IDF. BM25 is never the weighting dev selects for a linear model.
- **Pick on dev, not test.** On MELD the best test score (0.385, binary + LR) is not the pair dev picked (0.382); on EmoryNLP, TF-IDF + LR has the best test score (0.286) but dev picked TF + LR (0.279). Report the dev-selected pair.
- **DailyDialog is the exception.** The SVM at 0.485 is level with DistilBERT. A likely reason, not tested: its 87k training utterances, nine times MELD's.
- **Random forest grid.** A first grid with minimum leaf sizes 1 and 2 always chose 2 on dev and spent about 90% of its time on leaf size 1, so the final grid uses 2 and 5. Six of the nine earlier runs give identical results; three now pick 5 on dev and score 0.005–0.023 lower on test. No conclusion changes.

Scores of every pair are in the "term weighting x classifier" tables of [outputs/results_summary.md](outputs/results_summary.md), every grid point in [outputs/hparams_grid.csv](outputs/hparams_grid.csv).

### Model size and speed

The gate costs 0.9% more parameters and about 25% more inference time than concatenation, for no measurable accuracy gain. MELD, k = 3; latency is end to end (tokenise, forward pass, argmax) at batch size 1 on one A40 GPU:

| Model | Parameters | Of which gate | Latency (ms per utterance) | Test Macro-F1 |
|---|---:|---:|---:|---:|
| TF-IDF + LR | 0.27M weights | – | 0.67 (CPU) | 0.360 |
| Single | 66.37M | – | 3.96 | 0.437 |
| Concatenation | 66.37M | – | 3.95 | 0.428 |
| Fixed fusion | 66.37M | – | 4.65 | 0.361 |
| Adaptive fusion | 66.96M | 0.59M | 4.94 | 0.438 |
| Adaptive merged | 66.76M | 0.39M | 4.73 | 0.435 |

- The DistilBERT encoder is 66.36M of every neural model; the classifier head is 5,383 parameters.
- Fusion is slower than concatenation because each history turn goes through the encoder separately (up to four passes at k = 3, instead of one longer one).
- The pattern repeats on the other datasets: adaptive fusion is 21% slower than concatenation on EmoryNLP and 20% on DailyDialog.

### Other encoders

MELD, k = 3, test Macro-F1 over three seeds. Every encoder sees the same word pieces under the same token budget, training settings and dev selection; recurrent encoders read DistilBERT's word-piece embeddings (frozen) and train for up to 10 epochs.

| Encoder | Single | Concatenation | Fixed fusion | Adaptive fusion | Trained parameters | ms per utterance |
|---|---:|---:|---:|---:|---:|---:|
| DistilBERT | 0.437 ± 0.007 | 0.428 ± 0.012 | 0.361 ± 0.008 | 0.438 ± 0.006 | 66.4M | 4.0–4.9 |
| BERT-base | 0.446 ± 0.004 | 0.459 ± 0.007 | 0.384 ± 0.002 | 0.457 ± 0.012 | 109.5M | 8.5–9.6 |
| RoBERTa-base | 0.457 ± 0.002 | **0.470 ± 0.005** | 0.396 ± 0.007 | 0.468 ± 0.010 | 124.7M | 8.6–9.6 |
| RNN | 0.354 ± 0.006 | 0.320 ± 0.002 | | | 0.26M | 1.0–1.4 |
| Bidirectional RNN | 0.375 ± 0.005 | 0.322 ± 0.003 | | | 0.53M | 1.1–1.8 |
| LSTM | 0.402 ± 0.005 | 0.396 ± 0.015 | | | 1.1M | 1.0–1.4 |
| BiLSTM | 0.391 ± 0.009 | 0.391 ± 0.008 | 0.324 ± 0.005 | 0.391 ± 0.002 | 2.1M | 1.1–1.9 |
| GRU | 0.412 ± 0.011 | 0.417 ± 0.009 | | | 0.79M | 1.0–1.4 |
| Bidirectional GRU | 0.401 ± 0.012 | 0.406 ± 0.005 | | | 1.6M | 1.1–1.8 |

Recurrent encoders also hold a frozen 23.4M word-piece embedding table. Latency is end to end at batch size 1 on one A40, from the fastest to the slowest architecture of each encoder.

- **Larger encoders score higher, at twice the latency.** RoBERTa-base single beats DistilBERT single by 0.020 (p = 0.02); BERT-base by 0.010 (p = 0.21).
- **The architecture ranking is the same for every Transformer.** Adaptive fusion and concatenation are level (BERT −0.002, RoBERTa −0.002, p ≥ 0.76), fixed fusion is 0.07 below adaptive (p < 0.001). With BERT and RoBERTa, both context models are about 0.011–0.014 above the single-utterance model (p = 0.07–0.16), a gain DistilBERT does not show.
- **The gate behaves the same way in every Transformer:** it gives the current utterance 0.84 (DistilBERT), 0.84 (BERT) and 0.80 (RoBERTa) of the weight when all three sources exist. On BiLSTM it gives the current utterance all of the weight, so adaptive fusion equals the single-utterance model.
- **Recurrent encoders are about four times faster than DistilBERT but at least 0.02 lower.** LSTM and GRU variants beat the best traditional model (0.382); the RNNs do not, and concatenating history hurts them (0.354 → 0.320 one-directional). Bidirectionality helps only the single-utterance RNN.

### Hyper-parameter sweep

MELD, DistilBERT, k = 3: one setting changed at a time around the reference (learning rate 2e-5, batch size 16, dropout 0.1). Each configuration trains its single learning rate and selects the epoch on dev. Test Macro-F1 over three seeds:

| Setting | Single | Adaptive fusion |
|---|---:|---:|
| reference | 0.438 ± 0.004 | 0.438 ± 0.006 |
| learning rate 1e-5 / 3e-5 / 5e-5 / 1e-4 | 0.424 / 0.442 / 0.432 / 0.427 | 0.417 / 0.430 / 0.438 / 0.415 |
| batch size 8 / 32 | 0.430 / 0.426 | 0.447 / 0.425 |
| dropout 0 / 0.3 | 0.432 / 0.428 | 0.448 / 0.430 |

- **Learning rates from 2e-5 to 5e-5 form a plateau**; 1e-5 and 1e-4 lose 0.01–0.025.
- **No change raises either model by more than 0.011**, and neither model wins under every setting: adaptive minus single ranges from −0.012 (learning rate 3e-5 and 1e-4) to +0.017 (batch size 8, dropout 0). The main comparison is therefore not an artefact of the chosen settings.
- On dev, the best single change is dropout 0 for the single-utterance model (0.440 vs 0.428) and batch size 8 for adaptive fusion (0.448 vs 0.441); on test both stay within 0.01 of the reference.

Every setting with dev and test scores is in [outputs/hparams_summary.md](outputs/hparams_summary.md) and `outputs/hparams_sweep.csv`.

---

## For the presentation: how to say it

The honest story is a useful one: history only helps if the model can turn it down, and our gate learns to do exactly that. Answers to the three research questions (slides 15 and 18):

| Research question | Answer | Evidence |
|---|---|---|
| 1. Do 1, 3 or 5 previous turns help? | Barely on MELD: adaptive fusion rises slightly with k, concatenation does not. On EmoryNLP, concatenation beats Single by 0.022 (p = 0.009). | MELD adaptive 0.434 → 0.438 → 0.443; concatenation 0.426 → 0.428 → 0.424; Single 0.437 |
| 2. Does separating the speaker's own history help? | No clear gain, but the gate does prefer it. | separated 0.438 vs pooled 0.435 (p = 0.56); same-speaker weight 0.11 vs other-speaker 0.05 |
| 3. Do learned weights beat concatenation or equal weights? | Beat equal weights clearly; tie with concatenation. | vs fixed +0.077 (p < 0.001); vs concatenation +0.010 (p = 0.23); same with BERT and RoBERTa |

**Script lines that are safe to say**

- "Adaptive fusion has the best mean on MELD and DailyDialog, and the smallest spread across seeds of the four main models there. On EmoryNLP, concatenation and even TF-IDF are slightly ahead."
- "Weighting matters: averaging the history with equal weights costs 7.7 points of Macro-F1, and a paired bootstrap confirms that gap."
- "The gate weights have a physical meaning: how much the model trusts each source. It trusts the current utterance about 85%, and the speaker's own past twice as much as other people's."
- "For these datasets, the current utterance carries most of the signal. Context is cheap to add but hard to use well. EmoryNLP is the exception: there context adds 2 points, and the gate leans more on history."
- "A bigger encoder helps more than context: RoBERTa-base adds 2 points over DistilBERT at twice the latency, and the ranking of the architectures stays the same."
- "Fusion costs about 25% more inference time than concatenation, for no accuracy gain here."

**Do not say**

- That adaptive fusion improves over Single or concatenation: p = 0.82 and 0.23 over three seeds.
- That context or speaker separation helps in general: only EmoryNLP shows a significant context gain.
- That the gate helps most on short replies: its weights do not depend on length, and every model scores 0.506 on them.
- That DailyDialog's fusion numbers test speaker separation: it has no speaker IDs, so it uses the merged versions.
- Any comparison with published state-of-the-art numbers: they use larger encoders, other metrics (often Weighted-F1) and other preprocessing.

**Likely questions**

- *"0.44 Macro-F1 looks close to guessing."* Guessing the majority class gives 0.093. Seven imbalanced classes and noisy labels keep scores low: in MELD train, 105 distinct texts carry more than one gold label, and "what?" is labelled surprise 39 times and neutral 21 times. Weighted-F1 is 0.61.
- *"Why does fixed fusion do so badly?"* It forces a third of the weight onto history. Averaged history drowns the current utterance; the gate learns to turn it down to about 15%.
- *"Then what is the contribution?"* A controlled comparison: every model sees the same text under the same token budget, so differences come from how context is combined. It shows that a cheap, interpretable gate recovers what equal weights lose.
- *"Why DistilBERT?"* The project is about lightweight models: 66M parameters and under 5 ms per utterance. RoBERTa-base scores 0.02 higher at twice the latency (8.6 vs 4.0 ms), and the ranking of the architectures stays the same.
- *"How do you know you did not tune on the test set?"* Every choice (learning rate, epoch, grid point) is made on dev Macro-F1; each checkpoint is scored on test once.

---

## For the presentation: where to find things

Everything below is on `main`, including the run folders of both GPU batches. Rebuild the tables after new runs arrive (see the end of this section).

**A: problem, audience and research questions (slides 1–4, 18–19)**

| Topic | Where | Status |
|---|---|---|
| Problem, audience, purpose | The group proposal (PDF, not in the repository); [Why this project is useful](#why-this-project-is-useful) | Now |
| Problem statement and the three research questions | [docs/TECHNICAL.md §1](docs/TECHNICAL.md#1-problem-and-research-questions) | Now |
| Answers to the research questions, script lines, likely questions | [For the presentation: how to say it](#for-the-presentation-how-to-say-it), [Results so far](#results-so-far) (with significance tests) | Now |

**B: idea, architecture, data and design choices (slides 5–9)**

| Topic | Where | Status |
|---|---|---|
| Related work, CoMPM comparison, fusion formula, gate size | [Method](#method), [Models compared](#models-compared), [docs/TECHNICAL.md §4](docs/TECHNICAL.md#4-models) | Now |
| Architecture code | [models/neural.py](models/neural.py) (`FusionClassifier`) | Now |
| Datasets, splits, labels, imbalance, duplicates | [docs/DATA.md](docs/DATA.md) (columns used, cleaning steps), [docs/TECHNICAL.md §2](docs/TECHNICAL.md#2-data), [outputs/data_audit.md](outputs/data_audit.md) | Now |
| Training settings and why | [docs/TECHNICAL.md §5 and §9](docs/TECHNICAL.md#5-training-and-model-selection) | Now |
| Parameter counts per model, full hyper-parameter table, learning rate and epoch each run selected | [outputs/model_details.md](outputs/model_details.md) (`python -m eval.model_details`); summary under [Model comparison](#model-comparison-other-encoders-and-traditional-baselines) | Now |
| How hyper-parameters change results | [docs/HYPERPARAMETERS.md](docs/HYPERPARAMETERS.md), [outputs/hparams_summary.md](outputs/hparams_summary.md), [outputs/hparams_grid.csv](outputs/hparams_grid.csv) | Now |
| Engineering: pinned data, config generator, resumable runs, tests | [docs/TECHNICAL.md §10](docs/TECHNICAL.md#10-engineering-reproducibility-and-testing), [tests/](tests/) (`python -m pytest -q`: 114 tests) | Now |

**C: experiments and results (slides 10–14)**

| Topic | Where | Status |
|---|---|---|
| Baselines, metrics, seeds, selection protocol | [docs/TECHNICAL.md §6–7](docs/TECHNICAL.md#6-evaluation) | Now |
| Main comparison, per-class F1, latency | [Results so far](#results-so-far), [Model size and speed](#model-size-and-speed); [outputs/results_summary.md](outputs/results_summary.md) "main comparison" | Now |
| Chart data (mean and std per model, dataset and k) | [outputs/results_summary.csv](outputs/results_summary.csv); per seed: [outputs/results_runs.csv](outputs/results_runs.csv) | Now |
| Context length (k = 1, 3, 5) and ablations | [Context window](#context-window), [Inside the adaptive gate](#inside-the-adaptive-gate); [outputs/results_summary.md](outputs/results_summary.md) "context length", "ablations" | Now |
| GPU time per configuration | [outputs/run_all_status.log](outputs/run_all_status.log) (one A40: 7.75 h for the original study, 7.66 h for the second batch) | Now |
| Other encoders (BERT, RoBERTa, RNN/LSTM/GRU), term weighting × classifier, sweep | [Other encoders](#other-encoders), [Traditional baselines](#traditional-baselines), [Hyper-parameter sweep](#hyper-parameter-sweep); `outputs/results_summary.md` "encoder comparison", "term weighting x classifier"; chart data in [outputs/results_comparison.csv](outputs/results_comparison.csv) | Now |

**D: interpretation and demo (slides 15–17)**

| Topic | Where | Status |
|---|---|---|
| What the results mean, what not to overstate | [For the presentation: how to say it](#for-the-presentation-how-to-say-it), [docs/HANDOVER2.md](docs/HANDOVER2.md) | Now |
| Gate weights per utterance (how much the model trusts each source) | [Inside the adaptive gate](#inside-the-adaptive-gate); `outputs/runs/<dataset>_adaptive*_s<seed>/fusion_weights_test.csv`, e.g. [MELD seed 42](outputs/runs/meld_adaptive_k3_s42/fusion_weights_test.csv) | Now |
| Limitations | [docs/TECHNICAL.md §11](docs/TECHNICAL.md#11-limitations-and-risks) | Now |
| Live demo | [app/](app/) (`streamlit run app/streamlit_app.py`; setup in [app/README.md](app/README.md)) | Now |

**Rebuilding the tables.** Each command reads `outputs/runs/`, so run it after pulling new run folders:

```bash
python -m eval.aggregate        # results_summary.md / .csv, results_comparison.csv
python -m eval.model_details    # model_details.md
python -m eval.hparams          # hparams_summary.md and hparams_*.csv
```

`eval.aggregate` stops with an error instead of rebuilding `results_summary.*` when runs listed in `outputs/results_runs.csv` are missing from `outputs/runs/`, so a partial checkout never overwrites the committed tables. `eval.model_details` and `eval.hparams` only write their own files.

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

Model size, from [outputs/model_details.md](outputs/model_details.md) (MELD, 7 classes):

| Model | Parameters | Trained parameters |
|---|---:|---:|
| DistilBERT: single, concatenation, fixed fusion | 66.37M | 66.37M |
| DistilBERT: adaptive fusion (gate 0.59M, 0.9%) | 66.96M | 66.96M |
| BERT-base / RoBERTa-base, single | 109.49M / 124.65M | all |
| RNN, LSTM, GRU and bidirectional variants, single | 23.7M–25.5M | 0.26M–2.10M (word-piece embeddings frozen) |
| TF-IDF + LR | 0.27M weights (38,290 features × 7 classes) | all |

---

## Data

| Dataset | Train / dev / test utterances | Labels | License |
|---|---:|---|---|
| MELD | 9,989 / 1,109 / 2,610 | anger, disgust, fear, joy, neutral, sadness, surprise | GPL-3.0 |
| EmoryNLP (original text release) | 9,934 / 1,344 / 1,328 | joyful, mad, neutral, peaceful, powerful, sad, scared | Apache-2.0 |
| DailyDialog | 87,170 / 8,069 / 7,740 | anger, disgust, fear, happiness, no_emotion, sadness, surprise | CC BY-NC-SA 4.0 |

Which raw columns each dataset provides, which ones we use and every cleaning step are listed in [docs/DATA.md](docs/DATA.md).

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
