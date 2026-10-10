"""Pins the 2026-10-10 trigger round: each prompt is a dev-split miss where a neighbour outscored the right skill."""
import unittest
from pathlib import Path

from bossku.skills import rank_skills, select_skill_stack

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("pr has merge conflicts failing checks and three unresolved comments can u sort it before standup", "ci-triage"),
    ("Our API responses have gotten slow under load, I want to profile where the time is going and also put together "
     "basic dashboards so we see it happen next time.", "bosskuai-observability-sre"),
    ("Before we raise, I want a realistic financial model and also a structured debate on whether we should raise now "
     "or wait six more months of runway.", "bosskuai-council"),
    ("use the four-voice council skill to settle whether we should pivot to enterprise or stay self-serve, I want the "
     "disagreement laid out, not just one answer", "bosskuai-council"),
    ("Before merging, run a rigorous review on the auth changes, check whether the PR meets the required checks with "
     "every comment resolved, and make sure the retry logic actually has test coverage.", "bosskuai-pr-check"),
    ("This brutalist-style portfolio site needs to actually reflow on mobile instead of breaking below tablet width, "
     "it should be properly keyboard-navigable too, and the copy needs a refresh since we're using it for next week's "
     "launch.", "accessibility"),
    ("Redesigning the onboarding screens to feel less generic, and whatever we ship needs to actually pass a real "
     "accessibility check before launch.", "redesign-skill"),
    ("Building the animations for a new modal and card-hover state, and then I want someone to tell me honestly if "
     "they're actually good or just busy.", "review-animations"),
    ("Our Pinia store for the shopping cart re-renders the whole page on every quantity change and I'm not sure if "
     "that's a reactivity mistake.", "vue-patterns"),
    ("need the vps hardened and also figure out why mongo queries are so slow lately", "bosskuai-mongodb"),
    ("Our incident last week was a cross-tenant data leak, need the postmortem done properly and then an actual fix "
     "to the authorization boundary that caused it.", "bosskuai-incident-response"),
    ("Context's about to run out mid-task on this big migration, I want a BosskuAI skill written for our internal "
     "deploy checklist so it's not tribal knowledge anymore, and then a proper handoff doc so the next session can "
     "pick this up cleanly.", "bosskuai-skill-creator"),
    ("kita nak raise seed round tapi financial model masih messy, boleh tolong buat projection yang make sense?",
     "bosskuai-financial-modeling"),
    ("Traffic is fine but nobody converts on the pricing page, we want structured data added so the product shows up "
     "better in search results, and maybe an exit popup to catch the people who still bounce.", "schema"),
    ("app barely gets downloads on Play Store, why?", "aso"),
    ("page structure for a new law firm website", "site-architecture"),
    ("dedupe customers table by email, keep newest", "bosskuai-database-engineering"),
    ("I'm writing a Go worker that fans jobs out to 8 goroutines over a channel. Under load go test -race complains "
     "about a data race on a shared map.", "bosskuai-go-development"),
]


class RoutingRoundTests(unittest.TestCase):
    def test_right_skill_is_selected(self):
        for prompt, expected in CASES:
            with self.subTest(expected=expected, prompt=prompt[:60]):
                selected = [item["skill_id"] for item in select_skill_stack(prompt, ROOT, limit=5)["selected"]]
                top3 = [sid for sid, _ in rank_skills(prompt, ROOT, limit=3)]
                self.assertTrue(expected in selected or expected in top3, (selected, top3))


if __name__ == "__main__":
    unittest.main()
