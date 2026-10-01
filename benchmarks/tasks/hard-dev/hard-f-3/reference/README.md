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
- `list [filters/sort/paging - see below] [--currency USD]` - print
  expenses.
- `count` - print `{"count": <total number of expenses>}`. This always
  counts **every** expense in the file - it is completely unaffected by
  any filter given to `list`.

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

## Filtering, sorting and paging `list`

`list` takes these optional flags, all validated the same way as any
other input in this project - an invalid one is a `validation` error
(exit `2`), not a crash and not an empty/silent result:

- `--category C` - keep only expenses in that category, matched
  case-insensitively. An empty string is rejected (there's no "no
  category" concept here - every expense has one).
- `--from DATE` / `--to DATE` - keep only expenses with `date >= DATE`
  (`--from`) and/or `date < DATE` (`--to`) - `--from` is **inclusive**,
  `--to` is **exclusive**. `--from` equal to `--to` therefore matches
  nothing (not an error). Both must be real `YYYY-MM-DD` dates.
- `--sort-by {id,date,amount,category}` - sort key. Default (when not
  given) is `id`. `category` sorts case-insensitively.
- `--order {asc,desc}` - sort direction, default `asc`. Ties are always
  broken by `id` ascending, in both directions - `--order desc` only
  reverses the primary key, never the tie-break.
- `--page N` (default `1`) and `--page-size N` (default `10`, max `50`)
  - 1-based pagination, applied **after** filtering and sorting. A page
  past the end returns an empty `items` list, not an error. `total`,
  `pages`, and `total_amount` always describe the whole filtered set,
  the same on every page of it - not just the current page.

Filtering, sorting, and pagination are applied in that order.

Giving **any** of the flags above switches `list`'s output from the
plain array it has always printed to a paginated envelope:

```
{"items": [...], "total": ..., "page": ..., "page_size": ..., "pages": ..., "total_amount": ...}
```

`total_amount` is the sum of every matching expense's `amount` - not
just the current page's - rounded with `money.round_money` (the same
rounding rule used when each expense was created). This switch is based
purely on whether one of the flags above is *present on the command
line* - e.g. `list --order asc` still switches to the envelope, even
though `asc` is already the default, because `--order` was given.
`--currency` is the one exception: since it has never affected `list`'s
output (this is a single-currency ledger), it does not count, either
way - `list --currency USD` alone still prints the plain array, exactly
as before.

### Examples

```
$ python cli.py list --category Food
{
  "items": [
    {
      "id": 1,
      "date": "2024-01-05",
      "category": "Food",
      "amount": 12.0,
      "note": null
    },
    {
      "id": 3,
      "date": "2024-01-15",
      "category": "Food",
      "amount": 8.5,
      "note": null
    },
    {
      "id": 4,
      "date": "2024-02-01",
      "category": "Food",
      "amount": 1.01,
      "note": null
    }
  ],
  "total": 3,
  "page": 1,
  "page_size": 10,
  "pages": 1,
  "total_amount": 21.51
}
```

```
$ python cli.py list --from 2024-01-10 --to 2024-01-20
{
  "items": [
    {
      "id": 2,
      "date": "2024-01-10",
      "category": "Travel",
      "amount": 19.13,
      "note": null
    },
    {
      "id": 3,
      "date": "2024-01-15",
      "category": "Food",
      "amount": 8.5,
      "note": null
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10,
  "pages": 1,
  "total_amount": 27.63
}
```

(These two examples assume five expenses were added, in this order:
2024-01-05 Food 12.00, 2024-01-10 Travel 19.125, 2024-01-15 Food 8.50,
2024-02-01 Food 1.005, and 2024-01-20 Travel 20.00. Note that the
second example's `--to 2024-01-20` excludes the fifth expense, dated
exactly `2024-01-20`.)

## Errors and exit codes

Every error raised anywhere in this project is an instance of
`LedgerError` (see `errors.py`); its text is always
`"<category>: <detail>"`. The CLI catches these and turns them into a
single stderr line `error: <category>: <detail>` plus a process exit
code, looked up from `constants.EXIT_CODES`:

| category     | exit code | meaning                                      |
|--------------|-----------|-------------------------------------------------|
| `validation` | 2         | bad input (bad date, non-positive amount, bad sort/page, ...) |
| `not_found`  | 3         | no expense with the given id                    |
| `storage`    | 4         | the expense file could not be read/written      |

Nothing is ever written to stdout when a command fails. `main()` (in
`cli.py`) always returns this exit code as a plain `int`; it never raises
one of the three exceptions above as uncaught, and never calls
`sys.exit` itself for them - that is what lets tests call it directly,
and it applies to every flag on every command, including the new `list`
flags above. A command that runs successfully but matches nothing (an
empty `list`, for instance) is **not** an error: it exits `0`.
