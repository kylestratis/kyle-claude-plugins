# Expected Findings: Repetitive Comment

## Expected findings

id: DR-001
location: example.py:7-8
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Iterate through each item
      for item in items:
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent for loop and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-002
location: example.py:9-10
rule: WR-009
severity: minor
profile: comment
evidence: |
          # Add the item value to the total
          total += item["value"]
reason: |
  WR-009 (Repetitive comment) applies because the comment restates the adjacent addition and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-003
location: example.py:12-13
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Return the total
      return total
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent return statement and adds no contract information.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-004
location: example.py:20-21
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Loop through tasks
      for task in tasks:
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent for loop and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-005
location: example.py:22-23
rule: WR-009
severity: minor
profile: comment
evidence: |
          # Check if task is active
          if task.get("status") == "active":
reason: |
  WR-009 (Repetitive comment) applies because the comment restates the adjacent condition and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-006
location: example.py:24-25
rule: WR-009
severity: minor
profile: comment
evidence: |
              # If active, append to the active list
              active.append(task)
reason: |
  WR-009 (Repetitive comment) applies because the comment narrates the adjacent append operation and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-007
location: example.py:27-28
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Return the filtered list
      return active
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent return statement and adds no contract information.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-008
location: example.py:39-40
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Create workers
      for i in range(worker_count):
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent worker-creation loop and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-009
location: example.py:42-43
rule: WR-009
severity: minor
profile: comment
evidence: |
          # Add worker to the pool
          workers.append(worker)
reason: |
  WR-009 (Repetitive comment) applies because the comment restates the adjacent append operation and adds no rationale, invariant, constraint, or non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

## Protected text

- `example.py:docstring_1`: `Calculate the sum of item values.`
- `example.py:docstring_2`: `Filter tasks by active status.`
- `example.py:docstring_3`: `Initialize a pool of workers.`

## Expected zero-finding regions

- `example.py:3-4`: The function declaration and docstring state the function purpose and are outside WR-009.
- `example.py:16-17`: The function declaration and docstring state the function purpose and are outside WR-009.
- `example.py:31-36`: The function declaration and docstring describe the function and its parameter and are outside WR-009.
