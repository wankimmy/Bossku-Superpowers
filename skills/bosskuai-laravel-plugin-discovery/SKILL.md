---
name: bosskuai-laravel-plugin-discovery
description: "Use when the task explicitly concerns laravel plugin discovery. Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility."
metadata:
  origin: ECC-adaptation
---

# Laravel Plugin Discovery — portable workflow

Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-lead-intelligence`, `bosskuai-frontend-slides`, `bosskuai-ito-compute`, `bosskuai-documentation-lookup`, `bosskuai-laravel-development`, `bosskuai-laravel-security`, `bosskuai-laravel-tdd`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. MCP Tools.
2. SearchPluginTool.
3. GetPluginDetailsTool.
4. How It Works.
5. Finding Packages.
6. Evaluating Packages.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “MCP Tools”, “SearchPluginTool” guidance to the concrete request. Return the resulting laravel plugin discovery artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
