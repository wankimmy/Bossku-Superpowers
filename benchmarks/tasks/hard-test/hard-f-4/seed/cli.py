"""Command-line interface for the bookmark manager.

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
  add URL [--title T] [--tag TAG]*
  show ID
  visit ID
  delete ID
  list [--pretty]
  stats

``add`` on a url that's already stored never creates a duplicate - see
``repository.py`` for exactly how it merges instead.

``--pretty`` on ``list`` is accepted for backward compatibility; output
has always been pretty-printed (`indent=2`), so the flag has never
changed anything.
"""
import argparse
import json
import sys
import time

from constants import SUCCESS, EXIT_CODES
from errors import BookmarkError
from repository import BookmarkRepository

DEFAULT_DB_PATH = "bookmarks.json"


def _build_parser():
    parser = argparse.ArgumentParser(prog="bookmarks.py")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("url")
    add_p.add_argument("--title")
    add_p.add_argument("--tag", action="append", default=[])

    show_p = sub.add_parser("show")
    show_p.add_argument("id", type=int)

    visit_p = sub.add_parser("visit")
    visit_p.add_argument("id", type=int)

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("id", type=int)

    list_p = sub.add_parser("list")
    list_p.add_argument("--pretty", action="store_true")

    sub.add_parser("stats")

    return parser


def main(argv, stdout=None, stderr=None, db_path=DEFAULT_DB_PATH, clock=time.time):
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo = BookmarkRepository(db_path, clock=clock)

    try:
        if args.command == "add":
            result = repo.add(args.url, title=args.title, tags=args.tag)
        elif args.command == "show":
            result = repo.get(args.id)
        elif args.command == "visit":
            result = repo.visit(args.id)
        elif args.command == "delete":
            repo.delete(args.id)
            result = {"deleted": args.id}
        elif args.command == "list":
            result = repo.list_bookmarks()
        elif args.command == "stats":
            result = repo.stats()
        else:  # pragma: no cover - argparse enforces valid choices
            raise AssertionError(args.command)
    except BookmarkError as exc:
        stderr.write(f"error: {exc}\n")
        return EXIT_CODES[exc.category]

    stdout.write(json.dumps(result, indent=2) + "\n")
    return SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
