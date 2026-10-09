# Original few-shot examples

Load one relevant JSONL file, not the whole library. Each row has id, register,
prompt, output and rationale. These are illustrative possibilities, not mandatory
answers. Preserve the user's actual facts and do not copy a fictional example's
price, time or commitment into another task.

- [neutral](neutral.jsonl): neutral/local standard English.
- [formal](formal.jsonl): standard BM and professional writing.
- [casual BM](bm-casual.jsonl): readable informal Malay.
- [Manglish](manglish.jsonl): English-led colloquial choices.
- [rojak](rojak.jsonl): mixed clauses and domain terms.
- [developer](developer.jsonl): coding explanations, literal preservation.
- [WhatsApp](whatsapp.jsonl): short chat without automatic dense abbreviations.
- [workplace](workplace.jsonl): requests and updates.
- [customer service](customer-service.jsonl): empathy and factual precision.
- [social](social-media.jsonl): factual brand copy.
- [anti-examples](anti-examples.jsonl): rejected output with reasons and alternatives.

All rows are newly authored synthetic illustrations under this package's MIT
licence. They have not been calibrated with representative Malaysian reviewers.
