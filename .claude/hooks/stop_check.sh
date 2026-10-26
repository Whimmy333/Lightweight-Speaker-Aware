#!/usr/bin/env bash
# Stop: if work changed but docs/SYNC.md did not, ask Claude once to log it before stopping.
input=$(cat)
echo "$input" | grep -q '"stop_hook_active": *true' && exit 0
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
changed=$(git status --porcelain | grep -v 'docs/SYNC.md' | grep -v '^??.*\.claude/' )
unpushed=$(git log --oneline @{u}..HEAD 2>/dev/null)
synced=$( { git status --porcelain docs/SYNC.md; git diff --name-only @{u}..HEAD 2>/dev/null; } | grep 'SYNC.md')
if { [ -n "$changed" ] || [ -n "$unpushed" ]; } && [ -z "$synced" ]; then
  echo "You changed project files but did not update docs/SYNC.md. Add a dated (code) line to its Log, then commit and push so Claude chat sees it." >&2
  exit 2
fi
exit 0
