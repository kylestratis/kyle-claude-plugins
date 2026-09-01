# Expected Findings: Repository Precedence

## Expected findings

id: DR-001
location: README.md:5-19
rule: WR-001
severity: major
profile: documentation
evidence: |
  The README uses three distinct terms for the same concept:
  - "task" (line 5: "task orchestration", line 8: "Submitting Tasks", line 12: "Each task progresses")
  - "job" (line 9: "Prepare your job definition", line 10: "Submit the job", line 11: "Monitor the job status", line 19: "Each task...job lifecycle")
  
  The bundled writing rule WR-001 would flag this as inconsistent terminology. However, the repository directive in CLAUDE.md establishes "work item" as the canonical term for this concept.
reason: |
  WR-001 (Consistent terminology) ordinarily flags multiple terms for the same concept. However, per Fix Safety Policy precedence tier 1, the repository-specific directive in CLAUDE.md supersedes the bundled rule. CLAUDE.md explicitly designates "work item" as the preferred term. The README's use of "task" and "job" violates the repository standard, not just general consistency guidance. The controlling policy is the repository directive in CLAUDE.md:Terminology.
suggested_action: |
  Align the README with the repository directive by replacing "task" and "job" with "work item":
  - Line 5: "task orchestration" → "work item orchestration"
  - Line 8: "Submitting Tasks" → "Submitting Work Items"
  - Line 9: "job definition" → "work item definition"
  - Line 10: "the job" → "the work item"
  - Line 11: "the job status" → "the work item status"
  - Line 12: "Each task" → "Each work item"
  - Line 19: "job lifecycle" → "work item lifecycle"
fix_safety: review-required

## Protected text

- `CLAUDE.md:terminology_directive`: The repository directive establishing "work item" as canonical

## Expected zero-finding regions

- `README.md:1`: System name context, not subject to terminology rule
- `README.md:15-19`: This section's focus on system behavior is not affected by terminology choice
