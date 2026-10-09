---
name: fb-audit
description: Analyze published Facebook content and audience growth from authorized exports, screenshots, or observed metrics. Returns evidence-backed experiments, not draft scores or invented analytics.
---

# Performance and growth audit

Read [runtime](references/runtime.md), [metrics](references/metrics.md), and
[audit procedure](references/audit.md). Use [evidence](references/evidence.md)
for claim classification, [privacy](references/privacy.md) for data handling,
and [growth](references/growth.md) for audience-growth objectives.

## Establish the question and evidence

Use objective, surface(s), date range/timezone, actual posts/assets, available
owner data, publication-age snapshots, organic/paid information, and known
business outcomes. Identify exactly what is missing. A screenshot can support
visible fields, not a complete retention curve or attributable leads.
If only public response counts exist, offer a limited response audit, not
an end-to-end channel or algorithm diagnosis.

Normalize without inventing metric definitions or unknown counts. Where
appropriate, run `python3 /resolved/fb-audit/scripts/compare.py observations.csv`.
Inspect warnings, zero/insufficient baselines, and cohort comparability before
interpreting descriptive multiples. Actual performance outranks editorial
scores; an apparent outlier does not prove which hook or topic caused it.

## Learn and choose experiments

Compare both volume and valid rates, matched formats and ages, and samples of
strong/typical/weak work. Review topic, opening promise, payoff, presentation,
source originality, audience fit, and reply context; inspect timing as a
possible confounder, not a universal explanation. Retention diagnosis needs
actual timestamped retention plus relevant content alignment; otherwise ask
for data or give explicitly provisional creative hypotheses.

For growth, distinguish discovery, attention, sharing, attributed follows,
and account-level net growth. Do not infer unknown non-follower reach from
views/followers or assign net growth to one post without attribution.
For business, require actual inquiry/lead/conversion definitions and evidence.

## Deliver

Return coverage and limitations, primary objective metrics, traceable findings,
competing explanations, practical corrections, and a manageable experiment
list with metric, window and decision rule. 'Inconclusive' is a useful outcome.
Route learnings to `fb-plan` and selected revisions to composition skills when
available. No scraping, publishing changes, deletion, or account adjustments.
