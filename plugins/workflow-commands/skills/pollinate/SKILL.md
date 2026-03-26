---
name: pollinate
description: Port a feature from another codebase with convention mapping and behavioral equivalence verification
user-invocable: false
---

# Pollinate

## Overview

Analyze a source feature, map it to target project conventions, and generate a design document for porting. Delegates implementation to the standard `/plan` → `/execute` pipeline, and verification to `/pollinate-verify`.

**Announce:** "I'm analyzing the source feature for cross-codebase porting."

## Arguments

`<source-path-or-url> <feature> [--rigor critical]`

- `<source>`: Local filesystem path or GitHub/git URL
- `<feature>`: Function name, module name, or natural language description
- `--rigor critical`: Flag specific chunks for elevated verification (property-based testing, extra adversarial iterations)

## Process

*To be implemented in subsequent phases.*
