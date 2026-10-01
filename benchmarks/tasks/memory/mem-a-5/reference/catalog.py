"""Helpers for maintaining a small product catalog."""

import re


def make_slug(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower())
    return slug.strip("-")


def add_product(catalog, name, price_cents):
    slug = make_slug(name)
    if slug in catalog:
        raise ValueError("product {!r} already in catalog".format(name))
    catalog[slug] = {"name": name, "price_cents": price_cents}
    return slug


def import_products(lines):
    catalog = {}
    for line in lines:
        name, price_cents = line.split(",")
        add_product(catalog, name.strip(), int(price_cents))
    return catalog


def merge_product_lists(list_a, list_b):
    catalog = {}
    for name, price_cents in list_a:
        catalog[make_slug(name)] = {"name": name, "price_cents": price_cents}
    for name, price_cents in list_b:
        catalog[make_slug(name)] = {"name": name, "price_cents": price_cents}
    return catalog
