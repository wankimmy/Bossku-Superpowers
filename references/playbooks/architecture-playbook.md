# Architecture Playbook

> If the request is general, ambiguous, or touches many files — ask clarifying yes/no questions **before acting**. Use numbered bullets with explicit answer format: e.g. `1-yes/no  2-A/B`.

Use this when judging module boundaries, layering, scaling tradeoffs, or structural refactors.

## Workflow

1. Resolve the root and analysis scope, including revision or working-tree state when available. Identify the current architecture from code, not only docs, and report sampling limits.
2. Choose a boundary, sequence, dataflow, workflow, or lifecycle view for the question. Use text or Mermaid by default, with source locations for important relationships. Preserve direction, action/protocol, synchronous/asynchronous behavior, and verified failure paths; names and file proximity do not establish causality.
3. Evaluate whether the requested change fits the current structure.
4. Separate local fixes from architectural changes.
5. Explain tradeoffs, rejected alternatives, and long-term implications.
6. Report source inspection, checks actually run, and observed behavior separately. Re-check source locations after edits; rendering a diagram or finding a cited file does not prove the design correct.

## Output expectation

- current architecture summary
- structural risks
- boundary recommendations
- tradeoffs
- suggested direction
