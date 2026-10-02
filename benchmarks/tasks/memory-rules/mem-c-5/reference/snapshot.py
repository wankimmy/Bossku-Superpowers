"""Helpers for caching data-pipeline run state.

Snapshot files on disk always use the ``<run_id>.snapshot.json`` suffix and
are written atomically (temp file in the same directory, then
``os.replace`` into the final path).
"""

import json
import os
import tempfile

SNAPSHOT_SUFFIX = ".snapshot.json"


class RunState:
    def __init__(self, run_id, results):
        self.run_id = run_id
        self.results = results


def make_summary(run_state):
    return {"run_id": run_state.run_id, "result_count": len(run_state.results)}


def _snapshot_path(run_id, directory):
    return os.path.join(directory, f"{run_id}{SNAPSHOT_SUFFIX}")


def save_run_state(run_state, directory):
    target_path = _snapshot_path(run_state.run_id, directory)
    payload = {"run_id": run_state.run_id, "results": run_state.results}

    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".snapshot-tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(tmp_path, target_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    return target_path


def load_run_state(run_id, directory):
    with open(_snapshot_path(run_id, directory), "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return RunState(payload["run_id"], payload["results"])
