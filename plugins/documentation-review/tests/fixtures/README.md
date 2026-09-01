# Documentation Review Policy Fixtures

This directory contains repository-shaped test scenarios for the documentation review policy. Each scenario isolates a specific observable behavior defined by the writing rules, surface profiles, and fix-safety contract.

## Fixture Contract

Each scenario follows this structure:

- **`input/`** — A minimal directory acting as the repository root, containing the text to be reviewed.
- **`expected-findings.md`** — A document that describes the expected review findings.

### expected-findings.md Structure

Every `expected-findings.md` file contains exactly these three top-level sections:

#### ## Expected findings

A list of findings in the order they would appear in a review report. Each finding includes:

- `id`: Stable review-local identifier (`DR-001`, `DR-002`, etc.)
- `location`: File path and line number(s) (`file:line` or `file:start-end`)
- `rule`: Writing rule identifier (`WR-001`, `WR-002`, etc.)
- `severity`: One of `critical`, `major`, or `minor`
- `profile`: Text-surface profile (`documentation`, `procedure`, `prompt`, `docstring`, `comment`, `historical-record`, or `general`)
- `evidence`: Exact quoted text from the input
- `reason`: Evidence-backed explanation and controlling policy
- `suggested_action`: Replacement or corrective action
- `fix_safety`: One of `safe`, `review-required`, or `report-only`

If no findings are expected, place the literal text `No findings expected` under this heading.

#### ## Protected text

A list of content regions that must remain unchanged. Format:

```
- `file:region`: exact quoted text
```

Each entry describes a specific region that the finding's fix-safety class or the applicable rule protects. Examples:

- `README.md:command`: `docker run -d --name app myimage`
- `CHANGELOG.md:date`: `2026-08-31`
- `example.py:identifier`: `def calculate_value(x)`

Protected text is preserved byte-for-byte during review.

#### ## Expected zero-finding regions

Regions where no findings should be reported, even if they contain patterns similar to the finding's condition. Format:

```
- `file:region`: reason for no finding
```

Examples:

- `README.md:10-12`: Historical record; dates protected by WR-012
- `example.py:docstring`: Necessary types and signatures are not redundant

Zero-finding regions enforce that profile protections and safety constraints suppress false positives.

---

## Scenarios

### terminology

**Objective:** Verify that `WR-001` (Consistent terminology) flags two terms demonstrably naming the same object.

**Input:** A README demonstrating mixed terminology for one concept.

**Expected:** One finding citing `WR-001` with exact quoted evidence of both terms.

### repository-precedence

**Objective:** Verify that applicable repository directives (e.g., `CLAUDE.md`) override bundled writing rules per precedence rules.

**Input:** Two files: `CLAUDE.md` establishing a repository term preference, and `README.md` using a different term.

**Expected:** One `WR-001` finding whose reason cites the repository directive as the controlling precedence tier 1 source.

### historical-provenance

**Objective:** Verify that `WR-012` (Protected provenance) protects necessary dates, versions, ticket references, and authorship in historical records.

**Input:** A CHANGELOG.md with required metadata (dates, version numbers, ticket references, authorship).

**Expected:** All protected metadata is listed under "Protected text". No findings reported for their presence, as WR-012 protects them.

### quoted-and-technical-text

**Objective:** Verify that `WR-007` (Source fidelity) protects commands, URLs, identifiers, literals, technical terms, and quotations.

**Input:** A README containing exact quotations, shell commands, identifiers, URLs, and technical terms.

**Expected:** All protected content is listed under "Protected text", with `WR-007` cited in the reason. No findings change any of this content.

### ticket-only-rationale

**Objective:** Verify that `WR-005` (Ticket-only explanation) flags when a ticket reference substitutes for a lasting explanation.

**Input:** A Python file with a comment citing only a ticket number without explanation.

**Expected:** One finding citing `WR-005` with `fix_safety: report-only`. No invented replacement.

### repetitive-comment

**Objective:** Verify that `WR-009` (Repetitive comment) flags comments that narrate visible control flow.

**Input:** A Python file with an inline comment repeating adjacent code semantics.

**Expected:** One finding citing `WR-009`. The suggestion indicates that deletion requires independent verification.

### contract-poor-docstring

**Objective:** Verify that `WR-010` (Contract-poor docstring) flags docstrings that only repeat the function name, signature, or types.

**Input:** A Python file with a Google-style docstring that repeats function name, signature, and parameter types without contract details.

**Expected:** One finding citing `WR-010` with `fix_safety: report-only`. No invented contract details.

### mixed-profiles

**Objective:** Verify that the correct profile is assigned to each finding and that protected content in historical records does not trigger false positives.

**Input:** A SKILL.md (prompt profile), CHANGELOG.md (historical-record profile), and example.py (docstring and comment profiles).

**Expected:** Findings reflect each input's profile. No false positives in the CHANGELOG.

---

## Coverage Requirements

Every scenario is self-contained. A failure in one scenario must not invalidate others. Scenarios are designed to isolate specific rule behaviors without requiring the full review skill implementation.

The fixtures use original test data (not copied from standards or source materials) to verify observable behavior.
