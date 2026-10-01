# expense-ledger

A tiny on-disk expense ledger. Expenses live in a single JSON file
(default `expenses.json`, next to the CLI) and are managed through
`cli.py`.

Run the CLI with `python cli.py <command> ...`. Run the tests with
`python -m unittest discover -s tests`.

## Data model

Each expense has:

- `id` - positive integer, assigned by the repository. Ids are assigned
  once, in increasing order, and are **never reused**, even if the
  expense with the highest id is later deleted.
- `date` - a `"YYYY-MM-DD"` string that must be a real calendar date.
- `category` - non-empty string. Its original case is kept in storage;
  matching it (see below) is case-insensitive.
- `amount` - a positive number, rounded to the nearest cent with
  `money.round_money` at creation time (see `money.py` for exactly how -
  it is **not** the same as Python's built-in `round()`). Once rounded
  there, an amount is never rounded differently anywhere else in this
  project - any later total must reuse `round_money` too.
- `note` - a string, or `null`.

## Commands

- `add DATE CATEGORY AMOUNT [--note N]` - record an expense.
- `show ID` - print one expense.
- `recategorize ID NEW_CATEGORY` - change an expense's category. Setting
  it to the category it already has is a no-op (no error) - it's safe
  to call more than once with the same arguments.
- `delete ID` - remove an expense.
- `list [--currency USD]` - print every expense, `id` ascending.
  `--currency` only ever accepts `USD` (its default); this is a
  single-currency ledger, so the flag has never changed anything.
- `count` - print `{"count": <total number of expenses>}`.

Every command that succeeds prints one JSON value
(`json.dumps(..., indent=2)`) to stdout and nothing else, and exits `0`.
`list`, `show`, and `count` are **read-only**: they never write to the
expense file.

Every returned expense (from `add`, `show`, `recategorize`, or `list`)
is an independent copy - nothing you do to the returned value can
change the stored expense.

### Example

```
$ python cli.py add 2024-01-15 Travel 19.125 --note "taxi, converted from EUR"
{
  "id": 1,
  "date": "2024-01-15",
  "category": "Travel",
  "amount": 19.13,
  "note": "taxi, converted from EUR"
}
```

(`19.125` rounds up to `19.13` - see `money.py`.)

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`LedgerError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                      |
|--------------|-----------|-------------------------------------------------|
| `validation` | 2         | bad input (bad date, non-positive amount, ...)  |
| `not_found`  | 3         | no expense with the given id                    |
| `storage`    | 4         | the expense file could not be read/written      |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly.
A command that runs successfully but matches nothing (an empty `list`,
for instance) is **not** an error: it exits `0`.
