"""A tiny per-owner notes repository backed by an in-memory SQLite database."""
import sqlite3


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
        cur = self._conn.execute(
            f"INSERT INTO notes (owner, title, body, created_at) "
            f"VALUES ('{owner}', '{title}', '{body}', {created_at})"
        )
        self._conn.commit()
        return cur.lastrowid

    def get_notes_by_owner(self, owner):
        cur = self._conn.execute(
            f"SELECT id, owner, title, body, created_at FROM notes "
            f"WHERE owner = '{owner}' ORDER BY id ASC"
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def search_notes(self, owner, query_text):
        cur = self._conn.execute(
            f"SELECT id, owner, title, body, created_at FROM notes "
            f"WHERE owner = '{owner}' "
            f"AND (title LIKE '%{query_text}%' OR body LIKE '%{query_text}%') "
            f"ORDER BY id ASC"
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def list_notes_sorted(self, owner, sort_by):
        cur = self._conn.execute(
            f"SELECT id, owner, title, body, created_at FROM notes "
            f"WHERE owner = '{owner}' ORDER BY {sort_by} ASC"
        )
        return [self._row_to_dict(row) for row in cur.fetchall()]

    def delete_note(self, owner, note_id):
        cur = self._conn.execute(
            f"DELETE FROM notes WHERE id = {note_id} AND owner = '{owner}'"
        )
        self._conn.commit()
        if cur.rowcount == 0:
            raise KeyError(note_id)

    @staticmethod
    def _row_to_dict(row):
        return {
            "id": row[0],
            "owner": row[1],
            "title": row[2],
            "body": row[3],
            "created_at": row[4],
        }
