# Pack routing

Which skill takes which kind of task, pack by pack. `bossku skills find` and the prompt hint already apply these routes; read this table when routing is unclear or a host has no hint. Vendored packs are listed in [`skills/vendored.json`](../skills/vendored.json) and credited in [`third-party.md`](third-party.md).

| Task | Primary skill(s) |
|---|---|
| Any website, landing page, portfolio or marketing UI (default: Awwwards style) | `bosskuai-taste` house rule (depth: `awwwards-web-design` or `awwwards`; `taste-skill`/`hallmark` only by name); score with `jury`; gate `antislop` + `antislop-ui` |
| Final anti-AI-slop audit for UI, mobile, copy, comments, or code | antislop — `antislop` plus only the relevant specialist skill(s) |
| Large logs, files, searches, or tool output exhausting context | `bosskuai-headroom` (runtime installed/configured separately) |
| Soft / minimal / brutalist UI direction | taste-skill — `soft-skill`, `minimalist-skill`, or `brutalist-skill` |
| Redesign existing UI | `bosskuai-taste` (marketing sites) or `redesign-skill` (app UI) |
| Screenshot / mockup / Figma → code; dashboards and app screens | `bosskuai-ui-ux-design-to-code` with the Awwwards craft bar (`image-to-code-skill` and `imagegen-*` only when an image-generation tool is available) |
| Marketing, CRO, SEO, copy, GTM | marketingskills: start with `product-marketing`; primary by request: `seo-audit` (fix SEO), `ai-seo` (AI citations), `ads` / `ad-creative` (paid), `analytics` (tracking), `ab-testing`, `launch`, `competitor-profiling`, `antislop-copywriting` (de-AI copy); `bosskuai-*` marketing skills are one-pass strategy and readiness gates |
| Brainstorm → plan → execute → verify process | superpowers — `brainstorming`, `writing-plans`, `subagent-driven-development` / `executing-plans`, `verification-before-completion` (TDD: `bosskuai-tdd-loop`; debugging: `bosskuai-diagnose-loop`) |
| Codebase map, call tracing, where-does-X-live (source code) | `graft` (requires `@nanonets/graft` CLI + `graft build`) |
| Mixed-media corpus → knowledge graph (docs, papers, video, Neo4j/Obsidian export) | `graphify`, only when `graphify-out/` exists or the user asks for a graph (requires `graphifyy` CLI); ordinary codebase questions go to `bosskuai-project-understanding` or `graft` |
| Agent drives a live browser (navigate, fill, extract) | `browser-use` (`remote-browser` when sandboxed); Playwright suites in the repo: `e2e-testing`; QA smoke, visual regression, or scraping report: `bosskuai-browser-automation` |
| Browser Use Cloud API/SDK or the `browser_use` Python library | `cloud` / `open-source` (`x402` is excluded: it handles wallet keys and moves money) |
| Office/PDF/HTML → Markdown | `markitdown` (requires `markitdown[all]` pip package) |
| Structured PDF extraction, scanned OCR, tables, bounding boxes, or citation-ready RAG | `odl-pdf` (OpenDataLoader runtime installed separately; use `markitdown` for generic conversion) |
| Factual answers from documents, citations, accuracy or hallucination concerns | `bosskuai-grounding` (always on; + `bosskuai-deep-research` for multi-source synthesis, `odl-pdf` for citation-ready PDF extraction) |
| Agent loops: CI/PR/issue sweeps, budgeted triage | loop-engineering — `loop-triage`, `loop-verifier`, `minimal-fix` (+ pattern skills: `ci-triage`, `pr-review-triage`, etc.); release notes: `draft-release-notes` has no local contract, so follow `bosskuai-github-workflow` (Releases and dependencies) |
| Interactive isometric SVG explainer figure (a concept drawn as a physical machine, optional WebGL/3D) | `anatomy` (library-only; needs Node 20.10+ and Chrome for its checks) |
| Security pass on any change: loopholes or gaps across business flow, design, code, data, supply chain, infra, AI agents; latest CVEs and advisories | `bosskuai-security-gate` (always on; + `bosskuai-cybersecurity-risk` for the code layer, `bosskuai-business-logic-review` for deep workflow review) |
| Full codebase security audit or pen test | `security-audit` (library-only) |
| Logo, wordmark, monogram, app icon or favicon design, critique or redesign (SVG, brief to kit) | `logo-design` (library-only; Python 3 scripts; image-generated brand boards: `brandkit`) |
| One web technique (reveal, scroll scene, shader, mood system) | `mengto` library skills via `bossku skills find` |
| Scroll-scrub fly-through / diorama cinematic landing | `scroll-world` (Higgsfield + portable scrub engine; not generic GSAP-only heroes) |
| Agent shell/git safety / destructive command hooks | `dcg` (Destructive Command Guard; install upstream binary separately) |
| Motion craft / easing / gesture / UI polish | emil-skills — `animate` to build (`animate-expo` in Expo), `apple-design` for drag/sheet/momentum physics, `/review-animations` to critique (user-invoked; a model-run critique uses `emil-design-eng`'s Before/After/Why table), `improve-animations` to audit a codebase; never load `animate` and `emil-design-eng` together |
| Frontend library choice (toast, DnD, charts, OTP, …) | `/pick-ui-library` (user-invoked) |
| UI variant exploration behind a live picker | `/prototype` (user-invoked); model-run: `bosskuai-throwaway-prototype` (its UI.md builds switchable variants); `bosskuai-rapid-prototype` for MVP scaffolds |
| Sonner toasts / Swift or SwiftUI code | emil-skills — `ask-sonner`, `write-swift` |
| Reader wants action-first, numbered, no-preamble answers | `i-have-adhd` (explicit `/i-have-adhd`; persists until "stop adhd mode" / "normal mode"); the model cannot load it, so suggest `/i-have-adhd` and use `bosskuai-token-saver` meanwhile |
| Schema, index, and query-plan design; online migrations incl. Laravel/MariaDB | `bosskuai-database-engineering` |
| MySQL/MariaDB engine specifics (InnoDB, replication, pools) | ecc — `mysql-patterns` |
| ORM migration files (Prisma, Drizzle, Kysely, Django, golang-migrate) | ecc — `database-migrations` |
| Python code or pytest | ecc — `python-patterns`, `python-testing` |
| Vue 3 / Pinia outside Nuxt | ecc — `vue-patterns` (`bosskuai-nuxt-development` for Nuxt) |
| Verify actual product behavior, signup/checkout journeys, or CLI smoke checks | `bosskuai-product-verification`; delivery remains `bosskuai-engineering-delivery` |
| `/learn`, auto-learn pass, turning a session's lesson into a learned skill, consolidating learned skills | `bosskuai-learn` (decisions and facts stay `bosskuai-continuous-learning` + `bossku remember`) |
| Hindsight retain/recall/reflect, bank isolation, or memory integration | `bosskuai-hindsight-memory` (optional runtime); local Markdown remains `bosskuai-permanent-memory-orchestration` |
| Cypress tests: `cypress.config` files, `cy.*` commands, Cypress spec runs | `bosskuai-cypress`; Playwright suites stay with `e2e-testing` |
| Build an MCP server, Playwright E2E, WCAG 2.2 audit, ADR, error/retry design | ecc — `mcp-server-patterns`, `e2e-testing`, `accessibility`, `architecture-decision-records`, `error-handling` |

To change a vendored skill's routing, edit `CURATED_TRIGGERS` in [`bossku/index.py`](../bossku/index.py) rather than its text, then run `bossku skills index`.
