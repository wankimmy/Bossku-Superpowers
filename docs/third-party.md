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
| opendataloader-pdf | [opendataloader-project/opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) | Apache-2.0 | Copyright 2025-2026 Hancom, Inc. (upstream NOTICE; [LICENSE](third-party-licenses/opendataloader-pdf-LICENSE.txt) and [NOTICE](third-party-licenses/opendataloader-pdf-NOTICE.txt) kept here) |
| moli | [lexmount/moli](https://github.com/lexmount/moli) | MIT OR Apache-2.0 (used under MIT) | Copyright (c) 2026 Moli contributors ([MIT text](third-party-licenses/moli-LICENSE-MIT.txt), [Apache text](third-party-licenses/moli-LICENSE-APACHE.txt)) |
| greptile (adapted, first-party) | [greptileai/skills](https://github.com/greptileai/skills) | MIT | Copyright (c) 2026 Greptile AI |

`moli` vendors the upstream `moli-webfetch` and `moli-cdp-server` skills (the Rust browser itself is not bundled). One local deviation to re-apply on any re-vendor: step 1 of both `SKILL.md` files told the agent to install Moli by piping a remote installer script into a shell; it now says to stop, show the user the install instructions, and continue only after they have installed it or explicitly asked for the installer to be run (the binaries are unsigned and the installer has no checksum check). `moli-websearch` is deliberately not vendored (listed under `excluded`): its references tell the agent to scrape public API keys from third-party frontends and to switch search engines after a CAPTCHA.

`superpowers` has one local addition to re-apply on any re-vendor: `verification-before-completion/SKILL.md` has a section "Match Evidence to the Intended Outcome" (a build or test run supports only the behaviour it covers; for documentation and agent instructions, check how the consumer discovers and loads them; keep local runs, external CI and assumptions apart) and two extra rows in the "Common Failures" table. The upstream text is otherwise unchanged.

`markitdown` is a thin Bossku-authored skill that documents the upstream CLI; the Microsoft package is not bundled.

`graphify` upstream no longer keeps a static `SKILL.md` in its repo: the skill is rendered per host by `graphify install`. Bossku Superpower vendors the cross-framework Agent-Skills variant (`graphify/graphify/skill-agents.md`) plus its `skills/agents/references/` sidecar. Re-vendor from those two paths, not from a `skills/` folder.

`ecc` is a curated subset (10 of ~280 skills) chosen to fill gaps in the Bossku library - MySQL/MariaDB, migrations, error handling, MCP servers, Playwright, WCAG 2.2, ADRs, Vue 3, Python, pytest. Each is a single self-contained `SKILL.md` with no ECC-only tooling references; the many agent-stack ECC skills were already ported earlier as `bosskuai-*` skills.

`graft` vendors the upstream `SKILL.md` body verbatim; the CLI itself is not bundled (`npm install -g @nanonets/graft`, then `graft build` per repo). One local deviation: the frontmatter `description` was rewritten to state the `graft/`-index precondition, because upstream ships inside an already-indexed repo and asserts it flatly. Re-apply that edit on the next re-vendor.

`dcg` is a thin Bossku skill that documents the upstream Destructive Command Guard CLI/hooks; the Rust binary is not bundled. Upstream license is MIT **with an OpenAI/Anthropic rider** — read the upstream `LICENSE` before redistributing the binary or derivative works.

`antislop` vendors the upstream six-skill suite unchanged. Bossku adds routing metadata in its generated index rather than rewriting the vendored skill text.

`hallmark` moved from the recorded `togethercomputer/hallmark` (now 404) to `Nutlope/hallmark`; the vendored `SKILL.md` matches it apart from line endings. Its 21-theme catalog lives in upstream `site/css/tokens.css`, vendored at `site/css/tokens.css` because every hallmark link resolves `../../site/css/tokens.css`; `bossku install` copies `site/` next to the installed skills for the same reason.

`greptile` is not a vendored pack: `bosskuai-greptile-review-loop` and `bosskuai-pr-check` are first-party adaptations of `greptileai/skills`, kept under the upstream MIT notice above. Local deviations to re-apply on any resync: `git add` scoped to the files changed for the comments, a test and lint gate plus one ask before the first push, only Greptile-bot threads resolved without a code change (never a human reviewer's), bounded polling loops, paginated inline comments, and no `p4 review` commands (they do not list or mark reviews).

Deliberately not vendored (recorded under `excluded` in `skills/vendored.json` so a re-vendor leaves them out): `taste-skill-v1`, `gpt-tasteskill`, and `stitch-skill` from the taste-skill pack. `x402` stays vendored with browser-use but `bossku install` never copies it: it prints generated wallet keys and auto-tops-up spend.

`opendataloader-pdf` vendors the complete upstream `skills/odl-pdf/` bundle unchanged. Its maintenance-only sibling is intentionally excluded, and the optional OpenDataLoader runtime is not installed automatically.

## Studied tools and optional runtimes (not bundled)

These projects informed Bossku Superpower's own skills or are offered as opt-in tools through `bossku tools`. No upstream source text is copied unless a row says so; the notices are recorded so that the record stays accurate if text is ever adopted.

| Project | Upstream | License | Copyright | How it is used |
|---|---|---|---|---|
| e2e | [tester-army/e2e](https://github.com/tester-army/e2e) | Apache-2.0 | Copyright 2026 TesterArmy, Inc. (NOTICE: "includes software developed at TesterArmy, Inc.") | `bosskuai-agentic-e2e` is written in our own words from a read of the upstream docs (no code is copied); `npx e2e init` is an opt-in per-project step. Its CLI sends telemetry unless `npx e2e telemetry disable` or `E2E_TELEMETRY_DISABLED=1`. |
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
