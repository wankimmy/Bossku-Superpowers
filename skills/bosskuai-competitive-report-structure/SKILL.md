---
name: bosskuai-competitive-report-structure
description: "Use when the task explicitly concerns competitive report structure. Assemble scored competitor profile cards (from benchmark-methodology) into a decision-grade competitive report with landscape map, competitor tiers, benchmarking matrix, white-space analysis, strategic recommendations, and team alignment trigger questions. Use when presenting competitive findings to leadership or a board, writing a competitive landscape report, or as the final step of the competitive analysis pipeline."
metadata:
  origin: ECC-adaptation
---

# Competitive Report Structure — portable workflow

## Job and activation

Assemble scored competitor profile cards (from benchmark-methodology) into a decision-grade competitive report with landscape map, competitor tiers, benchmarking matrix, white-space analysis, strategic recommendations, and team alignment trigger questions. Use when presenting competitive findings to leadership or a board, writing a competitive landscape report, or as the final step of the competitive analysis pipeline.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-competitor-scoring`, `bosskuai-competitive-platform-analysis`, `bosskuai-deep-research`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Client positioning brief (establish first).
2. Framing principle.
3. Report sections.
4. 1. Executive summary.
5. 2. Market landscape & category framing.
6. 3. Competitor tiers.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-brand-discovery`, `bosskuai-competitive-platform-analysis`, `bosskuai-competitor-scoring`, `bosskuai-deep-research`, `bosskuai-performance-profiling`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Apply the source “Client positioning brief (establish first)”, “Framing principle” guidance to the concrete request. Return the resulting competitive report structure artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
