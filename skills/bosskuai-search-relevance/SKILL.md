---
name: bosskuai-search-relevance
description: "Use when tuning Elasticsearch or OpenSearch search quality: analyzers and mappings, BM25 query structure, hybrid lexical plus vector retrieval, judgment-list evaluation with nDCG, and safe reindexing behind aliases."
---

# BosskuAI Search Relevance

Use this skill when a search box returns poor results and you need to fix it with measurement, not opinion. Most bad search is a recall problem wearing a ranking costume.

## How this differs from nearby skills

- **`bosskuai-rag-pipelines`**: retrieval for LLM context (chunking, embeddings, vector index). This skill is user-facing search ranking on Elasticsearch/OpenSearch. They share hybrid search ideas.
- **`bosskuai-eval-driven-agent-improvement`**: evals for agents and LLM output. Here the eval is a judgment list scored with nDCG/MRR.
- **`bosskuai-database-engineering`**, **`bosskuai-postgres-patterns`**, **`bosskuai-mongodb`**: database indexes and queries. Use them for SQL full-text or Mongo text search; this skill covers a dedicated search engine.
- **`bosskuai-exa-search`**: using an external web search tool, not operating your own index.
- **`bosskuai-recsys-pipeline-architect`**: feed and recommendation ranking, not query-driven search.
- **`bosskuai-performance-profiling`**: general slowness; here only query latency budgets.

## Principles

- Do not tune by anecdote. Changes are scored against a judgment list sampled from real query logs (head, torso, tail) or they do not ship.
- Fix recall first. If the right document cannot match, no boost helps. Use the analyze and explain APIs and zero-result analysis before touching scoring.
- Analyzers are a contract between index time and query time. A stemmer on one side only breaks matching. Test both sides on real vocabulary.
- Score fields, do not stuff them. A single catch-all field loses signal; title, brand, and body deserve different weights.
- Query structure: `filter` for yes/no conditions, `must` for text match with field weights, `should` for popularity and freshness nudges that do not dominate text score.
- Identifiers (SKU, model numbers) need keyword fields, not stemming.
- Map money, IDs and SKUs by hand. Dynamic mapping sets a field's type from the first value it sees. If the first document sends a price as "0.01", the field becomes text, and range queries then compare text.
- Vectors complement BM25. Semantic search can miss exact codes and rare terms. Default to hybrid with rank fusion and prove any single-mode setup on the judgment set.
- Version indices and use aliases: build `name_v2`, reindex, verify, flip the alias, keep the old index for rollback. Writes made during a `_reindex` are not in `name_v2` unless you replay or dual-write them before the flip.
- A relevance gain that breaks the latency budget is a loss. Measure `took` and avoid leading wildcards on hot paths. A response with `timed_out: true` holds partial results, so count it as a failure in tests and alerts.

## Workflow

1. Mine query logs: segment head/torso/tail, list zero-result queries and reformulations.
2. Build a graded judgment set and version it next to the query templates.
3. Baseline nDCG@10, MRR, recall@k, zero-result rate, and p95 latency.
4. Fix recall (analyzers, synonyms, typo tolerance, missing fields). Verify on failing queries.
5. Then fix precision (field weights, signals, hybrid). Score each change before stacking the next.
6. Run the judgment set in CI; fail on a drop beyond the noise threshold, with a per-query diff.
7. Ship important changes behind interleaving or an A/B test. If online results disagree with offline, roll back.
8. Refresh the judgment set regularly because queries drift.
9. Check the change against the shared bar: `../../references/checklists/engineering-quality-bar.md`.

## Triage table

| Symptom | First check |
|---|---|
| Zero results for sensible queries | analyze query text vs indexed terms; minimum_should_match |
| Right document ranks low | explain on that document; field weights |
| Exact ID queries fail | analyze the ID; add keyword subfield |
| Good head, bad tail | nDCG by frequency segment |
| Fluent but wrong semantic results | compare BM25-only, kNN-only, hybrid |

## Guardrails

- Check the installed Elasticsearch/OpenSearch version before using retriever, RRF, or synonym-set features; names and availability differ. `GET /` on the cluster returns its version number.
- Do not apply mapping changes in place on a live index.
- Do not log raw user queries without a privacy decision.
- Old and new app code read the same alias during a deploy. Before any query reads a new field, every index behind the alias must have it. Add the field through the index-version steps above, not in place, then ship the query that reads it.

## Output format

```text
Problem segment: [queries, evidence]
Versions: [cluster version from GET /, client version from the lockfile, checked date]
Baseline: [nDCG@10, zero-result rate, p95]
Change: [analyzer / query / hybrid / reindex]
Result: [metric deltas per segment]
Rollout: [experiment, alias flip, rollback]
```

Adapted from agency-agents/engineering/engineering-search-relevance-engineer.md (agency-agents, MIT).
