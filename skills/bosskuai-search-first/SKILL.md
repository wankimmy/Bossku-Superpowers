---
name: bosskuai-search-first
description: Use when deciding whether to adopt an existing package, service, MCP, internal utility, or pattern before building custom code or workflow logic.
---

# Search first

Before building anything custom, check whether it already exists. Stop at the first tier that's a good fit — do not propose a build until every cheaper option is ruled out.

1. **Name the capability, not the implementation.** One line on what the code must do, plus the real constraints: stack version, license limits, latency, ops budget.
2. **Search in order, stop at the first good fit:** this repo (utility, module, skill, pattern) → framework/platform native feature → the current tool or MCP surface → a maintained ecosystem library → a managed service → custom code, last.
3. **Score every external candidate in one pass:** maintained within the last year, real adoption, no open Critical/High CVE, a compatible license (MIT/Apache/BSD; stop at GPL or "no license"), and it covers most of the need without heavy wrapping.
4. **One red flag kills the candidate.** Abandoned, an unpatched CVE, or an incompatible license — drop it and move to the next tier instead of rationalizing around it.
5. **If nobody is available to weigh in**, default to whichever option clears every check above with the least new code for you to maintain, and say so in one line.
6. **State the smallest next step**: for adopt, the integration point; for build, the minimal first version — not the full feature.

Check before you finish: you actually looked at the candidate's last commit and license before recommending it, you didn't reject an option just because it needs reading docs, and "we can just use X" is backed by a real check of X.

Full evaluation table, the build-vs-adopt matrix, and the output template: `reference.md`.
