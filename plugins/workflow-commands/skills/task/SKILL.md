---
name: task
description: Create and work on a small standalone task without design/planning phases
user-invocable: false
---

# Task

## Overview

Quick workflow for small, well-defined work that doesn't need design or planning phases.

**Use when:** The work is clear, takes <1 hour, and doesn't require architectural decisions.

**Announce:** "I'm starting a tracked task."

## Arguments

`"<task description>" [--priority <0-4>]`

- Priority defaults to 3 (Normal)
- Priority 0 = Critical, 1 = High, 2 = Medium, 3 = Normal, 4 = Backlog

## Process

### Step 1: Create Tracking

```bash
# Create beads task
bd create "<task description>" -t task -p <priority>

# Log deciduous goal
deciduous add goal "Task: <task description>" -c 80
```

Note the task ID for later.

### Step 2: Work Directly

Do the work. For significant decisions during implementation, log them:

```bash
deciduous add decision "<what you chose> because <why>" -c 80
```

For discoveries:

```bash
bd comment <task-id> "LEARNED: <important finding>"
```

### Step 3: Verify & Complete

When done:

```bash
# Update status
bd update <task-id> --status done

# Log outcome
deciduous add outcome "Completed: <summary of what was done>"

# Verify (optional but recommended)
# Run tests, lint, etc.

# Close task
bd close <task-id> --reason "Complete"
```

### Step 4: Commit

```bash
git add .
git commit -m "<commit message>"
```

**Handoff:**

```
Task complete! Next steps:
- Create PR: `gh pr create`
- Or continue with more work
```

## When NOT to Use

Use `/workflow-commands:design` instead when:
- Multiple approaches are possible and need evaluation
- Architectural decisions are required
- The work will take multiple sessions
- Multiple people need to understand the design

## Examples

**Good use cases:**
- `/task "Add logging to auth middleware"`
- `/task "Update error message for invalid email" --priority 2`
- `/task "Add unit test for parseConfig function"`

**Use design workflow instead:**
- "Add user authentication" (architecture needed)
- "Refactor database layer" (significant design decisions)
- "Implement caching strategy" (multiple valid approaches)
