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
- `list [--json]` - print every issue, `id` ascending. `--json` is
  accepted for older scripts that already pass it out of habit; output
  has always been JSON, so the flag has never changed anything.
- `summary` - print the count of issues in each status, plus a `total`.

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

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`IssueTrackerError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                              |
|--------------|-----------|---------------------------------------|
| `validation` | 2         | bad input (missing title, bad status) |
| `not_found`  | 3         | no issue with the given id             |
| `storage`    | 4         | the issue file could not be read/written |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly.
A command that runs successfully but matches nothing (an empty `list`,
for instance) is **not** an error: it exits `0`.
