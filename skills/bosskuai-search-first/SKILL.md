---
name: bosskuai-search-first
description: Use before building custom code or an unfamiliar feature to adopt an existing package, service, MCP, utility or pattern, or study open-source prior art.
---

# Search first

Before building anything custom, check whether it already exists. Stop at the first tier that's a good fit — do not propose a build until every cheaper option is ruled out.

1. **Name the capability, not the implementation.** One line on what the code must do, plus the real constraints: stack version, license limits, latency, ops budget.
2. **Search in order, stop at the first good fit:** this repo (utility, module, skill, pattern) → framework/platform native feature → the current tool or MCP surface → a maintained ecosystem library → a managed service → custom code, last.
3. **Score every external candidate in one pass:** maintained within the last year, real adoption, no open Critical/High CVE, a compatible license (MIT/Apache/BSD; stop at GPL or "no license"), and it covers most of the need without heavy wrapping.
4. **One red flag kills the candidate.** Abandoned, an unpatched CVE, or an incompatible license — drop it and move to the next tier instead of rationalizing around it.
5. **If nobody is available to weigh in**, default to whichever option clears every check above with the least new code for you to maintain, and say so in one line.
6. **Building, or the feature is new to you? Study prior art first.** Find 2-3 open-source projects that already ship it (`gh search repos "<capability>" --sort stars`, `gh search code`), read how each one does it, and compare in a few lines: approach, edge cases handled, known bugs in their issues. Pick one approach, then build. Borrow ideas freely; copy code only under a compatible license, with its notice kept.
7. **State the smallest next step**: for adopt, the integration point; for build, the minimal first version — not the full feature.

Check before you finish: you actually looked at the candidate's last commit and license before recommending it, you didn't reject an option just because it needs reading docs, and "we can just use X" is backed by a real check of X.

Full evaluation table, the build-vs-adopt matrix, and the output template: `reference.md`.

**Preflight the search channels you rely on** and report skipped ones honestly (never "nothing found" when a channel was unavailable):

- Repo: `rg --files` plus targeted `rg`; if that is all you could do, say only visible files were inspected.
- Package registry: confirm the package manager works (`npm --version`, `python -m pip --version`); otherwise use docs or web search and do not claim registry coverage.
- GitHub: `gh auth status`; if unauthenticated, use public web or local git history only.
- MCP and docs tools: check the available tool list or local MCP config; fall back to official docs.
- Local skills: list the skills directory; if none, say no skill catalog was available.

**Decision outcomes**: adopt as-is (exact match, maintained, permissive license); extend or wrap (partial match, thin wrapper); compose (2-3 small packages when several matches are weak); build (nothing suitable, but informed by what you found). Anti-patterns: over-customizing a library until it loses its benefit, and installing a large package for one small feature.

Adapted in part from ECC skills/search-first (affaan-m/ECC, MIT).
