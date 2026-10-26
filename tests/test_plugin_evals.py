"""The `claude plugin eval` suite in evals/ stays loadable and in step with the lean skill list.

The keys and grader types are the ones `claude plugin eval init` documents (Claude Code 2.1.310). A paid run is
the real test; this only catches a case the runner would refuse, or one that no longer matches a listed skill.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
PROMPT_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome",
               "model", "max_turns", "timeout_seconds", "allowed_tools", "disallowed_tools", "artifact_publish",
               "growthbook_overrides", "append_system_prompt", "env"}
GRADER_KEYS = {
    "regex": {"type", "target", "pattern", "flags", "match", "weight", "arm"},
    "tool_order": {"type", "before", "after", "weight", "arm"},
    "tool_used": {"type", "tool", "input_match", "min", "max", "weight", "arm"},
    "file_exists": {"type", "path", "exists", "weight", "arm"},
    "llm": {"type", "criteria", "focus", "weight", "arm"},
    "baseline": {"type", "baseline_file", "criteria", "weight", "arm"},
}
FOCUS = {"trace", "last_message", "files", "mock_calls"}
GATED = ("Bash", "Write", "Edit", "WebFetch", "PowerShell", "mcp__")
CASE_NAME = re.compile(r"^(?P<skill>[a-z0-9-]+)--(?P<kind>fires|quiet)-[a-z0-9-]+$")


def _scalar(raw: str):
    """The value forms the suite uses: JSON (strings, lists, maps), 'single quoted', true/false, ints, bare words."""
    raw = raw.strip()
    if raw[:1] in ('"', "[", "{"):
        return json.loads(raw)
    if raw[:1] == "'":
        return raw[1:-1].replace("''", "'")
    if raw in ("true", "false"):
        return raw == "true"
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def _read(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if match is None:
        raise AssertionError(f"{path}: no frontmatter")
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = _scalar(value)
    return meta, text[match.end():]


def _cases() -> list[Path]:
    return sorted(p for p in EVALS.iterdir() if p.is_dir() and p.name != "results")


class PluginEvalSuiteTests(unittest.TestCase):
    def test_every_case_is_one_the_runner_accepts(self):
        for case in _cases():
            with self.subTest(case=case.name):
                self.assertRegex(case.name, CASE_NAME)
                meta, body = _read(case / "prompt.md")
                self.assertLessEqual(set(meta), PROMPT_KEYS)
                self.assertTrue(body.strip())
                self.assertTrue(0 < meta["max_turns"] <= 200 and 0 < meta["timeout_seconds"] <= 3600)
                self.assertGreaterEqual(meta.get("runs", 3), 3)   # the eval guide's floor
                self.assertNotRegex(body, r"(^|\s)(~/|/home/|/Users/|[A-Za-z]:\\)")   # cases run in a sandbox cwd
                outcome = 0
                for grader in sorted((case / "graders").glob("*.md")):
                    fm, text = _read(grader)
                    self.assertIn(fm.get("type"), GRADER_KEYS, grader.name)
                    self.assertLessEqual(set(fm), GRADER_KEYS[fm["type"]], grader.name)
                    if fm["type"] == "tool_used":
                        re.compile(fm["input_match"])
                        continue
                    outcome += 1
                    if fm["type"] in ("llm", "regex"):
                        self.assertTrue(text.strip(), grader.name)
                    if fm["type"] == "regex":
                        re.compile(text.strip())
                    focus = fm.get("focus", "last_message")
                    if fm["type"] == "llm" and not isinstance(focus, dict):
                        self.assertIn(focus, FOCUS, grader.name)
                self.assertGreaterEqual(outcome, 1, "every case needs a grader on the result, not only tool_used")

    def test_each_lean_skill_has_two_should_load_cases_and_a_near_miss(self):
        listed = json.loads((ROOT / "skills" / "lean.json").read_text(encoding="utf-8"))["listed"]
        found: dict[str, list[str]] = {}
        for case in _cases():
            parts = CASE_NAME.match(case.name)
            found.setdefault(parts["skill"], []).append(parts["kind"])
        self.assertEqual(sorted(found), sorted(listed))
        for skill, kinds in found.items():
            with self.subTest(skill=skill):
                self.assertEqual(len(kinds), 3)
                # The default voice is meant to load on every reply, so it has no should-not-load case.
                want = 3 if skill == "malaysia-localisation" else 2
                self.assertEqual(kinds.count("fires"), want)

    def test_the_skill_check_matches_only_the_case_skill(self):
        for case in _cases():
            parts = CASE_NAME.match(case.name)
            skill = parts["skill"]
            with self.subTest(case=case.name):
                self.assertTrue((ROOT / "skills" / skill / "SKILL.md").is_file(), "plugins list skills/ only")
                name = "skill-fires" if parts["kind"] == "fires" else "skill-stays-quiet"
                fm, _ = _read(case / "graders" / f"{name}.md")
                self.assertEqual((fm["type"], fm["tool"]), ("tool_used", "Skill"))
                pattern = re.compile(fm["input_match"])
                call = lambda sid: json.dumps({"skill": sid, "args": ""}, separators=(",", ":"))   # noqa: E731
                self.assertRegex(call(skill), pattern)
                self.assertRegex(call(f"bossku-superpower:{skill}"), pattern)
                self.assertNotRegex(call(f"bossku-superpower:{skill}-extra"), pattern)
                self.assertNotRegex(call(f"x{skill}"), pattern)
                if parts["kind"] == "quiet":   # scored in both arms, so loading it costs the plugin
                    self.assertEqual((fm["min"], fm["max"], fm["arm"]), (0, 0, "both"))

    def test_tags_say_which_cases_need_a_tool_grant(self):
        # evals/README.md runs `--tag answer` with no grant; cases with gated tools must carry `work` or `cli`.
        for case in _cases():
            meta, _ = _read(case / "prompt.md")
            gated = [t for t in meta["allowed_tools"] if t.startswith(GATED)]
            with self.subTest(case=case.name):
                self.assertIn("Skill", meta["allowed_tools"])
                if gated:
                    self.assertTrue({"work", "cli"} & set(meta["tags"]), gated)
                else:
                    self.assertIn("answer", meta["tags"])

    def test_results_stay_out_of_git(self):
        self.assertIn("evals/results/", (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines())


if __name__ == "__main__":
    unittest.main()
