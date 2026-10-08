import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from bossku import vault
from bossku.memory import save_user_config


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


ENTRY_A = "## 2026-09-01 10:00 UTC\n\nUse integer cents for money."
ENTRY_B = "## 2026-09-02 10:00 UTC\n\nTests live next to the code."


MOVES = {"02dd35b7f2": "_archive/unsorted/02dd35b7f2", "web-legacy": "Shop/repos/web", "se": "_global/notes/se"}


class World:
    """A fake home, vault, project root with sub-repos, and Claude auto-memory."""

    def __init__(self, tmp: str, root_name: str = "Shop", **config):
        self.tmp = Path(tmp)
        self.home = self.tmp / "home"
        self.vault = self.tmp / "vault"
        self.root = self.tmp / "work" / root_name
        (self.vault / "BosskuAI").mkdir(parents=True)
        (self.root / "api").mkdir(parents=True)
        (self.root / "web").mkdir()
        self.cfg = {"obsidian_vault": str(self.vault), "memory_storage": "obsidian",
                    "memory_project_roots": [str(self.root)], **config}
        save_user_config(self.cfg, self.home)
        self.base = self.vault / "BosskuAI"

    def claude(self, folder: Path | str) -> Path:
        return self.home / ".claude" / "projects" / vault._slug(folder) / "memory"


class SyncTests(unittest.TestCase):
    def test_auto_memory_rules_and_legacy_notes_are_mirrored_and_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.claude(w.root) / "MEMORY.md", "- prefers short answers")
            write(w.claude(w.root / "api") / "api.md", "api facts")
            write(w.home / ".claude" / "CLAUDE.md", "Always run the tests.")
            write(w.root / "AGENTS.md", "Project rules.")
            write(w.root / ".bossku" / "memory" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
            result = vault.sync(w.root, home=w.home, force=True)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["namespace"], "Shop")
            self.assertIn("prefers short answers", (w.base / "Shop" / "claude-memory" / "root" / "MEMORY.md").read_text(encoding="utf-8"))
            self.assertTrue((w.base / "Shop" / "claude-memory" / "api" / "api.md").is_file())
            self.assertIn("Always run the tests.", (w.base / "_global" / "rules" / "claude-CLAUDE.md").read_text(encoding="utf-8"))
            self.assertTrue((w.base / "Shop" / "rules" / "AGENTS.md").is_file())
            self.assertTrue((w.base / "Shop" / "imported" / "repo-memory" / "decisions.md").is_file())
            index = (w.base / "Index.md").read_text(encoding="utf-8")
            self.assertIn("[[Shop/claude-memory/root/MEMORY", index)
            self.assertIn("## Global", index)

    def test_a_second_sync_changes_nothing_and_a_changed_source_is_picked_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            note = write(w.claude(w.root) / "MEMORY.md", "one")
            self.assertTrue(vault.sync(w.root, home=w.home, force=True)["changed"])
            self.assertEqual(vault.sync(w.root, home=w.home, force=True)["changed"], [])
            note.write_text("two", encoding="utf-8")
            again = vault.sync(w.root, home=w.home, force=True)
            self.assertIn("Shop/claude-memory/root/MEMORY.md", [c.replace("\\", "/") for c in again["changed"]])

    def test_a_sibling_folder_with_a_longer_name_is_not_part_of_the_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            sibling = w.root.parent / (w.root.name + "-old")
            sibling.mkdir()
            write(w.claude(sibling) / "MEMORY.md", "another project's note")
            vault.sync(w.root, home=w.home, force=True)
            self.assertFalse((w.base / "Shop" / "claude-memory" / "old").exists())

    def test_sync_is_throttled_per_project_unless_forced(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            other = w.tmp / "work" / "Blog"
            other.mkdir()
            write(w.claude(other) / "MEMORY.md", "blog note")
            vault.sync(w.root, home=w.home, force=True)
            self.assertEqual(vault.sync(w.root, home=w.home)["status"], "throttled")
            self.assertEqual(vault.sync(other, home=w.home)["status"], "ok")          # another project is not held back
            self.assertTrue((w.base / "Blog" / "claude-memory" / "root" / "MEMORY.md").is_file())

    def test_a_namespace_cannot_leave_the_vault_and_matches_where_notes_are_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            save_user_config({**w.cfg, "memory_project_namespaces": {str(w.root): "../../escape ns"}}, w.home)
            write(w.root / "AGENTS.md", "rules")
            result = vault.sync(w.root, home=w.home, force=True)
            self.assertEqual(result["namespace"], "------escape-ns")
            self.assertTrue((w.base / "------escape-ns" / "rules" / "AGENTS.md").is_file())
            self.assertFalse((w.tmp / "escape ns").exists())

    def test_a_missing_bosskuai_folder_is_not_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            (w.base).rmdir()
            self.assertEqual(vault.sync(w.root, home=w.home, force=True)["status"], "ok")
            self.assertEqual(vault.plan_tidy(home=w.home), [])

    def test_secrets_are_redacted_in_the_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.home / ".claude" / "CLAUDE.md",
                  "token: sk-ant-abcdefghijklmnopqrstuvwxyz0123456789\nuse sk-proj-abcdefghijklmnopqrstuvwxyz0123456789 here")
            vault.sync(w.root, home=w.home, force=True)
            copy = (w.base / "_global" / "rules" / "claude-CLAUDE.md").read_text(encoding="utf-8")
            self.assertNotIn("sk-ant-abcdefghijklmnop", copy)
            self.assertNotIn("sk-proj-abcdefghijklmnop", copy)

    def test_an_edited_copy_is_kept_when_the_original_changes_and_when_the_state_is_lost(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            rules = write(w.root / "AGENTS.md", "version one")
            vault.sync(w.root, home=w.home, force=True)
            copy = w.base / "Shop" / "rules" / "AGENTS.md"
            copy.write_text(copy.read_text(encoding="utf-8") + "\nMY OWN EDIT\n", encoding="utf-8")
            vault.sync(w.root, home=w.home, force=True)
            self.assertIn("MY OWN EDIT", copy.read_text(encoding="utf-8"))                 # original unchanged: left alone
            rules.write_text("version two", encoding="utf-8")
            vault.sync(w.root, home=w.home, force=True)
            self.assertIn("version two", copy.read_text(encoding="utf-8"))
            kept = list(copy.parent.glob("AGENTS.md.conflict*.md"))
            self.assertEqual(len(kept), 1)
            self.assertIn("MY OWN EDIT", kept[0].read_text(encoding="utf-8"))
            (w.home / ".bosskuai" / "vault-sync-state.json").write_text("{corrupt", encoding="utf-8")
            copy.write_text(copy.read_text(encoding="utf-8") + "\nSECOND EDIT\n", encoding="utf-8")
            rules.write_text("version three", encoding="utf-8")
            vault.sync(w.root, home=w.home, force=True)
            self.assertTrue(any("SECOND EDIT" in p.read_text(encoding="utf-8") for p in copy.parent.glob("AGENTS.md.conflict*.md")))

    def test_no_vault_means_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            save_user_config({}, home)
            self.assertEqual(vault.sync(Path(tmp), home=home)["status"], "skipped")


class MergeTests(unittest.TestCase):
    def test_merge_keeps_every_entry_once_oldest_first(self):
        a = "# Decisions\n\n" + ENTRY_B + "\n"
        b = "# Decisions\n\n" + ENTRY_A + "\n\n" + ENTRY_B + "\n"
        merged = vault.merge_notes(a, b)
        self.assertEqual(merged.count("Tests live next to the code."), 1)
        self.assertLess(merged.index("integer cents"), merged.index("next to the code"))

    def test_text_without_a_dated_entry_is_kept_and_not_repeated(self):
        merged = vault.merge_notes("# Decisions\n\n" + ENTRY_A + "\n", "# Decisions\n\nINTRO about money\n\n" + ENTRY_B + "\n")
        self.assertIn("INTRO about money", merged)
        self.assertEqual(vault.merge_notes(merged, "# Decisions\n\nINTRO about money\n").count("INTRO about money"), 1)
        plain = vault.merge_notes("# Notes\n\n" + ENTRY_A + "\n", "PLAIN-LEGACY note with no headings\n")
        self.assertIn("PLAIN-LEGACY note with no headings", plain)
        self.assertIn("integer cents", plain)


class TidyTests(unittest.TestCase):
    def build(self, w: World) -> None:
        write(w.base / "Shop" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
        write(w.base / "Shop" / "decisions.md.conflict.md", "# Decisions\n\nold copy\n")
        write(w.base / "api" / "decisions.md", "# Decisions\n\n" + ENTRY_B + "\n")
        write(w.base / "api" / "decisions.md.conflict.md", "# Decisions\n\nold api copy\n")
        write(w.base / "02dd35b7f2" / "learnings.md", "# Learnings\n\nbenchmark junk\n")
        write(w.base / "g-p-6aa3a5039a348191aa34f447d515df42" / "project.md", "# Projects\n\nsomething\n")
        write(w.base / "se" / "decisions.md", "# Decisions\n\nsomeone's three-letter project\n")
        write(w.base / "decade2025" / "learnings.md", "# Learnings\n\na real project that looks like a hash\n")
        write(w.base / "web-legacy" / "learnings.md", "# Learnings\n\na separate project named like a sub-repo\n")
        write(w.base / "other-project" / "learnings.md", "# Learnings\n\nkeep me\n")
        write(w.base / "Shop" / "learnings.conflicts.md", "# Learnings\n\na real note with an unlucky name\n")
        (w.base / "hel").mkdir()
        (w.base / "hel-2").mkdir()
        write(w.root / "web" / ".bossku" / "memory" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")

    def test_the_plan_sorts_each_folder_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp, vault_folder_moves=MOVES)
            self.build(w)
            before = sorted(p.relative_to(w.base).as_posix() for p in w.base.rglob("*"))
            plan = vault.plan_tidy(home=w.home)
            self.assertEqual(sorted(p.relative_to(w.base).as_posix() for p in w.base.rglob("*")), before)
            by = {(s["action"], Path(s["source"]).name, Path(s["source"]).parent.name) for s in plan}
            self.assertIn(("merge", "decisions.md", "api"), by)
            self.assertIn(("archive", "decisions.md.conflict.md", "Shop"), by)
            self.assertIn(("move", "learnings.md", "02dd35b7f2"), by)               # you asked for it
            self.assertIn(("merge", "learnings.md", "web-legacy"), by)
            self.assertIn(("move", "decisions.md", "se"), by)
            self.assertIn(("move", "project.md", "g-p-6aa3a5039a348191aa34f447d515df42"), by)
            self.assertIn(("remove-empty-folder", "hel", w.base.name), by)
            self.assertIn(("import", "decisions.md", "memory"), by)
            touched = [Path(s["source"]) for s in plan]
            for left_alone in ("other-project", "decade2025"):
                self.assertFalse([t for t in touched if t.parent.name == left_alone], left_alone)
            self.assertFalse([t for t in touched if t.name == "learnings.conflicts.md" or t == w.base / "Shop" / "decisions.md"])

    def test_folders_are_left_alone_unless_their_name_matches_exactly_or_you_say_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            self.build(w)
            touched = " ".join(s["source"] for s in vault.plan_tidy(home=w.home))
            for name in ("02dd35b7f2", "web-legacy", "decade2025", f"BosskuAI{Path('/').anchor}se"):
                self.assertNotIn(name, touched, name)
            self.assertNotIn(str(w.base / "se"), touched)

    def test_a_move_cannot_leave_the_bosskuai_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp, vault_folder_moves={"se": "../outside", "other-project": "_unsorted/../../outside"})
            self.build(w)
            plan = vault.plan_tidy(home=w.home)
            self.assertFalse([s for s in plan if Path(s["source"]).parent.name in ("se", "other-project")])

    def test_a_three_letter_project_keeps_its_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp, "TMS")
            write(w.base / "TMS" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
            vault.apply_tidy(vault.plan_tidy(home=w.home), home=w.home)
            self.assertIn("integer cents", (w.base / "TMS" / "decisions.md").read_text(encoding="utf-8"))

    def test_a_name_shared_by_two_roots_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            blog = w.tmp / "work" / "Blog"
            (blog / "api").mkdir(parents=True)
            save_user_config({**w.cfg, "memory_project_roots": [str(w.root), str(blog)]}, w.home)
            write(w.base / "api" / "learnings.md", "# Learnings\n\nwhich api?\n")
            self.assertNotIn(str(w.base / "api"), " ".join(s["source"] for s in vault.plan_tidy(home=w.home)))

    def test_applying_loses_no_note_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp, vault_folder_moves=MOVES)
            self.build(w)
            result = vault.apply_tidy(vault.plan_tidy(home=w.home), home=w.home)
            self.assertEqual(result["status"], "ok")
            with zipfile.ZipFile(result["backup"]) as archive:
                self.assertTrue(any(n.endswith("02dd35b7f2/learnings.md") for n in archive.namelist()))
            repo = (w.base / "Shop" / "repos" / "api" / "decisions.md").read_text(encoding="utf-8")
            self.assertIn("Tests live next to the code.", repo)
            web = (w.base / "Shop" / "repos" / "web" / "decisions.md").read_text(encoding="utf-8")
            self.assertIn("integer cents", web)                                       # imported from the repo's .bossku
            self.assertTrue((w.base / "_archive" / "conflicts" / "api" / "decisions.md.conflict.md").is_file())
            self.assertTrue((w.base / "_archive" / "unsorted" / "02dd35b7f2" / "learnings.md").is_file())    # via vault_folder_moves
            self.assertTrue((w.base / "_unsorted" / "g-p-6aa3a5039a348191aa34f447d515df42" / "project.md").is_file())
            self.assertTrue((w.base / "_global" / "notes" / "se" / "decisions.md").is_file())
            self.assertIn("separate project named like a sub-repo", (w.base / "Shop" / "repos" / "web" / "learnings.md").read_text(encoding="utf-8"))
            for kept in ("decade2025", "other-project"):
                self.assertTrue((w.base / kept / "learnings.md").is_file(), kept)
            self.assertTrue((w.base / "Shop" / "learnings.conflicts.md").is_file())
            self.assertFalse((w.base / "hel").exists())
            self.assertFalse((w.base / "api").exists())                               # nothing left behind
            self.assertTrue((w.root / "web" / ".bossku" / "memory" / "decisions.md").is_file())   # the original stays put
            self.assertEqual([s for s in vault.plan_tidy(home=w.home) if s["action"] != "import"], [])

    def test_applying_twice_never_overwrites_an_archived_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.base / "api" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
            write(w.base / "api" / "nested" / "decisions.md", "# Decisions\n\n" + ENTRY_B + "\n")
            vault.apply_tidy(vault.plan_tidy(home=w.home), home=w.home)
            write(w.base / "api" / "decisions.md", "# Decisions\n\n## 2026-09-03 10:00 UTC\n\nthird\n")
            vault.apply_tidy(vault.plan_tidy(home=w.home), home=w.home)
            archived = "".join(p.read_text(encoding="utf-8") for p in (w.base / "_archive" / "merged").rglob("*.md"))
            for text in ("integer cents", "next to the code", "third"):
                self.assertIn(text, archived)

    def test_a_note_saved_in_another_encoding_is_still_merged(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.base / "Shop" / "repos" / "api" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
            (w.base / "api").mkdir()
            (w.base / "api" / "decisions.md").write_bytes("# Decisions\n\n## 2026-09-04 10:00 UTC\n\ncaf\xe9 note\n".encode("cp1252"))
            write(w.base / "web" / "learnings.md", "# Learnings\n\nsomething\n")
            result = vault.apply_tidy(vault.plan_tidy(home=w.home), home=w.home)
            self.assertEqual(result["status"], "ok")
            self.assertIn("café note", (w.base / "Shop" / "repos" / "api" / "decisions.md").read_text(encoding="utf-8"))
            self.assertTrue((w.base / "Shop" / "repos" / "web" / "learnings.md").is_file())

    def test_two_backups_in_a_row_keep_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.base / "Shop" / "decisions.md", "x")
            first, second = vault.backup(w.base, w.home), vault.backup(w.base, w.home)
            self.assertNotEqual(first, second)
            self.assertTrue(first.is_file() and second.is_file())


if __name__ == "__main__":
    unittest.main()
