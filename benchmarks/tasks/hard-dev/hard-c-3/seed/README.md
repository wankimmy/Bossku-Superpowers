# feature-flags

In-memory feature flag registry used to gate experimental code paths
without a config deploy. It's intentionally simple - no persistence, no
remote config service, just a process-local on/off switch per flag name.

## Modules

- `flags.py` — the `FeatureFlags` class, plus module-level convenience
  functions (`enable`, `disable`, `is_enabled`, `all_flags`) that operate
  on one shared instance for the whole process. Most call sites just use
  the module-level functions and never touch `FeatureFlags` directly.
- `gating.py` — `run_if_enabled(name, func, *args, **kwargs)` runs `func`
  only if the named flag is on, and otherwise does nothing.
- `reporting.py` — `build_report()` formats the current flag state as
  plain text, for logging or an admin page.
- `cli.py` — a command-line front end for all of the above: enable a
  flag, disable one, or list the current state.

## Example

```
$ python cli.py enable new_checkout
enabled new_checkout
$ python cli.py list
new_checkout: ON
```

## Running the tests

```
python -m unittest discover -s tests
```

The tests in `tests/` only cover the common cases — they're a starting
point, not full coverage.
