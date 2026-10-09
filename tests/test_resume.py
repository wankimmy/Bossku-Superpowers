"""Cross-host resume, phase 1: Claude Code picks up a Codex task that stopped on its usage limit.

Every test builds synthetic Codex files (a state db and rollouts) in a temporary home. None reads the real ~/.codex,
the real ~/.bosskuai or the Obsidian vault.
"""

import contextlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from bossku import resume
from bossku.brief import memory_brief, session_output
from bossku.cli import main
from bossku.hint import hook_output, wants_resume
from bossku.memory import remember
from bossku.init_project import init_project
from bossku.resume import (
    BRIEF_CHARS, TAIL_BYTES, WINDOW, build_brief, debug_report, find_codex_stop, mark_continued, resume_context,
    session_pointer,
)

ROOT = Path(__file__).resolve().parents[1]
CWD = "C:\\work\\app"
LIMIT = {"message": "You hit your usage limit.", "codex_error_info": "usage_limit_exceeded"}
SECRET = "sk-abcdefghijklmnopqrstuvwxyz012345"


def iso(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def event(at, payload):
    return {"timestamp": iso(at), "type": "event_msg", "payload": payload}


def started(at):
    return event(at, {"type": "task_started", "turn_id": "t", "started_at": int(at)})


def complete(at, error=None, **extra):
    payload = {"type": "task_complete", "turn_id": "t", "last_agent_message": None, "completed_at": int(at), **extra}
    if error is not None:
        payload["error"] = error
    return event(at, payload)


def aborted(at):
    return event(at, {"type": "turn_aborted", "turn_id": "t", "reason": "interrupted", "completed_at": int(at)})


def item(at, **fields):
    return event(at, {"type": "item_completed", "thread_id": "x", "turn_id": "t", "item": fields})


def user(at, text):
    return item(at, type="UserMessage", id="u", client_id="c", content=[{"type": "text", "text": text, "text_elements": []}])


def agent(at, text):
    return item(at, type="AgentMessage", id="a", content=[{"type": "output_text", "text": text}], phase="final_answer")


def command(at, cmd, code, output="OUTPUT-NEVER-SHOWN"):
    return item(at, type="CommandExecution", id="c", command=["powershell.exe", "-Command", cmd], cwd=CWD,
                exit_code=code, aggregated_output=output, stdout=output, stderr=output, formatted_output=output)


def changed(at, *paths):
    return item(at, type="FileChange", id="f", status="completed", stdout="STDOUT-NEVER-SHOWN",
                changes={p: {"type": "update", "unified_diff": "DIFF-NEVER-SHOWN", "move_path": None} for p in paths})


def plan_call(at, steps):
    return {"timestamp": iso(at), "type": "response_item", "payload": {
        "type": "function_call", "name": "update_plan", "call_id": "p",
        "arguments": json.dumps({"plan": [{"step": s, "status": st} for s, st in steps]})}}


def rate_limits(at, resets_at):
    return event(at, {"type": "token_count", "info": None,
                      "rate_limits": {"limit_id": "codex", "primary": {"used_percent": 100.0, "window_minutes": 300,
                                                                       "resets_at": resets_at}}})


def write_rollout(path, records, tail=b""):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(r) + "\n" for r in records).encode("utf-8")
    path.write_bytes(data + tail)


def make_threads(home, rows, version=5):
    """A state db with the columns the resume code reads. A row is (id, rollout, cwd, updated_ms, archived, source)."""
    db = home / ".codex" / f"state_{version}.sqlite"
    db.parent.mkdir(parents=True, exist_ok=True)
    db.unlink(missing_ok=True)                 # a test may rebuild the threads it looks at
    con = sqlite3.connect(db)
    try:
        con.execute("CREATE TABLE threads (id TEXT PRIMARY KEY, rollout_path TEXT, cwd TEXT, updated_at_ms INTEGER, "
                    "archived INTEGER DEFAULT 0, thread_source TEXT, source TEXT, originator TEXT)")
        for tid, rollout, cwd, updated_ms, archived, source in rows:
            con.execute("INSERT INTO threads VALUES (?,?,?,?,?,?,?,?)",
                        (tid, str(rollout), cwd, updated_ms, archived, source, "vscode", "Codex Desktop"))
        con.commit()
    finally:
        con.close()


def tree(base):
    return {str(p.relative_to(base)): (p.stat().st_size, p.stat().st_mtime_ns) for p in sorted(base.rglob("*")) if p.is_file()}


def limit_session(at, goal="Add retry with backoff to the importer", cwd=CWD):
    """What the two real stops look like: the stop record is followed by a settings record and a new user message."""
    return [
        {"timestamp": iso(at - 400), "type": "session_meta", "payload": {"id": "t1", "cwd": cwd}},
        started(at - 300),
        user(at - 299, goal),
        plan_call(at - 250, [("Read the importer", "completed"), ("Add backoff", "in_progress"), ("Write tests", "pending")]),
        command(at - 200, "pytest tests/test_importer.py -q", 1),
        changed(at - 150, "c:\\work\\app\\importer.py", "c:\\work\\app\\tests\\test_importer.py"),
        agent(at - 100, "I added the backoff loop and the first test fails on the sleep call."),
        rate_limits(at - 50, int(at) + 3 * 3600),
        complete(at, LIMIT),
        event(at + 1, {"type": "thread_settings_applied", "thread_settings": {"cwd": cwd}}),
        user(at + 30, "continue"),
    ]


class ResumeBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.at = time.time() - 7200          # the stop: two hours ago
        self.now = self.at + 7200
        self.cwd = CWD

    def tearDown(self):
        self.tmp.cleanup()

    def thread(self, records, *, tid="t1", cwd=None, updated=None, archived=0, source="user", tail=b"", name=None):
        rollout = self.base / "sessions" / f"{name or tid}.jsonl"
        write_rollout(rollout, records, tail)
        return (tid, rollout, cwd or self.cwd, int((updated if updated is not None else self.at + 60) * 1000),
                archived, source)

    def build(self, *rows, version=5):
        make_threads(self.home, rows, version)

    def find(self, **kw):
        return find_codex_stop(kw.pop("cwd", self.cwd), self.home, kw.pop("now", self.now), **kw)


class FindStopTests(ResumeBase):
    def test_a_usage_limit_stop_is_found_and_the_pointer_says_so(self):
        self.build(self.thread(limit_session(self.at)))
        stop = self.find()
        self.assertEqual(stop.thread, "t1")
        self.assertAlmostEqual(stop.at, self.at, delta=1)
        self.assertEqual(session_pointer(self.cwd, home=self.home, now=self.now),
                         'Codex hit its usage limit 2h ago in this folder. Say "continue" to pick up its task. '
                         "Nothing loaded yet.")

    def test_the_reset_time_is_kept_only_when_it_lies_after_the_stop(self):
        self.build(self.thread(limit_session(self.at)))
        self.assertEqual(self.find().reset_at, int(self.at) + 3 * 3600)
        stale = limit_session(self.at)
        stale[7] = rate_limits(self.at - 50, int(self.at) - 3600)
        self.build(self.thread(stale))
        self.assertIsNone(self.find().reset_at)

    def test_a_reset_time_in_milliseconds_is_read_as_seconds(self):
        session = limit_session(self.at)
        session[7] = rate_limits(self.at - 50, (int(self.at) + 3 * 3600) * 1000)
        self.build(self.thread(session))
        self.assertEqual(self.find().reset_at, int(self.at) + 3 * 3600)

    def test_a_clean_end_is_not_a_stop(self):
        self.build(self.thread([started(self.at - 5), user(self.at - 4, "go"), complete(self.at, None)]))
        self.assertIsNone(self.find())
        self.build(self.thread([started(self.at - 5), complete(self.at, {"message": "boom", "codex_error_info": "other"})]))
        self.assertIsNone(self.find())

    def test_an_aborted_turn_is_not_a_stop(self):
        self.build(self.thread([started(self.at - 9), complete(self.at - 5, LIMIT), aborted(self.at)]))
        self.assertIsNone(self.find())
        self.build(self.thread([started(self.at - 9), complete(self.at - 5, LIMIT), started(self.at - 4), aborted(self.at)]))
        self.assertIsNone(self.find())

    def test_a_turn_started_after_the_stop_means_the_user_went_on_in_codex(self):
        self.build(self.thread(limit_session(self.at) + [started(self.at + 60)]))
        self.assertIsNone(self.find())

    def test_a_newer_thread_that_ended_cleanly_hides_an_older_stop(self):
        stopped = self.thread(limit_session(self.at - 6 * 3600), tid="old", updated=self.at - 6 * 3600 + 60)
        clean = self.thread([started(self.at - 5), user(self.at - 4, "Rename it"), complete(self.at, None)],
                            tid="new", updated=self.at + 60)
        self.build(stopped, clean)
        self.assertIsNone(self.find())
        self.assertIsNone(session_pointer(self.cwd, home=self.home, now=self.now))
        self.assertIsNone(resume_context(self.cwd, home=self.home, now=self.now))

    def test_once_the_newest_stop_is_continued_an_older_stop_is_not_offered(self):
        older = self.thread(limit_session(self.at - 3600), tid="old", updated=self.at - 3500)
        newest = self.thread(limit_session(self.at), tid="new", updated=self.at + 60)
        self.build(older, newest)
        self.assertEqual(self.find().thread, "new")
        self.assertIn("Add retry with backoff", resume_context(self.cwd, home=self.home, now=self.now))
        self.assertIsNone(self.find(now=self.now + 5))
        self.assertIsNone(resume_context(self.cwd, home=self.home, now=self.now + 5))
        self.assertEqual(self.find(now=self.now + 5, ignore_continued=False).thread, "new")   # `bossku resume` still shows it

    def test_a_thread_with_no_task_record_in_its_tail_is_skipped_and_the_next_one_decides(self):
        quiet = self.thread([{"timestamp": iso(self.at), "type": "session_meta", "payload": {"id": "q"}}], tid="quiet",
                            updated=self.at + 3000)
        self.build(quiet, self.thread(limit_session(self.at), tid="stopped"))
        self.assertEqual(self.find().thread, "stopped")

    def test_only_one_rollout_is_read_when_the_newest_thread_decides(self):
        rows = [self.thread([started(self.at - 5), complete(self.at, None)], tid=f"c{i}", updated=self.at + 100 + i)
                for i in range(10)]
        self.build(*rows, self.thread(limit_session(self.at), tid="old", updated=self.at))
        with mock.patch.object(resume, "_records", wraps=resume._records) as spy:
            self.assertIsNone(self.find())
        self.assertEqual(spy.call_count, 1)

    def test_the_folder_must_match_exactly_after_cleaning_up_the_path(self):
        for stored in ("\\\\?\\C:\\work\\app", "c:\\work\\app", "C:\\work\\app\\", "C:/work/app"):
            with self.subTest(stored=stored):
                self.build(self.thread(limit_session(self.at), cwd=stored))
                self.assertIsNotNone(self.find())
        self.build(self.thread(limit_session(self.at)))
        for asked in ("c:\\WORK\\app\\", "\\\\?\\C:\\work\\app", "C:/work/app/"):
            with self.subTest(asked=asked):
                self.assertIsNotNone(self.find(cwd=asked))
        for other in ("C:\\work\\app\\sub", "C:\\work\\app-wt", "C:\\work", "D:\\work\\app"):
            with self.subTest(other=other):
                self.assertIsNone(self.find(cwd=other))

    def test_subagent_guardian_and_archived_threads_are_ignored(self):
        rows = [self.thread(limit_session(self.at), tid=f"x{i}", source=source, archived=archived)
                for i, (source, archived) in enumerate((("subagent", 0), ("guardian_review", 0), ("user", 1), (None, 0)))]
        self.build(*rows)
        self.assertIsNone(self.find())

    def test_a_stop_older_than_the_window_is_not_offered(self):
        self.build(self.thread(limit_session(self.at)))
        self.assertIsNotNone(self.find(now=self.at + WINDOW - 60))
        self.assertIsNone(self.find(now=self.at + WINDOW + 60))
        # The thread was touched lately (the user kept chatting) but its last turn stopped long ago.
        old = self.at - WINDOW - 3600
        self.build(self.thread(limit_session(old), updated=self.at))
        self.assertIsNone(self.find())

    def test_the_newest_state_database_is_the_one_read(self):
        make_threads(self.home, [], version=4)
        self.build(self.thread(limit_session(self.at)), version=5)
        self.assertIsNotNone(self.find())
        make_threads(self.home, [], version=6)
        self.assertIsNone(self.find())

    def test_a_half_written_last_line_does_not_hide_the_stop(self):
        partial = b'{"timestamp": "2026-10-10T10:00:00.000Z", "type": "event_msg", "payload": {"type": "task_comp'
        self.build(self.thread(limit_session(self.at)[:-1], tail=partial))
        self.assertIsNotNone(self.find())

    def test_unexpected_shapes_raise_nothing_and_find_nothing(self):
        junk = [b"not json at all", b"[1, 2]", b'"text"', b"123", b"null", b"\xff\xfe\xfa", b"{}", b""]
        broken = [
            event(self.at, {"type": "task_complete", "error": "usage_limit_exceeded"}),
            event(self.at, {"type": "task_complete", "error": {"codex_error_info": ["usage_limit_exceeded"]}}),
            event(self.at, {"type": "task_complete", "error": {"message": "no info"}}),
            {"timestamp": iso(self.at), "type": "event_msg", "payload": "task_complete"},
            {"timestamp": iso(self.at), "type": "event_msg", "payload": None},
            {"timestamp": iso(self.at), "type": 7, "payload": {"type": "task_complete", "error": LIMIT}},
            {"type": "event_msg", "payload": {"type": "task_complete", "error": LIMIT}},   # no time anywhere
        ]
        for record in broken:
            with self.subTest(record=record):
                self.build(self.thread([started(self.at - 5), record], tail=b"\n".join(junk) + b"\n"))
                self.assertIsNone(self.find())
        # Junk lines between good records change nothing; a bad time falls back to completed_at.
        good = event(self.at, {"type": "task_complete", "error": LIMIT, "completed_at": int(self.at)})
        good["timestamp"] = "yesterday-ish"
        self.build(self.thread([started(self.at - 5), good], tail=b"\n".join(junk) + b"\n"))
        self.assertIsNotNone(self.find())

    def test_a_missing_database_rollout_or_folder_find_nothing(self):
        self.assertIsNone(self.find())
        self.build(("t1", self.base / "gone.jsonl", self.cwd, int(self.at * 1000), 0, "user"))
        self.assertIsNone(self.find())
        for bad in (None, "", 5, ["C:\\work\\app"]):
            self.assertIsNone(find_codex_stop(bad, self.home, self.now))

    def test_nothing_to_resume_means_no_pointer(self):
        self.assertIsNone(session_pointer(self.cwd, home=self.home, now=self.now))
        self.build(self.thread([started(self.at - 5), complete(self.at, None)]))
        self.assertIsNone(session_pointer(self.cwd, home=self.home, now=self.now))

    def test_a_stop_is_found_quickly_in_a_huge_rollout_and_at_most_two_mebibytes_are_read(self):
        path = self.base / "sessions" / "big.jsonl"
        pad = json.dumps({"type": "response_item", "payload": {"type": "message", "content": "x" * 1_000_000}}) + "\n"
        path.parent.mkdir(parents=True)
        with path.open("w", encoding="utf-8") as handle:
            for _ in range(50):
                handle.write(pad)
            for record in limit_session(self.at):
                handle.write(json.dumps(record) + "\n")
        self.assertGreater(path.stat().st_size, 50_000_000)
        self.assertLessEqual(len(resume._read_tail(path)), TAIL_BYTES)
        self.build(("big", path, self.cwd, int(self.at * 1000), 0, "user"))
        self.find()                                     # the first call loads sqlite3
        begun = time.perf_counter()
        stop = self.find()
        self.assertIsNotNone(stop)
        self.assertLess(time.perf_counter() - begun, 1.0)

    def test_a_stop_buried_deeper_than_the_tail_is_not_found(self):
        path = self.base / "sessions" / "deep.jsonl"
        pad = json.dumps({"type": "response_item", "payload": {"type": "message", "content": "x" * 1_000_000}}) + "\n"
        path.parent.mkdir(parents=True)
        with path.open("w", encoding="utf-8") as handle:
            handle.write(json.dumps(complete(self.at, LIMIT)) + "\n")
            for _ in range(4):
                handle.write(pad)
        self.build(("deep", path, self.cwd, int(self.at * 1000), 0, "user"))
        self.assertIsNone(self.find())

    def test_looking_for_a_stop_is_fast_when_there_is_none(self):
        self.assertIsNone(self.find())                  # no database at all
        begun = time.perf_counter()
        for _ in range(5):
            self.find()
        self.assertLess((time.perf_counter() - begun) / 5, 0.05)
        rows = [self.thread([started(self.at - 5), complete(self.at, None)], tid=f"c{i}", cwd=f"C:\\other\\p{i}")
                for i in range(40)]
        self.build(*rows)
        self.find()                                     # the first call loads sqlite3
        begun = time.perf_counter()
        for _ in range(5):
            self.assertIsNone(self.find())
        self.assertLess((time.perf_counter() - begun) / 5, 0.05)


class ContinuedMarkerTests(ResumeBase):
    def setUp(self):
        super().setUp()
        self.build(self.thread(limit_session(self.at)))

    def marker(self):
        return json.loads((self.home / ".bosskuai" / "resume-state.json").read_text(encoding="utf-8"))

    def test_delivering_the_brief_marks_the_thread_so_neither_pointer_nor_trigger_repeat(self):
        text = resume_context(self.cwd, home=self.home, now=self.now)
        self.assertIn("Add retry with backoff", text)
        self.assertEqual(set(self.marker()), {"continued"})
        self.assertEqual(list(self.marker()["continued"]), ["t1"])
        self.assertIsNone(resume_context(self.cwd, home=self.home, now=self.now + 5))
        self.assertIsNone(session_pointer(self.cwd, home=self.home, now=self.now + 5))
        self.assertIsNone(self.find(now=self.now + 5))
        self.assertIsNotNone(self.find(now=self.now + 5, ignore_continued=False))   # `bossku resume` still shows it

    def test_the_marker_holds_ids_and_times_only(self):
        resume_context(self.cwd, home=self.home, now=self.now)
        raw = (self.home / ".bosskuai" / "resume-state.json").read_text(encoding="utf-8")
        for text in ("Add retry", "backoff", "importer", "work", "pytest"):
            self.assertNotIn(text, raw)
        self.assertEqual(self.marker()["continued"]["t1"], self.now)

    def test_a_failed_marker_write_still_delivers_the_brief(self):
        (self.home / ".bosskuai").write_text("a file where the folder should be", encoding="utf-8")
        self.assertIn("Add retry with backoff", resume_context(self.cwd, home=self.home, now=self.now))
        self.assertFalse(mark_continued(self.find(), home=self.home, now=self.now))

    def test_old_entries_are_dropped_when_the_marker_is_written(self):
        state = self.home / ".bosskuai" / "resume-state.json"
        state.parent.mkdir()
        state.write_text(json.dumps({"continued": {"old": self.now - 8 * 86400, "recent": self.now - 86400}}), encoding="utf-8")
        mark_continued(self.find(), home=self.home, now=self.now)
        self.assertEqual(sorted(self.marker()["continued"]), ["recent", "t1"])

    def test_an_unreadable_marker_is_treated_as_empty(self):
        state = self.home / ".bosskuai" / "resume-state.json"
        state.parent.mkdir()
        for text in ("not json", "[]", json.dumps({"continued": "x"}), json.dumps({"continued": {"t1": "soon"}})):
            state.write_text(text, encoding="utf-8")
            self.assertIsNotNone(self.find(), text)

    def test_a_newer_stop_in_the_same_thread_is_offered_again(self):
        resume_context(self.cwd, home=self.home, now=self.now)
        later = self.at + 4 * 3600
        again = limit_session(self.at)[:-1] + [started(later - 20), complete(later, LIMIT)]
        self.build(self.thread(again, updated=later))
        self.assertIsNotNone(self.find(now=later + 60))


class SessionStartTests(ResumeBase):
    def payload(self, source, cwd=None):
        return json.dumps({"cwd": cwd or self.cwd, "source": source, "hook_event_name": "SessionStart"})

    def test_startup_and_clear_get_the_pointer_and_resume_and_compact_do_not(self):
        self.build(self.thread(limit_session(self.at)))
        for source in ("startup", "clear"):
            out = session_output(self.payload(source), home=self.home)
            self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
            self.assertIn("Codex hit its usage limit", out["hookSpecificOutput"]["additionalContext"])
        for source in ("resume", "compact", None):
            self.assertEqual(session_output(self.payload(source), home=self.home), {})
        self.assertEqual(session_output(json.dumps({"cwd": self.cwd}), home=self.home), {})

    def test_notes_and_pointer_arrive_as_one_context_and_notes_alone_still_work(self):
        project = self.base / "app"
        init_project(project, root=ROOT, home=self.home)
        remember(project, "plan", "Ship the importer next.", home=self.home)
        self.build(self.thread(limit_session(self.at), cwd=str(project)))
        out = session_output(self.payload("startup", str(project)), home=self.home)
        text = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Ship the importer next.", text)
        self.assertIn("Codex hit its usage limit", text)
        self.assertLess(text.index("Ship the importer"), text.index("Codex hit"))
        self.build(self.thread([started(self.at - 5), complete(self.at, None)], cwd=str(project)))
        notes_only = session_output(self.payload("startup", str(project)), home=self.home)["hookSpecificOutput"]["additionalContext"]
        self.assertNotIn("Codex hit", notes_only)
        self.assertIn("Ship the importer next.", notes_only)

    def test_a_failing_notes_lookup_does_not_drop_the_pointer(self):
        self.build(self.thread(limit_session(self.at)))
        (self.home / ".bosskuai").mkdir()
        (self.home / ".bosskuai" / "config.json").write_text("[]", encoding="utf-8")     # a config the notes code chokes on
        with self.assertRaises(AttributeError):
            memory_brief(Path(self.cwd), home=self.home)
        out = session_output(self.payload("startup"), home=self.home)
        self.assertIn("Codex hit its usage limit", out["hookSpecificOutput"]["additionalContext"])

    def test_nothing_to_say_prints_nothing(self):
        self.assertEqual(session_output(self.payload("startup"), home=self.home), {})
        self.assertEqual(session_output("", home=self.home), {})
        self.assertEqual(session_output(json.dumps({"source": "startup"}), home=self.home), {})


class TriggerTests(ResumeBase):
    def ask(self, prompt, cwd=None):
        return hook_output(json.dumps({"prompt": prompt, "cwd": cwd or self.cwd}), root=ROOT, home=self.home)

    def test_the_words_and_the_length_limit(self):
        for prompt in ("continue", "Continue please", "carry on", "keep going", "pick up where it stopped", "lanjut", "lanjutkan",
                       "sambung balik kerja tadi", "teruskan", "bossku resume", "ok continue with that now ya"):
            with self.subTest(prompt=prompt):
                self.assertTrue(wants_resume(prompt))
        for prompt in ("", "thanks", "continued", "discontinue the plan", "please continue with the whole refactor of the module",
                       "/continue", "!continue", "run the tests"):
            with self.subTest(prompt=prompt):
                self.assertFalse(wants_resume(prompt))

    def test_continue_with_a_stop_gives_the_brief_and_skips_the_skill_hint(self):
        self.build(self.thread(limit_session(self.at)))
        out = self.ask("continue")
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        text = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Continuing a Codex task", text)
        self.assertNotIn("skill hint", text)

    def test_continue_without_a_stop_gives_nothing_and_a_long_sentence_gives_nothing(self):
        self.assertEqual(self.ask("continue"), {})
        self.build(self.thread([started(self.at - 5), complete(self.at, None)]))
        self.assertEqual(self.ask("continue"), {})
        self.build(self.thread(limit_session(self.at)))
        self.assertEqual(self.ask("please continue with the whole refactor of the importer module now"), {})
        self.assertEqual(self.ask("continue", cwd="C:\\somewhere\\else"), {})
        self.assertEqual(hook_output(json.dumps({"prompt": "continue"}), root=ROOT, home=self.home), {})

    def test_the_brief_is_given_once(self):
        self.build(self.thread(limit_session(self.at)))
        self.assertTrue(self.ask("continue"))
        self.assertEqual(self.ask("continue"), {})

    def test_the_off_switch_stops_both_hooks_and_nothing_is_read_or_written(self):
        self.build(self.thread(limit_session(self.at)))
        start = json.dumps({"cwd": self.cwd, "source": "startup"})
        for value in ("off", "0", "false", " OFF "):
            with self.subTest(value=value), mock.patch.dict(os.environ, {"BOSSKU_RESUME": value}), \
                    mock.patch.object(resume, "_threads", side_effect=AssertionError("Codex's files were opened")):
                self.assertEqual(session_output(start, home=self.home), {})
                self.assertEqual(self.ask("continue"), {})
                self.assertIsNone(session_pointer(self.cwd, home=self.home, now=self.now))
                self.assertIsNone(resume_context(self.cwd, home=self.home, now=self.now))
        self.assertFalse((self.home / ".bosskuai" / "resume-state.json").exists(), "off: nothing is marked as handed over")
        with mock.patch.dict(os.environ, {"BOSSKU_RESUME": ""}):    # unset or empty: on
            self.assertIn("Codex hit its usage limit", session_output(start, home=self.home)["hookSpecificOutput"]["additionalContext"])
            self.assertIn("Continuing a Codex task", self.ask("continue")["hookSpecificOutput"]["additionalContext"])
        with mock.patch.dict(os.environ, {"BOSSKU_RESUME": "off"}):    # `bossku resume` is the user asking: it still works
            self.assertIsNotNone(find_codex_stop(self.cwd, self.home, self.now, ignore_continued=False))


class ImportCostTests(unittest.TestCase):
    """Every prompt and session start runs a hook; only a "continue" or a new session may pay for bossku.resume."""

    def loaded(self, home, *calls):
        lines = ["import json, sys", "from pathlib import Path", "import bossku.cli", "from bossku.hint import hook_output",
                 "from bossku.brief import session_output", f"home = Path({home!r})", *calls,
                 "print('bossku.resume' in sys.modules)"]
        run = subprocess.run([sys.executable, "-c", chr(10).join(lines)], capture_output=True, text=True,
                             env={**os.environ, "PYTHONPATH": str(ROOT)})
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout.split()[-1] == "True"

    def test_other_prompts_and_session_sources_do_not_import_it(self):
        def prompt(text):
            return f"hook_output(json.dumps({{'prompt': {text!r}, 'cwd': 'x'}}), home=home)"

        def session(source):
            return f"session_output(json.dumps({{'cwd': 'x', 'source': {source!r}}}), home=home)"

        with tempfile.TemporaryDirectory() as home:
            self.assertFalse(self.loaded(home))
            self.assertFalse(self.loaded(home, prompt("write a parser for dates")))
            self.assertFalse(self.loaded(home, session("compact")))
            self.assertTrue(self.loaded(home, prompt("continue")))
            self.assertTrue(self.loaded(home, session("startup")))


class BriefTests(ResumeBase):
    def brief(self, records=None, **kw):
        self.build(self.thread(records or limit_session(self.at)))
        return build_brief(self.find(), kw.pop("cwd", self.cwd), now=self.now)

    def test_the_brief_names_the_goal_plan_files_commands_and_last_message(self):
        text = self.brief()
        self.assertTrue(text.startswith("Continuing a Codex task."))
        self.assertIn("usage limit at", text)
        self.assertIn("2h ago", text)
        self.assertIn("Context only, not saved", text)
        self.assertIn("Add retry with backoff to the importer", text)        # the request of the stopped turn, not "continue"
        self.assertIn("[x] Read the importer", text)
        self.assertIn("[~] Add backoff", text)
        self.assertIn("[ ] Write tests", text)
        self.assertIn("importer.py", text)
        self.assertIn("pytest tests/test_importer.py -q", text)
        self.assertIn("exit 1", text)
        self.assertIn("the first test fails on the sleep call", text)
        self.assertIn("Do not redo finished steps", text)
        self.assertNotIn("powershell", text)

    def test_the_goal_is_the_last_request_before_the_stop_not_an_older_one_and_not_the_one_after(self):
        session = limit_session(self.at)
        session.insert(2, user(self.at - 298, "An older request that was already done"))
        session.insert(2, user(self.at - 400, "The very first request of the day"))
        text = self.brief(session)
        self.assertIn("Add retry with backoff to the importer", text)
        for other in ("older request", "very first", "continue"):
            self.assertNotIn(other, text.split("Goal (latest user request): ")[1].split("\n")[0])

    def test_a_request_typed_in_codex_after_the_stop_is_shown_but_a_plain_continue_is_not(self):
        session = limit_session(self.at)                        # ends with the user typing "continue"
        self.assertNotIn("Asked in Codex", self.brief(session))
        session[-1] = user(self.at + 30, f"Skip the tests and ship it, token {SECRET}")
        text = self.brief(session)
        self.assertIn("Asked in Codex after the stop: Skip the tests and ship it", text)
        self.assertNotIn(SECRET, text)
        self.assertNotIn("Skip the tests", text.split("Goal (latest user request): ")[1].split(chr(10))[0])
        session.append(user(self.at + 60, "Actually only run the importer tests"))
        text = self.brief(session)
        self.assertIn("Asked in Codex after the stop: Actually only run the importer tests", text)
        self.assertNotIn("Skip the tests", text)
        session.append(user(self.at + 90, "L" * 5000))
        text = self.brief(session)
        self.assertIn("L" * 147 + "...", text)
        self.assertNotIn("L" * 148, text)
        self.assertLessEqual(len(text), BRIEF_CHARS)

    def test_the_hard_cut_keeps_the_brief_inside_the_limit_when_nothing_else_helps(self):
        from unittest import mock
        with mock.patch("bossku.resume.BRIEF_CHARS", 300):
            text = self.brief()
        self.assertEqual(len(text), 300)
        self.assertTrue(text.endswith("..."))

    def test_the_text_of_tool_output_diffs_and_reasoning_is_never_included(self):
        session = limit_session(self.at)
        session.insert(3, item(self.at - 280, type="Reasoning", id="r", summary_text=["REASONING-NEVER-SHOWN"],
                               raw_content=["REASONING-NEVER-SHOWN"]))
        session.insert(3, {"timestamp": iso(self.at), "type": "response_item", "payload": {
            "type": "reasoning", "encrypted_content": "ENCRYPTED-NEVER-SHOWN"}})
        session.insert(3, {"timestamp": iso(self.at), "type": "compacted", "payload": {"replacement_history": ["HISTORY-NEVER-SHOWN"]}})
        text = self.brief(session)
        for planted in ("OUTPUT-NEVER-SHOWN", "STDOUT-NEVER-SHOWN", "DIFF-NEVER-SHOWN", "REASONING-NEVER-SHOWN",
                        "ENCRYPTED-NEVER-SHOWN", "HISTORY-NEVER-SHOWN"):
            self.assertNotIn(planted, text)

    def test_a_planted_secret_never_reaches_the_brief(self):
        session = [
            started(self.at - 300),
            user(self.at - 299, f"Deploy with token {SECRET} and API_KEY=hunter2hunter2 please"),
            plan_call(self.at - 250, [(f"Rotate {SECRET}", "pending")]),
            command(self.at - 200, f"curl -H 'Authorization: Bearer abc123def456ghi789' https://x.test --token={SECRET}", 0),
            changed(self.at - 150, f"c:\\work\\app\\{SECRET}.txt"),
            agent(self.at - 100, f"Done. The password: hunter2hunter2 and {SECRET} are in place."),
            complete(self.at, LIMIT),
        ]
        text = self.brief(session)
        self.assertIn("[REDACTED]", text)
        for secret in (SECRET, "hunter2hunter2", "abc123def456ghi789", "abcdefghijklmnopqrstuvwxyz012345"):
            self.assertNotIn(secret, text)

    def test_command_line_secrets_never_reach_the_brief(self):
        # Shell commands are shown verbatim, so the forms notes never carry matter here: flag values, short options,
        # a login line, a variable that ends in PASS. Each one is a separate session so the last-3 window cannot hide a miss.
        planted = "Hunter2pass"
        forms = [
            f"mysql -u root -p{planted} db",
            f"docker login -u bob -p {planted}",
            f"curl -u admin:{planted} https://api.test",
            f"curl -fsSLu admin:{planted} https://api.test",
            f"curl --user admin:{planted} https://api.test",
            f"psql --password {planted}",
            f"gh secret set X --body {planted}",
            f"gh secret set X -b {planted}",
            f"export DB_PASS={planted}",
            f"MYSQL_PWD={planted} mysqldump app",
            f"az login --password {planted}",
            f"tool --client-secret={planted} run",
            f"tool --db-pass {planted} run",
        ]
        for form in forms:
            with self.subTest(form=form):
                text = self.brief([started(self.at - 300), user(self.at - 299, "Deploy it"), command(self.at - 200, form, 0),
                                   complete(self.at, LIMIT)])
                self.assertNotIn(planted, text)
                self.assertIn("[REDACTED]", text)

    def test_ordinary_command_lines_stay_readable(self):
        same = ["mkdir -p build", "mysql -p app", "mysql -P 3306 -u root", "docker login --password-stdin", "PWD=/srv ls",
                "npm test -- --reporter=spec", "git push -u origin main", "curl -fsSL https://x.test -o out"]
        for form in same:
            with self.subTest(form=form):
                text = self.brief([started(self.at - 300), user(self.at - 299, "Deploy it"), command(self.at - 200, form, 0),
                                   complete(self.at, LIMIT)])
                self.assertIn(f"`{form}`", text)

    def test_a_secret_is_removed_before_the_text_is_cut_not_after(self):
        goal = "x" * 285 + " " + SECRET
        text = self.brief([started(self.at - 300), user(self.at - 299, goal), complete(self.at, LIMIT)])
        self.assertNotIn("sk-abc", text)
        self.assertNotIn("abcdefghijklmnop", text)

    def test_a_huge_session_still_fits_in_the_limit_and_keeps_the_goal(self):
        session = [started(self.at - 900), user(self.at - 899, "G" * 5000)]
        session.append(plan_call(self.at - 800, [(f"step number {i} " + "p" * 200, "pending") for i in range(30)]))
        for i in range(10):
            session.append(command(self.at - 700 + i, "run-" + "c" * 400 + str(i), i))
            session.append(changed(self.at - 600 + i, *[f"c:\\work\\app\\pkg{i}\\" + "d" * 150 + f"{j}.py" for j in range(3)]))
        session += [agent(self.at - 50, "M" * 5000), complete(self.at, LIMIT)]
        text = self.brief(session)
        self.assertLessEqual(len(text), BRIEF_CHARS)
        self.assertIn("Goal", text)
        self.assertIn("GGGG", text)

    def crowded(self, name_length, plan_steps=0):
        """A session with 3 long commands, 8 files, a 400 character last message and a 300 character request."""
        session = [started(self.at - 900), user(self.at - 899, "G" * 300)]
        if plan_steps:
            session.append(plan_call(self.at - 800, [(f"step {i} " + "s" * 60, "pending") for i in range(plan_steps)]))
        session.append(changed(self.at - 600, *["c:\\work\\app\\" + "d" * name_length + f"{i}.py" for i in range(8)]))
        session += [command(self.at - 500 + i, "run-" + "c" * 150 + str(i), 0) for i in range(3)]
        return session + [agent(self.at - 50, "M" * 400), complete(self.at, LIMIT)]

    def test_commands_are_cut_first_then_files_beyond_five_then_the_last_message(self):
        text = self.brief(self.crowded(75))                   # over the limit with commands, not without them
        self.assertEqual((text.count("Last commands"), text.count(".py"), text.count("M")), (0, 8, 400))
        text = self.brief(self.crowded(50, plan_steps=8))     # still over: files beyond five go too
        self.assertEqual((text.count("Last commands"), text.count(".py"), text.count("M")), (0, 5, 400))
        text = self.brief(self.crowded(90, plan_steps=8))     # and as a last step the message is cut to 200
        self.assertEqual((text.count("Last commands"), text.count(".py"), 190 < text.count("M") <= 200), (0, 5, True))
        for kept in (text, self.brief(self.crowded(75)), self.brief(self.crowded(10))):
            self.assertLessEqual(len(kept), BRIEF_CHARS)
            self.assertIn("G" * 300, kept)                    # the request is always kept
        self.assertIn("Last commands", self.brief(self.crowded(10)))   # nothing is cut when it all fits

    def test_a_session_with_odd_shapes_still_gives_a_brief(self):
        session = [
            started(self.at - 300),
            item(self.at - 299, type="UserMessage", content=7),
            item(self.at - 298, type="UserMessage", text="A plain text goal"),
            item(self.at - 297, type="CommandExecution", command=5, exit_code="x"),
            item(self.at - 296, type="CommandExecution", command="git status", exit_code=0),
            item(self.at - 295, type="FileChange", changes=["not", "a", "dict"]),
            item(self.at - 294, type="FileChange", changes={"relative/file.py": {}, 5: {}}),
            item(self.at - 293, type="Plan", text="1. read\n2. write"),
            item(self.at - 292, type="AgentMessage", content="a string body"),
            {"timestamp": iso(self.at - 291), "type": "response_item", "payload": {
                "type": "function_call", "name": "update_plan", "arguments": "{broken"}},
            "junk",
            complete(self.at, LIMIT),
        ]
        text = self.brief([r for r in session if isinstance(r, dict)], cwd="C:\\work\\app")
        self.assertIn("A plain text goal", text)
        self.assertIn("git status", text)
        self.assertIn("relative/file.py", text)
        self.assertIn("a string body", text)
        self.assertIn("read", text)

    def test_the_latest_of_a_plan_item_and_a_plan_call_wins(self):
        session = [started(self.at - 300), user(self.at - 299, "go"),
                   plan_call(self.at - 250, [("old call step", "completed")]),
                   item(self.at - 240, type="Plan", id="p", text="newer plan from the plan item"),
                   complete(self.at, LIMIT)]
        text = self.brief(session)
        self.assertIn("newer plan from the plan item", text)
        self.assertNotIn("old call step", text)
        session.insert(4, plan_call(self.at - 200, [("newest call step", "pending")]))
        text = self.brief(session)
        self.assertIn("newest call step", text)
        self.assertNotIn("newer plan from the plan item", text)

    def test_a_missing_rollout_gives_no_brief_and_no_error(self):
        self.build(self.thread(limit_session(self.at)))
        stop = self.find()
        Path(stop.rollout).unlink()
        self.assertEqual(build_brief(stop, self.cwd), "")
        self.assertEqual(build_brief(None, self.cwd), "")

    def test_the_reset_time_is_shown_when_known(self):
        self.assertIn("resets", self.brief())
        session = limit_session(self.at)
        del session[7]
        self.assertNotIn("resets", self.brief(session))

    def test_nothing_is_written_anywhere_by_looking(self):
        vault = self.base / "vault"
        (vault / "BosskuAI").mkdir(parents=True)
        (self.home / ".bosskuai").mkdir()
        (self.home / ".bosskuai" / "config.json").write_text(
            json.dumps({"memory_storage": "obsidian", "obsidian_vault": str(vault)}), encoding="utf-8")
        self.build(self.thread(limit_session(self.at)))
        before = tree(self.base)
        stop = self.find()
        build_brief(stop, self.cwd, now=self.now)
        session_pointer(self.cwd, home=self.home, now=self.now)
        debug_report(self.cwd, home=self.home, now=self.now)
        self.assertEqual(tree(self.base), before)
        resume_context(self.cwd, home=self.home, now=self.now)        # delivering writes the marker and nothing else
        after = tree(self.base)
        self.assertEqual({k for k in after if before.get(k) != after[k]}, {str(Path("home") / ".bosskuai" / "resume-state.json")})
        self.assertEqual(sorted(p.name for p in vault.rglob("*")), ["BosskuAI"])


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class GitCrossCheckTests(ResumeBase):
    def setUp(self):
        super().setUp()
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.cwd = str(self.repo)

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@example.test",
                        "-c", "core.autocrlf=false", *args], check=True, capture_output=True)

    def lowered(self, name):
        text = str(self.repo / name)
        return text[0].lower() + text[1:] if len(text) > 1 and text[1] == ":" else text

    def session(self, *paths):
        return [started(self.at - 300), user(self.at - 299, "Fix the parser"), changed(self.at - 100, *paths),
                complete(self.at, LIMIT)]

    def brief(self, records):
        self.build(self.thread(records))
        return build_brief(self.find(), self.cwd, now=self.now)

    def test_files_are_marked_dirty_or_clean_and_other_dirty_files_are_counted(self):
        self.git("init", "-q")
        (self.repo / "a.py").write_text("one\n", encoding="utf-8")
        (self.repo / "b.md").write_text("two\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "first")
        (self.repo / "a.py").write_text("one changed\n", encoding="utf-8")
        (self.repo / "other.txt").write_text("not from codex\n", encoding="utf-8")
        text = self.brief(self.session(self.lowered("a.py"), self.lowered("b.md")))
        self.assertIn("a.py (still dirty)", text)
        self.assertIn("b.md (clean now)", text)
        self.assertIn("+1 dirty file not from Codex", text)
        self.assertNotIn("unverified", text)

    def test_a_path_that_matches_nothing_in_git_says_the_list_is_unverified(self):
        self.git("init", "-q")
        (self.repo / "a.py").write_text("one\n", encoding="utf-8")
        text = self.brief(self.session("c:\\elsewhere\\gone.py"))
        self.assertIn("gone.py", text)
        self.assertIn("file list unverified", text)

    def test_a_folder_that_is_not_a_repository_says_the_list_is_unverified(self):
        text = self.brief(self.session(self.lowered("a.py")))
        self.assertIn("a.py", text)
        self.assertIn("file list unverified", text)

    def test_relative_paths_are_taken_from_the_session_folder(self):
        self.git("init", "-q")
        (self.repo / "sub").mkdir()
        (self.repo / "sub" / "r.py").write_text("x\n", encoding="utf-8")
        text = self.brief(self.session("sub/r.py"))
        self.assertIn("r.py (still dirty)", text)

    def test_git_is_asked_not_to_take_locks_so_looking_never_touches_the_index(self):
        from unittest import mock
        self.git("init", "-q")
        seen = []
        real = subprocess.run

        def spy(*args, **kw):
            seen.append(kw["env"].get("GIT_OPTIONAL_LOCKS"))
            return real(*args, **kw)

        with mock.patch("subprocess.run", spy):
            self.brief(self.session(self.lowered("a.py")))
        self.assertTrue(seen)
        self.assertEqual(set(seen), {"0"})

    def test_git_is_not_run_when_the_pointer_is_computed(self):
        self.build(self.thread(self.session(self.lowered("a.py"))))
        from unittest import mock
        with mock.patch("subprocess.run", side_effect=AssertionError("git ran")):
            self.assertIsNotNone(session_pointer(self.cwd, home=self.home, now=self.now))
            self.assertIsNotNone(self.find())


class CommandLineTests(ResumeBase):
    def setUp(self):
        super().setUp()
        self.project = self.base / "proj"
        self.project.mkdir()
        self.cwd = str(self.project)

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--home", str(self.home), *argv])
        return code, out.getvalue()

    def test_resume_prints_the_brief_or_says_there_is_nothing(self):
        self.assertEqual(self.run_cli("resume", "--project", self.cwd), (0, "Nothing to resume.\n"))
        self.build(self.thread(limit_session(self.at, cwd=self.cwd)))
        code, text = self.run_cli("resume", "--project", self.cwd)
        self.assertEqual(code, 0)
        self.assertIn("Continuing a Codex task", text)
        self.assertIn("Add retry with backoff", text)

    def test_looking_does_not_use_up_the_pointer(self):
        self.build(self.thread(limit_session(self.at, cwd=self.cwd)))
        self.run_cli("resume", "--project", self.cwd)
        self.run_cli("resume", "--project", self.cwd)
        self.assertFalse((self.home / ".bosskuai" / "resume-state.json").exists())
        self.assertIsNotNone(session_pointer(self.cwd, home=self.home))

    def test_a_continued_thread_can_still_be_looked_at(self):
        self.build(self.thread(limit_session(self.at, cwd=self.cwd)))
        resume_context(self.cwd, home=self.home)
        self.assertIn("Continuing a Codex task", self.run_cli("resume", "--project", self.cwd)[1])

    def test_the_two_hooks_work_end_to_end_through_the_command_line(self):
        self.build(self.thread(limit_session(self.at, cwd=self.cwd)))

        def hook(name, payload):
            run = subprocess.run([sys.executable, "-m", "bossku", "--home", str(self.home), name], input=json.dumps(payload),
                                 capture_output=True, text=True, cwd=self.base, env={**os.environ, "PYTHONPATH": str(ROOT)})
            self.assertEqual(run.returncode, 0, run.stderr)
            return json.loads(run.stdout) if run.stdout.strip() else {}

        started_up = hook("session-brief", {"cwd": self.cwd, "source": "startup"})
        self.assertIn("Codex hit its usage limit", started_up["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(hook("session-brief", {"cwd": self.cwd, "source": "compact"}), {})
        asked = hook("skill-hint", {"cwd": self.cwd, "prompt": "continue"})
        self.assertIn("Add retry with backoff", asked["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(hook("skill-hint", {"cwd": self.cwd, "prompt": "continue"}), {})
        self.assertEqual(hook("session-brief", {"cwd": self.cwd, "source": "startup"}), {})

    def test_debug_prints_structure_and_never_text(self):
        session = limit_session(self.at, cwd=self.cwd)
        session[1:1] = [{"timestamp": iso(self.at), "type": "event_msg", "payload": {"type": "TEXT-AS-A-TYPE NEVER SHOWN"}}]
        self.build(self.thread(session))
        code, text = self.run_cli("resume", "--debug", "--project", self.cwd)
        self.assertEqual(code, 0)
        for shown in ("task_complete", "usage_limit_exceeded", "error", "message", "codex_error_info", "item_completed"):
            self.assertIn(shown, text)
        for hidden in ("Add retry", "backoff", "importer", "pytest", "usage limit.", "You hit", "TEXT-AS-A-TYPE",
                       "OUTPUT-NEVER-SHOWN", "powershell", self.project.name + "\\", "sleep call"):
            self.assertNotIn(hidden, text)

    def test_debug_explains_why_there_is_no_stop(self):
        self.assertIn("no Codex state database", self.run_cli("resume", "--debug", "--project", self.cwd)[1])
        self.build(self.thread([started(self.at - 5), complete(self.at, None)], cwd=self.cwd))
        text = self.run_cli("resume", "--debug", "--project", self.cwd)[1]
        self.assertIn("not a stop", text)
        self.build()
        self.assertIn("no thread", self.run_cli("resume", "--debug", "--project", self.cwd)[1])


if __name__ == "__main__":
    unittest.main()
