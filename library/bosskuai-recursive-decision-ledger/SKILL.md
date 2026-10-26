---
name: bosskuai-recursive-decision-ledger
description: "Use when the task explicitly concerns recursive decision ledger. Run repeated rollouts (\"Prime Gauss\" style recursive prompting) while keeping an append-only decision ledger of trials, marks, coherence checks, and promotion gates, so recursive confidence never auto-approves live trading, deploy, or destructive actions. Use when the user asks for repeated rollouts, marked decision processes, high-dimensional search, stochastic optimization, local-optima exploration, ensemble comparison, or recursive reasoning with a visible evidence trail."
metadata:
  origin: ECC-adaptation
---

# Recursive Decision Ledger — portable workflow

Run repeated rollouts ("Prime Gauss" style recursive prompting) while keeping an append-only decision ledger of trials, marks, coherence checks, and promotion gates, so recursive confidence never auto-approves live trading, deploy, or destructive actions. Use when the user asks for repeated rollouts, marked decision processes, high-dimensional search, stochastic optimization, local-optima exploration, ensemble comparison, or recursive reasoning with a visible evidence trail.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-ito-baskets`, `bosskuai-deep-research`, `architecture-decision-records`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Ledger Contract.
2. Rollout Loop.
3. Coherence Mark.
4. Promotion Rules.
5. Summary Shape.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Ledger Contract”, “Rollout Loop” guidance to the concrete request. Return the resulting recursive decision ledger artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
