<!-- Generated from tests/nexttest by tests/_gen/build.py; edit there, not here. -->
# Next.js (App Router)

The default stack. Every file below was built and run under Next 16 with React 19, including
the transitions, back/forward navigation, the 404 and the WebGL planes. Next ships version-matched
docs in `node_modules/next/dist/docs/`; read the relevant guide whenever an API looks different
from what you remember.

## Scaffold

```bash
npx create-next-app@latest <dir> --ts --app --src-dir --eslint --no-tailwind --import-alias "@/*" --use-npm --yes
cd <dir> && npm i gsap lenis ogl && npm i -D playwright axe-core
```
Delete the starter page styles and assets. Tailwind is fine if the user or project uses it;
tokens then become `@theme` variables with the same names.

```
src/app/layout.tsx          flags script, persistent layers, loader, header, <Motion /> last
src/app/fonts.ts            next/font declarations
src/app/globals.css         tokens + engine.css (engine.md), then site styles
src/app/page.tsx, work/[slug]/page.tsx, not-found.tsx, sitemap.ts, robots.ts, icon.svg
src/components/Motion.tsx   client wrapper: <Engine setup={setupMotion} />
src/motion/setup.ts         global motion: transition, loader format/exit, background, driver
src/engine/                 engine.md files + next.tsx (below) + gl/ (webgl.md, optional)
src/data/site.ts            all content (content.md)
```

## Adapter: `src/engine/next.tsx`

A capture-phase click listener intercepts internal links: plain `<a>` and `next/link` (which
stands down when `defaultPrevented` is set). It plays the leave animation while prefetching,
cleans up, then pushes. A `usePathname` effect runs `enter()` once the new page is committed.
Back/forward skips the curtain.

```tsx
'use client';
// Next.js App Router adapter. Render <Engine setup={…} /> once, as the LAST child of <body> in the
// root layout (React runs child effects first, so page components register before the engine boots).
// `setup` (global motion: transition, loader, background, driver) must come from a client module.
// Internal links (plain <a> or next/link) get the leave → push → enter transition automatically.
// Opt a link out with data-no-transition. Back/forward re-inits the page without the curtain.
import { useEffect, useRef } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { boot, cleanup, enter, leave, onPage, type PageFn } from './index';

export function Engine({ setup }: { setup?: () => void }) {
  const router = useRouter();
  const pathname = usePathname();
  const mode = useRef<'idle' | 'push' | 'pop'>('idle');
  const first = useRef(true);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { boot(setup); }, []);

  useEffect(() => {
    const onClick = async (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = (e.target as Element).closest('a');
      if (!a || (a.target && a.target !== '_self') || a.hasAttribute('download') || a.hasAttribute('data-no-transition')) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname) return; // external, hash or same page
      e.preventDefault(); // next/link sees defaultPrevented and stands down
      if (mode.current !== 'idle') return;
      mode.current = 'push';
      const href = url.pathname + url.search + url.hash;
      router.prefetch(href);
      await leave();
      cleanup();
      router.push(href, { scroll: false });
    };
    const onPop = () => { mode.current = 'pop'; cleanup(); };
    document.addEventListener('click', onClick, true);
    addEventListener('popstate', onPop);
    return () => {
      document.removeEventListener('click', onClick, true);
      removeEventListener('popstate', onPop);
    };
  }, [router]);

  useEffect(() => {
    if (first.current) { first.current = false; return; }
    const pop = mode.current === 'pop';
    mode.current = 'idle';
    enter({ transition: !pop, scrollTop: !pop });
  }, [pathname]);

  return null;
}

/** Component-level page code: runs when the page is ready (after the loader), reverted on leave. */
export function usePage(fn: PageFn) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => onPage(fn), []);
}
```

## Layout: `src/app/layout.tsx`

```tsx
import type { Metadata } from 'next';
import { Header } from '@/components/Header';
import { Motion } from '@/components/Motion';
import { site } from '@/data/site';
import { display, text } from './fonts';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: { default: `${site.name} | ${site.role}`, template: `%s | ${site.name}` },
  description: site.description,
  alternates: { canonical: './' },
  openGraph: { type: 'website', siteName: site.name, images: ['/og.png'] },
  twitter: { card: 'summary_large_image' },
};

// Runs before first paint: hidden-until-revealed styles only apply when JS and motion are on.
const flags = `document.documentElement.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion')`;

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: site.name,
  jobTitle: site.role,
  url: site.url,
  email: `mailto:${site.email}`,
};

export default function RootLayout({ children }: LayoutProps<'/'>) {
  return (
    <html lang="en" className={`${display.variable} ${text.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: flags }} />
      </head>
      <body>
        <a className="skip-link" href="#main">Skip to content</a>
        <div id="gl" aria-hidden="true" />
        <div id="curtain" aria-hidden="true"><div className="curtain__panel" /></div>
        <div id="cursor" aria-hidden="true"><span data-cursor-label /></div>
        <div id="loader" role="status" aria-label="Loading">
          <div className="loader__inner">
            <span className="loader__name" data-loader-out>{site.name}</span>
            <span className="loader__count" data-loader-out data-loader-count>000</span>
          </div>
          <div className="loader__bar" data-loader-bar />
        </div>
        <Header />
        <main id="main" tabIndex={-1}>{children}</main>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c') }} />
        <Motion />
      </body>
    </html>
  );
}
```
- `suppressHydrationWarning` on `<html>` is required: the flags script and the engine add classes
  before React hydrates.
- `<Motion />` must be the **last** child of `<body>`. React runs effects children-first, so
  `usePage` registrations in pages happen before the engine boots.
- `#gl`, `#curtain`, `#cursor` and `#loader` live in the root layout, so they persist across
  navigations for free.
- Header with `aria-current`: a client component using `usePathname()`.

## Global motion: `src/components/Motion.tsx` + `src/motion/setup.ts`

```tsx
'use client';
import { Engine } from '@/engine/next';
import { setupMotion } from '@/motion/setup';

export function Motion() {
  return <Engine setup={setupMotion} />;
}
```
```ts
// src/motion/setup.ts (example: iris transition from the click point + a scroll-tinted background)
// Global motion for this site: runs once on the client, before the first page initializes.
import { gsap } from 'gsap';
import { ease, setBackground, setLoaderFormat, setTransition } from '@/engine';

const sky = /* glsl */ `
precision highp float;
varying vec2 vUv;
uniform float uScroll;
void main() {
  vec3 top = mix(vec3(0.95), vec3(0.85, 0.88, 0.93), uScroll);
  gl_FragColor = vec4(mix(vec3(0.95), top, vUv.y), 1.0);
}`;

export function setupMotion() {
  setLoaderFormat((p) => `${Math.round(p)}%`);
  let point = { x: innerWidth / 2, y: innerHeight / 2 };
  addEventListener('pointerdown', (e) => { point = { x: e.clientX, y: e.clientY }; });
  setTransition({
    leave: (c) => gsap.timeline()
      .set(c, { autoAlpha: 1 })
      .set(c.querySelector('.curtain__panel'), { yPercent: 0 })
      .fromTo(c.querySelector('.curtain__panel'),
        { clipPath: `circle(0% at ${point.x}px ${point.y}px)` },
        { clipPath: `circle(150% at ${point.x}px ${point.y}px)`, duration: 0.9, ease: ease.inOut }),
    enter: (c) => gsap.timeline()
      .to(c.querySelector('.curtain__panel'), { clipPath: 'circle(0% at 50% 50%)', duration: 0.9, ease: ease.inOut })
      .set(c, { autoAlpha: 0 }),
  });
  const bg = setBackground(sky);
  if (!bg) document.documentElement.style.background = '#f2f2f2';
}
```
`setupMotion` runs once on the client, after scroll and GL init and before the first page. It
is the only safe place for code that touches `window` at setup time. Never put DOM code at the
top level of a module: `'use client'` modules also run on the server.

## Component-level motion: `usePage`

```tsx
'use client';
import { useRef } from 'react';
import { gsap } from 'gsap';
import { onScroll } from '@/engine';
import { usePage } from '@/engine/next';

export function Marquee({ text }: { text: string }) {
  const track = useRef<HTMLDivElement>(null);
  usePage(() => {
    const loop = gsap.to(track.current, { xPercent: -50, ease: 'none', duration: 20, repeat: -1 });
    const off = onScroll(({ velocity }) => {
      gsap.to(loop, { timeScale: (velocity < 0 ? -1 : 1) * (1 + Math.min(Math.abs(velocity) / 8, 5)), duration: 0.4, overwrite: true });
    });
    return off;
  });
  return (
    <div style={{ overflow: 'clip', fontSize: 'var(--t-xl)', whiteSpace: 'nowrap' }} aria-hidden="true">
      <div ref={track} style={{ display: 'inline-flex', gap: '1em' }}>
        <span>{text}</span><span>{text}</span>
      </div>
    </div>
  );
}
```
`usePage(fn)` registers on mount and runs `fn` once the page is ready (after the loader). Its
tweens and ScrollTriggers are reverted on navigation, and the returned cleanup runs too. Use
refs for targets. Server components just use data attributes (`data-split`, `data-reveal`,
`data-gl`): no client code needed.

## Fonts: `src/app/fonts.ts`

```ts
import { Archivo } from 'next/font/google';
import localFont from 'next/font/local';

// Google families: next/font/google self-hosts them at build time.
export const display = Archivo({ subsets: ['latin'], axes: ['wdth'], variable: '--font-display', display: 'swap' });

// Fontshare (or licensed files): download with `font.mjs ... --next`, which prints this block.
export const text = localFont({
  src: [
    { path: '../fonts/satoshi-400-normal.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/satoshi-700-normal.woff2', weight: '700', style: 'normal' },
  ],
  variable: '--font-text',
  display: 'swap',
});
```
Add every `.variable` to `<html className>`. In tokens:
`--f-display: var(--font-display), system-ui, sans-serif;`. `next/font` handles preloading and
fallback metrics.

## Metadata, sitemap, robots, 404, icons

- `metadata` / `generateMetadata` per page: unique `title` and `description` (the layout's
  `title.template` adds the site name). `alternates: { canonical: './' }` in the layout
  resolves per page.
- OG image: `public/og.png` (1200x630, generate with `og.mjs`, then rebuild), or an
  `opengraph-image.tsx` file convention for per-page images.
- `src/app/sitemap.ts` and `src/app/robots.ts`:

```ts
import type { MetadataRoute } from 'next';
import { projects, site } from '@/data/site';

export default function sitemap(): MetadataRoute.Sitemap {
  return ['/', ...projects.map((p) => `/work/${p.slug}/`)].map((path) => ({ url: `${site.url}${path}` }));
}
```
```ts
import type { MetadataRoute } from 'next';
import { site } from '@/data/site';

export default function robots(): MetadataRoute.Robots {
  return { rules: { userAgent: '*', allow: '/' }, sitemap: `${site.url}/sitemap.xml` };
}
```
- `src/app/not-found.tsx` is the designed 404 (it carries the concept). Static routes with
  `generateStaticParams` + `export const dynamicParams = false` make unknown slugs 404.
- Favicon: `src/app/icon.svg` (file convention), plus `apple-icon.png` if possible.
- JSON-LD: a `<script type="application/ld+json">` in the layout or page, escaped as shown above.

## Pages

```tsx
// src/app/work/[slug]/page.tsx (a case page: static params, metadata, GL hero, next project)
import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { projects, site } from '@/data/site';

export const dynamicParams = false;
export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}
export async function generateMetadata({ params }: PageProps<'/work/[slug]'>): Promise<Metadata> {
  const { slug } = await params;
  const p = projects.find((x) => x.slug === slug);
  return p ? { title: p.title, description: `${p.title} (${p.year}): a case study page used to validate page transitions and the enter animation.` } : {};
}

export default async function Work({ params }: PageProps<'/work/[slug]'>) {
  const { slug } = await params;
  const i = projects.findIndex((x) => x.slug === slug);
  if (i < 0) notFound();
  const p = projects[i];
  const next = projects[(i + 1) % projects.length];
  return (
    <article style={{ padding: '18vh var(--gutter)', display: 'grid', gap: '8vh' }}>
      <h1 data-split="lines" data-intro style={{ fontSize: 'var(--t-xl)', lineHeight: 0.9 }}>{p.title}</h1>
      {p.cover.src ? (
        <figure data-gl data-gl-instant style={{ aspectRatio: '16 / 9' }}>
          <Image src={p.cover.src} alt={p.cover.alt} width={1600} height={1067} loading="eager" fetchPriority="high" sizes="100vw" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </figure>
      ) : (
        <figure data-gl="procedural" data-gl-instant data-seed={p.cover.seed} data-colors={site.glPalette.join(',')} style={{ aspectRatio: '16 / 9' }}>
          <div className="gl-fallback" role="img" aria-label={p.cover.alt} />
        </figure>
      )}
      <p data-split="lines" style={{ maxWidth: '40ch', fontSize: 'var(--t-m)' }}>
        The case page enters behind the curtain, plays its own intro, and reverts cleanly when you leave it again.
      </p>
      <Link href={`/work/${next.slug}/`} style={{ fontSize: 'var(--t-l)' }}>Next project: {next.title}</Link>
    </article>
  );
}
```
- Images: `next/image` with `width`/`height` (or `fill` + a sized parent) and `sizes`. The
  hero/LCP image takes `loading="eager" fetchPriority="high"` (`priority` is deprecated in
  Next 16). GL planes read the rendered `<img>`, so `next/image` works with `data-gl`.
- Inline styles in these examples are for brevity. Real projects use CSS modules or global
  classes from the system.

## Static export (optional)

For a site with no server features, `output: 'export'` in `next.config.ts` produces `out/`.
Deploy it anywhere and QA it with `serve.mjs out`. `next/image` then needs
`images: { unoptimized: true }`, so pre-size and compress images yourself. On Vercel, prefer
the default build: image optimization included.

## QA

```bash
npm run build && npx next start -p 4400          # background; production server
node $SKILL/scripts/audit.mjs http://127.0.0.1:4400/
node $SKILL/scripts/shoot.mjs http://127.0.0.1:4400/ --nav
```
Never QA `next dev`: it is slower, has dev overlays, and runs effects twice in Strict Mode.
The engine is idempotent, but timings and FPS are not representative.

## Pitfalls

- **SplitText vs React re-renders.** Only put `data-split` on text that never re-renders on the
  client (server components, static props). If a client component re-renders split text, React
  throws on the mutated DOM.
- **Don't remove React-owned nodes.** The engine hides the loader instead of removing it.
  Follow the same rule in your own code: hide, or render conditionally from state.
- **No DOM at module level** in anything imported by a client component. Put it in
  `setupMotion`, `usePage`, or effects.
- **Opting out:** `data-no-transition` on a link skips the curtain (downloads, modals, anchors
  handled elsewhere). `target="_blank"`, external, `mailto:` and same-page links are skipped
  automatically.
- **`loading.tsx` / Suspense:** the enter animation runs when the pathname commits. Avoid
  route-level loading UI on showcase pages, or the curtain lifts onto a skeleton.
- **Native alternative:** React's `<ViewTransition>` (docs:
  `node_modules/next/dist/docs/01-app/02-guides/view-transitions.md`) morphs shared elements
  with the browser View Transitions API. It is great for thumbnail → hero morphs. Don't combine
  it with the curtain on the same navigation.
- Bundle baseline: Next + React is roughly 170 KB of gzipped JS before your code; with GSAP,
  Lenis and OGL about 250 KB. Lazy-load anything heavier (`next/dynamic`, `await import()`).
