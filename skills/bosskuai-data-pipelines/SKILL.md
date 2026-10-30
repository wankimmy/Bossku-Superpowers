---
name: bosskuai-data-pipelines
description: Use when building or fixing batch or streaming data pipelines (ETL/ELT, CDC, bronze/silver/gold layers, dbt or Spark jobs) where reruns, schema drift, freshness, or data quality decide whether the data can be trusted.
---

# BosskuAI Data Pipelines

Use this skill to design, build, or review a pipeline that moves raw data into trusted tables for analytics, BI, or ML.

## How this differs from nearby skills

- **`bosskuai-data-architecture`**: entity modeling, ownership, retention, warehouse boundaries. This skill is the pipeline mechanics: idempotent loads, layers, contracts, freshness, backfills.
- **`bosskuai-data-throughput-accelerator`**: finding why a large data move is slow. Use it when the pipeline is correct but too slow.
- **`bosskuai-database-engineering`**: indexes, query plans, online migrations of an application database.
- **`bosskuai-clickhouse-io`**: ClickHouse-specific tables and queries.
- **`bosskuai-observability-sre`**: general alerts and SLOs. Here only the data-specific signals are listed.
- **`bosskuai-mle-workflow`**: training and model deployment, not the upstream data load.

## Principles

- Every load is idempotent: rerunning the same window gives the same result and no duplicates. Prefer merge on a key, or replace of an explicit date window, over blind append.
- Layers have one job each. Bronze is raw, append-only, with source and ingest metadata. Silver is cleaned, deduplicated, and typed. Gold is shaped for a business question.
- Consumers read gold, not bronze or silver, so upstream fixes do not break them.
- Write the data contract first: schema, ownership, freshness target, consumers. Schema drift should raise an alert, not silently change a column.
- Handle nulls on purpose per field: impute, flag, or reject. Do not let nulls flow into gold by accident.
- Recompute gold from a complete silver snapshot for a stated window. A partial batch can leave stale rows behind, for example revenue that was refunded.
- Incremental and CDC loads cost less than full refresh, but only when the source gives a reliable change key or log. Check that before choosing.
- Streaming versus micro-batch is a latency and cost choice. Pick the slowest option that meets the freshness target.
- Keep audit columns (created, updated, source system) and prefer soft deletes where history matters.

## Workflow

1. Profile the sources: row counts, null rates, key cardinality, update pattern, whether change capture exists.
2. Write the contract and the lineage map before writing pipeline code.
3. Build bronze with no transformation; record source file and ingest time.
4. Build silver: dedupe on key plus event time, standardize types, formats, and codes, and decide each null rule.
5. Build gold for named questions; agree the contract with consumers before deploying.
6. Add checks at each layer (see checklist) and a freshness alert.
7. Write a short runbook per pipeline: what breaks, how to rerun or backfill, who owns it.

## Checklist

- Rerun of the same window changes nothing. Test it.
- Unique key, not-null, accepted-range, and relationship checks exist on silver and gold.
- Row-count and freshness checks alert when a load is late or suspiciously small.
- Schema change from the source is detected before it reaches consumers. Compare types as well as names: an integer that turns into text, or a `DECIMAL(12,2)` that turns into a float, passes a name check and breaks sums.
- Backfill path exists and does not double-count.
- Incremental loads: an `updated_at` high-water mark misses any row that commits after the mark has moved to or past the row's `updated_at`. Same-second writes, long transactions, and clock skew all cause this. The mark never shows hard deletes. A soft delete shows only if its write also sets `updated_at`. Re-read a safety overlap, dedupe on the key, and capture deletes from the source's change log or CDC.
- Late-arriving and out-of-order events have a stated rule.
- Streaming jobs have a checkpoint location and a restart plan.
- Secrets and credentials are not in job code; PII columns are marked and access-limited. Bronze keeps raw values, so PII lands there first: restrict bronze access to the roles that need it. If a field must not be stored at all, the data contract names it, and the load log records the field name (never its value), because bronze cannot replay that field.
- Check the installed versions of Spark, Delta, Iceberg, or dbt before relying on a feature. Run `dbt --version` and `spark-submit --version`, and check that dbt-core and each adapter are compatible releases.
- Check the change against the shared bar, `../../references/checklists/engineering-quality-bar.md`: production data copy, types, deploy steps and proof.

## Guardrails

- Do not transform bronze in place.
- Do not "fix" bad data by dropping rows without logging what was dropped.
- Do not run a destructive overwrite or backfill on production without a stated window and a way back.
- Do not run a Spark overwrite until you know `spark.sql.sources.partitionOverwriteMode`. The default `static` mode can replace more partitions than the window you rebuild. Test it on a copy first.
- Do not MERGE a source that has two rows for one key. Delta can fail when two source rows match one target row and the merge updates it, and the docs do not say what an insert-only MERGE does. Other table formats and warehouses differ, so dedupe the source to one row per key first.

## Output format

```text
Sources and contract: [schema, owner, freshness target]
Versions: [Spark, dbt-core, adapter, table format; checked date]
Layers: [bronze / silver / gold tables and keys]
Idempotency rule: [merge key or replace window]
Quality checks: [list]
Alerts and runbook: [signals, owner]
Verification: [rerun test, check results]
```

Adapted from agency-agents/engineering/engineering-data-engineer.md (agency-agents, MIT).
