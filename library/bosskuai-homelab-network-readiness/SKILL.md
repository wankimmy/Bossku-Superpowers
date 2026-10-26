---
name: bosskuai-homelab-network-readiness
description: "Use when the task explicitly concerns homelab network readiness. Readiness checklist for homelab VLAN segmentation, local DNS filtering (Pi-hole, AdGuard Home), and WireGuard-style remote access. Use when planning or reviewing home network changes — splitting a flat network into trusted, IoT, guest, or management VLANs, moving DHCP to a local resolver, or adding VPN access — before changing router, firewall, DHCP, or VPN configuration."
metadata:
  origin: ECC-adaptation
---

# Homelab Network Readiness — portable workflow

Readiness checklist for homelab VLAN segmentation, local DNS filtering (Pi-hole, AdGuard Home), and WireGuard-style remote access. Use when planning or reviewing home network changes — splitting a flat network into trusted, IoT, guest, or management VLANs, moving DHCP to a local resolver, or adding VPN access — before changing router, firewall, DHCP, or VPN configuration.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-vlan-segmentation`, `bosskuai-homelab-pihole-dns`, `bosskuai-homelab-wireguard-vpn`, `bosskuai-homelab-network-setup`, `bosskuai-network-config-validation`, `bosskuai-network-interface-health`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Safety Rules.
2. Required Inventory.
3. VLAN And Trust-Zone Plan.
4. DNS Filtering Readiness.
5. Remote Access Readiness.
6. Change Sequence.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Review Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
