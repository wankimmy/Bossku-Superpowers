import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_charts as charts  # noqa: E402


def arm(passed, runs, tokens_in, tokens_out, edited=None, unchecked=0, timeouts=0):
    row = {"runs": runs, "passed": passed, "pass_rate": passed / runs, "pass_ci": [0.0, 1.0],
           "input_tokens_mean": tokens_in, "output_tokens_mean": tokens_out, "timeouts": timeouts}
    if edited is not None:
        row.update({"edited_runs": edited, "unchecked_finishes": unchecked, "unchecked_rate": unchecked / edited})
    return row


def coding(model="nemotron-3-nano:30b", gain=(0.05, 0.30)):
    return {"models": {model: {
        "arms": {"baseline": arm(10, 34, 85_000, 5_000, edited=34, unchecked=20),
                 "before": arm(11, 34, 200_000, 8_000, edited=34, unchecked=8),   # an older version: never drawn
                 "after": arm(16, 34, 150_000, 7_000, edited=34, unchecked=2, timeouts=3)},
        "paired": {"after": {"passed": {"tasks": 17, "mean_diff": 0.18, "ci": list(gain)}}}}}}


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


def memory():
    data = coding("claude-sonnet-5-5")
    data["models"]["claude-sonnet-5-5"]["arms"]["after"]["saved_a_note_rate"] = 0.9
    return data


def live():
    return {"deepseek-v4.1-flash": {"after": {"prompts": 73, "rate": 0.49, "ci": [0.38, 0.61]}}}


def save(folder: Path, **files):
    for name, content in files.items():
        (folder / name).write_text(json.dumps(content), encoding="utf-8")


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
        self.assert_svg(charts.chart_memory(memory()))

    def test_missing_data_skips_a_chart_instead_of_failing(self):
        self.assertIsNone(charts.chart_session_overhead({}))
        self.assertIsNone(charts.chart_routing({}))
        self.assertIsNone(charts.chart_pass_rates({}, {}))
        self.assertIsNone(charts.chart_checking({"models": {"m": {"arms": {"baseline": arm(1, 2, 1, 1)}}}}))

    def test_only_two_setups_are_drawn_and_named_plainly(self):
        svg = charts.chart_pass_rates(coding(), {})
        self.assertIn("Without BosskuAI", svg)
        self.assertIn("With BosskuAI", svg)
        self.assertNotIn("before", svg.lower())
        self.assertIn('class="s1"', svg)
        self.assertNotIn('class="s2"', svg)   # a third setup would need a third series

    def test_bars_start_at_one_baseline_and_labels_state_the_value(self):
        svg = charts.chart_routing(routing())
        self.assertIn("74%", svg)
        self.assertIn("60%", svg)
        self.assertNotIn("59%", svg)
        self.assertIn("prefers-color-scheme:dark", svg)


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.results = Path(self.tmp.name)

    def test_the_tables_quote_the_saved_numbers(self):
        save(self.results, **{"coding-test.json": coding(), "routing-heldout.json": routing(), "overhead.json": overhead(),
                              "routing-live.json": live()})
        text = charts.results_markdown(self.results)
        for expected in ("29% (10/34)", "47% (16/34)", "12,500", "74%", "6%", "49%"):
            self.assertIn(expected, text)
        self.assertNotIn("19,000", text)   # the older version stays out of the README
        self.assertIn("Without BosskuAI | With BosskuAI", text)

    def test_a_clear_gain_a_tie_and_a_loss_are_worded_differently(self):
        gain = charts.pass_bullet("nemotron-3-nano:30b", coding()["models"]["nemotron-3-nano:30b"], "tasks")
        self.assertIn("finished more tasks", gain)
        self.assertIn("+18 points", gain)
        self.assertIn("3 of the 34 runs with BosskuAI", gain)
        tie = charts.pass_bullet("m", coding("m", gain=(-0.05, 0.2))["models"]["m"], "tasks")
        self.assertIn("no clear difference", tie)
        loss = charts.pass_bullet("m", coding("m", gain=(-0.3, -0.05))["models"]["m"], "tasks")
        self.assertIn("finished fewer tasks", loss)

    def test_a_model_already_at_the_ceiling_is_said_to_have_no_room(self):
        block = coding("strong", gain=(-0.05, 0.1))["models"]["strong"]
        block["arms"]["baseline"] = arm(32, 34, 100_000, 4_000)
        block["arms"]["after"] = arm(33, 34, 160_000, 6_000)
        self.assertIn("near the ceiling", charts.pass_bullet("strong", block, "tasks"))

    def test_every_summary_is_built_from_the_data(self):
        save(self.results, **{"coding-test.json": coding(), "routing-heldout.json": routing(), "overhead.json": overhead(),
                              "routing-live.json": live(), "memory.json": memory()})
        blocks = charts.block_text(self.results)
        self.assertIn("saved the rule as a note 90%", blocks["summary-memory"])
        self.assertIn("+2,500 tokens", blocks["summary-overhead"])
        self.assertIn("74%", blocks["summary-routing"])
        self.assertIn("49%", blocks["summary-routing"])
        self.assertIn("finished more tasks", blocks["summary-pass"])
        self.assertIn("59%", blocks["summary-checking"])
        self.assertIn("6%", blocks["summary-checking"])
        self.assertIn("tokens per run", blocks["summary-effort"])
        self.assertIn("Nemotron 3 Nano 30B finished more tasks", blocks["summary-overall"])
        self.assertTrue(all(blocks[name] for name in blocks), blocks)

    def test_a_missing_result_gives_an_empty_summary_not_an_error(self):
        blocks = charts.block_text(self.results)
        self.assertEqual(set(blocks.values()), {""})


class ReadmeBlockTests(unittest.TestCase):
    def test_blocks_are_replaced_in_place_and_stay_stable(self):
        text = "intro\n<!-- results:start -->\nold\n<!-- results:end -->\nmid\n<!-- summary-pass:start -->\n<!-- summary-pass:end -->\nend\n"
        once = charts.inject_block(text, "results", "NEW")
        self.assertEqual(once, "intro\n<!-- results:start -->\nNEW\n<!-- results:end -->\nmid\n<!-- summary-pass:start -->\n<!-- summary-pass:end -->\nend\n")
        self.assertEqual(charts.inject_block(once, "results", "NEW"), once)
        self.assertEqual(charts.inject_block(text, "summary-effort", "X"), text)   # no such block: nothing changes

    def test_the_file_is_rewritten_only_when_something_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text("<!-- results:start -->\nold\n<!-- results:end -->\n", encoding="utf-8")
            self.assertTrue(charts.inject_all(readme, {"results": "NEW"}))
            self.assertFalse(charts.inject_all(readme, {"results": "NEW"}))
            readme.write_text("no markers here", encoding="utf-8")
            with self.assertRaises(SystemExit):
                charts.inject_all(readme, {"results": "NEW"})


if __name__ == "__main__":
    unittest.main()
