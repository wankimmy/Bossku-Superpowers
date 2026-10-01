"""Turn a request into a short numbered list of requirements, so nothing in a long request is dropped.

Strong coding agents rarely fail because they cannot write the code. They fail because a request names a dozen
details and one of them (an error type, a tie-break, an edge case, a second call site) quietly gets lost. This
module reads a request and lists what it asks for. The list is shown when the request arrives and again, as an
audit, before the agent is allowed to finish. It reads text only; it never edits or runs anything.
"""

from __future__ import annotations

import re

MAX_ITEMS = 24
MAX_ITEM_CHARS = 220
MIN_WORDS = 4

BULLET = re.compile(r"^\s*(?:[-*•]|\d{1,2}[.)])\s+(.*\S)\s*$")
FENCE = re.compile(r"```.*?```", re.S)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"'(\[])")
# Words that make a sentence a requirement rather than background.
CUE = re.compile(
    r"\b(?:must|should|shall|need|needs|never|always|exactly|only|at most|at least|no more than|no less than|"
    r"raise[sd]?|return[sd]?|reject[sd]?|ignore[sd]?|default[sd]?|otherwise|unless|even if|ties?|order(?:ed|ing)?|"
    r"sort(?:ed)?|case|empty|duplicates?|negative|preserve[sd]?|keep|keeps|stay|stays|do(?:es)? not|don't|doesn't|"
    r"cannot|can't|without|before|after|each|every|both|neither|either|when|if|then|also|too|still|whether|"
    r"add|create|implement|make|support|update|replace|rename|remove|fix|change|move|split|accept|allow|handle|"
    r"validate|log|print|show|include|exclude|skip|treat|count|round|truncate|normalize|escape|wrap)\b"
    r"|`[^`]+`|\d",
    re.I)


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.strip("-*• ")
    if len(text) > MAX_ITEM_CHARS:
        cut = text[:MAX_ITEM_CHARS].rsplit(" ", 1)[0]
        text = cut.rstrip(",;:") + "…"
    return text


def _words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9_`]+", text))


def extract_requirements(prompt: str, *, minimum: int = 4) -> list[str]:
    """The requirements a request states, in order; an empty list when the request is too short to need one."""
    text = FENCE.sub(" [code] ", (prompt or "").replace("\r\n", "\n"))
    items: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph:
            return
        joined = " ".join(paragraph)
        paragraph.clear()
        for sentence in SENTENCE_END.split(joined):
            sentence = sentence.strip()
            if _words(sentence) >= MIN_WORDS and CUE.search(sentence):
                items.append(_clean(sentence))

    last_bullet = -1
    for raw in text.split("\n"):
        line = raw.rstrip()
        bullet = BULLET.match(line)
        if bullet:
            flush_paragraph()
            items.append(_clean(bullet.group(1)))
            last_bullet = len(items) - 1
        elif not line.strip():
            flush_paragraph()
            last_bullet = -1
        elif last_bullet >= 0 and raw[:1] in " \t":
            items[last_bullet] = _clean(items[last_bullet] + " " + line.strip())   # a wrapped bullet
        else:
            last_bullet = -1
            paragraph.append(line.strip())
    flush_paragraph()

    seen: set[str] = set()
    unique = []
    for item in items:
        key = item.lower()
        if item and key not in seen:
            seen.add(key)
            unique.append(item)
    unique = unique[:MAX_ITEMS]
    return unique if len(unique) >= minimum else []


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def request_list(items: list[str]) -> str:
    """What the agent sees when the request arrives."""
    return (f"BosskuAI requirement list ({len(items)} items found in your request). Cover every item, and check each "
            f"one and its edge cases before you finish:\n{numbered(items)}")


def audit_reason(items: list[str]) -> str:
    """What the agent is told, once, when it believes it is done."""
    return ("BosskuAI requirement audit: before you finish, go through every requirement below. For each one, name "
            "the code and the check (a test or a run) that covers it. Fix and re-run anything that is not covered, "
            "then finish with the list marked done or not done.\n" + numbered(items))
