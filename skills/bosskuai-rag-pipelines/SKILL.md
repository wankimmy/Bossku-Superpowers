---
name: bosskuai-rag-pipelines
description: "Use when building or fixing retrieval-augmented generation pipelines: chunking, embedding choice, vector index and metadata filtering, hybrid search, re-ranking, and retrieval evals on a golden set."
---

# BosskuAI RAG Pipelines

Use this skill when an LLM answers from retrieved documents and the question is whether retrieval returns the right context. Check retrieval before blaming the model, and measure it.

## How this differs from nearby skills

- **`bosskuai-eval-driven-agent-improvement`**: general agent and LLM eval harnesses, including retrieval tests. This skill is the RAG build side: chunking, indexes, hybrid search, re-ranking. Use both: build here, score there.
- **`bosskuai-search-relevance`**: Elasticsearch/OpenSearch ranking and judgment lists for user-facing search. Use that when the consumer is a search box, this one when the consumer is an LLM.
- **`bosskuai-postgres-patterns`** and **`bosskuai-database-engineering`**: general SQL, indexing, and query plans. Here only the vector-column and filter choices.
- **`bosskuai-mle-workflow`**: model training and deployment, not retrieval systems.
- **`bosskuai-redis-caching-queues`**: queue mechanics for ingestion workers.
- **`bosskuai-deep-research`**: research done by an agent over the web, not a retrieval index you operate.

## Principles

- No change without a before and after eval run. "It feels better" is not evidence.
- Chunk for retrieval, not for ease of ingestion. Pick structural (headers), recursive, or semantic chunking by document type, then tune size and overlap by ablation.
- Test embedding models on a sample of your own corpus. A benchmark rank does not guarantee domain fit.
- Design the metadata schema before the index schema. Filter by scope (tenant, source, date, language) before similarity runs. In multi-tenant data, the filter is also an isolation boundary.
- Hybrid search (dense plus keyword) helps with exact terms, names, and codes. Fuse by rank (for example reciprocal rank fusion) rather than mixing raw scores. Tune weights on the golden set.
- Re-ranking is not free. Add a cross-encoder only when precision is the bottleneck and the latency budget allows. Keep it only if the eval shows a gain.
- Ingestion is I/O-bound: batch embedding calls, handle rate limits, and bulk insert. Confirm embedding output order or index matches the input.
- Index settings (HNSW vs IVFFlat, build and search parameters) trade recall against build time, memory, and latency. Benchmark on your data and check the installed version.

## Workflow

1. Audit the corpus: types, lengths, structure, languages, vocabulary. List the real query types.
2. Build a small golden set of queries with their relevant chunks or answers.
3. Compare at least two embedding models by recall@k on that set.
4. Build ingestion with metadata, batching, and chunk quality checks before bulk load.
5. Baseline: recall@k, precision, faithfulness, answer relevance, p95 latency.
6. Change one variable at a time (chunk size, overlap, top-k, fusion weight, re-ranker). Keep only changes that improve the target metric without hurting others.
7. In production, log query, retrieved chunk ids, scores, and latency. Watch for drift, such as falling top-1 similarity.

## Diagnosis hints

- Low recall with relevant text split across chunks: chunking problem.
- Right chunk retrieved but answer wrong: generation or context assembly problem.
- Misses on codes, names, or rare terms: add lexical retrieval.
- Good recall but noisy top results: filter first, then consider re-ranking.

## Guardrails

- Do not send private documents to an external embedding service without confirming policy.
- Do not skip dedupe in context assembly; repeated chunks waste the prompt.
- Agentic retries (reformulate, retrieve again) need an attempt cap.

## Output format

```text
Corpus and queries: [summary]
Chunking and metadata: [strategy, schema]
Retrieval: [index, hybrid, re-ranker decision]
Eval: [golden set size, metrics before/after]
Next experiment: [single variable]
```

Adapted from agency-agents/engineering/engineering-rag-pipeline-engineer.md (agency-agents, MIT).
