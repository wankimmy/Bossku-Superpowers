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


class TokenService:
    def __init__(self, secret_key, *, previous_keys=(), ttl, clock=time.time):
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self._key = secret_key.encode("utf-8") if isinstance(secret_key, str) else secret_key
        self._previous_keys = previous_keys
        self._ttl = ttl
        self._clock = clock

    def _sign(self, message):
        return hmac.new(self._key, message, hashlib.sha256).hexdigest()

    def issue(self, subject):
        issued_at = self._clock()
        message = f"{subject}:{issued_at}".encode("utf-8")
        signature = self._sign(message)
        return f"{subject}:{issued_at}:{signature}"

    def verify(self, token):
        subject, issued_at_repr, signature = token.split(":", 2)
        message = f"{subject}:{issued_at_repr}".encode("utf-8")
        expected = self._sign(message)
        if signature != expected:
            raise InvalidTokenError("signature mismatch")
        if self._clock() >= float(issued_at_repr) + self._ttl:
            raise ExpiredTokenError("token has expired")
        return subject
