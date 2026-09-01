#!/usr/bin/env python3

def calculate_total(items):
    """Calculate the sum of item values."""
    total = 0
    
    # Iterate through each item
    for item in items:
        # Add the item value to the total
        total += item["value"]
    
    # Return the total
    return total


def filter_active_tasks(tasks):
    """Filter tasks by active status."""
    active = []
    
    # Loop through tasks
    for task in tasks:
        # Check if task is active
        if task.get("status") == "active":
            # If active, append to the active list
            active.append(task)
    
    # Return the filtered list
    return active


def initialize_worker_pool(worker_count):
    """Initialize a pool of workers.
    
    Args:
        worker_count: Number of workers to create
    """
    workers = []
    
    # Create workers
    for i in range(worker_count):
        worker = Worker(id=i)
        # Add worker to the pool
        workers.append(worker)
    
    return workers
