---
name: bosskuai-web-performance
description: "Use when diagnosing or improving web performance, including Core Web Vitals, Lighthouse, CrUX or RUM, bundles, images, fonts, caching, CDNs, SSR or hydration cost, third-party scripts, and CI performance budgets; use performance profiling for backend CPU or memory."
---

# BosskuAI Web Performance

Use this skill when a page or app feels slow in the browser, when Search Console or Lighthouse flags Core Web Vitals, or when a frontend needs a performance budget before it grows.

## How this differs from nearby skills

- **`bosskuai-performance-profiling`**: server CPU, memory, queries, flame graphs; this skill starts where the response leaves the server.
- **`bosskuai-react-development`** / **`bosskuai-nuxt-development`**: framework correctness; this skill decides what to ship, when, and how much.
- **`bosskuai-seo-geo`**: ranking and discoverability; Core Web Vitals is the overlap, owned here.
- **`bosskuai-aws-deployment`** / **`bosskuai-vps-docker-deployment`**: CDN and caching infrastructure; this skill specifies the headers and edge rules.

## Mindset

- Field data at p75 on real users beats a lab score on a MacBook. Measure on a mid-range Android over 4G.
- The fastest byte is the one not sent; the fastest script is the one not run.
- Budgets, not heroics: a size or vitals budget in CI prevents the regression instead of chasing it.
- Every third-party tag is a performance and privacy decision with an owner.

## Targets (p75, field)

- LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1; TTFB ≤ 800 ms.
- Initial route JavaScript ≤ ~200 KB compressed for content sites, ≤ ~350 KB for apps; set the number per project and enforce it.

## Diagnose

Cover every route under the reported page first (list, detail, edit, each tab), measure each one, and keep a coverage table. Never call a page fine while a route under it is unmeasured (shared bar section 9).

1. Field: CrUX (Search Console, PageSpeed Insights "Discover what your real users are experiencing"), or your own RUM via the `web-vitals` library sent to analytics with route and device.
2. Lab: Lighthouse CI on a throttled profile, WebPageTest filmstrip, Chrome DevTools Performance panel (long tasks, LCP element, layout shift regions), Coverage tab for unused JS/CSS. Each score records `lighthouseVersion` and `userAgent` from the saved Lighthouse JSON report, since an upgrade can move a score with no code change.
3. Bundle: `vite-bundle-visualizer`, `next build` analyzer, `nuxi analyze`; look for duplicate dependencies, whole-library imports, and polyfills for supported browsers.
4. Network: waterfall for render-blocking CSS/JS, late-discovered LCP image, font chains, and third-party tags.

## LCP

- Cut TTFB first: cache the HTML (ISR/SWR at the edge), fix slow queries, put the origin behind a CDN.
- SSR or prerender the LCP element; never client-fetch hero content.
- Hero image: correct `srcset`/`sizes`, AVIF/WebP, `fetchpriority="high"`, `<link rel=preload>`, no `loading="lazy"` above the fold, explicit dimensions.
- Inline critical CSS, defer the rest; `font-display: swap` (or `optional` for non-brand text) and preload the one font file the LCP text uses.
- Subset fonts only to the scripts the page shows. A missing glyph (Chinese, Tamil, some emoji) makes the browser fetch a fallback font, and the text moves when it loads.

## INP

- Break long tasks (> 50 ms): chunk work, yield with `scheduler.yield()` or `setTimeout`, move heavy computation to a Web Worker.
- Trim hydration: fewer client components (RSC, Nuxt islands/lazy hydration), smaller initial state, defer non-critical widgets until idle or interaction.
- Keep handlers cheap: debounce input, avoid synchronous layout reads in handlers, update state in one batch.
- Third-party scripts: load after interaction or via Partytown, consent-gate, remove what nobody reads.

## CLS

- Width/height or `aspect-ratio` on every image, video, iframe, and ad slot; reserve space for late content.
- Font fallback metrics (`size-adjust`, `ascent-override`) so swaps do not shift text.
- Never insert content above existing content without user action; animate with `transform`/`opacity` only.

## JavaScript budget

- Route-level code splitting; dynamic import for editors, charts, maps, and anything below the fold.
- Modern build targets; drop legacy polyfills; check `sideEffects` for tree shaking; replace heavy utilities (moment → date-fns/Temporal, lodash → per-function imports).
- Deduplicate dependencies (`pnpm why`, `npm ls`); one icon strategy; one date library.

## Caching and delivery

- Hashed static assets: `Cache-Control: public, max-age=31536000, immutable`.
- HTML: `no-cache` with ETag, or `s-maxage` + `stale-while-revalidate` at the CDN for public pages.
- Brotli or gzip at the edge; HTTP/2 or HTTP/3; `preconnect` to the API and font origins; avoid redirect chains.
- ISR/SSG for public pages, SSR for personalized, SPA only behind login.
- Service worker only with an invalidation plan; otherwise it becomes the cache you cannot bust.
- Old tabs and cached HTML point at the previous deploy's hashed files. Keep those files for as long as an open tab might request them, or make a failed chunk load reload the page.

## Framework notes

- **Nuxt**: watch the payload size, use `useLazyAsyncData` for non-critical data, `nuxt/image`, `routeRules` with `swr`/`isr`/`prerender`, fix hydration mismatches (time, randomness, browser-only state).
- **Next.js**: keep the `"use client"` boundary low, `next/image`, `next/font`, `dynamic(..., { ssr: false })` for browser-only widgets, streaming with Suspense.
- **React SPA**: prerender or SSR the shell; lazy routes; virtualize lists.
- **Server-rendered (Laravel Blade, Django)**: full-page cache where possible, defer scripts, inline critical CSS, image pipeline.

## Budgets in CI

- Lighthouse CI assertions on key URLs (mobile profile) and `size-limit` or `bundlesize` on the initial chunk, failing the PR on regression.
- RUM dashboard with an alert when p75 LCP or INP regresses after a deploy.

## Workflow

1. Get field data per template (home, listing, detail, app shell) and pick the worst metric.
2. Reproduce in lab with throttling; identify the single biggest contributor.
3. Fix that one thing; measure again; keep or revert (`bosskuai-ratchet-loop`).
4. Set the budget that would have caught it; add it to CI.

## Guardrails

- Do not lazy-load the LCP image or hero content.
- Do not optimize lab scores that field data says are already fine.
- Do not claim "faster" without before/after p75 numbers or a filmstrip.
- Do not add a service worker for caching without an invalidation plan.
- Do not ship a third-party tag without an owner and a measured cost.
- Do not measure a dev build or a page with ten test rows. Use the production build and production-sized data.

## Output format

```text
Page/template: [...] - Field p75: LCP [..] INP [..] CLS [..] TTFB [..]
Biggest contributor: [what, evidence]
Fixes (ordered by impact/effort):
  [change] — [expected metric effect] — [where]
Budget to add: [metric/size, threshold, CI check]
Before/after: [numbers, method]
```

## References

- `../../references/checklists/web-performance-checklist.md`
- `../../references/pitfalls/performance-pitfalls.md`
- `../../references/checklists/seo-geo-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

## React and Next.js rules, in priority order
1. **Waterfalls first.** Check cheap synchronous conditions before awaiting remote data; move an `await` into the branch that uses it; run independent work with `Promise.all`; start promises early and await late; in Server Components split sibling awaits into child components so React runs them in parallel; put `<Suspense>` close to the data and reserve space for late content.
2. **Bundle.** Import from the file, not a barrel `index.ts` (Next's `optimizePackageImports` covers listed packages only); avoid dynamic `import()` paths built from variables; `dynamic()` for heavy components; load analytics and widgets after hydration; preload a route or chunk on hover or focus.
3. **Server.** Treat every `"use server"` function as a public endpoint and authenticate and authorize inside it. Use `React.cache` for per-request dedup and an LRU or `unstable_cache` for cross-request data. Never keep mutable module-level state in RSC or SSR code (shared across users); use request-scoped storage. Pass Client Components only the fields they need. Use `after()` for logging and cache warming after the response.
4. **Client fetching.** Use SWR or TanStack Query for shared data instead of hand-rolled `useEffect` + `fetch`; one shared scroll listener, `{ passive: true }`; version and minimize `localStorage` (it is synchronous).
5. **Re-renders.** Read state used only in callbacks with `getState()` instead of subscribing; subscribe to derived booleans (`cart.length > 0`); derive values during render, not in `useEffect` + `setState`; hoist default non-primitive props and use primitive effect deps; functional `setState`; lazy `useState` initializer; `startTransition` and `useDeferredValue` for non-urgent work; never define a component inside a component. `useMemo` on a cheap primitive is overhead. With React Compiler enabled, manual memoization is review-only.
6. **Rendering.** `content-visibility: auto` with `contain-intrinsic-size` for long lists; animate a wrapper `div`, not the SVG; set theme or locale before hydration with an inline script; `suppressHydrationWarning` only on known-divergent leaf nodes; `{count > 0 ? <X/> : null}` instead of `{count && <X/>}`; React 19 `<Activity>` to hide tabs without unmounting.
7. **Hot paths only:** `Map`/`Set` for repeated lookups, one pass instead of `filter().map()`, hoist RegExp out of loops, min/max by loop not `sort()`.

Metric mapping: LCP is mostly waterfalls and bundle size; INP is re-renders, rendering and JS; CLS is Suspense placement and image dimensions; TBT is bundle size, JS and third-party scripts.

Adapted in part from ECC skills/react-performance (affaan-m/ECC, MIT; itself from Vercel Labs react-best-practices, MIT).
