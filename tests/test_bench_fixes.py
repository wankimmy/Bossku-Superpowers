"""Regression tests for the benchmark scripts: arm names, cleanup after a crash, scrubbing, partial inputs, provenance.

Nothing here calls a model or touches the real home, ~/.claude or the Obsidian vault; every folder is a temp folder.
"""

import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_charts as charts  # noqa: E402
from scripts import benchmark_agent as ba  # noqa: E402
from scripts import benchmark_routing_heldout as heldout  # noqa: E402
from scripts import check_localisation_evals as cle  # noqa: E402
from scripts import skill_use_count as scu  # noqa: E402
from scripts.benchmark_rules import prepare, score  # noqa: E402


class ArmNameTests(unittest.TestCase):
    """The arm name becomes a folder under --work that build_template empties first."""

    def test_names_that_leave_the_work_folder_are_rejected(self):
        for spec in ("../../victim=.@lean", "..\\victim=.", "C:\\victim=.", "/abs=.", "a/b=.", "=.", "..=.", ".=.",
                     "-x=.", ".hidden=.", "trailing.=.", "a..b=.", "a b=."):
            with self.subTest(spec=spec), self.assertRaises(SystemExit):
                ba.parse_arm(spec)

    def test_documented_names_still_parse(self):
        for name in ("before", "after", "v1", "v2", "old-2", "my_arm", "v1.2", "A1"):
            with self.subTest(name=name):
                self.assertEqual(ba.parse_arm(f"{name}=/tmp/bossku@core").name, name)
        self.assertIsNone(ba.parse_arm("baseline").root)

    def test_a_bad_name_stops_the_run_before_anything_is_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "a" / "work"
            victim = work.parent / "victim"
            victim.mkdir(parents=True)
            (victim / "keep.txt").write_text("x", encoding="utf-8")
            task = Path(tmp) / "suite" / "t1"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({"id": "t1", "prompt": "x", "grader": {"cmd": ["true"]}}), encoding="utf-8")
            argv = ["run", "--suite", str(task.parent), "--arm", f"../../victim={ROOT}@lean", "--model", "m", "--claude", "claude",
                    "--work", str(work), "--out", str(Path(tmp) / "out"), "--dry-run"]
            with self.assertRaises(SystemExit):
                ba.main(argv)
            self.assertTrue((victim / "keep.txt").exists())


class ScrubFixTests(unittest.TestCase):
    def scrub_as(self, account, text):
        with mock.patch("pathlib.Path.home", return_value=Path("/somewhere") / account):
            return ba.scrub(text)

    def test_an_account_folder_named_home_does_not_rewrite_the_home_placeholder(self):
        self.assertEqual(self.scrub_as("home", "cd C:\\Users\\jo\\AppData\\x"), "cd <home>\\AppData\\x")
        self.assertEqual(self.scrub_as("home", "ls /home/ann/project"), "ls <home>/project")
        self.assertEqual(self.scrub_as("home", "written by home, not homer"), "written by <user>, not homer")

    def test_an_account_folder_named_user_does_not_rewrite_its_own_placeholder(self):
        self.assertEqual(self.scrub_as("user", "by user and <user>"), "by <user> and <user>")

    def test_a_provider_request_id_is_replaced_and_other_ids_are_not(self):
        text = ("usage credits: https://ollama.com/settings (ref: 76e45cb9-724a-4e4f-a28d-6e21bf55abed) "
                "task 3f2b1c4d-0000-4000-8000-000000000000")
        self.assertEqual(self.scrub_as("jo", text),
                         "usage credits: https://ollama.com/settings (ref: <request-id>) "
                         "task 3f2b1c4d-0000-4000-8000-000000000000")

    def test_the_provider_account_name_in_a_usage_limit_error_is_replaced(self):
        text = ("you (putrafyp) have reached your session usage limit, upgrade for higher limits: "
                "https://ollama.com/upgrade (ref: 76e45cb9-724a-4e4f-a28d-6e21bf55abed)")
        self.assertEqual(self.scrub_as("jo", text),
                         "you (<user>) have reached your session usage limit, upgrade for higher limits: "
                         "https://ollama.com/upgrade (ref: <request-id>)")
        plain = "you (a note) have asked; you have reached the end"
        self.assertEqual(self.scrub_as("jo", plain), plain, "only the provider's error form is rewritten")

    def test_no_saved_result_row_names_the_provider_account(self):
        # Re-run `compact` on a raw file if this fails: scrub() now removes the account name from the text.
        named = [path.name for path in sorted((ROOT / "benchmarks" / "results" / "raw").rglob("*.jsonl"))   # latest/ is ignored
                 if re.search(r"you \([^)\s<]+\) have reached", path.read_text(encoding="utf-8"))]
        self.assertEqual(named, [])

    def test_the_default_output_folder_is_not_tracked_by_git(self):
        try:
            run = subprocess.run(["git", "check-ignore", "-q", "benchmarks/results/latest/runs.jsonl"], cwd=ROOT)
        except OSError:
            self.skipTest("git is not installed")
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        self.assertEqual(run.returncode, 0, "benchmarks/results/latest/ holds unscrubbed rows and must be ignored")


class ExecuteCleanupTests(unittest.TestCase):
    """A grader crash must not leave the run's sessions in the real Claude config or its throwaway config folder."""

    def setup_run(self, tmp):
        work = Path(tmp) / "work"
        runner = ba.Runner.__new__(ba.Runner)   # skip __init__: it reads the real Obsidian vault
        runner.args = SimpleNamespace(retries=0, provider="anthropic", abort_after=4, keep_transcripts=False,
                                      keep_workdirs=False, timeout=5, budget=None, effort=None)
        runner.claude, runner.work, runner.out = "claude", work, Path(tmp) / "out"
        runner.lock, runner.abort, runner.consecutive_infra, runner.digests = threading.Lock(), threading.Event(), 0, set()
        digest = hashlib.sha1(b"run-1").hexdigest()[:10]
        workdir, config_dir = work / "r" / digest, work / "cfg" / digest
        claude_home = Path(tmp) / "claude-home"
        with mock.patch.dict("os.environ", {"CLAUDE_CONFIG_DIR": str(claude_home)}):
            sessions = ba.claude_session_dir(workdir)
        sessions.mkdir(parents=True)
        (sessions / "s.jsonl").write_text("prompt", encoding="utf-8")
        return runner, workdir, config_dir, sessions, claude_home

    def execute(self, runner, tmp, claude_home, grader):
        def prepare_workdir(arm, template, seed, workdir):
            workdir.mkdir(parents=True)
            return "seed"

        arm = ba.Arm("after", Path(tmp))
        prep = SimpleNamespace(template=Path(tmp), shim=Path(tmp), instructions=None, home=Path(tmp))
        task = {"id": "t", "grader": {"cmd": grader}}
        parsed = {"has_result": True, "is_error": False, "subtype": "success", "tokens": {"output": 5}}
        with mock.patch.dict("os.environ", {"CLAUDE_CONFIG_DIR": str(claude_home)}), \
                mock.patch.object(ba, "prepare_workdir", prepare_workdir), \
                mock.patch.object(ba, "invoke", return_value=(False, False, 1.0)), \
                mock.patch.object(ba, "parse_stream", return_value=parsed), \
                mock.patch.object(ba, "diff_stats", return_value={}):
            return runner._execute(arm, prep, Path(tmp) / "task", task, "m", "prompt", "run-1")

    def test_a_missing_grader_still_removes_the_sessions_and_the_config_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner, workdir, config_dir, sessions, claude_home = self.setup_run(tmp)
            with self.assertRaises(FileNotFoundError):
                self.execute(runner, tmp, claude_home, ["no-such-grader-command-for-the-test"])
            self.assertFalse(sessions.exists(), "the run's sessions were left in the Claude config")
            self.assertFalse(config_dir.exists())
            self.assertTrue(workdir.exists(), "a crashed run keeps its workdir for inspection")

    def test_a_finished_run_removes_all_of_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner, workdir, config_dir, sessions, claude_home = self.setup_run(tmp)
            with mock.patch.object(ba, "grade", return_value={"passed": True}):
                row = self.execute(runner, tmp, claude_home, ["unused"])
            self.assertTrue(row["passed"])
            self.assertFalse(sessions.exists() or config_dir.exists() or workdir.exists())


class InvokeCleanupTests(unittest.TestCase):
    def proc(self, running):
        proc = mock.MagicMock()
        proc.pid = 4242
        proc.poll.return_value = None if running else 0
        proc.stdout.readline.return_value = b""
        return proc

    def test_an_error_while_reading_the_stream_does_not_leave_the_agent_running(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_folder = Path(tmp) / "nope" / "t.jsonl"   # opening it fails after the process has started
            with mock.patch.object(ba.subprocess, "Popen", return_value=self.proc(running=True)), \
                    mock.patch.object(ba, "kill_tree") as kill, self.assertRaises(FileNotFoundError):
                ba.invoke(["claude"], "prompt", Path("."), {}, missing_folder, 5)
            kill.assert_called_with(4242)

    def test_a_process_that_already_ended_is_not_killed_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.proc(running=False)
            with mock.patch.object(ba.subprocess, "Popen", return_value=proc), mock.patch.object(ba, "kill_tree") as kill:
                ba.invoke(["claude"], "prompt", Path("."), {}, Path(tmp) / "t.jsonl", 5)
            kill.assert_not_called()


class RulesScoreTests(unittest.TestCase):
    def test_the_false_alarm_rate_is_also_given_with_nothing_dropped(self):
        flagged_non_rule = "From now on we use tabs."   # the writer meant it as a non-rule; the labeller disagrees
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "pos-a.json").write_text(json.dumps(["From now on always use tabs. Fix the header."]), encoding="utf-8")
            (d / "pos-b.json").write_text("[]", encoding="utf-8")
            (d / "neg-a.json").write_text(json.dumps(
                ["Why does parse_line return None?", "Thanks!", flagged_non_rule]), encoding="utf-8")
            (d / "neg-b.json").write_text(json.dumps(["Add a retry wrapper to the client."]), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                prepare(d)
            key = json.loads((d / "key.json").read_text(encoding="utf-8"))
            labels = {str(n): (1 if r["text"] == flagged_non_rule else r["label"]) for n, r in enumerate(key)}
            (d / "labels-0.json").write_text(json.dumps(labels), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                result = score(d)
        self.assertEqual((result["non_rules"], result["flagged"]), (3, 0))   # the headline: agreed messages only
        self.assertEqual((result["all_non_rules"], result["all_flagged"]), (4, 1))
        self.assertEqual((result["dropped_non_rules"], result["dropped_flagged"]), (1, 1))
        self.assertEqual((result["all_rules"], result["all_caught"]), (1, 1))
        self.assertIn("wrongly flagged: 1/4", out.getvalue())


class MakeChartsPartialInputTests(unittest.TestCase):
    PAGE = "<!-- results:start -->\nold table\n<!-- results:end -->\n"

    def run_main(self, tmp, results_files, *extra):
        results = Path(tmp) / "results"
        results.mkdir()
        for name in results_files:
            (results / name).write_text("{}", encoding="utf-8")
        page = Path(tmp) / "results.md"
        page.write_text(self.PAGE, encoding="utf-8")
        argv = ["make_charts", "--results", str(results), "--out", str(Path(tmp) / "out"), "--readme", str(page), *extra]
        err = io.StringIO()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = charts.main()
        return code, err.getvalue(), page.read_text(encoding="utf-8")

    def test_a_missing_result_file_stops_the_page_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, err, page = self.run_main(tmp, [n for n in charts.INPUTS if n != "memory.json"])
        self.assertEqual(code, 1)
        self.assertEqual(err.count("missing result file"), 1)
        self.assertIn("memory.json", err)
        self.assertEqual(page, self.PAGE)

    def test_allow_partial_warns_and_goes_on(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, err, page = self.run_main(tmp, [], "--allow-partial")
        self.assertEqual(code, 0)
        self.assertEqual(err.count("missing result file"), len(charts.INPUTS))
        self.assertNotIn("old table", page)

    def test_all_inputs_present_changes_nothing_about_the_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, err, _ = self.run_main(tmp, charts.INPUTS)
        self.assertEqual((code, err), (0, ""))


class ResultsDocsTests(unittest.TestCase):
    def test_the_memory_task_count_in_the_results_notes_is_the_number_of_saved_tasks(self):
        raw = sorted((ROOT / "benchmarks" / "results" / "raw").glob("memory-*.jsonl"))
        if not raw:
            self.skipTest("no memory rows saved")
        tasks = {json.loads(line)["task"] for path in raw for line in path.read_text(encoding="utf-8").splitlines()
                 if line.strip() and json.loads(line).get("kind") == "task"}
        suites = sum(len(list((ROOT / "benchmarks" / "tasks" / name).glob("*/task.json")))
                     for name in ("memory", "memory-rules"))
        self.assertEqual(len(tasks), suites)
        notes = (ROOT / "benchmarks" / "results" / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"`memory-*` ({len(tasks)} two-session tasks", notes)


class LocalisationCheckerSelfTests(unittest.TestCase):
    """A self-test of the checker. Passing reference fixtures is not a model evaluation (see the evals README)."""

    @classmethod
    def setUpClass(cls):
        cls.cases = cle.load_cases()

    def flagged(self, case_id, output):
        report = cle.check({case_id: self.cases[case_id]}, [{"id": case_id, "output": output}])
        return bool(report["failures"])

    def test_every_reference_output_passes_its_own_checks(self):
        report = cle.check(self.cases, [{"id": i, "output": c["reference_output"]} for i, c in self.cases.items()])
        self.assertEqual(report["failures"], [])
        self.assertEqual(report["missing"], [])
        self.assertTrue(report["literal_checks_complete_and_clean"])

    @staticmethod
    def alternatives(pattern):
        """The words of a plain \\b(a|b|c)\\b pattern, with `x+` written as `x`; None for any other shape."""
        match = re.fullmatch(r"\\b\(?([\w+| ]+)\)?\\b", pattern)
        return [re.sub(r"(\w)\+", r"\1", alt) for alt in match.group(1).split("|")] if match else None

    def test_every_listed_forbidden_word_is_flagged_when_added_to_the_reference(self):
        skipped = set()
        for case_id, case in self.cases.items():
            for pattern in case["checks"]["forbidden_regex"]:
                words = self.alternatives(pattern)
                if words is None:
                    skipped.add((case_id, pattern))
                    continue
                for word in words:
                    with self.subTest(case=case_id, word=word):
                        self.assertTrue(self.flagged(case_id, f"{case['reference_output']} {word}"))
        self.assertEqual(skipped, {("locale-01", "\\bRM\\s*\\d")}, "a new non-alternation pattern needs its own test")

    def test_particle_boundaries(self):
        rows = [
            ("over-01", "Ini salah.", False),            # "lah" inside a word is not a particle
            ("over-01", "Refund dah lulus lah.", True),
            ("over-01", "Okay lahh.", True),             # repeated letters
            ("over-01", "Okay lorr.", True),
            ("style-11", "Refund dah lulus lah.", True),
        ]
        for case_id, output, expected in rows:
            with self.subTest(case=case_id, output=output):
                self.assertEqual(self.flagged(case_id, output), expected)

    def test_skill_use_count_counts_completed_after_runs_that_opened_a_skill(self):
        rows = [
            {"kind": "task", "arm": "after", "skills_loaded": ["a"]},
            {"kind": "task", "arm": "after-hint", "skills_invoked": ["b"]},
            {"kind": "task", "arm": "after"},
            {"kind": "task", "arm": "baseline", "skills_loaded": ["x"]},
            {"kind": "task", "arm": "after", "infrastructure_failure": True, "skills_loaded": ["z"]},
            {"kind": "overhead", "arm": "after", "skills_loaded": ["y"]},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp)
            (raw / "coding-m.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n\n", encoding="utf-8")
            (raw / "routing.jsonl").write_text(json.dumps(rows[0]) + "\n", encoding="utf-8")   # skipped by name
            with mock.patch.object(scu, "RAW", raw):
                self.assertEqual(scu.count(), (3, 2, {"a", "b"}))


class HeldoutProvenanceTests(unittest.TestCase):
    def test_a_bad_baseline_arm_is_refused_before_any_work(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            heldout.main(["--arm", f"after={ROOT}", "--baseline-arm", "nope"])

    def test_the_report_names_the_arm_the_keyword_baseline_used_and_no_folder_paths(self):
        prompts = json.loads((ROOT / "benchmarks" / "routing-heldout" / "prompts.json").read_text(encoding="utf-8"))[:2]
        with tempfile.TemporaryDirectory() as tmp:
            prompts_file, out = Path(tmp) / "prompts.json", Path(tmp) / "out.json"
            prompts_file.write_text(json.dumps(prompts), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()) as shown:
                heldout.main(["--arm", f"after={ROOT}", "--prompts", str(prompts_file), "--out", str(out)])
            report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["baseline"]["arm"], "after")
        self.assertRegex(report["baseline"]["catalog_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn(report["baseline"]["catalog_sha256"][:12], shown.getvalue())
        self.assertEqual(set(report["arms"]), {"after"})
        self.assertEqual(set(report["arms"]["after"]), {"git_revision", "working_tree_modified"})
        provenance = json.dumps([report["arms"], report["baseline"]])
        self.assertNotIn(str(ROOT), provenance)
        self.assertNotIn(ROOT.as_posix(), provenance)


class HarnessArmTests(unittest.TestCase):
    """`+harness` builds the setup a 2.2 install ships: the Node gates as project hooks plus the deny rules."""

    def test_flag_is_parsed(self):
        arm = ba.parse_arm(f"ship={ROOT}@lean+hint+harness+brief")
        self.assertTrue(arm.harness and arm.hint and arm.brief)
        self.assertFalse(arm.gate)
        self.assertFalse(ba.parse_arm(f"old={ROOT}@lean+hint+gate+brief").harness)

    def test_gate_and_harness_together_are_refused(self):
        with self.assertRaises(SystemExit):
            ba.parse_arm(f"both={ROOT}@lean+gate+harness")

    def test_template_gets_the_harness_hooks_and_deny_rules(self):
        from bossku.hooks import DENY_RULES, HARNESS_EVENTS, HARNESS_MARKER
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "tpl"
            ba.build_template(ba.parse_arm(f"ship={ROOT}@lean+harness"), dest)
            settings = json.loads((dest / ".claude" / "settings.json").read_text(encoding="utf-8"))
            for event, matcher, script, _timeout in HARNESS_EVENTS:
                ours = [e for e in settings["hooks"][event] if HARNESS_MARKER in json.dumps(e)]
                self.assertEqual(len(ours), 1, event)
                self.assertIn(script, json.dumps(ours[0]))
                if matcher:
                    self.assertEqual(ours[0]["matcher"], matcher)
            self.assertEqual(sorted(settings["permissions"]["deny"]), sorted(DENY_RULES))
            self.assertNotIn("verify-gate", json.dumps(settings))


if __name__ == "__main__":
    unittest.main()
