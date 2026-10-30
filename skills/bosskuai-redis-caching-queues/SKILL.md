---
name: bosskuai-redis-caching-queues
description: Use when Redis, queues, or caching affect correctness or performance. Covers Redis caching, Laravel queues, cache invalidation, locks, rate limits, sessions, Horizon-style worker operations, and queue performance debugging.
---

# BosskuAI Redis Caching and Queues

Use this skill when Redis, queues, caching, sessions, distributed locks, rate limits, or background workers affect correctness or performance.

## How this differs from nearby skills

- **`bosskuai-database-engineering`**: database-backed queues (`SKIP LOCKED`) and the slow query a cache would hide.
- **`bosskuai-performance-profiling`**: proves a cache is needed.
- **`bosskuai-aws-deployment`**: ElastiCache and SQS provisioning.

## Operating principles

- Cache only when the source of truth and invalidation rule are clear.
- Make queued jobs idempotent, observable, and safe to retry.
- Use locks for coordination, not as a substitute for database constraints.
- Separate queue names by priority and workload type.
- Queues, locks, and sessions need `maxmemory-policy noeviction`; caches use `allkeys-lru`. Split them when they share memory, or jobs vanish under pressure. Check the live values with `CONFIG GET maxmemory-policy` and `CONFIG GET appendfsync`, not the config file.

## Checklist

- Versions: `INFO server` returns `redis_version`, the client version comes from `composer.lock` (predis, or the phpredis extension through `phpversion('redis')`), and the Laravel version comes from the composer files. Check the latest stable release on redis.io and in the Laravel release notes, and write down the date.
- Cache key names include tenant/user/context where needed.
- TTL and invalidation rule are defined.
- Job timeout, retry count, backoff, uniqueness, and failure handling are explicit.
- Workers are supervised and can be restarted safely during deployment. Laravel workers keep the code they loaded, so run `php artisan queue:restart` after each deploy (or `php artisan horizon:terminate` when you use Horizon).
- Each job's `timeout` is shorter than the connection's `retry_after` (with a margin), or the job runs twice.
- Long-running jobs chunk work and do not serialize heavy Eloquent models blindly.
- Rate limits protect expensive endpoints and third-party APIs.
- Redis is not publicly exposed and has persistence/backup settings appropriate to its role.

## Guardrails

- Do not cache authorization-sensitive data without tenant/user scoping.
- Do not use cache to hide slow queries before checking indexes.
- Do not rely on Redis as the only durable source of business-critical truth.
- Do not let failed jobs pile up without alerting.

## Output format

```text
Workload: [cache / queue / lock / rate limit / session]
Versions and live settings: [Redis, client, Laravel; maxmemory-policy, appendfsync]
Correctness risk: [main risk]
Recommended pattern: [Laravel/Redis pattern]
Operational settings: [workers, TTL, retry, monitoring]
Verification: [tests/commands/logs]
```

## References

- `../../references/playbooks/bosskuai-redis-caching-queues-playbook.md`
- `../../references/checklists/redis-caching-queues-checklist.md`
- `../../references/checklists/expert-cofounder-stack-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

## Pattern details

- Cache-aside for read-heavy data that tolerates slight staleness; write-through (write the database first, then refresh the cache) when stale reads are not acceptable. Always set a TTL; keys without one grow until memory pressure hits. Match TTL to data: sessions about a day, API response caches minutes, rate-limit keys the window length, short-lived tokens 5-10 minutes.
- Invalidate groups of related keys by registering them under a tag set with its own TTL, then delete the members and the set together.
- A single command is atomic; multi-step flows need a Lua script or MULTI/EXEC. Rate limits: fixed window (INCR plus EXPIRE in one transaction) for low-traffic endpoints, sliding window in a Lua script when accuracy matters.
- Locks: acquire with a unique token via `SET key token NX PX ttl`; release only if the stored token still matches (compare-and-delete in Lua). Set the TTL above the expected job duration and release in `finally`. Single-node locks only; multi-node needs a vetted Redlock implementation, and a lock never replaces a database constraint.
- Pub/Sub is fire-and-forget. Use Streams when you need delivery guarantees, consumer groups or replay: cap length (`maxlen`), read through a consumer group, and acknowledge only after processing succeeds.
- Cache-miss stampede on a cold or just-expired hot key: lock around the refill and re-check the cache after acquiring the lock (a cross-process lock when multiple workers run), or expire early with jitter.
- Avoid `KEYS *` in production (use `SCAN`), blobs above roughly 100 KB (store a reference to object storage), and mass deletes with a broad flush command; scope deletes by key pattern.
- Client config: connection pool sized to the workload with connect and socket timeouts; eviction policy per instance as above.
- Keys and shapes change on deploy. Version a key (for example a `v2:` segment) when its value shape changes, because old entries stay until their TTL. Prefer arrays or scalars for cached values. If you must cache an object, version its key whenever its class is renamed, moved or removed. Otherwise the old class name comes back as an object of `__PHP_Incomplete_Class`, and calls to its methods fail.
- Jobs queued before a deploy keep their class name and data. Renaming or removing the job class makes those jobs fail, so keep the old class until the queue is empty, or drain the queue before the deploy. A job that uses `SerializesModels` reloads its model when it runs; if the row was deleted, the job fails with `ModelNotFoundException`.
- Replication is asynchronous. After a failover, a lock or a queued job that the old primary had acknowledged can be missing. `WAIT` narrows that gap but does not close it, so keep the database as the final guard. With `appendfsync everysec`, a crash can lose about one second of writes.

Adapted in part from ECC skills/redis-patterns (affaan-m/ECC, MIT).
