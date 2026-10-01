# Cart Pricing Engine

Computes order totals with coupon codes.

Run tests: `python -m unittest discover -s tests`

## Money

All monetary amounts are exact to the cent. Whenever a calculation produces
a fraction of a cent, round **half up** to the nearest cent (so `2.625`
rounds to `2.63`, not `2.62`).

## Cart

- `Cart.add_item(sku, unit_price, quantity=1)` adds a line. If `sku` is
  already in the cart, the quantities are combined (`unit_price` must match
  the existing line's price, or a `ValueError` is raised).
- `Cart.subtotal()` returns the sum of `unit_price * quantity` across all
  lines, rounded half up to the cent.

## Coupon codes

Codes are matched **case-insensitively** and ignoring any leading/trailing
whitespace the customer typed (`"SAVE10 "`, `" save10"` and `"Save10"` are
all the same code).

Each code in the catalog is one of:

- a **percentage** code (e.g. 15% off the subtotal)
- a **fixed-amount** code (e.g. $5 off), never discounting below $0
- the **free-shipping** code `FREESHIP`

## Shipping

Shipping is a flat **$6.99**, except:

- it's always **$0.00 on an empty cart**, and
- it's **$0.00 whenever the cart's subtotal (before any discount) is
  $50.00 or more** — no code needed, or
- it's **$0.00 whenever the `FREESHIP` code is entered and recognized**,
  regardless of the subtotal.

## Stacking rules

A customer may enter more than one code at checkout. They combine as
follows:

- If more than one **percentage** code is entered, only the single best
  (highest percentage) one applies — percentage codes never stack with
  each other. If two entered percentage codes tie for best, the one that
  appears **earlier** in the entered list wins.
- If more than one **fixed-amount** code is entered, only the single best
  (largest amount) one applies — fixed-amount codes never stack with each
  other either. Ties break the same way: earlier entry wins.
- A percentage code and a fixed-amount code **do** combine: the percentage
  is applied to the subtotal first, then the fixed amount is subtracted
  from what's left (never going below $0 in total).
- `FREESHIP` combines with anything.
- Unknown codes (not in the catalog, even after normalizing case and
  whitespace) are silently ignored: no error, and they never appear on the
  receipt.

## Receipt

`build_receipt(cart, codes)` returns a dict:

```
{
  "subtotal": Decimal,       # before discount
  "discount": Decimal,       # total knocked off the subtotal
  "shipping": Decimal,       # 0.00 or 6.99, see "Shipping" above
  "total": Decimal,          # subtotal - discount + shipping
  "applied_codes": [...],    # see below
}
```

`applied_codes` lists, uppercased, the codes that matched the catalog and
were selected by the stacking rules above: the chosen percentage code (if
any), then the chosen fixed-amount code (if any), then `FREESHIP` (if it
was entered and recognized) — in that order, regardless of whether a given
code actually changed the final total (e.g. `FREESHIP` still shows up even
if the cart already qualified for free shipping by subtotal alone).
