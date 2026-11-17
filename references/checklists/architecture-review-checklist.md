# Architecture Review Checklist

- What are the core modules, layers, and boundaries?
- What root, revision or working-tree state, and sampling limits does this map cover?
- Does the chosen view answer the user's question, with source evidence for important relationships?
- Are direction, action/protocol, synchronous/asynchronous behavior, and failure paths preserved where verified?
- Is the responsibility placed in the right layer?
- Which abstractions are stable versus accidental?
- What coupling, scalability, or operability risks exist?
- What future changes become harder if this path is chosen?
- What should be a local fix versus a structural redesign?
- Are source inspection, automated checks, observed behavior, and visual review reported separately, with evidence refreshed after edits?
