# Fix Safety Policy

## Safety Constraints

Technical correctness and quoted-source fidelity override every style rule and invocation option. No style change, profile adjustment, or user preference may alter technical meaning, rewrite quoted material, or remove necessary provenance. If a proposed change violates these invariants, the finding must be marked `report-only` and the controlling safety constraint must be stated in the reason.

---

## Rule Precedence

When multiple rules or directives apply to the same prose region, higher-priority sources control the finding. A higher-priority rule suppresses conflicting lower-priority findings. Record the controlling source in the finding reason.

Define precedence in this exact order:

1. **Applicable repository and directory-specific writing directives** — Directives in `CLAUDE.md`, `.cursorrules`, domain-specific `CLAUDE.md` files, or policy files that apply to the repository or directory containing the reviewed text. These override all lower-priority sources.

2. **Explicit invocation overrides** — Rules, profiles, or severity adjustments passed as parameters to the review operation. These override profile-specific settings but must not violate safety constraints or repository directives.

3. **The classified text-surface profile** — The profile assigned to the reviewed prose (documentation, procedure, prompt, docstring, comment, historical-record, or general). Profiles define applicable rules and required protections for their surfaces.

4. **General bundled writing rules** — The 12 writing rules (WR-001 through WR-012) as applied to the classified profile. These are the fallback when no higher-priority source defines behavior.

---

## Finding Schema

Each finding must include these fields with the exact identifiers and values specified:

### id

A stable, review-local identifier in the form `DR-<three-digit sequence>` (e.g., `DR-001`, `DR-042`). Identifiers are assigned after consolidation and final ordering; they remain stable for the current review snapshot.

### location

The file containing the finding plus a precise line number or line range, or a precise region description that unambiguously identifies the reviewed text. Format: `file:line` or `file:start-end` or `file:region_name`. Example: `README.md:45-47` or `src/core.py:52`.

### rule

The stable identifier of the rule violated. Format: `WR-###` (e.g., `WR-001`). This field links findings to the writing rules catalogue.

### severity

The severity of the finding. One of:

- `critical` — A proposed change can alter technical meaning, protected source text, or required provenance. No automatic fix is permitted.
- `major` — The prose can misdirect implementation or operation, or lacks durable contract information. Review is required before any fix.
- `minor` — The issue reduces clarity or maintainability without changing the documented contract. Review is recommended before automated fixes, but automated fixes may be permitted if they are low-risk.

### profile

The classified text-surface profile of the reviewed prose. One of: `general`, `documentation`, `procedure`, `prompt`, `docstring`, `comment`, `historical-record`.

### evidence

The exact reviewed text, quoted to unambiguously identify the violation. Include enough context to understand the finding without re-reading the source file.

### reason

An evidence-backed description of the violation and the controlling policy. The reason must:

1. Quote or describe the specific violation.
2. Cite the applicable rule (WR-*) and its requirement.
3. If multiple rules or precedence tiers apply, name the controlling source.
4. If safety constraints apply, state them explicitly.
5. Do not invent rationale or contract details beyond what the evidence and applicable rules support.

### suggested_action

A replacement or corrective action. The action must:

1. Be specific and actionable (not a general request to "improve the text").
2. Quote the proposed replacement or describe the specific change.
3. Be consistent with the profile and applicable rules.
4. Preserve all protected content, technical meaning, and source fidelity.
5. If no suitable action exists (e.g., missing facts are required), state "No automatic action possible; requires investigation and user judgment."

### fix_safety

The safety class of the suggested action. One of:

- `safe` — The replacement is exact, local, conflict-free, source-preserving, and requires no inferred meaning, rationale, or scope decision. All conditions are required: a finding marked `safe` must meet all of them. Examples: fixing a typo, applying consistent terminology within a single phrase, correcting a date that is factually wrong.

- `review-required` — A reasonable replacement exists, but meaning, tone, scope, deletion safety, or policy choice requires user judgment. Examples: choosing between two synonyms, deciding whether to delete a comment, resolving ambiguous pronouns, consolidating repetitive sections.

- `report-only` — A correct replacement requires missing facts, an invented rationale, changes to protected content, or a non-writing change. The reviewer cannot propose a specific fix without additional context or a design decision outside the scope of documentation review. Examples: a ticket-only explanation (WR-005) lacks the missing context; a docstring (WR-010) lacks side effect information; a protected date is inaccurate and requires historical verification.

Default fix-safety values are defined per rule in the writing rules catalogue. Downgrade `safe` to `review-required` or `report-only` when any invariant is uncertain or when the change involves ambiguity. Never upgrade a finding past its rule default without explicit repository policy that supplies the exact replacement.

---

## Severity Definitions

### critical

A proposed change can alter technical meaning, protected source text, or required provenance. Examples:

- Rewriting quoted source material, command syntax, or identifiers.
- Changing a date, version number, or ticket reference in a historical record.
- Removing necessary authorship or context from a decision record.
- Altering the meaning of a specification or requirement that affects implementation.

Critical findings must always be `report-only` because any fix requires human judgment about what the correct meaning is or whether the protected content is accurate.

### major

The prose can misdirect implementation or operation, or lacks durable contract information. Examples:

- Inconsistent terminology that obscures whether two sections refer to the same feature.
- Ambiguous requirement strength ("should" vs. "must") that could lead to incorrect implementation.
- A procedure with multiple actions per step or missing prerequisites.
- A docstring that does not document errors or side effects.
- Transient context in an explanation without a lasting reason.

Major findings often allow `review-required` fixes because reasonable alternatives exist, but the choice between them depends on understanding the intent and context.

### minor

The issue reduces clarity or maintainability without changing the documented contract. Examples:

- A comment that narrates visible code.
- An unambiguous link that is not broken but could be more accessible.
- Inconsistent capitalization or formatting in examples.
- A docstring that is brief but complete.

Minor findings may allow `safe` or `review-required` fixes when they are low-risk and do not affect technical meaning.

---

## Fix Safety Definitions

### safe

The replacement is exact, local, conflict-free, source-preserving, and requires no inferred meaning, rationale, or scope decision. Every condition below is required:

- **Exact:** The replacement text is a straightforward substitution; no paraphrasing or interpretation is needed.
- **Local:** The change is confined to the identified region and does not require modifications elsewhere.
- **Conflict-free:** The change does not interact with other findings or rules in the same region.
- **Source-preserving:** The change preserves all quoted material, technical terms, identifiers, and necessary provenance.
- **No inferred meaning:** The replacement does not require guessing the author's intent or inferring missing context.

Examples of `safe` fixes:
- Fixing a typo: "bussiness" → "business".
- Applying consistent terminology: "container deployment" → "containerized deployment" (when uniformly applied).
- Correcting a date or version that is factually wrong in a historical record.

If any condition is uncertain, downgrade to `review-required` or `report-only`.

### review-required

A reasonable replacement exists, but meaning, tone, scope, deletion safety, or policy choice requires user judgment. Examples:

- Choosing the canonical term when multiple synonyms are used.
- Deciding whether a comment is safe to delete or should be preserved.
- Resolving ambiguous pronouns; the correct referent is clear from context, but confirming it requires human judgment.
- Reordering steps in a procedure; the order seems wrong, but operational impact must be verified.
- Adding a missing piece of information (e.g., a rationale) requires confirming the actual reason.

A `review-required` fix is proposed but marked for human review before application. The reviewer must examine the context, understand the intent, and confirm that the replacement is appropriate.

### report-only

A correct replacement requires missing facts, an invented rationale, changes to protected content, or a non-writing change. The reviewer cannot propose a specific fix without additional information or a decision outside the scope of documentation review. Examples:

- **Ticket-only explanation (WR-005):** The text "See issue #1234" lacks the missing explanation. Providing an explanation requires access to the issue tracker and understanding the decision history.
- **Contract-poor docstring (WR-010):** The docstring lacks error documentation. Inventing the possible errors would be incorrect; the author must provide this information.
- **Protected provenance (WR-012):** A date or version in a historical record is inaccurate. Correcting it requires verifying the historical record, not just fixing the text.
- **Source fidelity (WR-007):** Quoted source text has been altered. Restoring it requires access to the original source and confirmation of the correct text.

Report-only findings are documented but cannot be automatically fixed. They require additional investigation, design discussion, or domain expertise.

---

## Overlap and Conflicts

When multiple findings share overlapping evidence regions, consolidate them as follows:

1. **Group findings by evidence region:** Identify all findings whose evidence regions overlap or are adjacent (within 1-2 lines).

2. **Keep the highest-severity root finding:** Among overlapping findings, retain the finding with the highest severity (`critical` > `major` > `minor`). This becomes the root finding.

3. **Merge compatible reasons and rule identifiers:** Add the rule identifiers and evidence-backed reasons of subordinate findings to the root finding's reason. The merged reason explains all violations in the region.

4. **If replacements conflict:** When multiple findings in the same region propose different replacements or deletions:
   - Apply neither replacement.
   - Mark the finding as `unresolved`.
   - Note in the reason that replacements conflict and require manual triage.

5. **Order final findings by:** file path, starting line number, then severity (`critical`, `major`, `minor`).

Example:

**Finding 1 (WR-001, major):** "container" and "Docker" are inconsistent terms for the same feature (line 5).

**Finding 2 (WR-003, major):** "it" is ambiguous; could refer to "container" or "deployment" (line 6).

**Merged finding:** Identifies the terminology inconsistency and the ambiguous pronoun; gives the root finding severity `major` and rule `WR-001`; includes reason that explains both violations.

---

## Prohibited Automatic Changes

The following content categories must never be automatically modified, regardless of severity or fix-safety classification. Human review is always required:

- **code tokens:** Variable names, function names, class names, module names, or any identifier used in code.
- **identifiers:** Command names, option flags, environment variable names, file paths, or URL paths.
- **literals:** String values, numbers, boolean values, or any exact value used in code or configuration.
- **commands:** Shell commands, API calls, or sequences of instructions; preserve exact syntax and argument order.
- **URLs:** Hyperlinks, endpoint paths, or external references; preserve exact formatting and protocol.
- **quoted text:** Any material explicitly marked as a quote, copied from an external source, or referenced as an exact value.
- **necessary provenance:** Dates, version numbers, ticket references, authorship, or historical context that establishes when and why a decision was made.

No style rule, profile adjustment, or fix-safety class permits automatic modification of these categories.

---

## Stale-Target Prevention

An edit is permitted only when the current region exactly matches the reviewed region. Before applying a fix:

1. **Verify the region:** Re-read the current file at the location specified in the finding.
2. **Match the evidence:** Confirm that the evidence field's text matches the current file exactly, byte-for-byte.
3. **Apply only if matching:** If the current text matches the reviewed evidence, apply the fix.
4. **Abort if stale:** If the current text has changed since review (even a single character differs), do not apply the fix. Mark the finding as stale and require re-review.

Stale targets prevent fixes from being applied to the wrong text, which can occur when files are edited between the review snapshot and fix application.

---

## Example Finding

```
id: DR-023
location: docs/setup.md:15-17
rule: WR-008
severity: major
profile: procedure
evidence: |
  Create the configuration file and set the environment variable.
  Then run the setup script.
reason: |
  Step combines two required actions ("Create...file" and "set...variable")
  into a single step. Per WR-008 (Procedural clarity), each step must contain
  a single action. Applicable profile: procedure.
suggested_action: |
  Split into two steps:
  Step 1: Create the configuration file at /etc/app/config.yaml.
  Step 2: Set the environment variable DB_HOST to the database hostname.
fix_safety: safe
```
