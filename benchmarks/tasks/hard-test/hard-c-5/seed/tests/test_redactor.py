import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from redactor import redact


class RedactorTests(unittest.TestCase):
    def test_redacts_email(self):
        result, counts = redact("contact me at a@b.com")
        self.assertEqual(result, "contact me at [REDACTED-EMAIL]")
        self.assertEqual(counts["email"], 1)

    def test_no_match_leaves_text_unchanged(self):
        result, counts = redact("nothing here")
        self.assertEqual(result, "nothing here")

    def test_redacts_phone_number(self):
        result, counts = redact("call 555-123-4567 soon")
        self.assertEqual(result, "call [REDACTED-PHONE] soon")
        self.assertEqual(counts["phone"], 1)

    def test_counts_cover_every_default_rule(self):
        _, counts = redact("nothing here")
        self.assertEqual(set(counts), {"email", "phone"})


if __name__ == "__main__":
    unittest.main()
