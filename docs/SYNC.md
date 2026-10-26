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

- 2026-10-26 (chat): Slides 15–17 written into the team deck (EE6405_Slides, currently positions 16–18, after the team's content) with ~45 s spoken scripts in the speaker notes. Slide 17's demo script is a stub until the app exists: Code, log the final screen flow here so chat can script it. Slide 17 promises five models side by side and gate weights per utterance.
- 2026-10-26 (chat): Created branch, this file, `CLAUDE.md` and the session hooks. Next for Code: build
  the demo skeleton with TF-IDF live + neural loaders that activate when checkpoints appear. Next for
  chat: slides 15–17 and script, cut to fit the 10-minute cap.
