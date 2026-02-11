---
name: planning
description: Wrapper for ed3d start-implementation-plan with beads/deciduous tracking
user-invocable: false
---

# Planning

## Overview

Wraps `ed3d-plan-and-execute:start-implementation-plan` with integrated beads/deciduous tracking.

**Announce:** "I'm creating a tracked implementation plan."

## Arguments

`@path/to/design.md <workdir>`

## Before Starting

```bash
# Check for epic
bd list | grep -i "design:"

# Log goal
deciduous add goal "Plan implementation for <feature>" --confidence 0.9
```

## During Planning

Invoke ed3d skill:
```
Use your Skill tool to engage the `starting-an-implementation-plan` skill from ed3d-plan-and-execute.
```

**CRITICAL OVERRIDE:** The ed3d skill will output handoff instructions telling the user to run `/ed3d-plan-and-execute:execute-implementation-plan`. **DO NOT output those instructions.** Instead, when you reach the handoff step, use the wrapper command from "After Planning" below.

**When phases are defined, create beads tasks:**

```bash
# Epic (if not exists)
bd create "Implement: <feature>" -t epic -p 2

# Task per phase with sequential dependencies
bd create "Phase 1: <desc>" -t task -p 3
bd dep add <phase1-id> <epic-id>

bd create "Phase 2: <desc>" -t task -p 3
bd dep add <phase2-id> <phase1-id>

# Continue for all phases...
```

**Log planning decisions:**
```bash
deciduous add decision "Ordered phases X→Y→Z because <rationale>" --confidence 0.85
```

## After Planning

```bash
deciduous add outcome "Plan created: <N> phases"
bd comment <epic-id> "Plan: <path>"
```

**Handoff (REPLACES ed3d handoff):**

Output this instead of the ed3d handoff instructions:

```
Implementation plan complete!

**IMPORTANT: Copy the command below BEFORE running /clear.**

(1) Copy this command now:

/workflow-commands:execute <absolute-plan-dir> <absolute-workdir>

(2) Clear context:

/clear

(3) Paste and run the copied command.
```

Use the actual absolute paths from the planning session (get them with `git rev-parse --show-toplevel`).
