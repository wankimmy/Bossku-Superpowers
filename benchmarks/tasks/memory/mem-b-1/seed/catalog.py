"""Static catalog of known product SKUs for the warehouse."""

KNOWN_SKUS = {"SKU-1", "SKU-2", "SKU-3"}


def is_known_sku(sku):
    return sku in KNOWN_SKUS
