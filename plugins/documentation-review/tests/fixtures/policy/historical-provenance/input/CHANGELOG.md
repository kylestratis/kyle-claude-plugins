# Changelog

All notable changes to this project are documented in this file.

## [2.1.0] - 2026-08-31

**Released by:** alice@example.com

### Added

- Support for distributed task scheduling (resolves #487)
- New API endpoint for querying execution status
- Configuration option to customize worker timeout

### Fixed

- Worker crash when processing malformed task definitions (refs #502)
- Scheduler inconsistency under high concurrency (see incident report IR-2026-08-28)

### Changed

- Improved error messaging for connection failures
- Updated bundled Python runtime to 3.11.2

---

## [2.0.5] - 2026-07-15

**Released by:** bob@example.com

### Fixed

- Memory leak in long-running scheduler (ticket #445, verified by QA on 2026-07-14)
- Race condition in worker assignment logic

### Security

- Patched authentication bypass (CVE-2026-3847)

---

## [1.9.2] - 2026-03-10

**Released by:** charlie@example.com

**Deprecated:** Support for Python 3.8 ends in version 3.0.0.

### Added

- Compatibility with Kubernetes 1.28

The original implementation is documented in ADR-0015 (decision made 2025-11-12, superseded by ADR-0021 on 2026-01-20).
