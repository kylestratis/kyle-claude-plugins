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

### Layer 2: Adversarial Hardening

**Goal:** Generate edge-case inputs targeting language-specific divergence points and cross-chunk interactions to find remaining behavioral differences.

#### Iteration Loop (Max 3 Iterations)

**Per iteration:**

##### Step 1: Generate Edge Cases

Dispatch `ed3d-basic-agents:opus-general-purpose` with this prompt:

```
You are an adversarial test case generator for ported code.

Your task: Generate edge-case inputs that stress the ported feature and expose language-specific divergences.

Input:
- Source path: <SOURCE_PATH>
- Target path: . (current working directory)
- Source language: <SOURCE_LANG>
- Target language: <TARGET_LANG>
- Iteration: <N>/3

Generation strategy:
1. **Language-Specific Divergence Points:**
   - Float precision (NaN, Infinity, denormal numbers, rounding)
   - String encoding (Unicode, surrogate pairs, null bytes, normalization)
   - Null/None semantics (null coalescing, optional chaining, pattern matching)
   - Integer overflow/underflow behavior
   - Error handling semantics (checked exceptions vs unchecked, panic vs throw)
   - Type coercion and implicit conversions

2. **Cross-Chunk Interactions:**
   - Data flowing through multiple ported functions
   - Accumulated state across function calls
   - Async behavior and race conditions (if applicable)
   - Shared resources or side effects
   - Circular dependencies or mutual recursion

3. **Boundary Conditions:**
   - Empty inputs, empty collections, zero values
   - Maximum/minimum valid inputs for data types
   - Off-by-one conditions in loops and ranges
   - Platform-specific limits (max recursion depth, max file size, etc.)

4. **Critical Chunks** (if --rigor critical was specified):
   - Generate property-based test specifications using framework-appropriate tools:
     - Python: hypothesis with property decorators
     - Rust: proptest with arbitrary implementations
     - JavaScript: fast-check with Arbitraries
     - Go: gopter with Properties
   - For each critical chunk, define invariants that should hold
   - Generate 100+ random test cases per property
   - Document property specifications in code comments

Output format:

**Test Case 1: <description>**
Input: <JSON or code representation>
Expected: <description of what should happen>
Rationale: <why this case targets a divergence point>

**Test Case 2: <description>**
Input: <...>
Expected: <...>
Rationale: <...>

...

**Property-Based Tests** (critical chunks only):
Property: <invariant-name>
Framework: <hypothesis|proptest|fast-check|gopter>
Specification:
<code showing property definition>

Property: <next-invariant>
...

---

CRITICAL INSTRUCTIONS:
- Generate 10-20 test cases per iteration, focusing on unexplored divergence points
- Each case should target a specific divergence dimension (float precision, string handling, error semantics, etc.)
- For cross-chunk interactions, compose multiple function calls that thread data through the ported feature
- If previous iteration found specific divergences, escalate to more aggressive variants
- For critical chunks, write explicit property specifications
- Run each test case through BOTH source and target (simulated in this prompt)
- Classify findings: GENUINE DIVERGENCE, ACCEPTABLE DIFFERENCE, FALSE POSITIVE
- Stop generating if 75% of recent cases are FALSE POSITIVES (exhaustion indicator)
```

##### Step 2: Run Generated Tests

For each generated test case:

1. Run against source implementation
2. Run against target implementation
3. Compare outputs

**Execution pattern (depends on language):**

```bash
# For same-language ports: run both in same test file
pytest test_adversarial_layer2.py -v

# For cross-language ports: run source, capture output, validate target
python generate_adversarial_vectors.py > adversarial_vectors.json
npm test -- validate_adversarial_vectors.js

# Run property-based tests (critical chunks)
pytest test_critical_properties.py -v --hypothesis-seed=<iteration-seed>
```

##### Step 3: Triage Findings

For each finding, classify as:

| Finding | Classification | Action |
|---------|----------------|--------|
| Output differs (unexpected) | GENUINE DIVERGENCE | Document, mark for fixing |
| Output differs (acceptable per design) | ACCEPTABLE DIFFERENCE | Document rationale, mark approved |
| Output identical or behavior equivalent | FALSE POSITIVE | Count toward exhaustion |

Build triage table per iteration:

```
## Iteration <N> Triaging Results

| Test Case | Source Output | Target Output | Classification | Rationale |
|-----------|---------------|---------------|-----------------|-----------|
| divergence_float_nan | NaN | NaN | FALSE POSITIVE | Both handle correctly |
| divergence_unicode_emoji | "👍" | "👍" | FALSE POSITIVE | Both encode correctly |
| divergence_null_coalesce | <value> | <value> | GENUINE DIVERGENCE | Error handling differs |
| ... | | | | |

Summary:
- Genuine Divergences: X
- Acceptable Differences: Y
- False Positives: Z (Z% of findings)
```

#### Exhaustion Logic

After each iteration:

```bash
# Calculate false positive percentage
fp_percent = (false_positives / total_findings) * 100

# Check termination conditions
if fp_percent > 75%; then
  echo "Exhaustion reached: >75% false positives"
  terminate_loop = true
elif iteration >= 3; then
  echo "Max iterations reached"
  terminate_loop = true
elif critical_chunks_flagged AND iteration < 2; then
  echo "Critical chunks: enforce minimum 2 iterations"
  terminate_loop = false
else
  proceed_to_next_iteration
fi

# Log outcome
deciduous add outcome "Adversarial Layer 2: Iteration <N> complete: <X> genuine, <Y> acceptable, <Z> false positives"
```

#### Final Adversarial Summary

After all iterations complete:

```
## Layer 2: Adversarial Hardening Complete

Total iterations: <N>/3
Termination reason: Exhaustion | Max iterations | Critical chunk minimum met

| Iteration | Genuine Divergences | Acceptable Differences | False Positives | Action |
|-----------|---------------------|------------------------|-----------------|--------|
| 1 | <X> | <Y> | <Z> | <action> |
| 2 | <X> | <Y> | <Z> | <action> |
| ... | | | | |

Total findings: <X> genuine, <Y> acceptable, <Z> false positives

Next steps:
1. Layer 1 verified behavioral equivalence via differential testing
2. Layer 2 identified specific divergence points
3. Known acceptable differences documented (see section below)
4. Proceeding to Layer 3: Standard Verify
```
