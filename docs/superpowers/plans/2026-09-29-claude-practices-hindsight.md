# Claude practices and Hindsight implementation plan

> **For agentic workers:** Execute inline with `executing-plans`; the user authorized implementation, commit, and push to main.

**Goal:** Apply the practical README guidance and Hindsight memory lessons to BosskuAI, repair a confirmed activation bug, and publish verified changes.

**Architecture:** Keep the portable skill library and curated Markdown memory as the defaults. Add focused product-verification and optional Hindsight skills, supported by reference playbooks. Use the same executable-import predicate in initialization, validation, and doctor.

**Tech Stack:** Python 3.11+, standard-library unittest, Markdown Agent Skills.

**Spec:** User requested analysis of `claude-code-best-practice` and `hindsight`, practical guidance rather than wholesale library imports, followed by commit/push to main after `gh auth switch`.

## Global constraints

- Preserve existing instructions and unrelated user work.
- Do not change vendored skill text, install a Hindsight service, or ingest transcripts.
- Keep new skill descriptions under 300 characters and longer guidance in references.
- Preserve the bare `@AGENTS.md` adapter and rebuild the generated routing index.
- Main is explicitly authorized; use a normal fast-forward push, never force.

## Task 1: Repair instruction activation

**Files:** `bossku/validate.py`, `bossku/init_project.py`, `tests/test_instruction_imports.py`.

**Interface:** Existing `claude_imports_agents_md(text)` and `omp_imports_agents_md(text)` remain boolean predicates; both ignore inline and fenced code examples.

- [x] Add regression cases for prose, inline code, both fence types, differing fence lengths, unclosed fences, real imports, preservation, and idempotency.
- [x] Run `python -m unittest discover -s tests -p test_instruction_imports.py -v`; confirm the activation regressions fail before the fix.
- [x] Share import detection between init, validation, and doctor; prepend a live import only when absent.
- [x] Re-run the regression file and verify that existing project text survives two initialization runs.

## Task 2: Apply the reference guidance

**Files:** Existing Claude setup, CLAUDE.md management, skill creator, stocktake, engineering delivery, and permanent memory skills; their checklists; two new skills; reference playbooks; `docs/claude-practices-review.md`, `docs/memory.md`, `AGENTS.md`, `bossku/index.py`, `tests/test_practice_routing.py`.

**Interface:** New skills are `bosskuai-product-verification` and `bosskuai-hindsight-memory`; the former verifies actual user paths and the latter uses an already configured Hindsight connection or reports a gap.

- [x] Record pinned source revisions and a coverage map for all nine README skill tips, nine skill categories, demo skills, built-ins, and external catalogs.
- [x] Add concrete discovery checks, scoped configuration, context budgeting, gotchas, and invocation guidance to existing skill surfaces.
- [x] Add product verification with observed evidence and a Hindsight retain/recall/reflect workflow with project isolation and Markdown fallback.
- [x] Add routing cases for both new skills and verify unrelated memory and unit-test prompts still choose their existing skills.
- [x] Run `python -m bossku skills index --root .`, validation, and the full unittest suite.

## Task 3: Publish

**Files:** `README.md`, `CHANGELOG.md`, `.bossku/memory/` as required by the repository.

- [x] Review the complete diff and run install/doctor smoke checks in an isolated temporary home.
- [x] Apply only reviewed files to the clean canonical main checkout and verify there too.
- [x] Run `gh auth switch --hostname github.com --user wankimmy`, verify identity with `gh api user`, and fetch remote main (baseline matched).

Publication: record verified outcomes, commit only the intended files, push main normally, and verify remote main matches local HEAD. The resulting commit and remote ref provide the publication evidence.
