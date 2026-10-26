---
name: bosskuai-brand-discovery
description: "Use when the task explicitly concerns brand discovery. Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder tension) using laddering, 5 Whys, and projective techniques, persisting answers to disk and producing a master brandbook (90_SYNTHESIS.md). Use when creating or repositioning a brand, briefing designers or writers, or making implicit founder knowledge explicit."
metadata:
  origin: ECC-adaptation
---

# Brand Discovery — portable workflow

## Job and activation

Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder tension) using laddering, 5 Whys, and projective techniques, persisting answers to disk and producing a master brandbook (90_SYNTHESIS.md). Use when creating or repositioning a brand, briefing designers or writers, or making implicit founder knowledge explicit.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `marketing-plan`, `bosskuai-brand-voice`, `bosskuai-claude-devfleet`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Session start protocol.
2. Interview discipline.
3. Module sequence.
4. State write protocol.
5. Multi-founder mode.
6. Anti-Patterns.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-brand-voice`, `bosskuai-claude-devfleet`, `bosskuai-competitor-intelligence`, `marketing-plan`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

The full source bundle is retained, including 8 sidecar files. Code is reference-only until its runtime dependencies, input/output paths and requested operation are reviewed. This import did not execute its scripts.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

## Pass signal

Apply the source “Session start protocol”, “Interview discipline” guidance to the concrete request. Return the resulting brand discovery artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
