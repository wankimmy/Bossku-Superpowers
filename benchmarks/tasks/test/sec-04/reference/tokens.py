"""Sign and verify short-lived tokens for logged-in users."""
import hashlib
import hmac
import time


class TokenError(Exception):
    """Base class for token problems."""


class InvalidTokenError(TokenError):
    """The token is malformed, or its signature does not match any known key."""


class ExpiredTokenError(TokenError):
    """The token's signature is fine, but it has expired."""


def _to_bytes(key):
    return key.encode("utf-8") if isinstance(key, str) else key


class TokenService:
    def __init__(self, secret_key, *, previous_keys=(), ttl, clock=time.time):
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self._key = _to_bytes(secret_key)
        self._old_keys = [_to_bytes(k) for k in previous_keys]
        self._ttl = ttl
        self._clock = clock

    @staticmethod
    def _sign(message, key):
        return hmac.new(key, message, hashlib.sha256).hexdigest()

    def issue(self, subject):
        issued_at = self._clock()
        message = f"{subject}:{issued_at}".encode("utf-8")
        signature = self._sign(message, self._key)
        return f"{subject}:{issued_at}:{signature}"

    def verify(self, token):
        try:
            subject, issued_at_repr, signature = token.split(":", 2)
            issued_at = float(issued_at_repr)
        except (ValueError, AttributeError):
            raise InvalidTokenError("malformed token") from None

        message = f"{subject}:{issued_at_repr}".encode("utf-8")
        if not any(hmac.compare_digest(self._sign(message, key), signature)
                   for key in (self._key, *self._old_keys)):
            raise InvalidTokenError("signature mismatch")

        if self._clock() >= issued_at + self._ttl:
            raise ExpiredTokenError("token has expired")
        return subject
