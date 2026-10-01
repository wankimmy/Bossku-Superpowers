import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leaderboard import Leaderboard


class LeaderboardTests(unittest.TestCase):
    def setUp(self):
        self.board = Leaderboard()
        self.board.add_player("alice", 10)
        self.board.add_player("bob", 5)

    def test_rankings_update_after_record_score(self):
        self.assertEqual(self.board.rankings(), ["alice", "bob"])
        self.board.record_score("bob", 20)
        self.assertEqual(self.board.rankings(), ["bob", "alice"])

    def test_rankings_update_after_remove_player(self):
        self.board.add_player("carol", 1)
        self.assertEqual(self.board.rankings(), ["alice", "bob", "carol"])
        self.board.remove_player("alice")
        self.assertEqual(self.board.rankings(), ["bob", "carol"])

    def test_add_duplicate_raises(self):
        with self.assertRaises(ValueError):
            self.board.add_player("alice", 0)

    def test_score_of(self):
        self.assertEqual(self.board.score_of("alice"), 10)


if __name__ == "__main__":
    unittest.main()
