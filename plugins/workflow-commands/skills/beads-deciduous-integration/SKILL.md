---
name: beads-deciduous-integration
description: Reference for beads/deciduous tracking - used automatically by workflow-commands
user-invocable: true
---

# Beads & Deciduous Integration

## Key Principle

**Use `/workflow-commands:*` - they handle tracking automatically.**

| ❌ Don't use directly | ✅ Use instead |
|----------------------|----------------|
| `ed3d-plan-and-execute:start-design-plan` | `/workflow-commands:design` |
| `ed3d-plan-and-execute:start-implementation-plan` | `/workflow-commands:plan` |
| `ed3d-plan-and-execute:execute-implementation-plan` | `/workflow-commands:execute` |

## Automatic Tracking

| Command | Beads | Deciduous |
|---------|-------|-----------|
| `project-init` | Initializes `.beads/` | Initializes `.deciduous/` |
| `intake` | Creates epics | Logs goal/outcome |
| `explore` | Creates/closes task | Logs goal/outcome |
| `design` | Creates epic | **Logs all decisions** |
| `plan` | Creates phase tasks | Logs planning decisions |
| `execute` | Updates status | **Logs impl decisions** |
| `verify` | Closes epic | Logs outcome |
| `orchestrate` | Claims and reconciles tickets | Logs run action, wave and material routing/coupling decisions, and outcome |

## Tracked Export Allowlist

The default tracked export allowlist is exactly:

- `.beads/issues.jsonl`
- `.beads/interactions.jsonl`
- `.beads/metadata.json`
- `.deciduous/patches/**`

Repository directives may add exact paths. They never broaden the allowlist to a whole directory. If the effective allowlist is ambiguous, orchestration stops before claiming a ticket.

`orchestrating-beads-tickets` consumes this exact effective allowlist for source-content exclusions and reconciliation path proof.

Only these exported paths cross worktrees. The local Beads and Deciduous databases are untracked per-worktree state, so a workflow that spans multiple worktrees must mutate tracker state in one owning worktree and move the resulting allowlisted exports into any other worktree that commits them.

## Quick Reference

### Beads
```bash
bd init                          # Initialize
bd create "Task" -t task -p 3    # Create
bd list / bd ready               # View
bd update <id> --status in_progress  # Update status (no "done"; close to complete)
bd close <id> --reason "Done"    # Close
bd create "Phase" -t task --parent <epic-id>  # Hierarchy; remains ready
bd dep add <blocked-id> <blocker-id> --type blocks  # Hard prerequisite
bd comment <id> "LEARNED: ..."   # Note discoveries
```

### Deciduous
```bash
deciduous init
deciduous add goal "..." -c 80          # -c takes integer 0-100, NOT float
deciduous add decision "..." -c 80
deciduous add action "..."
deciduous add outcome "..."
deciduous nodes                         # View graph (also: edges, graph)
```

## Decision Quality

**Good:**
```bash
deciduous add decision "Chose PostgreSQL over MongoDB because: 1) ACID required, 2) team expertise, 3) JOIN performance" -c 85
```

**Bad:**
```bash
deciduous add decision "Using PostgreSQL" -c 80
```

## Commit Linking

Link commits to tracking for full traceability:

```bash
# After commit, link to beads task
bd comment <task-id> "Committed: $(git rev-parse --short HEAD)"

# Or link in deciduous with commit hash
deciduous add action "Implemented <feature>" --commit HEAD
```

## Entry Points

| Start From | When to Use |
|------------|-------------|
| `/workflow-commands:design` | New feature needing architecture |
| `/workflow-commands:plan` | Have design, need implementation tasks |
| `/workflow-commands:task` | Small standalone work (<1 hour) |
| `/workflow-commands:bug` | Fix a bug |
| `/workflow-commands:continue` | Resume existing work |
| `/workflow-commands:orchestrate` | Coordinate independent ready tickets in parallel |

## Full Workflow (Large Features)

```
/workflow-commands:project-init
    ↓
/workflow-commands:intake @roadmap.md --linear
    ↓
/workflow-commands:explore <topic>
    ↓
/workflow-commands:design
    ↓
/clear
/workflow-commands:plan @design.md .
    ↓
/clear
/workflow-commands:execute <plan> .
    ↓
/workflow-commands:verify --task <id>
    ↓
git commit / PR
```

## Quick Workflow (Small Tasks)

```
/workflow-commands:task "Add logging to auth"
    ↓
(work directly)
    ↓
git commit
    ↓
bd close <id>
```

## Bug Fix Workflow

```
/workflow-commands:bug "Users can't login"
    ↓
(investigate → find root cause → fix)
    ↓
git commit
    ↓
bd close <id>
```

## Resuming Work

```
/workflow-commands:continue <task-id>
    ↓
(continue working)
    ↓
git commit
    ↓
bd close <id>
```
