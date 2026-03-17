#!/usr/bin/env bash
# PreToolUse hook: sync tracking data before git commit
# Exports beads JSONL and deciduous patches, then stages them
# so tracking data is included in the same commit as code changes.

set -euo pipefail

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only act on git commit commands
if [ "$TOOL_NAME" != "Bash" ]; then
    exit 0
fi

if ! echo "$COMMAND" | grep -qE '^git\s+commit'; then
    exit 0
fi

# Flush beads JSONL if beads is initialized
if [ -f ".beads/beads.db" ]; then
    bd sync --flush-only 2>/dev/null || true
    git add .beads/issues.jsonl .beads/interactions.jsonl .beads/metadata.json 2>/dev/null || true
fi

# Export deciduous patch for current branch if deciduous is initialized
if [ -f ".deciduous/deciduous.db" ]; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$BRANCH" ]; then
        PATCH_FILE=".deciduous/patches/${BRANCH//\//-}.json"
        mkdir -p .deciduous/patches
        deciduous diff export \
            --branch "$BRANCH" \
            --output "$PATCH_FILE" \
            --base-commit "$(git rev-parse HEAD 2>/dev/null || echo '')" \
            2>/dev/null || true
        git add .deciduous/patches/ 2>/dev/null || true
    fi
fi

exit 0
