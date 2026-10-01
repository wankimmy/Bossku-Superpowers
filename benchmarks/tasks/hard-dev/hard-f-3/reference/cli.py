"""Command-line interface for the expense ledger.

Every command prints machine-readable JSON (``json.dumps(..., indent=2)``)
to ``stdout`` and nothing else on success, and exits ``0``. On failure,
nothing is written to stdout; a single line ``f"error: {exc}\\n"`` is
written to stderr and the process exits with
``constants.EXIT_CODES[exc.category]`` (see ``errors.py``). This mapping
applies to *every* error raised while handling a command, including the
ones ``list``'s new flags can raise below - not just ``add``/``show``/
``recategorize``/``delete``.

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
  list [--category C] [--from DATE] [--to DATE]
       [--sort-by FIELD] [--order asc|desc] [--page N] [--page-size N]
       [--currency USD]
  count

``list`` output format
-----------------------
``list`` with *none* of the flags from the block above on the command
line - not even one that is equal to its own default, such as
``--order asc`` - prints the plain legacy array: every expense, id
ascending, exactly as it always has. ``--currency`` does not count for
this: it is accepted for old scripts that already pass it out of habit,
it has never done anything (this is a single-currency ledger), and it
still does nothing now - ``list --currency USD`` alone must still print
the plain legacy array.

``list`` with any of ``--category``/``--from``/``--to``/``--sort-by``/
``--order``/``--page``/``--page-size`` on the command line (``--currency``
or no ``--currency``, it makes no difference) prints the paginated
envelope instead: ``{"items": [...], "total": ..., "page": ...,
"page_size": ..., "pages": ..., "total_amount": ...}``, using the
default sort (``id``/``asc``) and the default page/page_size (``1``/
``10``) for whichever of those were not themselves given. `total_amount`
is always the sum of every matching expense's amount (not just the
current page's), rounded with `money.round_money`.
"""
import argparse
import datetime
import json
import sys

from constants import SUCCESS, EXIT_CODES
from errors import LedgerError, ValidationError
from repository import ExpenseRepository

DEFAULT_DB_PATH = "expenses.json"
SORT_FIELDS = ("id", "date", "amount", "category")
MAX_PAGE_SIZE = 50
DEFAULT_PAGE_SIZE = 10


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
    list_p.add_argument("--category", default=None)
    list_p.add_argument("--from", dest="date_from", default=None)
    list_p.add_argument("--to", dest="date_to", default=None)
    list_p.add_argument("--sort-by", dest="sort_by", default=None)
    list_p.add_argument("--order", default=None)
    list_p.add_argument("--page", default=None)
    list_p.add_argument("--page-size", dest="page_size", default=None)
    list_p.add_argument("--currency", dest="currency", default="USD")

    sub.add_parser("count")

    return parser


def _positive_int(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{label} must be a positive integer")
    if parsed < 1:
        raise ValidationError(f"{label} must be a positive integer")
    return parsed


def _valid_date(value, label):
    try:
        datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{label} must be a YYYY-MM-DD date")
    return value


def _resolve_list_args(args):
    """Validate ``list``'s flags and decide legacy vs. paginated output.

    Returns ``(is_legacy, kwargs)`` where ``kwargs`` are the (validated,
    defaulted) keyword arguments for ``ExpenseRepository.list_expenses``.
    """
    if args.currency != "USD":
        raise ValidationError(f"unknown currency: {args.currency}")

    uses_new_flags = any([
        args.category is not None,
        args.date_from is not None,
        args.date_to is not None,
        args.sort_by is not None,
        args.order is not None,
        args.page is not None,
        args.page_size is not None,
    ])

    if not uses_new_flags:
        return True, {}

    category = args.category
    if category is not None and not category.strip():
        raise ValidationError("category filter must not be empty")

    date_from = _valid_date(args.date_from, "from") if args.date_from is not None else None
    date_to = _valid_date(args.date_to, "to") if args.date_to is not None else None

    sort_by = args.sort_by if args.sort_by is not None else "id"
    if sort_by not in SORT_FIELDS:
        raise ValidationError(f"unknown sort field: {sort_by}")

    order = args.order if args.order is not None else "asc"
    if order not in ("asc", "desc"):
        raise ValidationError(f"unknown order: {order}")

    page = _positive_int(args.page, "page") if args.page is not None else 1

    if args.page_size is not None:
        page_size = _positive_int(args.page_size, "page_size")
        if page_size > MAX_PAGE_SIZE:
            raise ValidationError(f"page_size must be between 1 and {MAX_PAGE_SIZE}")
    else:
        page_size = DEFAULT_PAGE_SIZE

    kwargs = dict(category=category, date_from=date_from, date_to=date_to,
                  sort_by=sort_by, order=order, page=page, page_size=page_size)
    return False, kwargs


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
            is_legacy, kwargs = _resolve_list_args(args)
            if is_legacy:
                result = repo.list_expenses()["items"]
            else:
                result = repo.list_expenses(**kwargs)
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
