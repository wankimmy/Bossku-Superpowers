"""Name the design direction for the product type when a prompt asks for UI.

Owner decision (2026-11-17), narrowing the 2026-10-21 one: classify the product first. Showcase web gets the
Awwwards house rule; task-first public pages, product UI and consumer or mobile apps put familiarity first. The
router picks the skill; this one line makes sure the right direction arrives even when the router picked a
neighbour or nothing at all.
"""

from __future__ import annotations

import re

_UI = re.compile(
    r"\b(?:landing ?pages?|websites?|web ?sites?|web ?design|homepages?|home ?pages?|portfolios?|hero|"
    r"(?:marketing|brand|launch|agency|studio|product|campaign) (?:site|page)s?|sites?|ui|ux|frontend|front-end|"
    r"interfaces?|layouts?|screens?|pages?|sections?|dashboards?|components?|storefronts?|online (?:store|shop)s?|"
    r"checkout (?:flow|form|screen)s?|laman(?: web)?|halaman|antaramuka)\b",
    re.I)
_MAKE = re.compile(
    r"\b(?:build|create|make(?! sure)|design|redesign|revamp|restyle|style|craft|prototype|mock ?up|generate|implement|"
    r"polish|beautify|fix the (?:layout|design|ui|styling) of|"
    r"buat(?:kan)?|bina(?:kan)?|reka|cantikkan|ubah ?suai)\b", re.I)
# Maintenance verbs count only next to a screen word ("update the profile screen"), not a product noun alone
# ("update the admin password").
_CHANGE = re.compile(r"\b(?:improve|refactor|update)\b", re.I)
# A bare "app" is a UI request only with a platform word or a design verb ("update the app dependencies" is not).
_DESIGN_VERB = re.compile(r"\b(?:design|redesign|prototype|mock ?up|restyle|revamp|beautify)\b", re.I)
_SHOWCASE = re.compile(
    r"\b(?:landing ?pages?|web ?design|portfolios?|(?:marketing|brand|launch|agency|studio|campaign) (?:site|page|website)s?|"
    r"awwwards?)\b", re.I)
_WEBSITE = re.compile(r"\b(?:websites?|web ?sites?|home ?pages?|hero|laman(?: web)?)\b", re.I)
_MOBILE = re.compile(r"\b(?:mobile|ios|android|expo|react native|flutter|swiftui|native app|social app)\b", re.I)
_TASK = re.compile(r"\b(?:storefronts?|stores?|shops?|e-?commerce|checkouts?|booking|pricing|docs|documentation)\b", re.I)
# A strong product noun wins over a bare website word such as hero ("the SaaS dashboard hero metrics").
_STRONG = re.compile(
    r"\b(?:dashboards?|admin|back ?office|erp|crm|hrms?|saas|data ?tables?|internal tools?|panel|web ?apps?)\b", re.I)
_PRODUCT = re.compile(
    r"\b(?:dashboards?|admin|back ?office|erp|crm|hrms?|saas|data ?tables?|crud|product ui|portal|panel|analytics|"
    r"internal tools?|onboarding flow|settings|tables?|forms?|web ?apps?)\b", re.I)
_APP = re.compile(r"\bapps?\b", re.I)
# Screen nouns only, so "a landing page for our SaaS" stays showcase.
_SCREEN = re.compile(
    r"\b(?:dashboards?|admin|back ?office|(?:data ?)?tables?|internal tools?|panel|erp|crm|hrms?|forms?|screens?|skrin|"
    r"tabs?|trackers?|apps?|management systems?)\b", re.I)
# Work on the UI that is not design: a bug, a test, a deploy. The router still names a skill for it.
# A bare "pipeline" is left out on purpose: a sales pipeline is a CRM screen.
_NOT_DESIGN = re.compile(
    r"\b(?:tests?|testing|bugs?|crash(?:es|ing)?|stack ?trace|deploy(?:ing|ment)?|(?:build|data|release|etl) pipelines?|"
    r"ci|migrations?|seo audit|database|sql|postgres|mysql|schema|apis?|endpoints?|typescript|readme|redux|pinia|"
    r"validation|dependenc(?:y|ies)|performance|quer(?:y|ies)|faster|controllers?|seeders?|webhooks?|cli|env|"
    r"codeowners|cron|queue workers?|schedulers?|middleware|rate limit(?:ing|s)?|cach(?:e|es|ing)|nullable|sitemaps?|"
    r"form requests?|soft deletes?|load time|nginx|package\.json|service class(?:es)?|export jobs?)\b", re.I)

WEB_REMINDER = ("BosskuAI design direction: showcase web (marketing site, landing page, portfolio, campaign, agency). "
                "Load bosskuai-taste (the house rule): concept and one signature moment first, finish with the jury "
                "score on a public URL or a local production build, unless the user or DESIGN.md names another style. "
                "If the product type is unclear, say which type you assumed.")
TASK_REMINDER = ("BosskuAI design direction: task-first public page (storefront, checkout, booking, docs, pricing). "
                 "Familiar commerce and form patterns, native scroll, trust and clarity first; house craft for type, "
                 "spacing and imagery; no intro loader, no scroll theatre. Follow bosskuai-ui-ux-design-to-code. If the "
                 "product type is unclear, say which type you assumed.")
PRODUCT_REMINDER = ("BosskuAI design direction: product UI (SaaS, ERP/CRM/HRMS, dashboard, admin, internal tool, forms). "
                    "The project's own design system and component library first; familiar navigation and controls; "
                    "task efficiency; no concept card, no signature moment, no jury. Follow "
                    "bosskuai-ui-ux-design-to-code; the verdict is a task walkthrough, the state list, the layout "
                    "check and screenshots. If the product type is unclear, say which type you assumed.")
APP_REMINDER = ("BosskuAI design direction: consumer or mobile app. Follow platform conventions first (native navigation, back "
                "behaviour, safe areas, thumb reach, keyboard avoidance), then the product UI rules in "
                "bosskuai-ui-ux-design-to-code. Engagement features only as the engagement ethics checklist allows. "
                "If the product type is unclear, say which type you assumed.")
NEUTRAL_REMINDER = ("BosskuAI design direction: the product type is not clear from the request. Pick one (showcase web, "
                    "task-first public page, product UI, consumer or mobile app), say in one line which type you "
                    "assumed, and follow its rule. For existing UI, follow the project's own design system.")


def design_reminder(prompt: str) -> str | None:
    """The design-direction line for a request to make or change UI, or None."""
    text = prompt[:4000]
    surface = _UI.search(text) or _PRODUCT.search(text) or (
        _APP.search(text) and (_MOBILE.search(text) or _DESIGN_VERB.search(text)))
    verb = _MAKE.search(text) or (_CHANGE.search(text) and _UI.search(text))
    if not (surface and verb) or _NOT_DESIGN.search(text):
        return None
    if _SHOWCASE.search(text):
        return NEUTRAL_REMINDER if _SCREEN.search(text) else WEB_REMINDER
    if _MOBILE.search(text):
        return APP_REMINDER
    if _STRONG.search(text):
        return PRODUCT_REMINDER
    if _TASK.search(text):
        return TASK_REMINDER
    if _APP.search(text):
        return APP_REMINDER
    if _PRODUCT.search(text):
        return PRODUCT_REMINDER
    return WEB_REMINDER if _WEBSITE.search(text) else NEUTRAL_REMINDER
