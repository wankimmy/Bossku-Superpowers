---
name: bosskuai-network-config-validation
description: "Use when the task explicitly concerns network config validation. Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale references, management-plane risk, and IOS-style security hygiene. Use when reviewing a router or switch configuration before deployment."
metadata:
  origin: ECC-adaptation
---

# Network Config Validation — portable workflow

Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale references, management-plane risk, and IOS-style security hygiene. Use when reviewing a router or switch configuration before deployment.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-network-readiness`, `bosskuai-cisco-ios-patterns`, `bosskuai-quarkus-verification`, `bosskuai-network-interface-health`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Dangerous Command Detection.
3. Duplicate IPs And Subnet Overlaps.
4. Management-Plane Checks.
5. Security Hygiene Checks.
6. Change-Window Preflight.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the platform and software version first (`show version` on the device, or the output saved with the config), check the vendor's latest stable release at work time, then the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

List config findings with exact lines, management-access impact and rollback requirements; no unapproved deployment occurs.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Test the planned config on a lab device or a copy before the change window, and confirm that the management interface, its VLAN and the route back to the admin host all survive it.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
