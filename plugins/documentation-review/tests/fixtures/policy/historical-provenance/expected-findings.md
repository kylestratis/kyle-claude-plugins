# Expected Findings: Historical Provenance

## Expected findings

No findings expected

## Protected text

WR-012 (Protected provenance) preserves each exact source span below:

- `CHANGELOG.md:version_2.1.0`: `[2.1.0]`
- `CHANGELOG.md:date_2.1.0`: `2026-08-31`
- `CHANGELOG.md:author_2.1.0`: `alice@example.com`
- `CHANGELOG.md:ticket_487`: `#487`
- `CHANGELOG.md:ticket_502`: `#502`
- `CHANGELOG.md:incident_report`: `IR-2026-08-28`
- `CHANGELOG.md:runtime_version`: `3.11.2`
- `CHANGELOG.md:version_2.0.5`: `[2.0.5]`
- `CHANGELOG.md:date_2.0.5`: `2026-07-15`
- `CHANGELOG.md:author_2.0.5`: `bob@example.com`
- `CHANGELOG.md:ticket_445`: `#445`
- `CHANGELOG.md:qa_date`: `2026-07-14`
- `CHANGELOG.md:cve`: `CVE-2026-3847`
- `CHANGELOG.md:version_1.9.2`: `[1.9.2]`
- `CHANGELOG.md:date_1.9.2`: `2026-03-10`
- `CHANGELOG.md:author_1.9.2`: `charlie@example.com`
- `CHANGELOG.md:deprecated_runtime`: `Python 3.8`
- `CHANGELOG.md:deprecation_version`: `3.0.0`
- `CHANGELOG.md:kubernetes_version`: `Kubernetes 1.28`
- `CHANGELOG.md:adr_0015`: `ADR-0015`
- `CHANGELOG.md:adr_0015_date`: `2025-11-12`
- `CHANGELOG.md:adr_0021`: `ADR-0021`
- `CHANGELOG.md:adr_0021_date`: `2026-01-20`

## Expected zero-finding regions

- `CHANGELOG.md:1-52`: The historical-record profile and WR-012 protect the necessary dates, versions, tickets, authorship, security advisory, deprecation record, platform version, and decision provenance throughout this record.
