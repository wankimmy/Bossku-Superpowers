"""Docs group: every doc, manifest and CI claim checked here is read from the file that makes it."""

import importlib.util
import json
import re
import unittest
from pathlib import Path

from bossku.paths import MARKER_END, MARKER_START
from bossku.skills import list_skill_ids

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def outside_fences(text):
    """Blank out fenced code so only prose and tables are scanned."""
    out, fence = [], None
    for line in text.splitlines():
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append("")
        elif m:
            fence = m.group(1)
            out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def indicator(rel):
    match = re.search(r"^\[BOSSKUAI\] \| Skill: (<[^>]+>) \| Agent: <([^>]+)> \| Model Role:", read(rel), re.M)
    assert match, f"no one-line [BOSSKUAI] indicator in {rel}"
    return match.group(1), match.group(2).split("|")


class ManifestTests(unittest.TestCase):
    def test_codex_marketplace_source_resolves_to_the_repo_root(self):
        data = json.loads(read(".agents/plugins/marketplace.json"))
        entry = next(p for p in data["plugins"] if p["name"] == "bossku-superpower")
        self.assertEqual(entry["source"]["path"], "./")
        # Static check only: Codex's own resolution of './' was not run (`codex plugin marketplace add ./`).
        self.assertEqual((ROOT / entry["source"]["path"]).resolve(), ROOT.resolve())

    def test_opencode_config_points_at_nothing_that_is_missing(self):
        config = ROOT / ".opencode" / "opencode.jsonc"
        data = json.loads(config.read_text(encoding="utf-8"))
        for key, ref in (data.get("references") or {}).items():
            self.assertTrue((config.parent / ref["path"]).exists(), f"references.{key} -> {ref['path']}")

    def test_codex_listing_does_not_promise_a_partial_load(self):
        data = json.loads(read(".codex-plugin/plugin.json"))
        self.assertEqual(data["skills"], "./skills/")
        self.assertNotIn("without loading the full toolkit", data["interface"]["longDescription"])


class CiWorkflowTests(unittest.TestCase):
    def test_matrix_timeout_and_token_scope(self):
        text = read(".github/workflows/integrity-check.yml")
        for version in ("3.11", "3.12", "3.13"):
            self.assertIn(f'python-version: "{version}"', text)
        self.assertRegex(text, r"(?m)^timeout-minutes:|^\s+timeout-minutes: \d+")
        self.assertRegex(text, r"(?m)^permissions:\n  contents: read$")
        self.assertIn("windows-latest", text)


class InstructionFileTests(unittest.TestCase):
    def test_indicator_is_one_format_with_the_full_agent_list(self):
        agents_skill, agents_list = indicator("AGENTS.md")
        cursor_skill, cursor_list = indicator(".cursor/rules/bosskuai.mdc")
        self.assertEqual(agents_skill, cursor_skill)
        self.assertEqual(agents_list, cursor_list)
        contracts = {p.stem for p in (ROOT / "agents").glob("*.md")}
        self.assertEqual(set(agents_list), contracts | {"clarification"})
        hook = ROOT / "hooks" / "session-start.mjs"
        if hook.is_file():
            for name in agents_list:
                self.assertIn(name, hook.read_text(encoding="utf-8"))

    def test_agents_md_links_every_agent_contract(self):
        text = read("AGENTS.md")
        for path in sorted((ROOT / "agents").glob("*.md")):
            self.assertIn(f"(agents/{path.name})", text)

    def test_memory_save_rule_is_stated_once_per_file(self):
        for rel in ("AGENTS.md", ".cursor/rules/bosskuai.mdc"):
            text = read(rel)
            with self.subTest(rel=rel):
                self.assertEqual(text.lower().count("automatically save"), 1)
                self.assertNotIn("## Automatic vault memory", text)
                for clause in ("handoffs", "memory_project_roots", "Never store secrets", "transcripts"):
                    self.assertTrue(clause in text, f"unique memory clause dropped: {clause}")

    def test_agents_md_keeps_a_small_managed_block_for_doctor(self):
        text = read("AGENTS.md")
        self.assertEqual(text.count(MARKER_START), 1)
        block = text[text.index(MARKER_START):text.index(MARKER_END)]
        self.assertLess(len(block), 120)

    def test_doctor_accepts_this_repos_own_agents_md_block(self):
        import tempfile
        from bossku.doctor import gather_doctor_issues

        with tempfile.TemporaryDirectory() as home:
            issues = gather_doctor_issues(ROOT, Path(home), project=ROOT)
        self.assertEqual([i for i in issues if "AGENTS.md" in i], [])

    def test_pr_route_names_the_single_pr_skill_and_it_exists(self):
        text = read("AGENTS.md")
        self.assertIn("one PR → `bosskuai-pr-check`", text)
        self.assertTrue((ROOT / "skills" / "bosskuai-pr-check" / "SKILL.md").is_file())

    def test_grounding_is_not_claimed_as_loaded_for_agents_that_do_not_list_it(self):
        self.assertNotIn("loaded for every agent", read("AGENTS.md"))

    def test_contributing_quotes_the_agents_md_budget_validate_enforces(self):
        from bossku import validate

        budget = getattr(validate, "AGENTS_MD_MAX_CHARS", None)
        if budget is None:
            self.skipTest("validate has no AGENTS.md budget")
        self.assertIn(f"{budget:,} characters", read("CONTRIBUTING.md"))
        self.assertLessEqual(len(read("AGENTS.md")), budget)


class DocClaimTests(unittest.TestCase):
    def test_security_md_describes_the_hooks_install_writes(self):
        text = read("SECURITY.md")
        self.assertNotIn("disabled by default", text)
        self.assertNotIn("settings.hooks.example.json", text)
        self.assertNotIn("ai-assistant", text)
        self.assertIn("bossku hooks uninstall", text)

    def test_readme_points_at_the_node_hook_switches(self):
        text = read("README.md")
        self.assertIn("BOSSKU_STOP_GATE=off", text)
        self.assertIn("(hooks/README.md)", text)

    def test_the_verify_gate_switch_is_never_described_as_the_default_switch(self):
        # A default install wires the Node stop gate, which reads only BOSSKU_STOP_GATE. BOSSKU_VERIFY_GATE=0 switches
        # off the Python gate, so a doc may name it only on a line that also says `--no-harness`.
        self.assertNotIn("BOSSKU_VERIFY_GATE", read("hooks/stop-gate.mjs"))
        for rel in ("README.md", "SECURITY.md", "docs/installation.md", "docs/memory.md", "CHANGELOG.md"):
            text = read(rel)
            self.assertIn("BOSSKU_STOP_GATE", text, rel)
            for number, line in enumerate(text.splitlines(), 1):
                if "BOSSKU_VERIFY_GATE" in line:
                    with self.subTest(rel=rel, line=number):
                        self.assertIn("--no-harness", line)

    def test_the_docs_list_the_engineering_profile_wherever_they_list_the_others(self):
        from bossku.skills import PROFILES

        self.assertIn("engineering", PROFILES)
        for rel in ("AGENTS.md", "docs/skills.md", "docs/installation.md"):
            text = read(rel)
            with self.subTest(rel=rel):
                self.assertNotIn("lean|core|full", text)
                self.assertIn("lean|core|engineering|full", text)
        self.assertIn("| `engineering` |", read("docs/installation.md"))
        self.assertIn("--profile engineering", read("docs/skills.md"))

    def test_the_install_docs_name_the_hooks_and_choices_install_really_sets_up(self):
        text = read("docs/installation.md")
        for needle in ("--no-harness", "--no-agents", "--no-claude", "~/.claude/agents", "permissions.deny", "hint_mode",
                       "bossku resume", "BOSSKU_RESUME=off", "PreToolUse", "PostToolUse", "UserPromptSubmit"):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)

    def test_security_md_says_what_the_resume_hooks_read_and_write_and_how_to_turn_them_off(self):
        text = read("SECURITY.md")
        for needle in ("state_*.sqlite", "2 MB", "2,000 characters", "resume-state.json", "never saved to the vault",
                       "BOSSKU_RESUME=off", "permissions.deny", "~/.claude/agents"):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)

    def test_no_doc_pipes_a_remote_script_into_a_shell(self):
        pipe = re.compile(r"(?i)\b(irm|iwr|curl|wget)\b[^|\n]*\|\s*(iex|sh|bash|zsh)\b")
        for rel in ["README.md", "CONTRIBUTING.md", "SECURITY.md", *sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "docs").glob("*.md"))]:
            with self.subTest(rel=rel):
                self.assertIsNone(pipe.search(read(rel)))

    def test_windows_junction_snippet_never_deletes_a_real_folder(self):
        text = read("docs/installation.md")
        self.assertNotIn("Remove-Item $pluginDir -Recurse", text)
        self.assertIn('LinkType -ne "Junction"', text)

    def test_plugin_install_sections_warn_about_the_full_skill_list(self):
        sections = read("docs/installation.md").split("\n### ")
        for host in ("Claude Code", "Cursor", "Codex"):
            body = next(s for s in sections if s.startswith(host))
            with self.subTest(host=host):
                self.assertIn("ignores `--profile lean`", body)
                self.assertIn("does not add the hooks", body)

    def test_install_docs_describe_uninstall_and_profile_behaviour(self):
        text = read("docs/installation.md")
        self.assertIn("a plain `bossku install` keep your profile", text)
        self.assertRegex(text, r"bossku uninstall --purge.*memory and voice blocks|bossku uninstall --purge.*those two blocks")

    def test_opencode_docs_do_not_promise_references(self):
        for rel in ("docs/installation.md", "docs/architecture.md"):
            self.assertNotRegex(read(rel), r"(?i)opencode[^\n]*references (only|`AGENTS)|uses `\.opencode/opencode\.jsonc` for references")

    def test_pack_table_counts_match_vendored_json(self):
        vendored = json.loads(read("skills/vendored.json"))["packs"]
        rows = {}
        for line in read("docs/skills.md").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 3 and cells[0] in vendored:
                rows[cells[0]] = cells[1]
        self.assertEqual(set(rows), set(vendored), "every vendored pack needs a row in docs/skills.md")
        for pack, cell in rows.items():
            lead = re.match(r"(\d+) ", cell)
            if lead:
                self.assertEqual(int(lead.group(1)), len(vendored[pack]), pack)

    def test_skill_count_claims_do_not_overstate(self):
        total = len(list_skill_ids(ROOT))
        for rel in ["README.md", "CONTRIBUTING.md", *sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "docs").glob("*.md"))]:
            text = read(rel)
            for claim in re.findall(r"(\d+)\+ (?:specialist )?skills", text):
                self.assertLessEqual(int(claim), total, f"{rel}: {claim}+ skills")
        self.assertNotRegex(read("docs/architecture.md"), r"~100 specialist")
        self.assertIn("Six roles", read("docs/architecture.md"))


class ReferenceTests(unittest.TestCase):
    def test_playbooks_do_not_load_retired_alias_ids(self):
        aliases = json.loads(read("skills/aliases.json"))["aliases"]
        for path in sorted((ROOT / "references").rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for retired, target in aliases.items():
                with self.subTest(file=path.name, alias=retired):
                    self.assertNotIn(f"`{retired}`", text, f"use `{target}`")

    def test_cross_references_in_first_party_references_resolve(self):
        files = [ROOT / "references" / f for f in ("workspace-layer-architecture.md", "memory-first-handoff-protocol.md")]
        files += sorted((ROOT / "references" / "playbooks").glob("*.md"))
        link = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")
        code = re.compile(r"`((?:\.\./)[^`\s#]+|[A-Za-z0-9-]+-(?:playbook|checklist)\.md)`")
        missing = []
        for path in files:
            text = outside_fences(path.read_text(encoding="utf-8"))
            for target in link.findall(text):
                if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) and not (path.parent / target).resolve().exists():
                    missing.append(f"{path.name}: {target}")
            for target in code.findall(text):
                if not (path.parent / target).resolve().exists():
                    missing.append(f"{path.name}: {target}")
        self.assertEqual(missing, [])

    def test_orphan_router_is_gone_and_its_escalation_rule_lives_in_the_skill(self):
        self.assertFalse((ROOT / "references" / "always-on-model-router.md").exists())
        skill = read("skills/bosskuai-ai-model-selection/SKILL.md")
        self.assertIn("repeated failures of the cheaper model", skill)
        self.assertIn("auth, sessions or secrets", skill)

    def test_anti_ai_checklist_has_a_loader(self):
        name = "anti-ai-writing-checklist.md"
        self.assertTrue((ROOT / "references" / "checklists" / name).is_file())
        self.assertIn(name, read("references/playbooks/bosskuai-content-calendar-playbook.md"))

    def test_model_roster_says_when_it_was_checked_and_where_the_live_one_is(self):
        skill = read("skills/bosskuai-ai-model-selection/SKILL.md")
        self.assertRegex(skill, r"Checked 20\d\d-\d\d")
        self.assertIn("Load `claude-api` for the live roster", skill)


class LocalisationEvalTests(unittest.TestCase):
    @staticmethod
    def cases():
        rows = {}
        for path in sorted((ROOT / "skills" / "malaysia-localisation" / "evals").glob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    rows[row["id"]] = row
        return rows

    def test_repeated_letter_particles_are_forbidden_too(self):
        cases = self.cases()
        for case_id, row in cases.items():
            for pattern in row["checks"]["forbidden_regex"]:
                for particle in ("lah", "lor"):
                    with self.subTest(case=case_id, particle=particle):
                        self.assertNotRegex(pattern, rf"[(|]{particle}[|)]")
        self.assertRegex("Refund dah lulus lahh", "(?i)" + cases["over-01"]["checks"]["forbidden_regex"][0])
        self.assertRegex("okay lorr", "(?i)" + cases["reg-02"]["checks"]["forbidden_regex"][0])

    def test_reference_outputs_still_pass_the_checker(self):
        script = ROOT / "scripts" / "check_localisation_evals.py"
        spec = importlib.util.spec_from_file_location("check_localisation_evals", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cases = module.load_cases()
        report = module.check(cases, [{"id": k, "output": v["reference_output"]} for k, v in cases.items()])
        self.assertEqual(report["failures"], [])


if __name__ == "__main__":
    unittest.main()
