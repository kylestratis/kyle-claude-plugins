# Writing Rules Reference

## Scope

This catalogue defines twelve foundational rules for reviewing technical documentation, source code comments, and procedural prose. Each rule targets a specific class of clarity, correctness, or maintainability issues. The rules apply consistently across documentation, procedures, prompts, docstrings, comments, and historical records, with surface-profile-specific adjustments and protections documented separately.

## Disclaimer

This guidance uses general controlled-language and simplified-English principles, including concepts inspired by ASD-STE100 Issue 9. It is not an ASD-STE100 implementation, is not endorsed by ASD, and does not claim compliance. It does not reproduce the ASD-STE100 rules or controlled vocabulary.

---

## WR-001 Consistent terminology

### Applies to

General prose, documentation, procedures, prompts, docstrings, and comments where technical concepts must be identifiable across the reviewed text.

### Evidence required

Flag two or more distinct terms that demonstrably refer to the same concept. Quote every variant found. List the locations where each variant appears. Establish the canonical term from context, usage frequency, or applicable directive.

### Severity

major

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. The reviewed text uses two or more terms interchangeably for one concept.
2. Each term appears in a complete, retrievable location.
3. Context or usage patterns establish that they name the same thing.

### Do not flag

- Synonyms used intentionally for stylistic variety in narrative prose.
- Technical terms that are defined differently in different contexts or standards.
- Single instances where a term appears in a quote or external reference that must be preserved.
- Deliberate use of both British and American spelling variants (e.g., "colour" and "color") when documented.

### Example

**Noncompliant:**

The system offers two deployment approaches: "containerized environment" in the configuration guide (line 5), "Docker deployment" in the API documentation (line 23), and "containerized stack" in the runbook (line 47). The inconsistency makes it unclear whether these refer to the same mechanism.

**Compliant:**

The system offers a containerized deployment approach, referred to as "container deployment" throughout this guide. Legacy documentation may use "Docker deployment" to refer to the same feature; see the migration guide in `docs/migration/docker-to-containers.md`.

---

## WR-002 Requirement strength

### Applies to

General prose, documentation, procedures, prompts, and docstrings where implementation or operational expectations are stated.

### Evidence required

Identify the requirement statement and the strength word used: `must`, `should`, `may`, or equivalent. `must` means required, `should` means recommended, and `may` means optional. Quote the sentence. If the strength is ambiguous or missing, cite the context that establishes the correct strength. Require evidence from the implementation, specification, or applicable directive before proposing a change to the modality.

### Severity

major

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. A requirement uses a strength word (`must`, `should`, `may`, or unclear phrasing like "will", "can", "try to").
2. The strength contradicts the implementation, specification, or applicable directive.
3. The mismatch could misdirect implementation or operation.

### Do not flag

- Informational or narrative uses of `can` or `may` that do not state requirements (e.g., "You can run the tool in two ways").
- Historical or conditional statements where strength is not binding (e.g., "In version 1.0, you could configure X").
- Explicit caveats or guidance that acknowledges ambiguity (e.g., "The spec is unclear; in practice, you should...").

### Example

**Noncompliant:**

To use the API, you may authenticate using either JWT or session cookies. The implementation requires JWT and rejects session cookies with a 403 error.

**Compliant:**

To use the API, you must authenticate using JWT. Session cookies are not supported and will result in a 403 error.

---

## WR-003 Unambiguous references

### Applies to

General prose, documentation, procedures, prompts, docstrings, and comments where pronouns, demonstratives, or other referring expressions are used.

### Evidence required

Identify the referring expression (`it`, `this`, `that`, `these`, `the`, or similar) and its location. List the two or more candidate antecedents and explain why each is a plausible referent based on proximity, grammatical role, or prior context. Quote the ambiguous sentence.

### Severity

major

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. A pronoun or demonstrative has two or more plausible antecedents in the relevant reviewed context.
2. Removing the ambiguity requires the reader to infer meaning from context.
3. The ambiguity could lead to misunderstanding the intended subject or action.

### Do not flag

- Well-established referents in code examples or formulas where context is explicit.
- References clearly scoped by a nested list or numbered section.
- Demonstratives in headings or titles where brevity is intentional.

### Example

**Noncompliant:**

Install the database driver and configure the connection pool. It requires a restart of the application to take effect.

(Does "it" refer to the driver installation, the configuration, or the connection pool?)

**Compliant:**

Install the database driver and configure the connection pool. The configuration takes effect after the application restarts. No restart is required for driver installation alone.

---

## WR-004 Durable rationale

### Applies to

General prose, documentation, procedures, docstrings, and comments where reasoning or context is offered to justify a design choice, constraint, or recommendation.

### Evidence required

Identify the statement that lacks lasting context. Quote it. Explain what transient project context (deadline, temporary constraint, future refactor, prototype status) the text presumes. Do not invent a rationale; describe what is missing.

### Severity

major

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. The text refers to transient project state without stating a lasting reason.
2. Examples: "We decided to use X for now", "This is temporary", "Once the migration is complete", "Until we have budget for Y".
3. A reader cannot determine why the choice is necessary or safe without access to project history or meetings.

### Do not flag

- Explicit caveats that name the constraint (e.g., "For performance reasons during the initial release", "Until the new API is stable").
- Historical records that intentionally document past decisions without re-justifying them.
- Recommendations prefaced with explicit conditions (e.g., "If you need X, then use Y").

### Example

**Noncompliant:**

We use this lightweight library for now because it was faster to integrate at the time. Consider replacing it with a more robust alternative later.

**Compliant:**

We use this lightweight library because it has minimal dependencies and integrates with the existing module system. If you need more advanced features, see the migration guide in `docs/migration/heavy-library.md`.

---

## WR-005 Ticket-only explanation

### Applies to

General prose, documentation, procedures, docstrings, and comments where an explanation or decision rationale is replaced by a ticket reference.

### Evidence required

Identify the statement that references a ticket and offers no explanation. Quote it. Note the ticket reference (URL, ID, or link). Preserve the ticket reference as provenance in any revision; do not remove it.

### Severity

major

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. A statement refers to a ticket or issue (by ID, URL, or link) instead of providing a lasting explanation.
2. Examples: "See #1234 for details", "Tracked in PROJ-567", "This is fixed in PR #89".
3. A reader cannot understand the issue or decision without access to an external system.

### Do not flag

- References that supplement a complete explanation (e.g., "We use this pattern because of performance constraints documented in #1234").
- Explicit caveats in historical records that note the ticket as context (e.g., "See #1234 for the original issue that prompted this change").
- Links to specification or standard documents that are stable references.

### Example

**Noncompliant:**

The configuration format changed. See issue #1234.

**Compliant:**

The configuration format changed from YAML to JSON in version 2.0 to improve integration with the deployment pipeline. See issue #1234 for the original problem statement.

---

## WR-006 Durable links

### Applies to

General prose, documentation, procedures, and docstrings where external references or links are provided.

### Evidence required

Identify the link and its location. Quote the surrounding context. Explain why the link is problematic: it is broken, inaccessible without credentials or context, or used instead of essential local information. Preserve valid source links and their purpose.

### Severity

minor

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. A link is invalid, returns an error, or is private without explanation.
2. A link is used instead of summarizing essential local context.
3. The link is the only explanation of a procedure or decision.

### Do not flag

- Links to stable specifications, standards, or official documentation when the link supplements sufficient local context.
- Links in comments that reference issue trackers or version control as historical context.
- Private links when access requirements are explicitly documented.

### Example

**Noncompliant:**

For instructions, follow this guide: https://internal.company.com/guides/deploy-v2.html (accessible only on the internal network).

**Compliant:**

From the repository root, the operator runs `./deploy --environment production`. The operator confirms that the command prints `Deployment complete`. The valid internal deployment guide at https://internal.company.com/guides/deploy-v2.html provides troubleshooting details and requires access to the company network.

---

## WR-007 Source fidelity

### Applies to

All surfaces: general prose, documentation, procedures, prompts, docstrings, comments, and historical records that quote or reference external sources, code, or technical material.

### Evidence required

Identify the original source text and the reviewed version. Quote both. Explain how the meaning, technical accuracy, or usability has changed. Include commands, literals, identifiers, URLs, file paths, technical terms, and version information as applicable.

### Severity

critical

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. Quoted source text is altered, simplified, or reworded in a way that changes meaning.
2. Commands, literals, identifiers, URLs, or technical terms are changed from their original form.
3. The change could affect implementation, operation, or understanding of the source.

### Do not flag

- Formatting changes that preserve exact content (e.g., converting code blocks between Markdown and other formats).
- Explicit replacements where the original source is no longer valid and the change is documented as a migration.
- Intentional simplifications that are not represented as exact source, preserve technical meaning and every protected token, and are marked as simplified.

### Example

**Noncompliant:**

The configuration uses the `log_level` option, for example: `set loglevel = INFO` (original API uses `set log_level = INFO`).

**Compliant:**

The configuration uses the `log_level` option, for example: `set log_level = INFO`. (See the vendor documentation at `https://vendor.example.com/config/options.html` for the complete reference.)

---

## WR-008 Procedural clarity

### Applies to

Procedures, numbered instructions, runbooks, setup guides, and migration steps.

### Evidence required

Identify the problematic sentence and its line number. Quote it. Explain the issue: multiple required actions in one step, missing actor (who performs the action), or a warning placed after the affected action. Quote any related steps that provide context.

### Severity

major

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. A single step contains two or more required actions, regardless of punctuation, conjunctions, or clause structure.
2. The actor (user, system, tool) is unclear or missing.
3. A warning or prerequisite is placed after the action it affects instead of before.

### Do not flag

- Multiple actions in a single step when they are alternatives clearly marked as such.
- Actions in a nested list that logically depend on a parent step.
- Conditional warnings (e.g., "If X happens, check Y") that follow the action but clearly apply to it.

### Example

**Noncompliant:**

3. Create the directory, add the configuration file, and run the setup script. Do not run this if the directory already exists.

**Compliant:**

2. The operator verifies that the directory does not exist.

3. The operator creates the directory.

4. The operator adds the configuration file.

5. The operator runs the setup script.

---

## WR-009 Repetitive comment

### Applies to

Inline and block code comments that accompany or explain source code.

### Evidence required

Identify the comment and its location. Quote both the comment and the adjacent code. Explain how the comment repeats or narrates the visible code without adding rationale, invariant, or non-obvious consequence. Do not assume deletion is safe; note that removal must be verified independently.

### Severity

minor

### Default fix safety

review-required

### Finding condition

A finding occurs when:
1. A comment restates the visible meaning of adjacent code without explaining why the code is written that way.
2. The comment narrates control flow that is evident from the code structure (e.g., "check if x is zero", "loop through the list").
3. The comment does not provide rationale, invariant, constraint, or non-obvious consequence.

### Do not flag

- Comments that explain non-obvious performance implications or correctness constraints.
- Comments that document the purpose or contract of a function, even if they partially restate the signature.
- Comments that explain workarounds, historical decisions, or constraints.

### Example

**Noncompliant:**

```python
# Check if the value is greater than 10
if value > 10:
    result = value * 2
```

**Compliant:**

```python
# Values above 10 must be scaled for compatibility with the data model.
# See WR-004: Durable rationale for domain constraints.
if value > 10:
    result = value * 2
```

---

## WR-010 Contract-poor docstring

### Applies to

Docstrings and prose descriptions attached to source declarations (functions, classes, modules, methods).

### Evidence required

Identify the docstring and its location. Quote it. Explain how it only repeats the declaration's name, signature, parameter names, or declared types without adding purpose, observable behavior, side effects, errors, or other contract information. Do not invent missing contract details. Require source evidence before claiming that undocumented side effects, errors, or other behavior exists.

### Severity

minor

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. A docstring repeats the declaration's name, signature, parameters, or declared types.
2. The docstring adds no purpose, observable behavior, side effect, error, or other contract information beyond that declared information.

### Do not flag

- Docstrings that document non-obvious side effects or error conditions.
- Docstrings that explain the purpose of a declaration, even briefly.
- Docstrings in tutorials or teaching examples where repetition is pedagogical.
- Docstrings that omit side effects or errors when the reviewed source gives no evidence that such behavior exists or is contract-relevant.

### Example

**Noncompliant:**

```python
def process_data(input_file: Path, output_file: Path) -> None:
    """process_data(input_file: Path, output_file: Path) -> None."""
```

**Compliant:**

```python
def process_data(input_file, output_file):
    """Parse CSV input and apply transformation rules.

    Write transformed rows to output_file in JSON format, one object per line.
    Raises ValueError if the CSV header is missing or malformed.
    """
```

---

## WR-011 Unsupported style claim

### Applies to

All surfaces: general prose, documentation, procedures, prompts, docstrings, comments, and historical records where a style rule violation is claimed.

### Evidence required

Identify the claimed violation and the rule it invokes. Quote the evidence from the reviewed text and cite the applicable directive (repository writing directive, profile-specific rule, or committed style choice). Do not report a style preference as a rule violation without supporting evidence.

### Severity

major

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. A style claim is made without evidence from the text or an applicable directive.
2. A taste preference is presented as a violation of a rule.
3. The claimed rule does not appear in the applicable writing rules or repository directives.

### Do not flag

- Claims that cite specific rules from the applicable profile or writing rules.
- Style guidance that acknowledges its own limitation (e.g., "This is a preference, not a requirement").
- Claims that refer to documented repository style choices or conventions.

### Example

**Noncompliant:**

The sentence "The environment variable must be set before the system is configured" violates the active-voice rule.

**Compliant:**

The repository directive `docs/style/active-voice.md` requires active voice. The sentence "The environment variable must be set before the system is configured" is passive because the subjects receive the actions. Replace it with "Set the environment variable before you configure the system." This replacement preserves the required modality.

---

## WR-012 Protected provenance

### Applies to

Historical records, changelogs, release notes, ADR status and history sections, migration records, and incident records.

### Evidence required

Identify the content that lacks necessary provenance. Quote it. Cite evidence that the provenance exists in a source record, was removed in a revision, or is required to identify the historical event. Specify what necessary provenance is missing: a date, version identifier, ticket or issue reference, authorship, or source history. Preserve necessary provenance in any revision. Never infer a ticket, author, date, version, or other missing fact.

### Severity

critical

### Default fix safety

report-only

### Finding condition

A finding occurs when:
1. Evidence shows that a historical record omits necessary provenance that identifies when, why, or by whom an event or decision occurred.
2. Necessary provenance is present but a revision makes it unclear or incomplete.
3. The omission makes the record unintelligible without the identified source context.

### Do not flag

- Content that explicitly notes changes but intends to preserve the original information (e.g., "Superseded by v2.0; see v1.0 for original details").
- Intentional anonymization of authorship for public release, when documented.
- Summarized records that reference detailed records for full provenance.

### Example

**Source record:**

- Version 1.2.0, released 2026-08-15: Fixed connection retry logic for timeouts. See issue #2847.

**Noncompliant revision:**

- Fixed the connection retry logic to handle timeouts correctly.

**Compliant revision:**

- Version 1.2.0, released 2026-08-15: Fixed connection retry logic for timeouts. See issue #2847.

---

## Sources

- https://www.asd-europe.org/standards-specifications/simplified-technical-english/
- https://peps.python.org/pep-0257/
- https://google.github.io/styleguide/pyguide.html
- https://developers.google.com/tech-writing/one/active-voice
