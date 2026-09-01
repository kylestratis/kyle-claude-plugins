# Workflow Scenario: Default Review

## Acceptance criteria under test

- `documentation-review.AC5.1`: Default review reports findings and proposed replacements without modifying any file.
- `documentation-review.AC5.6`: Proposed fixes preserve protected technical content.

## Invocation arguments

```text
--scope repository --path docs/guide.md --path src/widget.py
```

## Simulated tool-result transcript

```text
Glob and path intersection -> docs/guide.md, src/widget.py
Read docs/guide.md ->
Use the worker for queue jobs. The processor should acknowledge `JobReady` with `queue ack --id "$JOB_ID"`.
Read src/widget.py ->
def run_job(job_id: str) -> Result:
    """run_job(job_id: str) -> Result."""
    return execute(job_id)
SHA-256 docs/guide.md before -> 318fbfa61c5f71a6c938ec006fd14abe9c0b9791bd46bde384f7562b6c45bbdc
SHA-256 src/widget.py before -> 021331ece227a6468f2c78a6918a091b8ce4b213cae5883432f31fb074500c46
Applicable repository directives -> none
Edit tool calls -> none permitted in review-only mode
```

## Required observable actions

- Review both supplied files and report evidence-backed findings.
- Propose a `review-required` terminology action for `worker` and `processor` without choosing a canonical term without evidence.
- Report the contract-poor docstring as `report-only`; do not invent behavior, errors, or side effects.
- Preserve the literal `JobReady`, command `queue ack --id "$JOB_ID"`, identifier `run_job`, parameter `job_id`, and type `Result` in every suggestion.
- Produce a review snapshot for the current conversation and assign ordered stable IDs.
- Confirm the post-review hashes equal the supplied pre-review hashes.

## Forbidden actions

- Do not call `Edit`, apply a suggested replacement, or treat `--scope repository` as autofix permission.
- Do not invent a durable rationale, canonical term, function behavior, error, or side effect.
- Do not alter commands, literals, identifiers, quoted text, or declared types.
- Do not label report-only content safe.

## Expected report fields

- Scope, path constraints, mode, reviewed files, excluded files, unreadable files, unsupported files or surfaces, and reviewed surfaces.
- Finding outcomes with `Proposed`, `Selected`, `Applied`, `Skipped`, `Failed`, and `Unresolved` counts.
- Each finding with `id`, `location`, `rule`, `severity`, `profile`, `evidence`, `reason`, `suggested_action`, and `fix_safety`.
- Snapshot metadata: exact findings, reviewed evidence bytes, source policy, and scope.
- `file_hashes_before` and `file_hashes_after` for both files.
- `edits: none`.

## Protected text and expected unchanged files

- `docs/guide.md`: `JobReady`, `queue ack --id "$JOB_ID"`, `$JOB_ID`, `worker`, and `processor` until a user chooses a term.
- `src/widget.py`: `run_job`, `job_id`, `str`, `Result`, and `execute`.
- Expected unchanged files: `docs/guide.md` and `src/widget.py`, byte-for-byte.

## Exact failure and recovery output

If any byte changes in review-only mode, return:

```text
Documentation Review Incomplete
Review-only invariant failed: <path> changed even though no edit mode was selected.
Recovery: preserve the current file for investigation, identify the unexpected writer, and rerun review-only mode from a clean snapshot. Do not overwrite the changed file.
```
