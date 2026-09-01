# Changelog

## [1.2.0] - 2026-08-30

**Released by:** maintenance@example.com

### Added

- Support for conditional branching in workflows (PR #521, reviewed on 2026-08-28)
- New parallel execution mode for independent steps
- Configuration validation before workflow execution

### Fixed

- Workflow timeout not respected in edge cases (ticket #456)
- Race condition in step status updates

### Changed

- Updated internal task representation per ADR-0042 (decided 2026-08-15)

---

## [1.1.5] - 2026-07-20

**Released by:** dev@example.com

### Added

- Improved error messages
- Support for custom step handlers

### Fixed

- Memory leak in step execution loop
