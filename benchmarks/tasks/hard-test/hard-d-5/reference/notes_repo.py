"""A tiny per-owner notes repository backed by an in-memory SQLite database."""
import sqlite3


MAX_TITLE_LEN = 200
MAX_BODY_LEN = 5000
SORTABLE_COLUMNS = {"id", "title", "created_at"}


class NotesRepository:
    def __init__(self):
        self._conn = sqlite3.connect(":memory:")
        self._conn.execute(
            "CREATE TABLE notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "owner TEXT NOT NULL, "
            "title TEXT NOT NULL, "
            "body TEXT NOT NULL, "
            "created_at INTEGER NOT NULL)"
        )
        self._conn.commit()

    def add_note(self, owner, title, body, created_at):
        if len(title) > MAX_TITLE_LEN:
            raise ValueError(f"title longer than {MAX_TITLE_LEN} characters")
        if len(body) > MAX_BODY_LEN:
            raise ValueError(f"body longer than {MAX_BODY_LEN} characters")
        cur = self._conn.execute(
            "INSERT INTO notes (owner, title, body, created_at) VALUES (?, ?, ?, ?)",
            (owner, title, body, created_at),
        )
        self._conn.commit()
        return cur.lastrowid

    def get_notes_by_owner(self, owner):
        cur = self._conn.execute(
            "SELECT id, owner, title, body, created_at FROM notes "
            "WHERE owner = ? ORDER BY id ASC",
            (owner,),
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def search_notes(self, owner, query_text):
        pattern = "%" + self._escape_like(query_text) + "%"
        cur = self._conn.execute(
            "SELECT id, owner, title, body, created_at FROM notes "
            "WHERE owner = ? "
            "AND (title LIKE ? ESCAPE '\\' OR body LIKE ? ESCAPE '\\') "
            "ORDER BY id ASC",
            (owner, pattern, pattern),
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def list_notes_sorted(self, owner, sort_by):
        if sort_by not in SORTABLE_COLUMNS:
            raise ValueError(f"cannot sort by {sort_by!r}")
        # Safe to interpolate now: sort_by can only be one of the three
        # literal, hard-coded column names checked above.
        cur = self._conn.execute(
            f"SELECT id, owner, title, body, created_at FROM notes "
            f"WHERE owner = ? ORDER BY {sort_by} ASC",
            (owner,),
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def delete_note(self, owner, note_id):
        if not isinstance(note_id, int) or isinstance(note_id, bool):
            raise TypeError("note_id must be an int")
        cur = self._conn.execute(
            "DELETE FROM notes WHERE id = ? AND owner = ?",
            (note_id, owner),
        )
        self._conn.commit()
        if cur.rowcount == 0:
            raise KeyError(note_id)

    @staticmethod
    def _escape_like(text):
        return (
            text.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )

    @staticmethod
    def _row_to_dict(row):
        return {
            "id": row[0],
            "owner": row[1],
            "title": row[2],
            "body": row[3],
            "created_at": row[4],
        }
