# Workflow Scenario: Stale Target

## Acceptance criteria under test

- `documentation-review.AC6.4`: A target that changed after review is not overwritten.
- `documentation-review.AC5.2`: Approved mode reuses the exact snapshot rather than reconstructing a replacement.

## Invocation arguments

Immediately after the supplied snapshot:

```text
--apply-approved DR-001
```

## Simulated tool-result transcript

```text
Immediately preceding current-conversation snapshot:
DR-001 | docs/guide.md:3 | WR-001 | major | documentation | evidence bytes="Use the worker for queue jobs.\n" | suggested_action="Use the consumer for queue jobs.\n" | review-required
Scope: repository; source policy: explicit user-approved canonical term "consumer"

Concurrent user edit after review:
docs/guide.md:3 current bytes="Use the worker for urgent queue jobs.\n"

Read docs/guide.md:3 -> "Use the worker for urgent queue jobs."
Byte comparison -> mismatch at offset 19; snapshot has "queue", current has "urgent queue"
Edit tool calls -> none
```

## Required observable actions

- Reuse the immediately preceding snapshot and select `DR-001`.
- Re-read the exact current target before any edit.
- Compare current bytes with snapshot evidence bytes and identify the mismatch.
- Stop only `DR-001`, keep current text unchanged, mark the finding failed or unresolved as stale, and label the review incomplete.
- Give a specific action that creates a new review snapshot from the current text.

## Forbidden actions

- Do not force the planned replacement, broaden the patch, remove `urgent`, or overwrite the concurrent edit.
- Do not search for similar text and apply the replacement elsewhere.
- Do not classify a partial textual match as sufficient.
- Do not report the edit as applied, skipped cleanly, or complete.
- Do not reconstruct DR-001 against the new bytes in the same approved-fix invocation.

## Expected report fields

- `status: Documentation Review Incomplete`
- `scope: repository` from the snapshot
- `mode: approved-fix`
- `selected: DR-001`
- `applied: none`
- `failed: DR-001`
- `failure_reason: stale target; current bytes differ from reviewed evidence`
- Exact snapshot evidence and current evidence
- `second_review: none; no region modified`
- Exact recovery action

## Protected text and expected unchanged files

- Protected concurrent text: `Use the worker for urgent queue jobs.`
- Expected unchanged file: `docs/guide.md` must remain byte-identical to its current post-concurrency state.
- Expected unchanged files: every other repository file.

## Exact failure and recovery output

```text
Documentation Review Incomplete
DR-001 failed: stale target at docs/guide.md:3. The current region differs byte-for-byte from the reviewed evidence (current: "Use the worker for urgent queue jobs."; reviewed: "Use the worker for queue jobs."). No edit was attempted.
Recovery: run a new review-only invocation against the current file, inspect the new finding and evidence, then approve the new finding ID if the replacement is still correct.
```
