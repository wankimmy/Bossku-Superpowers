import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from url_fetcher import URLSecurityError, fetch


class UrlFetcherHappyPathTests(unittest.TestCase):
    def test_fetches_allowed_host_via_fake_opener(self):
        calls = []

        def fake_opener(url):
            calls.append(url)
            return b"payload"

        result = fetch(
            "http://example.com/data",
            allowed_hosts=["example.com"],
            opener=fake_opener,
        )
        self.assertEqual(result, b"payload")
        self.assertEqual(calls, ["http://example.com/data"])

    def test_rejects_host_not_in_allowlist(self):
        def fake_opener(url):
            return b"should not be called"

        with self.assertRaises(URLSecurityError):
            fetch("http://evil.com/data", allowed_hosts=["example.com"], opener=fake_opener)


if __name__ == "__main__":
    unittest.main()
