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
