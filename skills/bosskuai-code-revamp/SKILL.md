---
name: bosskuai-code-revamp
description: Use this for safe code modernization, structural cleanup, legacy refactors, and revamps that should still respect the current codebase structure and avoid unnecessary churn.
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
