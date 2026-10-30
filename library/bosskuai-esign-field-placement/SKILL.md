---
name: bosskuai-esign-field-placement
description: "Use when the task explicitly concerns esign field placement. Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, using a fixed signature page, numeric Location panel coordinates instead of drag, and a save-as-draft default. Use when automating envelope preparation for generated agreements and you need repeatable field positions, correct per-recipient ownership, and a hard gate before anything is sent or signed."
metadata:
  origin: ECC-adaptation
---

# E-Signature Field Placement — portable workflow

Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, using a fixed signature page, numeric Location panel coordinates instead of drag, and a save-as-draft default. Use when automating envelope preparation for generated agreements and you need repeatable field positions, correct per-recipient ownership, and a hard gate before anything is sent or signed.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-agent-introspection`, `bosskuai-automation-audit-ops`, `bosskuai-browser-automation`, `bosskuai-master-agreement-generator`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Preconditions.
3. Trusted browser target.
4. Recipients.
5. Calibration.
6. Placing fields.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “How It Works”, “Preconditions” guidance to the concrete request. Return the resulting e-signature field placement artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
