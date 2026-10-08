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


class World:
    """A fake home, vault, project root with sub-repos, and Claude auto-memory."""

    def __init__(self, tmp: str):
        self.tmp = Path(tmp)
        self.home = self.tmp / "home"
        self.vault = self.tmp / "vault"
        self.root = self.tmp / "work" / "Shop"
        (self.vault / "BosskuAI").mkdir(parents=True)
        (self.root / "api").mkdir(parents=True)
        (self.root / "web").mkdir()
        save_user_config({"obsidian_vault": str(self.vault), "memory_storage": "obsidian",
                          "memory_project_roots": [str(self.root)]}, self.home)
        self.base = self.vault / "BosskuAI"


class SyncTests(unittest.TestCase):
    def test_auto_memory_rules_and_legacy_notes_are_mirrored_and_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            claude = w.home / ".claude" / "projects" / vault._slug(w.root) / "memory"
            write(claude / "MEMORY.md", "- prefers short answers")
            sub = w.home / ".claude" / "projects" / (vault._slug(w.root) + "-api") / "memory"
            write(sub / "api.md", "api facts")
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
            note = write(w.home / ".claude" / "projects" / vault._slug(w.root) / "memory" / "MEMORY.md", "one")
            self.assertTrue(vault.sync(w.root, home=w.home, force=True)["changed"])
            self.assertEqual(vault.sync(w.root, home=w.home, force=True)["changed"], [])
            note.write_text("two", encoding="utf-8")
            again = vault.sync(w.root, home=w.home, force=True)
            self.assertIn("Shop\\claude-memory\\root\\MEMORY.md".replace("\\", "/"), [c.replace("\\", "/") for c in again["changed"]])

    def test_sync_is_throttled_unless_forced(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            vault.sync(w.root, home=w.home, force=True)
            self.assertEqual(vault.sync(w.root, home=w.home)["status"], "throttled")

    def test_secrets_are_redacted_in_the_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            write(w.home / ".claude" / "CLAUDE.md", "token: sk-ant-abcdefghijklmnopqrstuvwxyz0123456789")
            vault.sync(w.root, home=w.home, force=True)
            copy = (w.base / "_global" / "rules" / "claude-CLAUDE.md").read_text(encoding="utf-8")
            self.assertNotIn("sk-ant-abcdefghijklmnop", copy)

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


class TidyTests(unittest.TestCase):
    def build(self, w: World) -> None:
        write(w.base / "Shop" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")
        write(w.base / "Shop" / "decisions.md.conflict.md", "# Decisions\n\nold copy\n")
        write(w.base / "api" / "decisions.md", "# Decisions\n\n" + ENTRY_B + "\n")
        write(w.base / "api" / "decisions.md.conflict.md", "# Decisions\n\nold api copy\n")
        write(w.base / "02dd35b7f2" / "learnings.md", "# Learnings\n\nbenchmark junk\n")
        write(w.base / "g-p-6aa3a5039a348191aa34f447d515df42" / "project.md", "# Projects\n\nsomething\n")
        write(w.base / "se" / "decisions.md", "# Decisions\n\nglobal settings changed\n")
        write(w.base / "other-project" / "learnings.md", "# Learnings\n\nkeep me\n")
        (w.base / "hel").mkdir()
        (w.base / "hel-2").mkdir()
        write(w.root / "web" / ".bossku" / "memory" / "decisions.md", "# Decisions\n\n" + ENTRY_A + "\n")

    def test_the_plan_sorts_each_folder_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            self.build(w)
            before = sorted(p.relative_to(w.base).as_posix() for p in w.base.rglob("*"))
            plan = vault.plan_tidy(home=w.home)
            self.assertEqual(sorted(p.relative_to(w.base).as_posix() for p in w.base.rglob("*")), before)
            by = {(s["action"], Path(s["source"]).name, Path(s["source"]).parent.name) for s in plan}
            self.assertIn(("merge", "decisions.md", "api"), by)
            self.assertIn(("archive", "decisions.md.conflict.md", "Shop"), by)
            self.assertIn(("archive", "learnings.md", "02dd35b7f2"), by)
            self.assertIn(("move", "decisions.md", "se"), by)
            self.assertIn(("remove-empty-folder", "hel", w.base.name), by)
            self.assertIn(("import", "decisions.md", "memory"), by)
            self.assertNotIn("other-project", " ".join(s["source"] for s in plan))   # a normal project is left alone

    def test_applying_loses_no_note_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
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
            self.assertTrue((w.base / "_archive" / "unsorted" / "02dd35b7f2" / "learnings.md").is_file())
            self.assertTrue((w.base / "_unsorted" / "se" / "decisions.md").is_file())
            self.assertTrue((w.base / "other-project" / "learnings.md").is_file())
            self.assertFalse((w.base / "hel").exists())
            self.assertFalse((w.base / "api").exists())                               # nothing left behind
            self.assertTrue((w.root / "web" / ".bossku" / "memory" / "decisions.md").is_file())   # the original stays put
            self.assertEqual([s for s in vault.plan_tidy(home=w.home) if s["action"] != "import"], [])


if __name__ == "__main__":
    unittest.main()
