"""The agent contracts rendered as Codex, OpenCode, Cursor and Devin subagents, and installed for the tools in use."""

import json
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

from bossku.doctor import gather_doctor_issues
from bossku.host_agents import (
    HOSTS, ROLE_MODELS, file_name, host_dirs, opencode_provider, outdated_host_agents, remove_host_agents, render,
)
from bossku.install import AGENT_FILES, AGENT_SIGNATURE, install_user, uninstall_user
from bossku.skills import _parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
ROLES = [name[:-3] for name in AGENT_FILES]


def contract(role):
    return (ROOT / "agents" / f"{role}.md").read_text(encoding="utf-8")


def use_tools(home, *hosts):
    for host in hosts:
        host_dirs(home)[host][0].mkdir(parents=True, exist_ok=True)


class RenderTests(unittest.TestCase):
    def test_every_role_has_a_model_choice_for_every_tool(self):
        self.assertEqual(sorted(ROLE_MODELS), sorted(ROLES))
        for role, hosts in ROLE_MODELS.items():
            self.assertEqual(sorted(hosts), sorted(HOSTS), role)

    def test_codex_files_are_valid_toml_with_the_contract_as_instructions(self):
        for role in ROLES:
            data = tomllib.loads(render("codex", role, contract(role)))
            self.assertEqual(data["name"], role.replace("-", "_"))
            self.assertTrue(data["description"])
            self.assertIn(AGENT_SIGNATURE, data["developer_instructions"])
            self.assertNotIn("name: ", data["developer_instructions"].split("\n", 1)[0], "frontmatter left in the body")
            choice = ROLE_MODELS[role]["codex"]
            self.assertEqual(data.get("model"), choice["model"], role)
            self.assertEqual(data.get("model_reasoning_effort"), choice["effort"], role)
        for role in ROLES:   # Codex reads files through the shell: switching it off would leave an agent blind
            self.assertNotIn("features", tomllib.loads(render("codex", role, contract(role))), role)

    def test_codex_instructions_survive_triple_quotes(self):
        text = contract("researcher").replace("Stay under 400 words.", "Stay under 400 words. ''' and \"\"\" and \\n")
        body = tomllib.loads(render("codex", "researcher", text))["developer_instructions"]
        self.assertIn("''' and \"\"\" and \\n", body)

    def test_markdown_tools_get_frontmatter_they_read(self):
        for role in ROLES:
            for host in ("opencode", "cursor", "devin"):
                text = render(host, role, contract(role))
                front = _parse_frontmatter(text)
                self.assertTrue(front.get("description"), (host, role))
                self.assertIn(AGENT_SIGNATURE, text)
                self.assertEqual(text.count("\n---\n"), 1, (host, role, "one closing fence, body follows"))
        self.assertEqual(_parse_frontmatter(render("opencode", "executor", contract("executor")))["mode"], "subagent")

    def test_models_follow_the_table(self):
        r = lambda host, role, **kw: render(host, role, contract(role), **kw)
        self.assertIn("model: anthropic/claude-haiku-5-5", r("opencode", "researcher", provider="anthropic"))
        self.assertIn("model: ollama-cloud/deepseek-v4.1-flash", r("opencode", "researcher", provider="ollama-cloud"))
        self.assertIn("model: ollama-cloud/kimi-k2.7-code", r("opencode", "executor", provider="ollama-cloud"))
        self.assertIn("model: ollama-cloud/kimi-k3", r("opencode", "planner", provider="ollama-cloud"))
        self.assertNotIn("model:", r("opencode", "researcher"), "no provider set up: the subagent inherits")
        self.assertNotIn("model:", r("opencode", "orchestrator", provider="ollama-cloud"), "it follows the session")
        self.assertIn("model: composer-2.5", r("cursor", "researcher"))
        self.assertIn("model: claude-opus-5-5[effort=high]", r("cursor", "planner"))
        self.assertIn("model: claude-sonnet-5-5", r("cursor", "executor"))
        self.assertIn("model: gpt-5.6-sol", r("cursor", "auditor"))
        self.assertIn("model: inherit", r("cursor", "orchestrator"))
        self.assertIn("model: swe", r("devin", "researcher"))
        self.assertIn("model: opus", r("devin", "planner"))
        self.assertIn("model: codex", r("devin", "auditor"))
        self.assertNotIn("model:", r("devin", "orchestrator"))

    def test_the_checker_is_not_the_same_model_family_as_the_builder(self):
        # Creator and verifier apart: where a tool offers another family, the auditor does not grade its own family.
        family = lambda model: re.split(r"[-:.\[]", model)[0]
        for host, key in (("cursor", "model"), ("devin", "model"), ("opencode", "ollama-cloud")):
            builder = ROLE_MODELS["executor"][host][key]
            checker = ROLE_MODELS["auditor"][host][key]
            self.assertNotEqual(family(builder), family(checker), host)

    def test_read_only_roles_are_locked_and_builders_are_not(self):
        researcher = render("opencode", "researcher", contract("researcher"))
        self.assertIn("  edit: deny", researcher)
        self.assertIn("  bash: deny", researcher)
        self.assertIn("  task: deny", researcher, "no handing the work to a subagent that can edit")
        auditor = render("opencode", "auditor", contract("auditor"))
        self.assertIn("  edit: deny", auditor)
        self.assertNotIn("bash: deny", auditor, "the auditor runs the checks")
        self.assertNotIn("permission:", render("opencode", "executor", contract("executor")))
        self.assertIn("readonly: true", render("cursor", "planner", contract("planner")))
        self.assertNotIn("readonly", render("cursor", "auditor", contract("auditor")), "test runs write caches")
        self.assertNotIn("readonly", render("cursor", "orchestrator", contract("orchestrator")), "it writes the handoff")
        self.assertIn("allowed-tools:\n  - read\n  - grep\n  - glob", render("devin", "researcher", contract("researcher")))
        self.assertNotIn("allowed-tools", render("devin", "executor", contract("executor")))


class InstallTests(unittest.TestCase):
    def test_install_writes_only_for_tools_in_use_and_uninstall_removes_only_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            use_tools(home, "codex", "cursor")
            own = host_dirs(home)["cursor"][1] / "auditor.md"
            own.parent.mkdir(parents=True)
            own.write_text("---\nname: auditor\n---\nmine\n", encoding="utf-8")
            result = install_user(root=ROOT, home=home, profile="core")["host_agents"]
            self.assertEqual(sorted(result), ["codex", "cursor"], "OpenCode and Devin are not set up here")
            self.assertEqual(len(result["codex"]["installed"]), len(AGENT_FILES))
            self.assertEqual(result["cursor"]["kept"], ["auditor.md"])
            for role in ROLES:
                self.assertTrue((host_dirs(home)["codex"][1] / file_name("codex", role)).is_file())
            self.assertFalse(host_dirs(home)["opencode"][1].exists())
            self.assertEqual(outdated_host_agents(ROOT, home), {})
            self.assertFalse(any("subagents" in i for i in gather_doctor_issues(ROOT, home)))

            removed = uninstall_user(root=ROOT, home=home)["removed_host_agents"]
            self.assertEqual(len(removed["codex"]), len(AGENT_FILES))
            self.assertEqual(own.read_text(encoding="utf-8"), "---\nname: auditor\n---\nmine\n")

    def test_doctor_flags_a_stale_or_missing_copy_and_no_agents_removes_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            use_tools(home, "devin")   # set up after the install: nothing there yet
            self.assertIn("devin subagents missing or out of date (" + ", ".join(f"{r}.md" for r in ROLES)
                          + "); run `bossku update`", gather_doctor_issues(ROOT, home))
            install_user(root=ROOT, home=home, profile="core")
            planner = host_dirs(home)["devin"][1] / "planner.md"
            planner.write_bytes(planner.read_bytes().replace(b"\n", b"\r\n"))
            self.assertEqual(outdated_host_agents(ROOT, home), {}, "line endings alone are not drift")
            planner.write_text(planner.read_text(encoding="utf-8").replace("model: opus", "model: sonnet"), encoding="utf-8")
            self.assertEqual(outdated_host_agents(ROOT, home), {"devin": ["planner.md"]})
            install_user(root=ROOT, home=home, profile="core", agents=False)
            self.assertEqual(list(host_dirs(home)["devin"][1].glob("*.md")), [])
            self.assertFalse(any("subagents" in i for i in gather_doctor_issues(ROOT, home)), "--no-agents expects none")

    def test_a_tool_folder_linked_to_claude_agents_is_never_written_or_emptied(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="core")
            claude = home / ".claude" / "agents"
            before = {p.name: p.read_bytes() for p in claude.glob("*.md")}
            use_tools(home, "cursor")
            link = host_dirs(home)["cursor"][1]
            try:
                if sys.platform == "win32":
                    made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(claude)], capture_output=True).returncode == 0
                else:
                    link.symlink_to(claude, target_is_directory=True)
                    made = True
            except OSError:
                made = False
            if not made:
                self.skipTest("cannot create a folder link here")
            result = install_user(root=ROOT, home=home, profile="core")["host_agents"]
            self.assertEqual(result["cursor"]["installed"], [])
            self.assertIn("same folder as ~/.claude/agents", result["cursor"]["skipped"][0])
            self.assertEqual({p.name: p.read_bytes() for p in claude.glob("*.md")}, before, "Claude contracts unchanged")
            self.assertEqual(outdated_host_agents(ROOT, home), {})
            self.assertEqual(remove_host_agents(home), {})
            self.assertEqual(sorted(p.name for p in claude.glob("*.md")), sorted(before), "nothing deleted through the link")

    def test_the_opencode_provider_comes_from_its_login_or_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertIsNone(opencode_provider(home), "nothing set up: subagents inherit")
            auth = home / ".local" / "share" / "opencode" / "auth.json"
            auth.parent.mkdir(parents=True)
            auth.write_text(json.dumps({"openai": {"type": "api"}}), encoding="utf-8")
            self.assertIsNone(opencode_provider(home), "a provider Bossku has no picks for")
            auth.write_text(json.dumps({"ollama-cloud": {"type": "api"}}), encoding="utf-8")
            self.assertEqual(opencode_provider(home), "ollama-cloud", "/connect Ollama Cloud")
            auth.write_text(json.dumps({"anthropic": {"type": "oauth"}, "ollama-cloud": {"type": "api"}}), encoding="utf-8")
            self.assertEqual(opencode_provider(home), "ollama-cloud", "both set up and no default model: Ollama Cloud first")
            cfg = home / ".config" / "opencode" / "opencode.jsonc"
            cfg.parent.mkdir(parents=True)
            cfg.write_text('{\n  // mine\n  "model": "anthropic/claude-sonnet-5-5"\n}\n', encoding="utf-8")
            self.assertEqual(opencode_provider(home), "anthropic", "the user's default model picks the provider")
            auth.unlink()
            cfg.write_text('{"provider": {"openrouter": {"models": {"x": {"id": "anthropic/claude-haiku-5-5"}}}}}', encoding="utf-8")
            self.assertIsNone(opencode_provider(home), "an anthropic/ model id under another provider is not Anthropic")
            cfg.write_text('{"provider": {"ollama-cloud": {"options": {}}}}', encoding="utf-8")
            self.assertEqual(opencode_provider(home), "ollama-cloud")
            use_tools(home, "opencode")
            install_user(root=ROOT, home=home, profile="core")
            agents = host_dirs(home)["opencode"][1]
            self.assertTrue(re.search(r"(?m)^model: ollama-cloud/deepseek-v4.1-flash$", (agents / "researcher.md").read_text(encoding="utf-8")))
            self.assertTrue(re.search(r"(?m)^model: ollama-cloud/glm-5.3$", (agents / "auditor.md").read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
