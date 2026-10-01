import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_charts as charts  # noqa: E402


def arm(passed, runs, tokens_in, tokens_out, edited=None, unchecked=0):
    low, high = (0.0, 1.0)
    row = {"runs": runs, "passed": passed, "pass_rate": passed / runs, "pass_ci": [low, high],
           "input_tokens_mean": tokens_in, "output_tokens_mean": tokens_out}
    if edited is not None:
        row.update({"edited_runs": edited, "unchecked_finishes": unchecked, "unchecked_rate": unchecked / edited})
    return row


def coding(model="nemotron-3-nano:30b"):
    return {"models": {model: {"arms": {
        "baseline": arm(10, 34, 85_000, 5_000, edited=34, unchecked=20),
        "before": arm(11, 34, 200_000, 8_000, edited=34, unchecked=8),
        "after": arm(16, 34, 150_000, 7_000, edited=34, unchecked=2),
    }}}}


def routing():
    def stats(top1, top3, covered=None, whole=None):
        row = {"prompts": 73, "top1": {"rate": top1, "ci": [top1 - 0.1, top1 + 0.1]},
               "top3": {"rate": top3, "ci": [top3 - 0.1, top3 + 0.1]}}
        if covered is not None:
            row.update({"concern_coverage": covered, "all_concerns_covered": {"rate": whole}})
        return row
    return {"splits": {"test": {"description-only": stats(0.6, 0.77), "before": stats(0.59, 0.9, 0.51, 0.4),
                                "after": stats(0.74, 0.9, 0.7, 0.56)}}}


def overhead():
    return {"claude-sonnet-5-5": {a: {"runs": 3, "input_tokens_median": tokens, "cost_median": cost, "context_window": 1_000_000}
                                  for a, tokens, cost in (("baseline", 10_000, 0.02), ("before", 19_000, 0.055), ("after", 12_500, 0.027))}}


class ChartTests(unittest.TestCase):
    def assert_svg(self, svg):
        self.assertIsNotNone(svg)
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("viewBox", root.attrib)

    def test_every_chart_is_well_formed_svg(self):
        self.assert_svg(charts.chart_session_overhead(overhead()))
        self.assert_svg(charts.chart_routing(routing()))
        self.assert_svg(charts.chart_pass_rates(coding(), coding("deepseek-v4.1-flash")))
        self.assert_svg(charts.chart_checking(coding()))
        self.assert_svg(charts.chart_effort(coding()))

    def test_missing_data_skips_a_chart_instead_of_failing(self):
        self.assertIsNone(charts.chart_session_overhead({}))
        self.assertIsNone(charts.chart_routing({}))
        self.assertIsNone(charts.chart_pass_rates({}, {}))
        self.assertIsNone(charts.chart_checking({"models": {"m": {"arms": {"baseline": arm(1, 2, 1, 1)}}}}))

    def test_bars_start_at_one_baseline_and_labels_state_the_value(self):
        svg = charts.chart_routing(routing())
        self.assertIn("74%", svg)
        self.assertIn("59%", svg)
        self.assertIn("prefers-color-scheme:dark", svg)

    def test_the_summary_tables_quote_the_saved_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp)
            (results / "coding-test.json").write_text(json.dumps(coding()), encoding="utf-8")
            (results / "routing-heldout.json").write_text(json.dumps(routing()), encoding="utf-8")
            (results / "overhead.json").write_text(json.dumps(overhead()), encoding="utf-8")
            text = charts.results_markdown(results)
        self.assertIn("29% (10/34)", text)
        self.assertIn("47% (16/34)", text)
        self.assertIn("12,500", text)
        self.assertIn("74%", text)
        self.assertIn("6%", text)  # 2 of 34 runs still ended without running their code

    def test_readme_block_is_replaced_in_place_and_stays_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(f"intro\n{charts.README_START}\nold\n{charts.README_END}\noutro\n", encoding="utf-8")
            self.assertTrue(charts.inject_results(readme, "NEW"))
            text = readme.read_text(encoding="utf-8")
            self.assertEqual(text, f"intro\n{charts.README_START}\nNEW\n{charts.README_END}\noutro\n")
            self.assertFalse(charts.inject_results(readme, "NEW"))
            readme.write_text("no markers here", encoding="utf-8")
            with self.assertRaises(SystemExit):
                charts.inject_results(readme, "NEW")


if __name__ == "__main__":
    unittest.main()
