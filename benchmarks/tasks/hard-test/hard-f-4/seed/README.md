# bookmark-manager

A tiny on-disk bookmark manager. Bookmarks live in a single JSON file
(default `bookmarks.json`, next to the CLI) and are managed through
`cli.py`.

Run the CLI with `python cli.py <command> ...`. Run the tests with
`python -m unittest discover -s tests`.

## Data model

Each bookmark has:

- `id` - positive integer, assigned by the repository. Ids are assigned
  once, in increasing order, and are **never reused**, even if the
  bookmark with the highest id is later deleted.
- `url` - non-empty string starting with `http://` or `https://`.
- `title` - non-empty string; defaults to the bookmark's own `url` if
  none is given.
- `tags` - a list of strings (deduplicated, order-preserving).
- `added_at` - an ISO 8601 UTC timestamp, set once when the bookmark is
  first created.
- `visits` - non-negative integer, starts at `0`.

## Commands

- `add URL [--title T] [--tag TAG]*` - add a bookmark. If `URL` is
  already stored (exact, case-sensitive match), this does **not**
  create a duplicate - it merges into the existing bookmark instead:
  any newly given tags are added to its tag list (only the genuinely
  new ones), and `--title` replaces its title only if given and
  non-empty this call; `id`, `added_at`, and `visits` are left exactly
  as they were. Calling `add` twice in a row with identical arguments
  leaves the bookmark in the same state either way.
- `show ID` - print one bookmark.
- `visit ID` - record a visit: increments `visits` by one *every* call
  (this one is not a no-op the second time - each call is a real visit).
- `delete ID` - remove a bookmark.
- `list [--pretty]` - print every bookmark, `id` ascending. `--pretty`
  is accepted for backward compatibility; output has always been
  pretty-printed, so the flag has never changed anything.
- `stats` - print `{"bookmarks": <total count>, "total_visits": <sum of
  every bookmark's visits>}`. This always covers **every** bookmark - it
  is completely unaffected by any filter given to `list`.

Every command that succeeds prints one JSON value
(`json.dumps(..., indent=2)`) to stdout and nothing else, and exits `0`.
`list`, `show`, and `stats` are **read-only**: they never write to the
bookmark file.

Every returned bookmark (from `add`, `show`, `visit`, or `list`) is an
independent copy - nothing you do to the returned value (including
appending to its `tags` list) can change the stored bookmark.

### Example

```
$ python cli.py add https://example.com/guide --title "The Guide" --tag ref --tag howto
{
  "id": 1,
  "url": "https://example.com/guide",
  "title": "The Guide",
  "tags": [
    "ref",
    "howto"
  ],
  "added_at": "2024-01-15T12:00:00+00:00",
  "visits": 0
}
```

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`BookmarkError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                    |
|--------------|-----------|-----------------------------------------------|
| `validation` | 2         | bad input (bad url, bad sort/page, ...)        |
| `not_found`  | 3         | no bookmark with the given id                  |
| `storage`    | 4         | the bookmark file could not be read/written    |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly.
A command that runs successfully but matches nothing (an empty `list`,
for instance) is **not** an error: it exits `0`.
