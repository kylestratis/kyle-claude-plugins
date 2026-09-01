# Skill Documentation: Advanced Workflow Orchestration

This skill uses a run plan to control conditional branching and parallel execution paths.

## Overview

Use this skill to manage workflows. The usage instructions call the run plan an execution blueprint. Pass configuration to the `execute_workflow` function.

## Parameters

- `workflow_config`: The workflow configuration to execute
- `timeout`: How long to wait (in seconds) for completion
- `retries`: How many retries are allowed for failed steps

## Output

The skill returns a result object containing execution status and metrics.

## Example

To execute a workflow:

```python
result = execute_workflow(config, timeout=300)
```

This will run the workflow to completion or timeout.
