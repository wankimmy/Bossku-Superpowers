---
name: bosskuai-data-throughput-accelerator
description: "Use when the task explicitly concerns data throughput accelerator. Diagnose and accelerate large data movement — ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, and table synchronization — by isolating the true bottleneck, benchmarking variants, and codifying the fastest path with a hard accounting block proving rows and timestamps cohere. Use when a pipeline or backfill is too slow and must get faster without losing data correctness."
metadata:
  origin: ECC-adaptation
---

# Data Throughput Accelerator — portable workflow

Diagnose and accelerate large data movement — ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, and table synchronization — by isolating the true bottleneck, benchmarking variants, and codifying the fastest path with a hard accounting block proving rows and timestamps cohere. Use when a pipeline or backfill is too slow and must get faster without losing data correctness.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-performance-profiling`, `bosskuai-subagent-delegation`, `architecture-decision-records`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. First Distinction.
2. Fast Path Heuristics.
3. Workflow.
4. Accounting Output.
5. Guardrails.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the database or warehouse server version (for example `SELECT VERSION();` on MySQL), the client driver version in the lockfile, and each one's latest stable release, checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Workflow”, “Accounting Output” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Benchmark on a copy of production with its real row sizes and types, such as wide text, nulls and DECIMAL money. A sample of the first thousand rows hides the slow cases.
- Make each batch safe to retry: load into a staging table or behind a unique key, so no rows are written twice, and check the accounting block against the source before promotion.
- Run large loads in chunks, off-peak, and watch the target's locks and connection limits. The fastest load can block production writes.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
