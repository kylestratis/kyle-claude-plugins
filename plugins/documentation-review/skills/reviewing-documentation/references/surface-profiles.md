# Text-Surface Profiles

## Overview

Text-surface profiles classify prose by its context and function, enabling rules to be applied with appropriate emphasis and protection. Each profile defines which writing rules apply, what content must be preserved, and what structural clarity is essential. Best-effort language detection can classify only observed prose regions; a review must list the surfaces that it reviewed and must not claim complete language coverage.

---

## `general`

### Classification signals

Prose that does not fit a more specific profile: explanatory text, narrative prose, or generic guidance not tied to a procedure, declaration, or historical record.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-003 (Unambiguous references), WR-004 (Durable rationale), WR-005 (Ticket-only explanation), WR-006 (Durable links), WR-007 (Source fidelity), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Apply rules to achieve clarity and consistency.
- Transient context (e.g., "for now") must include a lasting reason or a note of the constraint.
- Avoid ambiguous pronouns; restate the subject if uncertain.

### Protected content

- Quoted passages from specifications, standards, or external sources.
- Example code or output snippets.
- URLs and references to stable sources.

### Example

**Compliant:**

To use the API, you must authenticate with an API key. Generate a key in your account settings under Security > API Keys. Include the key in the request header as `Authorization: Bearer YOUR_KEY`. For security, rotate your key every 90 days. See the security policy in `docs/security.md` for additional requirements.

**Noncompliant:**

To use the API, you can authenticate. Use an API key from Security > API Keys. The details are in the security policy.

(Missing requirement strength for "must", lacks specific header format, and insufficient context for reader action.)

### Coverage reporting

A review must list this profile and note which sections or regions received general profile review. Do not claim that all prose in a file received explicit review; identify the regions that were examined.

---

## `documentation`

### Classification signals

README files, API guides, architecture documents, design specifications, and user-facing or operator-facing guides. Text that explains systems, APIs, or procedures to audiences who need to understand purpose and usage.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-003 (Unambiguous references), WR-004 (Durable rationale), WR-005 (Ticket-only explanation), WR-006 (Durable links), WR-007 (Source fidelity), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Require consistent use of terms across the document and related guides.
- Requirement strength must be explicit: "must", "should", or "may".
- Explanations must be durable: replace ticket references with lasting context.
- Links must be stable and summarized with local context; do not expect readers to access external systems.

### Protected content

- Technical terms, API names, and identifiers as defined in the specification.
- Example code and output (preserve exact formatting and syntax).
- Quoted material from standards, specifications, or related documents.
- Version numbers and compatibility matrices.

### Example

**Compliant:**

The API supports three authentication methods: API keys, OAuth 2.0, and mutual TLS. API keys are suitable for backend services and short-lived processes; OAuth 2.0 is recommended for user-facing applications; mutual TLS is required for high-security environments. See Authentication in the API Reference for implementation details and code examples.

**Noncompliant:**

The API has three auth methods. Which one to use depends on your use case. See the docs.

(Vague terminology, no requirement strength, and insufficient guidance.)

### Coverage reporting

A review must identify which sections of the documentation were examined (e.g., "API Reference: Reviewed authentication methods section"; "Guides: Reviewed deployment and migration sections"). Note if certain sections were not reviewed.

---

## `procedure`

### Classification signals

Numbered instructions, runbooks, setup guides, migration steps, troubleshooting guides, and deployment procedures. Prose that prescribes a sequence of actions to accomplish a specific task.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-008 (Procedural clarity), WR-007 (Source fidelity), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Each step must contain a single required action; separate multiple actions into distinct steps.
- The actor (human, system, tool) must be explicit in each step.
- Prerequisites must precede the actions they affect; warnings must precede the dangerous action.
- Command names, option names, and ordered state transitions must be preserved exactly.
- Use active voice and direct commands (e.g., "Run the script" not "The script should be run").

### Protected content

- Command syntax and identifiers (preserve case and special characters).
- Option names and flags.
- File paths and environment variable names.
- URL and endpoint paths.
- Output or expected state descriptions that distinguish success from failure.

### Example

**Compliant:**

1. Verify that the database is running and accessible from your host.

2. Create a new configuration file at `/etc/myapp/config.yaml` with the template from `docs/config.template.yaml`.

3. Set the `DB_HOST` environment variable to the database hostname.

4. Run the initialization script: `./bin/init-db.sh --config /etc/myapp/config.yaml`. Wait for the output "Initialization complete".

5. Restart the application: `systemctl restart myapp`.

**Noncompliant:**

1. Ensure the database is ready and create a configuration file. Then set the environment variable and run the initialization script.

(Multiple actions in one step, unclear actor, and insufficient context for verification.)

### Coverage reporting

A review must list each procedure examined and note its location. For procedures with many steps, identify which steps received focused review (e.g., "Steps 1-5 reviewed in detail; steps 6-10 covered by WR-007").

---

## `prompt`

### Classification signals

Skills, commands, agent prompts, and repository directives that guide the behavior of tools, agents, or systems. Prose that prescribes what a system must do, its constraints, and its output contract.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-003 (Unambiguous references), WR-007 (Source fidelity), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Requirement strength must be explicit and consistent: use "must", "should", "may" as specified in RFC 2119.
- Scope must be clear: what the prompt applies to, what it does not apply to, and what happens outside its scope.
- Output contract must be explicit: what format, structure, or content is expected.
- Failure behavior must be documented: what the system should do if constraints cannot be met.
- Tool names, prompt variables, and quoted instructions must be preserved exactly.

### Protected content

- RFC 2119 strength words and their definitions.
- Tool names, command names, and identifiers.
- Prompt variables and their delimiters (e.g., `$VAR`, `<placeholder>`, `{template}`).
- Quoted instructions or constraints from external specifications.
- Example output that demonstrates the expected format.

### Example

**Compliant:**

## Goal

Review technical documentation and generate a report of findings.

## Requirements

- MUST identify findings with exact location, applicable rule, severity, and suggested action.
- SHOULD apply profiles to classify prose by its function (documentation, procedure, comment, etc.).
- SHOULD NOT report style preferences without supporting evidence.
- Failure: If critical inconsistencies are found, report them as blocking findings and do not suppress them.

## Output

A Markdown report with the structure defined in `docs/review-report-schema.md`.

**Noncompliant:**

Review documentation and generate findings. Identify issues and report them. Do not report preferences without evidence.

(Vague scope, no output contract, no failure behavior defined.)

### Coverage reporting

A review must identify the prompt or directive examined and note which sections (goals, constraints, output contract) received focus. Include any repository-specific directives or profiles that override the general prompt.

---

## `docstring`

### Classification signals

Prose descriptions attached to source code declarations: module docstrings, class docstrings, function docstrings, and method docstrings. Text that documents the purpose, contract, and usage of code.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-007 (Source fidelity), WR-010 (Contract-poor docstring), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Docstrings must document purpose, observable behavior, side effects, and errors; do not repeat the declaration's name or signature.
- Parameter names, types, and return types from the signature must not be restated unless they clarify non-obvious behavior.
- Use the language's docstring convention (Google style for Python, JSDoc for JavaScript, etc.).
- Do not invent missing behavior or side effects; flag docstrings that lack essential contract information as report-only findings.

### Protected content

- Signatures, type annotations, and identifiers exactly as declared.
- Exception and error type names.
- Example code that shows usage of the declaration.
- Quoted constraints or requirements from specifications.

### Example

**Compliant:**

```python
def find_user_by_email(email):
    """
    Retrieve a user record by email address.
    
    Performs a case-insensitive lookup in the user database.
    Returns None if no matching user is found.
    
    Args:
        email: A valid email string.
    
    Returns:
        A User object or None.
    
    Raises:
        ValueError: If email is None or an empty string.
        DatabaseConnectionError: If the database is unreachable.
    """
```

**Noncompliant:**

```python
def find_user_by_email(email):
    """Find a user by email. Returns a user or None."""
```

(Does not document side effects, error conditions, or non-obvious behavior like case-insensitivity.)

### Coverage reporting

A review must list the declarations examined (e.g., "Module docstring; functions: process_data, validate_input, export_results"). Note if certain declarations lacked docstrings or if docstrings were too brief to review meaningfully.

---

## `comment`

### Classification signals

Inline and block code comments that accompany or explain source code. Text that documents rationale, invariants, constraints, or non-obvious consequences within the code.

### Applicable rules

WR-001 (Consistent terminology), WR-004 (Durable rationale), WR-009 (Repetitive comment), WR-011 (Unsupported style claim)

### Profile-specific adjustments

- Comments must explain rationale, invariant, constraint, or non-obvious consequence; do not narrate visible code.
- Deletion of a comment must be review-required unless deletion is independently proven safe through testing or analysis.
- Comments that document workarounds or historical decisions must preserve the rationale; do not remove the explanation.
- Code semantics and behavior must not be inferred from comments; when a comment seems necessary to understand the code, the code likely needs refactoring.

### Protected content

- Code semantics and control flow (comments must not be deleted without independent verification).
- Workaround explanations and historical context.
- Constraints and invariants that the code enforces.

### Example

**Compliant:**

```python
# Exponential backoff with jitter prevents thundering herd 
# when retrying after a timeout. See PERF-123.
for attempt in range(max_retries):
    try:
        response = call_service()
        break
    except TimeoutError:
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        time.sleep(wait_time)
```

**Noncompliant:**

```python
# Check if attempts is less than max_retries
for attempt in range(max_retries):
    # Try to call the service
    try:
        response = call_service()
        # Break out of the loop on success
        break
    except TimeoutError:
        # Increment wait time exponentially
        wait_time = (2 ** attempt) + random.uniform(0, 1)
```

(Comments narrate visible control flow without explaining rationale or non-obvious behavior.)

### Coverage reporting

A review must list the code regions examined and identify which comments were reviewed (e.g., "Reviewed functions: process_event, cache_result; checked 8 comments for rationale and clarity"). Note if code lacked explanatory comments where rationale was non-obvious.

---

## `historical-record`

### Classification signals

Changelogs, release notes, ADR (Architecture Decision Record) status and history sections, migration records, incident reports, and version history documentation. Prose that documents past events, decisions, or changes with their context and provenance.

### Applicable rules

WR-001 (Consistent terminology), WR-002 (Requirement strength), WR-007 (Source fidelity), WR-012 (Protected provenance)

### Profile-specific adjustments

- All entries must use accurate past tense and correct historical context.
- Necessary dates, version numbers, ticket references, and authorship must be preserved and remain accurate.
- Changes to past records must preserve the original facts; corrections must be noted as amendments, not deletions.
- Source fidelity is critical: do not alter quoted decisions or cited reasoning.
- Summaries of past events must be consistent with detailed records; if summarizing, preserve the reference to the detailed record.

### Protected content

- Dates and version numbers (absolutely required; precision matters).
- Ticket and issue references (preserve identifiers and links where stable).
- Authorship and decision-maker names.
- Quoted decisions and reasoning from the time of the decision.
- Release notes and version tags exactly as released.

### Example

**Compliant:**

## Changelog

### Version 1.3.0 (2026-08-15)

- Fixed connection retry logic to handle timeouts correctly. Previously, the client would fail immediately when the server did not respond within 5 seconds. Now the client retries with exponential backoff (see issue #2847 for original problem description).
- Added support for mutual TLS authentication. Requires OpenSSL 1.1.1 or later.

(See the migration guide in `docs/migration/1.2-to-1.3.md` for upgrading from version 1.2.0.)

**Noncompliant:**

## Changelog

- Fixed connection retry timeout bug.
- Added TLS support.

(Missing dates, version numbers, ticket references, and context for what "fixed" means.)

### Coverage reporting

A review must identify the sections of historical records examined (e.g., "Changelog entries from version 1.0 through 1.3; all ADR status entries; migration guide for v1.2 to v1.3"). Note if certain time periods or sections were not reviewed. Do not claim complete historical accuracy; identify what was verified.

---

## Coverage Reporting Requirement

Best-effort language detection can classify only observed prose regions. A review must list the surfaces that it reviewed and must not claim complete language coverage.

A complete coverage report must include:
- Which profiles were applied (documentation, procedure, docstring, comment, historical-record, etc.).
- Which regions of the codebase were examined (file names, line ranges, or section names).
- Which profiles were not applicable and why (e.g., "binary files were not reviewed", "generated code was not reviewed").
- Confidence in the language detection (e.g., "Docstrings were reliably detected; comments were reviewed manually in 5 source files").
