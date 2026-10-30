---
name: bosskuai-coding-best-practices
description: "Use when writing or reviewing code for quality: maintainability, readability, testing expectations, error handling, naming, and best-practice checks that fit repo conventions."
---

# BosskuAI Coding Best Practices

Use this skill when writing or reviewing code that should be easy to change, hard to misuse, and aligned with the existing codebase.

## Operating principles

- Prefer boring, readable code over clever code.
- Follow current repo conventions unless they are clearly harmful.
- Optimize for the three expensive failures: wrong behavior, production breakage, and code that is hard to change.
- For new behavior, bug fixes, and risky refactors: prefer test-first or test-guided work when practical.
- Debug with hypotheses, not random edits.
- Use only the APIs that exist in the language and library versions the project runs. Read that version's docs first (`bosskuai-documentation-lookup`).
- Judge each change against how the system really runs: several instances at once (in-memory state, local files, sessions, a cron that runs on each instance), workers and queues, each environment, and the moment of deploy, when old and new code overlap.

## What good code looks like

- single-responsibility functions and modules
- explicit side effects and error paths
- meaningful names
- shallow control flow with guard clauses
- no hidden shared mutable state
- validation at system boundaries
- tests or verification that prove the claimed behavior

## Common problems to catch

- god functions or objects
- primitive obsession where domain values need stronger types
- boolean traps and unreadable call sites
- swallowed exceptions
- magic values
- copy-paste logic drift
- shotgun surgery across too many files for one behavior

## Local decision guide

- local cleanup: one function or module is unclear but isolated
- revamp: the same structural problem repeats across many files
- architecture escalation: boundaries or contracts are the real problem

Load `bosskuai-code-revamp` or `bosskuai-software-architecture` when the issue is bigger than a local fix.

## Verification bias

- reproduce before fixing when debugging
- add or run the narrowest test that proves the behavior
- re-read the saved diff before declaring success
- call out what could not be verified
- test with the value types and nulls production stores (a money value can arrive as the string "0.01"), and cover the edge cases: empty, zero, negative, boundary, null, wrong type, very long, non-ASCII.

## Guardrails

- Do not impose a foreign pattern or abstraction just because it is fashionable.
- Do not add abstraction without repeated need.
- Do not mix a broad refactor into a bug fix unless the user asked for both.
- Do not mirror a bad existing pattern silently; fix proportionally and call it out.
- Do not change a shared function's behavior without finding every caller and every flow that uses it.

## Output

Return:

- conventions observed
- findings or improvement opportunities
- whether the change should stay local, become a revamp, or escalate
- testing guidance or verification gaps

## References

- `../../references/checklists/coding-best-practices-checklist.md`
- `../../references/playbooks/coding-best-practices-playbook.md`
- `../../references/checklists/engineering-delivery-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

## Quick conventions

- Names: nouns for values, verb-noun for functions (`fetchMarketData`, `isValidEmail`), booleans read as questions (`isUserAuthenticated`); a one-letter or `flag` name is a finding.
- Default to returning new objects and arrays instead of mutating inputs; mutate deliberately and say why (for example a hot path over large arrays).
- Await independent calls together (`Promise.all` or the language equivalent) instead of one after another.
- Check the HTTP status before parsing a response body and wrap low-level errors with context; do not log and swallow them.
- Check-then-act needs one guard: a transaction with a row lock, an atomic update, or a unique constraint. A separate check followed by a write is a race.
- Comments explain why (a constraint, a trade-off), never what the next line does. Extract magic numbers into named constants with units (`DEBOUNCE_DELAY_MS`).
- Query only the columns you need; `SELECT *` on a wide table is a finding.
- Tests follow arrange, act, assert, and their names state the behaviour ("returns empty array when no markets match query"), not "works".
- Use one consistent response envelope for an API, validate request bodies against a schema at the boundary, and return field-level validation details with a 400.
- Parse external responses with a schema: ignore extra fields, reject missing fields and changed types, and never coerce them silently.

Adapted in part from ECC skills/coding-standards (affaan-m/ECC, MIT).
