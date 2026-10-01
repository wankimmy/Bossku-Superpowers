# Routing benchmark

This offline comparison measures BosskuAI's lexical routing against an ID/description-only keyword baseline on the existing curated regression corpus. It makes no model calls and requires only Python's standard library.

## Recorded results

The [machine-readable snapshot](routing.json) contains every prompt, defensible answer set, predicted ID, ranked score, and pass/fail outcome.

| Method | Top-one hits | Top-three hits |
|---|---:|---:|
| BosskuAI `find_skill` / `rank_skills` | 82/82 (100%) | 82/82 (100%) |
| ID/description-only keyword baseline | 46/82 (56.10%) | 61/82 (74.39%) |

Top one passes when the primary skill ID belongs to the prompt's expected set. Top three passes when at least one defensible ID appears in the first three candidates. Alternative defensible IDs are accepted; top-three scoring does not require every expected alternative to be selected.

These two columns measure legacy search ranking. The snapshot reports the actual `select_skill_stack` policy separately under `results.automatic_selection`, with every miss listed. Its actionable-route score accepts an expected model-invoked primary, or, for an entirely user-only expected set, an expected skill explicitly deferred for user invocation. Automatically loading any user-only skill fails that outcome. The model-primary and user-invocation groups have separate denominators; a command deferral is not an automatic-loading success.

| Automatic-selector outcome | Hits |
|---|---:|
| Defensible model primary | 79/79 (100%) |
| User-only command correctly deferred | 3/3 (100%) |
| All actionable route outcomes | 82/82 (100%) |

## Reproduce

From the repository root:

```console
python scripts/benchmark_routing.py
python scripts/benchmark_routing.py --check
python -m unittest discover -s tests -p test_routing_benchmark.py -v
```

The first command regenerates `docs/benchmarks/routing.json`. `--check` recomputes the benchmark and compares the recorded routing-input fingerprint and results; it exits nonzero if they differ. It ignores the recorded Git revision, dirty flag, and Python version so committing the same inputs does not invalidate the result. The script builds a fresh index in memory and passes it to the public routing APIs; it neither rewrites nor relies on the installed/generated routing cache. An input change during the run fails the benchmark instead of publishing a mixed snapshot.

The snapshot records the source Git revision and working-tree state, hashes of routing code and corpus inputs, a hash of the fresh index, and a corpus hash. Text-file hashes normalize line endings to LF through Python's text reader. The routing-input fingerprint identifies the measured working-tree content even when its revision records the preceding commit.

## Corpus and baseline

The corpus comes from the literal `ROUTING_CASES` and `REVIEW_ROUTING_CASES` assignments in [tests/test_routing.py](../../tests/test_routing.py). The script reads them with AST literal evaluation without importing or executing the test module. Identical prompts merge into one case with the union of their defensible IDs and source groups. The current corpus has 82 unique prompts. Both methods return candidates from the same installable inventory, excluding `NOT_INSTALLED` IDs such as `x402`.

The baseline uses only each skill ID and description. It removes the `bosskuai-` ID prefix, spaces the remaining hyphens, and applies the same `bossku.index.tokenize` normalization to documents and queries. Each document and query uses a set of terms. For `N` eligible documents, a term's weight is `log(1 + N / (1 + df(term)))`. A document's score is its matched query weight divided by total query weight; unseen query terms use the maximum document IDF. Ties sort by skill ID. The baseline adds no curated triggers, exclusions, aliases, body headings, phrase bonuses, or query-side morphological variants.

BosskuAI's top-one result uses `find_skill`; its top-three result uses `rank_skills`. Their normal routing behavior remains intact, including alias handling and curated evidence. Numeric scores from the two methods use different scales and should not be compared as confidence probabilities.

## Limits

The router has been tuned against these regression prompts. This corpus is not held-out, and these scores do not establish accuracy on unseen prompts. The benchmark measures candidate ranking and primary/defer policy outcomes, not whether every useful complement was selected, host loading, or task completion. Some corpus cases request user-invoked skills; a ranking hit does not authorize automatic loading.

There are no real coding runs or token-consumption measurements in this benchmark. It cannot establish coding-quality improvements, token savings, cost reductions, latency changes, or optional-runtime reliability. Keep those claims unmeasured until a separate task-level evaluation exists.
