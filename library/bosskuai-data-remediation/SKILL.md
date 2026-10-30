---
name: bosskuai-data-remediation
description: "Use when bad rows already reached your pipeline and must be fixed at scale: cluster anomalies into patterns, have a local model propose a sandboxed fix function, then stage, audit, and quarantine with zero row loss."
---

# BosskuAI Data Remediation

Use this skill for the repair layer after deterministic validation has isolated suspect rows. The model proposes fix logic; code executes and audits it; nothing is written to production unreviewed.

## How this differs from nearby skills

- **`bosskuai-data-pipelines`**: building the pipeline (idempotency, freshness, schema drift). This skill starts after rows are flagged and decides how to repair them.
- **`bosskuai-data-architecture`**: schemas and ownership. This skill does not redesign them.
- **`bosskuai-regex-vs-llm-structured-text`**: pick regex first when a pattern is simple. Use model-generated fixes only for the leftover families.
- **`bosskuai-rag-pipelines`**: shares embedding and vector-store tools but for retrieval, not repair.

## Workflow

1. Take only rows tagged by the deterministic layer (null, type, regex, range checks already ran). Queue them so the main pipeline does not wait.
2. Compress: embed suspect values locally, cluster them, and pull a few representative samples per cluster. Combine similarity with a hash of the primary key so distinct records never merge.
3. Ask a local model (data stays inside your network) for a single transformation expression per cluster in a strict JSON shape, plus a confidence value and a one-line reason.
4. Gate the output before running it: parse it, allow a narrow whitelist (for example one lambda or one SQL expression), reject imports, exec or eval, file, network, and shell access. Prefer a real expression parser or restricted evaluator over raw `eval`. Rejected clusters go to quarantine.
5. Apply the accepted function over the whole cluster in a staging schema, not production. Low confidence goes to human review.
6. Gate promotion with tests (row counts, type and range tests, sampled human review). Run the batch first on a masked copy of production data in a non-production environment the user approves: mask personal fields and keep each field's type, and test the function on the value types production stores.
7. Reconcile every batch: source rows must equal fixed rows plus quarantined rows. Any gap stops promotion and raises an alert. A second run of the same batch must not change any row it already fixed or quarantined.
8. Log per change: row id, old value, new value, function applied, confidence, model version, library versions, timestamp.

## Guardrails

- The model writes logic, never final data. Do not let it edit rows directly.
- Do not send PII or regulated data to an external API. If a cloud model is the only option, ask the user first.
- Executing generated code is the main risk. Sandbox it, set timeouts, and review the whitelist.
- Choose confidence and review thresholds from a labelled sample, not a guess.
- Keep a rollback path: staged output plus the audit log.
- Promote in small batches, each with a batch id. A rerun skips batches already promoted, and no production table stays locked for a whole run.
- Keep a restore point (a backup or snapshot) of the rows before promotion, and test the restore on the copy.
- Before promotion, list the reports and screens that read the changed rows, and tell the user what they will see.

## Output format

```text
Batch: [source rows, flagged rows]
Clusters: [id, size, pattern, representative samples]
Proposed fix: [expression, confidence, gate result]
Outcome: [fixed, quarantined, rejected]
Reconciliation: [source = fixed + quarantined? yes/no]
Audit log location and rollback step: [..]
```

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from agency-agents/engineering/engineering-ai-data-remediation-engineer.md (agency-agents, MIT).
