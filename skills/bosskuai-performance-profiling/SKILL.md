---
name: bosskuai-performance-profiling
description: "Use when investigating why something is slow or growing: CPU/memory profiling, bottleneck diagnosis, query optimization, caching strategy, flame graph reading, and evidence-backed fixes."
---

# Performance profiling

Use when the question is why something is slow or growing, not just "make it faster."

1. **Define the target before touching anything**: the metric (p50/p99 latency, throughput, memory ceiling, cache hit rate) and the number. No target means no "done". Measure on production-shaped data (real volume, types, nulls and key cardinality) from a masked copy of production data. Mask personal fields when the copy is made, keep each column's type, length and null pattern, and keep unique keys unique. A fixture of a thousand rows hides the full scan that a production table makes slow.
2. **Get a reproducible case** — load test, benchmark, specific query, or trace. If you can't reproduce it on demand, any profiling output is noise. Run load tests against a copy, with a rate cap: a load test on the live database can lock rows or fill a queue. For a slow page or feature, first list every screen, endpoint and job under it (list, detail, edit, each tab) and time each one on a masked production data copy, reading what each loads (query count, eager-loaded relations, payload size); the slow part is often not the one named (shared bar section 9).
3. **Profile with the real tool for the stack** instead of guessing: `py-spy`/`cProfile` (Python), `pprof` (Go), `--prof`/Clinic.js/`0x` (Node), async-profiler/JFR (JVM), `EXPLAIN ANALYZE`/`pg_stat_statements`/slow query log (SQL). Profile on the runtime version production runs, because a different version can show a different hot path.
4. **Read the widest bars only.** The hot path is whatever the profiler says, not whatever code looks ugliest.
5. **Write one bottleneck hypothesis backed by the evidence** — slow query, N+1, lock contention, a hot allocation loop, a network call on the hot path, a missing cache — before changing code.
6. **Apply the smallest fix that matches the pattern**: N+1 → batch/eager-load; missing index → add it and re-check the plan; hot-loop allocation → pool or pre-compute; sequential I/O → parallelize/batch; hot recomputation → memoize or cache with an explicit TTL; lock contention → shrink the critical section. A new cache needs a stampede guard (a lock or a single-flight call) and a versioned key, so an expiry does not send every request to the database at once, and a deploy does not read the old format.
7. **Re-run the exact same scenario after the fix** and report the measured before/after delta, not an impression that it feels faster. Check that the output still matches the old code on the same inputs. A faster wrong answer is a bug.
8. **Name the trade-off the fix adds** (staleness, memory, complexity), and check that p99 moved, not only p50 — a p50 win while p99 is still broken is not a fix.

Check before you finish: every recommendation traces to profiler evidence, no cache was added before the bottleneck was confirmed, and nothing off the critical path was "optimized" for free. The fix also needs old and new code to run side by side, and a known rollback path.

Profiling lenses per area and the output template: `reference.md`.

Shared bar: `../../references/checklists/engineering-quality-bar.md`.

## Bounded optimization loop and baselines

- **Set a search budget before trying variants**: max variants, max time, max spend, and the correctness gate that must stay green. Test one hypothesis per variant, on the same input shape.
- **Keep a variant ledger** (variant, hypothesis, command, time, correct?, notes). Compare against the last accepted winner, not only the previous run. Stop when the gain is within noise, correctness fails, the budget is spent, or you change more variables than you can explain. Say "best measured safe variant", not "optimum", unless the search was exhaustive.
- **Promote only when** tests pass, the delta repeats (or is explained), rollback is obvious, and the winning path is in source control or a runbook with exact commands and numbers.
- **Page baselines** (common targets): LCP < 2.5s, INP < 200ms, CLS < 0.1, FCP < 1.8s, TTFB < 800ms, JS < 200KB gzipped. Also count requests and render-blocking resources. **API baselines**: ~100 hits per endpoint for p50/p95/p99, plus a small concurrent run. **Build baselines**: cold build, hot reload, test, typecheck, lint.
- **Realtime paths**: write the path from source event to visible state (provider, ingest, queue, cache, edge, client, render) and time each hop. Also track freshness age and queue depth. Order of fixes: drop round trips, cache stable reads with freshness metadata, batch, split hot and cold paths, add backpressure before queues grow unbounded.
- Do not hide stale data behind fast cache hits, drop validation for speed, or claim millisecond behaviour from client labels without measurement.

Adapted in part from ECC skills/benchmark, skills/benchmark-optimization-loop and skills/latency-critical-systems (affaan-m/ECC, MIT).
