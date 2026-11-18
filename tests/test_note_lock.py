"""Two writers of one notes file take turns.

On Windows an append is "seek to the end, then write". Two `bossku remember` calls of one kind at the same moment
could pick the same end, and one note then overwrote the other. Both also saw an empty file and both wrote its title.

A real race is luck, so these tests force the overlap: the first writer is stopped between its "is the file empty"
check and its write, and the second writer, a separate process as in real use, is sent in then.
"""
import contextlib
import errno
import io
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.filelock import locked
from bossku.learn import apply_intent, show, store_dir
from bossku.memory import remember, save_user_config

ROOT = Path(__file__).resolve().parents[1]

# The second writer. It says "waiting" each time it sleeps for its turn and "saved" once its note is in the file,
# so the first line tells which came first, with no guess about timing.
SECOND_WRITER = """
import sys, time
from pathlib import Path
from bossku.memory import remember
nap = time.sleep
def sleep(seconds):
    print("waiting", flush=True)
    nap(seconds)
time.sleep = sleep
remember(Path(sys.argv[1]), "learning", sys.argv[2], home=Path(sys.argv[3]))
print("saved", flush=True)
"""


@contextlib.contextmanager
def first_writer_stopped_before_its_write(test, write, filename):
    """Start `write` in a thread and stop it right after it has seen that `filename` is empty. Leaving lets it go on."""
    seen_empty, go_on = threading.Event(), threading.Event()
    real_stat = Path.stat

    def stat(self, *args, **kwargs):
        result = real_stat(self, *args, **kwargs)
        if self.name == filename and not seen_empty.is_set():
            seen_empty.set()
            go_on.wait(120)      # longer than the second writer is given, so only the test lets the first one go
        return result

    with mock.patch.object(Path, "stat", stat), ThreadPoolExecutor(max_workers=1) as pool:
        first = pool.submit(write)
        try:
            test.assertTrue(seen_empty.wait(10), "the first writer never checked whether the notes file is empty")
            yield
        finally:
            go_on.set()
        first.result(30)


class TwoWritersTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.project = Path(tmp.name) / "repo"
        (self.project / ".git").mkdir(parents=True)
        self.vault = Path(tmp.name) / "vault"
        self.vault.mkdir()

    def second_writer(self, note):
        env = {**os.environ, "PYTHONPATH": str(ROOT), "HOME": str(self.home), "USERPROFILE": str(self.home)}
        child = subprocess.Popen([sys.executable, "-c", SECOND_WRITER, str(self.project), note, str(self.home)],
                                 cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        def stop():
            child.kill()
            child.communicate()

        self.addCleanup(stop)
        stuck = threading.Timer(60, child.kill)      # a child that never answers must not hang the suite
        stuck.start()
        self.addCleanup(stuck.cancel)
        return child

    def both_notes_land(self, notes_file):
        def first():
            remember(self.project, "learning", "FIRST note", home=self.home)

        with first_writer_stopped_before_its_write(self, first, "learnings.md"):
            child = self.second_writer("SECOND note")
            first_line = child.stdout.readline().strip()
            while_stopped = notes_file.read_text(encoding="utf-8")
        out, err = child.communicate(timeout=60)
        self.assertEqual(child.returncode, 0, err)
        self.assertEqual(first_line, "waiting",
                         "the second writer wrote while the first was between its check and its write: " + err)
        self.assertEqual(while_stopped, "", "the second writer had written before the first was let go")
        text = notes_file.read_text(encoding="utf-8")
        self.assertEqual(text.count("# Learnings"), 1, text)
        self.assertLess(text.index("FIRST note"), text.index("SECOND note"), text)
        self.assertEqual(text.count("\n## "), 2, text)
        # The bytes are what a plain text append has always written: the platform's line endings, nothing else.
        self.assertEqual(notes_file.read_bytes(), text.replace("\n", os.linesep).encode("utf-8"))

    def test_repo_notes_keep_both_notes_and_one_title(self):
        notes_file = self.project / ".bossku" / "memory" / "learnings.md"
        self.both_notes_land(notes_file)
        self.assertEqual(sorted(p.name for p in notes_file.parent.iterdir()), ["learnings.md", "sync-state.json"])

    def test_vault_notes_keep_both_notes_and_one_title(self):
        save_user_config({"obsidian_vault": str(self.vault), "memory_storage": "obsidian"}, self.home)
        notes_file = self.vault / "BosskuAI" / "repo" / "learnings.md"
        self.both_notes_land(notes_file)
        # Nothing but the note is left in the vault: no lock file for Obsidian or OneDrive to pick up.
        self.assertEqual([p.name for p in notes_file.parent.iterdir()], ["learnings.md"])

    def test_a_writer_that_never_gets_its_turn_fails_loudly_and_writes_nothing(self):
        def first():
            remember(self.project, "learning", "FIRST note", home=self.home)

        errors = io.StringIO()
        with first_writer_stopped_before_its_write(self, first, "learnings.md"), \
                mock.patch("bossku.filelock.LOCK_WAIT", 0.2):
            with self.assertRaisesRegex(TimeoutError, "nothing was written"):
                remember(self.project, "learning", "SECOND note", home=self.home)
            with contextlib.redirect_stderr(errors):       # the command an agent runs says so and exits non-zero
                code = main(["remember", "--home", str(self.home), "--project", str(self.project),
                             "--kind", "learning", "THIRD note"])
        self.assertEqual(code, 2)
        self.assertRegex(errors.getvalue(), r"^error: .*learnings\.md is still locked .*nothing was written")
        text = (self.project / ".bossku" / "memory" / "learnings.md").read_text(encoding="utf-8")
        self.assertIn("FIRST note", text)
        self.assertNotIn("SECOND note", text)
        self.assertNotIn("THIRD note", text)

    def test_a_file_system_without_locks_still_saves_the_note(self):
        with mock.patch("bossku.filelock._lock", side_effect=OSError(errno.ENOLCK, "No locks available")):
            result = remember(self.project, "learning", "Saved without a lock.", home=self.home)
        self.assertIs(result["saved"], True)
        self.assertIn("Saved without a lock.", Path(result["file"]).read_text(encoding="utf-8"))


class LedgerTests(unittest.TestCase):
    """The ledger of a learned skill is appended the same way, by `bossku learn show` and `bossku learn apply`."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.project = Path(tmp.name) / "proj"
        self.project.mkdir()
        apply_intent(self.project, {
            "action": "create", "name": "demo-skill", "reason": "a lesson", "evidence": "user: do it this way",
            "body": "---\nname: demo-skill\ndescription: Use when testing.\ncategory: test\nlearned: true\n---\n\n"
                    "# Demo\n\nRule.\n"}, home=self.home)
        self.ledger = store_dir(self.project, home=self.home) / "demo-skill" / "ledger.jsonl"

    def uses(self):
        return self.ledger.read_text(encoding="utf-8").count('"event": "use"')

    def test_a_ledger_line_waits_for_its_turn_and_fails_loudly_when_it_never_comes(self):
        with locked(self.ledger), mock.patch("bossku.filelock.LOCK_WAIT", 0.2):
            with self.assertRaisesRegex(TimeoutError, "nothing was written"):
                show(self.project, "demo-skill", home=self.home)
            self.assertEqual(self.uses(), 0)                      # and a reader is not locked out meanwhile
        show(self.project, "demo-skill", home=self.home)          # the lock is free again once the block ends
        self.assertEqual(self.uses(), 1)
        self.assertNotIn(b"\r", self.ledger.read_bytes())         # the ledger keeps its plain "\n" line ends
        self.assertEqual(sorted(p.name for p in self.ledger.parent.iterdir()), ["SKILL.md", "ledger.jsonl", "references"])


if __name__ == "__main__":
    unittest.main()
