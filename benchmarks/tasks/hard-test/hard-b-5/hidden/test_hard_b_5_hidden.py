import unittest

from acl.access import AccessControl
from acl.groups import Group


class AccessControlHiddenTests(unittest.TestCase):
    # ---- basics ----

    def test_default_is_deny(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        self.assertFalse(access.can("amy", "publish"))

    def test_direct_user_grant_allows(self):
        access = AccessControl()
        access.grant_user("amy", "publish")
        self.assertTrue(access.can("amy", "publish"))

    def test_group_grant_allows_all_members(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        access.add_member("staff", "ben")
        access.grant_group("staff", "publish")
        self.assertTrue(access.can("amy", "publish"))
        self.assertTrue(access.can("ben", "publish"))

    def test_group_rule_does_not_affect_non_members(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        access.grant_group("staff", "publish")
        self.assertFalse(access.can("carol", "publish"))

    def test_unknown_group_member_raises_keyerror(self):
        access = AccessControl()
        with self.assertRaises(KeyError):
            access.add_member("ghosts", "amy")

    def test_unknown_group_lookup_raises_keyerror(self):
        access = AccessControl()
        with self.assertRaises(KeyError):
            access.group("ghosts")

    def test_add_member_twice_does_not_duplicate(self):
        access = AccessControl()
        group = access.add_group("staff")
        access.add_member("staff", "amy")
        access.add_member("staff", "amy")
        self.assertEqual(group.members.count("amy"), 1)

    # ---- mutable default (defect) ----

    def test_new_group_has_own_empty_members(self):
        a = Group("a")
        a.add_member("amy")
        b = Group("b")
        self.assertEqual(b.members, [])

    # ---- case/whitespace normalization (defect) ----

    def test_group_and_user_lookup_case_and_whitespace_insensitive(self):
        access = AccessControl()
        access.add_group("Staff")
        access.add_member(" STAFF ", " Amy ")
        access.grant_group("staff", "Publish")
        self.assertTrue(access.can("AMY", " publish "))

    def test_duplicate_group_case_insensitive_raises(self):
        access = AccessControl()
        access.add_group("Staff")
        with self.assertRaises(ValueError):
            access.add_group(" staff ")

    # ---- inheritance ----

    def test_inheritance_is_transitive_through_three_levels(self):
        access = AccessControl()
        a = access.add_group("a")
        b = access.add_group("b")
        c = access.add_group("c")
        b.extend(a)
        c.extend(b)
        access.add_member("c", "amy")
        access.grant_group("a", "publish")
        self.assertTrue(access.can("amy", "publish"))

    def test_cycle_in_hierarchy_does_not_hang_and_still_resolves(self):
        access = AccessControl()
        a = access.add_group("a")
        b = access.add_group("b")
        a.extend(b)
        b.extend(a)  # cycle
        access.add_member("a", "amy")
        access.grant_group("a", "publish")
        self.assertTrue(access.can("amy", "publish"))

    # ---- precedence (defect) ----

    def test_group_deny_beats_group_allow_regardless_of_depth(self):
        access = AccessControl()
        editors = access.add_group("editors")
        suspended = access.add_group("suspended")
        editors.extend(suspended)
        access.add_member("editors", "amy")
        access.grant_group("editors", "publish")
        access.deny_group("suspended", "publish")
        self.assertFalse(access.can("amy", "publish"))

    def test_group_deny_beats_group_allow_from_two_direct_groups(self):
        access = AccessControl()
        access.add_group("editors")
        access.add_group("blocked")
        access.add_member("editors", "amy")
        access.add_member("blocked", "amy")
        access.grant_group("editors", "publish")
        access.deny_group("blocked", "publish")
        self.assertFalse(access.can("amy", "publish"))

    def test_direct_user_allow_beats_group_deny(self):
        access = AccessControl()
        access.add_group("blocked")
        access.add_member("blocked", "amy")
        access.deny_group("blocked", "publish")
        access.grant_user("amy", "publish")
        self.assertTrue(access.can("amy", "publish"))

    def test_direct_user_deny_beats_everything(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        access.grant_group("staff", "publish")
        access.grant_user("amy", "publish")
        access.deny_user("amy", "publish")
        self.assertFalse(access.can("amy", "publish"))

    # ---- cache invalidation (defect: add_member) ----

    def test_add_member_invalidates_cache_immediately(self):
        access = AccessControl()
        access.add_group("staff")
        access.grant_group("staff", "publish")
        self.assertFalse(access.can("amy", "publish"))  # populate cache as False
        access.add_member("staff", "amy")
        self.assertTrue(access.can("amy", "publish"))

    def test_grant_group_invalidates_cache_immediately(self):
        access = AccessControl()
        access.add_group("staff")
        access.add_member("staff", "amy")
        self.assertFalse(access.can("amy", "publish"))  # populate cache as False
        access.grant_group("staff", "publish")
        self.assertTrue(access.can("amy", "publish"))

    def test_deny_user_invalidates_cache_immediately(self):
        access = AccessControl()
        access.grant_user("amy", "publish")
        self.assertTrue(access.can("amy", "publish"))  # populate cache as True
        access.deny_user("amy", "publish")
        self.assertFalse(access.can("amy", "publish"))


if __name__ == "__main__":
    unittest.main()
