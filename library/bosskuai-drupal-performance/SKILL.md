---
name: bosskuai-drupal-performance
description: "Use when a Drupal 10 or 11 site is slow: fix cache tags, contexts and max-age instead of disabling caches, tame slow queries and Views, use lazy builders and BigPipe, trim front-end weight, and verify headers behind the CDN."
---

# BosskuAI Drupal Performance

Use this skill to make a Drupal site fast with measured, cause-level fixes. Most Drupal slowness is wrong cacheability metadata, unbounded Views, or an uncacheable block tainting the whole page.

## How this differs from nearby skills

- **`bosskuai-web-performance`**: framework-agnostic Core Web Vitals, bundles, images and CDNs. This skill adds Drupal's cache layers and render pipeline.
- **`bosskuai-performance-profiling`**: general CPU, memory and query profiling method. Use it for non-Drupal bottlenecks.
- **`bosskuai-redis-caching-queues`**: Redis as cache backend and queue; here Redis only fronts Drupal cache bins.
- **`bosskuai-laravel-development`**: another PHP framework; caching APIs differ.

## Workflow

1. Baseline before touching anything: Lighthouse or field data on key templates (mobile, throttled), the slowest queries from the query log or a profiler (Webprofiler, XHProf), cache status, and cache headers.
2. Check cache posture: Internal Page Cache (anonymous), Dynamic Page Cache, BigPipe. List every `max-age: 0` source and find its real cause.
3. Fix cacheability first: correct cache tags (entity, list, config), the narrowest cache contexts, and `max-age` only for genuinely time-bound data. Invalidate caches after the write is saved. If you invalidate first, a request in between can cache the old data again.
4. Isolate truly dynamic output behind a lazy builder or placeholder so the rest of the page stays cached.
5. Database and Views: bound every View (pager or range), load only used fields, use aggregate or count queries instead of loading entities, remove N+1 loads, index `field_*` columns that are filtered or sorted (read `EXPLAIN`).
6. Front end: enable CSS/JS aggregation and confirm nothing broke; defer non-critical assets; responsive image styles with explicit dimensions; lazy-load below the fold but never the LCP image.
7. Infrastructure: opcache sizing, PHP-FPM pool sizing, Redis or Memcache for cache bins, CDN honouring Drupal cache headers. Read the installed versions with `drush status` or `composer show drupal/core`, and `php -v`. Check the latest Drupal release and PHP support dates at drupal.org and php.net at work time, before you change a setting.
8. Verify: edit an entity and confirm the cached render updates; switch role and confirm the right variation; confirm `X-Drupal-Cache` and `X-Drupal-Dynamic-Cache` headers; confirm authenticated responses are not cached publicly at the edge.
9. Re-measure against the baseline and record what changed and why.

## Guardrails

- Never disable a cache to fix stale content; fix the tags.
- Use the Entity Query and Database APIs with placeholders, never string-built SQL.
- Views and field values can arrive as strings, empty arrays or NULL. Check the type before a comparison or a sort.
- Aggressive aggregation or defer order can break layout; test after each change.
- Report before and after numbers; do not claim gains without them.
- Deploy in order: put the new code on disk first, then run `drush updatedb` and `drush config:import` before traffic reaches code that needs them, keep old code working on the new schema, and rebuild caches (`drush cache:rebuild`) after both.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Baseline: [LCP, INP, CLS, slowest queries, cache status]
Cause: [uncacheable block / unbounded View / unindexed field / asset weight]
Fix: [metadata, query, front-end, infra change]
Verification: [headers, invalidation test, before/after]
Risk: [what could regress]
```

Adapted from agency-agents/engineering/engineering-drupal-performance.md (agency-agents, MIT).
