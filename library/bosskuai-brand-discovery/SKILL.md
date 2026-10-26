---
name: bosskuai-brand-discovery
description: "Use when the task explicitly concerns brand discovery. Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder tension) using laddering, 5 Whys, and projective techniques, persisting answers to disk and producing a master brandbook (90_SYNTHESIS.md). Use when creating or repositioning a brand, briefing designers or writers, or making implicit founder knowledge explicit."
metadata:
  origin: ECC-adaptation
---

# Brand Discovery — portable workflow

Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder tension) using laddering, 5 Whys, and projective techniques, persisting answers to disk and producing a master brandbook (90_SYNTHESIS.md). Use when creating or repositioning a brand, briefing designers or writers, or making implicit founder knowledge explicit.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `marketing-plan`, `bosskuai-brand-voice`, `bosskuai-claude-devfleet`, `bosskuai-competitor-intelligence`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Session start protocol.
2. Interview discipline.
3. Module sequence.
4. State write protocol.
5. Multi-founder mode.
6. Anti-Patterns.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 8 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Session start protocol”, “Interview discipline” guidance to the concrete request. Return the resulting brand discovery artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
