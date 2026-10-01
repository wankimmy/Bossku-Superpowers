"""Run redaction across a batch of documents."""

from redactor import DEFAULT_RULES, redact


def scan_documents(documents, rules=DEFAULT_RULES):
    """Redact each document in `documents` (each `str` or `bytes`,
    independently) and return `(results, totals)`: `results` is a list of
    `(redacted, counts)` pairs (one per document, in order, each keeping
    its own type), and `totals` sums each rule's count across all
    documents."""
    results = []
    totals = {rule.name: 0 for rule in rules}
    for doc in documents:
        redacted, counts = redact(doc, rules)
        results.append((redacted, counts))
        for name, n in counts.items():
            totals[name] += n
    return results, totals
