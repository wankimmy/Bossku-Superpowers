# Codebase Analysis Checklist

- What framework, runtime, and architectural style is this codebase using?
- What root, behavior, revision or working-tree state, and sampling scope does the analysis cover?
- Where are the entry points, core modules, and shared utilities?
- What is the request or execution path from input to side effects?
- Which source locations establish each important call, registration, dispatch, or transport rather than only a naming or proximity match?
- Are direction, action/protocol, synchronous/asynchronous behavior, and failure paths preserved where verified?
- Which files are source-of-truth versus generated or derived?
- Which conventions are real versus only aspirational docs?
- What is explicitly documented versus inferred from source?
- Which behavior was actually exercised, and which claims remain based on source inspection alone?
- Have source locations and maps been re-checked after edits, and are unread areas stated?
