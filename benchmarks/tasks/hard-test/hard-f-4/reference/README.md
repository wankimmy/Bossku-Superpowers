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
- `list [filters/sort/paging - see below] [--pretty]` - print bookmarks.
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

## Filtering, sorting and paging `list`

`list` takes these optional flags, all validated the same way as any
other input in this project - an invalid one is a `validation` error
(exit `2`), not a crash and not an empty/silent result:

- `--tag TAG` (repeatable) - by default, keep only bookmarks that have
  **every** given tag (AND). Add `--any-tag` to flip that to **at
  least one** of them (OR) instead - `--any-tag` only changes what
  `--tag` means; given by itself, with no `--tag` at all, there is
  nothing for it to flip, but it still counts as a flag that was given
  (see the output-format rule below).
- `--min-visits N` - keep only bookmarks with `visits >= N`.
- `--sort-by {id,added_at,visits,title}` - sort key. Default (when not
  given) is `id`. `title` sorts case-insensitively.
- `--order {asc,desc}` - sort direction, default `asc`. Ties are always
  broken by `id` ascending, in both directions - `--order desc` only
  reverses the primary key, never the tie-break.
- `--page N` (default `1`) and `--page-size N` (default `15`, max `40`)
  - 1-based pagination, applied **after** filtering and sorting. A page
  past the end returns an empty `items` list, not an error. `total` and
  `pages` always describe the whole filtered set, the same on every
  page of it - not just the current page.

Filtering, sorting, and pagination are applied in that order.

Giving **any** of the flags above switches `list`'s output from the
plain array it has always printed to a paginated envelope:

```
{"items": [...], "total": ..., "page": ..., "page_size": ..., "pages": ...}
```

using the defaults above for whichever of those flags weren't given.
This switch is based purely on whether one of those flags is *present
on the command line* - e.g. `list --order asc` still switches to the
envelope, even though `asc` is already the default, because `--order`
was given; the same is true of `list --any-tag` with no `--tag`.
`--pretty` is the one exception: since it has never affected `list`'s
output (output was always pretty-printed), it does not count, either
way - `list --pretty` alone still prints the plain array, exactly as
before.

### Examples

```
$ python cli.py list --tag ref --tag howto --any-tag
{
  "items": [
    {
      "id": 1,
      "url": "https://a.example.com/1",
      "title": "Zebra Guide",
      "tags": [
        "ref",
        "howto"
      ],
      "added_at": "2024-01-15T12:00:00+00:00",
      "visits": 0
    },
    {
      "id": 2,
      "url": "https://b.example.com/2",
      "title": "Beta Tools",
      "tags": [
        "howto"
      ],
      "added_at": "2024-01-15T12:00:01+00:00",
      "visits": 0
    },
    {
      "id": 3,
      "url": "https://c.example.com/3",
      "title": "Charlie Notes",
      "tags": [
        "ref"
      ],
      "added_at": "2024-01-15T12:00:02+00:00",
      "visits": 0
    },
    {
      "id": 4,
      "url": "https://d.example.com/4",
      "title": "delta reference",
      "tags": [
        "ref",
        "extra"
      ],
      "added_at": "2024-01-15T12:00:03+00:00",
      "visits": 0
    }
  ],
  "total": 4,
  "page": 1,
  "page_size": 15,
  "pages": 1
}
```

```
$ python cli.py list --page 2 --page-size 2
{
  "items": [
    {
      "id": 3,
      "url": "https://c.example.com/3",
      "title": "Charlie Notes",
      "tags": [
        "ref"
      ],
      "added_at": "2024-01-15T12:00:02+00:00",
      "visits": 0
    },
    {
      "id": 4,
      "url": "https://d.example.com/4",
      "title": "delta reference",
      "tags": [
        "ref",
        "extra"
      ],
      "added_at": "2024-01-15T12:00:03+00:00",
      "visits": 0
    }
  ],
  "total": 5,
  "page": 2,
  "page_size": 2,
  "pages": 3
}
```

(These two examples assume five bookmarks were added, in this order:
`https://a.example.com/1` "Zebra Guide" `ref`+`howto`,
`https://b.example.com/2` "Beta Tools" `howto`,
`https://c.example.com/3` "Charlie Notes" `ref`,
`https://d.example.com/4` "delta reference" `ref`+`extra`, and
`https://e.example.com/5` "apple five" with no tags - and none of them
has been visited.)

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`BookmarkError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                      |
|--------------|-----------|-------------------------------------------------|
| `validation` | 2         | bad input (bad url, bad sort/page/min-visits, ...) |
| `not_found`  | 3         | no bookmark with the given id                   |
| `storage`    | 4         | the bookmark file could not be read/written     |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly,
and it applies to every flag on every command, including the new `list`
flags above. A command that runs successfully but matches nothing (an
empty `list`, for instance) is **not** an error: it exits `0`.
