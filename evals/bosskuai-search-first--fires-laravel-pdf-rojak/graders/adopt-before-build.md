---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Names at least one existing, widely used way to make PDFs in Laravel (for example barryvdh/laravel-dompdf, or spatie/laravel-pdf with Browsershot).
- Advises checking maintenance, license and Laravel/PHP version support before adopting.
- Recommends a package over custom PDF code, with a first integration step (for example install it, render a Blade view of the invoice, return it from a download route).
- Fits the user's language (BM/rojak or simple English).

Pass only if every point holds.
