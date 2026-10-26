---
name: bosskuai-mle-workflow
description: "Use when the task explicitly concerns mle workflow. Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when building, reviewing, or hardening ML systems beyond one-off notebooks."
metadata:
  origin: ECC-adaptation
---

# Machine Learning Engineering Workflow — portable workflow

Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when building, reviewing, or hardening ML systems beyond one-off notebooks.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-pytorch-patterns`, `bosskuai-operations`, `bosskuai-ml-adoption-playbook`, `bosskuai-clickhouse-io`, `bosskuai-eval-driven-agent-improvement`, `bosskuai-postgres-patterns`, `bosskuai-qa-automation-strategy`, `database-migrations`, `python-patterns`, `python-testing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Scope Calibration.
2. Reuse the SWE Surface.
3. Ten MLE Task Simulations.
4. Iteration Compact.
5. Decision Brain.
6. Metric and Mistake Economics.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Machine Learning Engineering Workflow”, “Core Workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
