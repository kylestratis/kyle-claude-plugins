#!/usr/bin/env python3

def process_data(data):
    """Process data.

    Args:
        data: Data to process
    """
    return transform(data)


def validate_input(input_dict: dict) -> bool:
    """Validate the input dictionary.

    Args:
        input_dict: A dictionary to validate

    Returns:
        A boolean
    """
    return len(input_dict) > 0


def execute_workflow(config, timeout=None, retries=3):
    """Execute workflow with config, timeout, and retries.

    Args:
        config: Workflow configuration object
        timeout: Timeout value for execution
        retries: Number of retries

    Returns:
        Execution result
    """
    # Implementation details...
    pass


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
    return [item for item in items if predicate(item)]
