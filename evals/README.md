# Plugin evals

`claude plugin eval` cases for the 28 skills a lean install lists (`skills/lean.json`). They check two things: does the skill load when it should and stay out when it should not, and is the answer better with the plugin than without it.

Each skill has three cases:

- two where the skill should load: one written plainly, one casual or rojak;
- one near miss where it should not load.

`malaysia-localisation` is the default Bossku voice, so all three of its cases expect it to load. That gives 84 cases: 57 should load and 27 should not.

## What is in a case

A case is a folder named `<skill-id>--<fires|quiet>-<slug>/` with:

- `prompt.md`: frontmatter (tools, turn and time budget, tags) and the prompt;
- `graders/*.md`: one file per check.

The graders:

- `skill-fires` (should-load cases): did the Skill tool load the skill. In the default two-arm run this shows as a "plugin fired" indicator and is not scored.
- `skill-stays-quiet` (near misses): the skill must not load. It is scored in both arms (`arm: both`), so a skill that loads where it should not lowers the plugin's score.
- Every other grader checks the result. Most are rubrics for an LLM judge, written as concrete points; some are regex or file checks.

## Run it

Run from the repository root. Every run uses tokens on your own account; read the cost notes first.

```bash
# 68 cases that only need the answer
claude plugin eval . --tag answer --judge-model sonnet

# 11 cases where the agent saves files and runs Python's unittest
claude plugin eval . --tag work --judge-model sonnet --allow-tools Write Edit "Bash(python:*)" "Bash(python3:*)" "Bash(py:*)"

# 2 bosskuai-skill-finder cases: they need the bossku CLI on PATH (pip install -e .)
claude plugin eval . --tag cli --judge-model sonnet --allow-tools "Bash(bossku skills:*)"
```

- **One skill:** `--case 'bosskuai-tdd-loop--*'`.
- **Only the near misses:** `--tag quiet`.
- **Cost:** each case runs 3 times in 2 arms (with and without the plugin). Pilot first with `--runs 1 --no-publish`, and set a ceiling with `--max-cost-usd`.
- **Judge:** use a judge model that is not the model under test, sonnet-tier or larger. If your agent runs on Sonnet, pick a different judge.
- **Result:** the headline number is Δ, the with-plugin score minus the no-plugin score. Results go to `evals/results/`, which git ignores.

## Tags

| Tag | Meaning |
|---|---|
| `lean` | every case |
| `<skill-id>` | the skill the case is about |
| `fires` / `quiet` | should load / near miss |
| `answer` | the answer is in the reply; no gated tools |
| `work` | saves files and runs Python; needs the `--allow-tools` grant above |
| `cli` | runs `bossku skills find`; needs the CLI on PATH |

On Windows the work cases run Python through the Bash tool. If your Claude Code uses its PowerShell tool instead, add matching `PowerShell(python *)` entries to those cases' `allowed_tools` and to `--allow-tools`.

## Limits

- The prompts and rubrics were written for this suite. They are not real user traffic.
- An LLM judge grades most cases, so read failing traces before acting on a score.
- The suite was checked for format with `tests/test_plugin_evals.py`, not by a paid run. Run a pilot before you trust a number.

## When you change a lean skill

`tests/test_plugin_evals.py` fails when `skills/lean.json` lists a skill without three cases here, or a case names a skill that is not listed. Add or rename the cases in the same change.
