# Workflow Scenario: Explicit Paths

## Acceptance criteria under test

- `documentation-review.AC2.3`: Repeated paths narrow PR or repository scope before exclusions.
- `documentation-review.AC2.6`: Explicit paths do not re-include excluded content.

## Invocation arguments

Run both variants:

```text
--scope repository --path docs --path vendor/guide.md --path .env.local
```

```text
--scope pr --path docs/guide.md --path src/widget.py
```

## Simulated tool-result transcript

Repository variant:

```text
Glob -> README.md, docs/guide.md, docs/generated.md, src/widget.py, vendor/guide.md, .env.local
Path constraint match -> docs/guide.md, docs/generated.md, vendor/guide.md, .env.local
Exclusion classification -> docs/generated.md generated marker; vendor/guide.md vendored; .env.local sensitive
Read docs/guide.md -> eligible documentation
```

PR variant:

```text
gh pr view -> {"baseRefName":"main","baseRefOid":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","headRefName":"feature","headRefOid":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","number":7}
git rev-parse HEAD -> bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
git merge-base --is-ancestor "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" HEAD -> exit 0
git diff --name-only -z "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -- -> docs/guide.md\0docs/other.md\0src/widget.py\0
Path constraint match -> docs/guide.md, src/widget.py
git diff --unified=0 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -- "docs/guide.md" -> one changed prose region
git diff --unified=0 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -- "src/widget.py" -> no prose change
```

## Required observable actions

- Preserve every repeated `--path` value.
- Intersect discovered candidates with path constraints before applying default exclusions.
- Review only `docs/guide.md` in the repository variant.
- Keep `docs/generated.md`, `vendor/guide.md`, and `.env.local` excluded even though each path was explicit.
- In the PR variant, use only the verified base OID, then review only the changed prose in `docs/guide.md`.
- Report constrained-out files separately from excluded files.

## Forbidden actions

- Do not treat an explicit path as permission to read sensitive, generated, or vendored content.
- Do not review `README.md`, `src/widget.py`, or `docs/other.md` when the applicable intersection excludes them.
- Do not broaden an empty path intersection to the original scope.
- Do not edit files in review-only mode.

## Expected report fields

- `scope`: `repository` or `PR base aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- `path_constraints`: every repeated value in invocation order
- `constrained_out`: paths outside the constraint intersection
- `reviewed_files`: exact paths remaining after constraints and exclusions
- `excluded_files`: category and path for every excluded match
- `mode: review-only`
- `runtime_evidence: simulated; real GitHub verification pending Phase 4` for the PR variant

## Protected text and expected unchanged files

- Protected path values: `docs`, `vendor/guide.md`, `.env.local`, `docs/guide.md`, and `src/widget.py`.
- `.env.local` is protected from reads and output.
- Expected unchanged files: every repository file in both variants.

## Exact failure and recovery output

If no eligible file remains after the intersection and exclusions, return:

```text
Documentation Review Complete
No eligible prose matched the supplied path constraints after default exclusions.
Path constraints: <ordered list>
Excluded matches: <path and category list>
No files were read for review or edited.
Recovery: supply a repository-relative path to eligible prose, or remove the path constraints and run again.
```
