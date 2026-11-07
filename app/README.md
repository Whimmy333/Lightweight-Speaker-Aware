# app/ — two Streamlit front ends

Two versions of the demo, built on the same models and the same code in `core.py`:

| | Version 1: research demo | Version 2: Undertone |
|---|---|---|
| File | `streamlit_app.py` | `undertone_app.py` |
| Audience | Researchers and markers: the experiment, model by model | Consumers: a product that reads the mood of a chat with your partner |
| Datasets | MELD, EmoryNLP, DailyDialog | MELD |
| Input | Featured or test-set dialogue, or your own | Example couple chats, your own chat, or Friends test scenes |
| Main view | Table of every model's prediction per utterance, gate-weight charts, inspector | Chat bubbles with a mood per message and a “Based on” bar (the gate's weights) |
| Results | 📊 Results tab: all models, k, gate, size and latency | 📈 Does it work?: headline scores, score by model, gate, k, limits |
| Port | 8501 | 8502 |

```bash
pip install -r requirements.txt          # includes streamlit, plotly, pyarrow (pinned)
streamlit run app/streamlit_app.py       # version 1, from the repo root; opens http://localhost:8501
streamlit run app/undertone_app.py --server.port 8502 --theme.primaryColor "#e0457b"   # version 2
```

Both run on a laptop CPU. No GPU, no network needed once data and checkpoints are local. Both fall back to
TF-IDF when the neural checkpoints are missing. The sections below the Undertone one describe version 1 and
the shared set-up.

## Version 1: research demo (`streamlit_app.py`)

Pick a featured or test-set dialogue (or type your own) and see per-utterance emotion predictions from every
model side by side, the gate weights (current / same speaker / other speaker) for each turn, and the
aggregated results from `outputs/results_summary.csv`. Tabs: 🗣️ Live demo, 📊 Results, 🔧 Models.

## Version 2: Undertone (`undertone_app.py`)

Puts the same MELD models behind a consumer-style product: paste a chat with your partner (or pick an
example) and every message gets a mood, plus a bar showing how much of that reading came from the message
itself, the writer's own earlier messages and the other person's messages (the adaptive gate's weights).
It covers the same ground as version 1, in three tabs:

| Tab | Shows |
|---|---|
| 💞 Read a chat | Chat bubbles with a mood per message (adaptive weighting, k=3) and its source blend; the other person's mood mix, mood journey and the strongest difficult moment. Example chats, your own chat, or real MELD test scenes with the dataset's labels (✓/✗) |
| 🔬 Under the hood | The three sources, all five models side by side on the same chat, equal vs learned weights per message, what is installed |
| 📈 Does it work? | MELD test Macro-F1 and accuracy, score by model, where the gate looks (`core.gate_summary`), the effect of k, limits |

The friendly mood names (“annoyed”, “worried”, …) only relabel MELD's seven classes. Without neural
checkpoints it falls back to TF-IDF (“lite mode”) and says so; the example chats are hand-written and
unlabelled, so nothing is scored against them.

## What works without anything extra (version 1; version 2 needs the same files)

| Feature | Needs |
|---|---|
| Results tab (all charts, the “Where does the learned gate look?” and “How lightweight is it?” panels, the table) | nothing — reads `outputs/results_summary.csv`, the configs and the committed `fusion_weights_test.csv` of every seed |
| Featured dialogues and “Write your own” (TF-IDF needs the row below; neural models need theirs) | nothing to show the text |
| MELD / EmoryNLP test-set dialogues with gold labels | nothing — falls back to the committed `outputs/runs/<ds>_tfidf_lr/predictions_test.csv` |
| **TF-IDF + LR live predictions** | `python prepare_data.py` once (training data), then `python -m app.warm_cache` (re-runs the configured grid from `models/tfidf_lr.py`, ~1–2 min per dataset on a laptop, longer for DailyDialog; cached in `outputs/demo_cache/`). Without the warm-up the app trains on first use behind a spinner. Reproduces the committed baseline exactly (identical MELD and EmoryNLP test predictions). |
| Neural models, live on any dialogue | their checkpoints in `outputs/runs/` + the DistilBERT files from `prepare_data.py` |
| Neural models on Featured / Test set dialogues (💾) | nothing, on all three datasets: the seed-42 runs' `predictions_test.csv` (+ `fusion_weights_test.csv`) are committed, and the app replays the cluster's exact outputs. A checkpoint, when present, takes over and also enables typed dialogues |

Models that cannot run are left out of “Models to compare” and listed under Model status (sidebar) and the 🔧 Models tab with the reason; the rest of the app keeps working. Maintainer instructions live only here, not in the app.

## Switching on a neural model

Copy the run directory from NTU EEE Cluster 02 into `outputs/runs/<run_name>/`. The app rescans on every
click, so no restart is needed. It looks for the checkpoint in this order:

1. the path in `best.json` (cluster paths are re-rooted onto the local run directory);
2. `outputs/runs/<run_name>/best.pt` (a single file dropped in by hand);
3. `lr_*/checkpoints/best.pt` (if two learning rates kept one, the higher dev Macro-F1 in `epoch_metrics.jsonl`).

The demo uses the main comparison setting (MELD, seed 42, k=3): `meld_single_s42`, `meld_concat_k3_s42`,
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
| `streamlit_app.py` | Version 1 UI: sidebar (dataset, models; k=3 and seed 42 fixed), Live demo / Results / Models tabs |
| `core.py` | No Streamlit: run discovery, checkpoint lookup, TF-IDF and neural predictors, dialogue parsing |
| `undertone_app.py` | Version 2 UI: consumer-style front end on the same models (see above) |
| `insights.py` | No Streamlit: example couple chats, friendly mood names, the per-chat summary used by Undertone |
| `examples.py` | `FEATURED`: real MELD test dialogues (dataset gold) that each show one effect of context, checked against the live checkpoints; `TEMPLATES`: unlabelled starting points for “Write your own” |
| `../tests/test_undertone.py` | Undertone helpers, and the page itself run headless on every source and without neural checkpoints |
| `../tests/test_app.py` | Discovery, checkpoint resolution, both predictors on a tiny random DistilBERT (no download); `test_featured_descriptions_hold` re-checks the featured blurbs against the real checkpoints (skips without them) |
| `../.streamlit/config.toml` | Fixed light theme so the demo looks the same everywhere |

## Walkthrough

- Best viewed at 1920×1080; collapse the sidebar (`<` at its top) for the results charts. The first load of
  each checkpoint takes a few seconds.
- Featured dialogues (MELD, k=3):
  - “Phoebe's break-in” (`dia105`, line 2, gold fear): only Adaptive weighting predicts fear, with about a third
    of its weight on Phoebe's earlier line (confidence 26%).
  - “You know it?” (`dia257`, line 2, gold surprise): the context models (Concat, Adaptive) predict surprise;
    TF-IDF and Single predict neutral.
  - “Mr. Big” (`dia92`, line 5, gold joy): Single is right; Concat and Adaptive follow the preceding small talk
    to neutral, so context can also mislead.
- Gold labels and ✓/✗ appear only for dataset dialogues. Typed dialogues and the templates are never scored.
  The paired templates (“Fine.”, “Really?”) probe whether a model uses context; with these checkpoints the
  label mostly stays the same in both contexts.
- Adaptive and Single are within the seed-to-seed spread on MELD test Macro-F1 (Results tab).
- The Results tab's gate panel averages the per-utterance gate weights over the test set and the three seeds:
  on MELD the current line gets 84% when both kinds of history exist (own earlier turns 11%, other speakers 5%),
  against 33% each for fixed weighting; 88% across all test lines.
