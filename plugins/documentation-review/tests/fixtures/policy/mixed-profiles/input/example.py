#!/usr/bin/env python3

def parse_workflow_config(config_dict):
    """Parse configuration.
    
    Args:
        config_dict: Configuration dictionary
    
    Returns:
        Configuration object
    """
    # Parse the dictionary
    parsed = WorkflowConfig()
    for key, value in config_dict.items():
        # Set the configuration value
        parsed.set(key, value)
    return parsed


def execute_step(step, context):
    """Execute a workflow step.
    
    Args:
        step: Step definition
        context: Execution context
        
    Returns:
        Step execution result
    """
    # Initialize the step result
    result = StepResult()
    
    # Execute step logic
    try:
        # Run the step's action
        outcome = context.run_action(step.action)
        result.success = True
        result.data = outcome
    except Exception as e:
        # Handle step failure
        result.success = False
        result.error = str(e)
    
    return result
