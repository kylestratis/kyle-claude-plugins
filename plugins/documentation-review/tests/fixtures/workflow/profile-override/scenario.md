# Workflow Scenario: Profile Override

## Acceptance criteria under test

- `documentation-review.AC3.2`: A valid invocation profile overrides natural content classification and general bundled rules.
- `documentation-review.AC5.1`: The override changes findings, not file bytes, in review-only mode.

## Invocation arguments

```text
--scope repository --path docs/deploy.md --profile docs/deploy.md=procedure
```

## Simulated tool-result transcript

```text
Glob constrained to docs/deploy.md -> docs/deploy.md
Read docs/deploy.md ->
# Deployment

The deployment guide explains the release process.

Install the package and update `APP_CONFIG`. Then run `deploy --production`.

Natural classification -> documentation
Invocation profile mapping -> docs/deploy.md=procedure
Repository writing directives -> none applicable
```

Control run without the override:

```text
Invocation -> --scope repository --path docs/deploy.md
Natural classification -> documentation
Expected WR-008 findings -> none because WR-008 does not apply to documentation
```

## Required observable actions

- Classify the content naturally as `documentation`, then apply the explicit `procedure` override.
- Apply procedure protections before general rules and preserve `APP_CONFIG` and `deploy --production` exactly.
- Report one `WR-008` finding for multiple required actions in one procedural step.
- Set the finding profile to `procedure`, severity to `major`, and fix safety to `review-required`.
- Explain that invocation precedence tier 2 controls over the classified profile at tier 3 and general rules at tier 4.
- In the control run, report no `WR-008` finding.

## Forbidden actions

- Do not ignore the profile because the file looks like ordinary documentation.
- Do not let the override supersede source fidelity or an applicable repository directive.
- Do not rewrite command syntax, an environment variable, or action order.
- Do not edit the file.

## Expected report fields

- `scope: repository`
- `path_constraints: [docs/deploy.md]`
- `profile_overrides: [docs/deploy.md=procedure]`
- `natural_profile: documentation`
- `applied_profile: procedure`
- `controlling_policy: explicit invocation override, precedence tier 2`
- Complete finding fields: `id`, `location`, `rule`, `severity`, `profile`, `evidence`, `reason`, `suggested_action`, `fix_safety`
- `mode: review-only`

Expected finding core:

```text
id: DR-001
location: docs/deploy.md:5
rule: WR-008
severity: major
profile: procedure
evidence: Install the package and update `APP_CONFIG`. Then run `deploy --production`.
fix_safety: review-required
```

## Protected text and expected unchanged files

- Protected tokens: `APP_CONFIG` and `deploy --production`.
- Protected action order: install, update, then run.
- Expected unchanged file: `docs/deploy.md` must remain byte-identical.

## Exact failure and recovery output

No failure is injected. If the profile mapping does not match a discovered path, report:

```text
Profile override did not match a reviewed path: docs/deploy.md=procedure.
Recovery: correct the repository-relative path or path constraints and run the review again.
```
