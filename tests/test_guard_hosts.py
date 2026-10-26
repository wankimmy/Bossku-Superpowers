"""The destructive-command guard on Codex, Cursor and OpenCode: what `bossku hooks install` writes, and that it
comes out again. The guard's own rules are tested in tests/hooks.test.mjs."""
import json
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from bossku.hooks import HARNESS_MARKER, OPENCODE_GUARD_FILE, install_hooks, uninstall_hooks

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("codex", "cursor", "opencode")


def _home(tmp: str) -> Path:
    home = Path(tmp)
    for folder in (".codex", ".cursor", ".config/opencode"):
        (home / folder).mkdir(parents=True)
    return home


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@unittest.skipIf(shutil.which("node") is None, "the Codex and Cursor guard runs with node")
class GuardHostTests(unittest.TestCase):
    def test_install_wires_the_guard_in_each_tool_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = _home(tmp)
            result = install_hooks(home=home, tools=TOOLS, root=ROOT)
            for tool in TOOLS:
                self.assertEqual(result[f"{tool}_guard"]["status"], "installed", tool)
            codex = _read(home / ".codex" / "hooks.json")["hooks"]["PreToolUse"]
            self.assertEqual(len(codex), 1)
            self.assertEqual(codex[0]["matcher"], "Bash")
            command = codex[0]["hooks"][0]["command"]
            self.assertIn("hooks/guard.mjs", command)
            self.assertIn("--host codex", command)
            self.assertIn(HARNESS_MARKER, command)
            cursor = _read(home / ".cursor" / "hooks.json")
            self.assertEqual(cursor["version"], 1)
            self.assertIn("--host cursor", cursor["hooks"]["beforeShellExecution"][0]["command"])
            plugin = (home / ".config" / "opencode" / "plugins" / OPENCODE_GUARD_FILE).read_text(encoding="utf-8")
            self.assertIn((ROOT / "hooks" / "guard.mjs").resolve().as_posix(), plugin)
            again = install_hooks(home=home, tools=TOOLS, root=ROOT)
            for tool in TOOLS:
                self.assertEqual(again[f"{tool}_guard"]["status"], "already_installed", tool)

    def test_user_entries_stay_and_uninstall_and_no_harness_take_only_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = _home(tmp)
            mine = {"matcher": "Bash", "hooks": [{"type": "command", "command": "my-check.sh"}]}
            (home / ".codex" / "hooks.json").write_text(json.dumps({"hooks": {"PreToolUse": [mine]}}), encoding="utf-8")
            install_hooks(home=home, tools=TOOLS, root=ROOT)
            self.assertEqual(len(_read(home / ".codex" / "hooks.json")["hooks"]["PreToolUse"]), 2)
            off = install_hooks(home=home, tools=TOOLS, root=ROOT, harness=False)
            for tool in TOOLS:
                self.assertEqual(off[f"{tool}_guard"]["status"], "removed", tool)
            self.assertEqual(_read(home / ".codex" / "hooks.json")["hooks"]["PreToolUse"], [mine])
            self.assertNotIn("beforeShellExecution", _read(home / ".cursor" / "hooks.json")["hooks"])
            self.assertFalse((home / ".config" / "opencode" / "plugins" / OPENCODE_GUARD_FILE).exists())
            install_hooks(home=home, tools=TOOLS, root=ROOT)
            gone = uninstall_hooks(home=home, tools=TOOLS)
            for tool in TOOLS:
                self.assertEqual(gone[f"{tool}_guard"]["status"], "removed", tool)
            self.assertEqual(_read(home / ".codex" / "hooks.json")["hooks"]["PreToolUse"], [mine])

    def test_a_missing_tool_folder_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = install_hooks(home=Path(tmp), tools=TOOLS, root=ROOT)
            for tool in TOOLS:
                self.assertEqual(result[f"{tool}_guard"]["status"], "skipped_not_found", tool)

    def test_opencode_plugin_guards_both_opencode_1_and_2(self):
        # Load the generated plugin in node and drive it the way each OpenCode major calls plugins.
        driver = textwrap.dedent("""
            import assert from "node:assert/strict";
            import { pathToFileURL } from "node:url";
            const plugin = (await import(pathToFileURL(process.argv[2]).href)).default;
            const v1 = (await plugin.server({ directory: "/proj" }))["tool.execute.before"];
            await v1({ tool: "bash" }, { args: { command: "git status" } });
            await assert.rejects(v1({ tool: "bash" }, { args: { command: "git reset --hard" } }), /denied/);
            await assert.rejects(v1({ tool: "bash" }, { args: { command: "git push origin main" } }), /go-ahead/);
            const hooks = {};
            const on = (kind) => ({ hook: async (name, cb) => { hooks[kind + name] = cb; return {}; } });
            await plugin.setup({ tool: on("tool:"), permission: on("perm:") });
            await assert.rejects(hooks["tool:execute.before"]({ tool: "shell", input: { command: "rm -rf ~" } }), /denied/);
            await hooks["tool:execute.before"]({ tool: "shell", input: { command: "git push origin main" } });
            const request = { action: "shell", resources: ["npm test", "git push origin main"], effect: "allow" };
            await hooks["perm:evaluate"](request);
            assert.equal(request.effect, "ask");
            console.log("ok");
        """)
        with tempfile.TemporaryDirectory() as tmp:
            home = _home(tmp)
            install_hooks(home=home, tools=("opencode",), root=ROOT)
            script = Path(tmp) / "driver.mjs"
            script.write_text(driver, encoding="utf-8")
            plugin = home / ".config" / "opencode" / "plugins" / OPENCODE_GUARD_FILE
            run = subprocess.run(["node", str(script), str(plugin)], capture_output=True, text=True, timeout=60)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("ok", run.stdout)


if __name__ == "__main__":
    unittest.main()
