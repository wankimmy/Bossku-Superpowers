"""Two saves update .bossku/memory/sync-state.json one at a time, and a broken one does not stop the next save.

Every `bossku remember` in repo storage reads, changes and rewrites this one file, whatever the kind. Two saves at
the same moment could read it half rewritten (JSONDecodeError after the note was saved, so an agent saved the note
again), or write over each other and leave a file that broke every later save.

A real race is luck, so these tests force the overlap: the first writer is stopped in the middle of its rewrite, and
the second writer, a separate process as in real use, is sent in then.
"""
import contextlib
import io
import json
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
from bossku.memory import remember, save_user_config

ROOT = Path(__file__).resolve().parents[1]

# The second writer saves a decision. It says "waiting" each time it sleeps for its turn and "saved" once it is done,
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
remember(Path(sys.argv[1]), "decision", sys.argv[2], home=Path(sys.argv[3]))
print("saved", flush=True)
"""


@contextlib.contextmanager
def first_writer_stopped_mid_rewrite(test, write, emptied):
    """Run `write` in a thread and stop it when it starts to rewrite sync-state.json. Leaving lets it go on.

    With `emptied`, the file is emptied first, as a real rewrite does for a moment before the new text is in.
    """
    reached, go_on = threading.Event(), threading.Event()
    real_write_text = Path.write_text

    def write_text(self, data, *args, **kwargs):
        if self.name == "sync-state.json" and not reached.is_set():
            if emptied:
                self.open("w").close()
            reached.set()
            go_on.wait(120)      # longer than the second writer is given, so only the test lets the first one go
        return real_write_text(self, data, *args, **kwargs)

    with mock.patch.object(Path, "write_text", write_text), ThreadPoolExecutor(max_workers=1) as pool:
        first = pool.submit(write)
        try:
            test.assertTrue(reached.wait(10), "the first writer never rewrote sync-state.json")
            yield
        finally:
            go_on.set()
        first.result(30)


class SyncStateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.project = Path(tmp.name) / "repo"
        (self.project / ".git").mkdir(parents=True)
        self.mem = self.project / ".bossku" / "memory"
        self.state = self.mem / "sync-state.json"
        remember(self.project, "plan", "An earlier note, so the state file has content.", home=self.home)

    def pending(self):
        return json.loads(self.state.read_text(encoding="utf-8"))["pending"]

    def save(self, kind, note):
        """The command an agent runs: its exit code, the message it prints, and its error output."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["remember", "--json", "--home", str(self.home), "--project", str(self.project),
                         "--kind", kind, note])
        return code, json.loads(out.getvalue())["message"] if code == 0 else out.getvalue(), err.getvalue()

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

    def two_saves_take_turns(self, emptied):
        def first():
            remember(self.project, "learning", "FIRST note", home=self.home)

        with first_writer_stopped_mid_rewrite(self, first, emptied):
            child = self.second_writer("SECOND note")
            first_line = child.stdout.readline().strip()
        out, err = child.communicate(timeout=60)
        self.assertEqual(child.returncode, 0, err)
        self.assertEqual(first_line, "waiting",
                         "the second writer used sync-state.json while the first was rewriting it: " + err)
        self.assertEqual(sorted(self.pending()), ["decision", "learning", "plan"])
        self.assertIn("FIRST note", (self.mem / "learnings.md").read_text(encoding="utf-8"))
        self.assertIn("SECOND note", (self.mem / "decisions.md").read_text(encoding="utf-8"))
        self.assertEqual(sorted(p.name for p in self.mem.iterdir()),
                         ["decisions.md", "learnings.md", "plans.md", "sync-state.json"])

    def test_a_save_does_not_read_the_state_while_another_save_rewrites_it(self):
        self.two_saves_take_turns(emptied=True)        # was: JSONDecodeError in the second save

    def test_a_save_does_not_write_over_the_state_another_save_read(self):
        self.two_saves_take_turns(emptied=False)       # was: one of the two kinds dropped from "pending"

    def test_a_broken_state_file_is_kept_and_the_note_is_still_saved(self):
        broken = b'{\n  "pending": [\n    "plan"\n  ]\n}\n  "decision"\n  ]\n}'   # the tail of a longer rewrite
        self.state.write_bytes(broken)
        code, out, err = self.save("decision", "Saved next to a broken state file.")
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Saved next to a broken state file.", (self.mem / "decisions.md").read_text(encoding="utf-8"))
        kept = self.mem / "sync-state.json.broken"
        self.assertIn(f"sync-state.json could not be read, so a new one was started; the old one is kept as {kept}", out)
        self.assertEqual(kept.read_bytes(), broken)
        self.assertEqual(self.pending(), ["decision"])
        code, out, err = self.save("learning", "The next save is a plain one.")    # once, not on every save
        self.assertEqual((code, err), (0, ""))
        self.assertNotIn("could not be read", out)
        self.assertEqual(self.pending(), ["decision", "learning"])
        self.assertEqual(sorted(p.name for p in self.mem.glob("sync-state*")), ["sync-state.json", "sync-state.json.broken"])

    def test_a_vault_edit_is_kept_when_the_state_that_knew_the_copy_was_lost(self):
        vault = Path(self.home.parent) / "vault"           # in the temp folder too, so this project syncs to it
        vault.mkdir()
        save_user_config({"obsidian_vault": str(vault)}, self.home)
        remember(self.project, "plan", "Exported once.", home=self.home)
        copy = vault / "BosskuAI" / "repo" / "plans.md"
        copy.write_text(copy.read_text(encoding="utf-8") + "\nMY EDIT in the vault\n", encoding="utf-8")
        self.state.write_text('{"file_hashes": {"plans.md": "ab', encoding="utf-8")   # cut short
        code, out, err = self.save("decision", "Saved after the state was lost.")
        self.assertEqual((code, err), (0, ""))
        conflicts = list(copy.parent.glob("plans.md.conflict*.md"))
        self.assertEqual(len(conflicts), 1, out)
        self.assertIn("MY EDIT in the vault", conflicts[0].read_text(encoding="utf-8"))
        self.assertEqual(copy.read_text(encoding="utf-8"), (self.mem / "plans.md").read_text(encoding="utf-8"))
        state = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertNotIn("reset_from", state)               # the copies are known again, so the next sync is normal
        self.assertEqual(sorted(state["file_hashes"]), ["decisions.md", "plans.md"])

    def link(self, name, target):
        try:
            (self.mem / name).symlink_to(target)
        except OSError as exc:        # Windows needs a privilege or developer mode for links
            self.skipTest(f"cannot make a link here: {exc}")

    def test_a_state_file_that_is_a_link_is_not_repaired_through_the_link(self):
        outside = self.home / "my-own-file.txt"        # a cloned repo could commit such a link
        outside.write_text("not JSON, and not bossku's to rewrite\n", encoding="utf-8")
        self.state.unlink()
        self.link("sync-state.json", outside)
        code, out, err = self.save("decision", "Saved next to a linked state file.")
        self.assertEqual(code, 2)                       # fails loudly, as before: the note is in, nothing else is written
        self.assertIn("Saved next to a linked state file.", (self.mem / "decisions.md").read_text(encoding="utf-8"))
        self.assertEqual(outside.read_text(encoding="utf-8"), "not JSON, and not bossku's to rewrite\n")
        self.assertEqual(list(self.mem.glob("*.broken")), [])

    def test_the_copy_of_a_broken_state_file_is_never_written_through_a_link(self):
        outside = self.home / "planted.txt"
        self.link("sync-state.json.broken", outside)    # a link to a file that does not exist yet
        self.state.write_text("{broken", encoding="utf-8")
        code, out, err = self.save("decision", "Saved next to a planted link.")
        self.assertEqual(code, 2)
        self.assertFalse(outside.exists())
        self.assertEqual(self.state.read_text(encoding="utf-8"), "{broken")

    def test_a_state_file_that_stays_locked_does_not_fail_a_saved_note(self):
        with locked(self.state), mock.patch("bossku.filelock.LOCK_WAIT", 0.2):
            code, out, err = self.save("decision", "Saved while the state was busy.")
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Saved while the state was busy.", (self.mem / "decisions.md").read_text(encoding="utf-8"))
        self.assertIn("sync-state.json was busy", out)


if __name__ == "__main__":
    unittest.main()
