import unittest

from leaderboard import Leaderboard


class LeaderboardHiddenTests(unittest.TestCase):
    def make(self):
        board = Leaderboard()
        board.add_player("alice", 10)
        board.add_player("bob", 5)
        return board

    def test_add_player_default_score_zero(self):
        board = Leaderboard()
        board.add_player("zed")
        self.assertEqual(board.score_of("zed"), 0)

    def test_add_player_duplicate_raises(self):
        board = self.make()
        with self.assertRaises(ValueError):
            board.add_player("alice")

    def test_rankings_basic_order(self):
        board = self.make()
        self.assertEqual(board.rankings(), ["alice", "bob"])

    def test_rankings_tie_break_alphabetical(self):
        board = Leaderboard()
        board.add_player("zed", 10)
        board.add_player("amy", 10)
        board.add_player("mid", 10)
        self.assertEqual(board.rankings(), ["amy", "mid", "zed"])

    def test_record_score_updates_rankings_immediately(self):
        board = self.make()
        self.assertEqual(board.rankings(), ["alice", "bob"])  # populate the cache
        board.record_score("bob", 20)
        self.assertEqual(board.rankings(), ["bob", "alice"])

    def test_record_score_negative_points_updates_rankings(self):
        board = self.make()
        self.assertEqual(board.rankings(), ["alice", "bob"])  # populate the cache
        board.record_score("alice", -8)
        self.assertEqual(board.rankings(), ["bob", "alice"])

    def test_record_score_missing_player_raises(self):
        board = self.make()
        with self.assertRaises(KeyError):
            board.record_score("nobody", 5)

    def test_remove_player_updates_rankings_immediately(self):
        board = self.make()
        board.add_player("carol", 1)
        self.assertEqual(board.rankings(), ["alice", "bob", "carol"])  # populate the cache
        board.remove_player("alice")
        self.assertEqual(board.rankings(), ["bob", "carol"])

    def test_remove_player_missing_raises(self):
        board = self.make()
        with self.assertRaises(KeyError):
            board.remove_player("nobody")

    def test_reset_player_resets_score_and_updates_rankings(self):
        board = self.make()
        self.assertEqual(board.rankings(), ["alice", "bob"])  # populate the cache
        board.reset_player("alice")
        self.assertEqual(board.score_of("alice"), 0)
        self.assertEqual(board.rankings(), ["bob", "alice"])

    def test_reset_player_missing_raises(self):
        board = self.make()
        with self.assertRaises(KeyError):
            board.reset_player("nobody")

    def test_score_of_missing_raises(self):
        board = self.make()
        with self.assertRaises(KeyError):
            board.score_of("nobody")

    def test_top_truncates(self):
        board = self.make()
        board.add_player("carol", 1)
        self.assertEqual(board.top(2), ["alice", "bob"])

    def test_top_handles_n_larger_than_player_count(self):
        board = self.make()
        self.assertEqual(board.top(10), ["alice", "bob"])

    def test_top_reflects_update_after_record_score(self):
        board = self.make()
        self.assertEqual(board.top(1), ["alice"])  # populate the cache
        board.record_score("bob", 50)
        self.assertEqual(board.top(1), ["bob"])

    def test_top_reflects_update_after_remove_player(self):
        board = self.make()
        self.assertEqual(board.top(2), ["alice", "bob"])  # populate the cache
        board.remove_player("alice")
        self.assertEqual(board.top(2), ["bob"])


if __name__ == "__main__":
    unittest.main()
