---
name: bosskuai-unity-multiplayer-engineer
description: "Use when building networked Unity gameplay with Netcode for GameObjects and Unity Gaming Services: server authority, NetworkVariable vs RPC, client prediction, Relay and Lobby, bandwidth, lag tests, and anti-cheat checks."
---

# BosskuAI Unity Multiplayer Engineer

Use this skill to design and review Unity multiplayer code where the server owns truth, clients are untrusted, and the game must feel responsive at real-world latency.

## How this differs from nearby skills

- **`bosskuai-game-designer`**: what multiplayer rules should be; this skill makes them work over a network.
- **`bosskuai-technical-artist`**: render cost and assets, not netcode.
- **`bosskuai-godot-shader-developer`**: a different engine and a rendering topic.
- **`bosskuai-cybersecurity-risk`**: general application security; use it for backend services around the game.
- **`bosskuai-redis-caching-queues`**: backend queues, not in-game replication.

## Workflow

1. Choose the authority model (dedicated server, host-authoritative, or server-authoritative via host) and write down the trade-offs. Set maximum player count and a bandwidth budget per player.
2. Map all replicated state into three kinds: persistent state (`NetworkVariable`), client requests (server RPC), and confirmed one-time events (client RPC). If it persists, it is a variable; if it is an event, it is an RPC.
3. Server owns position, health, score, and item ownership. Clients send inputs, not results. Validate every server RPC input (range, rate, rules, ownership) before it changes state.
4. Movement: apply client prediction for the local player, simulate on the server, and reconcile when the difference exceeds a tolerance. Interpolate remote players between snapshots. Tune tolerances by testing, not by guess.
5. Bandwidth. Do not write a variable every frame; change it only when its value changes. Use custom serialisation for compound structs. Throttle non-critical state. Pool network objects instead of spawning and despawning constantly.
6. Spawning. Register every networked prefab in the prefab list; unregistered prefabs fail at spawn.
7. Unity Gaming Services. Use Relay for player-hosted games so host IPs are not exposed. Lobby holds metadata only (name, ready state, map), not gameplay state. Lobby data can be public by default, so set visibility per field. Keep the lobby alive with heartbeats within the service timeout. Check the current UGS docs for API names and limits.
8. Test under simulated latency, jitter, and packet loss at several levels with 2 to 8 players acting at once to find races. Verify reconciliation recovers state.
9. Anti-cheat review: list every client-to-server call, check each has validation, rate limits, and logging (time, player, action, inputs). Feed malformed data and check it is rejected.
10. Dedicated servers: build headless, containerise, report health and capacity to the orchestrator, and shut down gracefully.

## Guardrails

- Never trust a client value (position, damage, ownership, timing) without server validation.
- Netcode for GameObjects, Relay, and Lobby APIs change between package versions. Check the installed package version and its docs before copying a pattern.
- Do not claim bandwidth, success-rate, or latency targets without measuring with your own tools.
- Do not put UGS keys or secrets in the client build. Do not enable paid cloud services, matchmaking, or multiplayer hosting without explicit user approval.
- Minors and chat or voice features carry safety and privacy duties; check applicable rules.

## Output format

```text
Authority model and reasons: [text]
Replicated state map: [state, mechanism, frequency]
RPC list: [name, direction, validation]
Prediction/reconciliation plan: [tolerance, interpolation]
UGS setup: [Relay, Lobby fields and visibility]
Test matrix: [latency, loss, players, results]
Anti-cheat findings: [call, risk, fix]
```

Adapted from agency-agents/game-development/unity/unity-multiplayer-engineer.md (agency-agents, MIT).
