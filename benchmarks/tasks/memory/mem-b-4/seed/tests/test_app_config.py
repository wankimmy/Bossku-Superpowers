import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_config import signature_block


class AppConfigTests(unittest.TestCase):
    def test_signature_block_mentions_app_name(self):
        self.assertIn("NotifyPrototype", signature_block())


if __name__ == "__main__":
    unittest.main()
