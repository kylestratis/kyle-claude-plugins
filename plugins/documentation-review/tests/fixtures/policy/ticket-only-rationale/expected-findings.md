# Expected Findings: Ticket-Only Rationale

## Expected findings

id: DR-001
location: example.py:9
rule: WR-005
severity: major
profile: comment
evidence: |
      # See issue #1234 for context
reason: |
  WR-005 (Ticket-only explanation) applies because the comment gives only issue #1234 as context. A reader cannot recover the lasting reason from the source.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Preserve #1234 and ask the author for the missing lasting reason before revising the comment.
fix_safety: report-only

id: DR-002
location: example.py:17
rule: WR-005
severity: major
profile: comment
evidence: |
              # refs #3892
reason: |
  WR-005 (Ticket-only explanation) applies because the comment gives only ticket #3892. It does not explain the return decision.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Preserve #3892 and ask the author for the missing reason for this return before revising the comment.
fix_safety: report-only

id: DR-003
location: example.py:25
rule: WR-005
severity: major
profile: comment
evidence: |
      # This validation was updated per ticket #892 (see the discussion thread for rationale)
reason: |
  WR-005 (Ticket-only explanation) applies because the comment sends the reader to ticket #892 and its discussion instead of stating what changed and why.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Preserve #892 and ask the author what validation change and lasting reason the comment must record.
fix_safety: report-only

## Protected text

WR-005 preserves these exact ticket references as provenance:

- `example.py:ticket_1234`: `#1234`
- `example.py:ticket_3892`: `#3892`
- `example.py:ticket_892`: `#892`

## Expected zero-finding regions

- `example.py:1-8`: The function declaration and docstring provide no ticket-only explanation.
- `example.py:10-16`: The code between the first two ticket comments contains no documentation surface.
- `example.py:18-24`: The return path, next declaration, and observable validation docstring contain no ticket-only explanation.
- `example.py:26-29`: The validation implementation contains no documentation surface.
