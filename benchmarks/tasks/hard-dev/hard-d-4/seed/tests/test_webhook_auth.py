import hashlib
import hmac
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webhook_auth import verify_webhook


class WebhookAuthHappyPathTests(unittest.TestCase):
    def test_valid_signature_is_accepted(self):
        secret = "topsecret"
        payload = b'{"event":"ping"}'
        ts = str(int(time.time()))
        signed_message = f"{ts}.".encode("utf-8") + payload
        digest = hmac.new(secret.encode(), signed_message, hashlib.sha256).hexdigest()
        headers = {"X-Signature": f"sha256={digest}", "X-Timestamp": ts}

        self.assertTrue(verify_webhook(payload, headers, secret))


if __name__ == "__main__":
    unittest.main()
