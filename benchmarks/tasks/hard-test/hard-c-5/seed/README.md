# redactor

Finds and masks emails and phone numbers in text before it gets logged,
stored, or shown to someone who shouldn't see it.

## Modules

- `redactor.py` — `redact(content, rules=DEFAULT_RULES)` redacts one piece
  of content according to a list of `RedactionRule`s, applied in order.
- `pipeline.py` — `scan_documents(documents, rules=...)` redacts a whole
  batch of documents in one call and totals up how many matches each rule
  found across the batch.
- `cli.py` — redacts a single file and prints the result plus a count of
  matches per rule. Files ending in `.bin` are read as raw bytes;
  everything else is read as text.

## Rules

Each `RedactionRule` has a `name`, a regular-expression `pattern`, and a
`mask` string that replaces every match. The default rules are:

| name  | matches                      | mask                |
|-------|-------------------------------|----------------------|
| email | `name@domain.tld`-shaped text | `[REDACTED-EMAIL]`   |
| phone | `###-###-####`-shaped text    | `[REDACTED-PHONE]`   |

## Example

```
$ cat note.txt
Reach Sam at sam@example.com.
$ python cli.py note.txt
redacted: Reach Sam at [REDACTED-EMAIL].
email: 1
phone: 0
```

## Running the tests

```
python -m unittest discover -s tests
```

The tests in `tests/` only cover the common cases — they're a starting
point, not full coverage.
