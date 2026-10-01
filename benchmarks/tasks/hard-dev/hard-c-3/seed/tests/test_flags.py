import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flags import FeatureFlags


class FlagsTests(unittest.TestCase):
    def test_enable_then_is_enabled(self):
        board = FeatureFlags()
        board.enable("beta")
        self.assertTrue(board.is_enabled("beta"))

    def test_unset_flag_is_false(self):
        board = FeatureFlags()
        self.assertFalse(board.is_enabled("nope"))

    def test_disable_then_is_enabled_false(self):
        board = FeatureFlags()
        board.enable("beta")
        board.disable("beta")
        self.assertFalse(board.is_enabled("beta"))

    def test_all_flags_reflects_state(self):
        board = FeatureFlags()
        board.enable("beta")
        self.assertEqual(board.all_flags(), {"beta": True})


if __name__ == "__main__":
    unittest.main()
