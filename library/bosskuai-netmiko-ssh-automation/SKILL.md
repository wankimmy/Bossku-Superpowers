---
name: bosskuai-netmiko-ssh-automation
description: "Use when the task explicitly concerns netmiko ssh automation. Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network automation error handling. Use when automating network device access with Python Netmiko, whether collecting state or pushing guarded config changes."
metadata:
  origin: ECC-adaptation
---

# Netmiko SSH Automation — portable workflow

Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network automation error handling. Use when automating network device access with Python Netmiko, whether collecting state or pushing guarded config changes.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-network-bgp-diagnostics`, `bosskuai-dart-flutter-patterns`, `bosskuai-browser-automation`, `bosskuai-cisco-ios-patterns`, `bosskuai-network-config-validation`, `bosskuai-network-interface-health`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Safety Defaults.
2. Read-Only Connection Pattern.
3. Batch Collection.
4. Structured Parsing.
5. Guarded Config Pattern.
6. Review Checklist.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the Python version (`python --version`) and the Netmiko version (`pip show netmiko`) first, and the latest Netmiko release on PyPI at work time. Check each device's software version with its vendor's command (for example `show version` on Cisco and Junos, `display version` on Huawei and H3C, `show system info` on Palo Alto), then the source prerequisites. The source batch example runs `show version` on every device, so run the vendor's command there too. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- Research and review do not authorise signing, trading, booking, purchase or wallet access. Keep any transaction behind an exact operation scope and the user's approval, and never copy or expose private keys.

## Done when

Complete the source “Review Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Test the script on a lab device first, with a wrong password and an unreachable host. Catch `NetmikoTimeoutException` and `NetmikoAuthenticationException`, and log each device's result.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
