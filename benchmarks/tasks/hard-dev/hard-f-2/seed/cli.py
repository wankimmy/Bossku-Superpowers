"""Command-line interface for the contact book.

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
  add FULL_NAME [--email E] [--phone P] [--company C] [--tag TAG]*
  show ID
  delete ID
  tag ID TAG_NAME
  list [--format json]
  count

``--format`` on ``list`` only accepts ``json`` (its default); output has
always been JSON. Any other value is rejected the same way any other bad
input is.
"""
import argparse
import json
import sys
import time

from constants import SUCCESS, EXIT_CODES
from errors import ContactBookError, ValidationError
from repository import ContactRepository

DEFAULT_DB_PATH = "contacts.json"


def _build_parser():
    parser = argparse.ArgumentParser(prog="contacts.py")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("full_name")
    add_p.add_argument("--email")
    add_p.add_argument("--phone")
    add_p.add_argument("--company")
    add_p.add_argument("--tag", action="append", default=[])

    show_p = sub.add_parser("show")
    show_p.add_argument("id", type=int)

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("id", type=int)

    tag_p = sub.add_parser("tag")
    tag_p.add_argument("id", type=int)
    tag_p.add_argument("tag_name")

    list_p = sub.add_parser("list")
    list_p.add_argument("--format", dest="format", default="json")

    sub.add_parser("count")

    return parser


def main(argv, stdout=None, stderr=None, db_path=DEFAULT_DB_PATH, clock=time.time):
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo = ContactRepository(db_path, clock=clock)

    try:
        if args.command == "add":
            result = repo.add(args.full_name, email=args.email, phone=args.phone,
                               company=args.company, tags=args.tag)
        elif args.command == "show":
            result = repo.get(args.id)
        elif args.command == "delete":
            repo.delete(args.id)
            result = {"deleted": args.id}
        elif args.command == "tag":
            result = repo.tag(args.id, args.tag_name)
        elif args.command == "list":
            if args.format != "json":
                raise ValidationError(f"unknown format: {args.format}")
            result = repo.list_contacts()
        elif args.command == "count":
            result = repo.count()
        else:  # pragma: no cover - argparse enforces valid choices
            raise AssertionError(args.command)
    except ContactBookError as exc:
        stderr.write(f"error: {exc}\n")
        return EXIT_CODES[exc.category]

    stdout.write(json.dumps(result, indent=2) + "\n")
    return SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
