"""Install, uninstall, doctor and validate fixes. Every test uses a temporary home; none touches the real one."""

import contextlib
import io
import json
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path

from bossku import __version__
from bossku.cli import main
from bossku.doctor import format_doctor_success, gather_doctor_issues
from bossku.hooks import harness_status, uninstall_hooks
from bossku.init_project import init_project, upsert_managed_block
from bossku.install import remove_instruction_blocks, install_user, uninstall_user, update_user
from bossku.paths import MARKER_START, claude_skills_dir, user_config_dir
from bossku.skills import load_lean
from bossku.validate import (
    AGENTS_MD_MAX_CHARS,
    validate_hooks,
    validate_instructions,
    validate_plugin_manifests,
)

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*argv: str) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        return main(list(argv))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def edit_claude_hooks(home: Path, edit) -> None:
    path = home / ".claude" / "settings.json"
    data = read_json(path)
    edit(data["hooks"])
    write_json(path, data)


class PlainInstallTests(unittest.TestCase):
    def test_plain_install_keeps_the_profile_already_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(run_cli("--home", str(home), "--root", str(ROOT), "install", "--profile", "core"), 0)
            core_count = len(list(claude_skills_dir(home).iterdir()))
            self.assertEqual(run_cli("--home", str(home), "--root", str(ROOT), "install"), 0)
            self.assertEqual(read_json(user_config_dir(home) / "config.json")["profile"], "core")
            self.assertEqual(len(list(claude_skills_dir(home).iterdir())), core_count)

    def test_explicit_profile_still_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            run_cli("--home", str(home), "--root", str(ROOT), "install", "--profile", "core")
            run_cli("--home", str(home), "--root", str(ROOT), "install", "--profile", "lean")
            self.assertEqual(read_json(user_config_dir(home) / "config.json")["profile"], "lean")


class RoutingCacheTests(unittest.TestCase):
    def test_install_writes_no_routing_cache_and_removes_an_old_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            old = user_config_dir(home) / "routing-cache.json"
            old.parent.mkdir(parents=True)
            old.write_text("{}", encoding="utf-8")
            result = install_user(root=ROOT, home=home, profile="core")
            self.assertFalse(old.exists())
            self.assertNotIn("routing_cache", result)


class UninstallTests(unittest.TestCase):
    def _home_with_user_text(self, tmp: str) -> Path:
        home = Path(tmp)
        for folder in (home / ".claude", home / ".codex", home / ".config" / "opencode"):
            folder.mkdir(parents=True)
        (home / ".claude" / "CLAUDE.md").write_text("Keep my project glossary.\n", encoding="utf-8")
        (home / ".codex" / "AGENTS.md").write_text("# Mine\n\nUse tabs.\n", encoding="utf-8")
        return home

    def test_plain_uninstall_keeps_the_instruction_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home_with_user_text(tmp)
            install_user(root=ROOT, home=home, profile="core")
            result = uninstall_user(root=ROOT, home=home)
            self.assertEqual(result["cleaned_instructions"], [])
            text = (home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("bosskuai:memory:start", text)
            self.assertIn("bosskuai:voice:start", text)

    def test_purge_removes_both_blocks_and_only_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._home_with_user_text(tmp)
            install_user(root=ROOT, home=home, profile="core")
            result = uninstall_user(root=ROOT, home=home, purge=True)
            self.assertEqual(len(result["cleaned_instructions"]), 3)
            for name in (home / ".claude" / "CLAUDE.md", home / ".codex" / "AGENTS.md",
                         home / ".config" / "opencode" / "AGENTS.md"):
                self.assertNotIn("bosskuai:", name.read_text(encoding="utf-8"), msg=str(name))
            self.assertEqual((home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "Keep my project glossary.\n")
            self.assertEqual((home / ".codex" / "AGENTS.md").read_text(encoding="utf-8"), "# Mine\n\nUse tabs.\n")
            self.assertEqual(uninstall_user(root=ROOT, home=home, purge=True)["cleaned_instructions"], [])

    def test_removal_keeps_text_after_the_blocks_and_crlf_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            path = home / ".claude" / "CLAUDE.md"
            blocks = path.read_text(encoding="utf-8").replace("\n", "\r\n")
            path.write_bytes(("Mine.\r\n\r\n" + blocks.strip() + "\r\n\r\nAfter the blocks.\r\n").encode("utf-8"))
            self.assertEqual(remove_instruction_blocks(home), [str(path)])
            self.assertEqual(path.read_bytes(), b"Mine.\r\n\r\nAfter the blocks.\r\n")

    def test_removal_works_on_a_read_only_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            path = home / ".claude" / "CLAUDE.md"
            os.chmod(path, stat.S_IREAD)
            self.assertEqual(remove_instruction_blocks(home), [str(path)])
            self.assertNotIn("bosskuai:", path.read_text(encoding="utf-8"))

    def test_uninstall_removes_only_support_files_that_match_the_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            shared = next(p for p in sorted((ROOT / "references").rglob("*")) if p.is_file())
            edited = home / ".claude" / shared.relative_to(ROOT)
            edited.write_text(edited.read_text(encoding="utf-8") + "\nmy note\n", encoding="utf-8")
            mine = home / ".agents" / "references" / "my-own.md"
            mine.write_text("mine", encoding="utf-8")
            uninstall_user(root=ROOT, home=home)
            def support_files(parent: str) -> list[Path]:
                return [p for name in ("references", "site", "docs") for p in (home / parent / name).rglob("*") if p.is_file()]

            left_claude, left_agents = support_files(".claude"), support_files(".agents")
            self.assertEqual(left_claude, [edited])
            self.assertEqual(left_agents, [mine])

    def test_uninstall_leaves_no_support_folders_behind(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            uninstall_user(root=ROOT, home=home)
            for parent in (".agents", ".claude"):
                for name in ("references", "site", "docs"):
                    self.assertFalse((home / parent / name).exists(), msg=f"{parent}/{name}")

    def test_each_removed_skill_is_listed_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            removed = uninstall_user(root=ROOT, home=home)["removed_skills"]
            self.assertTrue(removed)
            self.assertEqual(len(removed), len(set(removed)))


class DoctorTests(unittest.TestCase):
    def test_a_partial_claude_hook_set_is_named_but_is_not_an_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            self.assertEqual(gather_doctor_issues(ROOT, home), [])
            edit_claude_hooks(home, lambda hooks: hooks.update(
                Stop=[e for e in hooks["Stop"] if "verify-gate" not in json.dumps(e)]))
            self.assertEqual(gather_doctor_issues(ROOT, home), [], "dropping the verify-gate is a user choice")
            lines = format_doctor_success(ROOT, home, version=__version__)
            # With the Node stop gate wired, it does the verify-gate's job, so the verify-gate is not called missing.
            gone = "" if harness_status(home)["hooks"] else " (not installed: verify-gate)"
            self.assertIn("  claude_code hooks: sync (Stop), sync (SessionEnd), skill-hint, session-brief" + gone, lines)

            uninstall_hooks(home=home, tools=("claude_code",))
            self.assertEqual(gather_doctor_issues(ROOT, home), [])
            lines = format_doctor_success(ROOT, home, version=__version__)
            self.assertIn("  claude_code hooks: none installed (opted out)", lines)

    def test_a_hook_that_runs_a_missing_program_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            gone = (home / "gone" / "bossku.EXE").as_posix()

            def point_at_gone(hooks):
                for entry in hooks["UserPromptSubmit"]:
                    for hook in entry["hooks"]:
                        hook["command"] = f'"{gone}" skill-hint'

            edit_claude_hooks(home, point_at_gone)
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("skill-hint hook runs" in i and "no longer exists" in i for i in issues), issues)

    def test_success_output_names_the_installed_pieces_and_gate_switches(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            old = os.environ.get("BOSSKU_VERIFY_GATE")
            os.environ["BOSSKU_VERIFY_GATE"] = "0"
            try:
                lines = format_doctor_success(ROOT, home, version=__version__)
            finally:
                if old is None:
                    del os.environ["BOSSKU_VERIFY_GATE"]
                else:
                    os.environ["BOSSKU_VERIFY_GATE"] = old
            self.assertTrue(any(l.startswith("  claude_code hooks:") and "skill-hint" in l for l in lines), lines)
            self.assertIn("  gate switches set in this shell: BOSSKU_VERIFY_GATE=0", lines)

    def test_a_missing_install_source_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            cfg_path = user_config_dir(home) / "config.json"
            cfg = read_json(cfg_path)
            cfg["installed_from"] = str(home / "no-such-checkout")
            write_json(cfg_path, cfg)
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("install source" in i and "is missing" in i for i in issues), issues)

    def test_an_installed_skill_that_differs_from_the_repo_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            skill = claude_skills_dir(home) / "cofounder" / "SKILL.md"
            original = skill.read_text(encoding="utf-8")
            skill.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(gather_doctor_issues(ROOT, home), [], "line endings are not drift")

            skill.write_text(original + "\nlocal edit\n", encoding="utf-8")
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("differ from the repo: cofounder" in i for i in issues), issues)

            update_user(root=ROOT, home=home)
            self.assertEqual(gather_doctor_issues(ROOT, home), [])

    def test_a_skill_missing_from_both_hosts_is_not_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            for host in (".agents", ".claude"):
                shutil.rmtree(home / host / "skills" / "bosskuai-engineering-delivery")
            self.assertFalse(any("differ" in i for i in gather_doctor_issues(ROOT, home)))

    def test_a_lean_install_is_clean_and_a_body_edit_is_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="lean")
            self.assertFalse(any("differ" in i for i in gather_doctor_issues(ROOT, home)),
                             "the lean description rewrite is not drift")
            listed = load_lean(ROOT)["listed"][0]
            skill = claude_skills_dir(home) / listed / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
            issues = gather_doctor_issues(ROOT, home)
            self.assertTrue(any("differ from the repo" in i and listed in i for i in issues), issues)

    def test_an_outdated_project_block_is_reported_until_init_runs_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "proj"
            install_user(root=ROOT, home=home, profile="core")
            init_project(project, root=ROOT, home=home)

            def project_issues():
                return [i for i in gather_doctor_issues(ROOT, home, project=project) if "AGENTS.md" in i]

            self.assertEqual(project_issues(), [])
            agents = project / "AGENTS.md"
            agents.write_text(upsert_managed_block(agents.read_text(encoding="utf-8"), "BosskuAI is active.\nOld rules."),
                              encoding="utf-8")
            self.assertTrue(any("out of date" in i for i in project_issues()), project_issues())
            init_project(project, root=ROOT, home=home)
            self.assertEqual(project_issues(), [])

    def test_the_repo_own_stub_block_is_not_out_of_date_but_the_same_stub_in_a_project_is(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            repo = mini_repo(tmp)
            stub = upsert_managed_block("# Rules\n", "Rules are in this file.")
            (repo / "AGENTS.md").write_text(stub, encoding="utf-8")
            other = Path(tmp) / "other"
            other.mkdir()
            (other / "AGENTS.md").write_text(stub, encoding="utf-8")

            def block_issues(project):
                return [i for i in gather_doctor_issues(repo, home, project=project) if "managed block" in i]

            self.assertEqual(block_issues(repo), [])
            self.assertTrue(any("out of date" in i for i in block_issues(other)), block_issues(other))
            (repo / "AGENTS.md").write_text("# Rules\n" + MARKER_START + "\nhalf a block\n", encoding="utf-8")
            self.assertTrue(any("no end marker" in i for i in block_issues(repo)), "the repo still needs a closed block")

    def test_a_project_block_with_no_end_marker_is_reported_as_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "proj"
            install_user(root=ROOT, home=home, profile="core")
            init_project(project, root=ROOT, home=home)
            (project / "AGENTS.md").write_text("# Mine\n" + MARKER_START + "\nhalf a block\n", encoding="utf-8")
            issues = [i for i in gather_doctor_issues(ROOT, home, project=project) if "AGENTS.md" in i]
            self.assertTrue(any("no end marker" in i for i in issues), issues)


def mini_repo(tmp: str) -> Path:
    """Just the files validate reads, so each test can break one of them."""
    root = Path(tmp) / "repo"
    root.mkdir()
    for name in (".claude-plugin", ".cursor-plugin", ".codex-plugin", ".agents", ".opencode", ".cursor", "agents"):
        shutil.copytree(ROOT / name, root / name)
    for name in ("pyproject.toml", "AGENTS.md"):
        shutil.copy2(ROOT / name, root / name)
    (root / "bossku").mkdir()
    shutil.copy2(ROOT / "bossku" / "__init__.py", root / "bossku" / "__init__.py")
    (root / "skills").mkdir()
    return root


class ValidateTests(unittest.TestCase):
    def test_a_copy_of_the_real_files_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            self.assertEqual(validate_plugin_manifests(root), [])
            self.assertEqual(validate_instructions(root), [])
            self.assertEqual(validate_hooks(root), [])

    def test_the_repository_instructions_fit_the_budget_and_carry_the_voice_rule(self):
        self.assertEqual(validate_instructions(ROOT), [])

    def test_marketplace_versions_must_match_pyproject(self):
        for rel, edit, label in (
            (".claude-plugin/marketplace.json", lambda d: d["plugins"][0].update(version="0.0.1"), "claude marketplace manifest plugin"),
            (".claude-plugin/marketplace.json", lambda d: d["metadata"].update(version="0.0.1"), "claude marketplace manifest metadata"),
            (".cursor-plugin/marketplace.json", lambda d: d["plugins"][0].update(version="0.0.1"), "cursor marketplace manifest plugin"),
            (".cursor-plugin/marketplace.json", lambda d: d["metadata"].update(version="0.0.1"), "cursor marketplace manifest metadata"),
            (".agents/plugins/marketplace.json", lambda d: d["plugins"][0].update(version="0.0.1"), "codex marketplace manifest plugin"),
        ):
            with self.subTest(rel=rel, label=label), tempfile.TemporaryDirectory() as tmp:
                root = mini_repo(tmp)
                data = read_json(root / rel)
                edit(data)
                write_json(root / rel, data)
                errors = validate_plugin_manifests(root)
                self.assertTrue(any(e.startswith(label) and "0.0.1" in e for e in errors), errors)

    def test_package_version_must_match_pyproject(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            (root / "bossku" / "__init__.py").write_text('__version__ = "9.9.9"\n', encoding="utf-8")
            errors = validate_plugin_manifests(root)
            self.assertTrue(any(e.startswith("bossku/__init__.py") and "9.9.9" in e for e in errors), errors)

    def test_codex_marketplace_source_is_the_repo_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            path = root / ".agents" / "plugins" / "marketplace.json"
            data = read_json(path)
            data["plugins"][0]["source"]["path"] = "./../.."
            write_json(path, data)
            self.assertTrue(any("source must be local ./" in e for e in validate_plugin_manifests(root)))

    def test_opencode_config_needs_valid_json_but_no_references_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            (root / ".opencode" / "opencode.jsonc").write_text('{"$schema": "https://opencode.ai/config.json"}', encoding="utf-8")
            self.assertEqual(validate_plugin_manifests(root), [])
            (root / ".opencode" / "opencode.jsonc").write_text("{", encoding="utf-8")
            self.assertTrue(any("invalid plugin JSON" in e for e in validate_plugin_manifests(root)))

    def test_agents_md_over_the_budget_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            agents = root / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "x" * AGENTS_MD_MAX_CHARS, encoding="utf-8")
            self.assertTrue(any("always-on budget" in e for e in validate_instructions(root)))

    def test_a_changed_voice_rule_copy_fails_but_rewrapping_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            executor = root / "agents" / "executor.md"
            original = executor.read_text(encoding="utf-8")
            executor.write_text(original.replace("Keep responses short, simple and easy to understand.",
                                                 "Keep responses short,\nsimple and easy to understand."), encoding="utf-8")
            self.assertEqual(validate_instructions(root), [])
            executor.write_text(original.replace("Answer first;", "Answer last;"), encoding="utf-8")
            self.assertTrue(any(e.startswith("agents/executor.md: voice rule") for e in validate_instructions(root)))
            cursor = root / ".cursor" / "rules" / "bosskuai.mdc"
            cursor.write_text(cursor.read_text(encoding="utf-8").replace("Answer first;", "Answer last;"), encoding="utf-8")
            self.assertTrue(any(e.startswith(".cursor/rules/bosskuai.mdc") for e in validate_instructions(root)))

    def test_hooks_must_exist_and_must_not_print_a_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = mini_repo(tmp)
            hooks = root / "hooks"
            hooks.mkdir()
            (hooks / "hooks.json").write_text(
                json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command",
                            "command": 'node "${CLAUDE_PLUGIN_ROOT}/hooks/stop-gate.mjs"'}]}]}}), encoding="utf-8")
            self.assertTrue(any("missing script: hooks/stop-gate.mjs" in e for e in validate_hooks(root)))
            (hooks / "stop-gate.mjs").write_text('const root = process.env.X || "<plugin-root>";\n', encoding="utf-8")
            self.assertEqual([e for e in validate_hooks(root) if "missing script" in e], [])
            self.assertTrue(any("unresolved placeholder <plugin-root>" in e for e in validate_hooks(root)))
            (hooks / "stop-gate.mjs").write_text('const root = process.env.X || "/real/path";\n', encoding="utf-8")
            self.assertEqual(validate_hooks(root), [])


if __name__ == "__main__":
    unittest.main()
