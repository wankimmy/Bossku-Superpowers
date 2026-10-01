import unittest

from notes_repo import NotesRepository


class NotesRepoHiddenTests(unittest.TestCase):
    def setUp(self):
        self.repo = NotesRepository()

    # ---- basic scoping sanity ----

    def test_get_notes_by_owner_scoped_correctly(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        self.repo.add_note("bob", "Trip", "pack bags", created_at=1)
        alice_notes = self.repo.get_notes_by_owner("alice")
        self.assertEqual(len(alice_notes), 1)
        self.assertEqual(alice_notes[0]["owner"], "alice")

    # ---- SQL injection ----

    def test_injection_quote_breakout_returns_empty(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        self.repo.add_note("bob", "Trip", "pack bags", created_at=1)
        result = self.repo.get_notes_by_owner("x' OR '1'='1")
        self.assertEqual(result, [])

    def test_injection_cross_owner_leak_blocked(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        self.repo.add_note("bob", "Trip", "pack bags", created_at=1)
        result = self.repo.get_notes_by_owner("alice' OR owner='bob")
        self.assertEqual(result, [])

    def test_search_quote_breakout_returns_empty(self):
        self.repo.add_note("alice", "Groceries", "milk, eggs", created_at=1)
        result = self.repo.search_notes("alice", "x' OR '1'='1")
        self.assertEqual(result, [])

    # ---- LIKE wildcard escaping ----

    def test_search_percent_literal(self):
        self.repo.add_note("carol", "PercentNote", "50% off today", created_at=1)
        self.repo.add_note("carol", "DecoyNote", "50xyz off today", created_at=2)
        result = self.repo.search_notes("carol", "50%")
        titles = [n["title"] for n in result]
        self.assertEqual(titles, ["PercentNote"])

    def test_search_underscore_literal(self):
        self.repo.add_note("dave", "UnderscoreNote", "a_b_test value", created_at=1)
        self.repo.add_note("dave", "UnderscoreDecoy", "axbxtest value", created_at=2)
        result = self.repo.search_notes("dave", "a_b_test")
        titles = [n["title"] for n in result]
        self.assertEqual(titles, ["UnderscoreNote"])

    # ---- sort_by allowlist ----

    def test_sort_by_allowlist_rejects_unknown_column(self):
        self.repo.add_note("alice", "A", "a", created_at=1)
        with self.assertRaises(ValueError):
            self.repo.list_notes_sorted("alice", "nonexistent_column_xyz")

    def test_sort_by_allowlist_rejects_injection_payload(self):
        self.repo.add_note("alice", "A", "a", created_at=1)
        with self.assertRaises(ValueError):
            self.repo.list_notes_sorted("alice", "id; DROP TABLE notes;--")
        # The table must still be fully intact and queryable afterwards.
        self.assertEqual(len(self.repo.get_notes_by_owner("alice")), 1)

    def test_sort_by_title_works(self):
        self.repo.add_note("alice", "Zebra", "z", created_at=1)
        self.repo.add_note("alice", "Apple", "a", created_at=2)
        result = self.repo.list_notes_sorted("alice", "title")
        self.assertEqual([n["title"] for n in result], ["Apple", "Zebra"])

    def test_sort_by_created_at_works(self):
        self.repo.add_note("alice", "Second", "s", created_at=20)
        self.repo.add_note("alice", "First", "f", created_at=10)
        result = self.repo.list_notes_sorted("alice", "created_at")
        self.assertEqual([n["title"] for n in result], ["First", "Second"])

    def test_sort_by_id_works(self):
        first_id = self.repo.add_note("alice", "First", "f", created_at=1)
        second_id = self.repo.add_note("alice", "Second", "s", created_at=1)
        result = self.repo.list_notes_sorted("alice", "id")
        self.assertEqual([n["id"] for n in result], [first_id, second_id])

    # ---- delete_note ownership and typing ----

    def test_delete_note_wrong_owner_rejected(self):
        note_id = self.repo.add_note("alice", "Secret", "shh", created_at=1)
        with self.assertRaises(KeyError):
            self.repo.delete_note("bob", note_id)
        self.assertEqual(len(self.repo.get_notes_by_owner("alice")), 1)

    def test_delete_note_nonexistent_id_rejected(self):
        with self.assertRaises(KeyError):
            self.repo.delete_note("alice", 999999)

    def test_delete_note_type_check_rejects_string(self):
        note_id = self.repo.add_note("alice", "A", "a", created_at=1)
        with self.assertRaises(TypeError):
            self.repo.delete_note("alice", str(note_id))

    def test_delete_note_type_check_rejects_injection_string(self):
        note_id = self.repo.add_note("alice", "Secret", "shh", created_at=1)
        with self.assertRaises(TypeError):
            self.repo.delete_note("bob", f"{note_id} OR owner='alice'")
        self.assertEqual(len(self.repo.get_notes_by_owner("alice")), 1)

    def test_delete_note_success_removes_only_that_note(self):
        keep_id = self.repo.add_note("alice", "Keep", "keep", created_at=1)
        gone_id = self.repo.add_note("alice", "Gone", "gone", created_at=2)
        self.repo.delete_note("alice", gone_id)
        remaining = self.repo.get_notes_by_owner("alice")
        self.assertEqual([n["id"] for n in remaining], [keep_id])

    # ---- normal use must still work ----

    def test_apostrophe_content_roundtrip(self):
        self.repo.add_note(
            "erin", "O'Brien's notes", "it's fine; drop nothing;", created_at=1
        )
        result = self.repo.get_notes_by_owner("erin")
        self.assertEqual(result[0]["title"], "O'Brien's notes")
        self.assertEqual(result[0]["body"], "it's fine; drop nothing;")

    def test_title_length_boundary_ok(self):
        title = "t" * 200
        self.repo.add_note("alice", title, "body", created_at=1)
        result = self.repo.get_notes_by_owner("alice")
        self.assertEqual(result[0]["title"], title)

    def test_title_length_exceeds_rejected(self):
        title = "t" * 201
        with self.assertRaises(ValueError):
            self.repo.add_note("alice", title, "body", created_at=1)

    def test_body_length_boundary_ok(self):
        body = "b" * 5000
        self.repo.add_note("alice", "title", body, created_at=1)
        result = self.repo.get_notes_by_owner("alice")
        self.assertEqual(result[0]["body"], body)

    def test_body_length_exceeds_rejected(self):
        body = "b" * 5001
        with self.assertRaises(ValueError):
            self.repo.add_note("alice", "title", body, created_at=1)

    def test_unicode_content_roundtrip(self):
        title = "日本語 😀"
        body = "café naïve 你好"
        self.repo.add_note("alice", title, body, created_at=1)
        result = self.repo.get_notes_by_owner("alice")
        self.assertEqual(result[0]["title"], title)
        self.assertEqual(result[0]["body"], body)


if __name__ == "__main__":
    unittest.main()
