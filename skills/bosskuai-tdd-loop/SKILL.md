---
name: bosskuai-tdd-loop
description: Use when the user asks for TDD, test-first, or red-green-refactor work on a feature or bug fix. Suite strategy and seam or contract tests belong to bosskuai-qa-automation-strategy and bosskuai-integration-testing.
---

# Test-driven development

Red, green, refactor, one behaviour at a time. Do not write all the tests first and all the code after: each test should teach you something for the next.

1. **Settle the public interface** from the request. If it is open and nobody can answer, pick the simplest one and say so in one line.
2. **List the behaviours worth testing**, most important first, including the edges: empty, boundary, invalid input, exact error type, repeated calls.
3. **For each behaviour:** write one test through the public interface, run it and see it fail for the right reason (an assertion on the missing behaviour, not a typo or an import error), write the least code that passes, run it again, then move on.
4. **Refactor only while green,** and run the tests after every step.
5. **Done** means the whole suite is green with clean output, run in this session.

A test describes behaviour, not implementation: it should survive an internal refactor. If it passes before you wrote any code, it tests nothing yet; fix the test. Examples and mocking rules: `tests.md`, `mocking.md`. The long version: `reference.md`.
