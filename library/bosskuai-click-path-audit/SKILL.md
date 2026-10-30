---
name: bosskuai-click-path-audit
description: "Use when the task explicitly concerns click path audit. Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores."
metadata:
  origin: ECC-adaptation
---

# /click-path-audit — Behavioural Flow Audit — portable workflow

Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-permanent-memory-orchestration`, `verification-before-completion`, `bosskuai-brownfield-retrospective`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. The Problem This Solves.
2. How It Works.
3. Execution Steps.
4. Step 1: Map State Stores.
5. Step 2: Audit Each Touchpoint.
6. Step 3: Report.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the UI framework and state library versions in the manifest and lockfile against their latest stable releases, checked live at work time, and the source prerequisites first. Read the docs for the version the app runs. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “The Problem This Solves”, “How It Works” guidance to the concrete request. Return the resulting /click-path-audit — behavioural flow audit artifact or diagnosis with source/command evidence for each conclusion.

- Walk each button with empty, normal and large data, with a slow or failing API response, and with a double click. Do this only on a staging copy of the app, loaded with a copy of production data, using test accounts and sandbox keys for payment, mail and SMS, so no real message, charge or record change can happen. Never click through production or a real tenant account. If there is no staging copy, ask the user to prepare one and carry on with read-only analysis.
- Compare the state after each action with the screen after a page reload. A mismatch is a bug, even when each function passes its own test.
- Check every role and tenant that can see the button, on the same staging copy, using test accounts only.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
