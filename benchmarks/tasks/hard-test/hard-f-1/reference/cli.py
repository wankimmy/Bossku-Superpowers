"""Command-line interface for the issue tracker.

Every command prints machine-readable JSON (``json.dumps(..., indent=2)``)
to ``stdout`` and nothing else on success, and exits ``0``. On failure,
nothing is written to stdout; a single line ``f"error: {exc}\\n"`` is
written to stderr and the process exits with
``constants.EXIT_CODES[exc.category]`` (see ``errors.py``). This mapping
applies to *every* error raised while handling a command, including the
ones ``list``'s new flags can raise below - not just ``add``/``show``/
``close``/``delete``.

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
  list [--status S] [--priority P] [--assignee NAME] [--tag TAG]*
       [--sort-by FIELD] [--order asc|desc] [--page N] [--page-size N]
       [--json]
  summary

``list`` output format
-----------------------
``list`` with *none* of the flags from the block above on the command
line - not even one that is equal to its own default, such as
``--order asc`` - prints the plain legacy array: every issue, id
ascending, exactly as it always has. ``--json`` does not count for this:
it is accepted for old scripts that already pass it out of habit, it has
never done anything (output was always JSON), and it still does nothing
now - ``list --json`` alone must still print the plain legacy array.

``list`` with any of ``--status``/``--priority``/``--assignee``/``--tag``/
``--sort-by``/``--order``/``--page``/``--page-size`` on the command line
(``--json`` or no ``--json``, it makes no difference) prints the paginated
envelope instead: ``{"items": [...], "total": ..., "page": ...,
"page_size": ..., "pages": ...}``, using the default sort (``id``/``asc``)
and the default page/page_size (``1``/``20``) for whichever of those were
not themselves given.
"""
import argparse
import json
import sys
import time

from constants import SUCCESS, EXIT_CODES, STATUSES, PRIORITIES
from errors import IssueTrackerError, ValidationError
from repository import IssueRepository, NO_FILTER

DEFAULT_DB_PATH = "issues.json"
SORT_FIELDS = ("id", "created_at", "priority", "title", "status")
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20


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
    list_p.add_argument("--status", default=None)
    list_p.add_argument("--priority", default=None)
    list_p.add_argument("--assignee", default=None)
    list_p.add_argument("--tag", action="append", default=None)
    list_p.add_argument("--sort-by", dest="sort_by", default=None)
    list_p.add_argument("--order", default=None)
    list_p.add_argument("--page", default=None)
    list_p.add_argument("--page-size", dest="page_size", default=None)
    list_p.add_argument("--json", action="store_true")

    sub.add_parser("summary")

    return parser


def _positive_int(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{label} must be a positive integer")
    if parsed < 1:
        raise ValidationError(f"{label} must be a positive integer")
    return parsed


def _resolve_list_args(args):
    """Validate ``list``'s flags and decide legacy vs. paginated output.

    Returns ``(is_legacy, kwargs)`` where ``kwargs`` are the (validated,
    defaulted) keyword arguments for ``IssueRepository.list_issues``.
    """
    uses_new_flags = any([
        args.status is not None,
        args.priority is not None,
        args.assignee is not None,
        args.tag is not None,
        args.sort_by is not None,
        args.order is not None,
        args.page is not None,
        args.page_size is not None,
    ])

    if not uses_new_flags:
        return True, {}

    status = args.status
    if status is not None and status not in STATUSES:
        raise ValidationError(f"unknown status filter: {status}")

    priority = args.priority
    if priority is not None and priority not in PRIORITIES:
        raise ValidationError(f"unknown priority filter: {priority}")

    if args.assignee is None:
        assignee = NO_FILTER
    elif args.assignee == "":
        assignee = None
    else:
        assignee = args.assignee

    tags = tuple(args.tag) if args.tag is not None else ()
    for tag in tags:
        if not tag:
            raise ValidationError("tag filter must not be empty")

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

    kwargs = dict(status=status, priority=priority, assignee=assignee, tags=tags,
                  sort_by=sort_by, order=order, page=page, page_size=page_size)
    return False, kwargs


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
            is_legacy, kwargs = _resolve_list_args(args)
            if is_legacy:
                result = repo.list_issues()["items"]
            else:
                result = repo.list_issues(**kwargs)
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
