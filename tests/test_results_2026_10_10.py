"""The 10 October 2026 result set: the saved summary, the tables of its page and the scrubbing of its rows must match the raw rows.

`benchmarks/results/raw/2026-10-10/` is the source of truth. `benchmarks/results/2026-10-10.json` is recomputed from it
(the same functions as `benchmark_agent.py report`), and the marked tables of `docs/benchmarks/results-2026-10-10.md` are
rebuilt from that summary. The 1-8 October files are checked by test_results_consistent.py and are not touched here.
"""

import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.benchmark_agent import coding_report, excluded, scrub  # noqa: E402
from scripts.summarize_run_set import BOTH, SUITES, marker, render, split_name, summarize  # noqa: E402
from tests.test_results_consistent import same  # noqa: E402

RAW = ROOT / "benchmarks" / "results" / "raw" / "2026-10-10"
SAVED = ROOT / "benchmarks" / "results" / "2026-10-10.json"
PAGE = ROOT / "docs" / "benchmarks" / "results-2026-10-10.md"
ARMS = {"baseline", "ship", "ship2"}


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RunSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = sorted(RAW.glob("*.jsonl"))
        cls.saved = json.loads(SAVED.read_text(encoding="utf-8"))

    def test_the_set_is_committed(self):
        self.assertTrue(self.files, f"no raw rows in {RAW}")
        self.assertTrue(PAGE.exists())

    def test_the_saved_summary_matches_its_rows(self):
        self.assertEqual(same(summarize(RAW), self.saved), [])

    def test_the_page_tables_are_rebuilt_from_the_saved_summary(self):
        page = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")
        for name, expected in render(self.saved).items():
            with self.subTest(block=name):
                start, end = marker(name, "start"), marker(name, "end")
                self.assertIn(start, page, f"the page is missing the {name} block")
                self.assertEqual(page.split(start, 1)[1].split(end, 1)[0].strip("\n"), expected)

    def test_a_cell_with_a_baseline_in_the_same_run_matches_the_report_command(self):
        """`benchmark_agent.py report` on the same files gives the arms and the paired differences of the summary."""
        by = {split_name(path): path for path in self.files}
        for suite in SUITES:
            for model, cell in self.saved["suites"][suite].items():
                if cell["arms"] and cell["baseline_source"] == "same run":
                    with self.subTest(suite=suite, model=model):
                        report = coding_report([str(by[(suite, model)])])["models"][model]
                        self.assertEqual(same(report["arms"], cell["arms"]), [])
                        self.assertEqual(same(report["paired"], cell["paired"]), [])
        for model, cell in self.saved["suites"][BOTH].items():
            if cell["baseline_source"] == "same run":
                with self.subTest(suite=BOTH, model=model):
                    report = coding_report([str(by[("memory", model)]), str(by[("memory-rules", model)])])["models"][model]
                    self.assertEqual(same(report["arms"], cell["arms"]), [])
                    self.assertEqual(same(report["paired"], cell["paired"]), [])

    def test_excluded_runs_are_counted_and_never_scored(self):
        for path in self.files:
            suite, model = split_name(path)
            cell = self.saved["suites"][suite][model]
            task_rows = [r for r in rows(path) if r["kind"] == "task"]
            scored = [r for r in task_rows if not excluded(r)]
            reused = 0 if cell["baseline_source"] == "same run" else cell["baseline_source"]["runs"]
            with self.subTest(file=path.name):
                self.assertEqual(sum(s["runs"] for s in cell["arms"].values()) - reused, len(scored))
                self.assertEqual(sum(cell["excluded_runs"].values()), len(task_rows) - len(scored))
                for r in task_rows:
                    if excluded(r):
                        self.assertFalse(r.get("passed"), f"{r['run_id']} is excluded but carries a pass")

    def test_every_row_names_its_model_and_a_known_setup(self):
        for path in self.files:
            suite, model = split_name(path)
            self.assertIn(suite, SUITES)
            for r in rows(path):
                with self.subTest(file=path.name, run=r["run_id"]):
                    self.assertEqual(r["model"], model)
                    self.assertIn(r["arm"], ARMS)
                    self.assertIn(r["kind"], {"task", "selftest"})

    def test_the_rows_carry_no_account_name_folder_path_or_request_id(self):
        """What `compact` is for: the author's account name, home folder, the Ollama account and request ids are gone."""
        home = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+\w|(?<![\w.])/(?:home|Users)/\w")
        request_id = re.compile(r"\(ref: [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)")
        account = re.compile(r"you \((?!<user>\))[^)\s]+\) have reached")
        author = re.compile(r"\bAdmin\b")   # the author's Windows account name, as scrub() would have replaced it
        for path in self.files:
            with self.subTest(file=path.name):
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    where = f"{path.name}:{number}"
                    self.assertIsNone(home.search(line), f"{where} has a home folder path")
                    self.assertIsNone(request_id.search(line), f"{where} has a provider request id")
                    self.assertIsNone(account.search(line), f"{where} names the provider account")
                    self.assertIsNone(author.search(line), f"{where} has the author's account name")
                    with mock.patch.object(Path, "home", return_value=Path("/zz-bench-sentinel")):
                        # scrub() also replaces the word that is this machine's account name; a fixed name that
                        # no row contains keeps the round trip the same on every machine
                        self.assertEqual(scrub(line), line, f"{where} still has something `compact` would replace")


if __name__ == "__main__":
    unittest.main()
