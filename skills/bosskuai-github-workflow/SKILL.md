---
name: bosskuai-github-workflow
description: Use this for GitHub workflow operations across issues, pull requests, Actions, releases, Dependabot, repository settings, and GitHub MCP-assisted project coordination.
---

# GitHub workflow

For GitHub as the delivery surface: issues, PRs, Actions runs, releases, Dependabot, and repo metadata. Not writing the pipeline YAML itself (`bosskuai-ci-cd-pipelines`) or reviewing the diff's code quality (`bosskuai-rigorous-code-review`).

1. **Identify the object and read local state first**: branch, `git status`, recent commits, CI config, contributing docs. Only then fetch remote truth with `gh` or GitHub MCP — never state an issue's, PR's, or run's status from memory.
2. **Keep confirmed facts separate from inference** in anything you write back; label a guess as a guess.
3. **For issues**: turn a fuzzy ask into acceptance criteria, check for duplicates and blocking dependencies first, and create or update with enough context to be actionable — problem, outcome, constraints, verification.
4. **For PRs**: confirm the branch has only the intended changes before opening it. Draft with summary, test evidence, risk areas, rollback, and linked issues. Check merge readiness — CI status, required reviews, conflicts, unresolved comments — before saying it is ready.
5. **For a failing Action**: find the workflow, job, failing step, and commit SHA; read the logs around the first failure, not the final cascade. Classify it (flake, dependency drift, test failure, permission error, real regression) before recommending a rerun.
6. **For releases and dependencies**: compare tags, group changes by user impact, call out breaking changes, and check exploitability and lockfile impact before recommending a Dependabot merge.
7. **Before finishing, check**: did I claim remote state I did not actually read through tooling; did I bury a failing or unrun check behind a clean summary; does anything I'm posting contain a secret, token, or private URL.

If an action is ambiguous — merge, close, label, rerun, or change a repo setting — and nobody can confirm it, do not perform it; report what you found instead. Branch protection and repo settings always need explicit approval.

The full capability map, phase-by-phase workflow, and output template: `reference.md`.
