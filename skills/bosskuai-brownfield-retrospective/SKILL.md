---
name: bosskuai-brownfield-retrospective
description: "Use when the task explicitly concerns brownfield retrospective. Run the the source pack engineering process retroactively against an existing project slice. Audit current state, reconstruct past decisions, produce a four-axis gap register (thinking, coding practice, missing features, technology selection), then execute fixes forward through the plan-TDD-review pipeline. Use when adopting the source pack mid-project, taking over an inherited codebase, or asking what was missed and what would have been built differently from day one."
metadata:
  origin: ECC-adaptation
---

# Brownfield Retrospective — portable workflow

## Job and activation

Run the ECC engineering process retroactively against an existing project slice. Audit current state, reconstruct past decisions, produce a four-axis gap register (thinking, coding practice, missing features, technology selection), then execute fixes forward through the plan-TDD-review pipeline. Use when adopting ECC mid-project, taking over an inherited codebase, or asking what was missed and what would have been built differently from day one.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-documentation-lookup`, `bosskuai-autonomous-loops`, `bosskuai-orch-build-mvp`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. The Working Set.
2. How It Works.
3. Phase 0 — Pick the Entry Point.
4. Phase 1 — Present-State Audit.
5. Phase 2 — Backward Reconstruction.
6. Phase 3 — Gap Analysis (Four Axes).

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `architecture-decision-records`, `bosskuai-autonomous-loops`, `bosskuai-cybersecurity-risk`, `bosskuai-documentation-lookup`, `bosskuai-orch-build-mvp`, `bosskuai-permanent-memory-orchestration`, `bosskuai-product-verification`, `bosskuai-project-understanding`, `bosskuai-tdd-loop`, `verification-before-completion`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Apply the source “The Working Set”, “How It Works” guidance to the concrete request. Return the resulting brownfield retrospective artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
