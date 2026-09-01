# Changelog

## workflow-commands 0.8.0

Coordinate independent Beads tickets with isolated workers, serial integration, and combined verification.

**New:**
- Added `/workflow-commands:orchestrate` and the `orchestrating-beads-tickets` skill
- Selects ready tickets with non-overlapping write sets, gives each active ticket one worktree, and preserves hard dependency order
- Delegates provider infrastructure fallback exclusively to the task runtime's configured automatic chain and handles only the settled task result
- Verifies the combined revision before publishing changes or closing represented tickets

**Fixed:**
- Starts each orchestration with a new run ID, rejects earlier ownership, preserves useful state for explicit manual recovery, and reports the administrative release procedure for stale empty claims
- Creates the integration branch and every worker branch from one recorded target revision
- Defines release and manual recovery state for every post-claim exit
- Accepts one exact `--max-parallel <positive-integer>` option before tracker mutation
- Removes coordinator-selected provider routes, explicit overrides, attempted-provider sets, and one-try promises
- Binds verification to source content excluding repository-declared tracker and generated decision-graph paths
- Presents local merge, pull request, and keep-as-is directly; accepted worker work cannot be discarded
- Makes tracker comments, closures, and outcomes final only after the exact tracker-only reconciliation commit passes its path check and reaches the target branch
- Accepts Linear issue identifiers and URLs, resolving each to an existing linked Beads ticket or creating one before any claim, and mirrors claim and final reconciliation back to Linear as reporting only

## workflow-commands 0.7.0

Add automated remediation for GitHub Codex Review findings.

**New:**
- Added `/fix-pr-review` and the `pr-review-loop` skill for automatic and on-demand processing of Codex findings on open pull requests
- The loop evaluates each finding against the current code, fixes legitimate issues, and replies with evidence when a finding is invalid
- Fix cycles push changes, explicitly request fresh Codex review, and stop only when the current PR head has no actionable findings
- The execution workflow now enters the PR review loop after creating a GitHub pull request

## tracking-hooks 0.3.1

Fix bd 1.0 CLI breakage in tracking hooks.

**Fixed:**
- Detection now checks the `.beads/` directory instead of the removed `.beads/beads.db` SQLite file (was causing false "tracking not initialized" warnings on every workflow skill under the embedded Dolt backend). Affects: workflow-tracking-check.py, session-start-tracking.sh, pre-commit-sync.sh, git-beads-reminder.py
- `pre-commit-sync.sh` uses `bd export` instead of the removed `bd sync --flush-only`
- Reconciled marketplace.json version (was stale at 0.1.0) with plugin.json (0.3.0 → 0.3.1)

## workflow-commands 0.6.1

Migrate workflow skills to the bd 1.0 CLI.

**Fixed:**
- Tracking detection now checks the `.beads/` directory instead of the removed `.beads/beads.db` SQLite file (bd 1.0 uses an embedded Dolt backend)
- Task completion uses `bd close` instead of `bd update --status done` (the `done` status was removed; valid statuses: open/in_progress/blocked/deferred/closed)
- Replaced the nonexistent `deciduous query` with `deciduous nodes`
- Affects skills: project-init, intake, designing, executing, bug, task, continue, beads-deciduous-integration, pollinate, pollinate-verify

## workflow-commands 0.6.0

Cross-codebase feature porting via `/pollinate` and `/pollinate-verify`.

**New:**
- Added `/pollinate` command and skill for analyzing source features, mapping conventions to target project, and generating design documents that feed into the standard `/plan` -> `/execute` pipeline
- Added `/pollinate-verify` command and skill with three-layer verification: differential testing, adversarial hardening (via Opus agent), and standard verify
- Added differential testing framework appendix with same-language, cross-language (test vector), and acceptable difference documentation patterns
- Added graceful degradation when beads/deciduous tracking tools are unavailable
- Added LEARNED comments and convention mapping rationale for reusable knowledge capture

## workflow-commands 0.5.0

Full workflow support from small tasks to large features.

**New:**
- Added `task`, `bug`, `continue` commands
- Expanded workflow coverage for small tasks and bug fixes

## workflow-commands 0.4.0

Initial tracked release with core workflow commands.

**New:**
- `project-init`, `intake`, `explore`, `design`, `plan`, `execute`, `verify` commands
- Beads/deciduous tracking integration
- Linear integration for issue import
- Intelligent test/lint detection (pytest, ruff)
