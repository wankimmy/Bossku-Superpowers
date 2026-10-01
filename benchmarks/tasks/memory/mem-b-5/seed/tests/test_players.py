import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from players import is_known_player


class PlayersTests(unittest.TestCase):
    def test_known_player(self):
        self.assertTrue(is_known_player("amy"))

    def test_unknown_player(self):
        self.assertFalse(is_known_player("zzz"))


if __name__ == "__main__":
    unittest.main()
