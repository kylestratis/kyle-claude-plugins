# Expected Findings: Terminology

## Expected findings

id: DR-001
location: README.md:7,11
rule: WR-001
severity: major
profile: documentation
evidence: |
  The system coordinates tasks across multiple workers. Each task executes independently on one assigned node.
  The API calls a task a work item. When you create a work item, the task dispatcher assigns it to an available worker. The worker then executes the work item inside a containerized environment.
reason: |
  WR-001 (Consistent terminology) applies because "task" and "work item" demonstrably name the same atomic object. README.md:11 explicitly states that the API calls a task a work item. No aggregate-to-member relationship is part of this finding.
suggested_action: |
  Choose either "task" or "work item" as the canonical term after review, then replace only the other alias. Preserve the documented execution model.
fix_safety: review-required

## Protected text

- `README.md:1`: `Task Execution System`

## Expected zero-finding regions

- `README.md:13-22`: This region uses "task" consistently and contains no competing alias.
