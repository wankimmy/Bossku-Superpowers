# notes_repo

A tiny per-owner notes store on top of an in-memory SQLite database.

```python
from notes_repo import NotesRepository

repo = NotesRepository()
note_id = repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
repo.get_notes_by_owner("alice")
repo.search_notes("alice", "milk")
repo.list_notes_sorted("alice", "title")
repo.delete_note("alice", note_id)
```

`created_at` is supplied by the caller (an integer sequence/sort key) rather
than generated internally, so callers - and tests - control ordering
exactly.

Run the visible tests: `python -m unittest discover -s tests`
