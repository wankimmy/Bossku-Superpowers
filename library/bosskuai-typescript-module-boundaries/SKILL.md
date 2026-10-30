---
name: bosskuai-typescript-module-boundaries
description: "Use when enforcing deep-module boundaries in a TypeScript repo with dependency-cruiser: root files as entry points, hidden subfolders, tests through entry points, no cycles, and a proof the rules fail on violations."
---

# BosskuAI TypeScript Module Boundaries

Use this skill to make each package a deep module: much behaviour behind a small interface, with the boundary enforced by a lint rule rather than by convention.

## How this differs from nearby skills

- **`bosskuai-architecture-deepening`**: finds which modules to merge or deepen. This skill installs the enforcement once the shape is chosen.
- **`bosskuai-hexagonal-architecture`**: ports-and-adapters layering; layering between packages is left to the repo in this skill.
- **`bosskuai-software-architecture`**: general design decisions.
- **`bosskuai-ci-cd-pipelines`**: where the new lint script is wired in.

## The shape

```text
<packages-root>/<name>/
  index.ts     entry point (public); a package may have several root files
  lib/         implementation, hidden from outside
  tests/       co-located tests and fixtures, private
```

The public surface is the package's root files. Anything in any subfolder is private, so adding a folder never needs a config change. Packages are flat: one tier of children under the root.

## Four rules, all errors

1. Code outside a package may import only that package's root files.
2. Files inside a package import each other freely.
3. Files in `<pkg>/tests/` may import any package's entry points and their own test fixtures, never any package's subfolder internals.
4. No dependency cycles.

Avoid barrel files that re-export a subtree. Prefer several small entry points.

## Steps

1. Detect the package manager from the lockfile, the TypeScript version (`npx tsc -v`), the packages root (`src/packages` if `src/` exists, else `packages`), and any existing `.dependency-cruiser.*` config. Merge into an existing config instead of overwriting it.
2. Install `dependency-cruiser` as a dev dependency. Read the docs for the version the lockfile resolves, not a newer one, for the config syntax and group-matching (`$1`) behaviour.
3. Write `.dependency-cruiser.cjs` with the four forbidden rules, using path-depth patterns and a `PACKAGES_ROOT` constant. Use `.cjs` so it works in ESM repos.
4. Add a `lint:boundaries` script and run it in the same umbrella command as typecheck. Do not change tsconfig or add path aliases.
5. Add a small example package (entry point that delegates to `lib/`, one test importing only the entry point) as a copy-me template.
6. Prove the rules bite: run and expect a pass; add a deep import in a test and expect a failure naming the rule; revert and expect a pass. If the violation does not fail, the rules are mis-wired.
7. Document the convention in a README in the packages folder, and add a one-line pointer from the repo's agent instructions file.

## Guardrails

- Do not finish without the pass, fail, pass observation.
- Do not flatten the group-matching rules into per-package rules.
- Confirm the packages root with the user if the repo already has another convention.
- Do not edit the repo's agent instructions or CI beyond the one-line pointer and script wiring without approval.
- Keep typecheck, lint and tests clean, with no new warnings. Fix an import that breaks a rule; do not add an exception without the user's approval.
- Meet the quality bar in `../../references/checklists/engineering-quality-bar.md`.

## Output format

```text
Environment: [package manager, TypeScript version, packages root, existing config]
Config: [rules added, merged or new]
Wiring: [script name, umbrella command]
Proof: [pass -> fail on deep import -> pass, rule name shown]
Docs: [README path, pointer added]
Checks: [typecheck, lint and tests, with the commands run and their results]
```

Adapted from mattpocock/skills/skills/in-progress/setup-ts-deep-modules/SKILL.md (mattpocock/skills, MIT).
