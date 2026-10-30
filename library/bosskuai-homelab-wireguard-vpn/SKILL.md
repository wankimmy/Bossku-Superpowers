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
- Check the WireGuard tools version (`dpkg -s wireguard-tools` on Debian or Ubuntu) and the kernel version (`uname -r`) first. WireGuard is in the Linux kernel from 5.6 on, and older kernels need a separate module. Check the latest stable WireGuard release at work time (wireguard.com) before any upgrade. Then check the source prerequisites. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Apply the source “How WireGuard Works”, “Server Setup (Linux)” guidance to the concrete request. Return the resulting homelab wireguard vpn artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Before a change, back up the current WireGuard config with `sudo install -m 600 /etc/wireguard/wg0.conf /root/wg0.conf.bak`. Keep the copy on the host, never in a repo or synced folder, and never paste its PrivateKey line into chat, logs or version control. Then set a timed rollback that restores the backup and restarts the tunnel unless you cancel it. A bad change then undoes itself if you lose access.

Check each peer's latest handshake with `wg show`, and test one client's route to the home network.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
