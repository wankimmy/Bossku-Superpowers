import re
import unittest

import assets

ID_PATTERN = re.compile(r"^(LP|MN|PH|KB|OT)-(\d{6})$")


class AssetAndRegistryFunctionalTests(unittest.TestCase):
    def test_asset_stores_fields_in_order(self):
        asset = assets.Asset("X-1", "laptop", "Mia")
        self.assertEqual(asset.asset_id, "X-1")
        self.assertEqual(asset.kind, "laptop")
        self.assertEqual(asset.owner, "Mia")

    def test_add_and_find(self):
        registry = assets.AssetRegistry()
        asset = assets.Asset("X-1", "laptop", "Mia")
        registry.add(asset)
        self.assertIs(registry.find("X-1"), asset)

    def test_add_raises_on_duplicate_id(self):
        registry = assets.AssetRegistry()
        registry.add(assets.Asset("X-1", "laptop", "Mia"))
        with self.assertRaises(ValueError):
            registry.add(assets.Asset("X-1", "monitor", "Noah"))

    def test_find_returns_none_when_missing(self):
        registry = assets.AssetRegistry()
        self.assertIsNone(registry.find("nope"))


class RegisterNewFunctionalTests(unittest.TestCase):
    def test_register_new_returns_an_asset(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("laptop", "Mia")
        self.assertIsInstance(asset, assets.Asset)
        self.assertEqual(asset.kind, "laptop")
        self.assertEqual(asset.owner, "Mia")

    def test_register_new_adds_to_registry(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("laptop", "Mia")
        self.assertIs(registry.find(asset.asset_id), asset)


class AssetIdFormatRuleTests(unittest.TestCase):
    """Project rule: generated IDs are '<TYPE>-<6-digit-counter>' with a
    per-kind counter, never uuid/random hex."""

    def test_laptop_id_matches_pattern_with_lp_code(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("laptop", "Mia")
        match = ID_PATTERN.match(asset.asset_id)
        self.assertIsNotNone(match, asset.asset_id)
        self.assertEqual(match.group(1), "LP")

    def test_monitor_phone_keyboard_type_codes(self):
        registry = assets.AssetRegistry()
        expected = {"monitor": "MN", "phone": "PH", "keyboard": "KB"}
        for kind, code in expected.items():
            asset = registry.register_new(kind, "Noah")
            match = ID_PATTERN.match(asset.asset_id)
            self.assertIsNotNone(match, asset.asset_id)
            self.assertEqual(match.group(1), code)

    def test_unknown_kind_uses_ot_code(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("desk-lamp", "Noah")
        self.assertTrue(asset.asset_id.startswith("OT-"))

    def test_counter_starts_at_one(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("laptop", "Mia")
        self.assertEqual(asset.asset_id, "LP-000001")

    def test_counter_increments_sequentially_per_type(self):
        registry = assets.AssetRegistry()
        ids = [registry.register_new("laptop", "Mia").asset_id for _ in range(4)]
        self.assertEqual(ids, ["LP-000001", "LP-000002", "LP-000003", "LP-000004"])

    def test_counters_are_independent_per_type(self):
        registry = assets.AssetRegistry()
        first_laptop = registry.register_new("laptop", "Mia")
        registry.register_new("monitor", "Noah")
        registry.register_new("monitor", "Noah")
        second_laptop = registry.register_new("laptop", "Mia")
        self.assertEqual(first_laptop.asset_id, "LP-000001")
        self.assertEqual(second_laptop.asset_id, "LP-000002")

    def test_generated_ids_are_six_digit_zero_padded(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("laptop", "Mia")
        number_part = asset.asset_id.split("-")[1]
        self.assertEqual(len(number_part), 6)
        self.assertTrue(number_part.isdigit())

    def test_no_duplicate_generated_ids_across_many_registrations(self):
        registry = assets.AssetRegistry()
        seen = set()
        for _ in range(10):
            asset = registry.register_new("laptop", "Mia")
            self.assertNotIn(asset.asset_id, seen)
            seen.add(asset.asset_id)

    def test_generated_id_does_not_look_like_a_uuid(self):
        registry = assets.AssetRegistry()
        asset = registry.register_new("phone", "Noah")
        # a uuid4 hex id would be far longer and contain more than one hyphen
        # (or none, if hex-only) -- our format is exactly TYPE-digits.
        self.assertEqual(asset.asset_id.count("-"), 1)
        self.assertLessEqual(len(asset.asset_id), 9)


if __name__ == "__main__":
    unittest.main()
