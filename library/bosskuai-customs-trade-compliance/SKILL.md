---
name: bosskuai-customs-trade-compliance
description: "Use when the task explicitly concerns customs trade compliance. Codified customs and trade compliance expertise — HS/HTS tariff classification with GRI rules, commercial invoices and entry documentation, Incoterms 2020, FTA qualification and duty optimization (USMCA, RCEP, FTZs, drawback), denied-party screening, and penalty mitigation across US, EU, UK, and APAC jurisdictions. Use when classifying goods, preparing import/export documentation, screening restricted parties, responding to customs audits or CF-28/penalty notices, or optimizing duties."
metadata:
  origin: ECC-adaptation
---

# Customs & Trade Compliance — portable workflow

Codified customs and trade compliance expertise — HS/HTS tariff classification with GRI rules, commercial invoices and entry documentation, Incoterms 2020, FTA qualification and duty optimization (USMCA, RCEP, FTZs, drawback), denied-party screening, and penalty mitigation across US, EU, UK, and APAC jurisdictions. Use when classifying goods, preparing import/export documentation, screening restricted parties, responding to customs audits or CF-28/penalty notices, or optimizing duties.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-production-scheduling`, `bosskuai-energy-procurement`, `bosskuai-inventory-demand-planning`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. HS Tariff Classification.
5. Documentation Requirements.
6. Incoterms 2020.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting customs & trade compliance artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
