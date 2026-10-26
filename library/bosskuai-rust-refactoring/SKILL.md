---
name: bosskuai-rust-refactoring
description: "Use when refactoring a Rust codebase at crate or workspace scale: safe renames, module restructuring, duplication removal, ownership and panic hardening, Clippy fixes, with an audit inventory and full-verification report."
---

# BosskuAI Rust Refactoring

Use this skill to carry out, or audit, a complete and coherent Rust refactor: every definition, caller, import, test, doc, and config reference updated together, with behaviour preserved unless a change is authorised. Rust has no classes, so read "class" as the relevant structs, enums, traits, impls, or modules.

## How this differs from nearby skills

- **`bosskuai-rust-patterns`**: idioms for writing new Rust (ownership, errors, traits). Use it as the style reference while refactoring.
- **`bosskuai-rust-testing`**: how to write Rust tests; here tests are used as the safety net and extended with characterization tests.
- **`bosskuai-code-revamp`**: safe refactors and legacy cleanup in any language; this skill holds the Rust-specific moves.
- **`bosskuai-business-logic-review`**: reviews business rules, not structure.

## Workflow

1. Classify the request: audit, implement, explain, or plan. Fix scope, objective, compatibility expectations, and which behaviour changes are authorised.
2. Read repository instructions, manifests, toolchain and lint config, CI, and feature definitions. Check uncommitted work and never overwrite changes you did not make.
3. Map the affected surface: definitions, callers, traits, impls, tests, re-exports, macros, features, errors, side effects. `pub` alone does not prove external reachability; check visibility and re-exports. Use the language server's references first, then search macro input, attributes, `include_*` paths, build scripts, snapshots, string dispatch, serialisation names, FFI names, and doctests.
4. Baseline. Run the narrowest existing tests and checks before editing and record pre-existing failures. Add characterization tests where behaviour matters but is underspecified. Profile or benchmark before any performance work.
5. Design coherent batches. Group mutually dependent changes, order by dependency, risk, and verification cost. Keep unrelated cleanup out.
6. Implement end to end. Leave no half-renamed symbols, duplicate old and new paths, or stale comments. Add regression tests for any defect you fix.
7. Verify with the relevant matrix: format check, targeted tests then crate or workspace tests, `cargo check`, Clippy, docs. Derive feature and target coverage from manifests, `cfg` use, and CI rather than assuming `--all-features` is valid. Run a semver checker if the public API may have changed.
8. Review the final diff: every changed file belongs to the transformation, no accidental lockfile, dependency, or formatting churn.

## Audit inventory item

```markdown
### RUST-001: category and short title
- Location: crate/path, symbol
- Evidence: what the code does and who calls it
- End state: the target design
- Coupled changes: files that must move together
- API or behaviour impact: internal only / needs authorisation
- Risk and value: low/medium/high
- Verification: tests and checks
```

Report every evidence-backed finding in scope, state what was and was not inspected (feature-gated, macro-generated, target-specific code), and skip style preferences.

## Behaviour that counts as observable

Public API shape, errors, ordering, side effects, panic conditions, serialisation, I/O, drop timing, lock scope, `.await` boundaries, cancellation. Iterator rewrites can change ordering or short-circuit behaviour; `entry().or_insert` is not the same as "update only if present".

## Guardrails

- Ask before changing public API, ABI, CLI, config, features, wire or persistence formats, dependencies, toolchain or MSRV, lint policy, or existing `unsafe`, FFI, cryptography, or authentication code.
- Do not add `unsafe` to get past the borrow checker. Do not weaken, skip, or rewrite tests to accept new behaviour.
- Do not replace an error with a default or ignored result unless the contract says so.
- Claim a speed-up only after a comparable measurement. Report a command as passed only if it ran and passed.
- No destructive Git operations (reset, clean, force checkout) without explicit authorisation. Do not expose secrets found while reading.
- If the existing design is clearer and safer, say so and leave it.

## Output format

```text
Implemented scope: [objective, batches]
Files and symbols: [moved, renamed, deleted]
Behavior and API: [preserved, intentional changes]
Verification: [exact commands and results]
Remaining risk: [unverified targets, deferred items]
```

Adapted from agency-agents/engineering/engineering-rust-refactoring-specialist.md (agency-agents, MIT).
