---
name: bosskuai-godot-multiplayer-engineer
description: "Use when building multiplayer in Godot 4: MultiplayerAPI, ENet or WebRTC, MultiplayerSpawner and Synchronizer, RPC modes, server authority, anti-cheat validation, and latency testing."
---

# BosskuAI Godot Multiplayer Engineer

Use this skill to make a Godot 4 multiplayer game authority-correct and hard to cheat, not just "working on localhost".

## How this differs from nearby skills

- **`bosskuai-roblox-systems-scripter`**: the same client-server trust ideas on Roblox/Luau. This skill covers Godot's scene replication API.
- **`bosskuai-realtime-collaboration`**: web sync (WebSocket, CRDT). This skill is game netcode with authority and RPCs.
- **`bosskuai-unity-editor-tool-developer`**: Unity editor tooling, not networking.
- **`bosskuai-tenant-isolation-security`**: SaaS tenant separation; the RPC validation habit is similar but the domain differs.

## Workflow

1. Choose the topology: dedicated or host server (peer 1 authoritative), or peer-to-peer with per-entity authority. Draw which nodes are server-owned and which are peer-owned before coding.
2. Set up a network manager (autoload) for create-server, join, disconnect, and the peer connected/disconnected signals. Handle server loss on clients.
3. Spawn networked nodes through `MultiplayerSpawner` only; a manual `add_child()` of a networked node can desynchronise peers. Register spawnable scenes in the spawner.
4. Set authority explicitly on spawned nodes (`set_multiplayer_authority(peer_id)`) and guard state changes with `is_multiplayer_authority()`.
5. Add `MultiplayerSynchronizer` only for state that every peer genuinely needs. Prefer on-change replication for non-physics state, and check that property paths are valid when the node enters the tree (bad paths can fail quietly).
6. RPC design: clients send requests, the server validates and updates state, then confirms. `any_peer` RPCs that touch gameplay state must check the sender ID (`get_remote_sender_id()`), types, ranges, and plausibility (distance, cooldown) inside the function.
7. Choose reliable or unreliable per RPC: critical events reliable, high-frequency input unreliable.
8. Audit every `any_peer` function with garbage and impossible values, and check that one client cannot call something meant for another.
9. Test with simulated latency and packet loss, plus drop and rejoin, and look for orphaned player nodes after disconnect.
10. For browsers, WebRTC needs a signalling server and STUN/TURN; check the current Godot docs because the API and export support change between versions.

## Guardrails

- Godot's multiplayer API names and defaults change; read the documentation for the installed 4.x version.
- Never trust client-reported position, damage, or inventory.
- Do not expose a public server before rate limiting and basic abuse handling exist.
- Read the engine version from `project.godot`, and check Godot's latest stable release notes for multiplayer changes before you use an API.
- A rejoin usually gets a new peer ID. Key player data by a stable account ID, and drop late RPCs from a peer that has already left.
- Test a client that joins mid-match, a host that leaves, and two players claiming one item on the same tick. The server decides once and rejects the second claim.
- Send the build version when a player joins, and reject a mismatch with a clear message. Player data saved by an older build must still load.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Topology: [server/peer, authority map]
Spawn/sync: [scenes, synchronized properties + mode]
RPC table: [name, mode, caller, validation]
Tests: [latency, loss, rejoin, malicious input results]
```

Adapted from agency-agents/game-development/godot/godot-multiplayer-engineer.md (agency-agents, MIT).
