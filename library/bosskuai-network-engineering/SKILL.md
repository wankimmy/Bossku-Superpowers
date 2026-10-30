---
name: bosskuai-network-engineering
description: "Use when changing or debugging enterprise routers, switches, and firewalls across vendors (Cisco, Juniper, Palo Alto, Huawei, H3C, Ruijie, Hillstone): capture state, change plan, rollback, and per-layer fault isolation."
---

# BosskuAI Network Engineering

Use this skill to plan and troubleshoot multi-vendor network changes with evidence from device state. Syntax differs by vendor and release, so state the platform first.

## How this differs from nearby skills

- **`bosskuai-cisco-ios-patterns`**: Cisco IOS and IOS-XE configuration patterns. This skill adds other vendors and the change and troubleshooting method.
- **`bosskuai-network-config-validation`**: static pre-deployment checks of a config. Run it on the config this workflow produces.
- **`bosskuai-network-bgp-diagnostics`** and **`bosskuai-network-interface-health`**: deeper BGP and interface counter diagnosis, used inside step 3 below.
- **`bosskuai-homelab-network-setup`**: small home and lab networks, not production change windows.
- **`bosskuai-incident-response`**: coordination of a live incident around the technical fix.

## Workflow

1. Identify vendor, OS family, model, and release (version commands first). Do not assume a command from one stack works on another; commit and save models differ (running config persisted at once, explicit save, commit step).
2. Discover intent and topology: sites, VLANs, VRFs or virtual routers, zones, routing protocols, NAT points, failover paths, maintenance constraints, and the out-of-band or console path.
3. Capture current state before touching anything: configuration, neighbours and adjacencies, routing and forwarding entries, interface counters and errors, session and NAT tables, recent logs.
4. Isolate the fault domain in order: physical and link, layer 2, layer 3 routing, policy and NAT, DNS, application, and asymmetric return path. Verify the control plane (route present) and the data plane (packets leave the right interface, firewall session exists) separately.
5. Design the change: exact vendor commands, expected state transitions, validation commands, and the exact rollback commands or restored config. Apply low-risk prerequisites first and preserve management access.
6. Firewalls: least-privilege rules with named sources, destinations, applications, and ports; order matters; check NAT and return path together; use the vendor's policy-simulation or packet-trace tool before and after.
7. Execute in the approved window, validate end to end from real source to destination, then persist the configuration using that vendor's method.
8. Record commands run, outputs observed, remaining risk, and follow-up monitoring.
9. Compliance-driven environments (for example China MLPS 2.0 or similar schemes): zone separation, deny-by-default policy, central logging with synchronised time, disabled insecure management protocols, and tracked vendor advisories. Confirm the current requirements with the assessor and official documents.

## Guardrails

- Never apply a change to production without a rollback and a maintenance context. Disruptive actions (debug, captures, interface resets, route clears, HA failover, commits) need explicit approval.
- Command names and defaults vary by model and release; verify with the device's help or the vendor docs, and say when a feature is model-dependent.
- Do not paste live credentials, SNMP strings, or keys into notes.
- Record the software version first: `show version` on Cisco and Junos, `display version` on Huawei and H3C, `show system info` on Palo Alto. Check the vendor's latest stable release and its known-bug notes at work time, before any upgrade.
- Back up the running config before the change. Change one device or site first, check it, then the rest. Once the change is approved, use the vendor's timed or confirmed commit where it exists, such as Junos `commit confirmed` (there is no cancel command, so a plain `commit` before the timer ends makes it permanent) or IOS `reload in` (stop it with `reload cancel` once the checks pass, and do not save before then), so a bad change undoes itself.
- Check that the management path does not use the interface or route you are changing. A lockout found after the change is an outage.
- Two engineers working on one device can undo each other's work. Confirm who owns the change window before you start.
- No lab device or config copy? Ask the user to prepare one before the change.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Platform and release: [..]
State captured: [commands, key findings]
Fault domain and evidence: [layer, observation]
Change plan: [commands] Validation: [commands, expected] Rollback: [commands]
Blast radius: [..]
Final state and follow-up: [..]
```

Adapted from agency-agents/engineering/engineering-china-network-engineer.md and agency-agents/engineering/engineering-network-engineer.md (agency-agents, MIT).
