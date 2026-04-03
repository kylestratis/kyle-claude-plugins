---
description: Three-layer verification for ported code - differential testing, adversarial hardening, and standard verify
argument-hint: [--task <beads-id>] [--source <path>]
---

# Pollinate Verify

**Arguments:** `$ARGUMENTS`

Use your Skill tool to engage the `pollinate-verify` skill. Follow it exactly as written.

This command runs after `/execute` completes a pollination port. It verifies behavioral equivalence with the source (differential tests + adversarial hardening) then runs standard project verification.
