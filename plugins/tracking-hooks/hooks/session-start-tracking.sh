#!/usr/bin/env bash
set -euo pipefail

# Session start hook: Check for beads/deciduous and surface tracking state

BEADS_INITIALIZED=false
DECIDUOUS_INITIALIZED=false
CONTEXT=""

# Check for beads
if [ -f ".beads/beads.db" ]; then
  BEADS_INITIALIZED=true
  # Get count of open tasks
  if command -v bd &> /dev/null; then
    OPEN_TASKS=$(bd list 2>/dev/null | grep -cE "(in_progress|todo|blocked)" || echo "0")
    if [ "$OPEN_TASKS" -gt 0 ]; then
      CONTEXT="${CONTEXT}Beads: ${OPEN_TASKS} open task(s). Run 'bd list' or 'bd ready' to see them.\\n"
    fi
  fi
fi

# Check for deciduous
if [ -d ".deciduous" ]; then
  DECIDUOUS_INITIALIZED=true
fi

# Build context message
if [ "$BEADS_INITIALIZED" = true ] || [ "$DECIDUOUS_INITIALIZED" = true ]; then
  TRACKING_MSG="<tracking_reminder>\\n"
  
  if [ "$BEADS_INITIALIZED" = true ]; then
    TRACKING_MSG="${TRACKING_MSG}✓ Beads task tracking is available in this project.\\n"
  fi
  
  if [ "$DECIDUOUS_INITIALIZED" = true ]; then
    TRACKING_MSG="${TRACKING_MSG}✓ Deciduous decision journaling is available in this project.\\n"
  fi
  
  if [ -n "$CONTEXT" ]; then
    TRACKING_MSG="${TRACKING_MSG}\\n${CONTEXT}"
  fi
  
  TRACKING_MSG="${TRACKING_MSG}\\nConsider using the beads-deciduous-integration skill for guidance on when to track.\\n</tracking_reminder>"
  
  # Output JSON for Claude Code hook
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${TRACKING_MSG}"
  }
}
EOF
else
  # No tracking tools, output empty
  echo "{}"
fi

exit 0
