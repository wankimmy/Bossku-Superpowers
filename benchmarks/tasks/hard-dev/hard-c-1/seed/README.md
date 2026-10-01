# chat-render

Tiny formatter that turns chat messages into fixed-width lines for a
terminal client. It's used by a couple of different front ends, so the
rendering rules live in one place and everything else just calls into it.

## Modules

- `render.py` — `render_message(author, text, timestamp, ...)` renders a
  single message as one display line: an optional timestamp prefix, the
  author name padded or truncated to a fixed width, and the message text,
  with the whole line truncated (with a trailing `...`) if it would
  otherwise run past the configured width.
- `history.py` — `render_history(messages, ...)` renders a whole list of
  messages (each a `{"author", "text", "timestamp"}` dict) by rendering
  each one and joining the results with newlines. It forwards its
  formatting options straight through to `render_message`.
- `cli.py` — a small command-line tool that replays a saved chat log
  through `render_message`, one line per message.

## Example

```python
from datetime import datetime
from render import render_message

render_message("alice", "hey, you around?", datetime(2024, 1, 1, 9, 30))
# "[09:30] alice       : hey, you around?"
```

## Log file format

`cli.py` reads a plain text log where each line is one message:

```
HH:MM|author|text
```

## Running the tests

```
python -m unittest discover -s tests
```

The tests in `tests/` only cover the common cases — they're a starting
point, not full coverage.
