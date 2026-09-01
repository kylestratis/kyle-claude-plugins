# Expected Findings: Quoted and Technical Text

## Expected findings

No findings expected

## Protected text

Protected content in this documentation is preserved by WR-007 (Source fidelity):

- `README.md:jwt_token`: JWT bearer token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
- `README.md:oauth_url`: URL reference "https://tools.ietf.org/html/rfc6749"
- `README.md:design_quote`: Quoted design specification "A task is a unit of executable work that contains one or more steps, each of which runs in an isolated environment."
- `README.md:task_id_identifier`: Code identifier "`task_id`"
- `README.md:workflow_id_identifier`: Code identifier "`workflow_id`"
- `README.md:execution_context_identifier`: Code identifier "`execution_context`"
- `README.md:api_endpoint`: HTTP request line "GET /api/v2/tasks/12345/status HTTP/1.1"
- `README.md:host_header`: HTTP header "Host: api.example.com"
- `README.md:function_signature`: Python function signature "execute_workflow(config: WorkflowConfig, timeout: int = 300) -> ExecutionResult"

## Expected zero-finding regions

- `README.md:6-11`: Authorization header with JWT token. The token value is an exact technical identifier and cannot be rewritten. Per WR-007, source fidelity and exact command syntax are protected.
- `README.md:14`: Quoted material from original design spec. Direct quotes from source material are protected by WR-007 and must not be altered or paraphrased.
- `README.md:16-20`: Code identifiers and technical terms. These are exact identifiers used in the actual system and cannot be changed. Per WR-007, identifier names are protected.
- `README.md:24-29`: API request example. HTTP request format, endpoint path, and headers are exact technical specifications. Per WR-007, commands and exact sequences cannot be changed.
- `README.md:33-35`: Python function signature. The exact types, parameter names, and return type must be preserved. Code signatures are protected by WR-007.
