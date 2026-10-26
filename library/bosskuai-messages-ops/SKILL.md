---
name: bosskuai-messages-ops
description: "Use when the task explicitly concerns messages ops. Evidence-first live messaging workflow for the source pack. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replying, or prove which message source was actually checked."
metadata:
  origin: ECC-adaptation
---

# Messages Ops — portable workflow

Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replying, or prove which message source was actually checked.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-automation-audit-ops`, `bosskuai-email-ops`, `bosskuai-finance-billing-ops`, `bosskuai-connections-optimizer`, `bosskuai-lead-intelligence`, `bosskuai-permanent-memory-orchestration`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Skill Stack.
2. Guardrails.
3. Workflow.
4. 1. Resolve the exact thread.
5. 2. Read before drafting.
6. 3. Handle codes as a focused retrieval task.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Workflow”, “Output Format” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
