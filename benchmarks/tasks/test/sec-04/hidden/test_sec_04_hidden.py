import unittest

from tokens import TokenService, TokenError, InvalidTokenError, ExpiredTokenError


class FakeClock:
    def __init__(self, now=1000.0):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TokenServiceHiddenTests(unittest.TestCase):
    def test_issue_then_verify_round_trips_subject(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        token = svc.issue("alice")
        self.assertIsInstance(token, str)
        self.assertEqual(svc.verify(token), "alice")

    def test_token_still_valid_just_before_ttl(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        token = svc.issue("alice")
        clock.advance(29)
        self.assertEqual(svc.verify(token), "alice")

    def test_token_expired_after_ttl(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        token = svc.issue("alice")
        clock.advance(31)
        with self.assertRaises(ExpiredTokenError):
            svc.verify(token)

    def test_expired_token_error_is_a_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=10, clock=clock)
        token = svc.issue("alice")
        clock.advance(11)
        with self.assertRaises(TokenError):
            svc.verify(token)

    def test_tampered_signature_raises_invalid_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        token = svc.issue("bob")
        tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
        with self.assertRaises(InvalidTokenError):
            svc.verify(tampered)

    def test_truncated_token_raises_invalid_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        token = svc.issue("bob")
        with self.assertRaises(InvalidTokenError):
            svc.verify(token[:-1])

    def test_garbage_token_raises_invalid_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        with self.assertRaises(InvalidTokenError):
            svc.verify("not-a-real-token")

    def test_empty_token_raises_invalid_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        with self.assertRaises(InvalidTokenError):
            svc.verify("")

    def test_invalid_token_error_is_a_token_error(self):
        clock = FakeClock()
        svc = TokenService("key-v1", ttl=30, clock=clock)
        with self.assertRaises(TokenError):
            svc.verify("garbage")

    def test_token_signed_with_unrelated_key_is_invalid(self):
        clock = FakeClock()
        svc_a = TokenService("key-A", ttl=60, clock=clock)
        svc_z = TokenService("totally-different-key", ttl=60, clock=clock)
        token = svc_a.issue("carol")
        with self.assertRaises(InvalidTokenError):
            svc_z.verify(token)

    def test_rotated_key_still_verifies_old_tokens(self):
        clock = FakeClock()
        svc_old = TokenService("key-A", ttl=60, clock=clock)
        token = svc_old.issue("carol")
        svc_new = TokenService("key-B", previous_keys=["key-A"], ttl=60, clock=clock)
        self.assertEqual(svc_new.verify(token), "carol")

    def test_new_tokens_are_not_signed_with_previous_keys(self):
        clock = FakeClock()
        svc_new = TokenService("key-B", previous_keys=["key-A"], ttl=60, clock=clock)
        token = svc_new.issue("dave")
        svc_old_only = TokenService("key-A", ttl=60, clock=clock)
        with self.assertRaises(InvalidTokenError):
            svc_old_only.verify(token)

    def test_rotation_supports_multiple_previous_keys(self):
        clock = FakeClock()
        svc_v1 = TokenService("key-A", ttl=60, clock=clock)
        token_v1 = svc_v1.issue("erin")
        svc_v3 = TokenService("key-C", previous_keys=["key-A", "key-B"], ttl=60, clock=clock)
        self.assertEqual(svc_v3.verify(token_v1), "erin")

    def test_ttl_must_be_positive(self):
        with self.assertRaises(ValueError):
            TokenService("key", ttl=0)
        with self.assertRaises(ValueError):
            TokenService("key", ttl=-5)

    def test_expiry_uses_the_time_at_issuance_not_at_verification(self):
        clock = FakeClock(1000.0)
        svc = TokenService("key-v1", ttl=10, clock=clock)
        token = svc.issue("alice")
        clock.advance(5)
        second_token = svc.issue("bob")
        clock.advance(6)  # alice's token (age 11) expired; bob's (age 6) is not
        with self.assertRaises(ExpiredTokenError):
            svc.verify(token)
        self.assertEqual(svc.verify(second_token), "bob")


if __name__ == "__main__":
    unittest.main()
