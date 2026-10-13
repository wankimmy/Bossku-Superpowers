---
name: bosskuai-roblox-systems-scripter
description: "Use when scripting a Roblox experience in Luau: server-authoritative design, RemoteEvent validation, DataStore saves with retry, module layout, and anti-exploit review."
---

# BosskuAI Roblox Systems Scripter

Use this skill to build Roblox game systems where the server is the source of truth and player data is not lost.

## How this differs from nearby skills

- **`bosskuai-godot-multiplayer-engineer`**: the same authority ideas in Godot. This skill covers Roblox's Remote objects, DataStore, and service model.
- **`bosskuai-unity-editor-tool-developer`**: Unity tooling, not runtime netcode.
- **`bosskuai-llm-trading-agent-security`**: untrusted-input handling in a different domain.
- **`bosskuai-redis-caching-queues`**: server-side retry and idempotency patterns in web stacks; Roblox uses its own DataStore service.

## Workflow

1. Split responsibilities: the server owns damage, currency, inventory, and position authority; the client displays state and requests actions.
2. Map every Remote: direction, caller, payload shape, and who validates it. Keep Remote references in one shared module or folder.
3. Validate every `OnServerEvent`: type, range, cooldown, distance, and that the player is allowed to ask. Assume payloads can be garbage.
4. Avoid `RemoteFunction:InvokeClient()` from the server (a bad client can stall the thread) and add a timeout path to `InvokeServer` uses.
5. Persistence: design the key schema and a version field first. Wrap every DataStore call in `pcall` with retry and backoff. Save on `PlayerRemoving` and in `BindToClose`. Respect the documented request budgets and check the current Roblox DataStore limits and error codes. Consider `UpdateAsync` for concurrent-write safety and session locking when a player may load on two servers.
6. Do not load default data over a failed read and then save it; treat a failed load as an error state that blocks save so data is not overwritten.
7. Structure the code as ModuleScripts with `init()` and thin bootstrap Scripts and LocalScripts. Put shared constants in one place.
8. Security review: fire Remotes with impossible values using a test script and confirm the server rejects them; check no server logic or secrets are reachable from the client.
9. Shutdown and stress test: rapid join and leave, server close during sessions, DataStore outage then recovery.

## Guardrails

- Roblox APIs, limits, and best practices change; check the current Creator documentation before using a service or quota.
- Follow Roblox's terms and safety policies, especially for chat, minors, and monetisation.
- Do not test destructive scripts on a live published experience.

## Output format

```text
Authority map: [state -> owner]
Remotes: [name, direction, validation]
Data: [key, schema version, save triggers, retry policy]
Modules: [list + init order]
Exploit tests: [input tried, result]
```

Adapted from agency-agents/game-development/roblox-studio/roblox-systems-scripter.md (agency-agents, MIT).
