# Expected Findings: Repetitive Comment

## Expected findings

id: DR-001
location: example.py:7
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Iterate through each item
  for item in items:
reason: |
  WR-009 (Repetitive comment) flags comments that only narrate visible control flow or repeat adjacent code. This comment states "Iterate through each item" but the for-loop syntax already clearly shows iteration. The comment adds no information beyond what the code itself communicates. Applicable profile: comment.
suggested_action: |
  Consider removing this comment unless it conveys non-obvious intent. For example, if the iteration order matters for correctness, or if a specific performance characteristic is important, document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-002
location: example.py:9
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Add the item value to the total
  total += item["value"]
reason: |
  WR-009 (Repetitive comment) flags comments that only narrate adjacent code. This comment "Add the item value to the total" merely restates what the += operation visibly performs. The code structure is self-explanatory. The comment narrates the control flow without providing rationale or non-obvious context. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "assumes item always has a 'value' key", "ignores missing values"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-003
location: example.py:18
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Loop through tasks
  for task in tasks:
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible control flow. "Loop through tasks" merely restates the for-loop's evident behavior. The comment adds no insight. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If the loop has non-obvious semantics (e.g., "processes tasks in submission order", "skips blocked tasks"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-004
location: example.py:20
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Check if task is active
  if task.get("status") == "active":
reason: |
  WR-009 (Repetitive comment) flags comments that narrate adjacent code. "Check if task is active" repeats what the if-condition visibly does. The code structure is clear. The comment does not explain the rationale for checking this field or the consequence of the check. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "only 'active' tasks can be scheduled", "ignores 'paused' tasks"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-005
location: example.py:22
rule: WR-009
severity: minor
profile: comment
evidence: |
  # If active, append to the active list
  active.append(task)
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible control flow. "If active, append to the active list" restates the append operation without adding insight. The code structure is self-evident. The comment does not explain the filtering strategy or the data structure choice. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "maintains insertion order", "active list cannot exceed 1000 items"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-006
location: example.py:25
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Return the filtered list
  return active
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible control flow. "Return the filtered list" merely restates what the return statement does. The code structure is clear. The comment does not explain what "filtered" means or the expected properties of the returned list. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "returns tasks in original order", "filters by active status only"), document that in the docstring instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-007
location: example.py:38
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Create workers
  for i in range(worker_count):
reason: |
  WR-009 (Repetitive comment) flags comments that narrate control flow. "Create workers" merely restates what the for-loop does. The comment adds no context about the worker creation strategy or the loop's purpose. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "worker IDs start at 0", "each worker is independently initialized"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-008
location: example.py:40
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Add worker to the pool
  workers.append(worker)
reason: |
  WR-009 (Repetitive comment) flags comments that narrate adjacent code. "Add worker to the pool" repeats what the append visibly does. The comment does not explain the pool management strategy or why appending is the right operation. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "workers are stored in FIFO order", "pool size must equal worker_count"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

## Protected text

- `example.py:docstring_1`: "Calculate the sum of item values."
- `example.py:docstring_2`: "Filter tasks by active status."
- `example.py:docstring_3`: "Initialize a pool of workers."

## Expected zero-finding regions

- `example.py:3-4`: Docstring context. Docstrings document observable contract, not code narration. No WR-009 findings.
- `example.py:14-16`: The filter_active_tasks function docstring is appropriate contract documentation. Not a repetitive comment.
- `example.py:30-36`: Function docstring and parameter documentation. These document the interface contract, not narrate code. No WR-009 findings.
