# Human-Centered Design Playbook

Use this before choosing a design direction, engagement mechanism or metric. Creative and marketing sites may use the Awwwards house rule. Operational products put familiarity first.

Goal: beautiful enough to get attention, familiar enough to understand at once, smooth enough to feel effortless, useful enough to return to. The [engagement ethics checklist](../checklists/engagement-ethics-checklist.md) wins over any skill that suggests otherwise.

Bracket tags are source ids from section 8. No tag means design judgement, not a measured result.

## 1. Classify the product first

| Product type | User came to | "Good" means | Prefer | Avoid |
| --- | --- | --- | --- | --- |
| Showcase web (portfolio, campaign, brand) | Be impressed, understand the brand | Memorable, still readable and fast | Awwwards house rule, bold type, considered motion | Motion that hides content or breaks on small screens |
| Task-first public pages (storefront, checkout) | Find, compare, buy | Confident purchase, few errors | Familiar cart and checkout, marked required and optional fields [C2: company-reported benchmark], plain error text | Forced account creation, surprise fees, fake urgency |
| Productivity SaaS | Finish work | Work done with less effort | Project's component library, keyboard paths, undo, saved state | Showcase motion, onboarding that blocks work |
| ERP, HRMS, CRM, internal tools | Enter, find and approve records fast | Speed, accuracy, no data loss | Dense tables, filters, bulk actions, clear status, standard forms | Decorative animation, novel navigation, hidden actions |
| Analytics dashboard | Read a number, decide | Right figure found in seconds | Few clear charts, labelled units, filters that persist | Chart ornament, animated counters on every load |
| Consumer mobile app | Do one job on the go | One-hand reach, quick return to the task | Platform navigation, three to five top destinations [U5: Android guidance], one primary action | Custom gestures with no hint, desktop layouts shrunk |
| Social or community | Take part, be seen, connect | Meaningful participation | Clear posting, moderation tools, notification control | Guilt notifications, endless-scroll traps |
| Learning | Master a skill | Visible progress toward mastery | Progress shown against goals, spaced practice, honest feedback | Points that reward clicking instead of learning |
| Fitness or habit | Build a routine | An achievable routine | Small daily goals, flexible streaks, opt-in reminders | Punishing a missed day, shame copy |
| Marketplace | Match buyer and seller with trust | Safe, clear transactions | Verified reviews, clear fees, familiar search and filter | Fabricated reviews or "N people viewing" |
| Health, well-being, religious | Support, calm, reflection | Supportive, private, no shame | Gentle tone, user-set reminders, privacy by default | Streak guilt, loss framing, public comparison |

## 2. Familiar before novel

- Use the project's component library and design system first.
- Keep standard patterns for navigation, forms, search and filter, settings, checkout and back behaviour.
- Novelty is allowed in showcase pages, brand moments and celebration states, not on screens where the user is finishing work.
- Polish raises perceived usability, not real usability [U2: professional guidance].

## 3. Autonomy, competence, relatedness, low effort

Self-determination theory names autonomy, competence and relatedness as basic needs [M1: professional guidance, secondary summary]. It lists user goals; it promises no engagement.

- **Autonomy.** Offer real choice in how to reach the goal, clear exits and undo [U1: professional guidance], and a way to turn off reminders and sounds.
- **Competence.** Show progress toward mastery in terms the user cares about [M1: professional guidance]. Give plain-language errors that say what happened and how to fix it [U1: professional guidance].
- **Relatedness.** Add social features only when they help the goal (shared goals, collaboration) [M1: professional guidance]. Let people mute or leave a group freely. A shared streak is worth testing, not assuming [P3: company description, no experimental data].
- **Low effort.** When a behaviour does not happen, check motivation, ability and prompt, and cut effort first [M6: professional guidance, untested model].

## 4. Engagement that serves the user

| Type | Engagement means | May fit | Does not fit |
| --- | --- | --- | --- |
| SaaS | Successful work, not time in the app | Templates, shortcuts, clear onboarding checklist the user ticks | Features that add clicks to raise session time |
| Commerce | Confident purchase | Honest stock and delivery info, easy returns, clear checkout | Fake countdowns, invented scarcity, hidden fees [E2: regulator press release] |
| Learning | Mastery | Progress against goals, feedback, light gamification (small learning effects, not retention) [M2: meta-analysis, learners only] | Rewards that reward speed over learning |
| Habit | Achievable routine | Small daily action separate from a bigger goal, limited streak freeze [P1, P2: one learning app, company-reported, not independently verified] | Streak loss as punishment, forced return prompts |
| Social | Meaningful participation | Friend or group goals [P3: one learning app], time-boxed challenges with visible rules [P4: help article, no outcome data] | Notifications that guilt people into returning |
| Health, religious | Supportive routine | User-set reminders, private progress, gentle wording | Shame, loss framing, public comparison |

P1 to P3 come from one language-learning app; they are untested for fitness, habit and social apps and say nothing about an enterprise dashboard or a shopping app.

## 5. Feedback and reward in proportion

- Show system status for any action that takes time [U1: professional guidance]. A progress indicator fits multi-step flows. Show real progress only; never tick a step the user did not do.
- A confirmation fits a save, send, submit or purchase. A small celebration fits a real milestone the user chose (first project shipped, course finished).
- Keep celebration for real milestones. One company reports a small retention lift (+1.7%) from new streak animations [P2: company-reported, not independently verified]; a learning app only.
- Never block the next action for decoration. Celebration is short, skippable and respects reduced motion.

## 6. Measuring it

HEART: happiness, engagement, adoption, retention, task success. The names come from the framework as commonly cited; the paper's full text was not read [C3: not read].

| Product type | One primary metric |
| --- | --- |
| Showcase web | Engaged visits that reach the intended action |
| SaaS, ERP, internal | Task success rate |
| Dashboard | Time to find the answer |
| Consumer mobile app | Completion of the app's main job |
| Marketplace | Completed transactions without disputes |
| Commerce | Completed purchases without returns or support contact |
| Learning | Mastery or assessment score |
| Habit | Share of users keeping their own chosen routine (for example Day 14 return) |
| Social | Meaningful actions per active user (replies, shared goals) |
| Health, religious | Self-reported benefit |

Guardrail metrics sit beside the primary one: notification opt-outs, uninstalls, complaints, error rate, unwanted purchases and refunds, task abandonment, cancellation complaints.

- A controlled experiment is required before saying a feature improved retention. Company figures and streak comparisons are correlational or unverified [P1, P2].
- Never optimise daily active use or session length alone.

## 7. Usability test template

Fill one block per flow.

- Intended user:
- Goal:
- Task scenario (in the user's words, no UI names):
- Expected result:
- Likely confusion:
- Observable success criteria (for example completes in under N steps with no help):
- Record: completion, errors, time, hesitation, comments.

About five users per round, in repeated rounds, find problems in qualitative testing [U3: observational]. That supports no retention figure; a quantitative claim needs 20 or more users. With no human test, write "heuristic assessment" and list findings from the heuristics. Never invent a user reaction.

## 8. Sources

| Id | Title | Evidence class | Status |
| --- | --- | --- | --- |
| M1 | APA, Self-determination theory: a quarter century of research | professional guidance (secondary summary) | read |
| M2 | Sailer and Homner, The Gamification of Learning (meta-analysis) | meta-analysis | read |
| M3 | Mobile app engagement through gamification (JMR) | not classified | not read |
| M4 | Randomized field experiment on mobile app engagement (Management Science) | not classified | not read |
| M5 | Nunes and Dreze, The Endowed Progress Effect | abstract only | not read (abstract only) |
| M6 | Fogg Behavior Model | professional guidance | read |
| P1 | Duolingo, Improving the Streak | company-reported A/B test | read |
| P2 | Duolingo, How Streaks Build Habits | company explainer, observational | read |
| P3 | Duolingo, Friend Streak | company description, no data | read |
| P4 | Strava Challenges help article | company description, no data | read |
| U1 | NN/g, Ten Usability Heuristics | professional guidance | read |
| U2 | NN/g, Aesthetic-Usability Effect | professional guidance | read |
| U3 | NN/g, How Many Test Users | observational | read |
| U4 | Apple Human Interface Guidelines | not classified | not read |
| U5 | Android layout and navigation patterns | professional guidance | read |
| U6 | WCAG 2.2 (W3C) | standard | read |
| C1 | Baymard, Checkout Usability Research | company-reported benchmark | read |
| C2 | Baymard, Current State of Checkout UX | company-reported benchmark | read |
| C3 | Rodden et al., HEART (CHI 2010) | listing abstract only | not read |
| C4 | Google, Core Web Vitals | professional guidance | read |
| C5 | Playwright, visual comparisons | professional guidance | read |
| E1 | OECD, Dark Commercial Patterns (topic page) | regulator or policy page | read (2022 paper not read) |
| E2 | FTC press release on dark patterns | regulator press release | read (staff report not read) |
