"""Harness layer: agent contracts, plugin hooks, profiles, install modes, and the gates."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from bossku import __version__
from bossku.doctor import gather_doctor_issues
from bossku.hooks import (
    DENY_RULES,
    HARNESS_EVENTS,
    HARNESS_MARKER,
    harness_status,
    install_hooks,
    plugin_double_load,
    uninstall_hooks,
)
from bossku.init_project import PROJECT_BLOCK, init_project
from bossku.install import AGENT_FILES, AGENT_SIGNATURE, install_user, uninstall_user, update_user
from bossku.memory import load_user_config
from bossku.skills import _profile_skills, list_skill_ids, load_pack_skill_ids
from bossku.validate import package_version, validate_agents, validate_hooks

ROOT = Path(__file__).resolve().parents[1]


class AgentContractTests(unittest.TestCase):
    def test_every_contract_has_valid_claude_code_frontmatter(self):
        errors = validate_agents(ROOT)
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_verifying_agents_can_run_commands(self):
        for name in ("executor.md", "auditor.md", "final-reviewer.md", "designer.md"):
            text = (ROOT / "agents" / name).read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^tools: .*\bBash\b", msg=name)

    def test_no_contract_references_phantom_agents(self):
        phantoms = ("code-simplifier", "build-fixer", "database-reviewer", "security-reviewer", "loop-operator", "TaskCheckoutService")
        for path in (ROOT / "agents").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for name in phantoms:
                self.assertNotIn(name, text, msg=f"{path.name} still references {name}")


class HooksManifestTests(unittest.TestCase):
    def test_hooks_json_and_scripts_exist(self):
        errors = validate_hooks(ROOT)
        self.assertEqual(errors, [], msg="\n".join(errors))

    def test_plugin_manifest_wires_hooks_and_designer(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["hooks"], "./hooks/hooks.json")
        self.assertIn("./agents/designer.md", manifest["agents"])

    @unittest.skipUnless(shutil.which("node"), "node not on PATH")
    def test_node_hook_suite_passes(self):
        result = subprocess.run(
            ["node", "--test", str(ROOT / "tests" / "hooks.test.mjs")],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=300,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout[-4000:] + result.stderr[-4000:])


class VersionTests(unittest.TestCase):
    def test_package_dunder_version_matches_pyproject(self):
        self.assertEqual(__version__, package_version(ROOT))


class ProfileTests(unittest.TestCase):
    def test_engineering_profile_drops_only_the_marketing_pack(self):
        full = set(list_skill_ids(ROOT))
        marketing = set(load_pack_skill_ids("marketingskills", ROOT))
        engineering = set(_profile_skills("engineering", ROOT))
        self.assertEqual(engineering, full - marketing)
        self.assertNotIn("copywriting", engineering)
        for keep in ("bosskuai-taste", "brainstorming", "hallmark", "mysql-patterns", "i-have-adhd"):
            self.assertIn(keep, engineering)


class InstallModeTests(unittest.TestCase):
    def test_no_claude_removes_managed_copies_and_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first = install_user(root=ROOT, home=home, profile="core")
            self.assertTrue((home / ".claude" / "skills" / "cofounder").is_dir())
            self.assertIn("executor.md", first["agents_installed"])
            agent = home / ".claude" / "agents" / "executor.md"
            self.assertIn(AGENT_SIGNATURE, agent.read_text(encoding="utf-8"))

            second = install_user(root=ROOT, home=home, profile="core", claude=False)
            self.assertFalse((home / ".claude" / "skills" / "cofounder").exists())
            self.assertIn("cofounder", second["claude_skills_removed"])
            self.assertTrue((home / ".agents" / "skills" / "cofounder").is_dir(), "other hosts keep their copy")
            self.assertFalse(load_user_config(home)["claude_skills"])

            third = update_user(root=ROOT, home=home)
            self.assertEqual(third["claude_count"], 0, "update honours the persisted --no-claude")
            self.assertFalse((home / ".claude" / "skills" / "cofounder").exists())

            issues = gather_doctor_issues(ROOT, home)
            self.assertFalse(any("~/.claude/skills" in i for i in issues), issues)

            removed = uninstall_user(root=ROOT, home=home)
            self.assertEqual(sorted(removed["removed_agents"]), sorted(AGENT_FILES))
            self.assertFalse(agent.exists())

    def test_user_owned_agent_file_is_never_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            own = home / ".claude" / "agents" / "auditor.md"
            own.parent.mkdir(parents=True)
            own.write_text("---\nname: auditor\ndescription: mine\n---\nmy own auditor\n", encoding="utf-8")
            install_user(root=ROOT, home=home, profile="core", agents=False)
            uninstall_user(root=ROOT, home=home)
            self.assertTrue(own.exists())
            self.assertIn("my own auditor", own.read_text(encoding="utf-8"))


class HarnessHooksTests(unittest.TestCase):
    def _seed(self, home: Path) -> Path:
        claude = home / ".claude"
        claude.mkdir(parents=True)
        settings = claude / "settings.json"
        settings.write_text(
            json.dumps(
                {
                    "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo unrelated"}]}]},
                    "permissions": {"deny": ["Bash(rm -rf /:*)"]},
                }
            ),
            encoding="utf-8",
        )
        return settings

    def test_install_adds_gates_and_deny_rules_additively(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            settings = self._seed(home)
            result = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(result["claude_harness"]["status"], "installed")
            data = json.loads(settings.read_text(encoding="utf-8"))
            for event, matcher, script, _timeout in HARNESS_EVENTS:
                entries = data["hooks"][event]
                ours = [e for e in entries if HARNESS_MARKER in json.dumps(e)]
                self.assertEqual(len(ours), 1, event)
                self.assertIn(script, json.dumps(ours[0]))
                if matcher:
                    self.assertEqual(ours[0]["matcher"], matcher)
            self.assertIn("echo unrelated", json.dumps(data["hooks"]["Stop"]))
            self.assertIn("Bash(rm -rf /:*)", data["permissions"]["deny"])
            for rule in DENY_RULES:
                self.assertIn(rule, data["permissions"]["deny"])
            status = harness_status(home)
            self.assertTrue(status["hooks"])
            self.assertTrue(status["deny_rules"])

            again = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(again["claude_harness"]["status"], "already_installed")

            removed = uninstall_hooks(home=home, tools=("claude_code",))
            self.assertEqual(removed["claude_harness"]["status"], "removed")
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertNotIn(HARNESS_MARKER, json.dumps(data))
            self.assertIn("echo unrelated", json.dumps(data["hooks"]["Stop"]))
            self.assertEqual(data["permissions"]["deny"], ["Bash(rm -rf /:*)"])
            self.assertFalse(harness_status(home)["hooks"])

    def test_no_harness_flag_installs_sync_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._seed(home)
            result = install_hooks(home=home, tools=("claude_code",), harness=False, root=ROOT)
            self.assertNotIn("claude_harness", result)
            self.assertFalse(harness_status(home)["hooks"])


class DoubleLoadTests(unittest.TestCase):
    def test_plugin_and_local_install_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            claude = home / ".claude"
            (claude / "plugins").mkdir(parents=True)
            cache = claude / "plugins" / "cache" / "bossku-ai" / "2.1.0"
            (cache / "hooks").mkdir(parents=True)
            (cache / "hooks" / "hooks.json").write_text("{}", encoding="utf-8")
            (claude / "settings.json").write_text(
                json.dumps({"enabledPlugins": {"bossku-ai@bosskuai-marketplace": True}}), encoding="utf-8"
            )
            (claude / "plugins" / "installed_plugins.json").write_text(
                json.dumps({"plugins": {"bossku-ai@bosskuai-marketplace": [{"installPath": str(cache), "version": "2.1.0"}]}}),
                encoding="utf-8",
            )
            dbl = plugin_double_load(home)
            self.assertTrue(dbl["plugin_enabled"])
            self.assertTrue(dbl["plugin_has_hooks"])
            self.assertEqual(dbl["version"], "2.1.0")

            install_user(root=ROOT, home=home, profile="core")
            install_hooks(home=home, tools=("claude_code",), root=ROOT)
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("loads twice" in i for i in issues), issues)
            self.assertTrue(any("fire twice" in i for i in issues), issues)

            install_user(root=ROOT, home=home, profile="core", claude=False)
            issues = gather_doctor_issues(ROOT, home)
            self.assertFalse(any("loads twice" in i for i in issues), issues)


class DesignStubTests(unittest.TestCase):
    # A temp home on every init: without one init_project reads the real ~/.bosskuai/config.json and, with
    # memory_storage=obsidian, would write a claim file and memory templates into the real vault.
    def test_init_scaffolds_design_stub_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            result = init_project(project, root=ROOT, home=Path(tmp))
            stub = project / ".bossku" / "DESIGN.md"
            self.assertEqual(result["design_md"], str(stub))
            text = stub.read_text(encoding="utf-8")
            self.assertIn("## 9. Agent Prompt Guide", text)
            stub.write_text("# filled in by the designer\n", encoding="utf-8")
            again = init_project(project, root=ROOT, home=Path(tmp))
            self.assertIsNone(again["design_md"])
            self.assertEqual(stub.read_text(encoding="utf-8"), "# filled in by the designer\n")

    def test_existing_root_design_md_is_respected(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            project.mkdir()
            (project / "DESIGN.md").write_text("# real one\n", encoding="utf-8")
            result = init_project(project, root=ROOT, home=Path(tmp))
            self.assertIsNone(result["design_md"])
            self.assertFalse((project / ".bossku" / "DESIGN.md").exists())
            meta = json.loads((project / ".bossku" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["bossku_version"], __version__)

    def test_existing_design_folder_file_is_respected(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            (project / "design").mkdir(parents=True)
            (project / "design" / "DESIGN.md").write_text("# real design system\n", encoding="utf-8")
            result = init_project(project, root=ROOT, home=Path(tmp))
            self.assertIsNone(result["design_md"])
            self.assertFalse((project / ".bossku" / "DESIGN.md").exists())

    def test_the_project_block_does_not_forbid_the_design_file(self):
        # The block says "never open or edit .bossku/ by hand" while the designer contract writes .bossku/DESIGN.md.
        self.assertNotRegex(PROJECT_BLOCK, r"never open or edit \.bossku/ ")
        self.assertIn(".bossku/memory", PROJECT_BLOCK)
        self.assertIn(".bossku/DESIGN.md and .bossku/shots/ are yours to read and write", PROJECT_BLOCK)

    @unittest.skipUnless(shutil.which("node"), "node not on PATH")
    def test_session_start_never_names_the_stub_over_a_real_design_file(self):
        def start(cwd: Path) -> str:
            run = subprocess.run(
                ["node", str(ROOT / "hooks" / "session-start.mjs")],
                input=json.dumps({"cwd": str(cwd)}), capture_output=True, text=True, encoding="utf-8", timeout=60,
            )
            return run.stdout

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            only_stub = home / "stub"
            init_project(only_stub, root=ROOT, home=home)
            out = start(only_stub)
            self.assertNotIn("Design source of truth", out, "an unfilled stub is not a source of truth")
            self.assertIn(".bossku/DESIGN.md is still an unfilled stub", out)

            # a root DESIGN.md written after init: the stub must not keep winning
            late = home / "late"
            init_project(late, root=ROOT, home=home)
            (late / "DESIGN.md").write_text("# real design system\n", encoding="utf-8")
            self.assertIn("Design source of truth: DESIGN.md.", start(late))

            # design/DESIGN.md written after init
            folder = home / "folder"
            init_project(folder, root=ROOT, home=home)
            (folder / "design").mkdir()
            (folder / "design" / "DESIGN.md").write_text("# real design system\n", encoding="utf-8")
            self.assertIn("Design source of truth: design/DESIGN.md.", start(folder))

            # once the designer fills the .bossku copy in, it is the source of truth again
            filled = home / "filled"
            init_project(filled, root=ROOT, home=home)
            (filled / ".bossku" / "DESIGN.md").write_text("# DESIGN.md\n\nStatus: done\n", encoding="utf-8")
            self.assertIn("Design source of truth: .bossku/DESIGN.md.", start(filled))


if __name__ == "__main__":
    unittest.main()
