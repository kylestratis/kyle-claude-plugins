---
name: bug
description: Fix a bug with investigation, root cause tracking, and verification
user-invocable: false
---

# Bug

## Overview

Workflow for fixing bugs with proper investigation and root cause tracking.

**Use when:** Something is broken and needs fixing.

**Announce:** "I'm investigating and fixing this bug."

## Arguments

`"<bug description>" [--priority <0-4>] [--blocks <task-id>]`

- Priority defaults to 2 (Medium) for bugs
- Use `--blocks` to link to a feature this bug is blocking

## Process

### Step 1: Create Tracking

```bash
# Create beads bug
bd create "Bug: <description>" -t bug -p <priority>

# Log deciduous goal
deciduous add goal "Fix: <description>" -c 70

# If blocking another task
bd dep add <blocker-id> <bug-id>
```

Note the bug ID.

### Step 2: Investigate

**CRITICAL: Find root cause before fixing.**

```bash
# Log investigation findings
bd comment <bug-id> "INVESTIGATION: <what you found>"
```

Use these investigation techniques:
1. Reproduce the bug
2. Find the failing code path
3. Identify root cause (not just symptoms)
4. Check for related issues

Log root cause when found:

```bash
deciduous add observation "Root cause: <detailed explanation>"
bd comment <bug-id> "ROOT CAUSE: <explanation>"
```

### Step 3: Fix

Implement the fix. Log what you're doing:

```bash
deciduous add action "Fixing: <approach>"
```

If you make design decisions about the fix:

```bash
deciduous add decision "Chose <fix approach> because <rationale>" -c 80
```

### Step 4: Verify

**CRITICAL: Verify the fix before closing.**

```bash
# Run relevant tests
# Add regression test if possible
# Confirm bug is actually fixed

bd comment <bug-id> "VERIFIED: <how you verified>"
```

### Step 5: Complete

```bash
# Update status
bd update <bug-id> --status done

# Log outcome
deciduous add outcome "Fixed: <summary of fix>"

# Close bug
bd close <bug-id> --reason "Fixed and verified"
```

### Step 6: Commit

```bash
git add .
git commit -m "fix: <description>"
```

**Handoff:**

```
Bug fixed! Next steps:
- Create PR: `gh pr create`
- Or continue with blocked work
```

## Bug Found During Feature Work

When you discover a bug while working on something else:

```bash
/bug "Found: <description>" --blocks <current-task-id>
```

This:
1. Creates a bug linked to current work
2. Lets you fix it now
3. Then resume the blocked feature

## Examples

**Simple bug:**
```
/bug "Login button doesn't respond on mobile"
```

**High priority:**
```
/bug "Users can't checkout - payment fails" --priority 1
```

**Bug blocking feature:**
```
/bug "Auth middleware crashes on empty token" --blocks beads-a1b2
```
