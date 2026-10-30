# Performance pitfalls

Recurring traps that cause latency, cost spikes, or collapse under load — tune with profiling; these are common design mistakes.

## Data access

- N+1 queries: a loop that hits the database per item instead of batching or joining.
- Unbounded lists: loading full tables into memory for dashboards or exports.
- Missing or wrong indexes on filters, sorts, and foreign keys used in hot paths.
- Detail endpoints that eager-load every relation "just in case", including large history or ledger tables, so the list is fast and the detail page is slow.

## Caching

- Caching without a clear invalidation story → stale reads or “cache poisoning” from shared keys.
- Caching personalized or authorization-sensitive responses under a key that ignores the user.
- No TTL on “infinite” caches → impossible recovery when bad data is written once.

## Frontend and assets

- Shipping huge JS bundles and images without code-splitting, compression, or modern formats.
- Animations or layout that force main-thread layout thrash (read/write/read cycles in a tight loop).
- Third-party scripts loaded synchronously without performance budgets.

## Async and concurrency

- Blocking the event loop or worker pool with CPU-heavy or synchronous I/O work.
- Unbounded queues for background jobs → memory exhaustion under burst.
- Retry storms: every client retries at once without jitter, amplifying outages.

## Cost at scale

- Per-request calls to paid APIs or LLMs without caching, batching, or tiering.
- Storing and serving large blobs through the application tier instead of object storage + CDN.

## Investigation

- Timing only the URL the user named: "the tenant page is slow" can mean the list, the detail page, the edit form or one tab. List every route under the path and time each one.
- Concluding "it is not in the code" after checking part of the surface. Keep a coverage table and conclude only when every row is checked.
- Skipping evidence already on screen: a first run that printed a method loading 16 relations was the answer.
- Measuring on a small dev database. Use a masked production data copy, or the slow query never shows up.
