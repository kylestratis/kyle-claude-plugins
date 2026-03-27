---
name: pollinate
description: Port a feature from another codebase with convention mapping and behavioral equivalence verification
user-invocable: false
---

# Pollinate

## Overview

Analyze a source feature, map it to target project conventions, and generate a design document for porting. Delegates implementation to the standard `/plan` → `/execute` pipeline, and verification to `/pollinate-verify`.

**Announce:** "I'm analyzing the source feature for cross-codebase porting."

## Arguments

`<source-path-or-url> <feature> [--rigor critical]`

- `<source>`: Local filesystem path or GitHub/git URL
- `<feature>`: Function name, module name, or natural language description
- `--rigor critical`: Flag specific chunks for elevated verification (property-based testing, extra adversarial iterations)

## Process

### Before Starting

```bash
# Verify tracking infrastructure
ls .beads/beads.db .deciduous/ || echo "Run /workflow-commands:project-init first"

# Create epic for feature extraction
bd create "Pollinate: Extract <feature> from <source>" -t epic -p 2

# Log goal with verbatim prompt
deciduous add goal "Port <feature> from <source> to this codebase" -c 80
```

### During Source Acquisition

#### Step 1: Parse Arguments

Detect source type and extract feature identifier:

**Source Type Detection:**
- Starts with `/`, `~`, or `.` → local filesystem path
- Starts with `https://github.com`, `git@`, or ends with `.git` → remote URL
- Otherwise → ask user via AskUserQuestion: "Is '<source>' a local path or GitHub URL?"

**Accepted Feature Identifiers:**
- Function name (e.g., `fetch_user`, `getUserData`)
- Module name (e.g., `auth`, `payment_processor`)
- Natural language description (e.g., "the user authentication flow")

**Optional flag:**
- `--rigor critical` → mark extracted chunks for elevated verification (property-based testing, adversarial iterations)

#### Step 2: Acquire Source & Extract Feature

**For Local Paths:**
Dispatch `ed3d-research-agents:codebase-investigator` with:

```
Your task: Extract a feature from the source codebase and return its complete dependency graph.

Input:
- Source path: <SOURCE_PATH>
- Feature identifier: <FEATURE_ID> (could be function name, module name, or natural language description)

Output: Structured response with these sections:

1. **Feature Location**
   - File path(s)
   - Line range (if applicable)
   - Programming language

2. **Feature Code**
   - Complete implementation (all non-library code)
   - Any inline documentation

3. **Direct Dependencies**
   - Imported functions/classes from same codebase
   - Parameters and their types
   - Return type

4. **Transitive Dependency Graph**
   - For each direct dependency, recursively trace its dependencies
   - Stop when reaching: standard library, third-party package, or circular reference
   - Format: Tree structure showing dependency depth

5. **External Dependencies**
   - Third-party libraries/frameworks used
   - Version constraints (if specified)
   - License types

6. **Line Count**
   - Total lines of feature code (including dependencies in same codebase)

CRITICAL INSTRUCTIONS:
- Accept function name, module name, or natural language description as feature identifier
- For natural language: search code comments, docstrings, and file structure to infer intent
- Trace recursively until hitting standard library or third-party package boundaries
- Report the complete transitive graph, not just direct imports
- If the feature is not found, ask clarifying questions about its name or location
```

**For Remote URLs:**
Dispatch `ed3d-research-agents:remote-code-researcher` with:

```
Your task: Clone a GitHub repository, extract a feature, and return its complete dependency graph.

Input:
- Repository URL: <REMOTE_URL>
- Feature identifier: <FEATURE_ID>

Output: Structured response with these sections:

1. **Feature Location**
   - File path(s)
   - Line range (if applicable)
   - Programming language

2. **Feature Code**
   - Complete implementation (all non-library code)
   - Any inline documentation

3. **Direct Dependencies**
   - Imported functions/classes from same codebase
   - Parameters and their types
   - Return type

4. **Transitive Dependency Graph**
   - For each direct dependency, recursively trace its dependencies
   - Stop when reaching: standard library, third-party package, or circular reference
   - Format: Tree structure showing dependency depth

5. **External Dependencies**
   - Third-party libraries/frameworks used
   - Version constraints (if specified)
   - License types

6. **Line Count**
   - Total lines of feature code (including dependencies in same codebase)

7. **Clone Path**
   - The path where you cloned the repository (will be needed for later verification)

CRITICAL INSTRUCTIONS:
- Accept function name, module name, or natural language description as feature identifier
- For natural language: search code comments, docstrings, and file structure to infer intent
- Trace recursively until hitting standard library or third-party package boundaries
- Report the complete transitive graph, not just direct imports
- If the feature is not found, ask clarifying questions about its name or location
- After cloning to a temporary location, output the clone path so we can persist it for later use.
```

After agent returns, capture the source path:
- **Local paths:** Record as `SOURCE_PATH = <original-path>`
- **Remote clones:** Record as `SOURCE_PATH = <clone-path>` (from agent response)

**Store SOURCE_PATH in a variable for later use in design doc generation.**

**Important for remote clones:** When generating the design doc in Phase 4, include in "Additional Considerations": "Source cloned to `<SOURCE_PATH>`. Do not delete until `/pollinate-verify` completes."

#### Step 3: Chunk Decomposition & Deciduous Logging

If feature ≤100 lines, skip to deciduous logging.

If feature >100 lines:

1. Analyze the dependency graph for natural decomposition boundaries:
   - Separate concerns (e.g., validation logic vs. API calls)
   - Independent subfeatures that could be implemented separately
   - Cohesive modules within the feature

2. Present chunk table to user via AskUserQuestion:

```
The extracted feature is <N> lines and has complex dependencies.

Suggested decomposition:

| Chunk | Lines | Dependencies | Notes |
|-------|-------|--------------|-------|
| <name1> | <L> | <deps> | <desc> |
| <name2> | <L> | <deps> | <desc> |
| ... | | | |

Choose one:
- "Use suggested chunks" → proceed with decomposition
- "Extract as monolithic feature" → treat entire feature as one unit
- "Custom chunks: <chunk1>, <chunk2>, ..." → specify your own
```

3. **Log deciduous decisions** (final action in Step 3):

Log the extraction result:
```bash
deciduous add action "Extracted <feature> from <source>: <N> lines, <M> dependencies" -c 85
```

If feature >100 lines and chunking was performed, also log the decomposition decision:

**If user chose monolithic:**
```bash
deciduous add decision "Kept <feature> as monolithic unit: <N> lines, <M> dependencies" -c 80
```

**If user chose suggested chunks:**
```bash
deciduous add decision "Decomposed <feature> into <K> chunks: <chunk-names>" -c 80
```

**If user specified custom chunks:**
```bash
deciduous add decision "Decomposed <feature> into custom chunks: <custom-names>" -c 80
```

These logs capture the source analysis decisions for audit trail and future reference.

#### Step 4: Target Convention Analysis

Dispatch `ed3d-research-agents:codebase-investigator` against the current (target) project to extract conventions:

```
Your task: Analyze the target project's conventions and patterns.

Input:
- Current project path: . (current working directory)

Output: Structured response with these sections:

1. **Project Overview**
   - Primary programming language(s)
   - Runtime/framework (Node.js, Python 3.x, Java, etc.)
   - Package manager (npm, pip, cargo, maven, etc.)

2. **Naming Conventions**
   - Variable/function naming style (snake_case, camelCase, PascalCase)
   - File naming patterns
   - Class/type naming patterns

3. **Code Organization**
   - Import/require patterns
   - Module structure
   - Folder organization

4. **Error Handling**
   - Exception/error types used
   - Error handling patterns (try-catch, Result types, error returns, etc.)
   - Logging approach

5. **Asynchronous Patterns**
   - async/await, promises, callbacks, or channels
   - Concurrency primitives used
   - Streaming vs buffering patterns

6. **Testing Framework & Patterns**
   - Test framework used (pytest, Jest, Go testing, etc.)
   - Test file location convention
   - Mocking approach (mocks, stubs, fixtures, etc.)

7. **Configuration & Dependency Management**
   - How external dependencies are declared (package.json, requirements.txt, Cargo.toml, etc.)
   - Currently installed dependencies relevant to the ported feature
   - Version pinning strategy

CRITICAL INSTRUCTIONS:
- Provide concrete examples from the actual codebase
- List all dependencies installed in the project
- Focus on patterns that would affect feature porting
```

**For cross-language ports:** Additionally dispatch `ed3d-research-agents:combined-researcher` to research idiomatic equivalents:

```
Your task: Research language-idiomatic patterns for cross-language feature porting.

Input:
- Source language: <SOURCE_LANGUAGE> (from Step 2)
- Target language: <TARGET_LANGUAGE> (detected from Step 4 codebase-investigator)
- Feature type: <FEATURE_TYPE> (e.g., async I/O, data validation, ORM usage, etc.)

Output: For each source pattern identified, provide:

1. **Pattern Name & Source Example**
   - The pattern as used in <SOURCE_LANGUAGE>
   - Concrete code snippet from the extracted feature

2. **Target Language Idiomatic Equivalent**
   - How this pattern is typically expressed in <TARGET_LANGUAGE>
   - Current best practice (as of 2026)
   - Trade-offs vs source approach

3. **Library/Framework Recommendations**
   - Idiomatic library/framework in target language
   - Whether it's already installed in the target project
   - Version requirements

Examples to research:
- Async I/O: asyncio (Python) → async/await or Tokio (Rust)?
- Error handling: Exceptions (Python) → Result types (Rust)?
- Data structures: dict (Python) → HashMap (Rust)?
- Testing: pytest (Python) → Go testing or custom framework?

CRITICAL INSTRUCTIONS:
- Focus on patterns actually present in the extracted feature
- Prioritize idiomatic approaches over literal translations
- Include performance/maintainability implications
```

After agents return, build two comparison tables and present to user:

**Convention Mapping Table:**

Present this table in text format:

```
| Aspect | Source | Target | Adaptation Notes |
|--------|--------|--------|-----------------|
| Language | <source-lang> | <target-lang> | |
| Naming | <source-style> | <target-style> | Use target style: <example> |
| Error Handling | <source-error> | <target-error> | Map <source> exceptions to <target> errors |
| Async Model | <source-async> | <target-async> | Use target async/await pattern |
| Testing | <source-test> | <target-test> | Target uses <framework> with <mocking> |
| ... | ... | ... | ... |
```

**Dependency Mapping Table:**

Present this table in text format:

```
| Source Dependency | Version | Target Equivalent | Status | User Decision? |
|------------------|---------|------------------|--------|---------------|
| <source-dep> | <ver> | <target-equiv> | already-installed | No |
| <source-dep> | <ver> | <target-equiv> | not-installed | Yes |
| <source-dep> | <ver> | None (implement inline) | — | Yes |
| ... | | | | |
```

Key decision markers:
- "already-installed" → No user decision needed, use equivalent as-is
- "not-installed" → Present as dependency swap option in Step 5
- "None (implement inline)" → Feature can be ported inline without external dep

Log deciduous decisions after building tables:

```bash
deciduous add action "Analyzed target project conventions: <N> conventions identified, <M> dependencies mapped" -c 85
```

If cross-language port: also log

```bash
deciduous add action "Researched cross-language idiom equivalents: <patterns>" -c 85
```

#### Step 5: User Decision Points

Surface trade-off decisions to the user in three categories. Use AskUserQuestion for each decision.

**1. Dependency Swaps**

For each dependency in the Dependency Mapping Table where source and target differ (not already-installed), present options:

**AskUserQuestion** (singleSelect):

```
Dependency Swap: <source-dep>

The source feature uses <source-dep> (<source-version>).
Target project equivalent: <target-equiv>

Behavioral difference (if any):
<desc of how target equiv differs, performance/accuracy implications>

Choose one:
- "Use target equivalent <target-equiv>" (Recommended) → Maps all source usages to target equiv
- "Port <source-dep> inline" → Minimal adaptation of source dep logic within ported feature
- "Skip this functionality" → Omit the <source-dep> feature entirely
```

Log each decision:

```bash
deciduous add decision "Dep swap: <source-dep> → <target-equiv> because <rationale>" -c 85
```

Or if skipped:

```bash
deciduous add decision "Dep swap: <source-dep> skipped because <rationale>" -c 85
```

**2. Architectural Adaptations**

For each architectural style difference identified in Convention Mapping Table, present options:

**AskUserQuestion** (singleSelect):

```
Architecture: <pattern-name>

Source uses: <source-style> (e.g., global state, dependency injection, service locator)
Target project uses: <target-style>

Performance/Accuracy implications:
- Target style: <implications>
- Source style kept: <implications>
- Hybrid approach: <implications>

Choose one:
- "Adapt to target style <target-style>" (Recommended) → Refactor feature to match target patterns
- "Keep source style" → Maintain source approach, add adapter layer if needed
- "Hybrid approach" → Selective adaptation of <components> to target style
```

Log each decision:

```bash
deciduous add decision "Architecture: adapted <pattern> to target style because <rationale>" -c 85
```

Or if kept source or hybrid:

```bash
deciduous add decision "Architecture: <pattern> kept source style because <rationale>" -c 85
```

**3. Rigor Flagging (Conditional)**

Only prompt if `--rigor critical` was NOT passed globally.

**AskUserQuestion** (multiSelect):

```
Rigor Flagging

For larger features or complex ports, you can flag individual chunks for elevated verification
(property-based testing, extra adversarial iterations, 10x more test cases).

Chunks from this feature:
- Chunk 1: <name> (<L> lines)
- Chunk 2: <name> (<L> lines)
- Chunk 3: <name> (<L> lines)
- ... (or "All chunks") ...

Flag chunks for critical rigor (select zero or more):
- [  ] Chunk 1: <name>
- [  ] Chunk 2: <name>
- [  ] Chunk 3: <name>
- [  ] All chunks
```

Log the decision:

```bash
deciduous add decision "Rigor: chunks <list> flagged critical because <rationale>" -c 80
```

If no chunks flagged:

```bash
deciduous add decision "Rigor: standard verification applied to all chunks" -c 80
```

**Summary Log After All Decisions**

After all three decision categories, log a summary action:

```bash
deciduous add action "User decisions captured: <N> dependency swaps, <M> architectural adaptations, rigor flagged for <chunks>" -c 85
```

This completes the target convention analysis and user decision phase. The decisions feed into the design document generation (Phase 4).

#### Step 6: Generate Design Document

Generate a design document that synthesizes all analysis into a structured plan for implementation and verification.

**Design Document Location:**

Create `docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md` where:
- `YYYY-MM-DD` is today's date
- `<feature-slug>` is a slugified version of the feature name (e.g., "gle-constraints" for "GLE Constraints")

**Design Document Structure:**

The design document must contain these sections in order:

**1. Summary**

Brief overview of what is being ported and why:
```
## Summary

Porting <feature-name> from <source-location> to <target-project>.

**Source:** <source-path-or-url>
**Target:** This project
**Rationale:** <why this feature is valuable>
**Feature Description:** <what it does>
```

**2. Source Feature**

Complete information from Step 2:
```
## Source Feature

**Location:** <file-paths>
**Language:** <source-language>
**Lines of Code:** <N> (including transitive dependencies)

**Complete Implementation:**

<code blocks showing the entire feature and all non-library dependencies>

**Direct Dependencies:**
- <dependency-1>: <description and type>
- <dependency-2>: <description and type>
- ...

**Transitive Dependency Graph:**

<ASCII tree showing full dependency depth>

**External Dependencies:**
- <lib-1> (version <ver>): <purpose>
- <lib-2> (version <ver>): <purpose>
- ...
```

**3. Convention Mapping Table**

Directly embed the convention mapping table from Step 4:

```
## Convention Mapping

| Aspect | Source | Target | Adaptation Notes |
|--------|--------|--------|-----------------|
| Language | <source-lang> | <target-lang> | |
| Naming | <source-style> | <target-style> | Use target style: <example> |
| Error Handling | <source-error> | <target-error> | Map <source> exceptions to <target> errors |
| Async Model | <source-async> | <target-async> | Use target async/await pattern |
| Testing | <source-test> | <target-test> | Target uses <framework> with <mocking> |
| ... | ... | ... | ... |
```

**4. Dependency Mapping Table**

Directly embed the dependency mapping table from Step 4, including user decisions from Step 5:

```
## Dependency Mapping

| Source Dependency | Version | Target Equivalent | Status | User Decision |
|------------------|---------|------------------|--------|---------------|
| <source-dep> | <ver> | <target-equiv> | already-installed | Use as-is |
| <source-dep> | <ver> | <target-equiv> | not-installed | <decision-from-step-5> |
| ... | | | | |
```

**5. Architectural Adaptations**

Document all user decisions from Step 5 with rationale:

```
## Architectural Adaptations

### Adaptation 1: <pattern-name>

**Decision:** <choice-from-step-5>

**Rationale:** <why-this-choice>

**Implementation Plan:** <how-to-implement-the-adaptation>

### Adaptation 2: ...
```

**6. Acceptance Criteria**

Generate behavioral equivalence criteria based on the feature's behavior and chunk boundaries:

```
## Acceptance Criteria

For **all chunks**, the ported feature must:
- [ ] Execute identical inputs through source and target, comparing outputs
- [ ] Produce behaviorally equivalent results (or document acceptable differences with rationale)
- [ ] Include differential tests validating outputs match

For **chunks flagged --rigor critical** (if any):
- [ ] Execute property-based testing (100+ random test cases per property)
- [ ] Document property invariants and their correctness proof
- [ ] Include adversarial test cases specifically designed to stress the adaptation boundaries

Examples of acceptable differences:
- Error message text (behavior is equivalent)
- Internal execution time (within 2x of source, if documented)
- Memory layout (same functional output)
```

**7. Implementation Phases**

Create one phase per chunk (or one phase if monolithic). For cross-language ports, include shared test vector format.

```
<!-- START_PHASE_1 -->
### Phase 1: <chunk-name>

**Chunk Description:** <what-this-chunk-does>

**Source Code Reference:**

<complete source code of this chunk>

**Differential Test Requirements:**

Write differential tests that run identical inputs through both source and target implementations, comparing outputs.

For cross-language ports, use this test vector format:
- Input specification (JSON/YAML): <example>
- Expected output (JSON/YAML): <example>
- Generation strategy: Extract test vectors from source tests or synthesize from behavior
- Validation: Run vectors against both implementations, compare outputs

Document acceptable differences with rationale:
- <example>: acceptable because <rationale>

**Commit Message Format:**

When implementing this chunk, use:
```
feat(pollinate): <chunk-name>

Ported from: <source-location>
Behavioral equivalence: <summary of verification approach>
```

**Implementation Notes:**
- <architectural-decision>
- <dependency-swap-details>
- <error-handling-approach>
- <async-pattern-details>

<!-- END_PHASE_1 -->
```

Repeat for each chunk.

**8. Final Verification Phase**

After all implementation phases, add this special phase:

```
<!-- START_PHASE_FINAL -->
### Final Verification Phase

After all implementation is complete, run this command to verify behavioral equivalence across the entire ported feature:

\`\`\`bash
/pollinate-verify --source <SOURCE_PATH> --task <beads-epic-id>
\`\`\`

The `/pollinate-verify` skill runs a three-layer verification strategy:
1. **Layer 1: Differential Testing** — Runs all differential test vectors and compares outputs
2. **Layer 2: Behavioral Equivalence** — Validates property-based testing for critical chunks
3. **Layer 3: Integration Verification** — Tests the ported feature's interaction with the target codebase

**Do NOT run standard `/verify`.** Use `/pollinate-verify` instead.

<!-- END_PHASE_FINAL -->
```

**9. Additional Considerations**

Document special notes for this port:

```
## Additional Considerations

**Source Availability:**
```

For **local paths:**
```
Source code is at: `<SOURCE_PATH>`
```

For **remote clones:**
```
Source cloned to `<SOURCE_PATH>`. Do not delete until `/pollinate-verify` completes.
```

```

**Cross-Language Porting Considerations** (if applicable):

```
Cross-language port from <source-lang> to <target-lang>.

Bridging strategy:
- <pattern-1>: <how-it-maps>
- <pattern-2>: <how-it-maps>

Test vector generation:
- Extract test vectors from source test suite
- Format as JSON/YAML for language-agnostic comparison
- Validate against both source and target

Cleanup instructions:
After `/pollinate-verify` completes successfully:
- <source-lang> clone at <SOURCE_PATH> can be deleted
- <target-lang> implementation should be integrated into CI/CD
```

```

**Final Steps:**

Log the design doc generation:

```bash
deciduous add action "Generated design doc: docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md" -c 90
```

#### Step 7: Commit Design Document

Commit the generated design document to the repository:

```bash
git add docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md
git commit -m "docs: pollinate design for <feature> from <source>"
```

This captures the design document in the repository history and marks the completion of the pollination analysis phase.

## After Pollination Analysis

Complete the tracking lifecycle:

```bash
# Log outcome with verbatim summary
deciduous add outcome "Pollination analysis complete: <feature> from <source> mapped to <N> phases with <M> dependencies"

# Update beads epic to done
bd update <epic-id> --status done

# Add comment with design doc link
bd comment <epic-id> "Design: docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md"
```

### Handoff Instructions

Pollination analysis complete! Design document committed to `docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md`.

**IMPORTANT: Copy the command below BEFORE running /clear.**

(1) Copy this command now:

```
/workflow-commands:plan @docs/design-plans/YYYY-MM-DD-pollinate-<feature-slug>.md .
```

(2) Clear context:

```
/clear
```

(3) Paste and run the copied command.

After planning and execution complete, the final phase will run `/pollinate-verify --source <SOURCE_PATH> --task <epic-id>`
instead of standard `/verify` to ensure behavioral equivalence with the source.

---

## Appendix: Differential Testing Patterns

### Same-Language Differential Testing Pattern

When source and target are written in the same language, the most direct verification approach is to import both implementations and run identical inputs through them.

**Pattern Description:**

1. Create a test file that imports both the source implementation and the target (ported) implementation
2. Define test cases with representative inputs covering:
   - Normal/happy path cases
   - Edge cases (empty inputs, boundary values, etc.)
   - Error cases (invalid inputs, exceptional conditions)
3. Run each input through both implementations
4. Assert that outputs match exactly (or within configured tolerance for floating-point values)
5. Document any acceptable differences (see below)

**Python pytest Example:**

```python
import sys
import pytest

# Import source implementation
sys.path.insert(0, '<SOURCE_PATH>')
from source_module import source_feature

# Import target (ported) implementation
from target_module import target_feature

class TestDifferentialEquivalence:
    """Test that source and target implementations produce identical outputs."""

    def test_basic_case(self):
        """Test basic happy path."""
        input_data = {"key": "value", "count": 42}
        source_result = source_feature(input_data)
        target_result = target_feature(input_data)
        assert source_result == target_result

    def test_edge_case_empty_input(self):
        """Test with empty/minimal input."""
        source_result = source_feature({})
        target_result = target_feature({})
        assert source_result == target_result

    def test_edge_case_large_values(self):
        """Test with large input values."""
        input_data = {"count": 999999999}
        source_result = source_feature(input_data)
        target_result = target_feature(input_data)
        assert source_result == target_result

    def test_float_tolerance(self):
        """Test floating-point outputs with tolerance."""
        input_data = {"value": 3.14159}
        source_result = source_feature(input_data)
        target_result = target_feature(input_data)
        # Use approximate equality for floats
        assert abs(source_result - target_result) < 1e-10

    def test_error_case_invalid_input(self):
        """Test error handling with invalid input."""
        with pytest.raises(ValueError):
            source_feature(None)
        with pytest.raises(ValueError):
            target_feature(None)
```

**Key Points:**

- Import source from its original location (`SOURCE_PATH`)
- Reuse the same test cases for both implementations
- For floating-point comparisons, use `pytest.approx()` or manual tolerance checks
- Organize tests by category: happy path, edge cases, error cases
- Run with: `pytest test_differential.py -v`

---

### Cross-Language Differential Testing Pattern (Test Vectors)

When source and target are in different languages, use language-agnostic test vectors to bridge the gap. Test vectors are input/output pairs serialized to JSON or YAML, allowing you to generate test data from the source and validate against the target.

**Two-Phase Approach:**

**Phase 1: Generate Test Vectors from Source**

Run the source implementation with representative inputs and capture the input/output pairs:

```python
# generate_vectors.py
import json
import sys

sys.path.insert(0, '<SOURCE_PATH>')
from source_module import source_feature

def generate_test_vectors():
    """Generate test vectors by running source implementation."""
    vectors = []

    test_cases = [
        {"name": "basic_case", "input": {"key": "value", "count": 42}},
        {"name": "empty_input", "input": {}},
        {"name": "large_values", "input": {"count": 999999999}},
        {"name": "string_data", "input": {"text": "hello world"}},
    ]

    for case in test_cases:
        try:
            output = source_feature(case["input"])
            vectors.append({
                "name": case["name"],
                "input": case["input"],
                "expected_output": output,
                "tolerance": {"float": 1e-10}
            })
        except Exception as e:
            vectors.append({
                "name": case["name"],
                "input": case["input"],
                "expected_error": str(e),
                "error_type": type(e).__name__
            })

    with open("test_vectors.json", "w") as f:
        json.dump({"test_vectors": vectors}, f, indent=2)

    print(f"Generated {len(vectors)} test vectors in test_vectors.json")

if __name__ == "__main__":
    generate_test_vectors()
```

**Phase 2: Validate Against Target**

Load the vectors and run them against the target implementation in the target language:

```javascript
// validate_vectors.js (Node.js example)
const fs = require("fs");
const targetFeature = require("./target_module").targetFeature;

function validateTestVectors() {
  const data = JSON.parse(fs.readFileSync("test_vectors.json", "utf8"));
  const vectors = data.test_vectors;

  let passed = 0;
  let failed = 0;

  for (const vector of vectors) {
    try {
      const result = targetFeature(vector.input);

      if ("expected_output" in vector) {
        // Compare output
        if (JSON.stringify(result) === JSON.stringify(vector.expected_output)) {
          console.log(`✓ ${vector.name}`);
          passed++;
        } else {
          console.log(`✗ ${vector.name}: output mismatch`);
          console.log(`  Expected: ${JSON.stringify(vector.expected_output)}`);
          console.log(`  Got:      ${JSON.stringify(result)}`);
          failed++;
        }
      }
    } catch (e) {
      if ("expected_error" in vector) {
        console.log(`✓ ${vector.name} (expected error)`);
        passed++;
      } else {
        console.log(`✗ ${vector.name}: unexpected error: ${e.message}`);
        failed++;
      }
    }
  }

  console.log(`\nResults: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

validateTestVectors();
```

**Test Vector JSON Format:**

```json
{
  "test_vectors": [
    {
      "name": "descriptive_case_name",
      "input": { "key": "value", "count": 42 },
      "expected_output": { "result": "computed_value" },
      "tolerance": { "float": 1e-10 }
    },
    {
      "name": "error_case",
      "input": null,
      "expected_error": "ValueError",
      "error_type": "ValueError"
    },
    {
      "name": "large_values",
      "input": { "count": 999999999 },
      "expected_output": { "result": "large_computed_value" },
      "tolerance": {}
    }
  ]
}
```

**Language-Pair Bridging Strategies:**

| Language Pair | Strategy | Notes |
|---------------|----------|-------|
| Python ↔ Python | Direct import (preferred) | See Same-Language pattern above |
| Python ↔ Rust | Test vectors (JSON) | Generate from Python, validate in Rust via serde_json |
| Python ↔ JavaScript | Test vectors (JSON) | Generate from Python, validate in Node.js via require |
| Python ↔ Go | Test vectors (JSON) | Generate from Python, validate via encoding/json |
| JavaScript ↔ TypeScript | Direct import (preferred) | Same language family, direct equivalence |
| Rust ↔ Go | Test vectors (JSON) | Serialize via serde_json and serde, deserialize via encoding/json |

**Key Points:**

- Generate vectors from source once, reuse across all target validations
- Store vectors in version control for reproducibility
- Include both happy-path and error-case vectors
- For floating-point fields, include explicit tolerance values
- Validate vectors match source behavior before considering them authoritative
- Use subprocess calls to invoke target implementations if direct imports aren't available

---

### Acceptable Difference Documentation

When source and target implementations diverge in behavior, document the differences explicitly with rationale. Silent acceptance of divergences is prohibited — every difference must be justified.

**Template:**

```markdown
## Known Acceptable Differences

| Difference | Source Behavior | Target Behavior | Rationale | Approved By |
|-----------|----------------|-----------------|-----------|------------|
| Float precision | 1e-15 tolerance | 1e-12 tolerance | Target uses f32 for performance; approved as sufficient for use case | User (2026-03-26) |
| Sort stability | Stable sort (guaranteed) | Unstable sort | Rust's default sort is unstable; docs verify correctness unchanged | Architecture review |
| Error message text | "Invalid key: 'foo'" | "Invalid key: foo" | Target omits quotes for brevity; behavior identical | User acceptance |
| Execution time | ~100ms | ~200ms | Cross-language overhead acceptable per requirements | Performance review |
| Memory layout | Pointer-based | Value-based | Internal structure differs; external API identical | Implementation team |
```

**Filling in the Template:**

1. **Difference**: Brief name of the behavioral divergence
2. **Source Behavior**: What the source implementation does
3. **Target Behavior**: What the target implementation does
4. **Rationale**: Why this difference is acceptable
   - Language-specific limitation ("Rust doesn't have X")
   - Performance trade-off ("Acceptable for 2x slower with 10x better memory")
   - Architectural choice ("New design better fits target patterns")
   - User approval ("Team approved at design review")
5. **Approved By**: Who signed off on the difference (user name/email, review date, or "Architecture review", etc.)

**Rules:**

- Every difference discovered during differential testing MUST be documented here
- Differences pre-approved by user during Step 5 decisions should be pre-populated during design doc generation
- Before finalizing the port, review this table with the user to ensure all differences are acceptable
- Do not merge differences without documented rationale
- Mark differences as "Approved by" only after user confirmation or architecture review

**Example Workflow:**

1. **During differential testing:** Discover that target's sort function is unstable, source's is stable
2. **Immediate action:** Add row to Known Acceptable Differences table
3. **Document rationale:** Research why (Rust's default sort), check if it affects output correctness (doesn't)
4. **Get approval:** Present to user, get sign-off ("Confirmed acceptable, 2026-03-26")
5. **Finalize:** Merge with documented approval
