---
name: designing
description: Wrapper for ed3d start-design-plan with beads/deciduous tracking
user-invocable: false
---

# Designing

## Overview

Wraps `ed3d-plan-and-execute:start-design-plan` with integrated beads/deciduous tracking.

**Announce:** "I'm running a tracked design process."

## Before Starting

```bash
# Verify tracking
ls .beads/beads.db .deciduous/ || echo "Run /workflow-commands:project-init first"

# Create epic
bd create "Design: <feature>" -t epic -p 2

# Log goal
deciduous add goal "Design <feature>" --confidence 0.8
```

## During Design

Invoke ed3d skill:
```
Use your Skill tool to engage the `starting-a-design-plan` skill from ed3d-plan-and-execute.
```

**CRITICAL OVERRIDE:** The ed3d skill will output handoff instructions in Phase 6 telling the user to run `/ed3d-plan-and-execute:start-implementation-plan`. **DO NOT output those instructions.** Instead, use the wrapper command from "After Design" below.

**CRITICAL: Log every design decision during brainstorming (Phase 4):**

```bash
deciduous add decision "Chose <option> over <alternatives> because <rationale>" --confidence 0.8
```

Log decisions for:
- Architecture choices
- Technology selections
- API design
- Data model choices
- Trade-off resolutions

**Be explicit about WHY.**

## After Design

```bash
deciduous add outcome "Design complete: <summary>"
bd update <epic-id> --status done
bd comment <epic-id> "Design: <path>"
```

**Handoff (REPLACES ed3d Phase 6 handoff):**

Output this instead of the ed3d handoff instructions:

```
Design complete! Document committed to `docs/design-plans/<filename>`.

**IMPORTANT: Copy the command below BEFORE running /clear.**

(1) Copy this command now:

/workflow-commands:plan @docs/design-plans/<filename>.md .

(2) Clear context:

/clear

(3) Paste and run the copied command.
```
