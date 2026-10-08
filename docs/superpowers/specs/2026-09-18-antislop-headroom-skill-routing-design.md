# Anti-slop, Headroom, and Skill Routing Design

## Goal

Make Bossku Superpower select a minimal, prompt-aware stack of skills, apply anti-slop and verification defaults across supported coding tools, and install every support file those skills need.

## Scope

- Vendor the six skills from the local `anti-slop` checkout without rewriting upstream content.
- Add a small Bossku-authored Headroom operating skill. Do not install or route provider traffic through Headroom in this change.
- Allow multiple complementary skills. Choose one primary skill, then add supporting skills only when the prompt or a loaded workflow requires them. Avoid loading overlapping alternatives.
- Keep Superpowers as the process layer for brainstorming, planning, TDD, debugging, and verification.
- Make design direction and anti-slop separate concerns: `bosskuai-taste` or another design skill supplies direction; `antislop-*` filters generic output and verifies usability.
- Copy shared Bossku references into both user-level skill roots so installed skills do not point to missing files.
- Fix Windows and OneDrive read-only removal failures so `bossku update` is repeatable.
- Add a library-wide audit surface for metadata cost, oversized skill bodies, and unresolved relative links.

## Shared Contract

The always-loaded rule surface stays compact:

1. Route from the user prompt and current task phase.
2. Use one primary skill plus the smallest useful set of complementary skills; do not impose a fixed cap when an explicit workflow requires more.
3. Use Superpowers process skills before implementation and fresh verification before completion.
4. Apply anti-slop to UI, copy, responsive layout, accessibility, and comments through the matching task-specific skill.
5. Preserve context by narrowing reads, avoiding repeated output, and compressing large logs or tool results when Headroom is available.
6. Re-read the request, inspect changed files, run the relevant checks, and report remaining uncertainty before claiming completion.

The canonical contract is mirrored into the Cursor rule and the managed project block written by `bossku init`.

## Routing

`bossku skills find` remains a ranked lexical router, but its output will explicitly expose a shortlist for stack composition. Curated triggers cover anti-slop, Headroom, design, and Superpowers phrases. Routing tests cover both single-domain prompts and prompts that require complementary capabilities.

The agent, not the lexical scorer, decides whether shortlist entries are complementary or alternatives. Examples:

- Premium responsive page with motion: design direction + `antislop-ui` + responsive/accessibility support + the relevant motion skill.
- New feature: `brainstorming`, then `writing-plans`, then `test-driven-development`, then `verification-before-completion` as phases advance.
- Large failing CI log: `ci-triage` + `systematic-debugging`; use `bosskuai-headroom` only when Headroom is installed or installation is part of the request.

## Installation

`bossku install` and `bossku update` continue to install skills to `~/.agents/skills` and `~/.claude/skills`. They also merge Bossku-owned files from `references/` into sibling `references/` directories without deleting unrelated user files. Installed files are made writable after copying.

Removal uses a Windows-safe tree remover that clears read-only attributes before retrying. Uninstall remains surgical for skill directories; shared references are retained unless a future manifest-based cleanup can prove ownership safely.

## Skill Quality

- Vendored skills remain byte-equivalent to their upstream source except line-ending normalization.
- New skills use concise discovery metadata and progressive disclosure.
- `bossku skills audit` measures every shipped skill and reports metadata size, large bodies, and broken relative Markdown links by pack.
- The audit distinguishes Bossku-authored defects from known upstream-pack gaps rather than silently treating either as healthy.
- High-traffic custom metadata, especially `bosskuai-taste`, is tightened without rewriting every skill body in one batch.

## Verification

Required evidence:

- Anti-slop repository check and installer smoke test.
- Failing then passing Windows update/uninstall regression tests.
- Failing then passing shared-reference install tests.
- Routing tests for anti-slop, Headroom, design, and multi-skill prompts.
- Rebuilt `skills/skill-index.json`.
- `python -m bossku validate --root .`.
- Full `python -m unittest discover -s tests -v`.
- Real `bossku update`, followed by file/count/hash checks in both installed roots.
- `bossku doctor` and representative `bossku skills find` checks.

## Non-goals

- No Headroom proxy, MCP, persistent deployment, or provider configuration changes.
- No bulk rewrite of vendored descriptions.
- No deletion of existing user skills or unrelated host configuration.
