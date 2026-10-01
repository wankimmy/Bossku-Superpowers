import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from bossku.cli import main
from bossku.install import install_user, uninstall_user
from bossku.paths import claude_skills_dir, library_dir
from bossku.skills import (
    MAX_LEAN_DESCRIPTION_CHARS, _parse_frontmatter, load_lean, locate_skill, set_description, validate_lean,
)

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


def description_chars(folder: Path) -> int:
    total = 0
    for skill_md in folder.glob("*/SKILL.md"):
        total += len(str(_parse_frontmatter(skill_md.read_text(encoding="utf-8")).get("description", "")))
    return total


class LeanProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.home = Path(cls.tmp.name) / "home"
        cls.home.mkdir()
        cls.result = install_user(root=ROOT, home=cls.home, profile="lean")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_the_repository_lean_list_is_valid(self):
        self.assertEqual(validate_lean(ROOT), [])

    def test_hosts_list_only_the_lean_skills_with_short_descriptions(self):
        listed = set(load_lean(ROOT)["listed"])
        installed = {p.name for p in claude_skills_dir(self.home).iterdir() if p.is_dir()}
        self.assertEqual(installed, listed)
        for skill_md in claude_skills_dir(self.home).glob("*/SKILL.md"):
            description = str(_parse_frontmatter(skill_md.read_text(encoding="utf-8")).get("description", ""))
            self.assertLessEqual(len(description), MAX_LEAN_DESCRIPTION_CHARS, skill_md.parent.name)

    def test_the_listing_is_a_fraction_of_the_full_profile(self):
        with tempfile.TemporaryDirectory() as full_tmp:
            full_home = Path(full_tmp)
            install_user(root=ROOT, home=full_home, profile="full")
            lean_chars = description_chars(claude_skills_dir(self.home))
            full_chars = description_chars(claude_skills_dir(full_home))
        self.assertLess(lean_chars * 8, full_chars)

    def test_the_library_keeps_every_other_skill_whole(self):
        listed = set(load_lean(ROOT)["listed"])
        library = library_dir(self.home)
        self.assertGreater(self.result["library_count"], 150)
        self.assertFalse(listed & {p.name for p in library.iterdir() if p.is_dir()})
        source = (ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual((library / "seo-audit" / "SKILL.md").read_text(encoding="utf-8"), source)
        self.assertTrue((library.parent / "references").is_dir(), "library skills link to ../../references")

    def test_listed_skills_keep_their_body_and_only_lose_description_text(self):
        source = (ROOT / "skills" / "bosskuai-tdd-loop" / "SKILL.md").read_text(encoding="utf-8")
        installed = (claude_skills_dir(self.home) / "bosskuai-tdd-loop" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(installed.split("\n---\n", 1)[1], source.split("\n---\n", 1)[1])

    def test_show_prints_a_library_skill_that_the_host_does_not_list(self):
        kind, path = locate_skill("seo-audit", ROOT, self.home)
        self.assertEqual(kind, "library")
        code, output = run_cli("--home", str(self.home), "--root", str(ROOT), "skills", "show", "seo-audit")
        self.assertEqual(code, 0)
        self.assertIn("# skill: seo-audit (library)", output)
        self.assertIn("name: seo-audit", output)

    def test_show_caps_long_output_and_names_the_file(self):
        code, output = run_cli("--home", str(self.home), "--root", str(ROOT), "skills", "show", "taste-skill",
                               "--max-chars", "500")
        self.assertEqual(code, 0)
        self.assertIn("output cut at 500", output)
        self.assertLess(len(output), 1200)

    def test_show_rejects_unknown_skills(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = main(["--home", str(self.home), "--root", str(ROOT), "skills", "show", "no-such-skill"])
        self.assertEqual(code, 2)

    def test_find_reaches_library_skills_and_says_how_to_load_them(self):
        code, output = run_cli("--home", str(self.home), "--root", str(ROOT), "skills", "find",
                               "audit my website for SEO issues and fix the title tags")
        self.assertEqual(code, 0)
        selected = json.loads(output)["selection"]["selected"]
        self.assertTrue(selected)
        for row in selected:
            self.assertIn(row["access"], {"listed", "library"})
            self.assertTrue(Path(row["path"]).is_file())
            if row["access"] == "library":
                self.assertEqual(row["load_with"], f"bossku skills show {row['skill_id']}")

    def test_doctor_is_happy_with_a_lean_install(self):
        from bossku.doctor import gather_doctor_issues
        issues = [i for i in gather_doctor_issues(ROOT, self.home) if "validate" not in i]
        self.assertEqual(issues, [])


class GlobalFlagTests(unittest.TestCase):
    def test_home_given_before_the_subcommand_is_honored(self):
        with tempfile.TemporaryDirectory() as tmp:
            home, vault = Path(tmp) / "home", Path(tmp) / "vault"
            (home / ".bosskuai").mkdir(parents=True)
            vault.mkdir()
            (home / ".bosskuai" / "config.json").write_text(
                json.dumps({"memory_storage": "obsidian", "obsidian_vault": str(vault)}), encoding="utf-8")
            for argv in (["--home", str(home), "memory-path", "--project", str(Path(tmp) / "proj")],
                         ["memory-path", "--home", str(home), "--project", str(Path(tmp) / "proj")]):
                code, output = run_cli(*argv)
                self.assertEqual(code, 0)
                self.assertTrue(json.loads(output)["memory_dir"].startswith(str(vault.resolve())), argv)


class LeanLifecycleTests(unittest.TestCase):
    def test_a_plain_install_is_lean(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            code, output = run_cli("--home", str(home), "--root", str(ROOT), "install")
            self.assertEqual(code, 0)
            self.assertGreater(json.loads(output)["library_count"], 150)
            self.assertEqual(json.loads((home / ".bosskuai" / "config.json").read_text(encoding="utf-8"))["profile"], "lean")

    def test_update_keeps_the_profile_that_was_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            run_cli("--home", str(home), "--root", str(ROOT), "install", "--profile", "core")
            run_cli("--home", str(home), "--root", str(ROOT), "update")
            self.assertEqual(json.loads((home / ".bosskuai" / "config.json").read_text(encoding="utf-8"))["profile"], "core")
            self.assertFalse(library_dir(home).exists())

    def test_switching_to_full_removes_the_library_and_lists_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="lean")
            self.assertTrue(library_dir(home).is_dir())
            result = install_user(root=ROOT, home=home, profile="full")
            self.assertFalse(library_dir(home).exists())
            self.assertIsNone(result["library_dir"])
            self.assertGreater(result["claude_count"], 200)

    def test_switching_from_full_to_lean_prunes_the_long_tail_from_the_hosts(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="full")
            install_user(root=ROOT, home=home, profile="lean")
            installed = {p.name for p in claude_skills_dir(home).iterdir() if p.is_dir()}
            self.assertEqual(installed, set(load_lean(ROOT)["listed"]))
            self.assertTrue((library_dir(home) / "seo-audit" / "SKILL.md").is_file())

    def test_uninstall_removes_the_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="lean")
            uninstall_user(root=ROOT, home=home)
            self.assertFalse(library_dir(home).exists())
            self.assertEqual([p for p in claude_skills_dir(home).iterdir() if p.is_dir()], [])

    def test_update_keeps_the_chosen_profile(self):
        from bossku.install import update_user
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile="lean")
            update_user(root=ROOT, home=home)
            installed = {p.name for p in claude_skills_dir(home).iterdir() if p.is_dir()}
            self.assertEqual(installed, set(load_lean(ROOT)["listed"]))


class SetDescriptionTests(unittest.TestCase):
    def rewrite(self, text: str, new: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(text, encoding="utf-8")
            set_description(path, new)
            return path.read_text(encoding="utf-8")

    def test_replaces_a_folded_block_scalar_and_keeps_neighbouring_keys(self):
        text = "---\nname: x\ndescription: >-\n  long text\n  more text\nlicense: MIT\n---\n\n# Body\n"
        out = self.rewrite(text, "Short: with a colon.")
        front = _parse_frontmatter(out)
        self.assertEqual(front["description"], "Short: with a colon.")
        self.assertEqual(front["license"], "MIT")
        self.assertEqual(front["name"], "x")
        self.assertTrue(out.endswith("# Body\n"))

    def test_replaces_a_quoted_single_line_description(self):
        out = self.rewrite('---\nname: x\ndescription: "Old \\"quoted\\" text"\n---\n\nBody\n', "New")
        self.assertEqual(_parse_frontmatter(out)["description"], "New")

    def test_files_without_frontmatter_are_left_alone(self):
        self.assertEqual(self.rewrite("# just a heading\n", "New"), "# just a heading\n")


class ValidateLeanTests(unittest.TestCase):
    def repo(self, tmp: str, lean: dict) -> Path:
        root = Path(tmp)
        for sid in ("bosskuai-skill-finder", "alpha"):
            folder = root / "skills" / sid
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                f"---\nname: {sid}\ndescription: A sufficiently long description for {sid} to pass checks.\n---\n",
                encoding="utf-8")
        (root / "skills" / "lean.json").write_text(json.dumps(lean), encoding="utf-8")
        return root

    def test_a_valid_config_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp, {"listed": ["bosskuai-skill-finder", "alpha"], "descriptions": {}})
            self.assertEqual(validate_lean(root), [])

    def test_missing_finder_unknown_skill_and_long_description_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp, {"listed": ["alpha", "ghost"],
                                   "descriptions": {"alpha": "x" * 200, "beta": "Not listed but described."}})
            text = "\n".join(validate_lean(root))
            self.assertIn("bosskuai-skill-finder must be listed", text)
            self.assertIn("listed skill has no folder: ghost", text)
            self.assertIn("alpha description is 200 chars", text)
            self.assertIn("description for a skill that is not listed: beta", text)


if __name__ == "__main__":
    unittest.main()
