import ast
import inspect
import os
import unittest

import ratelimiter
from ratelimiter import KeyedRateLimiter, TokenBucket, peek, reset

BUILTIN_EXCEPTION_NAMES = {
    "ValueError", "KeyError", "TypeError", "IndexError", "AttributeError",
    "RuntimeError", "Exception", "StopIteration", "LookupError",
    "NotImplementedError", "ArithmeticError", "OSError", "AssertionError",
    "NameError",
}


def _source_tree():
    path = os.path.abspath(ratelimiter.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


def _bare_builtin_raises(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and node.exc is not None:
            target = node.exc
            if isinstance(target, ast.Call):
                target = target.func
            if isinstance(target, ast.Name) and target.id in BUILTIN_EXCEPTION_NAMES:
                yield target.id


class RateLimiterFunctionalityTests(unittest.TestCase):
    # ---- session 1: peek / reset ----

    def test_peek_does_not_consume(self):
        bucket = TokenBucket(5)
        bucket.allow()
        self.assertEqual(peek(bucket), 4)
        self.assertEqual(peek(bucket), 4)

    def test_peek_initial_equals_capacity(self):
        bucket = TokenBucket(3)
        self.assertEqual(peek(bucket), 3)

    def test_reset_restores_capacity(self):
        bucket = TokenBucket(5)
        bucket.allow(3)
        reset(bucket)
        self.assertEqual(peek(bucket), 5)

    # ---- session 2: KeyedRateLimiter ----

    def test_allow_per_key_independent(self):
        limiter = KeyedRateLimiter(2)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))
        self.assertTrue(limiter.allow("b"))

    def test_lazy_bucket_creation_uses_default_capacity(self):
        limiter = KeyedRateLimiter(3)
        limiter.allow("a")
        limiter.allow("a")
        limiter.allow("a")
        self.assertFalse(limiter.allow("a"))

    def test_set_capacity_before_use_changes_limit(self):
        limiter = KeyedRateLimiter(10)
        limiter.set_capacity("small", 2)
        self.assertTrue(limiter.allow("small"))
        self.assertTrue(limiter.allow("small"))
        self.assertFalse(limiter.allow("small"))

    def test_set_capacity_does_not_affect_other_keys(self):
        limiter = KeyedRateLimiter(10)
        limiter.set_capacity("small", 1)
        limiter.allow("small")
        self.assertTrue(limiter.allow("other"))


class ErrorHierarchyRuleTests(unittest.TestCase):
    """The project rule: invalid usage raises RateLimiterError subclasses
    from errors.py, never a bare builtin exception."""

    def test_errors_module_defines_root(self):
        import errors

        self.assertTrue(issubclass(errors.RateLimiterError, Exception))
        self.assertIsNot(errors.RateLimiterError, Exception)

    def test_all_exception_classes_in_errors_module_subclass_root(self):
        import errors

        for name, obj in vars(errors).items():
            if inspect.isclass(obj) and issubclass(obj, BaseException):
                if obj in (Exception, BaseException, errors.RateLimiterError):
                    continue
                self.assertTrue(
                    issubclass(obj, errors.RateLimiterError),
                    f"errors.{name} does not subclass RateLimiterError",
                )

    def test_set_capacity_on_reused_key_raises_rate_limiter_error(self):
        import errors

        limiter = KeyedRateLimiter(5)
        limiter.allow("a")
        with self.assertRaises(errors.RateLimiterError):
            limiter.set_capacity("a", 2)

    def test_set_capacity_invalid_value_raises_rate_limiter_error(self):
        import errors

        limiter = KeyedRateLimiter(5)
        with self.assertRaises(errors.RateLimiterError):
            limiter.set_capacity("fresh", -1)
        with self.assertRaises(errors.RateLimiterError):
            limiter.set_capacity("fresh2", 0)

    def test_no_bare_builtin_exceptions_raised_in_ratelimiter_module(self):
        tree = _source_tree()
        offenders = list(_bare_builtin_raises(tree))
        self.assertEqual(
            offenders, [],
            f"ratelimiter.py raises a bare builtin exception {offenders}; "
            "use a RateLimiterError subclass instead",
        )


if __name__ == "__main__":
    unittest.main()
