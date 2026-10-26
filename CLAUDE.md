# CLAUDE.md

EE6405 group project: speaker-aware context fusion for conversational emotion recognition (MELD,
EmoryNLP, DailyDialog). Read `README.md` and `docs/TECHNICAL.md` for how the pipeline works.

## Working with Jingwei (Part D)

- **Read `docs/SYNC.md` first** every session (the SessionStart hook prints it). It is the shared board
  with Claude chat, which works on slides, script and documents in parallel.
- When you finish a meaningful step, add one dated line at the top of the Log in `docs/SYNC.md`
  (`- YYYY-MM-DD (code): what changed, what chat or the team needs to know`), then commit and push.
- Work on branch `feature/streamlit-demo`. Do not push to `main` or `feature/dailydialog-support`;
  teammates own those. Never commit checkpoints, data or `.pt` files.
- Make ordinary engineering decisions yourself. Stop and ask only for things that need a human:
  cluster access, getting files from teammates, anything that changes shared branches.

## Demo (`app/`)

- Streamlit, Python only. Reuse `data/context.py` and `models/` instead of reimplementing context building
  or the fusion module. Load everything on CPU.
- Must run on a laptop with no GPU and work when neural checkpoints are missing (TF-IDF still live,
  other models shown as unavailable with a clear note).
- Keep it presentable on a 10-minute video: one clean screen per idea, readable at 1080p.
- Add Streamlit (and anything else) to `requirements.txt` with a pinned version.
