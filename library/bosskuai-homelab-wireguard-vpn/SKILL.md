---
name: bosskuai-homelab-wireguard-vpn
description: "Use when the task explicitly concerns homelab wireguard vpn. WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home network from mobile and laptop clients. Use when setting up WireGuard for remote access to a home network, or deciding between split and full tunnel routing."
metadata:
  origin: ECC-adaptation
---

# Homelab WireGuard VPN — portable workflow

WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home network from mobile and laptop clients. Use when setting up WireGuard for remote access to a home network, or deciding between split and full tunnel routing.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-network-readiness`, `bosskuai-homelab-network-setup`, `bosskuai-homelab-pihole-dns`, `bosskuai-homelab-vlan-segmentation`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How WireGuard Works.
2. Server Setup (Linux).
3. Generate server keypair — create files with private permissions from the start.
4. Write server config — substitute the actual private key value.
5. Do not store private keys in version control or share them.
6. Scoped forwarding rules: allow VPN traffic in/out, not a blanket FORWARD ACCEPT.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Apply the source “How WireGuard Works”, “Server Setup (Linux)” guidance to the concrete request. Return the resulting homelab wireguard vpn artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
