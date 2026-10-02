"""Helpers for tracking office IT assets.

Generated asset IDs follow ``<TYPE>-<6-digit-zero-padded-counter>`` with a
per-kind counter and a 2-letter type code (``OT`` for anything unlisted).
"""

TYPE_CODES = {
    "laptop": "LP",
    "monitor": "MN",
    "phone": "PH",
    "keyboard": "KB",
}
DEFAULT_TYPE_CODE = "OT"


class Asset:
    def __init__(self, asset_id, kind, owner):
        self.asset_id = asset_id
        self.kind = kind
        self.owner = owner


class AssetRegistry:
    def __init__(self):
        self._assets = []
        self._counters = {}

    def add(self, asset):
        if self.find(asset.asset_id) is not None:
            raise ValueError(f"asset_id already registered: {asset.asset_id}")
        self._assets.append(asset)

    def find(self, asset_id):
        for asset in self._assets:
            if asset.asset_id == asset_id:
                return asset
        return None

    def register_new(self, kind, owner):
        type_code = TYPE_CODES.get(kind, DEFAULT_TYPE_CODE)
        next_number = self._counters.get(type_code, 0) + 1
        self._counters[type_code] = next_number
        asset_id = f"{type_code}-{next_number:06d}"
        asset = Asset(asset_id, kind, owner)
        self.add(asset)
        return asset
