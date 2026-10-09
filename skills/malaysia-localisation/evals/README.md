# Evaluating language behaviour

These are original scenario tests, not imported corpus benchmarks or certified
native-speaker ratings. Structure checks do not establish linguistic quality.

## Run a comparable evaluation

1. Use a fresh chat per case. Give the model only the case's context and prompt.
   For the skill-enabled run, make this skill available and explicitly invoke it.
   Do not show `reference_output` or `human_criteria` to the generating model.
2. Repeat with the same model/settings without the skill. Record model name,
   version, date, temperature if configurable and whether invocation occurred.
3. Save one JSONL record per case: `{"id":"reg-01","output":"..."}`. Use the
   case IDs unchanged. Keep outputs outside the skill folder, e.g. `work/run.jsonl`.
4. From the full package root run `python scripts/check_localisation_evals.py work/run.jsonl`.
   It checks preservation/explicit prohibited tokens only, rejects unknown or
   duplicate IDs, reports missing cases and exits nonzero for failed or incomplete
   runs. A clean result still requires human language review.
5. Have fluent reviewers familiar with the target setting compare blinded output
   pairs. Score each dimension 0–4: register fit, natural rhythm/switching,
   pragmatic/particle fit, meaning fidelity, local vocabulary, and respectful
   relationship/identity handling. 0 = serious failure; 2 = usable with edits;
   4 = natural and accurate for this context. Record disagreements, not just means.

Suggested pilot acceptance: no literal/meaning/identity failures; each dimension
at least 3 on average; no category systematically worse than baseline. This is
an editorial pilot threshold, not a statistically validated metric. Include
reviewers from different intended audiences and varieties; do not use one KL
speaker as a universal gold standard. Do not tune generation to exact references.
Hold back new cases for later releases to reduce overfitting.

## Files

- [register](register.jsonl): target artifact versus input style.
- [code-switch](code-switch.jsonl): useful mixing, negation, technical literals.
- [Indonesia leakage](indonesia-leakage.jsonl): contextual vocabulary and exceptions.
- [over-localisation](over-localisation.jsonl): particles, stereotyping, over-familiarity.
- [Malaysia knowledge](malaysia-knowledge.jsonl): locale formatting and uncertainty.
- [dialect](dialect.jsonl): scope limits and sample-led adaptation.
- [customer service](customer-service.jsonl): policies, empathy, invented commitments.
- [invocation](invocation.jsonl): explicit localisation and lightweight default voice.
- [response style](response-style.jsonl): brevity, clarity and explicit detail/format overrides.

`reference_output` is one plausible authored answer. A different answer can pass.
`checks` has `contains` for exact literals and `forbidden_regex` for narrow
case-specific failures. It is not a general Indonesian classifier, a particle
frequency score or an authenticity test. Invocation is a host observation;
record skill loading separately and judge those cases manually.

In this repository run `python -m bossku validate --root .` and
`python -m unittest discover -s tests -v` for integration checks. The default
voice installation regressions are in `tests/test_default_voice.py`. No network,
LLM API, account access or paid model calls are part of these checks.
