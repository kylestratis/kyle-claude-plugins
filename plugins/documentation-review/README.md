# Documentation Review

Automated review of repository prose with self-contained writing rules, evidence-backed findings, and controlled fixes.

## Installation

Add this repository to your marketplace and install the `documentation-review` plugin.

**Claude Code:**

```text
/plugin marketplace add /Users/kyle/code/kyle-claude-plugins
/plugin install documentation-review@kyle-claude-plugins
```

**OMP:**

```text
omp plugin marketplace add /Users/kyle/code/kyle-claude-plugins
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

The review process excludes binary files, generated artifacts, lock files, and compiled dependencies. Configuration and build output directories are also excluded by default.

## Fix modes

The documentation review command supports three edit modes:

**Review-only mode:** The default behavior. Findings are reported with evidence and context but no automatic fixes are applied.

**Approved-fix mode:** Apply fixes to findings that were previously reviewed and approved. Use `--apply-approved` with a list of finding IDs to apply specific fixes.

**Autofix mode:** Automatically apply fixes to all findings in the safe fix class. Use `--autofix` to enable this mode. Fixes outside the safe class are reported without being applied.

## Runtime status

This plugin is designed for use with Claude Code and OMP. Both runtimes can install and discover the `/documentation-review:review` command through the repository's marketplace entry.

## Limitations

Prose detection is best-effort and does not claim complete language coverage. The review may miss some documentation issues or flag non-prose content, particularly in complex embedded content or mixed-language files.
