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
- Check each device's firmware or software version first: `show version` on managed switches, the device list in the UniFi controller, the dashboard on pfSense and OPNsense, and `/system resource print` on MikroTik RouterOS. Check the vendor's latest stable release at work time before any upgrade. Then check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Review Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Back up each device's config before the change. Store each backup outside any git repo and synced folder such as OneDrive, and encrypt it if the device supports that, because it can hold Wi-Fi passwords, admin password hashes and VPN keys. Write the rollback steps down in order. Move one device or one VLAN first, then the rest. Keep one way in that the change cannot cut, such as a wired port or a timed rollback.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
