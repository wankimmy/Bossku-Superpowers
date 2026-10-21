# Ship: final checks and deploy

## Before deploy
1. **Production URL everywhere:** set `site.url` in `src/data/site.ts`, plus `metadataBase` in
   Next (it reads `site.url`) or `site` in `astro.config.mjs`. Canonical URLs, OG and the
   sitemap all depend on it. Update the sitemap URL in robots (`robots.ts` in Next,
   `public/robots.txt` in Astro).
2. **OG image:** run the production server, then
   `node $SKILL/scripts/og.mjs http://127.0.0.1:4400/ --out public/og.png`, then rebuild.
   Per-page images are optional: `--out public/og/<slug>.png`, referenced from that page's
   metadata.
3. **Favicon set:** an SVG identity mark (Next: `src/app/icon.svg`; Astro:
   `public/favicon.svg`), plus a 180 px apple-touch icon if possible.
4. **Final QA:** build, then `audit.mjs` → 0 FAIL, then one last `shoot.mjs` pass.

## Deploy
Deploying publishes the site: confirm with the user before running any of these.

| Host | Next.js | Astro (static `dist/`) |
|---|---|---|
| Vercel | `npx vercel --prod` (zero config) | `npx vercel --prod` |
| Netlify | `npx netlify deploy --prod` (Next runtime auto-detected) | `npx netlify deploy --prod --dir dist` |
| Cloudflare | OpenNext adapter (`@opennextjs/cloudflare`), or static export | `npx wrangler pages deploy dist` |
| GitHub Pages | static export only (`output: 'export'`, deploy `out/`) | official `withastro/action` (set `site`/`base`) |

A custom domain from the name (`<name>.studio`, `<name>.design`) reads best for personal sites.

## Hand-off
In the final message, list everything the owner must replace (from `placeholder: true`
entries), where the content lives (`src/data/site.ts`), and how to run, build and deploy.
