---
name: bosskuai-inventory-demand-planning
description: "Use when the task explicitly concerns inventory demand planning. Codified demand planning expertise for multi-location retailers: demand forecasting method selection, ABC/XYZ segmentation, safety stock and reorder-point optimization, promotional lift and post-promo dip estimation, and seasonal transition and markdown timing. Use when forecasting demand, setting safety stock, planning replenishment, managing promotions, or optimizing inventory levels."
metadata:
  origin: ECC-adaptation
---

# Inventory Demand Planning — portable workflow

## Job and activation

Codified demand planning expertise for multi-location retailers: demand forecasting method selection, ABC/XYZ segmentation, safety stock and reorder-point optimization, promotional lift and post-promo dip estimation, and seasonal transition and markdown timing. Use when forecasting demand, setting safety stock, planning replenishment, managing promotions, or optimizing inventory levels.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-customs-trade-compliance`, `bosskuai-energy-procurement`, `bosskuai-production-scheduling`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. Forecasting Methods and When to Use Each.
5. Forecast Accuracy Metrics.
6. Safety Stock Calculation.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-customs-trade-compliance`, `bosskuai-energy-procurement`, `bosskuai-production-scheduling`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting inventory demand planning artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
