# Documentation Review Design

## Summary
The `documentation-review` plugin follows the repository's thin-command pattern. `commands/review.md` forwards its full argument string to `skills/reviewing-documentation/SKILL.md`. The skill owns scope discovery, exclusions, surface classification, rule application, findings, fix control, verification, and reporting. Bundled references provide portable rules without a dependency on an external STE plugin.

The workflow reviews PR changes by default and supports explicit repository scope and path constraints. Repository writing directives override invocation settings, text-surface profiles, and general guidance. Technical correctness and source fidelity remain safety constraints. Structured fix-safety classes control default proposals, approved fixes, and autofix. A second review and stale-target checks protect concurrent work.

## Definition of Done
A third marketplace plugin provides Claude Code and OMP users with an explicit documentation-review workflow. It reviews PR changes by default or the whole repository on request, applies self-contained STE-inspired and evergreen-writing conventions to human-readable prose, and returns evidence-backed findings with proposed fixes. Explicit autofix mode safely applies eligible fixes, while document profiles preserve necessary historical context and default exclusions prevent review of generated or non-owned content.

## Acceptance Criteria
### documentation-review.AC1: Plugin installation and command routing

- **documentation-review.AC1.1 Success:** Claude Code installs the plugin from this repository's marketplace and discovers the review command.
- **documentation-review.AC1.2 Success:** OMP installs the same plugin source and discovers the review command.
- **documentation-review.AC1.3 Success:** The command passes the complete argument string to the review skill.
- **documentation-review.AC1.4 Failure:** Unknown or contradictory arguments stop the review and identify the invalid arguments.

### documentation-review.AC2: Review scope and discovery

- **documentation-review.AC2.1 Success:** An invocation without a scope reviews only eligible prose changed from the verified PR base.
- **documentation-review.AC2.2 Success:** Repository scope reviews all eligible repository prose.
- **documentation-review.AC2.3 Success:** Explicit paths narrow PR or repository scope.
- **documentation-review.AC2.4 Success:** The report identifies reviewed, excluded, unreadable, and unsupported files.
- **documentation-review.AC2.5 Failure:** A missing or ambiguous PR base stops the review with recovery instructions.
- **documentation-review.AC2.6 Failure:** Generated, vendored, build, tracking-export, minified, lock, binary, and dependency-cache content is excluded by default.

### documentation-review.AC3: Rule precedence and surface profiles

- **documentation-review.AC3.1 Success:** Applicable repository writing directives override invocation, profile, and bundled writing rules.
- **documentation-review.AC3.2 Success:** Explicit invocation overrides take precedence over profile and general rules.
- **documentation-review.AC3.3 Success:** Documentation, procedures, prompts, docstrings, comments, and historical records receive their applicable profiles.
- **documentation-review.AC3.4 Success:** Historical records can retain necessary dates, versions, ticket references, and provenance.
- **documentation-review.AC3.5 Failure:** A lower-priority style rule never changes technical meaning or quoted source text.
- **documentation-review.AC3.6 Failure:** The reviewer does not invent a rationale when a comment or docstring lacks one.

### documentation-review.AC4: Evidence-backed findings

- **documentation-review.AC4.1 Success:** Each finding includes its location, rule identifier, severity, profile, evidence, reason, suggested action, and fix-safety class.
- **documentation-review.AC4.2 Success:** The report identifies ticket references that replace a lasting explanation.
- **documentation-review.AC4.3 Success:** The report identifies docstrings that only repeat names, signatures, or declared types.
- **documentation-review.AC4.4 Success:** The report identifies comments that narrate visible control flow or repeat adjacent code.
- **documentation-review.AC4.5 Success:** Overlapping findings are consolidated and ordered by file, location, and severity.
- **documentation-review.AC4.6 Failure:** The reviewer does not claim complete language coverage and identifies the surfaces it reviewed.

### documentation-review.AC5: Fix behavior and safety

- **documentation-review.AC5.1 Success:** Default review proposes fixes and does not modify files.
- **documentation-review.AC5.2 Success:** Approved-fix mode applies only the findings selected by the user.
- **documentation-review.AC5.3 Success:** Autofix applies all and only findings classified as safe.
- **documentation-review.AC5.4 Failure:** Review-required findings remain unchanged until the user selects them.
- **documentation-review.AC5.5 Failure:** Report-only findings are never changed automatically.
- **documentation-review.AC5.6 Failure:** Safe fixes do not modify code tokens, identifiers, literals, commands, URLs, quoted text, or necessary provenance.
- **documentation-review.AC5.7 Failure:** Conflicting fixes remain unapplied and appear in the report.

### documentation-review.AC6: Verification and recovery

- **documentation-review.AC6.1 Success:** Every modified region receives a second review.
- **documentation-review.AC6.2 Success:** The completion report separates proposed, selected, applied, skipped, failed, and unresolved findings.
- **documentation-review.AC6.3 Success:** Independent successful fixes remain applied when another fix fails.
- **documentation-review.AC6.4 Failure:** A changed target or mismatched patch stops that edit without overwriting concurrent work.
- **documentation-review.AC6.5 Failure:** Every incomplete review or edit reports the exact reason and a specific recovery action.

## Glossary
- **STE (Simplified Technical English)**: The ASD-STE100 controlled-language standard for unambiguous technical prose. The plugin uses bundled STE-inspired guidance.
- **OMP (Oh My Pi)**: One target coding runtime for the plugin.
- **Claude Code**: One target coding runtime for the plugin.
- **Marketplace plugin**: A distributable unit registered in `.claude-plugin/marketplace.json`.
- **Plugin manifest**: The `.claude-plugin/plugin.json` file that declares plugin identity and metadata.
- **Routing-only command**: A command that forwards its complete argument string to a skill and contains no review logic.
- **Skill**: A capability defined by a `SKILL.md` file.
- **PR base**: The verified baseline commit for a pull-request comparison.
- **PR scope**: The default scope that reviews prose changed relative to the PR base.
- **Repository scope**: The explicit scope that reviews all eligible repository prose.
- **Evergreen prose**: Writing that stays valid without transient project context.
- **Text-surface profile**: The rules for one prose category, such as documentation, procedures, prompts, docstrings, comments, or historical records.
- **Docstring**: Documentation attached to a source declaration.
- **Historical record**: Content that can retain necessary dates, versions, ticket references, and past-tense provenance.
- **Provenance**: Information that records the source or history of a statement.
- **Fix-safety class**: A finding disposition of `safe`, `review-required`, or `report-only`.
- **Autofix mode**: An explicit mode that applies all findings classified as safe.
- **Approved-fix mode**: A continuation mode that applies only findings selected by the user.
- **Stale target**: A reviewed region whose content changed before the proposed edit.
- **Vendored dependency**: Third-party code copied into the repository and excluded from review by default.
- **Lockfile**: A dependency-pinning file excluded from review by default.
- **Tracking export**: Generated task or decision data excluded from review by default.

## Architecture

The repository will add a third marketplace plugin at `plugins/documentation-review/`. The plugin will use the same thin-command pattern as `workflow-commands`: `commands/review.md` passes the complete argument string to `skills/reviewing-documentation/SKILL.md`, and the skill owns argument parsing, scope discovery, review, fix control, verification, and reporting.

The skill supports two scopes:

- PR scope is the default. It reviews eligible prose changed relative to the verified PR base.
- Repository scope is explicit. It reviews all eligible prose in the repository.

Explicit paths can narrow either scope. The skill applies path constraints before exclusions and reports each excluded or unreadable file category. If it cannot establish a reliable PR base, it stops with recovery instructions. It does not select a different comparison range.

Eligible prose includes human-readable documentation, skill and agent instructions, command prompts, docstrings, and code comments. Detection is language-agnostic and best-effort. The report identifies the files and text surfaces that the skill reviewed. It does not claim complete parser coverage for all programming languages.

The plugin owns its writing rules. It does not require or invoke an external STE plugin. Reference files under `skills/reviewing-documentation/references/` define controlled-language guidance, evergreen prose, text-surface profiles, finding severities, and fix safety. `SKILL.md` defines operational exclusions as part of scope discovery.

Applicable repository and directory-specific writing directives take precedence over bundled writing rules. Explicit invocation overrides come next, followed by the selected text-surface profile and general guidance. Technical correctness and quoted-source fidelity are safety constraints and cannot be overridden by style policy.

### Review Flow

The skill uses this fixed pipeline:

1. Parse the scope, paths, edit mode, and profile overrides.
2. Establish the PR baseline when PR scope is active.
3. Discover eligible files and apply exclusions.
4. Classify each prose region by text-surface profile.
5. Apply repository rules and the applicable bundled rules.
6. Consolidate and order evidence-backed findings.
7. Propose fixes or apply the permitted fixes.
8. Re-review modified regions and report unresolved findings.

The default mode reports findings and proposes fixes without modifying files. An approved-fix continuation applies only findings that the user selects. Explicit autofix mode applies all findings classified as safe. Findings classified as review-required always need explicit selection. Report-only findings are never changed automatically.

### Finding Contract

Each finding contains:

- File and line or region
- Stable rule identifier
- Severity
- Text-surface profile
- Quoted evidence
- Explanation of the violation
- Suggested replacement or corrective action
- Fix safety: `safe`, `review-required`, or `report-only`

A safe fix must preserve technical meaning, avoid changes to code tokens and quoted material, use a precise replacement region, avoid conflicts with other edits, and require no invented rationale. The skill stops before an edit when the target changed after review or the proposed patch no longer matches.

## Existing Patterns

This design follows the marketplace structure in `.claude-plugin/marketplace.json` and the plugin manifest pattern in `plugins/workflow-commands/.claude-plugin/plugin.json`.

Commands remain routing-only, as shown by `plugins/workflow-commands/commands/fix-pr-review.md`. The command forwards the full argument string, while the skill documents flags, defaults, workflow phases, and completion output.

The evidence and disposition model follows `plugins/workflow-commands/skills/pr-review-loop/SKILL.md`. The new skill similarly requires concrete evidence before it proposes or applies a change. It extends that model with prose profiles and explicit fix-safety classes.

The repository has no established documentation exclusion system, safe prose-autofix contract, plugin-specific test layout, or deterministic prose checker. This design introduces the first three where required. It does not introduce a checker, hook, external NLP dependency, or reviewer agent.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Plugin Contract and Distribution

**Goal:** Register an installable documentation-review plugin with a stable user-facing command contract.

**Components:**

- `.claude-plugin/marketplace.json` - marketplace registration and pinned plugin version
- `plugins/documentation-review/.claude-plugin/plugin.json` - plugin identity and metadata
- `plugins/documentation-review/commands/review.md` - routing-only command that passes the full argument string
- `plugins/documentation-review/README.md` - installation, invocation modes, scope behavior, and compatibility claims

**Dependencies:** None.

**Done when:** Claude Code and OMP can install the plugin from this marketplace, discover the review command, and pass its complete argument string to the skill. Installation and command-discovery smoke checks pass in both runtimes.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Writing Policy and Profiles

**Goal:** Define the self-contained policy that controls review findings and fix safety.

**Components:**

- `plugins/documentation-review/skills/reviewing-documentation/references/writing-rules.md` - controlled language, evergreen prose, ticket-reference, terminology, and link rules
- `plugins/documentation-review/skills/reviewing-documentation/references/surface-profiles.md` - general, procedural, prompt, docstring, comment, and historical-record profiles
- `plugins/documentation-review/skills/reviewing-documentation/references/fix-safety.md` - finding severities, safety classes, precedence, conflict handling, and prohibited edits
- `plugins/documentation-review/tests/fixtures/` - representative compliant and noncompliant prose for each profile

**Dependencies:** Phase 1.

**Done when:** Each rule has a stable identifier, applicability, evidence requirement, and fix-safety default. Structurally correct fixtures cover repository-rule precedence, necessary historical provenance, technical terms, quoted text, ticket-only explanations, repetitive comments, and contract-poor docstrings for `documentation-review.AC3` and `documentation-review.AC4`. Phase 3 runs the skill against scope and policy fixtures to satisfy `documentation-review.AC2` through `documentation-review.AC4`.
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Review and Fix Workflow

**Goal:** Implement the complete review pipeline in one portable skill.

**Components:**

- `plugins/documentation-review/skills/reviewing-documentation/SKILL.md` - argument parsing, PR baseline selection, repository discovery, exclusions, surface classification, review, finding consolidation, fix control, verification, and completion reports
- `plugins/documentation-review/tests/fixtures/` - PR-scope, repository-scope, explicit-path, stale-target, partial-failure, and mixed-profile scenarios

**Dependencies:** Phases 1 and 2.

**Done when:** Behavioral evaluations verify every criterion in `documentation-review.AC1` through `documentation-review.AC6`. Default review makes no edits. Approved and autofix modes respect safety classes. Modified regions receive a second review, and every failure produces specific recovery instructions.
<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: Cross-Runtime Verification and Release

**Goal:** Prove the documented behavior in Claude Code and OMP and publish the plugin through the existing marketplace.

**Components:**

- `plugins/documentation-review/README.md` - verified runtime behavior, limitations, exclusions, and examples
- `.claude-plugin/marketplace.json` - release version and final metadata
- Behavioral evaluation records for Claude Code and OMP installations

**Dependencies:** Phases 1 through 3.

**Done when:** Both runtimes install the marketplace plugin and complete PR-scope, repository-scope, review-only, approved-fix, and autofix smoke scenarios. Documentation states only observed compatibility. All acceptance criteria pass in the applicable runtime evaluations.
<!-- END_PHASE_4 -->

## Additional Considerations

### Exclusions

Default exclusions cover generated content, vendored dependencies, build output, dependency caches, minified files, lockfiles, tracking exports, and non-text files. Historical records are not excluded. Their profile permits necessary dates, versions, ticket references, and past-tense descriptions.

### Concurrent Changes

The skill treats target content as stale when it differs from the reviewed region. It does not overwrite concurrent user changes or broaden a replacement region to force a patch to apply. Independent successful fixes can remain applied when another fix fails, but the report must distinguish each result.

### Deferred Components

The first release has no lifecycle hook, custom executable, external NLP package, deterministic checker, or reviewer agent. These components require new runtime assumptions or operational cost. They need evidence from first-release usage before they enter a later design.
