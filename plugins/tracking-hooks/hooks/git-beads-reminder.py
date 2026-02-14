#!/usr/bin/env python3
"""
PostToolUse hook that reminds about beads task updates
when git commit/push operations are detected.
"""
import json
import sys
import re
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Only process Bash tool
tool_name = input_data.get("tool_name", "")
if tool_name != "Bash":
    sys.exit(0)

tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

# Check if beads is initialized in this project
beads_db = os.path.join(os.getcwd(), ".beads", "beads.db")
if not os.path.exists(beads_db):
    sys.exit(0)

# Match git commit commands
if re.match(r"^git\s+commit", command):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Reminder: Link this commit to tracking:\\n"
                "- `bd comment <task-id> \"Committed: $(git rev-parse --short HEAD)\"` to link commit\\n"
                "- `deciduous add action \"Committed: <summary>\" --commit HEAD` to log with commit hash\\n"
                "\\n"
                "If this completes the task:\\n"
                "- `bd update <id> --status done && bd close <id> --reason \"<reason>\"`"
            )
        }
    }
    print(json.dumps(output))

# Match git push commands
elif re.match(r"^git\s+push", command):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Reminder: Sync tracking data:\\n"
                "- `bd sync` to push beads changes\\n"
                "- `deciduous sync` to export decision graph"
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
