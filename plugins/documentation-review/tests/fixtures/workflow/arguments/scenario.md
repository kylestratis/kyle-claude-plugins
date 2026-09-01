# Workflow Scenario: Arguments

## Acceptance criteria under test

- `documentation-review.AC1.3`: The complete routed argument string reaches the skill without dropping repeated values.
- `documentation-review.AC1.4`: All invalid and contradictory arguments are reported, and processing stops before discovery.

## Invocation arguments

Run each case as a separate invocation in the listed order.

1. Valid: `--scope repository --path docs/guide.md --path src/widget.py --profile docs/guide.md=procedure --profile src/widget.py=docstring`
2. Unknown and positional: `README.md --mystery yes --scope repository`
3. Missing values: `--path --profile --apply-approved`
4. Invalid values: `--scope branch --profile docs/guide.md=tutorial`
5. Outside repository: `--path ../private.txt --profile /tmp/note.md=comment`
6. Contradictory modes: `--autofix --apply-approved DR-002 --apply-approved DR-004`
7. Missing snapshot: `--apply-approved DR-001`

The valid grammar is:

```text
[--scope pr|repository]
[--path <repository-relative-path>]...
[--profile <repository-relative-path>=general|documentation|procedure|prompt|docstring|comment|historical-record]...
[--apply-approved <finding-id>]...
[--autofix]
```

## Simulated tool-result transcript

```text
Command router -> skill arguments:
--scope repository --path docs/guide.md --path src/widget.py --profile docs/guide.md=procedure --profile src/widget.py=docstring

Tool calls available: git, gh, Glob, Grep, Read, Edit
Tool results: NONE. Argument validation occurs before all tool calls.
Current-conversation review snapshot: NONE.
Repository root: /workspace/repo (provided only for lexical containment validation).
```

## Required observable actions

- Tokenize and validate the complete argument string before any discovery, file read, or edit.
- Preserve both `--path` values and both `--profile` mappings in their original order for the valid case.
- Resolve the valid case to scope `repository`, path constraints `docs/guide.md` and `src/widget.py`, profile overrides `docs/guide.md=procedure` and `src/widget.py=docstring`, and mode `review-only`.
- For each invalid case, list every invalid or contradictory argument in that invocation, print the complete valid grammar, and stop that invocation.
- Reject `DR-001` because the current conversation has no immediately preceding review snapshot.
- Record that zero discovery, read, and edit tools ran for every invalid case.

## Forbidden actions

- Do not silently discard, reorder, or coalesce repeated arguments.
- Do not interpret positional values as paths or finding IDs.
- Do not recover a missing value from the following flag.
- Do not normalize an outside path into the repository.
- Do not choose one edit mode when both edit modes are present.
- Do not run `git`, `gh`, `Glob`, `Grep`, `Read`, or `Edit` after validation fails.
- Do not reconstruct an approved finding from repository files or an earlier conversation.

## Expected report fields

For the valid case, report:

- `scope: repository`
- `path_constraints: [docs/guide.md, src/widget.py]`
- `profile_overrides: [docs/guide.md=procedure, src/widget.py=docstring]`
- `mode: review-only`
- `validation: valid`
- `routed_argument_string`: the exact invocation string

For each invalid case, report:

- `validation: invalid`
- `invalid_arguments`: every invalid or contradictory token with its reason
- `valid_grammar`: the complete grammar above
- `tools_called: none`
- `status: stopped before discovery`

## Protected text and expected unchanged files

- Protected argument text: repeated `--path` and `--profile` values must remain byte-identical.
- Expected unchanged files: every repository file. No case permits an edit.

## Exact failure and recovery output

Each invalid invocation must end with this structure and substitute the complete itemized reasons for `<all reasons>`:

```text
Argument validation failed:
<all reasons>
Valid grammar:
[--scope pr|repository]
[--path <repository-relative-path>]...
[--profile <repository-relative-path>=general|documentation|procedure|prompt|docstring|comment|historical-record]...
[--apply-approved <finding-id>]...
[--autofix]
Stopped before git discovery, file reads, or edits. Correct every listed argument and run the review again.
```

For case 7, the reason and recovery must be exact:

```text
- --apply-approved DR-001: no matching review snapshot exists in the current conversation. Run a review-only invocation first, then approve an ID from that immediately preceding snapshot.
```
