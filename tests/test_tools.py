import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from bossku import tools
from bossku.cli import main


class ToolRegistryTests(unittest.TestCase):
    def test_every_tool_names_a_skill_that_exists(self):
        skills = {p.name for p in (Path(__file__).resolve().parents[1] / "skills").iterdir() if p.is_dir()}
        for tool in tools.TOOLS:
            for skill in tool.skills:
                self.assertIn(skill, skills, f"{tool.id} points at a missing skill")

    def test_ids_are_unique_and_each_tool_says_how_to_get_it(self):
        self.assertEqual(len({t.id for t in tools.TOOLS}), len(tools.TOOLS))
        for tool in tools.TOOLS:
            self.assertTrue(tools.plan(tool) or tool.manual, f"{tool.id} has neither a plan nor manual instructions")

    def test_pip_and_npm_plans_are_fixed_argument_lists_never_shell_strings(self):
        for tool in tools.TOOLS:
            for command in tools.plan(tool):
                self.assertIsInstance(command, list)
                self.assertNotIn("|", " ".join(command))
                self.assertNotIn("curl", command)

    def test_manual_tools_are_never_run(self):
        calls = []
        result = tools.run_install(tools.BY_ID["moli"], runner=lambda *a, **k: calls.append(a))
        self.assertFalse(result["ok"])
        self.assertEqual(calls, [])
        self.assertIn("by hand", result["message"])


class DetectionTests(unittest.TestCase):
    def test_a_command_on_the_path_counts_as_installed(self):
        with mock.patch("bossku.tools._which", side_effect=lambda c: "/bin/graft" if c == "graft" else None):
            self.assertTrue(tools.installed(tools.BY_ID["graft"]))
            self.assertFalse(tools.installed(tools.BY_ID["moli"]))

    def test_a_program_in_the_current_folder_is_not_found(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as elsewhere:
            name = "planted-tool" + (".cmd" if os.name == "nt" else "")
            for folder in (tmp, elsewhere):
                path = Path(folder) / name
                path.write_text("echo hi", encoding="utf-8")
                path.chmod(0o755)
            old = os.getcwd()
            os.chdir(tmp)
            try:
                with mock.patch.dict(os.environ, {"PATH": os.pathsep.join([".", tmp, elsewhere])}):
                    self.assertEqual(Path(tools._which("planted-tool")).parent, Path(elsewhere))
                with mock.patch.dict(os.environ, {"PATH": os.pathsep.join([".", tmp])}):
                    self.assertIsNone(tools._which("planted-tool"))
            finally:
                os.chdir(old)

    def test_archify_is_found_under_the_given_home(self):
        with tempfile.TemporaryDirectory() as home, mock.patch("bossku.tools._which", return_value=None):
            self.assertFalse(tools.installed(tools.BY_ID["archify"], home=Path(home)))
            (Path(home) / ".claude" / "skills" / "archify").mkdir(parents=True)
            self.assertTrue(tools.installed(tools.BY_ID["archify"], home=Path(home)))

    def test_e2e_is_per_project_and_read_from_package_json(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch("bossku.tools._which", return_value=None):
            project = Path(tmp)
            self.assertFalse(tools.installed(tools.BY_ID["e2e"], project))
            (project / "package.json").write_text(json.dumps({"devDependencies": {"e2e": "^1.0.0"}}), encoding="utf-8")
            self.assertTrue(tools.installed(tools.BY_ID["e2e"], project))


class InstallTests(unittest.TestCase):
    def test_a_pip_install_runs_the_planned_command_and_reports_success(self):
        seen = []
        runner = lambda argv, **kw: seen.append(argv) or SimpleNamespace(returncode=0)
        result = tools.run_install(tools.BY_ID["markitdown"], runner=runner)
        self.assertTrue(result["ok"])
        self.assertEqual(seen[0][1:5], ["-P", "-m", "pip", "install"])     # -P: a pip.py in the current folder is not run
        self.assertIn("markitdown[all]>=0.1.0", seen[0])

    def test_a_failing_step_stops_the_plan(self):
        seen = []
        runner = lambda argv, **kw: seen.append(argv) or SimpleNamespace(returncode=3)
        with tempfile.TemporaryDirectory() as tmp, mock.patch("bossku.tools.sys.stdin.isatty", return_value=True):
            (Path(tmp) / "package.json").write_text("{}", encoding="utf-8")
            result = tools.run_install(tools.BY_ID["e2e"], project=Path(tmp), runner=runner, node_problem=lambda: "")
        self.assertFalse(result["ok"])
        self.assertEqual(len(seen), 1)    # `npx e2e init` was not attempted after the failed install
        self.assertEqual(seen[0][-1], "ai@7")

    def test_e2e_changes_nothing_when_it_cannot_finish(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "package.json").write_text("{}", encoding="utf-8")
            fail = lambda *a, **k: self.fail("ran")
            with mock.patch("bossku.tools.sys.stdin.isatty", return_value=False):          # no terminal for `npx e2e init`
                result = tools.run_install(tools.BY_ID["e2e"], project=project, runner=fail, node_problem=lambda: "")
            self.assertFalse(result["ok"])
            self.assertIn("terminal", result["message"])
            with mock.patch("bossku.tools.sys.stdin.isatty", return_value=True):
                result = tools.run_install(tools.BY_ID["e2e"], project=project, runner=fail,
                                           node_problem=lambda: "Node 20.1.0 is too old")
            self.assertFalse(result["ok"])
            self.assertIn("nothing was changed", result["message"])
            self.assertEqual((project / "package.json").read_text(encoding="utf-8"), "{}")

    def test_e2e_already_in_the_project_is_not_installed_or_initialised_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text(json.dumps({"devDependencies": {"e2e": "1"}}), encoding="utf-8")
            result = tools.run_install(tools.BY_ID["e2e"], project=Path(tmp), runner=lambda *a, **k: self.fail("ran"))
        self.assertTrue(result["ok"])
        self.assertIn("already", result["message"])

    def test_node_versions(self):
        for version, ok in (("v24.8.0", True), ("v24.7.9", False), ("v22.22.3", True), ("v22.22.2", False), ("v26.0.0", True), ("v20.0.0", False)):
            fake = subprocess.CompletedProcess([], 0, stdout=version + "\n")
            with mock.patch("bossku.tools._which", return_value="node"), mock.patch("bossku.tools.subprocess.run", return_value=fake):
                self.assertEqual(tools._node_problem() == "", ok, version)

    def test_a_timeout_stops_the_whole_process_tree(self):
        process = mock.MagicMock(pid=4242)
        process.wait.side_effect = [subprocess.TimeoutExpired("npm", 1), 0]
        with mock.patch("bossku.tools.subprocess.Popen", return_value=process), \
                mock.patch("bossku.tools.subprocess.run") as run, mock.patch("bossku.tools.os.name", "nt"):
            with self.assertRaises(subprocess.TimeoutExpired):
                tools._run(["npm", "install"], timeout=1)
        self.assertEqual(run.call_args.args[0], ["taskkill", "/T", "/F", "/PID", "4242"])

    def test_a_project_tool_needs_a_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = tools.run_install(tools.BY_ID["e2e"], project=Path(tmp), runner=lambda *a, **k: self.fail("ran"))
        self.assertFalse(result["ok"])
        self.assertIn("package.json", result["message"])


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_list_shows_every_tool_and_promises_not_to_install(self):
        code, out, _ = self.run_cli("tools", "list")
        self.assertEqual(code, 0)
        for tool in tools.TOOLS:
            self.assertIn(tool.id, out)
        self.assertIn("Nothing is installed", out)

    def test_list_can_be_machine_readable(self):
        code, out, _ = self.run_cli("tools", "list", "--json")
        rows = json.loads(out)
        self.assertEqual({r["id"] for r in rows}, {t.id for t in tools.TOOLS})

    def test_install_without_yes_only_prints_the_plan(self):
        with mock.patch("bossku.tools.run_install", side_effect=AssertionError("must not run")) as run:
            code, out, _ = self.run_cli("tools", "install", "headroom")
        run.assert_not_called()
        self.assertEqual(code, 0)
        self.assertIn("pip install", out)
        self.assertIn("Nothing was run", out)
        self.assertIn("HEADROOM_BEACON", out)     # the telemetry notice is shown before anything is installed

    def test_install_of_a_manual_tool_prints_where_to_get_it(self):
        code, out, _ = self.run_cli("tools", "install", "moli", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("github.com/lexmount/moli", out)

    def test_unknown_tool_is_an_error(self):
        code, _, err = self.run_cli("tools", "install", "nope")
        self.assertEqual(code, 2)
        self.assertIn("unknown tool", err)


if __name__ == "__main__":
    unittest.main()
