# issue-tracker

A tiny on-disk issue tracker for a small dev team. Issues live in a single
JSON file (default `issues.json`, next to the CLI) and are managed through
`cli.py`.

Run the CLI with `python cli.py <command> ...`. Run the tests with
`python -m unittest discover -s tests`.

## Data model

Each issue has:

- `id` - positive integer, assigned by the repository. Ids are assigned
  once, in increasing order, and are **never reused**, even if the
  issue with the highest id is later deleted.
- `title` - non-empty string.
- `status` - one of `open`, `in_progress`, `closed`. Defaults to `open`.
- `priority` - one of `low`, `medium`, `high`. Defaults to `medium`.
- `assignee` - a name, or `null` if unassigned.
- `tags` - a list of strings (deduplicated, order-preserving).
- `created_at` - an ISO 8601 UTC timestamp, set once when the issue is
  created.

## Commands

- `add TITLE [--priority P] [--assignee NAME] [--tag TAG]*` - create an
  issue. Repeating `--tag` adds more than one tag.
- `show ID` - print one issue.
- `close ID` - set an issue's status to `closed`.
- `delete ID` - remove an issue.
- `list [filters/sort/paging - see below] [--json]` - print issues.
- `summary` - print the count of issues in each status, plus a `total`.
  This always counts **every** issue in the file - it is completely
  unaffected by any filter given to `list`.

Every command that succeeds prints one JSON value
(`json.dumps(..., indent=2)`) to stdout and nothing else, and exits `0`.
`list` and `show` and `summary` are **read-only**: they never write to the
issue file.

Every returned issue (from `add`, `show`, `close`, or `list`) is an
independent copy - nothing you do to the returned value (including
appending to its `tags` list) can change the stored issue.

### Example

```
$ python cli.py add "Fix login bug" --priority high --assignee ren --tag auth
{
  "id": 1,
  "title": "Fix login bug",
  "status": "open",
  "priority": "high",
  "assignee": "ren",
  "tags": [
    "auth"
  ],
  "created_at": "2024-01-15T12:00:00+00:00"
}
```

## Filtering, sorting and paging `list`

`list` takes these optional flags, all of which are validated the same
way as any other input in this project - an invalid one is a `validation`
error (exit `2`), not a crash and not an empty/silent result:

- `--status {open,in_progress,closed}` - keep only that status.
- `--priority {low,medium,high}` - keep only that priority.
- `--assignee NAME` - keep only issues assigned to `NAME` (exact,
  case-sensitive match). `--assignee ""` (an explicit empty string) keeps
  only **unassigned** issues; leaving `--assignee` out entirely applies no
  assignee filter at all - those are different things.
- `--tag TAG` (repeatable) - keep only issues that have **every** given
  tag (it's an AND, not an OR).
- `--sort-by {id,created_at,priority,title,status}` - sort key. Default
  (when not given) is `id`. Sorting by `priority` uses severity order
  (`low < medium < high`), **not** alphabetical order.
- `--order {asc,desc}` - sort direction, default `asc`. Ties are always
  broken by `id` ascending, in both directions - `--order desc` only
  reverses the primary key, never the tie-break.
- `--page N` (default `1`) and `--page-size N` (default `20`, max `100`)
  - 1-based pagination, applied **after** filtering and sorting. A page
  past the end returns an empty `items` list, not an error. `total` and
  `pages` always describe the whole filtered set, the same on every page
  of it - not just the current page.

Filtering, sorting, and pagination are applied in that order: filter,
then sort, then page.

Giving **any** of the flags above switches `list`'s output from the
plain array it has always printed to a paginated envelope:

```
{"items": [...], "total": ..., "page": ..., "page_size": ..., "pages": ...}
```

using the defaults above for whichever of those flags weren't given.
This switch is based purely on whether one of those flags is *present on
the command line* - e.g. `list --order asc` still switches to the
envelope, even though `asc` is already the default, because `--order`
was given. `--json` is the one exception: since it has never affected
`list`'s output, it does not count, either way - `list --json` alone
still prints the plain array, exactly as before.

### Examples

```
$ python cli.py list --status open --sort-by priority
{
  "items": [
    {
      "id": 1,
      "title": "Fix login bug",
      "status": "open",
      "priority": "high",
      "assignee": "ren",
      "tags": [
        "auth"
      ],
      "created_at": "2024-01-15T12:00:00+00:00"
    },
    {
      "id": 3,
      "title": "Crash on logout",
      "status": "open",
      "priority": "high",
      "assignee": "kai",
      "tags": [
        "auth",
        "bug"
      ],
      "created_at": "2024-01-15T12:00:02+00:00"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

```
$ python cli.py list --page 2 --page-size 1
{
  "items": [
    {
      "id": 2,
      "title": "Write onboarding docs",
      "status": "closed",
      "priority": "low",
      "assignee": null,
      "tags": [
        "docs"
      ],
      "created_at": "2024-01-15T12:00:01+00:00"
    }
  ],
  "total": 3,
  "page": 2,
  "page_size": 1,
  "pages": 3
}
```

(These two examples assume three issues were added - "Fix login bug"
`high`/`ren`/`auth`, "Write onboarding docs" `low`/`docs`, "Crash on
logout" `high`/`kai`/`auth`+`bug` - and then issue `2` was closed.)

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`IssueTrackerError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                    |
|--------------|-----------|---------------------------------------------|
| `validation` | 2         | bad input (missing title, bad status/sort/page, ...) |
| `not_found`  | 3         | no issue with the given id                   |
| `storage`    | 4         | the issue file could not be read/written     |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly,
and it applies to every flag on every command, including the new `list`
flags above. A command that runs successfully but matches nothing (an
empty `list`, for instance) is **not** an error: it exits `0`.
