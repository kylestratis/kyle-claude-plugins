---
name: project-init
description: Initialize beads and deciduous tracking in a project
user-invocable: false
---

# Project Init

## Overview

Initialize beads (task tracking) and deciduous (decision journaling) in a project.

**Announce:** "I'm initializing project tracking."

## Arguments

`[--beads-only | --deciduous-only] [--with-guidance]`

## Process

### Step 1: Check Current State

```bash
ls .beads/beads.db 2>/dev/null && echo "beads: exists"
ls .deciduous/ 2>/dev/null && echo "deciduous: exists"
ls CLAUDE.md 2>/dev/null && echo "CLAUDE.md: exists"
```

### Step 2: Initialize Beads (unless --deciduous-only)

```bash
bd init
```

### Step 3: Initialize Deciduous (unless --beads-only)

```bash
deciduous init --claude
```

This creates:
- `.deciduous/` directory with config and database
- `.claude/commands/deciduous.decision.md` and `deciduous.recover.md`
- `.claude/skills/deciduous/SKILL.md`
- `.gitignore` entry for `.deciduous/` (database excluded from git)
- `CLAUDE.md` with decision graph workflow instructions
- GitHub Pages deployment files in `docs/` and `.github/workflows/`

**If CLAUDE.md already exists:** `deciduous init --claude` will not overwrite it. You must manually merge the deciduous instructions:

1. Run `deciduous init --claude` in a temp directory to get the generated CLAUDE.md
2. Read the generated content (the "Decision Graph Workflow" section)
3. Append it to the existing CLAUDE.md under a `## Decision Graph Workflow` heading
4. Ensure the project's `.gitignore` includes `.deciduous/deciduous.db`

**If CLAUDE.md does not exist:** `deciduous init --claude` creates it automatically. No extra steps needed.

### Step 4: Verify .gitignore

Ensure `.deciduous/deciduous.db` (or `.deciduous/`) is in `.gitignore`. The database is local state and must not be committed.

```bash
grep -q 'deciduous' .gitignore 2>/dev/null || echo '.deciduous/deciduous.db' >> .gitignore
```

### Step 5: Create Guidance (if --with-guidance)

Create `.ed3d/design-plan-guidance.md` and `.ed3d/implementation-plan-guidance.md`.

### Step 6: Report

```
## Initialized
- beads: .beads/
- deciduous: .deciduous/
- CLAUDE.md: updated with deciduous skills

Next: /workflow-commands:intake or /workflow-commands:explore
```
