# Expected Findings: Contract-Poor Docstring

## Expected findings

id: DR-001
location: example.py:3-8
rule: WR-010
severity: minor
profile: docstring
evidence: |
  """Process data.
  
  Args:
      data: Data to process
  """
reason: |
  WR-010 (Contract-poor docstring) flags docstrings that only repeat a declaration's name, signature, parameters, or declared types without documenting observable contract. This docstring repeats the function name "process_data" and merely restates the parameter "data" without explaining what processing occurs, what output to expect, what errors might occur, or when to use this function. The docstring lacks contract details. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must provide observable contract details, such as: what transformations occur, what the function returns, what happens if data is invalid, whether this function modifies input in-place, and any performance or side-effect considerations. Inventing these details would be incorrect.
fix_safety: report-only

id: DR-002
location: example.py:12-19
rule: WR-010
severity: minor
profile: docstring
evidence: |
  """Validate the input dictionary.
  
  Args:
      input_dict: A dictionary to validate
      
  Returns:
      A boolean
  """
reason: |
  WR-010 (Contract-poor docstring) flags docstrings that only restate parameters and return types without documenting observable contract. This docstring repeats the function name "Validate the input dictionary" and lists parameter types (dict) and return type (bool) but does not explain what validation rules are applied, what constitutes a valid dictionary, what happens when validation fails, or when the function returns True vs. False. The docstring lacks contract details. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must explain the actual validation rules: what fields are required, what constraints must be satisfied, what makes input valid or invalid, and when the function returns True vs. False. Inventing validation rules would be incorrect.
fix_safety: report-only

id: DR-003
location: example.py:24-32
rule: WR-010
severity: minor
profile: docstring
evidence: |
  """Execute workflow with config, timeout, and retries.
  
  Args:
      config: Workflow configuration object
      timeout: Timeout value for execution
      retries: Number of retries
      
  Returns:
      Execution result
  """
reason: |
  WR-010 (Contract-poor docstring) flags docstrings that only restate function names and parameters without documenting observable contract. This docstring repeats the function name and lists parameters and return type but does not explain what the function does, what workflow configuration must contain, what the timeout parameter affects, what retries means (retries of what, under what failure conditions), what errors might occur, whether the function blocks or returns asynchronously, or what an "execution result" contains. The docstring lacks contract details. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must document the actual behavior: what happens with the config, what the timeout duration affects, when and how retries are attempted, what the function returns in success vs. failure cases, whether the call blocks, and what exceptions might be raised. Inventing this behavior would be incorrect.
fix_safety: report-only

id: DR-004
location: example.py:35-51
rule: WR-010
severity: minor
profile: docstring
evidence: |
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
  WR-010 (Contract-poor docstring) flags docstrings that lack observable contract details. This docstring's opening sentence "Apply a filter to items" merely repeats the function name. The docstring then enumerates what a good docstring would include (filtering strategy, predicate behavior, order preservation, None handling, in-place vs. copy), but the actual Args and Returns sections only restate parameter names and types without answering any of those questions. The docstring fails to document the actual contract. Applicable profile: docstring.
suggested_action: |
  No automatic action possible; requires investigation and user judgment. The author must answer the questions the docstring itself raises: What filtering strategy does this function apply? What should predicate do? Is order preserved? What happens with None predicate? Does this function modify items or return a new list? Inventing these details would be incorrect.
fix_safety: report-only

## Protected text

- `example.py:function_names`: Function names "process_data", "validate_input", "execute_workflow", "apply_filter"
- `example.py:parameter_names`: Parameter names "data", "input_dict", "config", "timeout", "retries", "items", "predicate"
- `example.py:type_hints`: Type hints "dict", "bool", "Sequence", etc.

## Expected zero-finding regions

- `example.py:51`: Return statement. While the docstring is poor, the return statement's semantics are visible in code. No additional WR-010 finding.
