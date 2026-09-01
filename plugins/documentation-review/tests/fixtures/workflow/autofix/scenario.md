# Workflow Scenario: Autofix

## Acceptance criteria under test

- `documentation-review.AC5.3`: Autofix applies all and only safe findings.
- `documentation-review.AC5.4`: Review-required and report-only findings remain unchanged.
- `documentation-review.AC5.6`: Protected technical text remains unchanged.

## Invocation arguments

```text
--scope repository --path docs/guide.md --autofix
```

## Simulated tool-result transcript

```text
Applicable repository writing directive -> Unquoted prose typo "teh" must be replaced with "the".
Review snapshot:
DR-001 | docs/guide.md:3 | WR-011 | minor | documentation | evidence="Open teh dashboard at `https://status.example.test/app`." | suggested_action="Open the dashboard at `https://status.example.test/app`." | safe | exact policy-supplied replacement
DR-002 | docs/guide.md:5 | WR-001 | major | documentation | evidence="The worker and processor use one queue." | suggested_action="Choose one canonical term." | review-required
DR-003 | docs/guide.md:7 | WR-005 | major | documentation | evidence="The limit exists because of OPS-431." | suggested_action="No automatic action possible; requires investigation and user judgment." | report-only
Read current regions -> all evidence matches byte-for-byte
Edit DR-001 region -> success
Second Read DR-001 region -> "Open the dashboard at `https://status.example.test/app`."
```

## Required observable actions

- Select exactly `DR-001` because it alone is `safe` and policy-supplied.
- Re-read and byte-compare the selected region before editing.
- Apply `teh` to `the` without changing the URL or formatting.
- Keep `DR-002` and `DR-003` unchanged and report why each was not selected.
- Perform a second review of the modified region and confirm no protected span changed.

## Forbidden actions

- Do not treat autofix as permission to apply reasonable or report-only suggestions.
- Do not choose between `worker` and `processor`.
- Do not invent a rationale for `OPS-431` or remove the ticket.
- Do not modify `https://status.example.test/app`, code formatting, identifiers, commands, literals, quotes, or provenance.
- Do not expand the edit beyond the exact typo.

## Expected report fields

- `scope: repository`
- `mode: autofix`
- `selected: DR-001`
- `applied: DR-001`
- `skipped: DR-002, DR-003` with their safety classes
- Complete finding records and controlling policies
- Protected-span comparison for the URL and ticket
- Second-review result for `docs/guide.md:3`
- Finding outcome counts for proposed, selected, applied, skipped, failed, and unresolved

## Protected text and expected unchanged files

- Protected URL: `https://status.example.test/app`.
- Protected terminology: `worker` and `processor` until user review.
- Protected provenance: `OPS-431`.
- Expected changed bytes: only `teh` to `the` at `docs/guide.md:3`.
- Expected unchanged files: every file other than that exact region.

## Exact failure and recovery output

If the URL or any non-safe region changes, return:

```text
Documentation Review Incomplete
Autofix safety invariant failed: protected or non-safe content changed at <location>.
Recovery: do not overwrite the current file. Inspect the unexpected edit, restore it only with user authorization, and rerun the review to create a new snapshot.
```
