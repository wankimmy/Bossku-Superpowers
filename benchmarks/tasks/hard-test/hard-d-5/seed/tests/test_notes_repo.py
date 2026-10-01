import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notes_repo import NotesRepository


class NotesRepoHappyPathTests(unittest.TestCase):
    def setUp(self):
        self.repo = NotesRepository()

    def test_add_and_get_notes_by_owner(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        self.repo.add_note("alice", "Todo", "finish report", created_at=2)
        self.repo.add_note("bob", "Trip", "pack bags", created_at=1)

        alice_notes = self.repo.get_notes_by_owner("alice")
        self.assertEqual(len(alice_notes), 2)
        self.assertEqual(alice_notes[0]["title"], "Groceries")
        self.assertEqual(alice_notes[1]["title"], "Todo")

    def test_search_notes_finds_substring(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        results = self.repo.search_notes("alice", "milk")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Groceries")

    def test_delete_note_removes_it(self):
        note_id = self.repo.add_note("alice", "Temp", "delete me", created_at=1)
        self.repo.delete_note("alice", note_id)
        self.assertEqual(self.repo.get_notes_by_owner("alice"), [])


if __name__ == "__main__":
    unittest.main()
