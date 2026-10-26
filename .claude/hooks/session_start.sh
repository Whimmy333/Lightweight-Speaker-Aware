#!/usr/bin/env bash
# SessionStart: pull the latest branch state, then print docs/SYNC.md into Claude's context.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
git pull --ff-only --quiet >/dev/null 2>&1 || echo "(sync hook: git pull skipped — local changes or offline)"
echo "=== docs/SYNC.md (shared board with Claude chat) ==="
cat docs/SYNC.md 2>/dev/null || echo "docs/SYNC.md not found"
exit 0
