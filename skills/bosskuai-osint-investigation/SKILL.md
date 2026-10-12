---
name: bosskuai-osint-investigation
description: "Use when the task explicitly concerns osint investigation. Sparse-clue OSINT investigation methodology for extracting overlooked leads, connecting fragmented evidence, and testing explanations across sources. Use for multi-step CTF challenges, image/video geolocation, event reconstruction, public-account and entity verification, artifact interpretation, infrastructure research, or stalled investigations."
metadata:
  origin: ECC-adaptation
---

# OSINT Investigation — portable workflow

## Job and activation

Sparse-clue OSINT investigation methodology for extracting overlooked leads, connecting fragmented evidence, and testing explanations across sources. Use for multi-step CTF challenges, image/video geolocation, event reconstruction, public-account and entity verification, artifact interpretation, infrastructure research, or stalled investigations.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-autonomous-loops`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Scope and Trust.
2. How It Works.
3. 1. Define the Question.
4. 2. Separate Originals from Hypotheses.
5. 3. Execute the Cheapest Decisive Test.
6. 4. Change Strategy When Evidence Stops Changing.

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-autonomous-loops`, `bosskuai-cybersecurity-risk`, `bosskuai-deep-research`, `bosskuai-exa-search`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

The full source bundle is retained, including 1 sidecar files. Code is reference-only until its runtime dependencies, input/output paths and requested operation are reviewed. This import did not execute its scripts.

This domain can require a named provider/MCP/API. Discover available tools, verify the documented surface and scope, and report unavailable capabilities. Do not replace a missing provider with invented output.

For clinical, compliance, legal, regulatory or financial conclusions, obtain current authoritative sources and an independent review. Treat sample values and rules as examples until verified for the actual jurisdiction/system.

## Pass signal

Complete the source “5. Verify Lineage, Time, and Fidelity”, “6. Verify Visual Scenes and Geometry” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
