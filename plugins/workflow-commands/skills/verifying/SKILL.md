---
name: verifying
description: Final verification with intelligent tooling detection and tracking
user-invocable: false
---

# Verifying

## Overview

Detect project tooling, run tests/linters/pre-commit, dispatch code review, track outcomes.

**Announce:** "I'm verifying this implementation."

## Arguments

`[--skip-tests] [--skip-lint] [--skip-precommit] [--skip-review] [--task <id>]`

## Phase 1: Detect Tooling

**CRITICAL: Detect before running anything.**

### Python
```bash
# Tests
ls pytest.ini pyproject.toml 2>/dev/null  # pytest
ls tox.ini noxfile.py 2>/dev/null         # tox/nox

# Lint
ls ruff.toml .ruff.toml .flake8 2>/dev/null
grep -q "mypy" pyproject.toml 2>/dev/null

# Format
grep -q "black" pyproject.toml 2>/dev/null
```

### JavaScript/TypeScript
```bash
cat package.json | grep -E '"(test|lint)"'
ls .eslintrc* eslint.config.js tsconfig.json 2>/dev/null
```

### Rust
```bash
ls Cargo.toml  # cargo test, cargo clippy, cargo fmt
```

### Go
```bash
ls go.mod  # go test, go vet, gofmt
which golangci-lint
```

### Pre-commit
```bash
ls .pre-commit-config.yaml
```

## Phase 2: Run Checks

| Language | Tests | Lint | Format |
|----------|-------|------|--------|
| Python | `pytest -v` | `ruff check .` | `black --check .` |
| JS/TS | `npm test` | `npm run lint` | `prettier --check .` |
| Rust | `cargo test` | `cargo clippy` | `cargo fmt --check` |
| Go | `go test ./...` | `golangci-lint run` | `gofmt -l .` |

Also run:
- `mypy .` (if configured)
- `npx tsc --noEmit` (if tsconfig.json)
- `pre-commit run --all-files` (if configured)

## Phase 3: Auto-Fix

If checks fail, attempt auto-fix:
```bash
ruff format .      # or black .
prettier --write .
cargo fmt
gofmt -w .
```

Re-run failed checks after fix.

## Phase 4: Code Review

Dispatch `ed3d-plan-and-execute:code-reviewer`.

**Print full reviewer response.**

## Phase 5: Fix Issues

If review finds issues:
1. Create beads tasks
2. Dispatch `ed3d-plan-and-execute:task-bug-fixer`
3. Re-run checks + review
4. Max 3 cycles

## Phase 6: Complete

```bash
deciduous add outcome "Verified: <N> tests pass, lint clean, review approved"

# If --task provided
bd close <task-id> --reason "Verified and ready"
```

**Report:**
```
## Verification Complete ✅

| Check | Result |
|-------|--------|
| pytest | 47 passed |
| ruff | Clean |
| pre-commit | 8/8 passed |
| review | Approved |

Ready for `git commit` or PR.
```
