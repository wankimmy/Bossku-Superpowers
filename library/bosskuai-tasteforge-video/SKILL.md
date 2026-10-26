---
name: bosskuai-tasteforge-video
description: "Use when the task explicitly concerns tasteforge video. Use for file-driven multimodal image, video, and 3D-asset discovery; taste interviews; distill or apply workflows; style-pack validation; editable EDL/FCPXML export; provenance audits; and offline planning that must fail closed before provider generation."
metadata:
  origin: ECC-adaptation
---

# TasteForge Video — portable workflow

Use for file-driven multimodal image, video, and 3D-asset discovery; taste interviews; distill or apply workflows; style-pack validation; editable EDL/FCPXML export; provenance audits; and offline planning that must fail closed before provider generation.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-video-creative-direction`, `bosskuai-codebase-analysis`, `bosskuai-video-style-application`, `bosskuai-fal-ai-media`, `bosskuai-video-editing`, `bosskuai-video-style-distillation`, `content-strategy`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Local Deterministic Operations vs Provider Generation.
2. Canonical Implementation.
3. Chaining the Creative Skills.
4. Workflow.
5. Applying Real Footage Without Repeated Sources.
6. File-Driven Multimodal Contract.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Workflow” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
