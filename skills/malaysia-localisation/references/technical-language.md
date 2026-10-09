# Developer and technical language

Localise explanations without altering executable material. Preserve API,
backend, frontend, staging, deploy, branch, pull request, Docker, CI/CD and similar
terms when that is the audience's established vocabulary. Do not force direct
translations in casual developer chat. Formal BM documentation may appropriately
use pelayan, pangkalan data or antara muka; respect the glossary and reader.

Original peer explanation: “Check log dulu. Kalau request tu timeout, tengok
connection ke database.” A formal BM explanation can instead use “Semak log
terlebih dahulu” and a consistent approved terminology set.

Commands, filenames, code identifiers, string literals, flags, URLs, product
names and placeholders stay exact unless the user asks to edit them. If rewriting
“Run `npm run build` before merging PR #42”, the command and PR number must
survive unchanged. Do not translate `user_id` into a new identifier. Do not change
an error's quoted wording while explaining it in BM.

Preserve hedges and technical conditions: “might be a cache issue” cannot become
“confirm cache rosak”. An explanation of a failed test must not claim the fix is
verified. Use casual rhythm without inventing results, executing commands or
editing files merely because the localisation example mentions deployment.

When using translated dataset examples, compare code blocks and literals with
the original. A localised field or language-detection flag does not prove code
correctness. Keep executable tokens and identifier bindings intact, and localise
only the surrounding prose unless code changes are part of the request.

For public explanations, use the technical subject explicitly on first mention
when a shorter term is ambiguous (for example, AI agents rather than agents).
Explain what a measurement observes without inventing its mechanism or scoring.
Keep runs, tasks, rules and answers distinct when discussing percentages.
See [rewrite and explain](rewrite-and-explain.md) for metric clarity and the
boundary between rewriting a claim and verifying an experiment.
