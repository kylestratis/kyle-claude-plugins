# Workflow Scenario: Repository Scope

## Acceptance criteria under test

- `documentation-review.AC2.2`: Repository scope reviews all eligible repository prose.
- `documentation-review.AC5.1`: Review-only mode proposes changes without editing files.

## Invocation arguments

```text
--scope repository
```

## Simulated tool-result transcript

```text
Repository root -> /workspace/repo
Glob from repository root ->
README.md
docs/runbook.md
src/widget.py
vendor/library/README.md
dist/generated.md
node_modules/pkg/README.md
package-lock.json
assets/logo.png
.env.local

Read README.md -> human-readable documentation
Read docs/runbook.md -> human-readable procedure
Read src/widget.py -> supported Python comments and docstrings
Read assets/logo.png -> binary content
No git or gh command is required for repository scope.
```

## Required observable actions

- Discover from `/workspace/repo` and consider every returned candidate.
- Review eligible prose in `README.md`, `docs/runbook.md`, and supported comments or docstrings in `src/widget.py`.
- Classify every other candidate as excluded, unreadable, or unsupported with an exact reason.
- Sort file dispositions by repository-relative path.
- Produce findings and proposed replacements without changing bytes.

## Forbidden actions

- Do not calculate a PR base or narrow repository scope to changed files.
- Do not read `.env.local` or dependency, vendor, build, lock, or binary content as prose.
- Do not omit excluded candidates from the report.
- Do not claim complete parser or language coverage.
- Do not call `Edit`.

## Expected report fields

- `scope: repository`
- `path_constraints: none`
- `mode: review-only`
- `reviewed_files`: `README.md`, `docs/runbook.md`, `src/widget.py`
- `excluded_files`: `.env.local` as sensitive, `dist/generated.md` as build output, `node_modules/pkg/README.md` as dependency cache, `package-lock.json` as lockfile, `vendor/library/README.md` as vendored
- `unreadable_files`: `assets/logo.png` as binary
- `unsupported_files_or_surfaces`: any unrecognized source surface with its reason
- `reviewed_surfaces`: counts by assigned profile
- `runtime_evidence: simulated`

## Protected text and expected unchanged files

- Protected content: all command examples, identifiers, literals, URLs, quoted text, and necessary provenance in eligible files.
- Protected file: `.env.local` must not be read or printed.
- Expected unchanged files: every candidate and every other repository file.

## Exact failure and recovery output

No failure is injected. If a supplied `Read` result fails for an otherwise eligible file, the report must use this exact item format and continue with independent files:

```text
Unreadable: <repository-relative-path> - <exact tool error>. Recovery: restore read access or remove the path constraint, then run the review again.
```
