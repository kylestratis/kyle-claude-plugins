# Changelog

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
