# Expected Findings: Terminology

## Expected findings

id: DR-001
location: README.md:5-19
rule: WR-001
severity: major
profile: documentation
evidence: |
  "discrete units of work" (line 5), "tasks" (line 5), "work item" (line 8, 11), and "job" (line 11) all refer to the same concept: executable units in the system. The documentation uses four distinct terms for this single concept.
reason: |
  WR-001 (Consistent terminology) requires that a single concept use one term consistently throughout related documentation. The evidence shows four terms demonstrably naming the same atomic execution unit: "discrete units of work", "tasks", "work item", and "job". Using multiple terms obscures whether sections refer to the same feature or distinct features. Applicable profile: documentation.
suggested_action: |
  Select one canonical term (e.g., "task") and apply it consistently. The example suggests using "task" as the primary term:
  - Line 5: "Each job consists of" → "Each task consists of"
  - Line 8: "work item" → "task" 
  - Line 11: "work item" → "task"
  - Line 11: "work item status" → "task status"
  This makes the documentation more coherent and prevents confusion about whether multiple terms refer to different features.
fix_safety: review-required

## Protected text

- `README.md:1`: System name "Task Execution System"
- `README.md:command`: "Submit work items to the system"

## Expected zero-finding regions

- `README.md:14-18`: This is implementation guidance, not a terminology definition. The phrase "work items" here is protected as part of the API terminology, not redefinable in documentation.
