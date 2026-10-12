---
name: bosskuai-energy-procurement
description: "Use when the task explicitly concerns energy procurement. Procure electricity and natural gas for commercial and industrial facilities: tariff and rate-schedule optimization, demand-charge mitigation, supplier RFPs, fixed/index/block-and-index hedging, renewable PPA and REC evaluation, and sustainability reporting. Use when procuring energy, optimizing utility tariffs, managing demand charges, evaluating PPAs, or building energy budgets and hedge strategies."
metadata:
  origin: ECC-adaptation
---

# Energy Procurement — portable workflow

## Job and activation

Procure electricity and natural gas for commercial and industrial facilities: tariff and rate-schedule optimization, demand-charge mitigation, supplier RFPs, fixed/index/block-and-index hedging, renewable PPA and REC evaluation, and sustainability reporting. Use when procuring energy, optimizing utility tariffs, managing demand charges, evaluating PPAs, or building energy budgets and hedge strategies.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-customs-trade-compliance`, `bosskuai-carrier-relationship-management`, `bosskuai-inventory-demand-planning`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. Pricing Structures and Utility Bill Anatomy.
5. Procurement Strategies.
6. Demand Charge Management.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-carrier-relationship-management`, `bosskuai-customs-trade-compliance`, `bosskuai-inventory-demand-planning`, `bosskuai-performance-profiling`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

For clinical, compliance, legal, regulatory or financial conclusions, obtain current authoritative sources and an independent review. Treat sample values and rules as examples until verified for the actual jurisdiction/system.

## Pass signal

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting energy procurement artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
