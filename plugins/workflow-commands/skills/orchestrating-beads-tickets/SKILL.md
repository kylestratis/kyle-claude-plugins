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

Parse the complete argument string before any Beads or Deciduous mutation. Require the value supplied to `--max-parallel` to be a positive integer. A malformed flag, a missing flag value, zero, or a negative value stops the run without claiming tickets. Cap the effective value at the task runtime's advertised concurrent-agent limit.

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
5. Inspect OMP provider routing only with `omp config get retry.modelFallback` and `omp config get retry.fallbackChains`. Never read the full OMP config, dump the environment, or read credential files. If either field-scoped query is unavailable or fails, treat alternate routing as unavailable and use the blocked path in Section 4.
6. Establish the orchestration identity before candidate evaluation:
   - When explicit ticket IDs include in-progress tickets, inspect only their status and structured orchestration metadata. Recover the run ID only when every such ticket has the same non-empty `orchestration.run` value. Stop before tracker mutation if an in-progress ticket lacks that value or the values disagree.
   - Otherwise, generate a new unique run ID.
   - Set the run actor to `orchestrate:<run-id>`.
7. Log a Deciduous action with the run ID, target branch, and candidate ticket IDs. Do not include provider configuration or credentials.

If the current worktree contains unrelated changes, keep integration in a separate worktree.

### 2. Build one runnable wave

For each candidate:

1. Run `bd show <ticket-id> --json`.
2. Require an open ticket, or an in-progress ticket owned by the recovered run. Resume only when its assignee is exactly `orchestrate:<run-id>`, its `orchestration.run`, `orchestration.branch`, and `orchestration.worktree` metadata are complete and match the recovered identity, the recorded branch exists, and the recorded worktree exists with that branch checked out. Reject every other in-progress ticket.
3. Require a leaf implementation ticket with no unresolved hard blocker. Exclude epics, parent batches, and parents with required open children; reconcile these containers in Section 8.
4. Read its description, acceptance criteria, dependencies, parent-child relationships, comments, and referenced code.
5. Determine the smallest credible write set and verification surface.

Classify every pair:

| Relationship | Action |
|---|---|
| Hard dependency | Run in separate waves, blocker first |
| Parent-child relationship | Dispatch required leaf children first; treat the parent as a reconciliation dependency, not worker implementation |
| Overlapping file, symbol, schema, migration, or observable workflow | Serialize unless the write sets can be partitioned before dispatch |
| Unknown write set | Investigate before dispatch; serialize if it remains unknown |
| Non-overlapping write sets and no dependency | Eligible for the same wave |

Do not dispatch inspection-only workers or invent work to fill `--max-parallel`.

After selecting the wave and before creating worktrees:

1. Assign stable branch and absolute worktree paths to every selected open ticket. Retain the recorded names for resumed tickets.
2. Atomically claim each selected open ticket and set its ownership metadata in the same update:

   ```bash
   bd update <ticket-id> --claim --actor "orchestrate:<run-id>" \
     --set-metadata "orchestration.run=<run-id>" \
     --set-metadata "orchestration.branch=<branch>" \
     --set-metadata "orchestration.worktree=<absolute-worktree-path>"
   ```

   A nonzero claim means another actor owns the ticket. Exclude that ticket from the wave and do not overwrite its assignee or metadata.
3. Re-run `bd show <ticket-id> --json` after each claim. Require `in_progress` state, assignee `orchestrate:<run-id>`, and exact ownership metadata. Exclude the ticket when any check fails.
4. Log one Deciduous decision with the selected wave, every exclusion and reason, and the ownership partition.

### 3. Fix the contracts before fan-out

Define in the task batch's shared context:

- target branch and integration owner;
- ticket-to-worktree mapping;
- exclusive file or subsystem ownership;
- shared interfaces, schemas, and assumptions;
- forbidden cross-ticket edits;
- commit and result format; and
- the rule that workers skip project-wide tests, linters, formatters, builds, and tracker mutation.

Create one branch and worktree per newly claimed ticket with `using-git-worktrees`. Name them from stable ticket IDs. Reuse the verified recorded branch and worktree for each resumed ticket.

Immediately before dispatch, re-run `bd show <ticket-id> --json` and inspect the assigned Git state. Require `in_progress` state, assignee `orchestrate:<run-id>`, exact ownership metadata, an existing recorded branch, and an existing recorded worktree with that branch checked out. Exclude the ticket when any check fails.

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

Classify failure by cause, not by when it occurs. A rate limit, timeout, provider outage, or other provider infrastructure error at any stage is provider failure, even after useful work exists.

1. Keep the ticket open and preserve its assigned branch and worktree.
2. Inspect that worktree and preserve useful commits and uncommitted changes.
3. When useful state exists, resume the same assignment in the same worktree through a configured alternate provider. Start a fresh retry only when inspection proves that the worktree has no useful state.
4. Prefer existing fallback chains. If an explicit override is required, use the narrowest task or session scope and restore the prior route after the batch.
5. Use only the field-scoped routing queries from Section 1. Never read, print, or place provider credentials in prompts, logs, URLs, or command arguments.

If no alternate provider is configured or the field-scoped routing queries are unavailable, mark the ticket blocked with the exact infrastructure reason and continue independent successful tickets. Never describe the full batch as complete.

For implementation failures, preserve useful work, record the failure on that ticket, and let independent siblings finish. Do not discard successful sibling commits because one worker failed.

Log a Deciduous decision whenever provider availability materially changes a ticket's route or state. Record the ticket, failure class, chosen fallback or blocked path, and rationale without provider configuration or credentials.

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
5. Log each material coupling decision in Deciduous with the affected tickets, discovered boundary, chosen integration or deferral, and rationale.
6. Never force-push over another contributor's work.

A clean cherry-pick proves textual compatibility only.

### 7. Verify the integrated behavior

After the full successful wave is assembled:

1. Run every affected ticket's focused acceptance checks on the integrated tree.
2. Exercise each changed observable surface with a behavioral smoke test.
3. If two tickets interact only after fan-in, add or run the smallest durable test that protects that combined observable contract.
4. Require a clean integration worktree. Record the exact pre-gate `HEAD` SHA and Git tree.
5. Invoke `verifying` without `--task` to run the repository-required tests, linters, builds, and review once on the combined revision. The verifier must not close any orchestration ticket.
6. After `verifying`, require a clean integration worktree and compare both `HEAD` and the Git tree with the pre-gate values. If the SHA or tree changed for any reason, or the worktree became dirty, incorporate the change and restart all of Section 7.
7. If any later integration fix, target-branch update, or new test changes code, restart all of Section 7 against the new head.

After all checks pass without a revision change, record the exact verified `HEAD` SHA and Git tree. Verification evidence belongs only to that code content.

### 8. Publish, reconcile, and clean up

Use `finishing-a-development-branch` to choose and execute the repository's normal merge, PR, or direct-push publication path, but postpone every branch and worktree cleanup step from that workflow. Publication and cleanup are separate phases here. Preserve the integration branch and worktree through PR review, exact published-head verification, and tracker reconciliation. If an external publication step removes either one, recreate an integration worktree at the published revision before continuing.

If the publication path creates or updates a GitHub PR, invoke `pr-review-loop` and follow its timeout and clean-exit rules. If finishing, PR review, merge resolution, merge, publication, or a branch update changes code, return to Section 7 and record the new exact verified SHA before continuing.

After the verified revision is merged or otherwise published to the target branch:

1. Resolve the published target SHA and confirm that it contains each accepted worker change.
2. Before tracker mutation, require the published SHA to equal the recorded verified SHA, or to contain it with an identical Git tree. If the published tree differs, run Section 7 on that exact published revision and record its SHA.
3. Comment on each ticket with the commit or PR and verification evidence.
4. Close only tickets represented by the final verified published revision.
5. Leave failed, blocked, deferred, or omitted tickets open with exact state.
6. Close a parent batch or epic last, only when all required children are closed.
7. Log a final Deciduous outcome with the run ID, published branch or PR, closed tickets, and tickets left open with reasons.
8. Push tracker data and Git changes according to repository directives.
9. Only after tracker reconciliation and its push, remove completed worktrees and branches. Preserve any worktree that contains unresolved or recoverable work.

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
