---
name: bosskuai-competitor-scoring
description: "Use when the task explicitly concerns competitor scoring. Score a scoped competitor set into comparable profile cards: nine weighted dimensions (positioning, voice, visual craft, offer packaging, evidence, enterprise-readiness, thought leadership, pricing, client tension) with 1-5 evidence-anchored rubrics and a tension 2x2 plot. Use when benchmarking or scoring competitors, building a competitive comparison matrix, or grading rival positioning before assembling the report; runs after competitive-platform-analysis and before competitive-report-structure."
metadata:
  origin: ECC-adaptation
---

# Benchmark Methodology — portable workflow

## Job and activation

Score a scoped competitor set into comparable profile cards: nine weighted dimensions (positioning, voice, visual craft, offer packaging, evidence, enterprise-readiness, thought leadership, pricing, client tension) with 1-5 evidence-anchored rubrics and a tension 2x2 plot. Use when benchmarking or scoring competitors, building a competitive comparison matrix, or grading rival positioning before assembling the report; runs after competitive-platform-analysis and before competitive-report-structure.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-competitive-report-structure`, `bosskuai-competitive-platform-analysis`, `bosskuai-design-systems`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Client positioning brief (establish first).
2. Why these dimensions.
3. The nine dimensions (with weights).
4. Scoring rubric (1–5, applies to dimensions 1–8).
5. Tension axes (dimension 9) — score each 1–5.
6. How to collect the data.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-competitive-platform-analysis`, `bosskuai-competitive-report-structure`, `bosskuai-design-systems`, `bosskuai-performance-profiling`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Complete the source “Scoring rubric (1–5, applies to dimensions 1–8)”, “Competitor profile card (output format)” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
