---
name: bosskuai-finance-billing-ops
description: "Use when the task explicitly concerns finance billing ops. Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for the source pack. Use when the user wants a sales snapshot, pricing comparison, duplicate-charge diagnosis, or code-backed billing reality instead of generic payments advice."
metadata:
  origin: ECC-adaptation
---

# Finance Billing Ops — portable workflow

Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapshot, pricing comparison, duplicate-charge diagnosis, or code-backed billing reality instead of generic payments advice.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-messages-ops`, `bosskuai-automation-audit-ops`, `bosskuai-deep-research`, `bosskuai-customer-billing-ops`, `bosskuai-github-workflow`, `bosskuai-market-analysis`, `verification-before-completion`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Skill Stack.
2. Guardrails.
3. Workflow.
4. 1. Start from the freshest billing evidence.
5. 2. Separate customer incidents from product truth.
6. 3. Inspect code-backed billing behavior.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Workflow”, “Output Format” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
