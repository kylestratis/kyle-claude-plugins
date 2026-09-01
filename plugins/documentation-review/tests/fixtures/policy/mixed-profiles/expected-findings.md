# Expected Findings: Mixed Profiles

## Expected findings

id: DR-001
location: SKILL.md:6
rule: WR-001
severity: major
profile: documentation
evidence: |
  "workflow orchestration" (line 1), "workflows" (line 3, 6), "execute_workflow" (line 6), and "workflow" (line 12) refer to the same concept but use mixed terminology. The opening says "workflow orchestration" but later switches between "workflow" and "workflows". Additionally, "configuration" (line 6) is used interchangeably with "workflow config" (line 7) without clear distinction.
reason: |
  WR-001 (Consistent terminology) requires consistent use of a single term per concept. The SKILL documentation uses multiple terms for the workflow concept. While minor variations are acceptable in prose, WR-001 flags patterns where the inconsistency could obscure whether sections refer to the same feature. Applicable profile: documentation.
suggested_action: |
  Choose canonical terms and apply consistently throughout: either "workflow" as the singular and "workflows" as the plural for the feature, and "workflow configuration" as the consistent term for config. This makes the documentation's scope and feature boundaries clearer.
fix_safety: review-required

id: DR-002
location: example.py:4-12
rule: WR-010
severity: minor
profile: docstring
evidence: |
  """Parse configuration.
  
  Args:
      config_dict: Configuration dictionary
  
  Returns:
      Configuration object
  """
reason: |
  WR-010 (Contract-poor docstring) flags docstrings that only repeat parameter names and return types without explaining observable contract. This docstring restates "Parse configuration" (the function name) and lists "config_dict" (parameter name) and return type but does not explain what parsing means, what output format to expect, what happens if config is invalid, or whether the function validates. The docstring lacks contract details. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must document the parsing behavior: what transformation is applied, what output structure is produced, what validation occurs, what errors might be raised if config is malformed.
fix_safety: report-only

id: DR-003
location: example.py:14
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Parse the dictionary
  parsed = WorkflowConfig()
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible code. "Parse the dictionary" merely restates what the assignment and WorkflowConfig() constructor suggest. The comment narrates the code without explaining why this parsing strategy is chosen or what it accomplishes. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "converts flat dictionary to hierarchical config", "validates required fields"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-004
location: example.py:16
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Set the configuration value
  parsed.set(key, value)
reason: |
  WR-009 (Repetitive comment) flags comments that narrate adjacent code. "Set the configuration value" merely restates what the .set() method call does. The comment does not explain why this iteration pattern is used or what configuration semantics are established. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "overrides default values", "validates before setting"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-005
location: example.py:21-29
rule: WR-010
severity: minor
profile: docstring
evidence: |
  """Execute a workflow step.
  
  Args:
      step: Step definition
      context: Execution context
      
  Returns:
      Step execution result
  """
reason: |
  WR-010 (Contract-poor docstring) flags docstrings that only restate parameter names and return types. This docstring repeats "Execute a workflow step" (function name) and lists parameter and return type but does not explain what execution does, what side effects occur, what happens on success vs. failure, what errors might be raised, or what "result" contains. The docstring lacks contract details. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must document the execution behavior: what actions are triggered, what data is returned, how errors are represented, what exceptions might be raised, whether execution is synchronous or asynchronous.
fix_safety: report-only

id: DR-006
location: example.py:31
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Initialize the step result
  result = StepResult()
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible code. "Initialize the step result" merely restates the StepResult() constructor call. The comment does not explain the result structure, what fields will be populated, or why this pattern is used. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "result must be mutable for error handling", "default success=False"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-007
location: example.py:35
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Execute step logic
  try:
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible code. "Execute step logic" merely states what the try-except block visibly does. The comment does not explain why try-except is used, what recovery strategy is applied, or what specific errors are expected. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "catches network timeouts and retries", "logs all exceptions"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-008
location: example.py:37
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Run the step's action
  outcome = context.run_action(step.action)
reason: |
  WR-009 (Repetitive comment) flags comments that narrate adjacent code. "Run the step's action" merely restates what context.run_action() does. The comment does not explain why run_action is chosen, what it returns, or what happens to the outcome. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "returns raw output to be structured below", "may raise TimeoutError"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

id: DR-009
location: example.py:42
rule: WR-009
severity: minor
profile: comment
evidence: |
  # Handle step failure
  result.success = False
reason: |
  WR-009 (Repetitive comment) flags comments that narrate visible code. "Handle step failure" restates what the except block does. The comment does not explain the failure handling strategy, what information is preserved, or what downstream consumers do with failed results. Applicable profile: comment.
suggested_action: |
  Consider removing this comment. If there is important context (e.g., "sets success=False but continues execution", "logs failure for retry logic"), document that instead. Deletion remains review-required unless independently verified safe.
fix_safety: review-required

## Protected text

Protected content in historical record is preserved by WR-012 (Protected provenance):

- `CHANGELOG.md:version_1.2.0`: Version "[1.2.0]"
- `CHANGELOG.md:date_1.2.0`: Release date "2026-08-30"
- `CHANGELOG.md:author_1.2.0`: Author "maintenance@example.com"
- `CHANGELOG.md:pr_521`: Pull request reference "#521"
- `CHANGELOG.md:pr_521_date`: Review date "2026-08-28"
- `CHANGELOG.md:ticket_456`: Ticket reference "#456"
- `CHANGELOG.md:adr_0042`: Architecture decision reference "ADR-0042"
- `CHANGELOG.md:adr_0042_date`: ADR date "2026-08-15"
- `CHANGELOG.md:version_1.1.5`: Version "[1.1.5]"
- `CHANGELOG.md:date_1.1.5`: Release date "2026-07-20"
- `CHANGELOG.md:author_1.1.5`: Author "dev@example.com"

- `SKILL.md:function_name`: Function name "`execute_workflow`"
- `example.py:class_names`: Class names "WorkflowConfig", "StepResult"
- `example.py:method_names`: Method names "run_action", "set"

## Expected zero-finding regions

- `CHANGELOG.md:1-35`: Historical record profile. Dates, versions, ticket references, and authorship are protected by WR-012. No findings should be reported for the presence of this metadata in a historical record.

- `SKILL.md:16-18`: Code example. Commands in code examples are protected by WR-007. No findings for the function call.

- `example.py:43`: The result.error assignment. This is code implementation, not documentation. No docstring or comment finding.
