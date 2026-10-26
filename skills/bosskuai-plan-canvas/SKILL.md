---
name: bosskuai-plan-canvas
description: "Use when the task explicitly concerns plan canvas. Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes without leaving the page. Use when presenting a plan for review, or when feedback like \"move this, change that\" is easier pointed at than typed."
metadata:
  origin: ECC-adaptation
---

# Plan Canvas — portable workflow

Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes without leaving the page. Use when presenting a plan for review, or when feedback like "move this, change that" is easier pointed at than typed.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-engineering-delivery`, `bosskuai-product-strategy`, `bosskuai-flox-environments`, `bosskuai-taste`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. 1. Open the artifact in the user's browser (returns immediately).
3. 2. Block until the human responds. Leave running; re-run if interrupted:.
4. queued feedback is never lost..
5. Stay listening, or the human talks to an empty chair.
6. animated "agent is thinking..." bubble; refresh it during long work.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “How It Works”, “1. Open the artifact in the user's browser (returns immediately)” guidance to the concrete request. Return the resulting plan canvas artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
