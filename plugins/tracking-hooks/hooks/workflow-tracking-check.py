#!/usr/bin/env python3
"""
PreToolUse hook that blocks workflow-commands skills if beads/deciduous
are not initialized (except for project-init which initializes them).
"""
import json
import sys
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Only process Skill tool
tool_name = input_data.get("tool_name", "")
if tool_name != "Skill":
    sys.exit(0)

tool_input = input_data.get("tool_input", {})
skill_name = tool_input.get("skill", "")

# Workflow commands that require tracking (skip project-init as it creates them)
WORKFLOW_SKILLS = [
    "workflow-commands:design",
    "workflow-commands:plan",
    "workflow-commands:execute",
    "workflow-commands:verify",
    "workflow-commands:explore",
    "workflow-commands:intake",
    # Also match the skill names directly
    "designing",
    "planning",
    "executing",
    "verifying",
    "exploring",
    "intake",
]

# Check if this is a workflow skill (case-insensitive partial match)
skill_lower = skill_name.lower()
is_workflow_skill = any(ws.lower() in skill_lower for ws in WORKFLOW_SKILLS)

if not is_workflow_skill:
    sys.exit(0)

# Check for beads and deciduous initialization
beads_exists = os.path.exists(os.path.join(os.getcwd(), ".beads", "beads.db"))
deciduous_exists = os.path.exists(os.path.join(os.getcwd(), ".deciduous"))

missing = []
if not beads_exists:
    missing.append("beads (.beads/beads.db)")
if not deciduous_exists:
    missing.append("deciduous (.deciduous/)")

if missing:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": (
                f"<tracking_required>\n"
                f"The workflow skill '{skill_name}' requires tracking to be initialized.\n\n"
                f"Missing: {', '.join(missing)}\n\n"
                f"Run `/workflow-commands:project-init` first to initialize tracking.\n"
                f"</tracking_required>"
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
