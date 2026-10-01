# Saved benchmark results

These files are the evidence behind the numbers in the main [README](../../README.md). The method, rules, and limits are in the [benchmark notes](../../docs/benchmarks/README.md).

| Folder or file | What it holds |
|---|---|
| `raw/*.jsonl` | One row per agent run: model, version, task, tokens, turns, tool calls, hidden-test result. Free text is cut to 240 characters. |
| `overhead.json`, `routing-live.json`, `coding-test.json`, `humaneval.json` | Summaries computed from `raw/` by `scripts/benchmark_agent.py` (`overhead-report`, `routing-report`, `report`). |
| `routing-heldout.json` | The offline skill-search comparison, from `scripts/benchmark_routing_heldout.py`. It makes no model calls. |

## Where the numbers come from

- **With BosskuAI:** commit `b167823` (`b16782342726fb7d68ba60846107a2fbef1af613`). The test runs started after it was committed.
- **Previous release (internal check, not published in the README):** commit `8adea49`, run from a `git archive` copy. Its rows are the ones tagged `before` in `raw/`.
- **Without BosskuAI:** the rows tagged `baseline`; the BosskuAI rows are tagged `after`.
- **Agent:** Claude Code 2.1.284, headless, one run per row. Session overhead used Claude Haiku 4.5 and Claude Sonnet 5.5 with the author's own login; every other run used Ollama Cloud through its Anthropic-compatible API.
- **Date:** 1 October 2026.

## Check them

```bash
python -m unittest tests.test_results_consistent -v
```

The test recomputes every summary from `raw/`, redraws every chart in `docs/assets/`, and rebuilds the README table, then fails on any difference. It also fails if a saved coding run was ended by a dollar cap.
