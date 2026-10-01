"""Command-line interface for the issue tracker.

Every command prints machine-readable JSON (``json.dumps(..., indent=2)``)
to ``stdout`` and nothing else on success, and exits ``0``. On failure,
nothing is written to stdout; a single line ``f"error: {exc}\\n"`` is
written to stderr and the process exits with
``constants.EXIT_CODES[exc.category]`` (see ``errors.py``). This mapping
applies to *every* error raised while handling a command - not just the
ones below.

``main()`` always returns an ``int`` exit code: every ``ValidationError``/
``NotFoundError``/``StorageError`` raised while handling a parsed command
is caught right here and turned into the stderr-plus-exit-code pair above
- ``main`` never raises one of those three as an uncaught exception, and
never calls ``sys.exit`` itself for them. (A completely malformed command
line - an unknown subcommand, a missing required positional - is still
rejected by ``argparse`` in the usual way; that part is unchanged.) This
is what keeps ``main`` usable in-process from tests, not just from
``__main__`` below.

Commands:
  add TITLE [--priority P] [--assignee NAME] [--tag TAG]*
  show ID
  close ID
  delete ID
  list [--json]
  summary

``--json`` on ``list`` is accepted for backward compatibility with older
scripts that already pass it out of habit. Output has always been JSON;
the flag has never changed anything and still doesn't.
"""
import argparse
import json
import sys
import time

from constants import SUCCESS, EXIT_CODES
from errors import IssueTrackerError
from repository import IssueRepository

DEFAULT_DB_PATH = "issues.json"


def _build_parser():
    parser = argparse.ArgumentParser(prog="issues.py")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("title")
    add_p.add_argument("--priority")
    add_p.add_argument("--assignee")
    add_p.add_argument("--tag", action="append", default=[])

    show_p = sub.add_parser("show")
    show_p.add_argument("id", type=int)

    close_p = sub.add_parser("close")
    close_p.add_argument("id", type=int)

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("id", type=int)

    list_p = sub.add_parser("list")
    list_p.add_argument("--json", action="store_true")

    sub.add_parser("summary")

    return parser


def main(argv, stdout=None, stderr=None, db_path=DEFAULT_DB_PATH, clock=time.time):
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo = IssueRepository(db_path, clock=clock)

    try:
        if args.command == "add":
            result = repo.add(args.title, priority=args.priority,
                               assignee=args.assignee, tags=args.tag)
        elif args.command == "show":
            result = repo.get(args.id)
        elif args.command == "close":
            result = repo.close(args.id)
        elif args.command == "delete":
            repo.delete(args.id)
            result = {"deleted": args.id}
        elif args.command == "list":
            result = repo.list_issues()
        elif args.command == "summary":
            result = repo.summary()
        else:  # pragma: no cover - argparse enforces valid choices
            raise AssertionError(args.command)
    except IssueTrackerError as exc:
        stderr.write(f"error: {exc}\n")
        return EXIT_CODES[exc.category]

    stdout.write(json.dumps(result, indent=2) + "\n")
    return SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
