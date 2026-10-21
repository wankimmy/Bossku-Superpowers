"""Name the house design style when a prompt asks for UI.

Awwwards is the default design style (user decision, 2026-10-21). The router picks the skill; this one line makes
sure the style arrives even when the router picked a neighbour (site structure, a tenant-security skill for
"design a dashboard for tenant management") or nothing at all. Websites, landing pages and portfolios get the full
house rule; dashboards and app screens get its craft bar and keep native scroll.
"""

from __future__ import annotations

import re

_UI = re.compile(
    r"\b(?:landing ?pages?|websites?|web ?sites?|web ?design|homepages?|home ?pages?|portfolios?|hero|"
    r"(?:marketing|brand|launch|agency|studio|product|campaign) (?:site|page)s?|sites?|ui|ux|frontend|front-end|"
    r"interfaces?|layouts?|screens?|pages?|sections?|dashboards?|components?|laman(?: web)?|halaman|antaramuka)\b",
    re.I)
_MAKE = re.compile(
    r"\b(?:build|create|make(?! sure)|design|redesign|revamp|restyle|style|craft|prototype|mock ?up|generate|implement|"
    r"polish|beautify|buat(?:kan)?|bina(?:kan)?|reka|cantikkan|ubah ?suai)\b", re.I)
_PRODUCT = re.compile(
    r"\b(?:dashboards?|admin|back ?office|settings|data ?tables?|tables?|forms?|crud|app screens?|product ui|portal|"
    r"panel|analytics|internal tools?|onboarding flow|checkout)\b", re.I)
_WEB = re.compile(
    r"\b(?:landing|websites?|web ?sites?|web ?design|homepages?|home ?pages?|portfolios?|hero|marketing|brand|"
    r"launch|agency|studio|campaign|laman web|awwwards|award)\b", re.I)
# Work on the UI that is not design: a bug, a test, a deploy. The router still names a skill for it.
_NOT_DESIGN = re.compile(
    r"\b(?:tests?|testing|bugs?|crash(?:es|ing)?|stack ?trace|deploy(?:ing|ment)?|pipelines?|"
    r"ci|migrations?|seo audit|database|sql|postgres|mysql|schema|apis?|endpoints?)\b", re.I)

WEB_REMINDER = ("BosskuAI design default: Awwwards style. Load bosskuai-taste (the Awwwards house rule) and follow it "
                "unless the user or DESIGN.md names another style: concept and one signature moment first, finish "
                "with the jury self-score.")
PRODUCT_REMINDER = ("BosskuAI design default: the Awwwards craft bar for product UI. Follow bosskuai-ui-ux-design-to-code "
                    "with the product rules in bosskuai-taste: native scroll, no loader, no WebGL theatrics, unless the "
                    "user or DESIGN.md says otherwise.")


def design_reminder(prompt: str) -> str | None:
    """The house-style line for a request to make or restyle UI, or None."""
    text = prompt[:4000]
    if not ((_UI.search(text) or _PRODUCT.search(text)) and _MAKE.search(text)) or _NOT_DESIGN.search(text):
        return None
    if _PRODUCT.search(text) and not _WEB.search(text):
        return PRODUCT_REMINDER
    return WEB_REMINDER
