# When does context help?

**Short answer:** only where the current utterance alone is weak, and only when the model is free to turn
the history down. On EmoryNLP context helps. On MELD and DailyDialog with DistilBERT it adds nothing
measurable, and forcing it in with equal weights makes results worse.

Numbers are test Macro-F1, mean over seeds 42, 43 and 44, at k = 3 previous turns unless stated. p-values
come from a paired bootstrap: 10,000 resamples of test utterances, each scoring both models on the same
utterances for all three seeds.

## The answer, condition by condition

| Condition | Verdict | Evidence |
|---|---|---|
| EmoryNLP | **Helps** | Concatenation 0.292 vs single-utterance 0.270 (+0.022, p = 0.009); adaptive weighting +0.012 (p = 0.06). The gate gives history 23% of the weight (MELD 16%). |
| Larger encoders (BERT-base, RoBERTa-base), MELD | Helps a little, not significant | Concatenation and adaptive weighting are 0.011–0.014 above single (p = 0.07–0.16); with DistilBERT the gap is 0.002. |
| MELD and DailyDialog, DistilBERT | No gain | Adaptive vs single: +0.002 (p = 0.82) and +0.012 (p = 0.29). Concatenation vs single on MELD: −0.009 (p = 0.22). |
| More history (k = 1, 3, 5), MELD | No clear gain | Adaptive 0.434, 0.438, 0.443, within the seed spread; concatenation 0.426, 0.428, 0.424. |
| Short replies (3 words or fewer, 27% of MELD test) | No gain | Single, concatenation and adaptive weighting all score 0.506. The gate's weights do not change with length (correlation −0.01 to +0.01). |
| Separating the speaker's own history, MELD | No clear gain | Separated 0.438 vs pooled 0.435 (p = 0.56), although the gate weights same-speaker history twice as much as other speakers' (0.11 vs 0.05). |
| History forced in with equal weights (fixed weighting) | **Hurts** | MELD 0.361 vs single 0.437; EmoryNLP 0.248 vs 0.270. The learned gate recovers the loss: adaptive beats fixed by 0.077 and 0.035 (p < 0.001). |

## Why

When all three sources exist, the gate keeps 0.84 of the weight on the current utterance and gives 0.11 to
the same speaker and 0.05 to other speakers. This holds on every seed (0.84, 0.85, 0.84) and barely varies
between utterances (10–90% range 0.79–0.88). Adaptive weighting therefore behaves mostly like the
single-utterance model.

Fixed weighting gives each source a third, so two thirds of the weight goes to history and the current
utterance is drowned out. On EmoryNLP, where context does help, the gate leans more on history: 0.77 on
the current utterance.

The gate costs little in size but more in time. It adds 0.59M parameters (0.9% of the model), but each
history turn is encoded separately, so adaptive weighting takes 4.9 ms per utterance against 4.0 ms for
concatenation on an A40.

## What this means in practice

- Start from the single-utterance model, and add context only if it beats that model on dev for your data.
- If you add history, let the model weight it (a gate or attention); do not average it in with fixed weights.
- Test small gains with a paired test over seeds: most gaps here are smaller than one seed standard
  deviation.

## Where the numbers come from

- [README, Results so far](../README.md#results-so-far): main table, significance tests, context window,
  gate analysis and other encoders.
- [outputs/results_summary.md](../outputs/results_summary.md): every model, per-class F1 and latency.
- `outputs/runs/<dataset>_adaptive*_s<seed>/fusion_weights_test.csv`: the gate's weights for every test
  utterance.
