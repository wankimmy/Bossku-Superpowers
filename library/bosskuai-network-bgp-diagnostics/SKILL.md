---
name: bosskuai-network-bgp-diagnostics
description: "Use when the task explicitly concerns network bgp diagnostics. Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence collection. Use when a BGP neighbor is down, routes are missing, or prefix policy and AS path need inspection."
metadata:
  origin: ECC-adaptation
---

# Network BGP Diagnostics — portable workflow

Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence collection. Use when a BGP neighbor is down, routes are missing, or prefix policy and AS path need inspection.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-netmiko-ssh-automation`, `bosskuai-operations`, `bosskuai-documentation-lookup`, `bosskuai-cisco-ios-patterns`, `bosskuai-network-config-validation`, `bosskuai-network-interface-health`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Read-Only Triage Flow.
2. State Interpretation.
3. Transport Checks.
4. Route Policy Checks.
5. AS Path And Prefix Review.
6. Parser Pattern.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Record relevant neighbour state, policy/route evidence and supported root-cause hypothesis using read-only commands; no config change is implied.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
