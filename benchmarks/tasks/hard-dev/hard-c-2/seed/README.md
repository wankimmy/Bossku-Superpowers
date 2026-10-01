# password-strength

Scores how strong a password is and explains what's missing, for use in a
signup form's "strength meter" and in a batch audit tool for existing
accounts.

## Modules

- `checker.py` — `check_strength(password)` scores one password against a
  handful of fixed criteria (length, character classes) and returns which
  ones it failed.
- `report.py` — `summarize_one`/`summarize_many` turn a score into a
  human-readable line, and `rank_by_strength` orders a batch of passwords
  from strongest to weakest.
- `cli.py` — ranks a list of passwords given on the command line and
  prints a short report, headlined by the strongest one.

## Scoring

A password can earn up to 5 points, one for each of: being at least 12
characters long, containing a lowercase letter, containing an uppercase
letter, containing a digit, and containing a symbol. Any whitespace in the
password is treated as an automatic failure, regardless of anything else.

## Example

```
$ python cli.py "short1!" "Str0ngPassword!23"
strongest: Str0ngPassword!23 (5/5)
...
```

## Running the tests

```
python -m unittest discover -s tests
```

The tests in `tests/` only cover the common cases — they're a starting
point, not full coverage.
