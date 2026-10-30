---
name: bosskuai-realtime-collaboration
description: "Use when building realtime or collaborative features: WebSocket/SSE sync, presence, CRDT or OT editing, offline-first queues, reconnect and resume, and fan-out scaling, where convergence and no lost or duplicate edits matter."
---

# BosskuAI Realtime Collaboration

Use this skill when several clients edit or watch shared state live and the network can drop, reorder, or duplicate messages. "Use WebSockets" is the start of the design, not the answer.

## How this differs from nearby skills

- **`bosskuai-redis-caching-queues`**: Redis caches, queues, and locks. Pub/sub or presence keys may use Redis, but the sync protocol and convergence model live here.
- **`bosskuai-kotlin-ktor-patterns`**: WebSocket routing and plugins in Ktor. This skill is framework-independent protocol design.
- **`bosskuai-database-engineering`**: transactions, locking, and constraints for durable storage of the op log.
- **`bosskuai-canary-watch`**: post-deploy checks of SSE endpoints, not designing sync.
- **`bosskuai-observability-sre`**: general metrics. The realtime-specific signals are listed below.
- **`bosskuai-expo-react-native`**: mobile offline storage in general. Use this skill for the sync and conflict rules.

## Principles

- Design reconnect before connect. Clients track the last applied server sequence number and resume from it. A connection that cannot resume loses data.
- Every operation is idempotent, keyed by a client-generated id. Applying it twice is a no-op on server and clients.
- The server owns ordering. Use server sequence numbers or logical clocks, not client wall clocks.
- Choose the convergence model per data type:
  - rich text: a CRDT library or server-side OT; do not hand-roll merge logic
  - form fields and status: server-arbitrated last-writer-wins with a version check
  - counters: send the increment operation, not the computed total
  - ordered lists: fractional indexing with a server tiebreak
  - cursors and selections: ephemeral broadcast
- Presence is ephemeral, documents are durable. Separate channels. Presence uses a TTL, is coalesced, and may be dropped without harm. Dropping all presence messages must break nothing durable.
- Bound every queue. A slow consumer gets coalesced state and a resync, not unbounded buffering.
- Deploys drain connections, send reconnect hints, and clients use exponential backoff with jitter to avoid a reconnect storm.
- Version the protocol, and read the sync library's version from the lockfile. A client and server on different versions may not interoperate. The handshake carries the protocol version; keep the previous version working while any such client runs.
- Connections die quietly. Load balancers and proxies often close idle connections after about 60 seconds by default, so heartbeat more often than the shortest idle timeout on the path.
- Auth can expire while a socket stays open. Check the token again on reconnect and on a timer, and close the socket when it expires.
- Single writer per room (rooms sharded across nodes) makes ordering simple. Add a pub/sub backplane when measurement says one node is not enough.
- Offline-first is a data-model decision. Decide whether a simple version-check-and-retry is enough before adding a sync engine.

## Workflow

1. Label every field: durable or ephemeral, convergent or arbitrated, hot or cold.
2. Write the consistency contract: what users see during a partition, what "saved" means, which conflicts show in the UI.
3. Build the append-only per-room op log, server sequencing, client ack, and resume before any UI polish.
4. Pick convergence machinery per field using the list above.
5. Add presence on a separate path.
6. Run the hostile-network suite (below) in CI.
7. Load-test one hot room and many small rooms separately; they fail differently.

## Hostile-network tests

- Kill the socket mid-operation, reconnect: applied exactly once, no gap.
- Long offline period with a queue of ops, then reconnect: replays in order and converges with remote edits.
- Two clients edit the same range at once: identical final state, no silent loss.
- Server deploy during a session: clients reconnect without lost ops or a herd.
- Slow consumer on a busy room: server memory stays bounded.
- Replay real-shaped ops (long text, emoji, right-to-left text) in a room at its real peak size, and run an old protocol client against the new server.

## Signals to watch

Connection churn, resume success rate, op-apply latency, duplicate-apply count, and sampled state-hash comparison across replicas to catch divergence.

## Output format

```text
State classification: [field -> durable/ephemeral, model]
Protocol: [sequence, ack, resume, dedupe key]
Scaling plan: [room sharding, backplane, backpressure]
Failure tests: [list run and results]
Open risk: [what is unproven]
```

## References

- `../../references/checklists/engineering-quality-bar.md`: the shared bar.

Adapted from agency-agents/engineering/engineering-realtime-collaboration-engineer.md (agency-agents, MIT).
