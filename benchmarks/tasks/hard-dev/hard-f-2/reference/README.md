# contact-book

A tiny on-disk contact book. Contacts live in a single JSON file (default
`contacts.json`, next to the CLI) and are managed through `cli.py`.

Run the CLI with `python cli.py <command> ...`. Run the tests with
`python -m unittest discover -s tests`.

## Data model

Each contact has:

- `id` - positive integer, assigned by the repository. Ids are assigned
  once, in increasing order, and are **never reused**, even if the
  contact with the highest id is later deleted.
- `full_name` - non-empty string.
- `email` - `null`, or a string with exactly one `@` and a non-empty
  part on each side.
- `phone` - `null`, or digits (an optional leading `+`, spaces/dashes
  stripped out).
- `company` - `null`, or a non-empty string.
- `tags` - a list of strings (deduplicated, order-preserving).
- `created_at` - an ISO 8601 UTC timestamp, set once when the contact is
  created.

## Commands

- `add FULL_NAME [--email E] [--phone P] [--company C] [--tag TAG]*` -
  create a contact. Repeating `--tag` adds more than one tag.
- `show ID` - print one contact.
- `delete ID` - remove a contact.
- `tag ID TAG_NAME` - add a tag to a contact. Adding a tag the contact
  already has is a no-op (no duplicate, no error) - it's safe to call
  more than once with the same arguments.
- `list [search/filter/sort/paging - see below] [--format json]` -
  print contacts.
- `count` - print `{"count": <total number of contacts>}`. This always
  counts **every** contact in the file - it is completely unaffected by
  any search/filter given to `list`.

Every command that succeeds prints one JSON value
(`json.dumps(..., indent=2)`) to stdout and nothing else, and exits `0`.
`list`, `show`, and `count` are **read-only**: they never write to the
contact file.

Every returned contact (from `add`, `show`, `tag`, or `list`) is an
independent copy - nothing you do to the returned value (including
appending to its `tags` list) can change the stored contact.

### Example

```
$ python cli.py add "Ada Lovelace" --email ada@example.com --company Acme --tag vip
{
  "id": 1,
  "full_name": "Ada Lovelace",
  "email": "ada@example.com",
  "phone": null,
  "company": "Acme",
  "tags": [
    "vip"
  ],
  "created_at": "2024-01-15T12:00:00+00:00"
}
```

## Searching, filtering, sorting and paging `list`

`list` takes these optional flags, all validated the same way as any
other input in this project - an invalid one is a `validation` error
(exit `2`), not a crash and not an empty/silent result:

- `--q TEXT` - case-insensitive substring search. Matches a contact if
  `TEXT` is found in `full_name` **or** `email` **or** `company` (never
  `phone`) - that's an OR across those three fields, but it still
  combines with every other filter below using AND.
- `--tag TAG` (repeatable) - keep only contacts that have **every**
  given tag (it's an AND, not an OR).
- `--company NAME` - keep only contacts whose `company` matches `NAME`
  exactly, case-insensitively. `--company ""` (an explicit empty
  string) keeps only contacts with **no** company; leaving `--company`
  out entirely applies no company filter at all - those are different
  things.
- `--sort-by {id,created_at,name,company}` - sort key. Default (when
  not given) is `id`. `name` sorts by the **last word** of `full_name`,
  lowercased (so "Ada Lovelace" sorts under "lovelace") - not by the
  full string. `company` sorts case-insensitively, treating no company
  as `""` (sorts first).
- `--order {asc,desc}` - sort direction, default `asc`. Ties are always
  broken by `id` ascending, in both directions - `--order desc` only
  reverses the primary key, never the tie-break.
- `--page N` (default `1`) and `--page-size N` (default `25`, max `50`)
  - 1-based pagination, applied **after** searching/filtering and
  sorting. A page past the end returns an empty `items` list, not an
  error. `total` and `pages` always describe the whole matching set,
  the same on every page of it - not just the current page.

Searching/filtering, sorting, and pagination are applied in that order.

Giving **any** of the flags above switches `list`'s output from the
plain array it has always printed to a paginated envelope:

```
{"items": [...], "total": ..., "page": ..., "page_size": ..., "pages": ...}
```

using the defaults above for whichever of those flags weren't given.
This switch is based purely on whether one of those flags is *present
on the command line* - e.g. `list --order asc` still switches to the
envelope, even though `asc` is already the default, because `--order`
was given. `--format json` is the one exception: since it has never
affected `list`'s output (and `json` is its only accepted value),
it does not count, either way - `list --format json` alone still
prints the plain array, exactly as before.

### Examples

```
$ python cli.py list --company Acme --sort-by name
{
  "items": [
    {
      "id": 1,
      "full_name": "Ada Lovelace",
      "email": "ada@acme.io",
      "phone": null,
      "company": "Acme",
      "tags": [
        "vip"
      ],
      "created_at": "2024-01-15T12:00:00+00:00"
    },
    {
      "id": 2,
      "full_name": "Bob Zephyr",
      "email": "bob@example.com",
      "phone": null,
      "company": "acme",
      "tags": [
        "eng"
      ],
      "created_at": "2024-01-15T12:00:01+00:00"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 25,
  "pages": 1
}
```

```
$ python cli.py list --page 2 --page-size 2
{
  "items": [
    {
      "id": 3,
      "full_name": "Carol Analyst",
      "email": null,
      "phone": null,
      "company": "Zenith",
      "tags": [
        "vip",
        "eng"
      ],
      "created_at": "2024-01-15T12:00:02+00:00"
    },
    {
      "id": 4,
      "full_name": "Dana Admin",
      "email": null,
      "phone": null,
      "company": null,
      "tags": [],
      "created_at": "2024-01-15T12:00:03+00:00"
    }
  ],
  "total": 4,
  "page": 2,
  "page_size": 2,
  "pages": 2
}
```

(These two examples assume four contacts were added, in this order:
"Ada Lovelace" `ada@acme.io`/`Acme`/`vip`, "Bob Zephyr"
`bob@example.com`/`acme`/`eng`, "Carol Analyst" `Zenith`/`vip`+`eng`,
and "Dana Admin" with no email/company/tags.)

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`ContactBookError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                      |
|--------------|-----------|------------------------------------------------|
| `validation` | 2         | bad input (missing name, bad email/sort/page, ...) |
| `not_found`  | 3         | no contact with the given id                   |
| `storage`    | 4         | the contact file could not be read/written     |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly,
and it applies to every flag on every command, including the new `list`
flags above. A command that runs successfully but matches nothing (an
empty `list`, for instance) is **not** an error: it exits `0`.
