---
name: bosskuai-logistics-exception-management
description: "Use when the task explicitly concerns logistics exception management. Codified freight-exception handling expertise for shipment delays, damages, losses, shortages, and carrier disputes, with escalation protocols, carrier-specific behaviors by mode, claims procedures, and eat-the-cost vs fight-the-claim judgment frameworks. Use when handling shipping exceptions, freight claims, delivery issues, or carrier disputes."
metadata:
  origin: ECC-adaptation
---

# Logistics Exception Management — portable workflow

Codified freight-exception handling expertise for shipment delays, damages, losses, shortages, and carrier disputes, with escalation protocols, carrier-specific behaviors by mode, claims procedures, and eat-the-cost vs fight-the-claim judgment frameworks. Use when handling shipping exceptions, freight claims, delivery issues, or carrier disputes.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-returns-reverse-logistics`, `bosskuai-production-scheduling`, `bosskuai-carrier-relationship-management`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Role and Context.
2. How It Works.
3. Core Knowledge.
4. Exception Taxonomy.
5. Carrier Behaviour by Mode.
6. Claims Process Fundamentals.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- For clinical, compliance, legal, regulatory or financial conclusions, use current authoritative sources and an independent review; treat sample values and rules as examples until checked for the actual jurisdiction or system.

## Done when

Apply the source “Role and Context”, “How It Works” guidance to the concrete request. Return the resulting logistics exception management artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
