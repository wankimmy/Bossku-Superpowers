import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from bossku.cli import main
from bossku.evidence import summarize


def use(name, id, **args):
    return json.dumps({"type": "assistant", "timestamp": "2026-01-01T00:00:01Z",
                       "message": {"content": [{"type": "tool_use", "id": id, "name": name, "input": args}]}})


def result(id, is_error=False):
    return json.dumps({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": id, "content": "x", "is_error": is_error}]}})


def prompt(text):
    return json.dumps({"type": "user", "message": {"role": "user", "content": text}})


class EvidenceTests(unittest.TestCase):
    def summary(self, lines):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join(lines), encoding="utf-8")
            return summarize(str(path))

    def test_no_code_change(self):
        got = self.summary([prompt("explain"), use("Read", "r1", file_path="a.py"), result("r1")])
        self.assertEqual(got, {"code_edits": [], "checks": [], "state": "no_code_change"})

    def test_edit_without_a_check_is_unverified(self):
        got = self.summary([prompt("fix"), use("Edit", "e1", file_path="a.py"), result("e1"),
                            use("Bash", "b1", command="cat pytest.ini"), result("b1")])
        self.assertEqual((got["state"], got["code_edits"], got["checks"]), ("unverified", ["a.py"], []))

    def test_a_failed_last_check_is_failed_verification(self):
        got = self.summary([prompt("fix"), use("Edit", "e1", file_path="a.py"),
                            use("Bash", "b1", command="pytest"), result("b1", True)])
        self.assertEqual(got["state"], "failed_verification")
        self.assertEqual(got["checks"], [{"command": "pytest", "ok": False, "timestamp": "2026-01-01T00:00:01Z"}])

    def test_a_passing_check_after_the_last_edit_is_verified_and_a_missing_result_is_null(self):
        lines = [prompt("fix"), use("Edit", "e1", file_path="a.py"), use("Bash", "b1", command="pytest"),
                 result("b1", True), use("Edit", "e2", file_path="a.py"), use("Bash", "b2", command="pytest"),
                 result("b2")]
        got = self.summary(lines)
        self.assertEqual((got["state"], [c["ok"] for c in got["checks"]]), ("verified", [False, True]))
        self.assertEqual(self.summary(lines[:6])["checks"][-1]["ok"], None)
        self.assertEqual(self.summary(lines[:6])["state"], "verified")

    def test_a_denied_or_aborted_check_is_not_run_and_does_not_decide(self):
        denied = json.dumps({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "b2", "is_error": True,
             "content": "Permission for this action was denied by the Claude Code auto mode classifier."}]}})
        lines = [prompt("fix"), use("Edit", "e1", file_path="a.py"), use("Bash", "b1", command="pytest"), result("b1"),
                 use("Bash", "b2", command="pytest -x"), denied]
        got = self.summary(lines)
        self.assertEqual((got["state"], [c["ok"] for c in got["checks"]]), ("verified", [True, "not_run"]))
        only = self.summary([lines[0], lines[1], lines[4], denied])
        self.assertEqual((only["state"], [c["ok"] for c in only["checks"]]), ("unverified", ["not_run"]))

    def test_only_the_last_turn_counts(self):
        got = self.summary([prompt("one"), use("Edit", "e1", file_path="a.py"), prompt("two")])
        self.assertEqual(got["state"], "no_code_change")

    def test_a_project_in_the_temp_folder_is_read_from_the_transcript_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "app.py")
            lines = [json.dumps({"type": "user", "cwd": tmp, "message": {"role": "user", "content": "fix"}}),
                     json.dumps({"type": "assistant", "cwd": tmp, "message": {"content": [
                         {"type": "tool_use", "id": "e1", "name": "Edit", "input": {"file_path": target}}]}})]
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join(lines), encoding="utf-8")
            got = summarize(str(path))
        self.assertEqual((got["state"], got["code_edits"]), ("unverified", [target]))

    def test_a_long_check_command_is_capped(self):
        got = self.summary([prompt("fix"), use("Edit", "e1", file_path="a.py"),
                            use("Bash", "b1", command="pytest " + "x" * 500)])
        self.assertEqual(len(got["checks"][0]["command"]), 200)

    def test_cli_prints_the_dict_as_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join([prompt("fix"), use("Edit", "e1", file_path="a.py")]), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(["evidence", "--transcript", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue())["state"], "unverified")


if __name__ == "__main__":
    unittest.main()
