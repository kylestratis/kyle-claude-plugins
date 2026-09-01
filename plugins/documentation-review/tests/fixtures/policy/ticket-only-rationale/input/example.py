#!/usr/bin/env python3

def process_workflow(workflow_data):
    """Process a workflow and execute its steps.
    
    Args:
        workflow_data: Dictionary containing workflow configuration
    """
    # See issue #1234 for context
    config = parse_config(workflow_data)
    
    # Initialize the execution context
    context = ExecutionContext()
    
    # Execute each step
    for step in config.steps:
        result = execute_step(step, context)
        if not result.success:
            # refs #3892
            return None
    
    return context.results


def validate_workflow(workflow_data):
    """Validate workflow structure."""
    # This validation was updated per ticket #892 (see the discussion thread for rationale)
    required_fields = ["name", "steps", "timeout"]
    for field in required_fields:
        if field not in workflow_data:
            raise ValueError(f"Missing required field: {field}")
