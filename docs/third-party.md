# Third-party skill packs

Bossku Superpower vendors Agent Skills from these open-source upstream projects. Provenance is tracked in [`skills/vendored.json`](../skills/vendored.json).

| Pack | Upstream | License | Copyright |
|---|---|---|---|
| marketingskills | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | Copyright (c) 2025 Corey Haines |
| superpowers | [obra/superpowers](https://github.com/obra/superpowers) | MIT | Copyright (c) 2025 Jesse Vincent |
| hallmark | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | MIT | Copyright (c) 2026 Hallmark contributors |
| browser-use | [browser-use/browser-use](https://github.com/browser-use/browser-use) | MIT | Copyright (c) 2024 Gregor Zunic |
| graphify | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | MIT | Copyright (c) 2026 Safi Shamsi |
| markitdown | [microsoft/markitdown](https://github.com/microsoft/markitdown) | MIT | Copyright (c) Microsoft Corporation |
| loop-engineering | [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering) | MIT | Copyright (c) 2026 Cobus Greyling and contributors |
| taste-skill | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | Copyright (c) 2026 Leonxlnx |
| scroll-world | [oso95/scroll-world](https://github.com/oso95/scroll-world) | MIT | Copyright (c) 2026 cyw |
| dcg | [Dicklesworthstone/destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard) | MIT with OpenAI/Anthropic rider | Copyright (c) 2026 Jeffrey Emanuel |
| emil-skills | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | Copyright (c) 2026 Emil Kowalski |
| graft | [NanoNets/Graft](https://github.com/NanoNets/Graft) | MIT | Copyright (c) 2026 Context Graph Engine contributors |
| i-have-adhd | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | MIT | Copyright (c) 2026 Ayoub Ghriss |
| ecc | [affaan-m/ECC](https://github.com/affaan-m/ECC) | MIT | Copyright (c) 2026 Affaan Mustafa |
| antislop | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) | MIT | Copyright (c) anti-slop contributors |
| anatomy | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | MIT | Copyright (c) 2026 Ryan |
| logo-design | [kaankiziltug/logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) | MIT (reference logos excluded, see below) | Copyright (c) 2026 kaankiziltug |
| awwwards-web-design | [owenisas/awwwards-web-design](https://github.com/owenisas/awwwards-web-design) | MIT | Copyright (c) 2026 owenisas |
| awwwards-jury | [juliobsz/skills](https://github.com/juliobsz/skills) | MIT | Copyright (c) 2026 Julio (juliobsz) |
| mengto | [MengTo/Skills](https://github.com/MengTo/Skills) | MIT (vendored GSAP/Three runtimes and demo media not bundled) | Copyright (c) 2026 Meng To |
| security-audit | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | MIT | Copyright (c) 2025-2026 Cloudflare, Inc. |
| opendataloader-pdf | [opendataloader-project/opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) | Apache-2.0 | Copyright 2025-2026 Hancom, Inc. (upstream NOTICE; [LICENSE](third-party-licenses/opendataloader-pdf-LICENSE.txt) and [NOTICE](third-party-licenses/opendataloader-pdf-NOTICE.txt) kept here) |
| moli | [lexmount/moli](https://github.com/lexmount/moli) | MIT OR Apache-2.0 (used under MIT) | Copyright (c) 2026 Moli contributors ([MIT text](third-party-licenses/moli-LICENSE-MIT.txt), [Apache text](third-party-licenses/moli-LICENSE-APACHE.txt)) |
| greptile (adapted, first-party) | [greptileai/skills](https://github.com/greptileai/skills) | MIT | Copyright (c) 2026 Greptile AI |
| agency-agents (adapted, first-party) | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | MIT | Copyright (c) 2025 AgentLand Contributors |
| mattpocock/skills (adapted, first-party) | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | Copyright (c) 2026 Matt Pocock |

`moli` vendors the upstream `moli-webfetch` and `moli-cdp-server` skills (the Rust browser itself is not bundled). One local deviation to re-apply on any re-vendor: step 1 of both `SKILL.md` files told the agent to install Moli by piping a remote installer script into a shell; it now says to stop, show the user the install instructions, and continue only after they have installed it or explicitly asked for the installer to be run (the binaries are unsigned and the installer has no checksum check). `moli-websearch` is deliberately not vendored (listed under `excluded`): its references tell the agent to scrape public API keys from third-party frontends and to switch search engines after a CAPTCHA.

`superpowers` has one local addition to re-apply on any re-vendor: `verification-before-completion/SKILL.md` has a section "Match Evidence to the Intended Outcome" (a build or test run supports only the behaviour it covers; for documentation and agent instructions, check how the consumer discovers and loads them; keep local runs, external CI and assumptions apart) and two extra rows in the "Common Failures" table. The upstream text is otherwise unchanged. The 2026-10-12 sync (version 7.0.0, which adds `diagnosing-superpowers`) was copied from a local snapshot of the upstream repository, not fetched from GitHub.

`agency-agents` and `mattpocock/skills` are not vendored: on 2026-10-12 their methods were rewritten as five new first-party skills (`bosskuai-data-pipelines`, `bosskuai-desktop-apps`, `bosskuai-rag-pipelines`, `bosskuai-realtime-collaboration`, `bosskuai-search-relevance`) and short additions to 28 existing first-party skills, each ending with an "Adapted from ..." line. On 2026-10-13 the remaining 137 useful niche workflows from the same audit (GIS, game engines, healthcare and legal operations, China platforms, finance operations and more) were added the same way as library-only skills, with a not-professional-advice guardrail on every regulated domain. Persona text, invented metrics and passages the source credits to others (`pr/CREDITS.md`) were left out. The decisions and source quotes are in [`local-pack-audit-skills-agency.md`](superpowers/plans/local-pack-audit-skills-agency.md); the snapshot was local, not fetched from GitHub.

`markitdown` is a thin Bossku-authored skill that documents the upstream CLI; the Microsoft package is not bundled.

`graphify` upstream no longer keeps a static `SKILL.md` in its repo: the skill is rendered per host by `graphify install`. Bossku Superpower vendors the cross-framework Agent-Skills variant (`graphify/graphify/skill-agents.md`) plus its `skills/agents/references/` sidecar. Re-vendor from those two paths, not from a `skills/` folder.

`ecc` is a curated subset (10 of ~280 skills) chosen to fill gaps in the Bossku library - MySQL/MariaDB, migrations, error handling, MCP servers, Playwright, WCAG 2.2, ADRs, Vue 3, Python, pytest. Each is a single self-contained `SKILL.md` with no ECC-only tooling references; the many agent-stack ECC skills were already ported earlier as `bosskuai-*` skills. On 2026-10-12, 173 more ECC skills (niche stacks such as C++, Rust, GIS, scientific databases and network operations) were added as library-only `bosskuai-*` wrappers listed in `skills/library-only.json`: each `SKILL.md` is a short Bossku workflow that points to the complete upstream skill and its sidecar files, kept unchanged with the MIT licence under `references/upstream/`, and `SOURCE.json` records the source path and SHA-256. They came from a local snapshot, not GitHub; their scripts are reference only and were not run. On 2026-10-13 newer ECC methods that Bossku's earlier ports lacked were appended to 51 first-party skills, each addition ending with an "Adapted in part from ECC skills/..." line; the 11 vendored skills the stocktake also named were left for a re-vendor.

`graft` vendors the upstream `SKILL.md` body verbatim; the CLI itself is not bundled (`npm install -g @nanonets/graft`, then `graft build` per repo). One local deviation: the frontmatter `description` was rewritten to state the `graft/`-index precondition, because upstream ships inside an already-indexed repo and asserts it flatly. Re-apply that edit on the next re-vendor.

`dcg` is a thin Bossku skill that documents the upstream Destructive Command Guard CLI/hooks; the Rust binary is not bundled. Upstream license is MIT **with an OpenAI/Anthropic rider** — read the upstream `LICENSE` before redistributing the binary or derivative works.

`antislop` vendors the upstream six-skill suite unchanged. Bossku adds routing metadata in its generated index rather than rewriting the vendored skill text.

`hallmark` moved from the recorded `togethercomputer/hallmark` (now 404) to `Nutlope/hallmark`; the vendored `SKILL.md` matches it apart from line endings. Its 21-theme catalog lives in upstream `site/css/tokens.css`, vendored at `site/css/tokens.css` because every hallmark link resolves `../../site/css/tokens.css`; `bossku install` copies `site/` next to the installed skills for the same reason.

`greptile` is not a vendored pack: `bosskuai-greptile-review-loop` and `bosskuai-pr-check` are first-party adaptations of `greptileai/skills`, kept under the upstream MIT notice above. Local deviations to re-apply on any resync: `git add` scoped to the files changed for the comments, a test and lint gate plus one ask before the first push, only Greptile-bot threads resolved without a code change (never a human reviewer's), bounded polling loops, paginated inline comments, and no `p4 review` commands (they do not list or mark reviews), and `allowed-tools` limited to read-only `git`, `gh`, `glab` and `p4` commands plus `git add` and `git commit`, so a push, merge or shelve goes through the normal permission prompt.

Deliberately not vendored (recorded under `excluded` in `skills/vendored.json` so a re-vendor leaves them out): `taste-skill-v1`, `gpt-tasteskill`, and `stitch-skill` from the taste-skill pack, and `x402` from browser-use: it prints generated wallet keys and spends from a crypto wallet. It used to stay in `skills/` with `bossku install` skipping it, but the plugin manifests list every folder in `skills/`, so it is no longer shipped at all.

`scroll-world` local deviation to re-apply on any resync: its `allowed-tools` drops the blanket `Bash` grant and pre-approves only `higgsfield workspace`, `higgsfield model`, `ffmpeg`, `ffprobe` and `mkdir`, so `higgsfield generate` (it spends credits) asks first. `bossku validate` rejects a blanket shell grant or a catch-all for a CLI that can push, publish or deploy, in any skill.

`opendataloader-pdf` vendors the complete upstream `skills/odl-pdf/` bundle unchanged. Its maintenance-only sibling is intentionally excluded, and the optional OpenDataLoader runtime is not installed automatically.

## Studied tools and optional runtimes (not bundled)

These projects informed Bossku Superpower's own skills or are offered as opt-in tools through `bossku tools`. No upstream source text is copied unless a row says so; the notices are recorded so that the record stays accurate if text is ever adopted.

| Project | Upstream | License | Copyright | How it is used |
|---|---|---|---|---|
| e2e | [tester-army/e2e](https://github.com/tester-army/e2e) | Apache-2.0 | Copyright 2026 TesterArmy, Inc. (NOTICE: "includes software developed at TesterArmy, Inc.") | `bosskuai-agentic-e2e` is written in our own words from a read of the upstream docs (no code is copied); `npx e2e init` is an opt-in per-project step. Its CLI sends telemetry unless `npx e2e telemetry disable` or `E2E_TELEMETRY_DISABLED=1`. |
| cypress | [cypress-io/cypress](https://github.com/cypress-io/cypress) | MIT | Copyright (c) 2023 Cypress.io | `bosskuai-cypress` is written in our own words from the official Cypress docs, which the skill cites; no code or text is copied. `bossku tools install cypress` is an opt-in per-project npm install. Cypress sends crash reports (exception data) to `api.cypress.io` unless `CYPRESS_CRASH_REPORTS=0` is set ([advanced installation](https://docs.cypress.io/app/references/advanced-installation), "Privacy and messaging"); its separate OpenTelemetry telemetry is off by default (`packages/telemetry/README.md` on the develop branch). |
| headroom | [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | Apache-2.0 | Copyright 2025 Headroom Contributors | `headroom-ai` is an opt-in pip install, never run automatically. It sends an anonymous usage beacon unless `HEADROOM_BEACON=off` or `DO_NOT_TRACK=1`. |
| archify | [tt-a1i/archify](https://github.com/tt-a1i/archify) | MIT | Copyright (c) 2026 tt-a1i (Archify); Copyright (c) 2025 Cocoon AI | `bosskuai-archify-diagrams` documents the upstream CLI; the runtime is not bundled. Its update check contacts a GitHub Pages URL by default. |
| hindsight | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | MIT | Copyright (c) 2025 Vectorize AI, Inc. | `bosskuai-hindsight-memory` is first-party; the CLI is an opt-in install. |
| claude-code-best-practice | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | MIT | Copyright (c) 2025-2026 Shayan Rais | Reviewed in [claude-practices-review.md](claude-practices-review.md); nothing is copied. |

License texts are kept in [`third-party-licenses/`](third-party-licenses/): one shared MIT notice that lists the copyright line of every MIT-licensed pack above ([`MIT-packs.txt`](third-party-licenses/MIT-packs.txt)), the MIT and Apache-2.0 texts for moli, and the LICENSE and NOTICE of OpenDataLoader PDF. Packs that were only studied (archify, hindsight, claude-code-best-practice) are not copied, so they have no notice here.

## Benchmark data

The coding benchmark uses the public [HumanEval](https://github.com/openai/human-eval) problem set (MIT, Copyright (c) OpenAI) from `benchmarks/datasets/HumanEval.jsonl.gz` (sha256 `b796127e635a67f93fb35c04f4cb03cf06f38c8072ee7cee8833d7bee06979ef`, 164 problems). The hidden-test tasks in `benchmarks/tasks/` were written for this repository.

## Review cadence

Models improve faster than vendored prompt text does, so packs are reviewed on a
rolling window rather than only when something breaks. `skills/vendored.json` records
`provenance.<pack>.last_synced` and a shared `review_days` (default 180).

```bash
python -m bossku skills stocktake            # age every pack against the window
python -m bossku skills stocktake --strict   # exit 1 when a pack is overdue (CI)
```

`bossku validate` prints a warning for overdue packs but stays green - a pack going
stale is a prompt to review, not a broken repo. Missing provenance *is* a hard error.

To refresh a pack: re-copy from upstream, re-run `bossku skills index`, then set
`last_synced` to today in `skills/vendored.json`.

These dates are recorded syncs, not a live upstream check - the tool reports that a
pack is due for review, never that upstream actually changed.

`anatomy` is vendored without the built example pages (`examples/*/*.html`, about 8 MB); `node examples/<name>/build.mjs` writes them again. Upstream repo files (README, CHANGELOG, contributing docs, CI, `evals/`) are left out. The 2026-10-13 sync was copied from a local clone at upstream commit 454a0ef.

`logo-design` is vendored without its reference logo library (`assets/library/svg/`, 1,432 trademarked logos, about 12 MB) and `gallery.html`; the MIT licence does not cover those logos (upstream `TRADEMARKS.md`). `catalog.json`, `classifications.json` and `stats.json` are kept, so `search_library.py`, `svg_audit.py` and the scripts that need no reference files work. Options that read reference files (`--refs`, `--refs-industry`, `--format paths`) need the SVGs: copy upstream `skills/logo-design/assets/library/svg/` into the skill's `assets/library/svg/` (ignored by git here). Upstream repo files (README, TRADEMARKS, CI, `evals/`, `tools/`, `docs/images/`, `.claude-plugin/`) are left out. The 2026-10-14 sync was copied from a local clone at upstream commit 0ecf52e.

`awwwards-web-design` is vendored with its references, recipes, `data/` evidence (the repo's `data/` ignore rule is lifted for it in `.gitignore`) and `scripts/site_probe.py` for audit mode. Its four crawler scripts are left out (`awwwards_corpus.py`, `font_census.py`, `element_frames.py`, `gather_evidence.py`): they crawl awwwards.com and every winning site with a spoofed browser user agent, so its Refresh mode does not run here. Upstream `NOTICE.md` is kept in the skill folder (the data is measurements of third-party sites; Awwwards and the named brands belong to their owners). Upstream repo files (README, CHANGELOG, CI, `docs/`, `.claude-plugin/`) are left out. The 2026-10-21 sync was copied from a local clone at upstream commit 4546147.

`awwwards-jury` vendors `awwwards` and `jury` whole; the upstream `tests/` fixtures (Next.js and Astro sample apps) and repo files are left out. Both skills install Playwright and axe-core only when the user runs them, `jury` into `~/.cache/jury`, never into the reviewed project; deploys in `awwwards` `references/ship.md` wait for the user's confirmation. The 2026-10-21 sync was copied from a local clone at upstream commit ea8f145.

`mengto` vendors 114 of the 177 upstream skills as text only (SKILL.md, REFERENCES.md, PROMPT.md, `references/`, `scripts/`, `agents/openai.yaml`), all library-only: `web-design` (90 of 92), `ui` (3), `3d` (16), `media` (2) and three `codex` skills (`optimize-web-animations`, `stitched-full-page-capture`, `audit-reference-originality`). Demo pages, preview images, `assets/` and the vendored GSAP, Three and Tailwind runtimes (about 130 MB) are left out, so a skill that names its `demo/` folder has no demo here. Left out on purpose: the `game-development` and `game-combat` skills (not web design), `illustration` (the house rule bans model-drawn illustration), `workflow` (`workflow-ship-change` treats push and publish as standing authorizations, against this repo's risk pauses), and the remaining `codex` skills (Meng To's own X, voice and publishing workflows), and `landing-page` and `pricing-page` (their generic ids outranked the house rule on every landing or pricing page prompt, and `bosskuai-taste` with marketingskills `page-cro`, `copywriting` and `pricing` cover them). One local format fix to re-apply on a re-vendor: `3d-metal-material`'s description is quoted, because its unquoted `: ` broke strict YAML parsers. The 2026-10-21 sync was copied from a local clone at upstream commit 398cd41.

`security-audit` vendors the `security-audit` skill whole (SKILL.md, the phase and attack-class references, `report-schema.json` and the two dependency-free Node validators with their tests); it is library-only. Upstream repo files (README, LICENSE, `.git`) are left out. Its full six-phase audit runs only on an explicit codebase audit, pen-test or report request; anything smaller stays in guidance mode, and `bosskuai-cybersecurity-risk` keeps ordinary security reviews. Its validators open input with `O_NOFOLLOW` and `O_NONBLOCK`, which Node does not offer on native Windows, so there they exit with "OS no-follow and nonblocking input protection is unavailable" (7 of the 65 upstream tests fail for the same reason); run them under macOS, Linux or WSL. The 2026-10-22 sync was copied from a local clone at upstream commit c1c8a8c.
