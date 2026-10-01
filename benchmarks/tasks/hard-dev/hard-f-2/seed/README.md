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
- `list [--format json]` - print every contact, `id` ascending.
  `--format` only ever accepts `json` (its default); output has always
  been JSON.
- `count` - print `{"count": <total number of contacts>}`.

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

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`ContactBookError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                 |
|--------------|-----------|-------------------------------------------|
| `validation` | 2         | bad input (missing name, bad email, ...)  |
| `not_found`  | 3         | no contact with the given id              |
| `storage`    | 4         | the contact file could not be read/written |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly.
A command that runs successfully but matches nothing (an empty `list`,
for instance) is **not** an error: it exits `0`.
