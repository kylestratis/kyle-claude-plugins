# API Integration Guide

This guide explains how to integrate with the task execution platform using its REST API.

## Authentication

The API uses bearer token authentication. Include the token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

See the original OAuth 2.0 specification at https://tools.ietf.org/html/rfc6749 for details on bearer token semantics.

## Core Concepts

The platform defines several core entities. According to the original design spec: "A task is a unit of executable work that contains one or more steps, each of which runs in an isolated environment."

The system uses three identifiers internally:
- `task_id`: The unique identifier for a work item
- `workflow_id`: The identifier for a collection of related tasks
- `execution_context`: The runtime environment name

## Example Request

To query a task status, make a GET request to:

```
GET /api/v2/tasks/12345/status HTTP/1.1
Host: api.example.com
Authorization: Bearer TOKEN
```

The endpoint returns a JSON response with the current status field.

## Integration Pattern

When using the platform as a library, call the `execute_workflow()` function with the workflow configuration. The function signature is:

```python
execute_workflow(config: WorkflowConfig, timeout: int = 300) -> ExecutionResult
```

This call triggers background task processing and returns immediately.
