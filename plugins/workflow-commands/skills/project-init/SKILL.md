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
```

### Step 2: Initialize

```bash
# Beads (unless --deciduous-only)
bd init

# Deciduous (unless --beads-only)
deciduous init
```

### Step 3: Create Guidance (if --with-guidance)

Create `.ed3d/design-plan-guidance.md` and `.ed3d/implementation-plan-guidance.md`.

### Step 4: Report

```
## Initialized ✅
- beads: .beads/
- deciduous: .deciduous/

Next: /workflow-commands:intake or /workflow-commands:explore
```
