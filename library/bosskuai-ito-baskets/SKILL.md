---
name: bosskuai-ito-baskets
description: "Use when the task explicitly concerns ito baskets. Read-only Itô basket and prediction-market data skill. Index the live basket catalog, compare a basket against user-supplied research or a watchlist, build a source-grounded market brief, or draft a non-executable planning worksheet. Use when a user asks to browse or index Itô baskets, compare a basket against notes or a thesis, research prediction-market events/venues/liquidity, or plan a basket or market idea without trading. Never advises, orders, trades, reserves, or executes."
metadata:
  origin: ECC-adaptation
---

# Itô Baskets — portable workflow

Read-only Itô basket and prediction-market data skill. Index the live basket catalog, compare a basket against user-supplied research or a watchlist, build a source-grounded market brief, or draft a non-executable planning worksheet. Use when a user asks to browse or index Itô baskets, compare a basket against notes or a thesis, research prediction-market events/venues/liquidity, or plan a basket or market idea without trading. Never advises, orders, trades, reserves, or executes.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-prediction-market-oracle-research`, `bosskuai-deep-research`, `bosskuai-documentation-lookup`, `bosskuai-exa-search`, `bosskuai-ito-compute`, `bosskuai-market-analysis`, `bosskuai-prediction-market-risk-review`, `bosskuai-x-api`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Non-negotiable boundaries.
2. Access surfaces.
3. Bundled read-only client.
4. Anonymous index reads (no credential is ever sent):.
5. Keyed reads (require ITO_API_KEY in the environment):.
6. Mode workflows.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 2 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Mode workflows”, “Output contracts” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
