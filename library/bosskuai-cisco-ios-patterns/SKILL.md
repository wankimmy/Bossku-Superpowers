---
name: bosskuai-cisco-ios-patterns
description: "Use when the task explicitly concerns cisco ios patterns. Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe change-window verification. Use when reading, writing, or reviewing Cisco IOS / IOS-XE configuration or planning a change window."
metadata:
  origin: ECC-adaptation
---

# Cisco IOS Patterns — portable workflow

Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe change-window verification. Use when reading, writing, or reviewing Cisco IOS / IOS-XE configuration or planning a change window.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-network-config-validation`, `bosskuai-rust-patterns`, `database-migrations`, `bosskuai-network-interface-health`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Operating Rules.
2. Mode Reference.
3. Read-Only Collection.
4. Wildcard Masks.
5. ACL Placement Review.
6. Interface Hygiene.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the IOS or IOS-XE version first with `show version`. Command support and defaults change by platform and release, so check each command against that version. Check the vendor's latest stable release notes at work time before any upgrade. Then check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Change-Window Verification” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

At the start of the change window, after approval and out-of-band access are confirmed, copy the running config to an approved destination, never `startup-config`, because the copy holds secrets. Then schedule `reload in <minutes>` as a timed rollback, with `<minutes>` long enough for the change and the checks, and answer `no` to any 'System configuration has been modified. Save?' prompt. Make the change and run the checks. Run `reload cancel` only after the checks pass, then confirm with `show reload`. Do not save the change to startup config until the reload is cancelled. The rollback reloads startup-config, so it works only while startup-config still holds the pre-change config.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
