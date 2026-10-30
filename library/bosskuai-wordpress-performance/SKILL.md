---
name: bosskuai-wordpress-performance
description: "Use when a WordPress site is slow: profile with Query Monitor and Lighthouse, fix WP_Query and autoload bloat, layer object, page and CDN caching safely, defer assets, optimise images and tune PHP-FPM or opcache."
---

# BosskuAI WordPress Performance

Use this skill to make a WordPress site fast by measuring first, removing waste, and caching at the right layer. Most slow WordPress sites are slow because of what was added to them.

## How this differs from nearby skills

- **`bosskuai-web-performance`**: framework-neutral Core Web Vitals, bundles and CDN work. This skill is WordPress-specific: queries, options, plugins and caching layers.
- **`bosskuai-redis-caching-queues`**: Redis correctness for Laravel-style apps; here Redis or Memcached is the object cache drop-in.
- **`bosskuai-database-engineering`**: indexes and query plans in general.
- **`bosskuai-performance-profiling`**: generic profiling method.

## Workflow

1. Baseline before changing anything: Query Monitor on key templates (query count, time, slow queries, plugin cost), Lighthouse on throttled mobile (LCP, INP, CLS), autoloaded options size, and the current caching stack.
2. Cut database waste first. Bound every user-facing `WP_Query` (`posts_per_page`, avoid `-1`), use `no_found_rows` when not paginating, request only needed fields, remove N+1 patterns, and index columns used in meta or taxonomy filters.
3. Trim autoload: large values that are not needed on every request move to non-autoloaded, and orphaned options from removed plugins are cleaned up.
4. Audit plugins and theme by real per-request cost. Remove or replace the worst offenders and dequeue their assets on pages that do not use them. Prefer subtraction to adding another speed plugin.
5. Layer caching: persistent object cache (verify it is actually hitting), transients for expensive computed data with expirations matched to data volatility, page cache for anonymous HTML, CDN for static assets. A popular transient that expires can be rebuilt by many requests at once, so guard an expensive rebuild with a lock, or serve the old value while one request refreshes it.
6. Exclude dynamic pages (cart, checkout, account, logged-in views) from page and edge caching, and verify the bypass at the edge.
7. Front end: minify, defer non-critical scripts, inline critical CSS, and re-test that menus, forms and scripts still work after each change.
8. Images: correct sizes with `srcset`, modern formats with fallback, explicit width and height, lazy loading below the fold, and the LCP image preloaded and not lazy loaded.
9. Infrastructure: opcache sizing and timestamp validation, PHP-FPM worker count sized to memory, slow log enabled. Check the installed versions with `wp core version` (WP-CLI), `wp plugin list` and `php -v`, then the latest WordPress release at wordpress.org and the PHP support dates at php.net/supported-versions.php, at work time. Use only functions the installed version has. Check the host's built-in caching too.
10. Re-measure against the baseline on mobile and keep a short note of what changed and why.

## Guardrails

- Never optimise blind. Every change has a before and after.
- A cached cart or account page can show one user another's data. Treat it as a privacy defect.
- Backup the site and database before changes, and test on staging. Do not change production plugins, cache settings or database tables without explicit user approval.
- Do not claim a gain from a desktop or lab score alone; check mobile.
- Values from options and post meta usually come back as strings. Cast them before a comparison or arithmetic.
- Run option or table changes on a version check (for example on `plugins_loaded`), not on every request. Test each plugin update on staging, after a fresh backup.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Baseline: [CWV, queries per request, autoload size, cache status]
Findings: [cost source, evidence]
Changes: [query / plugin / cache / asset / image / infra]
Cache safety: [dynamic pages excluded, verified how]
Result: [before and after per metric]
Notes: [what not to undo]
```

Adapted from agency-agents/engineering/engineering-wordpress-performance.md (agency-agents, MIT).
