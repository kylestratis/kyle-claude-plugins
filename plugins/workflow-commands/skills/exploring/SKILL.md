---
name: exploring
description: Research a topic with automatic beads/deciduous tracking
user-invocable: false
---

# Exploring

## Overview

Research across codebase and web with integrated tracking.

**Announce:** "I'm researching this topic systematically."

## Arguments

`<topic> [--codebase-only | --web-only] [--no-tracking]`

## Process

### Step 1: Track

```bash
deciduous add goal "Exploring: <topic>" -c 80

# Unless --no-tracking
bd create "Research: <topic>" -t task -p 3
```

### Step 2: Research

Dispatch based on scope:
- Combined: `ed3d-research-agents:combined-researcher`
- Codebase: `ed3d-research-agents:codebase-investigator`
- Web: `ed3d-research-agents:internet-researcher`

**Print full agent response.**

### Step 3: Synthesize

```markdown
## Research Summary: <topic>

### Key Findings
### Codebase State
### External Context
### Open Questions
### Next Steps
```

### Step 4: Complete

```bash
deciduous add outcome "Explored <topic>: <summary>"
bd close <id> --reason "Research complete"
```

**Next:** "Ready to design? Run `/workflow-commands:design`"
