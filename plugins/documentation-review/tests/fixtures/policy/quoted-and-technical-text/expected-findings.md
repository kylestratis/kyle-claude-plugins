# Expected Findings: Quoted and Technical Text

## Expected findings

No findings expected

## Protected text

WR-007 (Source fidelity) preserves each exact source span below:

- `README.md:authorization_token_header`: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- `README.md:oauth_term`: `OAuth 2.0`
- `README.md:oauth_url`: `https://tools.ietf.org/html/rfc6749`
- `README.md:design_quote`: `"A task is a unit of executable work that contains one or more steps, each of which runs in an isolated environment."`
- `README.md:task_id_identifier`: `` `task_id` ``
- `README.md:workflow_id_identifier`: `` `workflow_id` ``
- `README.md:execution_context_identifier`: `` `execution_context` ``
- `README.md:request_command`: `GET /api/v2/tasks/12345/status HTTP/1.1`
- `README.md:host_header`: `Host: api.example.com`
- `README.md:request_authorization_header`: `Authorization: Bearer TOKEN`
- `README.md:function_identifier`: `` `execute_workflow()` ``
- `README.md:type_identifier`: `WorkflowConfig`
- `README.md:literal`: `300`
- `README.md:function_signature`: `execute_workflow(config: WorkflowConfig, timeout: int = 300) -> ExecutionResult`

## Expected zero-finding regions

- `README.md:7-13`: WR-007 protects the complete Authorization header, OAuth 2.0 technical term, and URL.
- `README.md:17`: WR-007 protects the exact quotation, including its quotation marks.
- `README.md:19-22`: WR-007 protects the exact code identifiers.
- `README.md:26-32`: WR-007 protects the complete request command and both HTTP headers.
- `README.md:38-42`: WR-007 protects the function identifier, type identifier, literal, and complete function signature.
