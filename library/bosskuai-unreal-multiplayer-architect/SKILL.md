---
name: bosskuai-unreal-multiplayer-architect
description: "Use when building or auditing Unreal Engine multiplayer: server-authoritative design, replication and RPC validation, GameMode/GameState/PlayerState roles, GAS replication, bandwidth profiling and dedicated servers."
---

# BosskuAI Unreal Multiplayer Architect

Use this skill so the server owns game truth, clients feel responsive, and replication cost and cheat surface are measured rather than guessed.

## How this differs from nearby skills

- **`bosskuai-cpp-coding-standards`**: general C++ style. This skill covers Unreal's networking model.
- **`bosskuai-realtime-collaboration`**: web real-time sync, not game replication.
- **`bosskuai-performance-profiling`**: general profiling method; here the tools are Unreal's network profiling.
- **`bosskuai-cybersecurity-risk`**: wider threat review; the RPC audit here is one part of it.

## Workflow

1. Choose the authority model: dedicated server, listen server or peer-hosted. Check the installed engine version, since networking APIs change between releases.
2. Place state by class role: GameMode on the server only; GameState replicated to all for shared world state; PlayerState replicated for per-player public data; PlayerController for the owning client's input and UI.
3. Replicate only state clients need. Use RepNotify when clients must react. Use conditional replication (owner-only, simulated-only) to cut bandwidth. Set per-class update frequency instead of the default.
4. Clients request, the server decides. Every state mutation checks authority.
5. Every game-affecting Server RPC has validation. Reject (and disconnect) only inputs an honest player could never send. Conditions that lag can cause, such as a target already gone, out of range, or a cooldown not yet over, are checked in the implementation: ignore the request and keep the player connected.
6. Use reliable RPCs for gameplay-critical events and unreliable for frequent or cosmetic data. Do not mix per-frame data into reliable calls. Cosmetic effects go through multicast.
7. For GAS: keep the ability system component on the PlayerState so it survives respawn, with the character as avatar. Initialise on both paths: server on possession, client when the PlayerState replicates. Pick the replication mode deliberately.
8. Profile with the engine's network tools at the expected player count and simulated latency. Look at per-class bandwidth and correction frequency.
9. Audit RPCs for cheating: can a client send impossible values, or trigger another player's damage, score or pickup?
10. Configure and package the dedicated server build; verify behaviour on target hardware.

## Guardrails

- No state change without authority checks.
- Set bandwidth and correction targets from measurements on your own game, not borrowed numbers.
- Test at realistic latency before tuning.
- Verify API names against current Unreal documentation for your version.
- Read the exact engine version from `Engine/Build/Build.version` in the installed engine, and check its release notes before you use a networking API.
- Test a client that disconnects mid-RPC, a late join, and a pawn that reaches a client before its PlayerState. Do not assume replication order.
- Check business flaws as well as cheats: send one purchase or pickup request twice, or fire it at the cooldown edge, and confirm it applies once.
- Send the build version at join and reject a mismatch with a clear message. Saves from the last shipped build must still load.

Full quality bar (versions, edge cases, data, deploy, proof): `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Authority model: [type, rationale]
State map: [class, what it holds, replication condition]
RPC table: [name, reliability, validation, ignore cases]
GAS setup: [component owner, init paths, replication mode]
Profile results: [bandwidth per class, corrections, latency tested]
Security audit: [RPC, risk, fix]
```

Adapted from agency-agents/game-development/unreal-engine/unreal-multiplayer-architect.md (agency-agents, MIT).
