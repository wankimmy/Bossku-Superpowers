"""Verify inbound webhook requests before trusting their payload."""
import hashlib
import hmac


SIGNATURE_HEADER = "X-Signature"
TIMESTAMP_HEADER = "X-Timestamp"


class WebhookVerificationError(Exception):
    """Raised when an inbound webhook fails signature checks."""


def verify_webhook(payload, headers, secret, *, now_fn=None):
    sig_header = headers.get(SIGNATURE_HEADER)
    ts_header = headers.get(TIMESTAMP_HEADER)
    if sig_header is None or ts_header is None:
        raise WebhookVerificationError("missing required headers")

    algo, _, hex_digest = sig_header.partition("=")
    try:
        hasher = getattr(hashlib, algo)
    except AttributeError:
        raise WebhookVerificationError(f"unknown algorithm: {algo}") from None

    signed_message = f"{ts_header}.".encode("utf-8") + payload
    expected = hmac.new(secret.encode("utf-8"), signed_message, hasher).hexdigest()

    if expected != hex_digest:
        raise WebhookVerificationError("signature mismatch")

    return True
