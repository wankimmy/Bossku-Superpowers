import unittest

from semver import parse, sort_versions


class ParseTests(unittest.TestCase):
    def test_parse_basic_core_only(self):
        v = parse("1.2.3")
        self.assertEqual((v.major, v.minor, v.patch), (1, 2, 3))
        self.assertEqual(v.prerelease, ())
        self.assertEqual(v.build, "")

    def test_parse_with_prerelease(self):
        v = parse("1.2.3-alpha.1")
        self.assertEqual(v.prerelease, ("alpha", 1))
        self.assertEqual(v.build, "")

    def test_parse_with_build(self):
        v = parse("1.2.3+build.5")
        self.assertEqual(v.prerelease, ())
        self.assertEqual(v.build, "build.5")

    def test_parse_with_prerelease_and_build(self):
        v = parse("2.0.0-rc.1+build.5")
        self.assertEqual((v.major, v.minor, v.patch), (2, 0, 0))
        self.assertEqual(v.prerelease, ("rc", 1))
        self.assertEqual(v.build, "build.5")

    def test_single_zero_prerelease_identifier_is_valid(self):
        v = parse("1.0.0-0")
        self.assertEqual(v.prerelease, (0,))

    def test_invalid_version_strings_raise(self):
        bad = [
            "01.2.3",       # leading zero in major
            "1.02.3",       # leading zero in minor
            "1.2",          # missing patch
            "a.2.3",        # non-numeric major
            "1.2.3-",       # empty prerelease section
            "1.2.3-alpha..1",  # empty identifier between dots
            "1.2.3-alpha.",    # trailing dot / empty identifier
            "1.0.0-al_pha",    # disallowed character
            "1.0.0-01",        # leading zero in numeric prerelease identifier
        ]
        for s in bad:
            with self.subTest(version=s):
                with self.assertRaises(ValueError):
                    parse(s)


class CompareTests(unittest.TestCase):
    def test_major_minor_patch_ordering(self):
        self.assertLess(parse("1.9.9"), parse("2.0.0"))
        self.assertLess(parse("1.2.3"), parse("1.2.4"))
        self.assertLess(parse("1.2.9"), parse("1.3.0"))

    def test_release_outranks_prerelease_of_same_core(self):
        self.assertGreater(parse("1.0.0"), parse("1.0.0-rc.1"))

    def test_numeric_prerelease_identifiers_compare_numerically(self):
        self.assertLess(parse("1.0.0-alpha.2"), parse("1.0.0-alpha.10"))

    def test_numeric_identifier_always_less_than_string_identifier(self):
        self.assertLess(parse("1.0.0-alpha.1"), parse("1.0.0-alpha.x"))

    def test_shorter_prerelease_with_shared_prefix_is_lesser(self):
        self.assertLess(parse("1.0.0-alpha"), parse("1.0.0-alpha.1"))

    def test_build_metadata_ignored_for_equality_and_ordering(self):
        self.assertEqual(parse("1.0.0+001"), parse("1.0.0+002"))
        self.assertEqual(parse("1.0.0-rc.1+aaa"), parse("1.0.0-rc.1+zzz"))
        self.assertFalse(parse("1.0.0+001") < parse("1.0.0+002"))
        self.assertFalse(parse("1.0.0+001") > parse("1.0.0+002"))


class SortVersionsTests(unittest.TestCase):
    def test_sort_versions_basic_ordering(self):
        versions = ["1.2.3", "1.0.0", "2.0.0-rc.1", "2.0.0", "1.0.0-alpha"]
        expected = ["1.0.0-alpha", "1.0.0", "1.2.3", "2.0.0-rc.1", "2.0.0"]
        self.assertEqual(sort_versions(versions), expected)

    def test_sort_versions_stable_on_ties_and_preserves_original_strings(self):
        versions = ["1.0.0+ccc", "1.0.0+aaa", "2.0.0"]
        expected = ["1.0.0+ccc", "1.0.0+aaa", "2.0.0"]
        self.assertEqual(sort_versions(versions), expected)


if __name__ == "__main__":
    unittest.main()
