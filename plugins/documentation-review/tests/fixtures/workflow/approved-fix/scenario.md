# Workflow Scenario: Approved Fix

## Acceptance criteria under test

- `documentation-review.AC5.2`: Approved-fix mode applies only selected findings from the immediately preceding snapshot.
- `documentation-review.AC5.4`: Omitted review-required findings stay unchanged.
- `documentation-review.AC5.6`: Protected content stays unchanged.

## Invocation arguments

Immediately after the supplied snapshot:

```text
--apply-approved DR-001 --apply-approved DR-003
```

## Simulated tool-result transcript

```text
Immediately preceding current-conversation review snapshot:
Scope: repository; path: docs/guide.md
DR-001 | docs/guide.md:3 | WR-001 | major | documentation | evidence="Use the worker for queue jobs." | suggested_action="Use the consumer for queue jobs." | review-required
DR-002 | docs/guide.md:5 | WR-003 | major | documentation | evidence="Restart it after updating the worker." | suggested_action="Restart the consumer after updating the worker." | review-required
DR-003 | docs/guide.md:7 | WR-005 | major | documentation | evidence="See OPS-431 for the reason." | suggested_action="No automatic action possible; requires investigation and user judgment." | report-only
Reviewed evidence bytes and source policy are stored with each record.

Read docs/guide.md current regions -> every region exactly matches the snapshot evidence
Edit docs/guide.md:3 -> success; replacement exactly matches DR-001
Second Read docs/guide.md:3 -> "Use the consumer for queue jobs."
```

## Required observable actions

- Reuse only the immediately preceding snapshot and preserve its scope.
- Select `DR-001` and `DR-003`; do not implicitly select `DR-002`.
- Re-read each selected target and compare it byte-for-byte with snapshot evidence.
- Apply the selected `review-required` `DR-001` replacement.
- Reject selected `report-only` `DR-003` without changing it.
- Keep omitted `DR-002` unchanged.
- Perform and record a second review of the modified `DR-001` region.

## Forbidden actions

- Do not reconstruct findings, rerun discovery, widen scope, or renumber the snapshot.
- Do not apply `DR-002` because it is nearby or easy.
- Do not apply or invent a replacement for `DR-003`.
- Do not change `OPS-431`, `worker` occurrences outside DR-001, or unrelated bytes.

## Expected report fields

- `scope: repository` from the snapshot
- `mode: approved-fix`
- `selected: DR-001, DR-003`
- `applied: DR-001`
- `skipped: DR-002` with `not selected`
- `rejected/skipped: DR-003` with `report-only findings cannot be applied`
- Complete original finding records
- Second-review result for `docs/guide.md:3`
- Recovery entry for rejected `DR-003`

## Protected text and expected unchanged files

- Protected content: `Restart it after updating the worker.` and `See OPS-431 for the reason.`
- Protected provenance: `OPS-431`.
- Expected changed region: only `docs/guide.md:3` from `worker` to `consumer` as specified by DR-001.
- Expected unchanged files: every file except that exact region in `docs/guide.md`.

## Exact failure and recovery output

The report entry for selected report-only `DR-003` must be exact:

```text
DR-003 skipped: report-only findings cannot be applied, even when selected. Recovery: investigate OPS-431 and supply the missing durable rationale in a new review; do not invent or remove provenance.
```
