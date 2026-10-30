---
name: bosskuai-project-understanding
description: "Use when learning what a repo is, who it serves, what defines its behavior and which skills to load next: oriented reading plus selective sampling over full-tree dumps."
---

# Project understanding

Use when the first task is learning what a repo is before touching it. For tracing how code runs, hand off to `bosskuai-codebase-analysis`.

1. **Resolve memory first.** Run `bossku memory-path --project <project-root>`; read `handoff.md` and `project.md` there if present before reading anything else.
2. **Read orientation artifacts**: nearest README, AGENTS.md/CLAUDE.md, docs, manifests, env examples, CI/runtime config. Record the current versions from the manifests, lockfiles and runtime files as confirmed facts. Check the latest stable release live, never from memory.
3. **Verify every doc claim against real source.** README and docs are aspirational until the code backs them up.
4. **Sample with a budget, not exhaustively**: entry points and framework config, one representative domain slice, the data/model layer, integration boundaries, a few high-signal tests. Expand only to close a real uncertainty.
5. **Synthesize** purpose, likely users, stack, architecture style, and the source-of-truth files. Label every claim confirmed, inferred, or unknown. Also list what a release needs that you could not see: a production data copy, the deploy and rollback steps, CI status, logs and dashboards. Ask the user to prepare or grant what is missing.
6. **If a business detail can't be confirmed and nobody is available to ask**, mark it `Inferred:` with the best-supported reading — do not guess silently and do not block on it.
7. **Save the verified understanding** with `bossku remember --project <project-root> --kind project`; never write inferred or unknown claims to memory.
8. **Recommend the next 1-3 skills** for the concerns that remain, and say what each one will resolve.

Check before you finish: every claim in the summary cites a file, sampled vs unread areas are stated, and any existing memory or map was re-checked against current source rather than trusted as-is. Each infra part in the map cites its file, or is marked `unknown`.

Full workflow, output template, and checklist: `reference.md`.

Shared bar: `../../references/checklists/engineering-quality-bar.md`.

## Onboarding extras
- Start recon with cheap signals via glob and grep, not full reads: package manifests, framework configs, entry points (`main.*`, `index.*`, `cmd/`), a depth-2 tree without vendor and build folders, CI and Docker files, and test layout and runner config.
- Trace one request end to end: where it enters, how it is validated, where the business logic sits, how it reaches the database.
- Detect conventions from the code: file and test naming, error-handling style, async and state patterns, and from recent commits the branch and commit style. If history is missing or shallow, write "Git history unavailable or too shallow" instead of guessing.
- If the repo's detected framework disagrees with what the code actually does, trust the code. If a convention is not detectable, say "could not determine".
- Compare the data the code expects with a production data copy or a schema the user provides, never a live production connection or production credentials found in the repo: column types, nullable fields and enum values. If neither exists, ask the user to prepare one. Mark an inferred type as inferred.
- Map the current infra from the compose files, Dockerfiles, IaC, CI/CD workflows, env examples and deploy docs: where each part runs (VPS, containers, serverless or managed service), and the web, worker and scheduler processes, databases, caches, queues, storage and CDN.
- Note how config and secrets reach each environment (names and mechanism only; never copy secret values into the summary or memory), how deploys and migrations run, and how many instances run at once. Mark what the repo does not show as `unknown` (live instance count, production hosts, CDN and secret store settings, who holds access), and ask the user to confirm it before you rely on it.
- If the user wants a guide or an instruction file, keep it scannable in two minutes: a "I want to... / look at..." table, common commands, key entry points. Keep any generated CLAUDE.md under about 100 lines, list only dependencies that shape how code is written, and do not copy the README. If one exists, read it first, extend it, and mark what was added.

Adapted in part from ECC skills/codebase-onboarding (affaan-m/ECC, MIT).
