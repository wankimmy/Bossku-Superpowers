---
name: bosskuai-prediction-market-risk-review
description: "Use when the task explicitly concerns prediction market risk review. Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk. Use before any workflow handles venue auth, user portfolio data, API keys, or trade planning."
metadata:
  origin: ECC-adaptation
---

# Prediction Market Risk Review — portable workflow

Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk. Use before any workflow handles venue auth, user portfolio data, API keys, or trade planning.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-ito-baskets`, `bosskuai-product-strategy`, `bosskuai-prediction-market-oracle-research`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Review Gates.
2. Advice Boundary.
3. Venue And Regulatory Boundary.
4. Data Quality.
5. Security.
6. Privacy.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Complete the source “Data Quality”, “Output Contract” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
