---
name: bosskuai-carrier-relationship-management
description: "Use when the task explicitly concerns carrier relationship management. Manage truckload, LTL, and intermodal carrier portfolios: sourcing and FMCSA vetting, freight rate and fuel-surcharge negotiation, RFPs and routing guides, carrier scorecards, allocation, and renewals. Use when onboarding carriers, running freight RFPs, negotiating rates, evaluating carrier performance, reallocating freight, or building freight strategy."
metadata:
  origin: ECC-adaptation
---

# Carrier Relationship Management — portable workflow

Manage truckload, LTL, and intermodal carrier portfolios: sourcing and FMCSA vetting, freight rate and fuel-surcharge negotiation, RFPs and routing guides, carrier scorecards, allocation, and renewals. Use when onboarding carriers, running freight RFPs, negotiating rates, evaluating carrier performance, reallocating freight, or building freight strategy.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-energy-procurement`, `bosskuai-compose-multiplatform-patterns`, `bosskuai-logistics-exception-management`, `bosskuai-performance-profiling`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. Rate Negotiation Fundamentals.
5. Carrier Scorecarding.
6. Portfolio Strategy.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting carrier relationship management artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
