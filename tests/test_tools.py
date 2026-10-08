import contextlib
import io
import json
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
        with mock.patch("bossku.tools.shutil.which", side_effect=lambda c: "/bin/graft" if c == "graft" else None):
            self.assertTrue(tools.installed(tools.BY_ID["graft"]))
            self.assertFalse(tools.installed(tools.BY_ID["moli"]))

    def test_e2e_is_per_project_and_read_from_package_json(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch("bossku.tools.shutil.which", return_value=None):
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
        self.assertEqual(seen[0][1:4], ["-m", "pip", "install"])
        self.assertIn("markitdown[all]>=0.1.0", seen[0])

    def test_a_failing_step_stops_the_plan(self):
        seen = []
        runner = lambda argv, **kw: seen.append(argv) or SimpleNamespace(returncode=3)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text("{}", encoding="utf-8")
            result = tools.run_install(tools.BY_ID["e2e"], project=Path(tmp), runner=runner)
        self.assertFalse(result["ok"])
        self.assertEqual(len(seen), 1)    # `npx e2e init` was not attempted after the failed install

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
        with mock.patch("bossku.tools.subprocess.run", side_effect=AssertionError("must not run")):
            code, out, _ = self.run_cli("tools", "install", "headroom")
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
