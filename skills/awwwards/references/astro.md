<!-- Generated from tests/astrotest by tests/_gen/build.py; edit there, not here. -->
# Astro

Use Astro when the site is a content-only showcase and motion is the product: a WebGL-heavy
portfolio, a launch microsite, a scroll story with page transitions. It ships static HTML with
minimal JS (about 75 KB gzipped with the full engine, versus about 250 KB on Next.js). Its
ClientRouter lets the leave animation overlap with fetching the next page. Every file below was
built and run under Astro 7.

## Scaffold

```bash
npm create astro@latest <dir> -- --template minimal --add sitemap --install --no-git --skip-houston --yes
cd <dir> && npm i gsap lenis ogl && npm i -D playwright axe-core @astrojs/check typescript
```

```
astro.config.mjs            site URL, sitemap, prefetch
src/layouts/Base.astro      head/SEO, ClientRouter, persisted layers, loader, engine start
src/components/Loader.astro
src/pages/index.astro, work/[slug].astro, 404.astro
src/styles/tokens.css, engine.css (engine.md), site styles
src/motion/setup.ts         global motion: transition, loader format/exit, background, driver
src/engine/                 engine.md files + astro.ts (below) + gl/ (webgl.md, optional)
src/data/site.ts            all content (content.md)
public/robots.txt, favicon.svg, og.png, fonts/
```

## Adapter: `src/engine/astro.ts`

```ts
// Astro adapter (ClientRouter). Call start(setup) once from the layout's <script>.
// The leave animation runs IN PARALLEL with fetching the next page, so transitions add no latency.
import { boot, cleanup, enter, leave, syncFlags } from './index';

let navigating = false;

export function start(setup?: () => void) {
  document.addEventListener('astro:before-preparation', (e) => {
    navigating = true;
    const load = e.loader;
    e.loader = async () => { await Promise.all([leave(), load()]); };
  });
  document.addEventListener('astro:before-swap', () => cleanup());
  document.addEventListener('astro:after-swap', () => {
    syncFlags(); // Astro replaces <html> attributes; restore flags before paint
    document.getElementById('loader')?.remove(); // the loader is first-load only
  });
  document.addEventListener('astro:page-load', () => {
    if (!navigating) return void boot(setup); // first load (boot is idempotent)
    navigating = false;
    enter();
  });
  // Module scripts run after parsing: boot now instead of waiting for the first astro:page-load.
  boot(setup);
}
```

## Layout: `src/layouts/Base.astro`

```astro
---
import { ClientRouter } from 'astro:transitions';
import { site } from '../data/site';
import Loader from '../components/Loader.astro';
import '../styles/tokens.css';
import '../styles/base.css';

interface Props {
  title?: string;
  description?: string;
  image?: string; // absolute or root-relative OG image (1200x630)
  theme?: string; // per-page theme hook, e.g. data-theme="dark"
}
const { title, description = site.description, image = '/og.png', theme } = Astro.props;
const fullTitle = title ? `${title} | ${site.name}` : `${site.name} | ${site.role}`;
const canonical = new URL(Astro.url.pathname, Astro.site ?? site.url).href;
const ogImage = new URL(image, Astro.site ?? site.url).href;
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: site.name,
  jobTitle: site.role,
  url: site.url,
  email: `mailto:${site.email}`,
  sameAs: site.socials.map((s) => s.href),
};
---
<!doctype html>
<html lang="en" transition:animate="none" data-theme={theme}>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{fullTitle}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    <meta name="theme-color" content="#101010" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="sitemap" href="/sitemap-index.xml" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content={fullTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta property="og:image" content={ogImage} />
    <meta name="twitter:card" content="summary_large_image" />
    <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />
    <!-- Font preloads: one <link rel="preload"> per above-the-fold woff2 in /public/fonts -->
    <slot name="head" />
    <!-- Before first paint: flag JS + motion so hidden-until-revealed states never flash. -->
    <script is:inline>
      document.documentElement.classList.add('js');
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('motion');
    </script>
    <ClientRouter fallback="swap" />
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <div id="gl" transition:persist="gl" aria-hidden="true"></div>
    <div id="curtain" transition:persist="curtain" aria-hidden="true"><div class="curtain__panel"></div></div>
    <div id="cursor" transition:persist="cursor" aria-hidden="true"><span data-cursor-label></span></div>
    <Loader />
    <slot name="header" />
    <main id="main" tabindex="-1">
      <slot />
    </main>
    <slot name="footer" />
    <script>
      import { start } from '../engine/astro';
      import { setupMotion } from '../motion/setup';
      start(setupMotion);
    </script>
  </body>
</html>
```
- `transition:persist` keeps `#gl`, `#curtain` and `#cursor` alive, because Astro replaces
  `<body>` on navigation. `transition:animate="none"` on `<html>` disables Astro's own
  crossfade, since the engine owns the transition.
- Fonts: run `font.mjs` (writes to `public/fonts`), paste the `@font-face` blocks into
  `tokens.css` and the preload tags into the head (the `head` slot or inline).

## Loader: `src/components/Loader.astro`

```astro
---
// First-load moment. Restyle per project; keep the data-* hooks the engine reads:
//   [data-loader-count] 000→100 text, [data-loader-bar] scaleX 0→1, [data-loader-out] exits first.
import { site } from '../data/site';
---
<div id="loader" role="status" aria-label="Loading">
  <div class="loader__inner">
    <span class="loader__name" data-loader-out>{site.name}</span>
    <span class="loader__count" data-loader-out data-loader-count>000</span>
  </div>
  <div class="loader__bar" data-loader-bar></div>
</div>
```

## Global motion: `src/motion/setup.ts`

```ts
// Global motion for this site: runs once on the client, before the first page initializes.
import { setLoaderFormat } from '../engine';

export function setupMotion() {
  setLoaderFormat((p) => String(Math.round(p)).padStart(3, '0'));
}
```
Same contract as in Next: runs once on the client, after scroll/GL init and before the first
page. Register `setTransition`, `setLoaderFormat`, `setLoaderExit`, `setBackground` and driver
modules here.

## Config: `astro.config.mjs`

```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Set `site` to the production URL before deploying: canonical, OG and sitemap depend on it.
export default defineConfig({
  site: 'https://example.com',
  integrations: [sitemap()],
  prefetch: { prefetchAll: true, defaultStrategy: 'hover' },
  build: { inlineStylesheets: 'auto' },
});
```
`public/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://<domain>/sitemap-index.xml
```

## Component scripts

Astro bundles each `<script>` once per site and runs it once. Register page work through
`onPage`; never run DOM code at the top level, because it would not re-run after navigation.

```astro
<script>
  import { gsap } from 'gsap';
  import { onPage } from '../engine';
  onPage(() => {
    const el = document.querySelector('[data-marquee]');
    if (!el) return;                     // runs on every page: check presence
    /* ... */
  });
</script>
```

## Pages

- `src/pages/work/[slug].astro` with `getStaticPaths()` from `site.ts`. Pass `title`,
  `description` and `image` to `Base` for per-page SEO.
- `src/pages/404.astro` is the designed 404. Static hosts serve it for unknown URLs, and so do
  `serve.mjs` and `astro preview`.
- Images: Astro's `<Image>` from `astro:assets` (sized, modern formats) for files in
  `src/assets`. GL planes read the rendered `<img>`.

## QA

```bash
npm run build
node $SKILL/scripts/serve.mjs dist --port 4400     # background
node $SKILL/scripts/audit.mjs dist                 # or the URL
node $SKILL/scripts/shoot.mjs http://127.0.0.1:4400/ --nav
```

## Pitfalls

- Astro swaps `<html>` attributes on navigation. The adapter restores the engine flags in
  `astro:after-swap`; if you add your own classes to `<html>`, restore them there too.
- The loader markup is in every page's HTML. The adapter removes it after each swap, so it only
  plays on first load.
- `astro:page-load` also fires on the first load: the adapter ignores it, because `start()`
  boots immediately.
