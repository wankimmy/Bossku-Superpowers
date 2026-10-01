# Portable skill selection and source-practice integration

Goal: select one primary skill and useful complements from distinct prompt concerns, explain selection and ambiguity, preserve portable defaults, and release the already approved vault-memory work with the improvements.

User decisions: include pending vault-memory changes; Archify and Hindsight remain optional. Commit and ordinary push to main are authorized. Do not deploy services, capture transcripts, install runtimes, or change provider routing.

## Phase 1: selection behavior (root executor)

Files: `bossku/skills.py`, `bossku/cli.py`, `bossku/index.py`, `tests/test_skill_selection.py`, routing docs and entry instructions.

Add a structured `select_skill_stack(task, root=None, limit=5, available=None)` result alongside the existing lexical ranking API. Preserve legacy `find_skill` ranking contracts. Select from installable skills, honor named ids/aliases, keep slash-command-only skills out of automatic loading, suppress incompatible alternatives, and add complements only when they explain another concern. Report reasons, deferred candidates, confidence, and uncovered named skills. A core-profile filter must never suggest loading a full-only skill. Expose the selection in `bossku skills find`; the ranked `matches` remain inspection candidates.

Regression cases: explicit aliases and multiple named skills; unmatched and weak requests; blocked x402; user-only commands; overlapping debugging and design directions; responsive UI plus mobile/keyboard concerns; code plus separate marketing concern; core profile; positive-score cutoff; deterministic output and index freshness. Write failing cases first, implement, then run `python -m unittest discover -s tests -p test_skill_selection.py -v` and existing routing tests. Keep the implementation stdlib-only.

## Phase 2: source adaptations (parallel file scopes)

Archify executor owns codebase-analysis/project-understanding skills, their checklist/playbooks, and an Archify evidence reference. Use verified extraction versus semantic claims, evidence freshness and bounded exploration; no graph runtime requirement or new synonym skill.

Claude executor owns Claude setup/MD management/skill creator/subagent-delegation skills and Claude practice references. Correct configured-memory wording and add only verified missing portable practices. Host-specific fields require capability checks. Do not modify vendored skills.

Hindsight executor owns hindsight-memory skill and its playbook. Correct configured-memory ownership, clarify verified missing operation/API boundaries and evaluation, keep banks scoped and uploads authorized. No live backend testing or deployment.

Each executor returns source file:line evidence, changed paths, exclusions, and validation. Root rebuilds the generated index after parallel edits finish.

## Phase 3: audit and release

Independent auditor reviews selection regressions, pending memory changes, install cache/profile behavior, referenced guidance, and source-adaptation claims. Limit a repeated failing fix to three attempts; an open material finding cannot pass. Correct remaining obsolete canonical-memory instructions in active agent contracts and references.

Run `python -m bossku skills index --root .`, `python -m bossku validate --root .`, and `python -m unittest discover -s tests -v`. Use a writable temporary test directory if the sandbox denies the Windows default temp location. Run core/full install-init-doctor and selection CLI smoke checks in isolated homes. Review the complete diff, commit explicit paths, fetch/verify main, push without force, confirm remote SHA, run `bossku update`, then doctor and compare installed routing caches and changed skill files. Save verified outcomes using the configured memory path. Report backend/host behavior that was not live tested.
