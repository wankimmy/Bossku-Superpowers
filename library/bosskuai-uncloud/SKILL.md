---
name: bosskuai-uncloud
description: "Use when the task explicitly concerns uncloud. Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices, publishing ports, scaling, inspecting logs, or managing machines and volumes with the `uc` CLI."
metadata:
  origin: ECC-adaptation
---

# Uncloud Cluster Management — portable workflow

Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices, publishing ports, scaling, inspecting logs, or managing machines and volumes with the `uc` CLI.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-homelab-pihole-dns`, `bosskuai-hexagonal-architecture`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Core Concepts.
3. CLI Quick Reference.
4. Machines.
5. Services.
6. Images.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the source prerequisites first. Then check the `uc` CLI version on your machine and the Docker version on each cluster machine. Compare each one live with its latest stable release at work time, never from memory. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Common Workflows” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Tag every image with a version and keep the previous tag, so a rollback can redeploy a known image. Back up volumes before any change that could remove or move them.
- Check that the new containers are healthy before the old ones stop, so users keep getting answers during the switch.
- By default, Docker-published ports bypass ufw, so a ufw rule alone does not close them. Publish a port to the network only when it must be public. Bind every other port to 127.0.0.1 (for example -p 127.0.0.1:5432:5432@host). Docker releases older than 28.0.0 let hosts on the same local network reach 127.0.0.1 ports, so check each machine's Docker version first. From another machine, test that a port meant to stay closed is closed.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
