# Saved benchmark results

These files are the evidence behind the numbers in the main [README](../../README.md). The method, rules, and limits are in the [benchmark notes](../../docs/benchmarks/README.md).

| Folder or file | What it holds |
|---|---|
| `raw/*.jsonl` | One row per agent run: model, version, task, tokens, turns, tool calls, hidden-test result. Free text is cut to 240 characters, and account and folder names are replaced with placeholders. |
| `overhead.json`, `routing-live.json`, `coding-test.json`, `hard.json`, `memory.json`, `humaneval.json` | Summaries computed from `raw/` by `scripts/benchmark_agent.py` (`overhead-report`, `routing-report`, `report`). |
| `routing-heldout.json` | The offline skill-search comparison, from `scripts/benchmark_routing_heldout.py`. It makes no model calls. |

`raw/timeouts-first-attempt.jsonl` holds the first tries of the runs that hit the 25-minute limit while the model service was slow. Each was run again with a 60-minute limit, and the rerun is the one counted in the other files.

The live skill-use check on 73 requests with the older router, quoted in the benchmark notes (55% and 27%), has no file in this folder. Its rows are in git history: `git show 9a1eb6d:benchmarks/results/raw/routing.jsonl`.

`latest/` is where `scripts/benchmark_agent.py` writes by default. Git ignores it because its rows are not scrubbed; run `compact` to make a copy you can commit.

Raw files are named after the check and the model: `coding-*` (17 coding test tasks), `hard-*` (14 harder test tasks), `memory-*` (22 two-session tasks: the 10 in `benchmarks/tasks/memory` and the 12 in `benchmarks/tasks/memory-rules`), `humaneval-*` (40 problems), `routing.jsonl` (live skill use), `overhead.jsonl` (first call of a session).

## Where the numbers come from

- **With BosskuAI:** commit `02ee2f2` (`02ee2f2212b4493970993839d8f41e0e9045394e`). It was committed before the final runs started, and the runs read a copy exported from that commit. The rows are tagged `after`.
- **Without BosskuAI:** the rows tagged `baseline`, run at the same time on the same tasks.
- **Previous release (internal check, not published in the README):** commit `8adea49`, run from a `git archive` copy. Only the session-overhead rows are tagged `before` in `raw/overhead.jsonl`.
- **Agent:** Claude Code 2.1.284, headless, one run per row. Session overhead used Claude Haiku 4.5 and Claude Sonnet 5.5 with the author's own login; every other run used Ollama Cloud through its Anthropic-compatible API.
- **Date:** 1 October 2026.

## Check them

```bash
python -m unittest tests.test_results_consistent -v
```

The test recomputes every summary from `raw/`, redraws every chart in `docs/assets/`, and rebuilds the README text, then fails on any difference. It also fails if a saved coding run was ended by a dollar cap, or if a saved row carries a home folder path or a provider request id (in `raw/` or `raw/earlier/`).

`python scripts/make_charts.py --readme docs/benchmarks/results.md` rewrites the results page from these files. It stops with exit code 1 and changes nothing when one of the summary files is missing; pass `--allow-partial` to rewrite the page anyway.
