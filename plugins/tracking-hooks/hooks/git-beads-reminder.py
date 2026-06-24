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
beads_dir = os.path.join(os.getcwd(), ".beads")
if not os.path.isdir(beads_dir):
    sys.exit(0)

# Match git commit commands
if re.match(r"^git\s+commit", command):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Reminder: If this commit completes a tracked task, consider:\\n"
                "- `bd close <id> --reason \"<reason>\"` to close with context\\n"
                "- `deciduous add outcome \"<summary>\"` to log the result"
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
