"""What the last turn of a transcript shows ran: the code edits, the checks and whether the last check passed.

Reads the transcript with the parsing of bossku/gate.py, so this report and the stop gate cannot disagree.
"""

from __future__ import annotations

from bossku.gate import _is_check, _is_code_edit, _scan, _turn_lines, _verification
from bossku.redact import redact_command


def summarize(transcript_path: str, project: str = "") -> dict:
    """{code_edits, checks: [{command, ok, timestamp}], state} for the turn after the user's latest prompt.
    `ok` is None when the transcript holds no result for that check
    and "not_run" when the command was denied or aborted (it never ran, so it neither passed nor failed)."""
    turn = _scan(_turn_lines(transcript_path))
    project = project or turn.cwd   # the same folder the Stop hook sends, so a project in the temp folder is gated
    edits, checks = [], []
    for name, args in turn.calls:
        if _is_code_edit(name, args, project):
            edits.append(str(args.get("file_path") or args.get("path") or args.get("notebook_path") or ""))
    for call in turn.calls:
        name, args = call
        if _is_check(name, args):
            state = turn.errors.get(call.id)
            ok = "not_run" if state == "not_run" else None if state is None else not state
            checks.append({"command": redact_command(" ".join(str(args.get("command", "")).split())[:2000])[:200], "ok": ok,
                           "timestamp": call.timestamp})
    return {"code_edits": edits, "checks": checks, "state": _verification(turn.calls, project, turn.errors)[0]}
