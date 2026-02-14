---
name: continue
description: Resume work on an existing beads task with context recovery
user-invocable: false
---

# Continue

## Overview

Resume work on an existing task in a new session. Recovers context from beads and sets up for continued work.

**Use when:** Starting a new session and continuing previous work.

**Announce:** "I'm resuming work on this task."

## Arguments

`<task-id>`

- The beads task ID (e.g., `beads-a1b2` or just `a1b2`)

If no task ID provided, show available work:

```bash
bd ready
bd list --status=in_progress
```

## Process

### Step 1: Load Context

```bash
# Get task details
bd show <task-id>
```

Display to user:
- Task title and description
- Current status
- Dependencies (what's blocking/blocked by)
- Comments (especially LEARNED notes)

### Step 2: Claim Task

If not already in_progress:

```bash
bd update <task-id> --status in_progress
```

Log continuation:

```bash
deciduous add action "Continuing: <task title>"
```

### Step 3: Summarize State

Present the user with:

```markdown
## Resuming: <task title>

**Status:** <status>
**Priority:** <priority>

### Context
<description and notes from task>

### Recent Activity
<comments, especially LEARNED notes>

### Dependencies
- Blocked by: <list or "none">
- Blocking: <list or "none">

### Suggested Next Steps
<based on task type and state>
```

### Step 4: Work

Continue working on the task. Use normal patterns:

```bash
# Discoveries
bd comment <task-id> "LEARNED: <finding>"

# Decisions
deciduous add decision "<choice> because <rationale>" -c 80

# Progress
bd comment <task-id> "PROGRESS: <what was done>"
```

### Step 5: Complete (when done)

```bash
bd update <task-id> --status done
deciduous add outcome "Completed: <summary>"
bd close <task-id> --reason "Complete"
```

## Finding Tasks to Continue

If you don't remember the task ID:

```bash
# Show in-progress work
bd list --status=in_progress

# Show ready work (no blockers)
bd ready

# Search by text
bd search "<keyword>"
```

## Examples

**Direct resume:**
```
/continue beads-a1b2
```

**Find and resume:**
```
User: /continue
Claude: Here's your current work:

In Progress:
- beads-a1b2: Implement token refresh (High)

Ready to Start:
- beads-c3d4: Add logout endpoint (Normal)

Which task would you like to continue?
```
