import tempfile
import unittest
from pathlib import Path

from bossku.doctor import gather_doctor_issues
from bossku.init_project import init_project
from bossku.validate import claude_imports_agents_md, omp_imports_agents_md


ROOT = Path(__file__).resolve().parents[1]


class InstructionImportTests(unittest.TestCase):
    def test_code_examples_do_not_activate_imports(self):
        for check, import_line in (
            (claude_imports_agents_md, "@AGENTS.md"),
            (omp_imports_agents_md, "@../AGENTS.md"),
        ):
            examples = (
                f"`{import_line}`\n",
                f"Use {import_line} to activate.\n",
                f"```markdown\n{import_line}\n```\n",
                f"~~~markdown\n{import_line}\n~~~\n",
                f"````markdown\n```\n{import_line}\n````\n",
                f"```markdown\n~~~\n{import_line}\n```\n",
                f"```markdown\n{import_line}\n",
                f"    {import_line}\n",
                f"\t{import_line}\n",
            )
            for text in examples:
                with self.subTest(check=check.__name__, text=text):
                    self.assertFalse(check(text))

    def test_real_import_after_closed_fence_is_detected(self):
        for check, import_line in (
            (claude_imports_agents_md, "@AGENTS.md"),
            (omp_imports_agents_md, "@../AGENTS.md"),
        ):
            for fence in ("```", "~~~~", "   ```"):
                text = f"{fence}markdown\nexample\n{fence}\n{import_line}\n"
                with self.subTest(check=check.__name__, fence=fence):
                    self.assertTrue(check(text))
            self.assertTrue(check(f"   {import_line}  \n"))

    def test_fence_with_trailing_text_does_not_close_example(self):
        text = "```markdown\n``` not a closing fence\n@AGENTS.md\n```\n"
        self.assertFalse(claude_imports_agents_md(text))

    def test_init_repairs_documented_import_and_preserves_existing_text(self):
        examples = (
            "`@AGENTS.md`\n",
            "Use @AGENTS.md to activate.\n",
            "```markdown\n@AGENTS.md\n```\n",
            "~~~markdown\n@AGENTS.md\n~~~\n",
        )
        for example in examples:
            with self.subTest(example=example), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                claude = project / "CLAUDE.md"
                original = "# My instructions\n\n" + example + "\nKeep this rule.\n"
                claude.write_text(original, encoding="utf-8")
                omp = project / ".omp" / "AGENTS.md"
                omp.parent.mkdir()
                omp_original = original.replace("@AGENTS.md", "@../AGENTS.md")
                omp.write_text(omp_original, encoding="utf-8")

                init_project(project, root=ROOT)
                self.assertEqual(claude.read_text(encoding="utf-8"), "@AGENTS.md\n\n" + original)
                self.assertEqual(omp.read_text(encoding="utf-8"), "@../AGENTS.md\n\n" + omp_original)
                before = claude.read_bytes(), omp.read_bytes()
                init_project(project, root=ROOT)
                self.assertEqual((claude.read_bytes(), omp.read_bytes()), before)
                issues = gather_doctor_issues(ROOT, project, project=project)
                self.assertFalse(any("must include bare" in issue for issue in issues))

    def test_init_preserves_live_import_without_rewriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            claude = project / "CLAUDE.md"
            original = "# Project\n\n@AGENTS.md\n\nKeep this rule.\n"
            claude.write_text(original, encoding="utf-8")
            init_project(project, root=ROOT)
            self.assertEqual(claude.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
