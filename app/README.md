# app/ — Streamlit demo

Live demo for the video (slide 17): pick or type a dialogue, see per-utterance emotion predictions from every
model side by side, the fusion weights (current / same speaker / other speaker) for each turn, and the
aggregated results from `outputs/results_summary.csv`.

```bash
pip install -r requirements.txt          # includes streamlit, plotly, pyarrow (pinned)
streamlit run app/streamlit_app.py       # from the repo root; opens http://localhost:8501
```

Runs on a laptop CPU. No GPU, no network needed once data and checkpoints are local.

## What works without anything extra

| Feature | Needs |
|---|---|
| Results tab (all charts, the “How lightweight is it?” panel and the table) | nothing — reads `outputs/results_summary.csv` and the configs |
| Example dialogues and "write your own" | nothing |
| MELD / EmoryNLP test-set dialogues with gold labels | nothing — falls back to the committed `outputs/runs/<ds>_tfidf_lr/predictions_test.csv` |
| **TF-IDF + LR live predictions** | `python prepare_data.py` once (training data), then `python -m app.warm_cache` (re-runs the configured grid from `models/tfidf_lr.py`, ~1–2 min per dataset on a laptop, longer for DailyDialog; cached in `outputs/demo_cache/`). Without the warm-up the app trains on first use behind a spinner. Reproduces the committed baseline exactly (identical MELD and EmoryNLP test predictions). |
| Neural models, live on any dialogue | their checkpoints in `outputs/runs/` + the DistilBERT files from `prepare_data.py` |
| Neural models on test-set dialogues only (💾) | just the run's `predictions_test.csv` (+ `fusion_weights_test.csv` for fusion models) in `outputs/runs/<run>/`: the app replays the cluster's exact outputs. A checkpoint, when present, takes over |

Anything missing is listed in the sidebar and the 🔧 Models tab with the reason; the rest of the app keeps working.

## Switching on a neural model

Copy the run directory from NTU EEE Cluster 02 into `outputs/runs/<run_name>/`. The app rescans on every
click, so no restart is needed. It looks for the checkpoint in this order:

1. the path in `best.json` (cluster paths are re-rooted onto the local run directory);
2. `outputs/runs/<run_name>/best.pt` (a single file dropped in by hand);
3. `lr_*/checkpoints/best.pt` (if two learning rates kept one, the higher dev Macro-F1 in `epoch_metrics.jsonl`).

Wanted for the demo (MELD, seed 42, k=3 as agreed by the team): `meld_single_s42`, `meld_concat_k3_s42`,
`meld_fixed_k3_s42`, `meld_adaptive_k3_s42`. Checkpoints are ~260 MB each and git-ignored; never commit them.

```bash
rsync -av --include='*/' --include='best.json' --include='config.yaml' --include='best.pt' \
      --exclude='*' USER@<cluster-login>:<project>/outputs/runs/meld_adaptive_k3_s42 outputs/runs/
```

## How it reuses the project code

- Contexts: `data.context.build_contexts` — the same k-turn windows and same/other/unknown speaker relations as training.
- Neural inference: the checkpoint's saved config → `models.neural.build_model`, batched with
  `models.batching.Collator` (same 80-word-piece budget, same source pooling), all on CPU.
- TF-IDF: `models.tfidf_lr.run` with `configs/<ds>/tfidf_lr.yaml`, output redirected to `outputs/demo_cache/`.

## Files

| File | Content |
|---|---|
| `streamlit_app.py` | UI: sidebar (dataset, k, seed, models), Live demo / Results / Models tabs |
| `core.py` | No Streamlit: run discovery, checkpoint lookup, TF-IDF and neural predictors, dialogue parsing |
| `examples.py` | Hand-written dialogues in pairs ("Fine." after an argument vs after good news) |
| `../tests/test_app.py` | Discovery, checkpoint resolution, both predictors on a tiny random DistilBERT (no download) |
| `../.streamlit/config.toml` | Fixed light theme so the recording looks the same everywhere |

## Recording tips

- Record at 1920×1080 with the browser at 100% zoom; collapse the sidebar (`<` at its top) for the results charts.
- Warm up first: click each model once so checkpoints are loaded before you hit record (the first load of each takes a few seconds).
- Suggested flow: Example "“Fine.” after an argument" → its pair "after good news" (same last line, context
  changes the reading) → slide k from 1 to 5 → inspector on the last turn → Results tab.
