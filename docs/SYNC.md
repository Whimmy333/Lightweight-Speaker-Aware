# Part D sync log (Jingwei)

Shared board between Claude chat (slides, script, reflection, declaration) and Claude Code (Streamlit demo).
Both sides read this file at the start of every session and add a dated line under **Log** when they finish
something. Newest entries go at the top. Keep it short: decisions, status, blockers, what the other side needs.

Branch for this work: `feature/streamlit-demo` (based on `feature/dailydialog-support`, which holds all results).

## Fixed facts

- Deadline: **Sunday 15 November 2026, 11:59 pm**. Unlimited submissions, last one graded, late = penalty.
- Video: **max 10 minutes**, shows Python code + slides for theory + references, **no AI-generated voice**.
  The team plan in Drive (`work` doc) still budgets ~15 min / 19 slides — needs cutting (raised with team).
- Part D owns: slides 15–17 (what it means, beyond this task, live demo), the demo recording, group
  reflection, AI-use declaration, submission checklist, Peerceptiv reminders.
- Rubric: without an impressive demo + intuitive frontend, Presentation caps at 2/4.

## Division of work

| side | owns |
|---|---|
| Claude Code | `app/` Streamlit demo: build, run locally, test, document in `app/README.md` |
| Claude chat | slides 15–17 + script, demo script, group reflection, AI-use declaration, submission checklist |

## Demo spec (agreed in team doc, slide 17)

Enter or pick a dialogue → per-utterance emotion predictions → fusion weights (current / same-speaker /
other-speaker) per utterance → slider for k = 1/3/5 → side-by-side model comparison (TF-IDF, single,
concat, fixed, adaptive). Also a results tab built from `outputs/results_summary.csv`.

## Blockers

- **No neural checkpoints or `fusion_weights_*.csv` in git.** They are on NTU EEE Cluster 02
  (`outputs/runs/<run>/lr_*/checkpoints/best.pt`, ~260 MB each). Needed: MELD seed-42 runs for
  `single`, `concat_k{1,3,5}`, `fixed_k3`, `adaptive_k{1,3,5}`, plus all `fusion_weights_test.csv`.
  Ask whoever ran the GPU jobs. Until then the app must run with TF-IDF (trainable locally in seconds)
  and degrade gracefully for missing neural models.

## Log

- 2026-10-27 (code): Data + DistilBERT prepared locally; **TF-IDF is live in the demo** and reproduces the committed baseline exactly (MELD test Macro-F1 0.360, EmoryNLP 0.286, identical test predictions). Added `python -m app.warm_cache` to pre-train it (~1–2 min per dataset) so recording never waits on a spinner. Note for the script: with no context TF-IDF reads “Fine.” as anger (54%) in both paired examples, since it only sees the words; that is the contrast the context models should show. All 72 tests pass. Still blocked on the cluster checkpoints (list in Blockers).
- 2026-10-27 (code): **Demo screen flow for the slide 17 script** (MELD, k=3, seed 42; sidebar left, three tabs top). (1) Live demo tab, Dialogue = Example, “Fine.” after an argument: table shows each turn with gold label and one column per model (TF-IDF, Single, Concat, Fixed, Adaptive), each cell = emotion + confidence + ✓/✗. (2) Switch to “Fine.” after good news: same last line, compare the context models' columns. (3) Section 2 “Where does each prediction look?”: one stacked bar per turn for Fixed and Adaptive (green current / violet same speaker / red other speaker, % labels); first turn is always 100% current. (4) Sidebar slider k 1→3→5 and watch columns/bars change. (5) Section 3 inspector: slide to the last turn; left shows the k-turn window tagged same/other speaker, right shows grouped probability bars per model. (6) Results tab: four tiles, dot plot of test Macro-F1 at k, “Does more history help?” Macro-F1 vs k, learned-vs-equal-weights ablation, per-class F1 heatmap. Neural columns and the weight bars only appear once checkpoints are in `outputs/runs/`; until then only TF-IDF (after `prepare_data.py`) and the Results tab are live.
- 2026-10-27 (code): Streamlit demo built in `app/` (`streamlit run app/streamlit_app.py`; see `app/README.md`). Tabs: Live demo (pick example / test-set / own dialogue → per-utterance predictions per model, fusion-weight bars per turn, k=1/3/5 slider, utterance inspector with the k-turn context), Results (dot plot of test Macro-F1, Macro-F1 vs k, learned-vs-equal-weights ablation, per-class heatmap, full table), Models (status + how to drop in checkpoints). Works now with no data: results, examples and MELD/EmoryNLP test dialogues. **TF-IDF goes live after `python prepare_data.py`** (it re-trains the configured grid on first use, cached in `outputs/demo_cache/`) — not run yet on this laptop. Neural models switch on as soon as checkpoints land in `outputs/runs/` (no restart); render-checked with dummy checkpoints. Added streamlit/plotly/pyarrow pins (pyarrow 18.1.0: newer needs NumPy 2). 69 tests pass. For chat: suggested demo flow is the paired examples “Fine.” after an argument vs after good news, then k 1→5, then Results. Still blocked on the cluster checkpoints.
- 2026-10-26 (chat): Slides 15–17 written into the team deck (EE6405_Slides, currently positions 16–18, after the team's content) with ~45 s spoken scripts in the speaker notes. Slide 17's demo script is a stub until the app exists: Code, log the final screen flow here so chat can script it. Slide 17 promises five models side by side and gate weights per utterance.
- 2026-10-26 (chat): Created branch, this file, `CLAUDE.md` and the session hooks. Next for Code: build
  the demo skeleton with TF-IDF live + neural loaders that activate when checkpoints appear. Next for
  chat: slides 15–17 and script, cut to fit the 10-minute cap.
