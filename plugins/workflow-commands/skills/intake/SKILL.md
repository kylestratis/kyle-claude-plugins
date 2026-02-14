---
name: intake
description: Import features from roadmap into beads (and optionally Linear)
user-invocable: false
---

# Intake

## Overview

Parse features from markdown or inline list, create beads epics, optionally sync to Linear.

**Announce:** "I'm importing features into beads."

## Arguments

`<@file.md | "feature1" "feature2" ...> [--linear] [--team <n>]`

## Process

### Step 1: Verify Beads

```bash
ls .beads/beads.db || echo "Run /workflow-commands:project-init first"
```

### Step 2: Log Goal

```bash
deciduous add goal "Intake features" -c 90
```

### Step 3: Parse Features

Look for headings, checkboxes, or tables. Map priorities:
- Critical/Urgent → 1
- High → 2
- Normal → 3
- Low → 4

### Step 4: Create Beads Epics

```bash
bd create "<feature>" -t epic -p <priority>
```

### Step 5: Create Linear Issues (if --linear)

Use `Linear:create_issue`, then link:
```bash
bd comment <id> "Linear: <url>"
```

### Step 6: Report & Log

```bash
deciduous add outcome "Imported N features"
```

Next: `/workflow-commands:explore` or `/workflow-commands:design`
