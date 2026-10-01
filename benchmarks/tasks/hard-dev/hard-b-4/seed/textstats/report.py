"""Build a simple text-analytics summary."""

from .frequency import most_common, word_frequencies


def summarize(text, stopwords=None, top_n=5):
    counts = word_frequencies(text, stopwords)
    total = sum(counts.values())
    return {
        "total_words": total,
        "distinct_words": len(counts),
        "top_words": most_common(counts, top_n),
    }
