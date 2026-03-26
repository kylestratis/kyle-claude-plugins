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

**Announce:** "I'm analyzing the source feature for cross-codebase porting."

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

Your response must include:
1. The path where you cloned the repository (will be needed for later verification)
2. All sections from the local path instructions above

CRITICAL: After cloning to a temporary location, output the clone path so we can persist it for later use.
```

After agent returns, capture the source path:
- **Local paths:** Record as `SOURCE_PATH = <original-path>`
- **Remote clones:** Record as `SOURCE_PATH = <clone-path>` (from agent response)

**Store SOURCE_PATH in a variable for later use in design doc generation.**

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

3. Log decomposition decision to deciduous:

```bash
# After user chooses decomposition approach
if [ "$(user_choice)" = "monolithic" ]; then
  deciduous add decision "Kept <feature> as monolithic unit: <N> lines, <M> dependencies" -c 80
else
  deciduous add decision "Decomposed <feature> into <K> chunks: <chunk-names>" -c 80
fi
```

4. **End of Step 3:** Log source extraction outcome to deciduous:

```bash
deciduous add action "Extracted <feature> from <source>: <N> lines, <M> dependencies" -c 85

# If chunks were analyzed (regardless of choice):
# (this decision was logged above in Step 3)
```
