---
name: bosskuai-unified-notifications-ops
description: "Use when the task explicitly concerns unified notifications ops. Operate notifications as one portable workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real problem is alert routing, deduplication, escalation, or inbox collapse."
metadata:
  origin: ECC-adaptation
---

# Unified Notifications Ops — portable workflow

## Job and activation

Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real problem is alert routing, deduplication, escalation, or inbox collapse.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-project-flow-ops`, `bosskuai-google-workspace-ops`, `bosskuai-tools`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Preferred Surface.
2. Non-Negotiable Rules.
3. Event Pipeline.
4. Default Severity Model.
5. Workflow.
6. 1. Inventory the current surface.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-customer-billing-ops`, `bosskuai-github-workflow`, `bosskuai-google-workspace-ops`, `bosskuai-permanent-memory-orchestration`, `bosskuai-project-flow-ops`, `bosskuai-tools`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Complete the source “Workflow”, “4. Design the ECC-native workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
