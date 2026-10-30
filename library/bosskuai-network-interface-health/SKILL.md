---
name: bosskuai-network-interface-health
description: "Use when the task explicitly concerns network interface health. Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, and Linux hosts. Use when an interface shows errors, drops, CRCs, flapping, or a duplex or speed mismatch."
metadata:
  origin: ECC-adaptation
---

# Network Interface Health — portable workflow

Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, and Linux hosts. Use when an interface shows errors, drops, CRCs, flapping, or a duplex or speed mismatch.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-network-setup`, `bosskuai-network-config-validation`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Counter Reference.
3. Diagnosis Flow.
4. CRCs Or Input Errors.
5. Drops.
6. Duplex And Speed.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the software version first with `show version` on routers and switches, and `ethtool -i <interface>` on Linux hosts, then the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Compare interface counters/state across at least two timestamped samples taken a known time apart, since one reading shows no trend. Tie each diagnosis to observed output.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

On Cisco IOS, `clear counters` resets the counters you are comparing. Save a baseline first, and run it only with approval.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
