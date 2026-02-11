---
name: executing
description: Wrapper for ed3d execute-implementation-plan with beads/deciduous tracking
user-invocable: false
---

# Executing

## Overview

Wraps `ed3d-plan-and-execute:execute-implementation-plan` with integrated beads/deciduous tracking.

**Announce:** "I'm running a tracked implementation."

## Arguments

`<plan-dir> <workdir>`

## Before Starting

```bash
# Find tasks
bd list | grep -E "(Phase|Implement)"
bd ready

# Log goal
deciduous add goal "Execute: <feature>" --confidence 0.9
```

## During Execution

Invoke ed3d skill:
```
Use your Skill tool to engage the `executing-an-implementation-plan` skill from ed3d-plan-and-execute.
```

**CRITICAL OVERRIDE:** The ed3d skill will activate `finishing-a-development-branch` at the end. Follow that skill's merge/PR/keep/discard flow, but after completion, use the wrapper verify command from "After All Phases" below instead of stopping.

**For EACH phase:**

**Starting:**
```bash
bd update <phase-id> --status in_progress
deciduous add action "Starting Phase <N>: <desc>"
```

**During - log decisions as they happen:**
```bash
deciduous add decision "Implemented <component> using <approach> because <rationale>" --confidence 0.8
```

**Discoveries (LEARNED pattern):**
```bash
bd comment <phase-id> "LEARNED: <important discovery>"
```

**Completing:**
```bash
bd update <phase-id> --status done
deciduous add outcome "Completed Phase <N>: <summary>"
bd ready  # Check next phase
```

## After All Phases

```bash
deciduous add outcome "Implementation complete: <summary>"
bd update <epic-id> --status done
```

**Handoff (after finishing-a-development-branch completes):**

Tell the user:
```
Ready for verification. Run:

/workflow-commands:verify --task <epic-id>
```

Note: Unlike planning→execute, no `/clear` is needed here because the execution phase already ran with fresh context.
