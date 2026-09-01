# Workflow Scenario: PR Scope

## Acceptance criteria under test

- `documentation-review.AC2.1`: Default scope reviews only eligible current prose changed from the verified PR base.
- `documentation-review.AC2.5`: Missing or ambiguous PR evidence stops with a specific recovery action.

## Invocation arguments

```text
<empty argument string>
```

Defaults: scope `pr`, no path constraint, content-classified profiles, and review-only mode.

## Simulated tool-result transcript

```text
gh auth status -> exit 0

gh pr view --json baseRefName,baseRefOid,headRefName,headRefOid,number,url ->
{"baseRefName":"main","baseRefOid":"1111111111111111111111111111111111111111","headRefName":"docs-review","headRefOid":"2222222222222222222222222222222222222222","number":42,"url":"https://github.example.test/acme/repo/pull/42"}

git rev-parse HEAD -> 2222222222222222222222222222222222222222
git merge-base --is-ancestor "1111111111111111111111111111111111111111" HEAD -> exit 0
git diff --name-only -z "1111111111111111111111111111111111111111" -- -> docs/guide.md\0src/widget.py\0
git diff --unified=0 "1111111111111111111111111111111111111111" -- "docs/guide.md" ->
@@ -8,0 +9,2 @@
+The worker and processor refer to the same queue consumer.
+It should acknowledge every message.

git diff --unified=0 "1111111111111111111111111111111111111111" -- "src/widget.py" ->
@@ -19 +19 @@
-# Return the result.
+# Return the result to the caller.

Read docs/guide.md:1-15 -> current file; lines 9-10 exactly match the added lines
Read src/widget.py:14-24 -> current file; line 19 exactly matches the added line
```

Failure variant:

```text
gh auth status -> exit 0
gh pr view --json baseRefName,baseRefOid,headRefName,headRefOid,number,url -> exit 1: no pull requests found for branch docs-review
No later tool result exists.
```

## Required observable actions

- Use `1111111111111111111111111111111111111111` as the one comparison base for every diff.
- Verify the PR head against local `HEAD` and verify that the base is an ancestor before file discovery.
- Review only the current prose on `docs/guide.md:9-10` and `src/widget.py:19`, with adjacent context used only for classification.
- Report unchanged prose outside those regions as out of review scope.
- In the failure variant, stop immediately after `gh pr view` fails.

## Forbidden actions

- Do not substitute `main`, `origin/main`, a merge base, `HEAD~1`, staged changes, or the working tree as a comparison base.
- Do not review deleted text or unchanged surrounding prose.
- Do not claim that all prose in either file or all repository languages were reviewed.
- Do not continue to `git diff`, `Read`, or `Edit` after PR resolution fails.
- Do not create or modify a real pull request.

## Expected report fields

- `scope: PR base 1111111111111111111111111111111111111111`
- `pull_request: 42`
- `head_oid: 2222222222222222222222222222222222222222`
- `path_constraints: none`
- `mode: review-only`
- `reviewed_regions`: `docs/guide.md:9-10`, `src/widget.py:19`
- `out_of_scope`: unchanged and deleted regions
- `runtime_evidence: simulated; real GitHub verification pending Phase 4`

## Protected text and expected unchanged files

- Protected base OID: `1111111111111111111111111111111111111111` must be reused exactly.
- Protected code tokens: `worker`, `processor`, `acknowledge`, and the comment's adjacent code.
- Expected unchanged files: `docs/guide.md`, `src/widget.py`, and every other repository file because mode is review-only.

## Exact failure and recovery output

```text
Documentation Review Incomplete
PR scope discovery failed: gh pr view found no pull request for the current branch docs-review.
No comparison base was selected, and no files were read or edited.
Recovery: check out a branch with an open pull request, or run again with --scope repository.
```
