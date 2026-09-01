# Expected Findings: Contract-Poor Docstring

## Expected findings

id: DR-001
location: example.py:3-8
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def process_data(data):
      """Process data.

      Args:
          data: Data to process
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the docstring repeats the declaration and parameter without adding purpose or observable contract information.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual transformation and observable return contract before revising the docstring.
fix_safety: report-only

id: DR-002
location: example.py:12-20
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def validate_input(input_dict: dict) -> bool:
      """Validate the input dictionary.

      Args:
          input_dict: A dictionary to validate

      Returns:
          A boolean
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the prose only restates the declaration, parameter type, and return type. It does not state the validation condition or when the result is true.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual validation rule and result conditions before revising the docstring.
fix_safety: report-only

id: DR-003
location: example.py:24-34
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def execute_workflow(config, timeout=None, retries=3):
      """Execute workflow with config, timeout, and retries.

      Args:
          config: Workflow configuration object
          timeout: Timeout value for execution
          retries: Number of retries

      Returns:
          Execution result
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the prose repeats the declaration and parameter names without defining the execution contract, parameter effects, or result.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual execution behavior, parameter semantics, and result contract before revising the docstring.
fix_safety: report-only

id: DR-004
location: example.py:39-55
rule: WR-010
severity: minor
profile: docstring
evidence: |
  def apply_filter(items, predicate):
      """Apply a filter to items.

      A good docstring would explain:
      - When to use this function (what filtering strategy it applies)
      - What the predicate parameter should do
      - How order is preserved
      - What happens if predicate is None
      - Whether the function modifies items in-place or returns a new list

      Args:
          items: Sequence of items to filter
          predicate: Filtering predicate

      Returns:
          Filtered items
      """
reason: |
  WR-010 (Contract-poor docstring) applies because the docstring lists unanswered contract questions, then repeats parameter and result labels without supplying the answers.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. Ask the author for the actual filter, predicate, ordering, mutation, and result contracts before revising the docstring.
fix_safety: report-only

## Protected text

Each value below is an exact contiguous source span:

- `example.py:function_process_data`: `process_data`
- `example.py:function_validate_input`: `validate_input`
- `example.py:function_execute_workflow`: `execute_workflow`
- `example.py:function_apply_filter`: `apply_filter`
- `example.py:parameter_data`: `data`
- `example.py:parameter_input_dict`: `input_dict`
- `example.py:parameter_config`: `config`
- `example.py:parameter_timeout`: `timeout`
- `example.py:parameter_retries`: `retries`
- `example.py:parameter_items`: `items`
- `example.py:parameter_predicate`: `predicate`
- `example.py:type_dict`: `dict`
- `example.py:type_bool`: `bool`

## Expected zero-finding regions

- `example.py:56`: The return expression is source code, not a docstring surface.
