---
name: bosskuai-click-path-audit
description: "Use when the task explicitly concerns click path audit. Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores."
metadata:
  origin: ECC-adaptation
---

# /click-path-audit — Behavioural Flow Audit — portable workflow

## Job and activation

Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-permanent-memory-orchestration`, `verification-before-completion`, `bosskuai-brownfield-retrospective`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. The Problem This Solves.
2. How It Works.
3. Execution Steps.
4. Step 1: Map State Stores.
5. Step 2: Audit Each Touchpoint.
6. Step 3: Report.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-brownfield-retrospective`, `bosskuai-permanent-memory-orchestration`, `verification-before-completion`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

## Pass signal

Apply the source “The Problem This Solves”, “How It Works” guidance to the concrete request. Return the resulting /click-path-audit — behavioural flow audit artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
