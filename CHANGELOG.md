# Changelog

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
