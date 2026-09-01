# Expected Findings: Mixed Profiles

## Expected findings

id: DR-001
location: SKILL.md:3-7
rule: WR-001
severity: major
profile: prompt
evidence: |
  This skill uses a run plan to control conditional branching and parallel execution paths.

  ## Overview

  Use this skill to manage workflows. The usage instructions call the run plan an execution blueprint. Pass configuration to the `execute_workflow` function.
reason: |
  WR-001 (Consistent terminology) applies because "run plan" and "execution blueprint" are nontechnical aliases for the same control concept. SKILL.md is a skill prompt, so the controlling profile is prompt. The protected `execute_workflow` identifier is not terminology evidence.
suggested_action: |
  Choose either "run plan" or "execution blueprint" as the canonical prompt term after review, then replace only the other alias. Preserve all technical identifiers.
fix_safety: review-required

id: DR-002
location: example.py:3-11
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def parse_workflow_config(config_dict):
      """Parse configuration.

      Args:
          config_dict: Configuration dictionary

      Returns:
          Configuration object
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the docstring repeats the declaration, parameter, and result label without defining observable parsing behavior.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual parsing and result contract before revising the docstring.
fix_safety: report-only

id: DR-003
location: example.py:12-13
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Parse the dictionary
      parsed = WorkflowConfig()
reason: |
  WR-009 (Repetitive comment) applies because the comment narrates the adjacent constructor assignment without adding rationale, an invariant, a constraint, or a non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-004
location: example.py:15-16
rule: WR-009
severity: minor
profile: comment
evidence: |
          # Set the configuration value
          parsed.set(key, value)
reason: |
  WR-009 (Repetitive comment) applies because the comment restates the adjacent method call without adding rationale, an invariant, a constraint, or a non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-005
location: example.py:20-29
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def execute_step(step, context):
      """Execute a workflow step.

      Args:
          step: Step definition
          context: Execution context

      Returns:
          Step execution result
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the docstring repeats the declaration, parameters, and result label without defining observable execution behavior.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual step execution and result contract before revising the docstring.
fix_safety: report-only

id: DR-006
location: example.py:30-31
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Initialize the step result
      result = StepResult()
reason: |
  WR-009 (Repetitive comment) applies because the comment narrates the adjacent constructor assignment without adding rationale, an invariant, a constraint, or a non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-007
location: example.py:33-34
rule: WR-009
severity: minor
profile: comment
evidence: |
      # Execute step logic
      try:
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent control-flow block.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-008
location: example.py:35-36
rule: WR-009
severity: minor
profile: comment
evidence: |
          # Run the step's action
          outcome = context.run_action(step.action)
reason: |
  WR-009 (Repetitive comment) applies because the comment restates the adjacent method call without adding rationale, an invariant, a constraint, or a non-obvious consequence.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

id: DR-009
location: example.py:39-41
rule: WR-009
severity: minor
profile: comment
evidence: |
      except Exception as e:
          # Handle step failure
          result.success = False
reason: |
  WR-009 (Repetitive comment) applies because the comment only narrates the adjacent exception path and assignment.
suggested_action: |
  Review whether the comment can be deleted without losing required context. Deletion remains review-required until independently verified safe.
fix_safety: review-required

## Protected text

WR-012 (Protected provenance) preserves each exact historical source span:

- `CHANGELOG.md:version_1.2.0`: `[1.2.0]`
- `CHANGELOG.md:date_1.2.0`: `2026-08-30`
- `CHANGELOG.md:author_1.2.0`: `maintenance@example.com`
- `CHANGELOG.md:pr_521`: `#521`
- `CHANGELOG.md:pr_521_date`: `2026-08-28`
- `CHANGELOG.md:ticket_456`: `#456`
- `CHANGELOG.md:adr_0042`: `ADR-0042`
- `CHANGELOG.md:adr_0042_date`: `2026-08-15`
- `CHANGELOG.md:version_1.1.5`: `[1.1.5]`
- `CHANGELOG.md:date_1.1.5`: `2026-07-20`
- `CHANGELOG.md:author_1.1.5`: `dev@example.com`

WR-007 (Source fidelity) preserves each exact technical source span:

- `SKILL.md:function_name`: `execute_workflow`
- `SKILL.md:example_command`: `result = execute_workflow(config, timeout=300)`
- `example.py:class_workflow_config`: `WorkflowConfig`
- `example.py:class_step_result`: `StepResult`
- `example.py:method_run_action`: `run_action`
- `example.py:method_set`: `set`

## Expected zero-finding regions

- `CHANGELOG.md:1-35`: The historical-record profile and WR-012 protect the necessary dates, versions, ticket references, authorship, and decision provenance.
- `SKILL.md:19-25`: WR-007 protects the exact code example and command syntax.
- `example.py:44`: This return statement is source code, not a documentation surface.
