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
deciduous add goal "Execute: <feature>" -c 90  # -c takes integer 0-100, NOT float
```

## During Execution

Invoke ed3d skill:
```
Use your Skill tool to engage the `executing-an-implementation-plan` skill from ed3d-plan-and-execute.
```

**After ed3d completes:** Run local verification with `/workflow-commands:verify --task <epic-id>` to confirm all phase implementations meet requirements. Only if verification passes, proceed to the next step.

**For EACH phase:**

**Starting:**
```bash
bd update <phase-id> --status in_progress
deciduous add action "Starting Phase <N>: <desc>"
```

**During - log decisions as they happen:**
```bash
deciduous add decision "Implemented <component> using <approach> because <rationale>" -c 80
```

**Discoveries (LEARNED pattern):**
```bash
bd comment <phase-id> "LEARNED: <important discovery>"
```

**Completing:**
```bash
bd close <phase-id> --reason "Phase <N> complete"
deciduous add outcome "Completed Phase <N>: <summary>"
bd ready  # Check next phase
```

## After All Phases

```bash
deciduous add outcome "Implementation complete: <summary>"
bd close <epic-id> --reason "Implementation complete"
```

**After `finishing-a-development-branch` returns:**

If it created a GitHub pull request, immediately use the Skill tool to engage
`pr-review-loop` for that PR. Wait for Codex Review, fix legitimate findings,
reply with evidence to invalid findings, and continue until the skill's clean
exit conditions are met. Do not stop at PR creation.

If no pull request was created, skip `pr-review-loop`. The implementation is
complete.
