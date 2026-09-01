# Documentation Review

Automated review of repository prose with self-contained writing rules, evidence-backed findings, and controlled fixes.

## Installation

Add this repository to your marketplace and install the `documentation-review` plugin.

**Claude Code:**

```text
/plugin marketplace add <repository-path-or-URL>
/plugin install documentation-review@kyle-claude-plugins
```

**OMP:**

```text
omp plugin marketplace add <repository-path-or-URL>
omp plugin install --scope user documentation-review@kyle-claude-plugins
```

## Usage

Once installed, use the `/documentation-review:review` command to start a documentation review session.

**Default behavior (PR scope):**

```text
/documentation-review:review
```

**Review the entire repository:**

```text
/documentation-review:review --scope repository
```

**Narrow to specific paths:**

```text
/documentation-review:review --path docs/design-plans --path scripts
```
**Use a custom writing profile:**

```text
/documentation-review:review --profile <path=profile>
```

Repeated `--profile` flags allow you to apply multiple writing profiles in sequence.


**Apply previously approved findings:**

```text
/documentation-review:review --apply-approved finding-id-1 finding-id-2
```

**Automatically fix all findings:**

```text
/documentation-review:review --autofix
```

## Scope and exclusions

By default, the review command scans changes in the current pull request. Use `--scope repository` to review the entire codebase.

The `--path` flag narrows the review to specific directories or files. Provide multiple paths with repeated `--path` flags.

Default exclusions cover generated content, vendored dependencies, build output, dependency caches, minified files, lockfiles, tracking exports, and non-text files.

## Fix modes

The documentation review command supports three edit modes:

**Review-only mode:** The default behavior. Findings are reported with evidence and context but no automatic fixes are applied.

**Approved-fix mode:** Apply fixes to findings that were previously reviewed and approved. Use `--apply-approved` with a list of finding IDs to apply specific fixes.

**Autofix mode:** Automatically apply fixes to all findings in the safe fix class. Use `--autofix` to enable this mode. Fixes outside the safe class are reported without being applied.

## Runtime status

Claude Code and OMP are the supported runtimes. Installation, command discovery, and a repository-scope review-only run were verified on Claude Code 2.1.252 and OMP 18.0.11.

## Limitations

Prose detection is best-effort and does not claim complete language coverage. The review may miss some documentation issues or flag non-prose content, particularly in complex embedded content or mixed-language files.
