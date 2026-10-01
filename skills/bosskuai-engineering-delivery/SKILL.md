---
name: bosskuai-engineering-delivery
description: Use when implementing a software change through planning, tests, review, and observed product verification.
---

# Engineering delivery

Ship the change in this order. Work on your own; ask the user only if the request reads two ways and the code cannot tell you which.

1. **Orient.** Read the code, tests and README the change touches. List every entry point that reaches it: other modules, CLI, scripts, README and docs examples. Follow the project's conventions.
2. **List the requirements.** Number every rule in the request and write the check that will prove each one. If something is ambiguous, take the reading the README, tests or existing code support, and state it in one line.
3. **Test first.** For each requirement add a test, plus the edge cases it implies: empty, one, many, duplicates, boundaries, wrong type, repeated calls, input left unchanged, exact error type. Run them and see them fail for the right reason.
4. **Make the smallest change that passes.** Update every call site: search for the old name, signature or behaviour across code, scripts and docs. Leave unrelated code alone; remove only what your change orphaned.
5. **Run everything.** The whole test suite, then your own checks. Read the output. Fix the code, never the test, until it is green.
6. **Audit.** Re-read the request line by line against your diff. For each requirement name the code and the run that covers it. Fix any gap and run again.
7. **Report** what you ran, what passed, and anything you could not verify.

Migrations, public APIs, security-sensitive changes, rollback plans, feature flags, ADRs and the long Definition of Done: read `reference.md` in this folder.
