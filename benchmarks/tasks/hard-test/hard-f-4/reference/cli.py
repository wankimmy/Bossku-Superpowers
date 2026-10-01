"""Command-line interface for the bookmark manager.

Every command prints machine-readable JSON (``json.dumps(..., indent=2)``)
to ``stdout`` and nothing else on success, and exits ``0``. On failure,
nothing is written to stdout; a single line ``f"error: {exc}\\n"`` is
written to stderr and the process exits with
``constants.EXIT_CODES[exc.category]`` (see ``errors.py``). This mapping
applies to *every* error raised while handling a command, including the
ones ``list``'s new flags can raise below - not just ``add``/``show``/
``visit``/``delete``.

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
  list [--tag TAG]* [--any-tag] [--min-visits N]
       [--sort-by FIELD] [--order asc|desc] [--page N] [--page-size N]
       [--pretty]
  stats

``list`` output format
-----------------------
``list`` with *none* of the flags from the block above on the command
line - not even one that is equal to its own default, such as
``--order asc`` - prints the plain legacy array: every bookmark, id
ascending, exactly as it always has. ``--pretty`` does not count for
this: it is accepted for old scripts that already pass it out of habit,
it has never done anything (output was always pretty-printed), and it
still does nothing now - ``list --pretty`` alone must still print the
plain legacy array.

``list`` with any of ``--tag``/``--any-tag``/``--min-visits``/
``--sort-by``/``--order``/``--page``/``--page-size`` on the command line
(``--pretty`` or no ``--pretty``, it makes no difference) prints the
paginated envelope instead: ``{"items": [...], "total": ..., "page":
..., "page_size": ..., "pages": ...}``, using the default sort (``id``/
``asc``) and the default page/page_size (``1``/``15``) for whichever of
those were not themselves given. This includes ``--any-tag`` given by
itself, with no ``--tag`` at all - it still counts as a flag that was
given, even though there's then no tag filter for it to flip the
meaning of.
"""
import argparse
import json
import sys
import time

from constants import SUCCESS, EXIT_CODES
from errors import BookmarkError, ValidationError
from repository import BookmarkRepository

DEFAULT_DB_PATH = "bookmarks.json"
SORT_FIELDS = ("id", "added_at", "visits", "title")
MAX_PAGE_SIZE = 40
DEFAULT_PAGE_SIZE = 15


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
    list_p.add_argument("--tag", action="append", default=None)
    list_p.add_argument("--any-tag", dest="any_tag", action="store_true", default=None)
    list_p.add_argument("--min-visits", dest="min_visits", default=None)
    list_p.add_argument("--sort-by", dest="sort_by", default=None)
    list_p.add_argument("--order", default=None)
    list_p.add_argument("--page", default=None)
    list_p.add_argument("--page-size", dest="page_size", default=None)
    list_p.add_argument("--pretty", action="store_true")

    sub.add_parser("stats")

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
    defaulted) keyword arguments for ``BookmarkRepository.list_bookmarks``.
    """
    uses_new_flags = any([
        args.tag is not None,
        args.any_tag is not None,
        args.min_visits is not None,
        args.sort_by is not None,
        args.order is not None,
        args.page is not None,
        args.page_size is not None,
    ])

    if not uses_new_flags:
        return True, {}

    tags = tuple(args.tag) if args.tag is not None else ()
    for tag in tags:
        if not tag:
            raise ValidationError("tag filter must not be empty")
    any_tag = bool(args.any_tag)

    if args.min_visits is not None:
        try:
            min_visits = int(args.min_visits)
        except (TypeError, ValueError):
            raise ValidationError("min_visits must be a non-negative integer")
        if min_visits < 0:
            raise ValidationError("min_visits must be a non-negative integer")
    else:
        min_visits = None

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

    kwargs = dict(tags=tags, any_tag=any_tag, min_visits=min_visits, sort_by=sort_by,
                  order=order, page=page, page_size=page_size)
    return False, kwargs


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
            is_legacy, kwargs = _resolve_list_args(args)
            if is_legacy:
                result = repo.list_bookmarks()["items"]
            else:
                result = repo.list_bookmarks(**kwargs)
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
