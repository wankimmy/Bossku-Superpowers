import hashlib
import hmac
import unittest
from unittest import mock

from webhook_auth import WebhookVerificationError, verify_webhook

SECRET = "topsecret"
FIXED_NOW = 1700000000.0


def _now():
    return FIXED_NOW


def _sign(secret, ts_str, payload, algo_name="sha256", hasher=hashlib.sha256):
    signed_message = f"{ts_str}.".encode("utf-8") + payload
    digest = hmac.new(secret.encode("utf-8"), signed_message, hasher).hexdigest()
    return f"{algo_name}={digest}"


def _headers(ts, payload, secret=SECRET, algo_name="sha256", hasher=hashlib.sha256):
    ts_str = str(ts)
    return {
        "X-Signature": _sign(secret, ts_str, payload, algo_name, hasher),
        "X-Timestamp": ts_str,
    }


class WebhookAuthHiddenTests(unittest.TestCase):
    def test_valid_signature_accepted(self):
        payload = b'{"event":"ping"}'
        headers = _headers(FIXED_NOW, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_return_value_is_true_on_success(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        result = verify_webhook(payload, headers, SECRET, now_fn=_now)
        self.assertIs(result, True)

    def test_tampered_payload_rejected(self):
        payload = b"original"
        headers = _headers(FIXED_NOW, payload)
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(b"tampered", headers, SECRET, now_fn=_now)

    def test_wrong_secret_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload, secret="othersecret")
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_missing_signature_header_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        del headers["X-Signature"]
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_missing_timestamp_header_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        del headers["X-Timestamp"]
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_malformed_signature_no_prefix_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        headers["X-Signature"] = headers["X-Signature"].split("=", 1)[1]
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_malformed_signature_bad_hex_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        headers["X-Signature"] = "sha256=not-hex-zzz"
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_algorithm_downgrade_sha1_rejected(self):
        payload = b"abc"
        # A cryptographically *correct* HMAC-SHA1 signature, properly signed
        # with the real secret - must still be rejected because sha256 is
        # the only algorithm this verifier is allowed to accept.
        headers = _headers(FIXED_NOW, payload, algo_name="sha1", hasher=hashlib.sha1)
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_timestamp_too_old_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW - 301, payload)
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_timestamp_too_new_rejected(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW + 301, payload)
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_timestamp_boundary_allowed_past(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW - 300, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_timestamp_boundary_allowed_future(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW + 300, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_non_numeric_timestamp_rejected(self):
        payload = b"abc"
        ts_str = "banana"
        headers = {
            "X-Signature": _sign(SECRET, ts_str, payload),
            "X-Timestamp": ts_str,
        }
        with self.assertRaises(WebhookVerificationError):
            verify_webhook(payload, headers, SECRET, now_fn=_now)

    def test_uses_constant_time_compare(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        with mock.patch(
            "webhook_auth.hmac.compare_digest", wraps=hmac.compare_digest
        ) as spy:
            self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))
        self.assertTrue(spy.called)

    def test_case_insensitive_hex_signature_accepted(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        algo, _, hexpart = headers["X-Signature"].partition("=")
        headers["X-Signature"] = f"{algo}={hexpart.upper()}"
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_raw_bytes_payload_used_exactly(self):
        payload = b'{"a": 1,   "b": 2}\n'
        headers = _headers(FIXED_NOW, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_empty_payload_handled(self):
        payload = b""
        headers = _headers(FIXED_NOW, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_unicode_payload_handled(self):
        payload = "café ☃".encode("utf-8")
        headers = _headers(FIXED_NOW, payload)
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))

    def test_extra_unrelated_headers_ignored(self):
        payload = b"abc"
        headers = _headers(FIXED_NOW, payload)
        headers["Content-Type"] = "application/json"
        headers["X-Request-Id"] = "abc-123"
        self.assertTrue(verify_webhook(payload, headers, SECRET, now_fn=_now))


if __name__ == "__main__":
    unittest.main()
