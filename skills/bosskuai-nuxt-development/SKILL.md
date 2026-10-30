---
name: bosskuai-nuxt-development
description: "Use when the app is Nuxt 3 or 4: rendering modes and routeRules, useFetch/useAsyncData, server routes, runtimeConfig secrets, hydration, and SEO meta, verified against official docs via Context7. Plain Vue components and Pinia go to vue-patterns."
---

# BosskuAI Nuxt Development

Use this skill for building, auditing, or debugging Nuxt 3/4 applications, where the answer depends on Nuxt's rendering model rather than general Vue knowledge.

## How this differs from nearby skills

- **`bosskuai-polyglot-engineering`**: general cross-language guidance; this skill knows Nuxt's specific rendering and data-fetching rules.
- **`bosskuai-performance-profiling`**: profiles a running system; this skill covers Nuxt-specific hydration and payload costs.
- **`bosskuai-ui-ux-design-to-code`**: interface and accessibility work; this skill covers the framework beneath it.
- **`bosskuai-seo-geo`**: SEO strategy; this skill wires the meta, sitemap, and rendering that implement it.
- **`vue-patterns`** (ecc): Vue components, Composition API, and Pinia outside Nuxt; this skill owns Nuxt rendering, data fetching, server routes, and config.

## Ground API details in official docs

Nuxt's API surface moves between versions, and 3 vs 4 differ in directory structure and defaults. Resolve the library through Context7 (`resolve-library-id`, then `get-library-docs`) for the specific composable or config option rather than answering from memory. State the version you targeted.

## Orient before changing anything

1. Read `package.json` for the Nuxt version, and `nuxt.config.ts` for modules, rendering mode, and `routeRules`. The installed version is in the lockfile or `node_modules/nuxt/package.json`; the latest is `npm view nuxt version` (release notes: github.com/nuxt/nuxt/releases).
2. Determine the structure: Nuxt 4 `app/` directory or Nuxt 3 root-level.
3. Identify rendering mode per route: SSR, SSG, ISR, hybrid, or client-only. Many bugs are a route rendering differently than assumed.

## Rules that catch most Nuxt bugs

- `useFetch` for component-bound data; `useAsyncData` when you need control over the key or handler.
- The same call site runs on the server and reuses on hydration. Duplicate fetches usually mean an unstable key.
- Server routes (`server/api/*`) own external API calls and secrets, not page components.
- `useHead` / `useSeoMeta` belong in `setup()`. Inside `onMounted` they never render server-side.
- `routeRules` in `nuxt.config.ts` declares SSR/SSG/ISR/CDN behavior per path.
- Audit the hydration payload: full database rows or secrets serialized into the page are both a leak and a performance cost.
- Hydration mismatches usually come from time, randomness, or browser-only state used during render.
- Server memory is shared by every request. A top-level `let` or a module singleton on the server leaks one user's data into another user's page. Keep per-request data in `useState` (keyed) or `event.context` in server routes.

## Guardrails

- Never expose private keys through `runtimeConfig.public` or a client-visible composable.
- Do not reach for client-only rendering to silence a hydration warning; find the mismatch.
- Do not add a module for something Nuxt already provides natively.
- Confirm which Nuxt major version the code targets before quoting an API.

## Verification

```bash
pnpm nuxt typecheck
pnpm nuxt build --analyze     # bundle composition
pnpm nuxt preview             # production-like local run
```

Check headers with `curl -I` and measure Core Web Vitals on a real device profile, not localhost.

## Output format

```text
Nuxt version: [3.x / 4.x] - Structure: [app/ or root] - Rendering: [per route]
Docs consulted: [Context7 topics, or why not needed]

Findings:
  P0/P1/P2 - [file:line] - [issue] - [fix]

Change plan: [smallest correct change]
Verification: [commands run and result]
```

## References

- `../../references/playbooks/bosskuai-nuxt-development-playbook.md` — audit reference, wrong-way/right-way pairs
- `../../references/playbooks/nuxt-development-detailed-playbook.md` — feature development workflow
- `../../references/checklists/expert-cofounder-stack-checklist.md`
- `../../references/checklists/engineering-quality-bar.md` — the shared bar: versions, data types, scenario walk, deploy and proof.

## More Nuxt checks (verify against the docs for the version in use)
- Hydration: keep the first render deterministic; move `Date.now()`, `Math.random()`, storage reads and browser APIs behind `onMounted`, `import.meta.client`, `<ClientOnly>` or a `.client.vue` component. Use Nuxt's `useRoute()`, not the `vue-router` one, and do not drive SSR markup from `route.fullPath` (URL fragments are client-only).
- `useAsyncData`: use it when the fetcher is not a plain `$fetch`, or when composing several sources. Give it a stable key (a getter keyed on the route param works) and keep the handler free of side effects, since it can run during SSR and hydration.
- Use `$fetch` for user-triggered writes, not for page data that should hydrate from SSR.
- Non-critical data: `lazy: true` (or `useLazyFetch`) and handle `status === 'pending'` in the UI. Use `server: false` only when the data is not needed for SEO or first paint. Trim payload with `pick`.
- `routeRules` per route group, not globally: `prerender` (static at build), `swr` (serve cached, revalidate in background), `isr` (platform dependent), `ssr: false` (client-rendered, for admin areas), `cache`/`redirect` (Nitro level).
- Lazy loading: use the `Lazy` prefix with `v-if` so the chunk loads only when needed, and `hydrate-on-visible` or `defineLazyHydrationComponent()` for below-the-fold interactive UI. Passing new props to a lazily hydrated component forces immediate hydration. Use `NuxtLink` for internal links so routes and payloads prefetch.
- Pass the locale and time zone explicitly to `Intl` and date helpers, on the server and in the browser. A UTC server renders yesterday's date for a Malaysian user before 8 am.
- Race check: make a slow first request and a fast second one (for example, change a route param twice). The page must end on the second result.
- Deploys: an open tab can request `_nuxt/` chunks that the new build replaced. Check how the installed version handles a failed chunk load in its docs, add a reload prompt if it has none, and keep API routes compatible with the previous build.
- Review checklist: first SSR render equals the hydrated render, page data goes through `useFetch`/`useAsyncData`, loading UI exists for lazy data, route rules match SEO and freshness needs.

Adapted in part from ECC skills/nuxt4-patterns (affaan-m/ECC, MIT).
