# Kyle's Claude Code Plugins

Personal plugin marketplace for Claude Code workflow extensions with beads/deciduous tracking integration, lightly and lovingly wrapping ed3d's coding plugins.
In desperate search of a name that doesn't suck.

## Table of Contents

- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Commands Reference](#commands-reference)
- [Workflow](#workflow)
- [Customization](#customization)
- [Structure](#structure)

---

## Installation

### 1. Register the marketplace

Claude Code:

```bash
/plugin marketplace add kylestratis/kyle-claude-plugins
```

OMP:

```bash
omp plugin marketplace add kylestratis/kyle-claude-plugins
```

Use a local path instead of the repository slug to install from a working tree:
`add /path/to/kyle-claude-plugins`. Installs then resolve from that checkout,
including uncommitted changes.

### 2. Install plugins

The tracking hooks need their scripts executable before installation:

```bash
chmod +x plugins/tracking-hooks/hooks/*.sh plugins/tracking-hooks/hooks/*.py
```

Claude Code:

```bash
# Workflow commands (required)
/plugin install workflow-commands@kyle-claude-plugins

# Tracking hooks (optional - session start reminders, git hooks)
/plugin install tracking-hooks@kyle-claude-plugins

# Documentation review (optional - prose review with controlled fixes)
/plugin install documentation-review@kyle-claude-plugins
```

OMP:

```bash
omp plugin install --scope user workflow-commands@kyle-claude-plugins
omp plugin install --scope user tracking-hooks@kyle-claude-plugins
omp plugin install --scope user documentation-review@kyle-claude-plugins
```

Use `--scope project` to install for one repository instead of your user account.

### 3. Load the plugins

Run `/reload-plugins` in either runtime, or start a new session.

### Updating

OMP upgrades in place. Claude Code pins each install to a commit, so reinstall
to pick up new commits:

```bash
# OMP
omp plugin upgrade documentation-review@kyle-claude-plugins

# Claude Code
/plugin marketplace update kyle-claude-plugins
/plugin uninstall documentation-review@kyle-claude-plugins
/plugin install documentation-review@kyle-claude-plugins
```

---

## Prerequisites

### Required Tools

#### 1. beads (Task Tracking)

Local task/issue tracking stored in `.beads/` directory.

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Verify
bd --version
```

**Key commands:**
```bash
bd init                          # Initialize in project
bd create "Task" -t task -p 3    # Create task (priority 0-4)
bd list                          # List all tasks
bd ready                         # Show unblocked tasks
bd update <id> --status done     # Update status
bd close <id> --reason "Done"    # Close task
```

#### 2. deciduous (Decision Journaling)

Decision graph stored in `.deciduous/` directory.

```bash
# Install
npm install -g deciduous

# Verify
deciduous --version
```

**Key commands:**
```bash
deciduous init                             # Initialize in project
deciduous add goal "What I'm doing" -c 80  # Confidence 0-100
deciduous add decision "Choice and why" -c 80
deciduous add action "What I did"
deciduous add outcome "What happened"
deciduous add action "Committed X" --commit HEAD  # Link to git
deciduous query                            # View graph
```

#### 3. ed3d-plugins (Core Workflow)

Design and implementation workflow framework.

```bash
# Register marketplace
/plugin marketplace add https://github.com/ed3dai/ed3d-plugins.git

# Install plugins
/plugin install ed3d-plan-and-execute@ed3d-plugins
/plugin install ed3d-research-agents@ed3d-plugins
/plugin install ed3d-basic-agents@ed3d-plugins
```

### Optional Tools

#### Linear Integration

If using `--linear` flag with `/workflow-commands:intake`:
- Must have Linear MCP connector enabled in Claude
- Requires access to at least one Linear team

#### GitHub Codex Review

The `/workflow-commands:fix-pr-review` command requires:

- GitHub CLI authenticated through `gh auth login`
- An open GitHub pull request
- Codex code review enabled for the repository

The workflow uses GitHub CLI authentication and never reads or prints token
values.

#### Pre-commit

For automatic verification hooks:
```bash
pip install pre-commit
pre-commit install  # In each project
```

---

## Commands Reference

### `/workflow-commands:project-init`

Initialize beads and deciduous tracking in a project.

```bash
/workflow-commands:project-init [--beads-only | --deciduous-only] [--with-guidance]
```

| Flag | Description |
|------|-------------|
| `--beads-only` | Only initialize beads, skip deciduous |
| `--deciduous-only` | Only initialize deciduous, skip beads |
| `--with-guidance` | Create `.ed3d/` directory with customization files |

**Creates:**
- `.beads/` - Task database
- `.deciduous/` - Decision graph
- `.ed3d/` - Guidance files (if `--with-guidance`)

---

### `/workflow-commands:intake`

Import features from a roadmap file or inline list.

```bash
# From markdown file
/workflow-commands:intake @docs/roadmap.md

# With Linear sync
/workflow-commands:intake @docs/roadmap.md --linear

# Inline features
/workflow-commands:intake "OAuth integration" "Rate limiting" "Audit logging"

# Inline with Linear and team
/workflow-commands:intake "Feature 1" "Feature 2" --linear --team Engineering
```

| Argument | Description |
|----------|-------------|
| `@file.md` | Path to markdown roadmap file |
| `"feature"` | Inline feature names (quoted) |
| `--linear` | Also create Linear issues |
| `--team <n>` | Linear team name (required if multiple teams) |

**Roadmap format:**
```markdown
## Q1 Features

### OAuth Integration
Support Google and GitHub providers.
Priority: High

### Rate Limiting  
Token bucket algorithm.
Priority: Normal
```

**Creates:**
- Beads epic per feature (with priority)
- Linear issue per feature (if `--linear`)
- Bidirectional links between beads and Linear

---

### `/workflow-commands:explore`

Research a topic with automatic tracking.

```bash
/workflow-commands:explore <topic> [--codebase-only | --web-only] [--no-tracking]
```

| Flag | Description |
|------|-------------|
| `--codebase-only` | Only search local codebase |
| `--web-only` | Only search web |
| `--no-tracking` | Skip beads task creation (deciduous still logs) |

**Examples:**
```bash
/workflow-commands:explore OAuth2 PKCE flow
/workflow-commands:explore authentication patterns --codebase-only
/workflow-commands:explore React 19 changes --web-only
```

**Tracking:**
- Creates deciduous goal at start
- Creates beads task (unless `--no-tracking`)
- Logs outcome on completion
- Closes beads task

---

### `/workflow-commands:design`

Start a design plan with decision logging. Wraps `ed3d-plan-and-execute:start-design-plan`.

```bash
/workflow-commands:design [feature description]
```

**Tracking:**
- Creates beads epic: "Design: \<feature\>"
- Logs deciduous goal
- **Logs every design decision during brainstorming**
- Updates beads on completion

**Decision logging examples:**
```bash
deciduous add decision "Chose PostgreSQL over MongoDB because: ACID compliance required, team expertise, JOIN performance" -c 85
deciduous add decision "Using event sourcing pattern because: audit trail required, temporal queries needed" -c 80
```

---

### `/workflow-commands:plan`

Create an implementation plan with task creation. Wraps `ed3d-plan-and-execute:start-implementation-plan`.

```bash
/workflow-commands:plan @path/to/design.md <workdir>
```

| Argument | Description |
|----------|-------------|
| `@design.md` | Path to design document |
| `workdir` | Working directory (usually `.`) |

**Example:**
```bash
/clear
/workflow-commands:plan @docs/design-plans/2026-02-10-oauth.md .
```

**Tracking:**
- Creates beads task per implementation phase
- Sets up task dependencies (sequential)
- Logs planning decisions to deciduous

---

### `/workflow-commands:execute`

Execute an implementation plan with status updates. Wraps `ed3d-plan-and-execute:execute-implementation-plan`.

```bash
/workflow-commands:execute <plan-dir> <workdir>
```

| Argument | Description |
|----------|-------------|
| `plan-dir` | Path to implementation plan directory |
| `workdir` | Working directory (usually `.`) |

**Example:**
```bash
/clear
/workflow-commands:execute docs/implementation-plans/2026-02-10-oauth/ .
```

**Tracking:**
- Updates beads task status per phase (in_progress → done)
- **Logs implementation decisions as they happen**
- Uses LEARNED pattern for discoveries

**Decision logging examples:**
```bash
deciduous add decision "Implemented retry with exponential backoff because upstream API is flaky" -c 80
deciduous add decision "Resolved circular dependency by extracting shared types to common module" -c 85
```

---

### `/workflow-commands:verify`

Final verification with intelligent tooling detection.

```bash
/workflow-commands:verify [--skip-tests] [--skip-lint] [--skip-precommit] [--skip-review] [--task <id>]
```

| Flag | Description |
|------|-------------|
| `--skip-tests` | Skip test execution |
| `--skip-lint` | Skip linting |
| `--skip-precommit` | Skip pre-commit hooks |
| `--skip-review` | Skip code review |
| `--task <id>` | Beads task ID to close on success |

**Automatic detection:**

| Language | Tests | Lint | Format |
|----------|-------|------|--------|
| Python | pytest, tox, nox, unittest | ruff, flake8, pylint | black, ruff format |
| JS/TS | npm test (jest, vitest, mocha) | eslint | prettier |
| Rust | cargo test | cargo clippy | cargo fmt |
| Go | go test | golangci-lint, go vet | gofmt |

**Also detects:**
- Pre-commit hooks (`.pre-commit-config.yaml`)
- Type checkers (mypy, tsc)
- Makefile targets
- Package.json scripts

**Behavior:**
1. Detects all project tooling
2. Runs tests, linters, formatters, pre-commit
3. Attempts auto-fix for formatting issues
4. Dispatches code review
5. Logs deciduous outcome
6. Closes beads task (if `--task` provided)

---
### `/workflow-commands:fix-pr-review`

Process Codex Review findings on an open GitHub pull request.

```bash
# Current branch's PR
/workflow-commands:fix-pr-review

# Explicit PR
/workflow-commands:fix-pr-review 123
/workflow-commands:fix-pr-review https://github.com/owner/repo/pull/123
```

The workflow waits for Codex Review, evaluates each finding against the current
code, fixes legitimate issues, and replies with technical evidence when a
finding is invalid. After fixes are pushed, it requests another Codex review
and repeats until the current PR head has no actionable findings.

`/verify` remains the pre-PR local verification workflow.
`/fix-pr-review` operates on asynchronous Codex findings posted through the
GitHub PR interface.

---

### `/workflow-commands:pollinate`

Port a feature from another codebase into the current project.

```bash
/workflow-commands:pollinate <source-path-or-url> <feature> [--rigor critical]
```

| Argument | Description |
|----------|-------------|
| `<source-path-or-url>` | Local path or URL of the source codebase |
| `<feature>` | Feature to port |
| `--rigor critical` | Raise verification rigor for high-risk ports |

Analyzes the source feature, maps it to this project's conventions, and generates
a design document. It does **not** write code directly — it feeds the standard
`/plan` → `/execute` → `/verify` pipeline.

**Examples:**
```bash
/workflow-commands:pollinate ../other-repo "retry middleware"
/workflow-commands:pollinate https://github.com/owner/repo "token refresh" --rigor critical
```

---

### `/workflow-commands:pollinate-verify`

Three-layer verification for ported code.

```bash
/workflow-commands:pollinate-verify [--task <beads-id>] [--source <path>]
```

| Argument | Description |
|----------|-------------|
| `--task` | Beads task to close on success |
| `--source` | Source codebase to compare against |

Runs after `/execute` completes a pollination port: differential tests against the
source, adversarial hardening, then standard project verification.

---


### `/workflow-commands:task`

Small standalone work that doesn't need design/planning phases.

```bash
/workflow-commands:task "<task description>" [--priority <0-4>]
```

| Argument | Description |
|----------|-------------|
| `"<description>"` | Task description (quoted) |
| `--priority` | 0=Critical, 1=High, 2=Medium, 3=Normal (default), 4=Backlog |

**Use when:** Work is clear, takes <1 hour, doesn't require architectural decisions.

**Examples:**
```bash
/workflow-commands:task "Add logging to auth middleware"
/workflow-commands:task "Update error message for invalid email" --priority 2
```

---

### `/workflow-commands:bug`

Fix a bug with investigation and root cause tracking.

```bash
/workflow-commands:bug "<bug description>" [--priority <0-4>] [--blocks <task-id>]
```

| Argument | Description |
|----------|-------------|
| `"<description>"` | Bug description (quoted) |
| `--priority` | 0=Critical, 1=High, 2=Medium (default), 3=Normal, 4=Backlog |
| `--blocks` | Link to task this bug is blocking |

**Workflow:**
1. Creates beads bug
2. Investigate → find root cause
3. Fix → verify
4. Close bug

**Examples:**
```bash
/workflow-commands:bug "Login button doesn't respond on mobile"
/workflow-commands:bug "Users can't checkout" --priority 1
/workflow-commands:bug "Auth crashes on empty token" --blocks beads-a1b2
```

---

### `/workflow-commands:continue`

Resume work on an existing beads task.

```bash
/workflow-commands:continue [<task-id>]
```

| Argument | Description |
|----------|-------------|
| `<task-id>` | Beads task ID (e.g., `beads-a1b2` or just `a1b2`) |

**If no task ID:** Shows available tasks (`bd ready`, `bd list --status=in_progress`).

**Examples:**
```bash
/workflow-commands:continue beads-a1b2  # Resume specific task
/workflow-commands:continue              # Show available tasks
```

---
### `/workflow-commands:orchestrate`

Coordinate independent open leaf Beads tickets in isolated worktrees.

```bash
/workflow-commands:orchestrate [<ticket-id> ...] [--max-parallel <count>]
```

| Argument | Description |
|----------|-------------|
| `<ticket-id>` | Restrict the candidate set to specific open leaf Beads tickets |
| `--max-parallel <count>` | Optional exact two-token positive worker limit; use it at most once; defaults to 4 and is capped at the runtime limit |

Without ticket IDs, the workflow starts from `bd ready`. Each invocation creates a new run and rejects in-progress, blocked, or stale-owned tickets; useful state stays on its exact branch and worktree for explicit manual recovery, while an interrupted empty claim requires administrative release. The task runtime owns its configured automatic provider fallback chain. The workflow creates its integration branch and all worker branches from one target revision, integrates worker commits serially, and verifies source content while excluding repository-declared tracker and generated decision-graph paths. It offers a local merge, a pull request, or keep-as-is; accepted worker work cannot be discarded. Ticket comments, closures, and outcomes become final only after a local reconciliation commit passes the tracker-path-only check and its push succeeds.

---

### `/documentation-review:review`

Review repository documentation, prompts, docstrings, and comments against
evidence-backed writing rules.

```bash
/documentation-review:review [--scope pr|repository] [--path <path> ...] \
                             [--profile <path>=<profile> ...] \
                             [--apply-approved <finding-id> ... | --autofix]
```

| Argument | Description |
|----------|-------------|
| `--scope` | `pr` (default) reviews prose changed from the verified PR base; `repository` reviews all eligible prose |
| `--path` | Repeated, repository-relative; narrows either scope. Cannot re-include excluded content |
| `--profile` | Repeated `<path>=<profile>`; overrides content classification |
| `--apply-approved` | Repeated `DR-###` IDs from the immediately preceding review in this conversation |
| `--autofix` | Applies all and only `safe` findings. Mutually exclusive with `--apply-approved` |

**Profiles:** `general`, `documentation`, `procedure`, `prompt`, `docstring`,
`comment`, `historical-record`.

**Fix safety classes:**

| Class | Behavior |
|-------|----------|
| `safe` | Applied by `--autofix` or when approved |
| `review-required` | Applied only when explicitly approved by ID |
| `report-only` | Never applied automatically, even when selected |

Default invocation modifies no files: it reports findings and creates a review
snapshot that `--apply-approved` consumes. Every edit re-reads its target and
requires byte-for-byte equality with the reviewed evidence, so a concurrently
changed target stops that edit alone and reports a recovery action. Protected
content — commands, identifiers, literals, URLs, quoted text, and necessary
provenance — is never rewritten.

**Examples:**
```bash
# Review prose changed in the current PR
/documentation-review:review

# Review the whole repository, narrowed to two paths
/documentation-review:review --scope repository --path README.md --path docs/

# Treat a file as a procedure regardless of content classification
/documentation-review:review --profile docs/deploy.md=procedure

# Apply two approved findings from the preceding review
/documentation-review:review --apply-approved DR-001 --apply-approved DR-004

# Apply only findings classified safe
/documentation-review:review --scope repository --autofix
```

---

## Entry Points

| Start From | When to Use | Creates |
|------------|-------------|---------|
| `/workflow-commands:design` | New feature needing architecture | Epic |
| `/workflow-commands:plan` | Have design doc, need tasks | Phase tasks |
| `/workflow-commands:task` | Small standalone work (<1hr) | Single task |
| `/workflow-commands:bug` | Fix a bug | Bug |
| `/workflow-commands:continue` | Resume existing work | Nothing (uses existing) |
| `/workflow-commands:orchestrate` | Run independent ready tickets concurrently | Nothing (uses existing) |
| `/workflow-commands:explore` | Research before design | Research task |
| `/workflow-commands:intake` | Import roadmap | Epics |
| `/workflow-commands:pollinate` | Port a feature from another codebase | Design document |
| `/documentation-review:review` | Review prose before commit or PR | Nothing (report + review snapshot) |

---

## Workflow

### Full Feature Workflow

```
/workflow-commands:project-init          # Once per project
    │
    ▼
/workflow-commands:intake @roadmap.md --linear   # Import features
    │
    │   ┌───────────────────────────────────────┐
    │   │  For each feature:                    │
    ▼   ▼                                       │
/workflow-commands:explore <topic>              │  ← deciduous: goal/outcome
    │                                           │    beads: research task
    ▼                                           │
/workflow-commands:design                       │  ← deciduous: ALL design decisions
    │                                           │    beads: design epic
    ▼                                           │
/clear                                          │
/workflow-commands:plan @design.md .            │  ← deciduous: planning decisions
    │                                           │    beads: phase tasks
    ▼                                           │
/clear                                          │
/workflow-commands:execute <plan-dir> .         │  ← deciduous: impl decisions
    │                                           │    beads: status updates
    ▼                                           │
/workflow-commands:verify --task <epic-id>      │  ← deciduous: outcome
    │                                           │    beads: close epic
    ▼                                           │
git commit / PR ────────────────────────────────┘
```

### Parallel Ticket Workflow

For existing ready tickets with disjoint ownership:

```bash
/workflow-commands:orchestrate beads-a1b2 beads-c3d4 --max-parallel 2
# isolated workers → serial integration → combined verification → publish → close
```

Dependent or overlapping open tickets can remain for a later wave. Failed or unverified useful state remains on its recorded branch and worktree for explicit manual recovery and is never adopted by a later orchestration run.

### Quick Task Workflow

For smaller tasks that don't need full design:

```bash
/workflow-commands:task "Add logging to auth middleware"
# ... work directly ...
/workflow-commands:verify
git commit -m "feat: add auth middleware logging"
```

### Bug Fix Workflow

```bash
/workflow-commands:bug "Users can't login on mobile"
# ... investigate root cause ...
# ... fix it ...
/workflow-commands:verify
git commit -m "fix: mobile login issue"
```

### Resume Work

```bash
/workflow-commands:continue beads-a1b2   # Resume specific task
# or
/workflow-commands:continue              # Show available tasks
```

---

## Customization

### Project-Specific Guidance

Run `/workflow-commands:project-init --with-guidance` to create:

```
.ed3d/
├── design-plan-guidance.md       # Customize design phase
└── implementation-plan-guidance.md  # Customize implementation
```

#### design-plan-guidance.md

```markdown
# Design Plan Guidance

## Domain Context
<!-- Describe your project's domain, terminology, key concepts -->

## Architectural Constraints
<!-- Decisions that designs must follow -->
- All services must be stateless
- Use PostgreSQL for persistence
- REST APIs only (no GraphQL)

## Technology Stack

### Required
- Python 3.11+
- FastAPI
- PostgreSQL

### Preferred
- Redis for caching
- Celery for async tasks

### Forbidden
- MongoDB (we standardized on PostgreSQL)
- Synchronous external API calls in request handlers

## Stakeholders
<!-- Who approves designs? -->

## Design Conventions
<!-- Project-specific patterns -->
```

#### implementation-plan-guidance.md

```markdown
# Implementation Plan Guidance

## Coding Standards
<!-- Reference style guide or key conventions -->
- Follow PEP 8
- Use type hints everywhere
- Docstrings for public functions

## Testing Requirements
- Minimum 80% coverage for new code
- Integration tests for API endpoints
- Unit tests for business logic

## Review Criteria
- Security review for auth changes
- Performance review for database changes

## Quality Gates
- All tests pass
- No new lint errors
- Type check passes (mypy)
- Pre-commit hooks pass

## Build & Deploy
- CI runs on push to main
- Deploy via GitHub Actions
```

### Verify Customization

The verify skill auto-detects tooling, but you can influence it by:

1. **Adding config files** - The skill looks for:
   - `pytest.ini`, `pyproject.toml` (pytest)
   - `ruff.toml`, `.ruff.toml` (ruff)
   - `.pre-commit-config.yaml` (pre-commit)
   - etc.

2. **Package.json scripts** - Define `test`, `lint` scripts:
   ```json
   {
     "scripts": {
       "test": "vitest run",
       "lint": "eslint . && prettier --check ."
     }
   }
   ```

3. **Makefile targets** - The skill checks for:
   ```makefile
   test:
       pytest -v
   
   lint:
       ruff check . && mypy .
   
   verify: test lint
       pre-commit run --all-files
   ```

### Decision Logging Guidelines

The workflow commands explicitly log decisions. For best results:

**Always include:**
- What was decided
- What alternatives were considered
- Why this choice was made
- Confidence level (50 = tentative, 90 = very confident, scale 0-100)

**Good example:**
```bash
deciduous add decision "Chose Redis for session storage because: 1) sub-ms latency required, 2) built-in TTL for session expiry, 3) team already has Redis expertise. Considered: PostgreSQL (too slow), Memcached (no persistence)." -c 85
```

**Bad example:**
```bash
deciduous add decision "Using Redis" -c 80
```

---

## Structure

```
kyle-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── workflow-commands/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/
│   │   │   ├── project-init.md
│   │   │   ├── intake.md
│   │   │   ├── explore.md
│   │   │   ├── design.md
│   │   │   ├── plan.md
│   │   │   ├── execute.md
│   │   │   ├── verify.md
│   │   │   ├── fix-pr-review.md
│   │   │   ├── task.md          # NEW
│   │   │   ├── bug.md           # NEW
│   │   │   ├── continue.md
│   │   │   └── orchestrate.md
│   │   └── skills/
│   │       ├── project-init/SKILL.md
│   │       ├── intake/SKILL.md
│   │       ├── exploring/SKILL.md
│   │       ├── designing/SKILL.md
│   │       ├── planning/SKILL.md
│   │       ├── executing/SKILL.md
│   │       ├── verifying/SKILL.md
│   │       ├── pr-review-loop/SKILL.md
│   │       ├── task/SKILL.md              # NEW
│   │       ├── bug/SKILL.md               # NEW
│   │       ├── continue/SKILL.md          # NEW
│   │       ├── orchestrating-beads-tickets/SKILL.md
│   │       └── beads-deciduous-integration/SKILL.md
│   └── tracking-hooks/
│       ├── .claude-plugin/plugin.json
│       └── hooks/
│           ├── hooks.json
│           ├── session-start-tracking.sh
│           └── git-beads-reminder.py
└── README.md
```

---

## License

MIT
