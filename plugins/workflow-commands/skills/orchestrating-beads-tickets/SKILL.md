---
name: orchestrating-beads-tickets
description: Use when coordinating two or more independent ready Beads tickets in parallel - isolates workers, preserves dependency order, handles provider failures, integrates serially, and verifies the combined result before closing tickets
user-invocable: false
---

# Orchestrating Beads Tickets

## Overview

Run independent tickets concurrently, then integrate their work serially. The coordinator owns selection, isolation, provider routing, fan-in, verification, and tracker reconciliation. Each worker owns one ticket.

**Announce:** "I'm orchestrating independent Beads tickets in isolated worktrees."

## Arguments

`[<ticket-id> ...] [--max-parallel <count>]`

- With ticket IDs, evaluate only those tickets.
- Without ticket IDs, start from `bd ready --json`.
- `--max-parallel` defaults to 4 and limits a wave; it is not a target to fill.

## When to Use

Use this workflow when at least two ready tickets have:

- no blocking dependency between them;
- disjoint write ownership;
- acceptance criteria that can be verified on one integrated revision; and
- enough implementation work to justify worktree and integration overhead.

Run one ticket directly when work is small, ownership is uncertain, or the tickets modify the same behavior. Parallel waiting is not useful concurrency.

## Invariants

1. Each active ticket has exactly one worker, branch, and worktree.
2. A wave contains only ready tickets whose write sets do not overlap.
3. Workers never edit the coordinator's or another worker's worktree.
4. Workers never close tickets or mutate the integration branch.
5. Integration is serial, even when implementation is parallel.
6. Worker reports and clean cherry-picks are evidence, not verification.
7. Tickets close only after the integrated revision passes its required checks and is published through the repository's normal completion path.

Deadline, sunk-cost, or authority pressure does not weaken these invariants. Reduce the wave or ship a verified subset instead.

## Workflow

### 1. Establish the integration baseline

1. Read the repository's tracking and completion directives.
2. Invoke `beads-deciduous-integration` for canonical tracker semantics.
3. Record the current target branch and preserve unrelated changes.
4. Refresh the target branch before creating worker branches.
5. Read provider routing without exposing credentials. In OMP, inspect `retry.modelFallback` and `retry.fallbackChains`.

If the current worktree contains unrelated changes, keep integration in a separate worktree.

### 2. Build one runnable wave

For each candidate:

1. Run `bd show <ticket-id> --json`.
2. Require an open or in-progress ticket with no unresolved hard blocker.
3. Read its description, acceptance criteria, dependencies, comments, and referenced code.
4. Determine the smallest credible write set and verification surface.

Classify every pair:

| Relationship | Action |
|---|---|
| Hard dependency | Run in separate waves, blocker first |
| Overlapping file, symbol, schema, migration, or observable workflow | Serialize unless the write sets can be partitioned before dispatch |
| Unknown write set | Investigate before dispatch; serialize if it remains unknown |
| Non-overlapping write sets and no dependency | Eligible for the same wave |

Do not dispatch inspection-only workers or invent work to fill `--max-parallel`.

### 3. Fix the contracts before fan-out

Define in the task batch's shared context:

- target branch and integration owner;
- ticket-to-worktree mapping;
- exclusive file or subsystem ownership;
- shared interfaces, schemas, and assumptions;
- forbidden cross-ticket edits;
- commit and result format; and
- the rule that workers skip project-wide tests, linters, formatters, builds, and tracker mutation.

Create one branch and worktree per ticket with `using-git-worktrees`. Name branches and worktrees from stable ticket IDs.

Dispatch the complete wave in one parallel task batch. Each assignment must contain:

```text
# Target
Ticket ID, worktree, owned files or subsystem, and explicit non-goals.

# Change
Required behavior, acceptance criteria, existing patterns to reuse, and commit requirement.

# Acceptance
Observable result, changed paths, commit SHA, and any unresolved risk. Skip validation; the coordinator validates after fan-in.
```

A worker implements and commits its ticket directly. It does not dispatch subagents.

### 4. Handle worker and provider failures

A provider error before the worker reads or edits the ticket is infrastructure failure, not ticket failure.

1. Keep the ticket open.
2. Retry the same assignment through a configured alternate provider.
3. Prefer existing fallback chains. If an explicit override is required, use the narrowest task or session scope and restore the prior route after the batch.
4. Never read, print, or place provider credentials in prompts, logs, URLs, or command arguments.

If no alternate provider is configured, mark the ticket blocked with the exact infrastructure reason and continue independent successful tickets. Never describe the full batch as complete.

For implementation failures, preserve useful work, record the failure on that ticket, and let independent siblings finish. Do not discard successful sibling commits because one worker failed.

### 5. Verify worker deliveries

For each successful worker, independently confirm:

- the reported commit exists on the assigned branch;
- the diff contains only owned changes;
- the worktree has no uncommitted implementation;
- no tracker, integration-branch, or unrelated files changed; and
- the implementation addresses the ticket's acceptance criteria.

Reject or repair a delivery that violates ownership before integration. Agent self-reports are not sufficient.

### 6. Integrate serially

Use one integration owner and one integration branch.

1. Refresh the target branch again. Preserve another contributor's newer commits.
2. Apply worker commits one at a time in dependency and semantic order.
3. Inspect the complete integrated diff after every commit.
4. Resolve conflicts in the integration worktree. Treat a conflict or semantic collision as evidence of hidden coupling. Continue serial fan-in if the integration owner can satisfy both accepted contracts. Defer a ticket to a later wave only when it requires rework, and record the corrected ownership boundary.
5. Never force-push over another contributor's work.

A clean cherry-pick proves textual compatibility only.

### 7. Verify the integrated behavior

After the full successful wave is assembled:

1. Run every affected ticket's focused acceptance checks on the integrated tree.
2. Exercise each changed observable surface with a behavioral smoke test.
3. Run the repository-required tests, linters, builds, and review once on the combined revision through `verifying` or the repository's equivalent gate.
4. Re-run affected checks after any integration fix or target-branch update.

If two tickets interact only after fan-in, add or run the smallest durable test that protects that combined observable contract.

### 8. Publish, reconcile, and clean up

Use `finishing-a-development-branch` for the repository's normal merge, PR, or direct-push path. If this path creates or updates a GitHub PR, invoke `pr-review-loop`. Follow its timeout and clean-exit rules.

After the verified revision is merged or otherwise published to the target branch:

1. Confirm the published revision contains each accepted worker change.
2. Comment on each ticket with the commit or PR and verification evidence.
3. Close only tickets represented by the published revision.
4. Leave failed, blocked, deferred, or omitted tickets open with exact state.
5. Close a parent batch or epic last, only when all required children are closed.
6. Remove completed worktrees and branches. Preserve any worktree that contains unresolved or recoverable work.
7. Push tracker data and Git changes according to repository directives.

## Completion Report

Report facts in a table:

| Ticket | Worker result | Integrated commit | Verification | Tracker state |
|---|---|---|---|---|

Also report:

- tickets excluded from the wave and why;
- provider fallback used, without credential details;
- conflicts or hidden coupling found;
- published branch or PR; and
- remaining ready or blocked tickets.

## Rationalization Guard

| Temptation | Required response |
|---|---|
| "Worktree setup costs too much" | Reduce the wave; never share a mutable worktree |
| "They touch the same file but can coordinate" | Serialize them or partition ownership before dispatch |
| "The worker says tests passed" | Verify the integrated revision independently |
| "The cherry-pick was clean" | Run combined behavioral verification |
| "One provider is rate-limited" | Retry through a configured alternate provider |
| "The deadline requires closing now" | Publish a verified subset and leave unfinished tickets open |
