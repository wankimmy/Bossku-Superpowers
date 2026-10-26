---
name: bosskuai-osint-investigation
description: "Use when the task explicitly concerns osint investigation. Sparse-clue OSINT investigation methodology for extracting overlooked leads, connecting fragmented evidence, and testing explanations across sources. Use for multi-step CTF challenges, image/video geolocation, event reconstruction, public-account and entity verification, artifact interpretation, infrastructure research, or stalled investigations."
metadata:
  origin: ECC-adaptation
---

# OSINT Investigation — portable workflow

Sparse-clue OSINT investigation methodology for extracting overlooked leads, connecting fragmented evidence, and testing explanations across sources. Use for multi-step CTF challenges, image/video geolocation, event reconstruction, public-account and entity verification, artifact interpretation, infrastructure research, or stalled investigations.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-autonomous-loops`, `bosskuai-cybersecurity-risk`, `bosskuai-deep-research`, `bosskuai-exa-search`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Scope and Trust.
2. How It Works.
3. 1. Define the Question.
4. 2. Separate Originals from Hypotheses.
5. 3. Execute the Cheapest Decisive Test.
6. 4. Change Strategy When Evidence Stops Changing.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Complete the source “5. Verify Lineage, Time, and Fidelity”, “6. Verify Visual Scenes and Geometry” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
