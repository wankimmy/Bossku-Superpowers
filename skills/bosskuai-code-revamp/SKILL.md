---
name: bosskuai-code-revamp
description: "Use when revamping legacy code safely: modernization, structural cleanup, and refactors that respect the current codebase structure and avoid unnecessary churn."
---

# Code revamp

For refactors and migrations that touch several files. Behaviour must not change except where the request says so.

1. **Map the blast radius before you edit.** Search for every use of what you are changing: imports, calls, string references, `__all__` and re-exports, scripts and CLI entry points, README and docs examples, tests.
2. **Pin today's behaviour** with tests (write them if they are missing) before you touch the code.
3. **Work in small slices that each leave the tests green.** Put the new shape next to the old one (alias, shim, wrapper, deprecation warning), move callers one at a time, and remove the old path only if the request says to.
4. **Keep old import paths and signatures working** unless told otherwise. Warn with the right category, once per call, not once per item.
5. **Search again for the old name** when you finish; run the full tests and the code in the README.
6. **Do not mix refactoring with new behaviour,** and do not tidy code you were not asked to touch.

A revamp needs a concrete harm to justify it; a local fix is better when one will do. Migration patterns (strangler fig, module extraction, interface introduction), the risk matrix and the rollback checklist: read `reference.md` in this folder.

## Inheriting a legacy style
When new code must match a hand-written codebase, extract its unwritten rules first instead of imposing your own:
- Size the repo (count source files) and pick the depth: under ~50 files read closely; 50-500 read the infrastructure layer fully and sample 2-3 files per dimension in the business layer; above ~500 sample strictly from a `git diff --stat` or tree summary.
- Scan four dimensions: in-file declaration order, naming of state/async/pagination/flags, where cross-cutting code lives (middleware, formatters, interceptors), and error handling (try/catch, global handler, result types, null checks).
- A tiny minority (under ~5% and fewer than ~10 occurrences) is noise: the majority wins and the minority goes on the DONT list. In a small project, "3 vs 2" is not a majority; ask.
- Resolve real conflicts with the user one question at a time, citing a file for each side, with options: follow A, follow B, the project is evolving, or give a new rule.
- Record the result as golden-file exemplars (path plus what each shows), checkable naming and control-flow rules, and DONTs. Date the file and append later changes as a log; never overwrite old rules.
- Before writing code, name the exemplar you follow and the DONTs you avoid. Reuse the exemplar's structure, not its bugs; flag defects instead of copying them. Ask before adding any enforcing hook.

Adapted in part from ECC skills/inherit-legacy-style (affaan-m/ECC, MIT).
