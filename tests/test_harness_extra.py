"""The harness Python side beyond tests/test_harness.py: product rules, edge cases and the fixes that landed with it.

Every test uses a temporary home; none touches the real one, the real settings or the vault.
"""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku.doctor import format_doctor_success, gather_doctor_issues
from bossku.hooks import (
    DENY_RULES,
    HARNESS_EVENTS,
    HARNESS_MARKER,
    ensure_verify_gate_hook,
    harness_status,
    install_hooks,
    plugin_double_load,
    uninstall_hooks,
)
from bossku.init_project import init_project, upsert_managed_block
from bossku.install import AGENT_FILES, install_user, uninstall_user, update_user
from bossku.memory import load_user_config
from bossku.paths import MARKER_END, MARKER_START, user_config_dir
from bossku.skills import _profile_skills
from bossku.validate import validate_agents

ROOT = Path(__file__).resolve().parents[1]
NEEDS_NODE = unittest.skipUnless(shutil.which("node"), "node not on PATH")
REAL_WHICH = shutil.which


def settings_path(home: Path) -> Path:
    return home / ".claude" / "settings.json"


def read_settings(home: Path) -> dict:
    return json.loads(settings_path(home).read_text(encoding="utf-8"))


def write_settings(home: Path, data: dict) -> None:
    settings_path(home).parent.mkdir(parents=True, exist_ok=True)
    settings_path(home).write_text(json.dumps(data), encoding="utf-8")


def stop_commands(home: Path) -> list[str]:
    return [h["command"] for e in read_settings(home)["hooks"]["Stop"] for h in e["hooks"]]


def without_node(name, *args, **kwargs):
    return None if name == "node" else REAL_WHICH(name, *args, **kwargs)


class SourcesOfTruthTests(unittest.TestCase):
    def test_harness_events_match_hooks_json(self):
        declared = []
        for event, groups in json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    script = re.search(r"/hooks/([\w.-]+\.mjs)", hook["command"]).group(1)
                    declared.append((event, group.get("matcher"), script, hook["timeout"]))
        self.assertEqual(sorted(declared, key=str), sorted(HARNESS_EVENTS, key=str))

    def test_deny_rules_are_the_perms_of_the_guard_script(self):
        guard = (ROOT / "hooks" / "guard.mjs").read_text(encoding="utf-8")
        perms = [p for block in re.findall(r"perm:\s*\[([^\]]*)\]", guard) for p in re.findall(r'"([^"]+)"', block)]
        self.assertEqual(sorted(perms), sorted(DENY_RULES))


@NEEDS_NODE
class OneStopGateTests(unittest.TestCase):
    """The user keeps one Stop gate: the Node one. The Python verify-gate never sits beside it."""

    def _home(self, tmp: str) -> Path:
        home = Path(tmp)
        (home / ".claude").mkdir()
        return home

    def test_harness_install_leaves_the_python_verify_gate_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            result = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(result["claude_harness"]["status"], "installed")
            self.assertNotIn("verify-gate", result["claude_code"]["added"])
            commands = stop_commands(home)
            self.assertFalse(any("verify-gate" in c for c in commands), commands)
            self.assertEqual(sum("stop-gate.mjs" in c for c in commands), 1)
            self.assertTrue(any("sync-hook" in c for c in commands), "the memory sync still goes in")

    def test_an_existing_verify_gate_is_removed_and_the_second_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            write_settings(home, {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}})
            install_hooks(home=home, tools=("claude_code",))   # no root: today's behaviour, with the gate
            self.assertTrue(any("verify-gate" in c for c in stop_commands(home)))

            result = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(result["claude_harness"]["status"], "installed")
            self.assertEqual(result["claude_harness"]["removed"], ["verify-gate"])
            commands = stop_commands(home)
            self.assertFalse(any("verify-gate" in c for c in commands), commands)
            self.assertIn("echo mine", commands)

            before = settings_path(home).read_text(encoding="utf-8")
            again = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(again["claude_harness"]["status"], "already_installed")
            self.assertEqual(again["claude_code"]["status"], "already_installed")
            self.assertEqual(settings_path(home).read_text(encoding="utf-8"), before)

    def test_without_the_harness_the_verify_gate_stays(self):
        for label, kwargs in (("harness=False", {"harness": False, "root": ROOT}), ("no root", {})):
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                home = self._home(tmp)
                result = install_hooks(home=home, tools=("claude_code",), **kwargs)
                self.assertNotIn("claude_harness", result)
                self.assertTrue(any("verify-gate" in c for c in stop_commands(home)))
                self.assertNotIn(HARNESS_MARKER, settings_path(home).read_text(encoding="utf-8"))
                self.assertNotIn("permissions", read_settings(home))

    def test_no_node_skips_the_harness_and_keeps_the_verify_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            with mock.patch("bossku.hooks.shutil.which", side_effect=without_node):
                result = install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(result["claude_harness"]["status"], "skipped_no_node")
            self.assertEqual(result["claude_code"]["status"], "installed")
            self.assertTrue(any("verify-gate" in c for c in stop_commands(home)))
            text = settings_path(home).read_text(encoding="utf-8")
            self.assertNotIn(HARNESS_MARKER, text)
            self.assertNotIn("permissions", read_settings(home), "no deny rules without the hooks that explain them")

    def test_a_checkout_without_hooks_is_an_error_and_writes_no_broken_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            empty = Path(tmp) / "checkout"
            empty.mkdir()
            result = install_hooks(home=home, tools=("claude_code",), root=empty)
            self.assertEqual(result["claude_harness"]["status"], "error")
            self.assertIn("hooks/hooks.json", result["claude_harness"]["message"])
            self.assertNotIn(HARNESS_MARKER, settings_path(home).read_text(encoding="utf-8"))
            self.assertTrue(any("verify-gate" in c for c in stop_commands(home)))


@NEEDS_NODE
class NodeGateAlreadyInSettingsTests(unittest.TestCase):
    """The Node gate is already in settings.json (the user's live shape). A call that does not wire the harness
    itself must not put the Python verify-gate beside it."""

    def _live_home(self, tmp: str, extra: dict | None = None) -> Path:
        home = Path(tmp)
        (home / ".claude").mkdir()
        if extra:
            write_settings(home, extra)
        result = install_hooks(home=home, tools=("claude_code",), root=ROOT)
        self.assertEqual(result["claude_harness"]["status"], "installed")
        self.assertEqual(self._gates(home), ["stop-gate.mjs"])
        return home

    def _gates(self, home: Path) -> list[str]:
        return [re.search(r"stop-gate\.mjs|verify-gate", c).group(0)
                for c in stop_commands(home) if re.search(r"stop-gate\.mjs|verify-gate", c)]

    def test_calls_that_do_not_wire_the_harness_keep_exactly_one_stop_gate(self):
        empty_checkout = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, empty_checkout, True)
        cases = (
            ("no root", {}, None),
            ("empty checkout", {"root": empty_checkout}, None),
            ("node missing", {"root": ROOT}, without_node),
        )
        for label, kwargs, which in cases:
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                home = self._live_home(tmp)
                before = settings_path(home).read_text(encoding="utf-8")
                with mock.patch("bossku.hooks.shutil.which", side_effect=which or REAL_WHICH):
                    install_hooks(home=home, tools=("claude_code",), **kwargs)
                self.assertEqual(self._gates(home), ["stop-gate.mjs"])
                self.assertEqual(settings_path(home).read_text(encoding="utf-8"), before, "nothing to change")
                self.assertTrue(harness_status(home)["hooks"])

    def test_a_verify_gate_beside_the_node_gate_is_removed_without_a_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._live_home(tmp)
            ensure_verify_gate_hook(settings_path(home))
            self.assertEqual(sorted(self._gates(home)), ["stop-gate.mjs", "verify-gate"])
            result = install_hooks(home=home, tools=("claude_code",))
            self.assertEqual(result["claude_code"]["removed"], ["verify-gate"])
            self.assertEqual(self._gates(home), ["stop-gate.mjs"])
            self.assertTrue(any("sync-hook" in c for c in stop_commands(home)), "the memory sync stays")
            before = settings_path(home).read_text(encoding="utf-8")
            again = install_hooks(home=home, tools=("claude_code",))
            self.assertNotIn("removed", again["claude_code"])
            self.assertEqual(settings_path(home).read_text(encoding="utf-8"), before)

    def test_harness_false_takes_our_gates_and_deny_rules_out_and_leaves_the_verify_gate(self):
        mine = {"matcher": "Bash", "hooks": [{"type": "command", "command": "echo my-guard"}]}
        with tempfile.TemporaryDirectory() as tmp:
            home = self._live_home(tmp, {"hooks": {"PreToolUse": [mine]}, "permissions": {"deny": ["Bash(rm -rf /:*)"]}})
            result = install_hooks(home=home, tools=("claude_code",), harness=False, root=ROOT)
            self.assertEqual(result["claude_harness"]["status"], "removed")
            data = read_settings(home)
            self.assertNotIn(HARNESS_MARKER, json.dumps(data))
            self.assertEqual(self._gates(home), ["verify-gate"], "the opt-out falls back to the Python gate")
            self.assertEqual(data["hooks"]["PreToolUse"], [mine])
            self.assertEqual(data["permissions"]["deny"], ["Bash(rm -rf /:*)"])
            before = settings_path(home).read_text(encoding="utf-8")
            again = install_hooks(home=home, tools=("claude_code",), harness=False, root=ROOT)
            self.assertNotIn("claude_harness", again)
            self.assertEqual(settings_path(home).read_text(encoding="utf-8"), before)


@NEEDS_NODE
class HarnessSettingsTests(unittest.TestCase):
    def _home(self, tmp: str, settings: dict | None = None) -> Path:
        home = Path(tmp)
        (home / ".claude").mkdir()
        if settings is not None:
            write_settings(home, settings)
        return home

    def test_one_install_makes_one_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp, {"theme": "dark"})
            install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(len(list(settings_path(home).parent.glob("settings.json.bak-*"))), 1)
            self.assertEqual(read_settings(home)["theme"], "dark")

    def test_a_moved_checkout_replaces_the_old_commands_and_adds_no_rule_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "one", Path(tmp) / "two"
            for checkout in (first, second):
                shutil.copytree(ROOT / "hooks", checkout / "hooks")
            home = Path(tmp) / "home"
            (home / ".claude").mkdir(parents=True)
            install_hooks(home=home, tools=("claude_code",), root=first)
            result = install_hooks(home=home, tools=("claude_code",), root=second)
            self.assertEqual(result["claude_harness"]["status"], "installed")
            data = read_settings(home)
            for event, _matcher, script, _timeout in HARNESS_EVENTS:
                ours = [e for e in data["hooks"][event] if HARNESS_MARKER in json.dumps(e)]
                self.assertEqual(len(ours), 1, event)
                self.assertIn(f"{second.resolve().as_posix()}/hooks/{script}", ours[0]["hooks"][0]["command"])
            self.assertEqual(sorted(data["permissions"]["deny"]), sorted(DENY_RULES))

    def test_a_deny_rule_the_user_already_has_is_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp, {"permissions": {"deny": [DENY_RULES[0]], "allow": ["Bash(ls:*)"]}})
            install_hooks(home=home, tools=("claude_code",), root=ROOT)
            permissions = read_settings(home)["permissions"]
            self.assertEqual(permissions["deny"].count(DENY_RULES[0]), 1)
            self.assertEqual(permissions["allow"], ["Bash(ls:*)"])

    def test_uninstall_keeps_the_users_hooks_and_leaves_no_empty_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            mine = {"matcher": "Bash", "hooks": [{"type": "command", "command": "echo my-guard"}]}
            home = self._home(tmp, {"hooks": {"PreToolUse": [mine]}})
            install_hooks(home=home, tools=("claude_code",), root=ROOT)
            self.assertEqual(len(read_settings(home)["hooks"]["PreToolUse"]), 2)
            uninstall_hooks(home=home, tools=("claude_code",))
            data = read_settings(home)
            self.assertEqual(data["hooks"], {"PreToolUse": [mine]})
            self.assertNotIn("permissions", data)

    def test_status_of_a_missing_or_broken_settings_file_is_all_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            off = {"hooks": False, "deny_rules": False, "events": []}
            self.assertEqual(harness_status(home), off)
            settings_path(home).write_text("{ not json", encoding="utf-8")
            self.assertEqual(harness_status(home), off)

    def test_a_partial_install_is_not_reported_as_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home(tmp)
            install_hooks(home=home, tools=("claude_code",), root=ROOT)
            data = read_settings(home)
            del data["hooks"]["Stop"][[i for i, e in enumerate(data["hooks"]["Stop"]) if HARNESS_MARKER in json.dumps(e)][0]]
            write_settings(home, data)
            status = harness_status(home)
            self.assertFalse(status["hooks"])
            self.assertNotIn("Stop", status["events"])


class PluginDetectionTests(unittest.TestCase):
    def _plugin_home(self, tmp: str, key: str, enabled: bool) -> Path:
        home = Path(tmp)
        cache = home / ".claude" / "plugins" / "cache" / "x" / "3.0.0"
        (cache / "hooks").mkdir(parents=True)
        (cache / "hooks" / "hooks.json").write_text("{}", encoding="utf-8")
        write_settings(home, {"enabledPlugins": {key: enabled}})
        (home / ".claude" / "plugins" / "installed_plugins.json").write_text(
            json.dumps({"plugins": {key: [{"installPath": str(cache), "version": "3.0.0"}]}}), encoding="utf-8")
        return home

    def test_the_current_plugin_name_counts_and_a_disabled_plugin_does_not(self):
        key = "bossku-superpower@bossku-superpower-marketplace"
        with tempfile.TemporaryDirectory() as tmp:
            found = plugin_double_load(self._plugin_home(tmp, key, True))
            self.assertEqual((found["plugin_enabled"], found["plugin_has_hooks"], found["version"]), (True, True, "3.0.0"))
            self.assertEqual(found["plugin"], key)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(plugin_double_load(self._plugin_home(tmp, key, False))["plugin_enabled"])

    def test_someone_elses_plugin_and_unreadable_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(plugin_double_load(self._plugin_home(tmp, "other-tool@market", True))["plugin_enabled"])
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            write_settings(home, {"enabledPlugins": {"bossku-ai@m": True}})
            (home / ".claude" / "plugins").mkdir()
            (home / ".claude" / "plugins" / "installed_plugins.json").write_text("[", encoding="utf-8")
            self.assertFalse(plugin_double_load(home)["plugin_enabled"])


@NEEDS_NODE
class DoctorHarnessTests(unittest.TestCase):
    def test_a_harness_hook_whose_script_is_gone_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            self.assertEqual(gather_doctor_issues(ROOT, home), [])
            data = read_settings(home)
            for entry in data["hooks"]["Stop"]:
                for hook in entry["hooks"]:
                    hook["command"] = hook["command"].replace("/hooks/stop-gate.mjs", "/moved/stop-gate.mjs")
            write_settings(home, data)
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("stop-gate.mjs" in i and "no longer exists" in i for i in issues), issues)

    def test_success_output_names_the_harness_and_the_agent_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            lines = format_doctor_success(ROOT, home, version="x")
            self.assertIn("  harness gates: guard, post-edit lint, stop gate, session contract + deny rules", lines)
            self.assertIn(f"  claude_code agents: {len(AGENT_FILES)} of {len(AGENT_FILES)} contracts", lines)
            uninstall_hooks(home=home, tools=("claude_code",))
            self.assertIn("  harness gates: not installed; run `bossku install`", format_doctor_success(ROOT, home, version="x"))

    def test_the_double_load_advice_does_not_strip_the_sync_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core", claude=False)
            key = "bossku-superpower@bossku-superpower-marketplace"
            cache = home / ".claude" / "plugins" / "cache" / "x" / "3.0.0"
            (cache / "hooks").mkdir(parents=True)
            (cache / "hooks" / "hooks.json").write_text("{}", encoding="utf-8")
            data = read_settings(home)
            write_settings(home, {**data, "enabledPlugins": {key: True}})
            (home / ".claude" / "plugins" / "installed_plugins.json").write_text(
                json.dumps({"plugins": {key: [{"installPath": str(cache), "version": "3.0.0"}]}}), encoding="utf-8")
            twice = [i for i in gather_doctor_issues(ROOT, home) if "fire twice" in i]
            self.assertEqual(len(twice), 1, twice)
            self.assertNotIn("hooks uninstall", twice[0], "that command also removes the vault sync hooks")
            self.assertIn(f"/plugin disable {key}", twice[0])

    def test_a_saved_opt_out_is_not_answered_with_run_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core", agents=False, harness=False)
            lines = format_doctor_success(ROOT, home, version="x")
            self.assertIn("  harness gates: off (`bossku install --no-harness`)", lines)
            self.assertIn("  claude_code agents: off (`bossku install --no-agents`)", lines)


class InstallChoicesTests(unittest.TestCase):
    @NEEDS_NODE
    def test_install_wires_the_harness_and_the_choice_survives_update_and_purge(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first = install_user(root=ROOT, home=home, profile="core")
            self.assertEqual(first["hooks"]["claude_harness"]["status"], "installed")
            self.assertTrue(harness_status(home)["hooks"])
            uninstall_user(root=ROOT, home=home, purge=True)
            self.assertFalse(harness_status(home)["hooks"])
            self.assertFalse(harness_status(home)["deny_rules"])

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core", harness=False)
            self.assertFalse(load_user_config(home)["harness"])
            self.assertNotIn("claude_harness", update_user(root=ROOT, home=home)["hooks"])
            self.assertNotIn("claude_harness", install_user(root=ROOT, home=home, profile="core")["hooks"])
            self.assertFalse(harness_status(home)["hooks"])

    def test_a_plain_reinstall_keeps_no_claude_and_no_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core", claude=False, agents=False)
            again = install_user(root=ROOT, home=home, profile="core")
            self.assertEqual(again["claude_count"], 0)
            self.assertEqual(again["agents_installed"], [])
            self.assertFalse((home / ".claude" / "skills" / "cofounder").exists())
            self.assertFalse((home / ".claude" / "agents").exists())
            config = load_user_config(home)
            self.assertEqual((config["claude_skills"], config["agents"]), (False, False))
            back = install_user(root=ROOT, home=home, profile="core", claude=True, agents=True)
            self.assertGreater(back["claude_count"], 0)
            self.assertEqual(sorted(back["agents_installed"]), sorted(AGENT_FILES))

    def test_no_claude_does_not_touch_the_users_own_claude_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            mine = home / ".claude" / "skills" / "my-own-skill"
            mine.mkdir(parents=True)
            (mine / "SKILL.md").write_text("---\nname: my-own-skill\ndescription: mine\n---\n", encoding="utf-8")
            install_user(root=ROOT, home=home, profile="core")
            result = install_user(root=ROOT, home=home, profile="core", claude=False)
            self.assertNotIn("my-own-skill", result["claude_skills_removed"])
            self.assertTrue((mine / "SKILL.md").is_file())

    def test_agent_contracts_never_overwrite_or_remove_a_users_own_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            own = home / ".claude" / "agents" / "auditor.md"
            own.parent.mkdir(parents=True)
            own.write_text("---\nname: auditor\ndescription: mine\n---\nmy own auditor\n", encoding="utf-8")
            result = install_user(root=ROOT, home=home, profile="core")
            self.assertEqual(result["agents_kept"], ["auditor.md"])
            self.assertNotIn("auditor.md", result["agents_installed"])
            self.assertIn("my own auditor", own.read_text(encoding="utf-8"))
            self.assertEqual(len(result["agents_installed"]), len(AGENT_FILES) - 1)
            off = install_user(root=ROOT, home=home, profile="core", agents=False)
            self.assertEqual(sorted(off["agents_removed"]), sorted(set(AGENT_FILES) - {"auditor.md"}))
            self.assertTrue(own.is_file())

    def test_a_retired_reference_copy_is_removed_by_install_and_by_uninstall(self):
        retired = "always-on-model-router.md"
        if (ROOT / "references" / retired).exists():
            self.skipTest("the repo ships the file again, so it is no longer retired")
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            copies = [home / host / "references" / retired for host in (".agents", ".claude")]
            copies.append(user_config_dir(home) / "references" / retired)
            for copy in copies:
                copy.parent.mkdir(parents=True)
                copy.write_text("old router", encoding="utf-8")
            keep = home / ".claude" / "references" / "my-notes.md"
            keep.write_text("mine", encoding="utf-8")
            install_user(root=ROOT, home=home, profile="core")
            self.assertEqual([c.exists() for c in copies], [False, False, False])
            self.assertTrue(keep.is_file())

            copies[1].write_text("old router", encoding="utf-8")
            uninstall_user(root=ROOT, home=home)
            self.assertFalse(copies[1].exists())
            self.assertTrue(keep.is_file(), "a file that is not ours stays")


class ProfileTests(unittest.TestCase):
    def test_an_unknown_profile_is_refused(self):
        with self.assertRaises(ValueError):
            _profile_skills("everything", ROOT)

    def test_engineering_install_has_no_marketing_pack_and_never_x402(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="engineering", claude=False, agents=False)
            installed = {p.name for p in (home / ".agents" / "skills").iterdir() if p.is_dir()}
            self.assertIn("hallmark", installed)
            self.assertNotIn("copywriting", installed)
            self.assertNotIn("x402", installed, "x402 handles wallet keys: no profile installs it")


class InitProjectTests(unittest.TestCase):
    def test_a_start_marker_without_an_end_marker_is_refused_and_nothing_is_written(self):
        broken = "# Mine\n" + MARKER_START + "\nhalf a block\n\nmy notes\n"
        with self.assertRaises(ValueError) as caught:
            upsert_managed_block(broken, "rules")
        self.assertIn("end marker", str(caught.exception))
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            project.mkdir()
            (project / "AGENTS.md").write_bytes(broken.encode("utf-8"))
            with self.assertRaises(ValueError):
                init_project(project, root=ROOT, home=Path(tmp) / "home")
            self.assertEqual((project / "AGENTS.md").read_bytes(), broken.encode("utf-8"))

    def test_a_stray_end_marker_before_the_block_does_not_duplicate_or_swallow_text(self):
        existing = f"intro\n{MARKER_END}\nmiddle\n{MARKER_START}\nold body\n{MARKER_END}\ntail\n"
        result = upsert_managed_block(existing, "new body")
        for text in ("intro", "middle", "tail", "new body"):
            self.assertEqual(result.count(text), 1, text)
        self.assertNotIn("old body", result)
        self.assertEqual(result.count(MARKER_START), 1)

    def test_upsert_keeps_the_text_around_the_block_and_is_stable(self):
        once = upsert_managed_block("# Mine\n\nbefore\n", "rules")
        twice = upsert_managed_block(once, "rules")
        self.assertEqual(once, twice)
        edited = upsert_managed_block(once + "\nafter\n", "newer rules")
        self.assertTrue(edited.startswith("# Mine\n\nbefore\n"))
        self.assertTrue(edited.endswith("\nafter\n"))
        self.assertIn("newer rules", edited)
        self.assertNotIn("\nrules\n", edited)


class AgentContractValidationTests(unittest.TestCase):
    def _root(self, tmp: str) -> Path:
        root = Path(tmp) / "repo"
        shutil.copytree(ROOT / "agents", root / "agents")
        return root

    def _change(self, root: Path, name: str, old: str, new: str) -> None:
        path = root / "agents" / name
        text = path.read_bytes().decode("utf-8")
        self.assertIn(old, text)
        path.write_bytes(text.replace(old, new, 1).encode("utf-8"))

    def test_the_real_contracts_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(validate_agents(self._root(tmp)), [])

    def test_each_kind_of_breakage_is_named(self):
        cases = (
            ("tools without Bash", "executor.md", '"Edit", "Write", "Bash"', '"Edit", "Write"', "must include Bash"),
            ("unknown tool", "planner.md", '"Grep"', '"Frobnicate"', "unknown tool Frobnicate"),
            ("name differs from the file", "planner.md", "name: planner", "name: planer", "frontmatter name must be planner"),
            ("bad model", "planner.md", "model: opus", "model: gpt-4", "not a Claude Code value"),
            ("no runtime core", "auditor.md", "<!-- runtime-core:start -->", "", "missing runtime-core block"),
            ("no description", "orchestrator.md", "description:", "summary:", "missing description"),
        )
        for label, name, old, new, expected in cases:
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                root = self._root(tmp)
                self._change(root, name, old, new)
                errors = validate_agents(root)
                self.assertTrue(any(expected in e and e.startswith(f"agents/{name}") for e in errors), errors)

    def test_a_missing_contract_or_folder_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "agents" / "designer.md").unlink()
            self.assertEqual(validate_agents(root), ["missing agent contract: agents/designer.md"])
            shutil.rmtree(root / "agents")
            self.assertEqual(validate_agents(root), ["missing agents/"])

    def test_a_file_without_frontmatter_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "agents" / "planner.md").write_text("# Planner\n", encoding="utf-8")
            self.assertTrue(any("planner.md: missing YAML frontmatter" in e for e in validate_agents(root)))


if __name__ == "__main__":
    unittest.main()
