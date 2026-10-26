---
description: "Approved spec, multi-file change: an ordered plan with files and tests before any code."
tags: ["lean", "writing-plans", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Spec is approved: add multi-currency invoices (MYR, SGD, USD) to our Django invoicing app. Existing invoices are all MYR. Amounts are stored as integer cents in `invoices.Invoice.total_cents`. Each invoice gets a `currency` field; totals are shown with the right symbol; reports still sum in MYR using a daily rate table we'll add. Before anyone touches code, write the implementation plan. Put the plan in your reply; don't create files.

Relevant files: invoices/models.py, invoices/views.py, invoices/templates/invoices/detail.html, reports/services.py, invoices/tests/.
