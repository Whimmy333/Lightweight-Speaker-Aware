# Showing hyper-parameter effects

This page explains which hyper-parameter effects we
can show, where the numbers come from, what changed in the code to provide them, and how to plot them.

## What we can show

| question | data | available |
|---|---|---|
| How do learning rate and number of epochs change dev Macro-F1 (every neural model)? | `hparams_epochs.csv` | now |
| How do C, alpha, class weights, n-grams and min_df change dev Macro-F1 (traditional models)? | `hparams_grid.csv` | now |
| How do learning rate, batch size and dropout change **test** Macro-F1 (Single and Adaptive on MELD)? | `hparams_sweep.csv` | now |
| How does the context window k change results? | `results_summary.md`, "context length" | now |

No result in these files is used to choose a setting of the main study. The main study's settings were
fixed before training, and its checkpoints are selected on dev Macro-F1 only.

## What changed in the code

- **No change to training.** Every neural run already trains each learning rate in its grid (2e-5 and
  5e-5 for Transformers, 1e-3 and 3e-3 for recurrent encoders) and logs dev metrics after every epoch in
  `outputs/runs/<run>/lr_<lr>/epoch_metrics.jsonl`. Traditional models log every grid point in
  `grid_search.csv`. These files only need to be collected.
- **New: `eval/hparams.py`** collects them into three tidy CSV files and a readable summary:
  `python -m eval.hparams` → `outputs/hparams_epochs.csv`, `outputs/hparams_grid.csv`,
  `outputs/hparams_sweep.csv`, `outputs/hparams_summary.md`.
- **New: sweep configurations** (`configs/generate_configs.py`, section 9; `run_all.sh`, section 9). On
  MELD with DistilBERT and k = 3, Single and Adaptive are trained with one setting changed at a time
  around the reference (learning rate 2e-5, batch size 16, dropout 0.1):

  | setting | values |
  |---|---|
  | learning rate | 1e-5, 2e-5, 3e-5, 5e-5, 1e-4 |
  | batch size | 8, 16, 32 |
  | dropout | 0.0, 0.1, 0.3 |

  Each sweep config trains a single learning rate, picks its epoch on dev and is evaluated once on test,
  so every setting has its own test score. Three seeds each: 18 settings × 3 seeds = 54 configurations,
  named `configs/meld/sweep_<model>_<setting>_s<seed>.yaml` (for example `sweep_single_lr0.0001_s42`).
  Their config has a `sweep: {param, value}` block.
- **`eval/aggregate.py`** keeps sweep runs out of the main tables. `results_summary.csv` (read by the
  demo) now holds the main study only; the encoder comparison, traditional baselines and sweeps go to
  `results_comparison.csv`.

## The files

All files have one row per measurement and plain column names.

**`hparams_epochs.csv`**: one row per (run, learning rate, epoch).
`run_name, dataset, model, arch, backbone, k, seed, sweep_param, sweep_value, lr, epoch, train_loss,
dev_macro_f1, dev_weighted_f1, dev_accuracy, epoch_seconds, selected`.
`selected` is true for the (learning rate, epoch) the run kept. `model` is the configured model name
(`adaptive`, `bert_concat`, `bilstm_single`, ...); `arch` and `backbone` split it into architecture and
encoder.

**`hparams_grid.csv`**: one row per grid point of a traditional model.
`dataset, model, weighting, classifier, <grid parameters>, dev_macro_f1, dev_weighted_f1, n_features,
fit_seconds, selected`. The grid parameters are `ngram_range, min_df` plus `C, class_weight` (lr, svm),
`alpha` (mnb, cnb), `fit_prior` (mnb) or `n_estimators, min_samples_leaf, class_weight` (rf). They are
stored as text (`"[1, 2]"`, `"None"`); convert with `pd.to_numeric` where needed.

**`hparams_sweep.csv`**: one row per sweep run.
`run_name, dataset, model, arch, backbone, k, seed, sweep_param, sweep_value, selected_lr,
selected_epoch, dev_macro_f1, test_macro_f1, test_weighted_f1, latency_ms`.

## Plotting examples

Learning-rate curves over epochs for one model (Plotly, as in the demo):

```python
import pandas as pd
import plotly.express as px

ep = pd.read_csv("outputs/hparams_epochs.csv")
g = ep[(ep.dataset == "meld") & (ep.model == "adaptive") & (ep.k == 3)]
mean = g.groupby(["lr", "epoch"], as_index=False).dev_macro_f1.agg(["mean", "std"])
fig = px.line(mean, x="epoch", y="mean", error_y="std", color=mean.lr.map("{:g}".format), markers=True,
              labels={"mean": "dev Macro-F1", "color": "learning rate"})
```

Sweep: test Macro-F1 against the learning rate, one line per model:

```python
sw = pd.read_csv("outputs/hparams_sweep.csv")
lr = sw[sw.sweep_param == "lr"].groupby(["arch", "sweep_value"], as_index=False).test_macro_f1.agg(["mean", "std"])
fig = px.line(lr, x="sweep_value", y="mean", error_y="std", color="arch", log_x=True, markers=True,
              labels={"sweep_value": "learning rate", "mean": "test Macro-F1"})
```

Traditional models: effect of C for logistic regression under each weighting scheme:

```python
gr = pd.read_csv("outputs/hparams_grid.csv")
c = gr[(gr.dataset == "meld") & (gr.classifier == "lr")].assign(C=lambda d: pd.to_numeric(d.C))
best = c.groupby(["weighting", "C"], as_index=False).dev_macro_f1.max()  # best over the rest of the grid
fig = px.line(best, x="C", y="dev_macro_f1", color="weighting", log_x=True, markers=True)
```

## How to talk about it

- Curves from `hparams_epochs.csv` and `hparams_grid.csv` are **dev** scores. They show how the model
  selection behaved; they are not test results.
- Only the sweep has a test score per setting. Each point is a separate training run, and three seeds
  give the error bars; differences within about one standard deviation are noise.
- The sweep changes one setting at a time around one reference point. It shows sensitivity near that
  point, not the best possible combination.
- Recurrent encoders use larger learning rates (1e-3, 3e-3) than Transformers; compare learning-rate
  effects within an encoder family only.

## Regenerating

```bash
python -m eval.aggregate        # results tables (main study + comparison)
python -m eval.hparams          # hyper-parameter tables
python -m eval.model_details    # parameter counts and the full hyper-parameter list
```

All three read `outputs/runs/`, so they reflect whatever runs are present locally.
