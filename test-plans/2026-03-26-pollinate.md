# Human Test Plan: Pollinate Skills

**Generated:** 2026-03-27
**Implementation Plan:** docs/implementation-plans/2026-03-26-pollinate/
**Coverage:** 70/70 automated criteria PASS

## Prerequisites

- Claude Code installed with `kyle-claude-plugins` plugin directory configured
- A local project with established conventions (Python, JavaScript, Rust, or Go)
- Access to a public GitHub repository with a non-trivial feature
- One test project with `beads` and `deciduous` installed and initialized
- One test project WITHOUT `beads` or `deciduous` installed

## Phase 1: Minimal Same-Language Port (Local Source)

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open a Python project in Claude Code with `pyproject.toml`, `tests/`, and established conventions. | Project opens. |
| 2 | Run `/pollinate /path/to/another/python/project SomeClass.method` (feature under 100 lines). | Claude announces "I'm analyzing the source feature for cross-codebase porting." |
| 3 | Observe Step 1 output. | Source classified as "local filesystem path." Feature identifier recognized. |
| 4 | Observe Step 2 output (codebase-investigator dispatch). | Structured output: Feature Location, Feature Code, Dependencies (direct+transitive), Line Count. |
| 5 | Confirm no chunking prompt (feature under 100 lines). | No AskUserQuestion about chunks. Proceeds to Step 4. |
| 6 | Observe Step 4 (target convention analysis). | Convention Mapping Table and Dependency Mapping Table displayed. |
| 7 | Respond to Step 5 dependency swap prompts. Choose "Use target equivalent." | Decisions logged. |
| 8 | Respond to architectural adaptation prompts. Choose "Adapt to target style." | Decisions logged. |
| 9 | Respond to rigor flagging by selecting no chunks. | Proceeds to design doc generation. |
| 10 | Check `docs/design-plans/YYYY-MM-DD-pollinate-<slug>.md` created and committed. | File exists. Git log shows commit. |
| 11 | Verify design doc has all 9 sections. | Summary, Source Feature, Convention Mapping, Dependency Mapping, Architectural Adaptations, Acceptance Criteria, Implementation Phases, Final Verification Phase, Additional Considerations. |
| 12 | Verify Convention Mapping Table has non-empty Rationale column. | Each adaptation explains WHY. |
| 13 | Verify Final Verification Phase references `/pollinate-verify` not `/verify`. | Contains `/pollinate-verify --source <path> --task <id>`. |
| 14 | Verify handoff message with "IMPORTANT: Copy the command below BEFORE running /clear." | Command matches `/workflow-commands:plan @docs/design-plans/<filename> .` |
| 15 | Verify Implementation Phases reference same-language differential testing pattern. | References "Same-Language Differential Testing Pattern." |

## Phase 2: Cross-Language Port (Remote Source)

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open a JavaScript/TypeScript project. | Project opens. |
| 2 | Run `/pollinate https://github.com/some-org/some-python-repo some.module` (module >100 lines). | Source classified as "remote URL." |
| 3 | Observe clone operation (remote-code-researcher). | Repo cloned. SOURCE_PATH captured. |
| 4 | Observe chunking prompt (feature >100 lines). | AskUserQuestion with chunk table. Options: suggested/monolithic/custom. |
| 5 | Choose "Use suggested chunks." | Proceeds to convention analysis. |
| 6 | Observe both `codebase-investigator` and `combined-researcher` dispatched. | Convention and Dependency Mapping Tables show Python vs JS/TS. |
| 7 | Respond to dependency swap decisions with mix of choices. | Each decision logged with rationale. |
| 8 | Observe architectural adaptation prompts (sync-vs-async, exceptions-vs-Promises). | Trade-offs with performance/accuracy implications. |
| 9 | Verify design doc references cross-language patterns. | "Cross-Language Differential Testing Pattern (Test Vectors)." Additional Considerations: "Source cloned to `<path>`. Do not delete until `/pollinate-verify` completes." |
| 10 | Verify test vector JSON format and bridging strategy mentioned. | JSON with `name`, `input`, `expected_output`, `tolerance`. Python-to-JavaScript bridging. |

## Phase 3: Rigor Critical and Multi-Chunk

| Step | Action | Expected |
|------|--------|----------|
| 1 | Run `/pollinate /path/to/source large_feature --rigor critical` (>100 lines). | `--rigor critical` parsed. |
| 2 | Observe no rigor flagging AskUserQuestion appears. | All chunks automatically flagged critical. |
| 3 | Verify design doc Acceptance Criteria includes property-based testing for critical chunks. | "Execute property-based testing (100+ random test cases per property)." |

## Phase 4: Pollinate-Verify Execution

| Step | Action | Expected |
|------|--------|----------|
| 1 | After `/plan` + `/execute` for a pollinated feature, run `/pollinate-verify --source <path> --task <id>`. | Announces three-layer verification. |
| 2 | Observe Layer 1: Differential Testing. | Framework detected, differential tests located and run, structured results table. |
| 3 | If Layer 1 passes, observe Layer 2: Adversarial Hardening. | Edge-case inputs targeting float precision, string encoding, null semantics, integer overflow. |
| 4 | Observe cross-chunk interaction tests. | Tests exercise data flow across chunk boundaries. |
| 5 | Observe triage table per iteration. | Each finding: GENUINE DIVERGENCE, ACCEPTABLE DIFFERENCE, or FALSE POSITIVE. |
| 6 | If >75% false positives, confirm early termination. | "Exhaustion reached" message. |
| 7 | Observe Layer 3: Standard Verify. | `verifying` skill executes (tests, lint, format, code review). |
| 8 | Verify Three-Layer Verification Report. | All three layers, per-iteration breakdown, Known Acceptable Differences, overall status. |

## Phase 5: Critical Chunks in Adversarial Hardening

| Step | Action | Expected |
|------|--------|----------|
| 1 | Run `/pollinate-verify` after porting with `--rigor critical` chunks. | Layer 2 begins. |
| 2 | Observe property-based tests for critical chunks. | hypothesis/proptest/fast-check/gopter specs generated. |
| 3 | Observe minimum 2 iterations enforced for critical chunks. | Loop does not terminate after iteration 1 even if >75% FP. |

## Phase 6: Graceful Degradation (No Tracking Tools)

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open project WITHOUT beads or deciduous installed. | Project opens. |
| 2 | Run `/pollinate /path/to/source some_feature`. | Skill begins without errors. |
| 3 | Observe full analysis workflow (Steps 1-7). | All steps complete. No "command not found" errors. |
| 4 | Verify design doc generated and committed normally. | All 9 sections present. |
| 5 | Run `/pollinate-verify --source <path>`. | All three layers execute without tracking errors. |

## End-to-End: Full Pipeline Test

| Step | Action | Expected |
|------|--------|----------|
| 1 | In a project with beads+deciduous, run `/pollinate /path/to/source complex_feature`. | Beads epic created. Deciduous goal logged. |
| 2 | Complete all user decision prompts. | LEARNED comments added to beads epic. |
| 3 | Verify design doc generated. Copy handoff command. | Design doc committed. |
| 4 | Run `/clear`, paste and run `/plan` command. | Planning begins in fresh context. |
| 5 | Run `/execute` to implement all phases. | Differential tests written per phase. |
| 6 | Run `/pollinate-verify --source <path> --task <epic-id>`. | Three-layer verification executes. |
| 7 | Verify final report. | Comprehensive report. Beads task closed. Deciduous outcome logged. |
