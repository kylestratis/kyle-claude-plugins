---
name: orchestrating-beads-tickets
description: Use when coordinating two or more independent ready Beads tickets in parallel - isolates workers, preserves dependency order, delegates provider fallback to the task runtime, integrates serially, and verifies the combined result before closing tickets
user-invocable: false
---

# Orchestrating Beads Tickets

## Overview

Run independent tickets concurrently, then integrate their work serially. The coordinator owns selection, isolation, fan-in, verification, and tracker reconciliation. The task runtime owns provider fallback. Each worker owns one ticket.

**Announce:** "I'm orchestrating independent Beads tickets in isolated worktrees."

## Arguments

`[<ticket-id> ...] [--max-parallel <count>]`

- With ticket IDs, evaluate only those tickets.
- Without ticket IDs, start from `bd ready --json`.
- `--max-parallel` defaults to 4 and limits a wave; it is not a target to fill.

Parse the complete argument string before any Beads or Deciduous mutation:

1. Accept zero or one exact two-token `--max-parallel <count>` option in any argument position.
2. Require `<count>` to match `^[1-9][0-9]*$`.
3. Reject a duplicate option, an unknown option, `--max-parallel=<count>`, a missing value, zero, a negative value, or any malformed value.
4. Treat all remaining tokens as ticket IDs.

Stop without mutation when parsing fails. Cap the effective value at the task runtime's advertised concurrent-agent limit.

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
7. Ticket closure remains provisional until the verified source is published and its local reconciliation commit passes the path check and push.

Deadline, sunk-cost, or authority pressure does not weaken these invariants. Reduce the wave or ship a verified subset instead.

## Workflow

### 1. Establish the integration baseline

1. Read the repository's tracking and completion directives.
2. Invoke `beads-deciduous-integration` for canonical tracker semantics and the repository-declared tracker and generated decision-graph paths.
3. Record the current target branch and preserve unrelated changes.
4. Refresh the target branch. Resolve and record its exact `target-sha`.
5. Generate a new unique run ID for every invocation. Set the run actor to `orchestrate:<run-id>`. Never recover a run ID or adopt branch, worktree, assignee, or metadata from an earlier run.
6. Log a Deciduous action with the run ID, target branch, `target-sha`, and candidate ticket IDs. Do not include infrastructure configuration or credentials.

The integration branch always uses a dedicated integration worktree. Preserve unrelated changes in every existing worktree.

### 2. Build one runnable wave

For each candidate:

1. Run `bd show <ticket-id> --json`.
2. Require `open` status. Reject every in-progress or blocked ticket. Earlier orchestration ownership is stale: never adopt its run ID, branch, worktree, assignee, or metadata. Report useful state for explicit manual recovery, or report the exact administrative release procedure below for an empty claim.
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

1. Assign a stable branch and absolute worktree path to every selected ticket.
2. Atomically claim each ticket and set its ownership metadata in the same update:

   ```bash
   bd update <ticket-id> --claim --actor "orchestrate:<run-id>" \
     --set-metadata "orchestration.run=<run-id>" \
     --set-metadata "orchestration.branch=<branch>" \
     --set-metadata "orchestration.worktree=<absolute-worktree-path>"
   ```

   A nonzero claim means another actor owns the ticket. Exclude that ticket from the wave and do not overwrite its assignee or metadata.
3. Re-run `bd show <ticket-id> --json` after each successful claim. Require `in_progress` status, assignee `orchestrate:<run-id>`, and exact ownership metadata. Apply the post-claim exit contract when any check fails.
4. Log one Deciduous decision with the selected wave, every exclusion and reason, and the ownership partition.

#### Post-claim exit contract

Every exit after a successful claim must use one of these paths. This includes setup errors, validation failures, worker failures, cancellation, deferral, publication errors, and coordinator interruption.

Useful state is an implementation commit, an uncommitted implementation change, or ticket-specific investigation that an operator can resume manually. An empty branch or worktree is not useful state.

When no useful state exists in the current run:

1. Remove the partial worker worktree and branch.
2. While the ticket is still owned by `orchestrate:<run-id>`, release it atomically:

   ```bash
   bd update <ticket-id> --status open --assignee "" \
     --unset-metadata orchestration.run \
     --unset-metadata orchestration.branch \
     --unset-metadata orchestration.worktree \
     --actor "orchestrate:<run-id>"
   ```

3. Re-run `bd show <ticket-id> --json`. Require `open` status, no assignee, and no orchestration metadata. Also confirm that the partial worker branch and worktree no longer exist.
4. Stop and report the exact unreleased state if any release check fails. If the run has no claimed tickets, also remove its unused integration branch and worktree.

A later invocation never releases ownership from an earlier run. Report the ticket as stale ownership with its exact status, assignee, run ID, branch, and worktree. For an interrupted empty claim, report this administrative release procedure exactly:

1. Inspect the recorded branch and worktree and prove that neither contains a commit, uncommitted implementation, or ticket-specific investigation.
2. Remove the empty recorded worktree, then delete its empty branch. If either no longer exists, record that fact.
3. Run:

   ```bash
   bd update <ticket-id> --status open --assignee "" \
     --unset-metadata orchestration.run \
     --unset-metadata orchestration.branch \
     --unset-metadata orchestration.worktree \
     --actor "admin:release-stale-orchestration"
   ```

4. Re-run `bd show <ticket-id> --json` and confirm `open` status, no assignee, no orchestration metadata, and no recorded branch or worktree. If useful state is found at step 1, stop: preserve it and recover it manually instead.

When useful state exists:

1. Preserve the exact worker branch, worktree, current commit, and uncommitted changes.
2. Keep the ticket in progress. Mark it blocked only when a final infrastructure error says that the task runtime exhausted its automatic fallback chain.
3. Record the failure class, exact reason, current commit, uncommitted paths, completed work, remaining work, branch, and worktree.
4. Require explicit manual recovery in that recorded worktree on that exact branch and state. A later orchestration invocation rejects the ticket and never adopts it.

### 3. Fix the contracts before fan-out

Define in the task batch's shared context:

- target branch, `target-sha`, and integration owner;
- ticket-to-worktree mapping;
- exclusive file or subsystem ownership;
- shared interfaces, schemas, and assumptions;
- forbidden cross-ticket edits;
- commit and result format; and
- the rule that workers skip project-wide tests, linters, formatters, builds, and tracker mutation.

Before creating any worker branch, use `using-git-worktrees` to create a dedicated integration branch and worktree at exactly `target-sha`. Confirm that the integration worktree owns that branch and has `target-sha` as its `HEAD`.

Create every worker branch and worktree from the same recorded `target-sha`, not from the coordinator's current `HEAD` or another worker branch. Name them from stable ticket IDs. A setup failure after claim uses the post-claim exit contract. If integration setup fails, release every claimed ticket that has no useful state.

Immediately before dispatch, re-run `bd show <ticket-id> --json` and inspect the assigned Git state. Require `in_progress` status, assignee `orchestrate:<run-id>`, exact ownership metadata, and a worker worktree that owns its recorded branch at the expected starting revision. Apply the post-claim exit contract when any check fails.

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

### 4. Handle worker and runtime failures

The task runtime owns its configured automatic provider fallback chain. The coordinator does not inspect provider routing, select providers, track attempted providers, set overrides, retry a provider, or mutate provider configuration. Wait for each dispatched task to settle after the runtime has applied its fallback behavior.

When a task settles successfully, continue with Section 5.

When a task settles with a final provider infrastructure error after runtime fallback exhaustion:

1. Inspect the assigned worktree and preserve useful commits and uncommitted changes.
2. Apply the post-claim exit contract.
3. Report the final infrastructure error without credentials, endpoints, routing configuration, or other provider details.

For implementation failures, apply the post-claim exit contract and let independent siblings finish. Do not discard successful sibling commits because one worker failed.

Log a Deciduous decision for a settled failure. Record the ticket, failure class, final reason, preserved state, and exit path. Do not record provider identifiers, routing configuration, or credentials.

### 5. Verify worker deliveries

For each successful worker, independently confirm:

- the reported commit exists on the assigned branch;
- the diff contains only owned changes;
- the worktree has no uncommitted implementation;
- no tracker, integration-branch, or unrelated files changed; and
- the implementation addresses the ticket's acceptance criteria.

Repair a delivery that violates ownership before integration. If the delivery is rejected or cannot be repaired, apply the post-claim exit contract. Agent self-reports are not sufficient.

### 6. Integrate serially

Use one integration owner and the dedicated integration branch and worktree created in Section 3. Run every integration command from the worktree that owns the integration branch.

1. Refresh the target branch view again. If it advanced after `target-sha`, incorporate the newer target commits into the integration branch before worker fan-in and record the new integration base.
2. Apply worker commits one at a time in dependency and semantic order.
3. Inspect the complete integrated diff after every commit.
4. Resolve conflicts in the integration worktree. Treat a conflict or semantic collision as evidence of hidden coupling. Continue serial fan-in if the integration owner can satisfy both accepted contracts. Defer a ticket only when it requires rework, and apply the post-claim exit contract with the corrected ownership boundary.
5. Log each material coupling decision in Deciduous with the affected tickets, discovered boundary, chosen integration or deferral, and rationale.
6. Never force-push over another contributor's work.

A clean cherry-pick proves textual compatibility only.

### 7. Verify the integrated behavior
Run this section in the integration worktree before publication. If Section 8 returns with a changed published revision, run it from the existing worktree that owns the published branch. Never switch a required branch into another worktree.

After the full successful wave is assembled:

1. Run every affected ticket's focused acceptance checks on the integrated tree.
2. Exercise each changed observable surface with a behavioral smoke test.
3. If two tickets interact only after fan-in, add or run the smallest durable test that protects that combined observable contract.
4. Require the source portion of the integration worktree to be clean. Source content is every tracked and untracked path except the repository-declared tracker and generated decision-graph paths. Record the exact pre-gate `HEAD` SHA and a snapshot of that source content.
5. Invoke `verifying` without `--task` to run the repository-required tests, linters, builds, and review once on the combined revision. The verifier must not close any orchestration ticket.
6. After `verifying`, compare the source-content snapshot with the pre-gate snapshot. Declared tracker or generated decision-graph mutations do not restart verification; preserve them in the worktree and carry them into Section 8. If any source content changed, incorporate the change and restart all of Section 7.
7. If any later integration fix, target-branch update, new test, or other mutation changes source content, restart all of Section 7 against the new source revision. Do not require whole-worktree cleanliness when only declared tracker or generated decision-graph paths differ.

After all checks pass without a source-content change, record the pre-gate `HEAD` as `verified-code-sha`. Verification evidence belongs only to that source content. Tracker-only mutations or commits do not replace `verified-code-sha`.

### 8. Publish, reconcile, and clean up

Present these worktree-aware choices directly:

- **Local merge:** merge from the existing worktree that owns the target branch.
- **Pull request:** create and update the PR from the integration worktree that owns the integration branch.
- **Keep as-is:** preserve the exact integration and worker branches, worktrees, ticket ownership, and recorded recovery context. This does not publish or close tickets and requires explicit manual recovery.

Discard is unavailable after worker work has been accepted. Defer all branch and worktree cleanup until publication and reconciliation succeed.

If the publication path creates or updates a GitHub PR, invoke `pr-review-loop` and follow its timeout and clean-exit rules. If PR review, merge resolution, publication, or a branch update changes source content, return to Section 7 and record the new `verified-code-sha`.

After the verified source reaches the target branch:

1. Resolve the published target SHA and confirm that it contains each accepted worker change.
2. Require its source content to match `verified-code-sha`. If source content differs, run Section 7 on that exact published revision and record a new `verified-code-sha`.
3. Record the exact pre-reconciliation ticket states and ownership. Treat every following tracker comment, closure, parent reconciliation, and Deciduous outcome as provisional.
4. Add the commit or PR and verification evidence to each represented ticket, close represented tickets, reconcile eligible parents last, and log the final Deciduous outcome. Leave failed, blocked, deferred, or omitted tickets in their recorded state.
5. From the existing worktree that owns the published target branch, create the reconciliation commit locally according to repository directives. It must contain the provisional tracker and generated decision-graph changes, including tracker-only mutations carried from Section 7.
6. Before any push, diff the reconciliation commit from `verified-code-sha`. Require every changed path to be a repository-declared tracker path or generated decision-graph path.
7. If the diff contains a source path, do not push. Reopen closed tickets and restore every provisional ticket state and ownership to the recorded pre-reconciliation values. Preserve all worker and integration branches and worktrees. Repair or verify the source change through Section 7, then repeat publication and reconciliation with a new local reconciliation commit.
8. Push the reconciliation commit only after the path check succeeds. Tracker comments, closures, parent state, and Deciduous outcomes become final only when that push succeeds. On push failure, keep them provisional, preserve ownership and all recovery state, and report the publication error.
9. Do not compare or claim whole-tree identity between `verified-code-sha` and the reconciliation commit. The pre-push path-bound diff is the reconciliation proof.
10. Only after the reconciliation push succeeds, remove completed worktrees and branches. Preserve any worktree that contains unresolved or recoverable work.

## Completion Report

Report facts in a table:

| Ticket | Worker result | Integrated commit | Verification | Tracker state |
|---|---|---|---|---|

Also report:

- tickets excluded from the wave and why;
- final infrastructure errors, without routing configuration, provider identifiers, or credentials;
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
| "One provider is rate-limited" | Let the task runtime apply its configured automatic fallback chain; act only on the settled task result |
| "The deadline requires closing now" | Publish a verified subset and leave unfinished tickets open |
