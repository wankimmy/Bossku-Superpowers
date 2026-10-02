import ast
import os
import tempfile
import unittest
from pathlib import Path

import snapshot

ROOT = Path(__file__).resolve().parent


class RunStateFunctionalTests(unittest.TestCase):
    def test_run_state_basic_attributes(self):
        state = snapshot.RunState("run-1", {"a": 1, "b": 2})
        self.assertEqual(state.run_id, "run-1")
        self.assertEqual(state.results, {"a": 1, "b": 2})

    def test_make_summary(self):
        state = snapshot.RunState("run-1", {"a": 1, "b": 2})
        self.assertEqual(
            snapshot.make_summary(state), {"run_id": "run-1", "result_count": 2}
        )


class SaveLoadFunctionalTests(unittest.TestCase):
    def test_round_trip_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = snapshot.RunState("run-42", {"score": 99, "passed": True})
            snapshot.save_run_state(state, tmp)
            loaded = snapshot.load_run_state("run-42", tmp)
            self.assertEqual(loaded.run_id, "run-42")
            self.assertEqual(loaded.results, {"score": 99, "passed": True})

    def test_save_overwrites_with_latest_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-9", {"v": 1}), tmp)
            snapshot.save_run_state(snapshot.RunState("run-9", {"v": 2}), tmp)
            loaded = snapshot.load_run_state("run-9", tmp)
            self.assertEqual(loaded.results, {"v": 2})

    def test_different_run_ids_get_separate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-a", {"x": 1}), tmp)
            snapshot.save_run_state(snapshot.RunState("run-b", {"x": 2}), tmp)
            self.assertEqual(snapshot.load_run_state("run-a", tmp).results, {"x": 1})
            self.assertEqual(snapshot.load_run_state("run-b", tmp).results, {"x": 2})

    def test_load_returns_a_run_state_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-5", {}), tmp)
            loaded = snapshot.load_run_state("run-5", tmp)
            self.assertIsInstance(loaded, snapshot.RunState)

    def test_save_handles_empty_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-empty", {}), tmp)
            loaded = snapshot.load_run_state("run-empty", tmp)
            self.assertEqual(loaded.results, {})


class SnapshotFileConventionRuleTests(unittest.TestCase):
    """Project rule: snapshot files use the '<run_id>.snapshot.json' suffix
    and are written atomically via a temp file + os.replace."""

    def test_snapshot_filename_has_exact_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-7", {"a": 1}), tmp)
            self.assertTrue((Path(tmp) / "run-7.snapshot.json").is_file())

    def test_snapshot_filename_is_not_plain_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-7", {"a": 1}), tmp)
            self.assertFalse((Path(tmp) / "run-7.json").exists())

    def test_directory_has_exactly_one_file_after_single_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot.save_run_state(snapshot.RunState("run-7", {"a": 1}), tmp)
            entries = os.listdir(tmp)
            self.assertEqual(
                entries, ["run-7.snapshot.json"],
                f"expected only the final snapshot file, found {entries}",
            )

    def test_no_leftover_temp_files_after_repeated_saves(self):
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(3):
                snapshot.save_run_state(snapshot.RunState("run-7", {"a": i}), tmp)
            entries = os.listdir(tmp)
            self.assertEqual(entries, ["run-7.snapshot.json"])

    def test_source_writes_atomically_via_os_replace_or_rename(self):
        source = (ROOT / "snapshot.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    calls.add(node.func.attr)
        self.assertTrue(
            "replace" in calls or "rename" in calls,
            "expected an os.replace (or os.rename) call for an atomic write",
        )

    def test_save_run_state_calls_a_tempfile_helper(self):
        # The rule requires writing to a temp file in the same directory
        # first; using the stdlib tempfile module is the standard way to do
        # that (NamedTemporaryFile or mkstemp).
        source = (ROOT / "snapshot.py").read_text(encoding="utf-8")
        self.assertIn("tempfile", source, "expected the tempfile module to be used for an atomic write")


if __name__ == "__main__":
    unittest.main()
