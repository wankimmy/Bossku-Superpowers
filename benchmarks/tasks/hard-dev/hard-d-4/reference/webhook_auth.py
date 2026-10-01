"""Verify inbound webhook requests before trusting their payload."""
import hashlib
import hmac
import time


class WebhookVerificationError(Exception):
    """Raised when an inbound webhook fails signature or freshness checks."""


TOLERANCE_SECONDS = 300
SIGNATURE_HEADER = "X-Signature"
TIMESTAMP_HEADER = "X-Timestamp"


def verify_webhook(payload, headers, secret, *, now_fn=time.time):
    """Verify an inbound webhook. Returns True, or raises WebhookVerificationError."""
    sig_header = headers.get(SIGNATURE_HEADER)
    ts_header = headers.get(TIMESTAMP_HEADER)
    if sig_header is None:
        raise WebhookVerificationError("missing signature header")
    if ts_header is None:
        raise WebhookVerificationError("missing timestamp header")

    if "=" not in sig_header:
        raise WebhookVerificationError("malformed signature header")
    algo, _, hex_digest = sig_header.partition("=")
    if algo != "sha256":
        raise WebhookVerificationError(f"unsupported signature algorithm: {algo!r}")
    try:
        provided = bytes.fromhex(hex_digest)
    except ValueError:
        raise WebhookVerificationError("signature is not valid hex") from None

    try:
        timestamp = float(ts_header)
    except (TypeError, ValueError):
        raise WebhookVerificationError("timestamp is not numeric") from None

    now = now_fn()
    if abs(now - timestamp) > TOLERANCE_SECONDS:
        raise WebhookVerificationError("timestamp outside the allowed tolerance")

    signed_message = f"{ts_header}.".encode("utf-8") + payload
    expected = hmac.new(secret.encode("utf-8"), signed_message, hashlib.sha256).digest()

    if not hmac.compare_digest(provided, expected):
        raise WebhookVerificationError("signature mismatch")

    return True
