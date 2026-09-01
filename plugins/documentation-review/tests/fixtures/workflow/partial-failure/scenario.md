# Workflow Scenario: Partial Failure

## Acceptance criteria under test

- `documentation-review.AC6.3`: An independent successful edit remains after another edit fails.
- `documentation-review.AC6.4`: A stale target is not overwritten.
- `documentation-review.AC6.5`: Every incomplete edit has an exact reason and recovery action.

## Invocation arguments

```text
--scope repository --path docs/a.md --path docs/b.md --autofix
```

## Simulated tool-result transcript

```text
Applicable repository writing directive -> replace unquoted prose typo "teh" with "the".
Review snapshot:
DR-001 | docs/a.md:3 | evidence="Open teh dashboard." | suggested_action="Open the dashboard." | safe
DR-002 | docs/b.md:4 | evidence="Close teh dashboard." | suggested_action="Close the dashboard." | safe

Read docs/a.md:3 -> exact byte match
Edit docs/a.md:3 -> success: "Open the dashboard."
Second Read and review docs/a.md:3 -> current bytes match replacement; no remaining finding

Concurrent user edit before DR-002 verification:
Read docs/b.md:4 -> "Close teh production dashboard."
Byte comparison -> mismatch with DR-002 evidence
Edit docs/b.md -> no call
Final Read docs/a.md:3 -> "Open the dashboard."
```

## Required observable actions

- Select both safe findings.
- Verify and apply `DR-001`, then second-review its modified region.
- Verify `DR-002`, detect its stale bytes, and stop only that edit.
- Preserve the successful `DR-001` edit after `DR-002` fails.
- Preserve the concurrent `docs/b.md` text and mark the overall run incomplete.
- Report separate outcomes and a specific recovery action for `DR-002`.

## Forbidden actions

- Do not roll back `DR-001` because `DR-002` failed.
- Do not force, broaden, or relocate the `DR-002` patch.
- Do not remove `production` from the concurrent text.
- Do not label the run complete, all-applied, or clean.
- Do not omit the second review for `DR-001`.

## Expected report fields

- `status: Documentation Review Incomplete`
- `scope: repository`
- `mode: autofix`
- `proposed: DR-001, DR-002`
- `selected: DR-001, DR-002`
- `applied: DR-001`
- `failed: DR-002`
- `unresolved: DR-002 stale target`
- Second-review result for `docs/a.md:3`
- Exact current and reviewed evidence for `docs/b.md:4`
- Recovery action for `DR-002`

## Protected text and expected unchanged files

- Expected final `docs/a.md:3`: `Open the dashboard.`
- Protected concurrent `docs/b.md:4`: `Close teh production dashboard.`
- Expected unchanged files: all other files.
- The successful edit in `docs/a.md` is protected from rollback.

## Exact failure and recovery output

```text
Documentation Review Incomplete
DR-001 applied and passed second review at docs/a.md:3.
DR-002 failed: stale target at docs/b.md:4. Current evidence "Close teh production dashboard." differs from reviewed evidence "Close teh dashboard." No edit was attempted, and DR-001 remains applied.
Recovery: run a new review-only invocation for docs/b.md, inspect the new evidence, then run autofix again only if the new finding is safe.
```
