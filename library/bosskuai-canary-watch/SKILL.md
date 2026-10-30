---
name: bosskuai-canary-watch
description: "Use when the task explicitly concerns canary watch. Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions after deploys, merges, or dependency upgrades. Smoke / canary / post-deploy verification."
metadata:
  origin: ECC-adaptation
---

# Canary Watch — Post-Deploy Monitoring — portable workflow

Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions after deploys, merges, or dependency upgrades. Smoke / canary / post-deploy verification.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-browser-automation`, `bosskuai-quarkus-verification`, `bosskuai-laravel-verification`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. What It Watches.
3. Watch Modes.
4. Alert Thresholds.
5. Notifications.
6. Output.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the deployed build's release tag or commit, and the versions of the monitoring tool and the browser or HTTP client, each checked live at work time, and the source prerequisites first. Record them with every check. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Output” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Take a baseline before the release: status codes, latency, error rate, asset sizes and whether each SSE stream stays open. A number counts as a regression only against that baseline.
- Check a sample of real API responses for field names and types, not only the status code. Mask personal data and secrets in any response, log or command output you keep. A changed field can still return 200.
- Set the rollback threshold before the deploy, and check that an alert reaches a person. A failed notification counts as a failed check.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
