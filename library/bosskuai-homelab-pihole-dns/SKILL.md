---
name: bosskuai-homelab-pihole-dns
description: "Use when the task explicitly concerns homelab pihole dns. Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS resolution on a home network. Use when the task explicitly involves Pi-hole — installing it, managing blocklists, configuring DoH or DHCP, adding local DNS records, or diagnosing DNS resolution with Pi-hole in the path."
metadata:
  origin: ECC-adaptation
---

# Homelab Pi-hole DNS — portable workflow

Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS resolution on a home network. Use when the task explicitly involves Pi-hole — installing it, managing blocklists, configuring DoH or DHCP, adding local DNS records, or diagnosing DNS resolution with Pi-hole in the path.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-network-readiness`, `bosskuai-homelab-network-setup`, `bosskuai-homelab-wireguard-vpn`, `bosskuai-homelab-vlan-segmentation`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How Pi-hole Works.
2. Docker (Recommended).
3. docker-compose.yml.
4. Bare-Metal Install (Raspberry Pi OS / Debian / Ubuntu).
5. Step 1: Assign a static IP (edit /etc/dhcpcd.conf on Pi OS).
6. Add at the bottom:.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the Pi-hole version first with `pihole -v`, and the Docker image tag or OS package version if you installed it that way. Check the latest Pi-hole release notes at work time before any upgrade. Then check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Prefer Cloudflare's package repository for automatic signed package verification.”, “If you download a binary directly, pin a release version and verify its checksum.” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Back up Pi-hole first (Teleporter export: Settings > Teleporter > Export). On the Pi, run `unzip -t <backup>.zip` and confirm it reports no errors before you change anything. If the export or this check fails, stop and do not change anything. Decide whether DHCP also gives out a fallback DNS server, since clients lose DNS when Pi-hole is down without one.

After each change, test one allowed name, one blocked name and one local record from a wired and a Wi-Fi client.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
