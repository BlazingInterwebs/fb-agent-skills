---
name: fb-research
description: Research accessible Facebook content and account-relative outliers using traceable public observations or authorized data. Produces original concept briefs, not guaranteed viral predictions.
---

# Facebook research

Read [runtime](references/runtime.md), [evidence](references/evidence.md), and
[metrics](references/metrics.md). Apply [privacy](references/privacy.md) to
collection and source reuse; [growth](references/growth.md) guides concepts.

## Collect a defensible sample

Clarify niche, intended audience, surface, objective, and available examples.
Use direct and adjacent creators for different purposes: direct examples for
audience needs; adjacent examples for mechanisms. Very large accounts can
inspire creative directions but are not cadence or results benchmarks.
Record how accounts/posts were selected so a convenient winner-only sample
is not disguised as representative research. Include typical posts and weak
examples as comparison material when accessible.

Use exposed browsing tools or user-supplied examples only. Log URL/source,
capture date, format, account, visible metrics, post age, visibility and
known promotion. Don't scrape at scale, ask for passwords, bypass login gates,
or invent hidden analytics. If counts are missing, offer qualitative analysis
and say that numerical outlier ranking cannot be supported.

## Compare and interpret

Normalize observed records to the metric schema. When sufficient, run
`python3 /resolved/fb-research/scripts/compare.py observations.csv`.
Inspect comparability and warnings before interpreting multiples. Don't treat
follower-normalized views as a median baseline, or reactions as reach.
Distinguish measured patterns, plausible mechanisms, and alternative causes
such as an existing audience, timely event, promotion, or a different subject.
No helper score establishes what caused performance or will transfer.

For each promising example, describe the audience tension, opening mechanism,
context, structure, payoff, and permission-safe lesson. Study weaker examples
to check whether the alleged mechanism also appears without strong results.
Avoid reproducing scripts or a creator's distinctive personal story/identity.

## Deliver

Return source-backed examples, comparison table where valid, sample limitations,
confidence in plain language, and a few original briefs using the user's own
available evidence. A brief names the reader need, new angle, feasible format,
payoff, facts required, and experiment metric. Label extrapolations from other
platforms as such. Route selected briefs to `fb-post` or `fb-video`; use
`fb-audit` for the user's actual results. Do not claim an inaccessible sample
was reviewed or that an observation guarantees virality.
