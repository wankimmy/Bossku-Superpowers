"""The numbers in the results page and the charts must be the numbers in the saved run files, nothing typed by hand.

Each check recomputes a summary from `benchmarks/results/raw/*.jsonl` and compares it with the committed summary,
the charts, and the results page block. A check is skipped while its result files do not exist yet.
"""

import json
import math
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_charts as charts  # noqa: E402
from scripts.benchmark_agent import coding_report, overhead_summary, routing_summary  # noqa: E402

RESULTS = ROOT / "benchmarks" / "results"
RESULTS_PAGE = ROOT / "docs" / "benchmarks" / "results.md"
RAW = RESULTS / "raw"


def same(a, b, path="") -> list[str]:
    """Differences between two JSON-like values; floats compare to 9 digits and NaN equals NaN."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = [f"{path}/{k}: missing" for k in a.keys() ^ b.keys()]
        for key in a.keys() & b.keys():
            out += same(a[key], b[key], f"{path}/{key}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: length {len(a)} != {len(b)}"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in same(x, y, f"{path}[{i}]")]
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if (isinstance(a, float) and math.isnan(a)) and (isinstance(b, float) and math.isnan(b)):
                return []
            return [] if math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) else [f"{path}: {a} != {b}"]
    return [] if a == b else [f"{path}: {a!r} != {b!r}"]


def saved(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


class SavedResultsTests(unittest.TestCase):
    def need(self, *paths: Path) -> None:
        for path in paths:
            if not path.exists():
                self.skipTest(f"{path.name} has not been generated yet")

    def test_the_overhead_summary_matches_its_rows(self):
        self.need(RAW / "overhead.jsonl", RESULTS / "overhead.json")
        self.assertEqual(same(overhead_summary([str(RAW / "overhead.jsonl")]), saved("overhead.json")), [])

    def test_the_live_routing_summary_matches_its_rows(self):
        self.need(RAW / "routing.jsonl", RESULTS / "routing-live.json")
        self.assertEqual(same(routing_summary([str(RAW / "routing.jsonl")]), saved("routing-live.json")), [])

    def test_the_coding_summaries_match_their_rows(self):
        for prefix, name in (("coding-", "coding-test.json"), ("humaneval-", "humaneval.json"),
                             ("hard-", "hard.json"), ("memory-", "memory.json")):
            with self.subTest(name=name):
                files = sorted(RAW.glob(f"{prefix}*.jsonl")) if RAW.is_dir() else []
                if not files or not (RESULTS / name).exists():
                    self.skipTest(f"{name} has not been generated yet")
                self.assertEqual(same(coding_report([str(f) for f in files]), saved(name)), [])

    def test_saved_rows_carry_no_home_folder_paths_or_provider_request_ids(self):
        files = sorted(RAW.rglob("*.jsonl")) if RAW.is_dir() else []   # raw/earlier/ is committed too
        if not files:
            self.skipTest("no raw rows yet")
        home = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+\w|(?<![\w.])/(?:home|Users)/\w")
        request_id = re.compile(r"\(ref: [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)")
        for path in files:
            with self.subTest(file=path.relative_to(RAW).as_posix()):
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    self.assertIsNone(home.search(line), f"{path.name}:{number} has a home folder path")
                    self.assertIsNone(request_id.search(line), f"{path.name}:{number} has a provider request id")

    def test_no_saved_coding_run_was_cut_short_by_a_dollar_cap(self):
        for name in ("coding-test.json", "humaneval.json", "hard.json", "memory.json"):
            if not (RESULTS / name).exists():
                continue
            for model, block in saved(name)["models"].items():
                for arm, summary in block["arms"].items():
                    self.assertEqual(summary["budget_stops"], 0, f"{name} {model} {arm}")

    def test_the_charts_are_drawn_from_the_saved_summaries(self):
        if not (RESULTS / "overhead.json").exists():
            self.skipTest("no saved results yet")
        data = lambda name: charts.load(RESULTS, name)  # noqa: E731
        drawn = {
            "benchmark-session-overhead.svg": charts.chart_session_overhead(data("overhead.json")),
            "benchmark-routing.svg": charts.chart_routing(data("routing-heldout.json")),
            "benchmark-pass-rates.svg": charts.chart_pass_rates(data("coding-test.json"), data("humaneval.json"),
                                                                data("hard.json")),
            "benchmark-checking.svg": charts.chart_checking(data("coding-test.json")),
            "benchmark-effort.svg": charts.chart_effort(data("coding-test.json"), data("hard.json"), data("memory.json")),
            "benchmark-memory.svg": charts.chart_memory(data("memory.json")),
        }
        for name, svg in drawn.items():
            path = ROOT / "docs" / "assets" / name
            with self.subTest(chart=name):
                if svg is None:
                    self.assertFalse(path.exists(), f"{name} is committed but its data is missing")
                else:
                    self.assertTrue(path.exists(), f"{name} should be committed")
                    self.assertEqual(path.read_text(encoding="utf-8").replace("\r\n", "\n"), svg)

    def test_the_readme_tables_and_summaries_are_rebuilt_from_the_saved_results(self):
        readme = RESULTS_PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")
        if charts.marker("results", "start") not in readme or not (RESULTS / "overhead.json").exists():
            self.skipTest("results page has no results block yet")
        for name, expected in charts.block_text(RESULTS).items():
            with self.subTest(block=name):
                start, end = charts.marker(name, "start"), charts.marker(name, "end")
                if not expected and start not in readme:
                    continue   # nothing was measured for this block, so the results page need not have it
                self.assertIn(start, readme, f"results page is missing the {name} block")
                shown = readme.split(start, 1)[1].split(end, 1)[0].strip("\n")
                self.assertEqual(shown, expected)

    def test_the_readme_shows_two_setups_only(self):
        readme = RESULTS_PAGE.read_text(encoding="utf-8")
        if charts.marker("results", "start") not in readme:
            self.skipTest("results page has no results block yet")
        block = readme.split(charts.marker("results", "start"), 1)[1].split(charts.marker("results", "end"), 1)[0]
        self.assertIn("Without Bossku Superpower", block)
        self.assertIn("With Bossku Superpower", block)
        self.assertNotIn("Before", block)
        self.assertNotIn("After", block)


if __name__ == "__main__":
    unittest.main()
