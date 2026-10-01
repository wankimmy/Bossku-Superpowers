"""Command-line interface for the expense ledger.

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
  add DATE CATEGORY AMOUNT [--note N]
  show ID
  recategorize ID NEW_CATEGORY
  delete ID
  list [--currency USD]
  count

``--currency`` on ``list`` only accepts ``USD`` (its default); this is a
single-currency ledger, so the flag has never changed anything.
"""
import argparse
import json
import sys

from constants import SUCCESS, EXIT_CODES
from errors import LedgerError, ValidationError
from repository import ExpenseRepository

DEFAULT_DB_PATH = "expenses.json"


def _build_parser():
    parser = argparse.ArgumentParser(prog="expenses.py")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("date")
    add_p.add_argument("category")
    add_p.add_argument("amount")
    add_p.add_argument("--note")

    show_p = sub.add_parser("show")
    show_p.add_argument("id", type=int)

    recat_p = sub.add_parser("recategorize")
    recat_p.add_argument("id", type=int)
    recat_p.add_argument("new_category")

    delete_p = sub.add_parser("delete")
    delete_p.add_argument("id", type=int)

    list_p = sub.add_parser("list")
    list_p.add_argument("--currency", dest="currency", default="USD")

    sub.add_parser("count")

    return parser


def main(argv, stdout=None, stderr=None, db_path=DEFAULT_DB_PATH):
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo = ExpenseRepository(db_path)

    try:
        if args.command == "add":
            result = repo.add(args.date, args.category, args.amount, note=args.note)
        elif args.command == "show":
            result = repo.get(args.id)
        elif args.command == "recategorize":
            result = repo.recategorize(args.id, args.new_category)
        elif args.command == "delete":
            repo.delete(args.id)
            result = {"deleted": args.id}
        elif args.command == "list":
            if args.currency != "USD":
                raise ValidationError(f"unknown currency: {args.currency}")
            result = repo.list_expenses()
        elif args.command == "count":
            result = repo.count()
        else:  # pragma: no cover - argparse enforces valid choices
            raise AssertionError(args.command)
    except LedgerError as exc:
        stderr.write(f"error: {exc}\n")
        return EXIT_CODES[exc.category]

    stdout.write(json.dumps(result, indent=2) + "\n")
    return SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
