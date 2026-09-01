# Agent Instructions

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**

```bash
bd ready                                     # Find unblocked work
bd create "Title" --type task --priority 2   # Create issue
bd show <id>                                 # View issue details
bd update <id> --claim                       # Claim work
bd close <id>                                # Complete work
```

For full workflow details: `bd prime`
<!-- END BEADS INTEGRATION -->

## Issue Tracking Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files; search it with `bd memories <keyword>`

**Architecture in one line:** issues live in a local Dolt database under `.beads/` (gitignored); this repo has **no Dolt remote** (`bd dolt remote list` reports "No remotes configured", so `bd dolt push` is a no-op), so issues travel between clones solely through the git-tracked `.beads/issues.jsonl` export that the installed `pre-commit` hook regenerates with `bd export` on every commit.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   bd export -o .beads/issues.jsonl  # optional: the pre-commit hook already does this
   git add .beads
   git commit -m "<message>"
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
