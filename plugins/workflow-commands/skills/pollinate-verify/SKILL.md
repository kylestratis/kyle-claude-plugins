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

### Before Starting

```bash
# Verify tracking infrastructure
ls .beads/beads.db .deciduous/ || echo "Run /workflow-commands:project-init first"

# Create deciduous goal
deciduous add goal "Verify ported feature via three-layer verification" -c 85

# Update beads task (if --task provided)
if [ -n "$TASK_ID" ]; then
  bd update "$TASK_ID" --status in-progress
fi
```

### Layer 1: Differential Testing

**CRITICAL: Detect test framework before running anything.**

#### Step 1: Detect Test Framework

Apply the same framework detection logic as the `verifying` skill:

**Python:**
```bash
ls pytest.ini pyproject.toml 2>/dev/null  # pytest
ls tox.ini noxfile.py 2>/dev/null         # tox/nox
```

**JavaScript/TypeScript:**
```bash
cat package.json | grep -E '"(test|lint)"'
ls .eslintrc* eslint.config.js tsconfig.json 2>/dev/null
```

**Rust:**
```bash
ls Cargo.toml  # cargo test
```

**Go:**
```bash
ls go.mod  # go test
```

#### Step 2: Run Differential Tests

Locate and run differential tests only (test files/directories matching "differential"):

```bash
# Python
pytest tests/differential_*.py -v --tb=short

# JavaScript/TypeScript
npm test -- --testPathPattern=differential

# Rust
cargo test --test differential_ -- --nocapture

# Go
go test -v ./.../*differential*
```

#### Step 3: Report Results

Capture test output and build a structured results table:

```
| Test Name | Source Output | Target Output | Status |
|-----------|---------------|---------------|--------|
| differential_test_1 | <src-output> | <tgt-output> | PASS/FAIL |
| differential_test_2 | <src-output> | <tgt-output> | PASS/FAIL |
| ... | | | |
```

#### Step 4: Stop Gate

**If any differential test FAILS:**
```
Report failures and STOP. Do not proceed to Layer 2.

Failures found:
- <test-name>: <reason>
- ...

Actions:
1. Review differential test logic
2. Check source vs target output alignment
3. Fix mismatches or document as acceptable differences
4. Re-run differential tests until all pass
5. Then proceed to Layer 2
```

**If all differential tests PASS:**
```
Differential testing complete: X/X tests pass.
Proceeding to Layer 2: Adversarial Hardening.
```
