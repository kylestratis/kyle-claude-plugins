# Expected Findings: Repository Precedence

## Expected findings

id: DR-001
location: README.md:3-19
rule: WR-001
severity: major
profile: documentation
evidence: |
  This guide describes how to use the workflow system for task orchestration.

  ## Submitting Tasks

  To submit a task to the workflow system:

  1. Prepare your job definition
  2. Submit the job to the scheduler
  3. Monitor the job status

  Tasks are distributed across available workers based on resource requirements and current load.

  ## Job Lifecycle

  Each task progresses through several states: pending, assigned, running, and complete. The job lifecycle ensures consistent processing and error handling.

  When a job fails, the system logs the failure and optionally retries based on your configuration.
reason: |
  WR-001 (Consistent terminology) applies because README.md uses "task" and "job" for executable units. Precedence tier 1 controls the canonical choice: CLAUDE.md:7-9 requires "work item" for executable units in new documentation.
suggested_action: |
  Replace each executable-unit use of "task" or "job" in README.md:3-19 with the corresponding singular or plural form of "work item". Keep unrelated wording unchanged.
fix_safety: review-required

## Protected text

The controlling repository directive is:

- `CLAUDE.md:7-9`:
  ```text
  In this repository, the preferred term for executable units in the workflow system is **"work item"**. This term emphasizes the data-centric model where items flow through the system. Alternative terms such as "task" or "job" may appear in external documentation or legacy comments but are not canonical in this repository.

  All new documentation and guides must use "work item" consistently when referring to executable units.
  ```

## Expected zero-finding regions

- `README.md:1`: The document title contains no executable-unit terminology.
