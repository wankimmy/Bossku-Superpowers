"""Spot a message in which the user states a rule that should outlive the request.

Remembering a project rule only works when somebody saves it, and in the two-session tests models differ a lot in whether
they do so on their own (docs/benchmarks/README.md). A stated rule often has
telltale wording ("from now on", "our team rule", "we decided", "we never ..."), so the prompt hook points it out and
the stop hook sends the agent back once, with the exact command, if it never saved it.

Wording is only a proxy, and it was measured, not assumed. Other agents wrote and labelled messages blind (data and
scoring script: benchmarks/rules-eval, scripts/benchmark_rules.py). On a set the cues were not tuned on, the current
rules catch about a third of the stated rules and wrongly flag about 4% of the non-rules; the figures are in
docs/memory.md. Earlier sets, whose data was lost, showed the same pattern: a phrase list tuned on its own examples
scores near 100% and falls to 40-60% on new wording. A requirement for the one thing being built
("it must never mutate its input") is not a rule for the project, and a wrong reminder costs the agent a turn, so
both reminders say "if" and let the agent finish when no rule was stated.
"""

from __future__ import annotations

import re

_SENTENCE = r"[^.!?\n]{0,80}"
_NEAR = r"[^.!?\n]{0,60}"
# Whitespace after punctuation is bounded: an unbounded run made the scan quadratic on thousands of blank lines.
_GAP = r"[ \t]{0,3}"
_ARTIFACT = (r"(?:code|modules?|functions?|files?|endpoints?|classes|tests?|features?|scripts?|tools?|components?|"
             r"(?:sql )?migrations?|prs?|services?|packages?|dependencies|routes?|apis?|tables?|screens?|pages?|"
             r"commits?|branches|models?|handlers?|hooks?)\b")

CUES = re.compile("|".join([
    r"\bfrom (?:now|here|this point|today) on(?:ward|wards)?\b",
    r"\b(?:going|moving) forward\b",
    r"\bstarting (?:now|today|from now)\b",
    r"\b(?:our|the|my|one|a|this) (?:team|project|company|org|repo|house|coding|style|api|code|logging|naming|testing|"
    r"branching|commit) (?:rules?|polic(?:y|ies)|conventions?|standards?|guidelines?)\b",
    r"\bwhenever (?:this|the|our) (?:project|repo|repository|codebase|service|app|module|package)\b",
    r"\bheads[- ]up for later\b", r"\bone important thing\b", r"\bplease (?:never(?! mind)|always|don'?t ever)\b",
    r"(?<!least )\b(?:one|a|new) rule (?:for (?:this|the|all|every|each|our|any|everything|anything|new)"
    r"|of the|here|going|from|that (?:applies|we)|to follow)\b",
    r"(?<!least )\b(?:one|a|new) rule:",
    r"\b(?:ground|hard|strict|golden|house) rules?\b",
    r"\brule of thumb\b",
    r"\bwe (?:always|never|decided|agreed|settled|standardi[sz]ed|no longer|stopped|switched|banned|dropped)\b",
    r"\bwe(?:'ve| have) (?:decided|agreed|settled|standardi[sz]ed|switched|banned|dropped)\b",
    r"\b(?:it|that) was decided\b",
    r"\bfor (?:everything|anything|all|every) (?:new|we|that|you|future)\b",
    r"\ball (?:new|future) " + _ARTIFACT,
    r"\bevery (?:new|future) " + _ARTIFACT,
    r"\b(?:never|don'?t ever|do not ever|always|must|should only|only)" + _SENTENCE +
    r"\b(?:in|across|throughout) (?:this|the|our) (?:repo|repository|codebase|code base|project|package|module|app|service)\b",
    r"\b(?:in|across|throughout) (?:this|the|our) (?:repo|repository|codebase|code base|project|package)" +
    _SENTENCE + r"\b(?:never|always|must|only)\b",
    r"\bacross the (?:codebase|repo|project|board)\b" + _NEAR + r"\b(?:let'?s|we|always|never|must|only|should)\b",
    r"\bheads[- ]up (?:for|on|untuk) (?:the )?(?:whole|entire|rest|this|seluruh)\b",
    # A policy named as one: "Team policy:", "Standing rule:", "Our logging standard is ...", "a small rule for the repo"
    r"(?<!content )(?<!content-)\b(?:team|company|standing|house|firm|org|engineering|security|coding)[- ](?:wide )?"
    r"(?:policy|rule|instruction|practice|standard|convention|guideline)s?\b",
    r"\b(?:small|simple|quick|tiny|little|standing|firm|housekeeping) (?:housekeeping )?"
    r"(?:rule|policy|convention|guideline)s?\b",
    r"\bour (?:rule|convention|policy|standard)s? (?:is|are)\b",
    r"\b(?:company|org|team)-wide\b", r"\bstandard practice\b",
    r"\bnon-negotiable\b", r"\bno exceptions\b", r"\bfull stop\b", r"\bthat'?s (?:the|our) (?:rule|policy)\b",
    r"\bthat'?s firm\b", r"\bso we'?re aligned\b", r"\bkeep following\b",
    r"\b(?:branch|file|variable|function|class|commit|table|column|test) names? (?:must|should|need to|have to)\b",
    r"\bstanding (?:thing|note|order|reminder)\b",
    # A label in front of the rule: "Rule for this repo: ...", "Environment rule: ...", "Team decision: ...", "Decision: ..."
    r"(?:^|\n|[.!?]" + _GAP + r")(?:[a-z]+ )?(?:rule|policy|decision|convention|standard|guideline)"
    r"(?: (?:for|from) [^:.!?\n]{1,40})?:",
    # Carry on as before, or from now on in other words
    r"\b(?:keep|continue) (?:doing|following)\b", r"\b(?:make it|keeping this as|as a) policy\b",
    r"\bas a baseline\b", r"\b(?:i want us to|let'?s|we should|we need to|we must) (?:always|never)\b",
    r"\bfor future (?:PRs?|work|code|changes|commits|tickets|features)\b",
    r"\bthat'?s (?:just )?how (?:it is|we do|things work)\b", r"\bthat'?s been the (?:convention|gate|rule|policy|standard|practice)\b",
    r"\bsince day one\b", r"\b(?:just )?agreed (?:with|as|on|in)\b", r"\bwe (?:require|pin|cap|enforce|mandate|follow)\b",
    r"\bwe don'?t support\b",
    r"\bour (?:commit messages|branch(?:es)?|PRs?|pull requests|tests|CI|builds?|releases?|deploys?|code reviews?|"
    r"migrations?|logs?|branch protection rule) (?:must|should|need|require)",
    # A decision: "Decided not to adopt ...", "Team decided against ...", "Decision from last retro"
    r"(?:^|\n|[.!?:]" + _GAP + r")decided\b", r"\b(?:team|everyone|management|leadership) (?:decided|agreed)\b",
    r"\bdecision (?:from|in|at|of|made)\b", r"\bdecided (?:not to|against|in standup|this morning|in the)\b",
    # Habits and bans: "Don't ever ...", "We don't write raw SQL", "Nobody merges their own PR", "no more console.log"
    r"\bdon'?t ever\b", r"\bdo not ever\b",
    r"\bwe (?:don'?t|do not) (?:ever )?(?:use|write|let|allow|ship|merge|commit|accept|add|put|store|log|touch|skip|push)\b",
    r"\bwe keep (?:everything|all|our|the)\b", r"\b(?:nobody|no one) (?:merges|ships|pushes|commits|deploys)\b",
    r"(?:^|[,;:.!?—–-]" + _GAP + r")no more (?!than\b|pages?\b|items?\b|results?\b|data\b|rows?\b)\w+",
    r"\b(?:anything|everything) (?:touching|that touches)\b" + _NEAR + r"\b(?:needs?|must|has to|goes|go through|requires?|should)\b",
    r"\bany (?:PR|pull request)s?\b" + _NEAR + r"\b(?:needs?|must|has to|requires?|should)\b",
    # Malay, as written by Malaysian developers
    r"\blepas ni\b", r"\bmulai sekarang\b", r"\bdari sekarang\b", r"\bperaturan (?:kita|team|projek|kami)\b",
    r"\bkita (?:dah |telah )?(?:decide|putuskan|sepakat|setuju|agree)\b", r"\brule ni\b", r"\bdah tetapkan\b",
    r"\bconvention kita\b",
]), re.IGNORECASE)


# Phrases alone reach about half of the ways people state a rule, so a sentence also counts when a group ("we", "our
# team", "kita", "nobody") is paired with an act or ban within a few words and an absolute ("never", "only") sits in
# the same sentence, or when a rule word ("policy", "convention", "per our") comes with an owner and an absolute.
# "all" and "must" are not absolutes here: "we can run all the tests" and "it must retry" are requests, not rules.
_ACT = (r"(?:never|always|no longer|don'?t|do not|can'?t|cannot|stopped|dropped|banned|decided|agreed|"
        r"require[sd]?|moved|switched|migrated|keep(?! \w+ing\b)|pin|treat|guna|adopt(?:ed|ing)|standardi[sz]ed|locked|stuck|"
        r"target|support|allow|ship|merge|commit|store|log|write|use|expose|call|run|stay|are on|is on|"
        r"jangan|tak boleh|dah)")
_GROUP_DOES = re.compile(r"\b(?:we|we're|we've|kita|kami|nobody|no one|everyone|everybody|our team|the team|the company|"
                         r"this (?:repo|project|codebase|service|app)) (?:\S+ ){0,2}?" + _ACT + r"\b", re.IGNORECASE)
_RULE_WORD = re.compile(r"\b(?:policy|rule|convention|standard|guideline|decision|non-negotiable|house style|"
                        r"dasar|polisi|peraturan|per our|per the team)\b", re.IGNORECASE)
_OWNER = re.compile(r"\b(?:we|our|kita|kami|team|company|org|house|everyone|nobody|no one|per)\b", re.IGNORECASE)
_ABSOLUTE = re.compile(r"\b(?:never|always|only|no longer|anymore|banned|forbidden|deprecated|not allowed|"
                       r"no exceptions|jangan|tak boleh|mesti|kena)\b", re.IGNORECASE)
_SENTENCES = re.compile(r"[.!?\n;]|\s[-—–]\s")
_SCAN_LIMIT = 6000
# A message that only asks about an existing rule ("does our style guide say X? is that documented?") sets none.
_ASKS_FOR_WORK = re.compile(r"\b(?:can|could|would|will) (?:you|we)\b|\bplease\b|\bpls\b|\bboleh\b|\btolong\b|\bkindly\b",
                            re.IGNORECASE)
_TRAILING_QUESTION = re.compile(r"(?<=[.!;\n])[^.!?;\n]*\?\s*$")


def _states_in_a_sentence(text: str) -> bool:
    for sentence in _SENTENCES.split(text):
        if _ABSOLUTE.search(sentence) and (_GROUP_DOES.search(sentence)
                                           or (_RULE_WORD.search(sentence) and _OWNER.search(sentence))):
            return True
    return False


def states_rule(prompt: str) -> bool:
    """True when the text states a rule, convention or decision meant to govern later work too."""
    text = (prompt if isinstance(prompt, str) else "").strip().replace("’", "'").replace("‘", "'")
    if len(text) > _SCAN_LIMIT:   # a pasted file or log: the user's own words are at the start or the end
        text = text[:_SCAN_LIMIT * 3 // 4] + "\n" + text[-_SCAN_LIMIT // 4:]
    if text.endswith("?") and not _ASKS_FOR_WORK.search(text):
        # "From now on always use tabs. Understood?" keeps its first sentence; a lone question states nothing.
        rest = _TRAILING_QUESTION.sub("", text)
        if rest == text:
            return False
        text = rest.strip()
    return bool(CUES.search(text)) or _states_in_a_sentence(text)


def _quoted_path(project: str) -> str:
    """The project folder as one literal word for both bash and PowerShell, or '.' when that is not possible."""
    folder = (project or ".").replace("\\", "/")
    if any(ch in folder for ch in "'\n\r\0"):
        return "."
    return f"'{folder}'"


def save_command(project: str) -> str:
    return f'bossku remember --project {_quoted_path(project)} --kind decision "<the rule as the user stated it, and why>"'


def prompt_reminder(project: str) -> str:
    return ("BosskuAI: this request may state a rule or decision that should outlive it. If it does, do the work and "
            f"then save the rule before you finish: {save_command(project)}")


def stop_reminder(project: str) -> str:
    return ("BosskuAI memory gate: the request seems to state a rule or decision for later work, and it was not saved. "
            f"Do not describe it: call the Bash tool now and run {save_command(project)} with the rule in your own "
            "words (under 200 characters), then finish. If the request stated no rule, just finish.")
