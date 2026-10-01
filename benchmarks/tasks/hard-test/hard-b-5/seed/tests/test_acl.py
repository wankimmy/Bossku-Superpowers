import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from acl.access import AccessControl


class AccessControlTests(unittest.TestCase):
    def test_default_is_deny(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        self.assertFalse(access.can("amy", "publish"))

    def test_group_grant_allows_member(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        access.grant_group("staff", "publish")
        self.assertTrue(access.can("amy", "publish"))

    def test_direct_user_deny_overrides_group_allow(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        access.grant_group("staff", "publish")
        access.deny_user("amy", "publish")
        self.assertFalse(access.can("amy", "publish"))

    def test_duplicate_group_raises(self):
        access = AccessControl()
        access.add_group("staff")
        with self.assertRaises(ValueError):
            access.add_group("staff")


if __name__ == "__main__":
    unittest.main()
