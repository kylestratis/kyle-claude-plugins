---
name: pollinate-verify
description: Three-layer verification for ported code - differential testing, adversarial hardening, and standard verify
user-invocable: false
---

# Pollinate Verify

## Overview

Extended verification for code ported via `/pollinate`. Wraps the standard `/verify` skill with two additional layers: differential testing (behavioral equivalence) and adversarial hardening (edge-case hunting).

**Announce:** "I'm running pollinate verification — differential tests, adversarial hardening, then standard verify."

## Arguments

`[--task <beads-id>] [--source <path>]`

- `--task`: Beads task ID for tracking
- `--source`: Path to source codebase for differential testing

## Process

*To be implemented in Phase 6.*
