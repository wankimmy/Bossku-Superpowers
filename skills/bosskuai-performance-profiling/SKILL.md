---
name: bosskuai-performance-profiling
description: Use this for CPU/memory profiling, bottleneck diagnosis, query optimization, caching strategy, flame graph reading, and turning performance intuition into evidence-backed fixes.
---

# Performance profiling

Use when the question is why something is slow or growing, not just "make it faster."

1. **Define the target before touching anything**: the metric (p50/p99 latency, throughput, memory ceiling, cache hit rate) and the number. No target means no "done".
2. **Get a reproducible case** — load test, benchmark, specific query, or trace. If you can't reproduce it on demand, any profiling output is noise.
3. **Profile with the real tool for the stack** instead of guessing: `py-spy`/`cProfile` (Python), `pprof` (Go), `--prof`/Clinic.js/`0x` (Node), async-profiler/JFR (JVM), `EXPLAIN ANALYZE`/`pg_stat_statements`/slow query log (SQL).
4. **Read the widest bars only.** The hot path is whatever the profiler says, not whatever code looks ugliest.
5. **Write one bottleneck hypothesis backed by the evidence** — slow query, N+1, lock contention, a hot allocation loop, a network call on the hot path, a missing cache — before changing code.
6. **Apply the smallest fix that matches the pattern**: N+1 → batch/eager-load; missing index → add it and re-check the plan; hot-loop allocation → pool or pre-compute; sequential I/O → parallelize/batch; hot recomputation → memoize or cache with an explicit TTL; lock contention → shrink the critical section.
7. **Re-run the exact same scenario after the fix** and report the measured before/after delta, not an impression that it feels faster.
8. **Name the trade-off the fix adds** (staleness, memory, complexity), and check that p99 moved, not only p50 — a p50 win while p99 is still broken is not a fix.

Check before you finish: every recommendation traces to profiler evidence, no cache was added before the bottleneck was confirmed, and nothing off the critical path was "optimized" for free.

Profiling lenses per area and the output template: `reference.md`.
