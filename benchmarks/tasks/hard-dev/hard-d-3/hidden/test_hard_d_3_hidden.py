import unittest

from url_fetcher import Redirect, URLSecurityError, fetch


class RecordingOpener:
    """Fake opener: records every URL it's called with, in order.

    `responses` maps a URL to either bytes (returned) or a Redirect
    instance (raised).
    """

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        # Fall back to a harmless sentinel for an unmapped URL rather than
        # raising KeyError, so a solution that wrongly calls the opener on
        # a URL it should have rejected surfaces as a clean assertion
        # failure instead of an error in this fixture.
        result = self.responses.get(url, b"unexpected-call")
        if isinstance(result, Redirect):
            raise result
        return result


class UrlFetcherHiddenTests(unittest.TestCase):
    # ---- scheme ----

    def test_rejects_scheme_ftp(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch("ftp://allowed.example.com/file", ["allowed.example.com"], opener)
        self.assertEqual(opener.calls, [])

    def test_rejects_scheme_file(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch(
                "file://allowed.example.com/etc/passwd",
                ["allowed.example.com"],
                opener,
            )
        self.assertEqual(opener.calls, [])

    def test_rejects_scheme_missing_host(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch("javascript:alert(1)", ["allowed.example.com"], opener)
        self.assertEqual(opener.calls, [])

    def test_allows_case_insensitive_scheme(self):
        url = "HTTPS://allowed.example.com/path"
        opener = RecordingOpener({url: b"ok"})
        result = fetch(url, ["allowed.example.com"], opener)
        self.assertEqual(result, b"ok")

    # ---- userinfo ----

    def test_rejects_userinfo_with_otherwise_allowed_host(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch(
                "http://user:pass@allowed.example.com/path",
                ["allowed.example.com"],
                opener,
            )
        self.assertEqual(opener.calls, [])

    def test_rejects_userinfo_host_confusion(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch(
                "http://allowed.example.com@evil.com/path",
                ["allowed.example.com"],
                opener,
            )
        self.assertEqual(opener.calls, [])

    # ---- host matching precision ----

    def test_rejects_host_suffix_confusion(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch(
                "http://example.com.evil.net/path",
                ["example.com", "api.example.com"],
                opener,
            )

    def test_rejects_host_prefix_confusion(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch(
                "http://notexample.com/path",
                ["example.com", "api.example.com"],
                opener,
            )

    def test_rejects_host_not_allowlisted_plain(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch("http://evil.com/path", ["example.com"], opener)

    def test_allows_exact_host_match(self):
        url = "http://example.com/path"
        opener = RecordingOpener({url: b"exact"})
        result = fetch(url, ["example.com", "api.example.com"], opener)
        self.assertEqual(result, b"exact")

    def test_allows_case_insensitive_host(self):
        url = "http://EXAMPLE.COM/path"
        opener = RecordingOpener({url: b"case-ok"})
        result = fetch(url, ["example.com"], opener)
        self.assertEqual(result, b"case-ok")

    def test_allows_trailing_dot_host(self):
        url = "http://example.com./path"
        opener = RecordingOpener({url: b"trailing-dot-ok"})
        result = fetch(url, ["example.com"], opener)
        self.assertEqual(result, b"trailing-dot-ok")

    def test_rejects_subdomain_not_explicitly_listed(self):
        opener = RecordingOpener({})
        with self.assertRaises(URLSecurityError):
            fetch("http://sub.example.com/path", ["example.com"], opener)

    def test_allows_other_explicit_allowlisted_host(self):
        url = "http://api.example.com/path"
        opener = RecordingOpener({url: b"api-ok"})
        result = fetch(url, ["example.com", "api.example.com"], opener)
        self.assertEqual(result, b"api-ok")

    def test_allows_port_is_ignored_for_match(self):
        url = "http://example.com:8443/path"
        opener = RecordingOpener({url: b"port-ok"})
        result = fetch(url, ["example.com"], opener)
        self.assertEqual(result, b"port-ok")

    # ---- redirects ----

    def test_redirect_to_allowed_host_followed(self):
        start = "http://example.com/start"
        final = "http://example.com/final"
        opener = RecordingOpener({start: Redirect(final), final: b"final-bytes"})
        result = fetch(start, ["example.com"], opener)
        self.assertEqual(result, b"final-bytes")
        self.assertEqual(opener.calls, [start, final])

    def test_redirect_to_disallowed_host_rejected(self):
        start = "http://example.com/start"
        evil = "http://evil.com/steal"
        opener = RecordingOpener({start: Redirect(evil)})
        with self.assertRaises(URLSecurityError):
            fetch(start, ["example.com"], opener)
        self.assertEqual(opener.calls, [start])

    def test_redirect_limit_boundary_allowed(self):
        urls = [f"http://example.com/hop{i}" for i in range(4)]
        responses = {urls[i]: Redirect(urls[i + 1]) for i in range(3)}
        responses[urls[3]] = b"done"
        opener = RecordingOpener(responses)
        result = fetch(urls[0], ["example.com"], opener)
        self.assertEqual(result, b"done")
        self.assertEqual(opener.calls, urls)

    def test_redirect_limit_exceeded_rejected(self):
        urls = [f"http://example.com/hop{i}" for i in range(5)]
        responses = {urls[i]: Redirect(urls[i + 1]) for i in range(4)}
        opener = RecordingOpener(responses)
        with self.assertRaises(URLSecurityError):
            fetch(urls[0], ["example.com"], opener)
        self.assertEqual(opener.calls, urls[:4])

    # ---- baseline ----

    def test_plain_fetch_no_redirect_single_call(self):
        url = "http://example.com/plain"
        opener = RecordingOpener({url: b"plain-bytes"})
        result = fetch(url, ["example.com"], opener)
        self.assertEqual(result, b"plain-bytes")
        self.assertEqual(opener.calls, [url])


if __name__ == "__main__":
    unittest.main()
