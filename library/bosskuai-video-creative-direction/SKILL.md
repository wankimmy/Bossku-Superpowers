---
name: bosskuai-video-creative-direction
description: "Use when the task explicitly concerns video creative direction. Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop family — a named-genre aesthetic vocabulary, mood + color + light system, beat-synced editing grammar, and a pipeline chaining the source pack's video skills from b-roll generation to distribution. Use when a video must feel intentional rather than merely functional — music videos, fancams, moodboard-driven reels, or giving AI-generated b-roll a coherent visual direction."
metadata:
  origin: ECC-adaptation
---

# Taste — portable workflow

Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop family — a named-genre aesthetic vocabulary, mood + color + light system, beat-synced editing grammar, and a pipeline chaining ECC's video skills from b-roll generation to distribution. Use when a video must feel intentional rather than merely functional — music videos, fancams, moodboard-driven reels, or giving AI-generated b-roll a coherent visual direction.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-frontend-slides`, `bosskuai-manim-video`, `bosskuai-tasteforge-video`, `animate`, `bosskuai-fal-ai-media`, `bosskuai-remotion-video-creation`, `bosskuai-taste`, `bosskuai-video-editing`, `bosskuai-videodb`, `content-strategy`, `emil-design-eng`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Thesis.
2. The Aesthetic Vocabulary (distilled).
3. The Mood System — angelcore × cloud-trance.
4. Palette.
5. Light & texture.
6. Motion.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Produce a video creative direction tied to supplied references, mood/visual vocabulary and the requested track/edit constraints.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
