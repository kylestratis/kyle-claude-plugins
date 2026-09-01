# Expected Findings: Ticket-Only Rationale

## Expected findings

id: DR-001
location: example.py:10
rule: WR-005
severity: major
profile: comment
evidence: |
  # See issue #1234 for context
reason: |
  WR-005 (Ticket-only explanation) flags when a comment or docstring cites a ticket reference that substitutes for a lasting explanation. This comment provides no rationale—only a ticket number. Future readers cannot understand why the code is structured this way without access to the ticket tracker. The comment lacks durable rationale. Applicable profile: comment.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must either:
  1. Provide a lasting explanation in the comment (e.g., "See issue #1234 for context. The config parser requires both nested and flat structures due to legacy API constraints."), or
  2. Replace the comment with a documented rationale that explains the decision without requiring external ticket access.
fix_safety: report-only

id: DR-002
location: example.py:20
rule: WR-005
severity: major
profile: comment
evidence: |
  # refs #3892
reason: |
  WR-005 (Ticket-only explanation) flags comments that cite only a ticket reference without explaining the decision or context. This comment provides no lasting rationale—only a ticket identifier. The comment lacks durable context. Applicable profile: comment.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must either:
  1. Explain the failure condition in the comment (e.g., "Return None if any step fails. See issue #3892 for retry policy discussion."), or
  2. Provide a documented reason for the return-None behavior that does not depend on ticket access.
fix_safety: report-only

id: DR-003
location: example.py:26
rule: WR-005
severity: major
profile: comment
evidence: |
  # This validation was updated per ticket #892 (see the discussion thread for rationale)
reason: |
  WR-005 (Ticket-only explanation) flags comments that delegate rationale to external sources (tickets, discussion threads) instead of providing durable explanation. This comment says the validation was updated "per ticket #892" but does not explain what changed or why. Readers cannot understand the update without accessing the ticket and discussion thread. The comment lacks lasting rationale. Applicable profile: comment.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must:
  1. Explain what was changed in the validation and why. For example: "This validation was updated to require 'timeout' field after discovering timeout-less workflows caused scheduler deadlocks (ticket #892)."
fix_safety: report-only

## Protected text

- `example.py:ticket_1234`: Ticket reference "#1234"
- `example.py:ticket_3892`: Ticket reference "#3892"
- `example.py:ticket_892`: Ticket reference "#892"

## Expected zero-finding regions

- `example.py:1-8`: The function docstring does not cite a ticket; it provides observable contract. No findings.
- `example.py:14-16`: The comment "Initialize the execution context" describes the code action, not a ticket reference. Not a WR-005 violation.
- `example.py:23-29`: The validate_workflow function's logic. The comment structure describes the validation, not ticket references. No WR-005 findings expected in this region.
