# Skill Routing Coverage Implementation Plan

> **For agentic workers:** Use the existing Executor and Auditor contracts for implementation and independent review.

**Goal:** Route short, concrete, BM/rojak and mixed requests to suitable skills and show complementary skills in Claude/Codex hints.

**Architecture:** Keep the lexical router and stdlib implementation. Normalize common local task vocabulary, retain original explicit requests and exclusions, and judge hint eligibility from actual task evidence instead of prompt length alone. Preserve v1/v2 rendering compatibility where possible; intentionally replace their old silence rules.

**Tech Stack:** Python stdlib, unittest, existing JSON skill index.

**Spec:** User request: fix the observed gaps and allow combinations of skills for distinct concerns. Reference: the 22 scenario experiment in this chat.

## Constraints

- No model/API dependency, automatic Claude model calls, commits or pushes.
- Respect availability, exclusions, user-only skills and overlapping alternatives.
- Keep hints bounded; do not turn greetings and status questions into specialist requests.
- Test local routing and actual hook delivery separately from live Claude skill invocation.

## Tasks

- [x] Add failing coverage cases for short/explicit/BM/rojak/concrete/mixed requests and irrelevant complements.
- [x] Improve normalization, curated intent evidence and concern composition in `bossku/index.py` and `bossku/skills.py`.
- [x] Replace length/score-only hint gates in `bossku/hint.py`; support up to three distinct skills in both modes and preserve invocation safeguards.
- [x] Fix signature scan cost without stale caches; independently verify mutation detection.
- [x] Update obsolete policy tests and document the new hint contract.
- [x] Rebuild the index, run focused checks, validator and full unittest suite using a writable temporary directory.
- [x] Run independent Auditor/cleanup review, rerun scenario outputs, and verify installed hook loading from this checkout.

## Verification

Focused: `test_routing_coverage.py`, `test_skill_selection.py`, `test_hooks_gate_hint.py`, `test_smart_lean.py`, existing routing regression suites.

Required: `python -m bossku skills index --root .`, `python -m bossku validate --root .`, full unittest discovery. Use a short writable temporary directory in this sandbox. Windows copied fixtures clear OneDrive read-only directory attributes; Git isolation fixtures set GIT_CEILING_DIRECTORIES so workspace-local temp folders do not inherit the parent checkout.

Verified baseline before additional pack imports: 816 unittest tests passed, validator passed, index fresh, diff whitespace check passed. Installed skill-hint executable delivered short/explicit/BM combination hints. Live Claude Skill invocation remains unverified (CLI unavailable).
