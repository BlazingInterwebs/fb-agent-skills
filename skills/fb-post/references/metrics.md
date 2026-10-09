# Metric definitions and comparable evidence

## Availability

Ordinary profiles/public research: supplied or visible reactions, comments,
shares and sometimes video counts; no inferred private reach or retention.
Professional-mode profiles/Pages: use owner exports/screenshots and their actual
field definitions. Group admin data: membership, activity, or other genuinely
exposed fields, not an assumed Page schema. Messages/CRM: authorized records
only, with explicit attribution and deduplicated lead definitions.

| Objective | Conditional evidence | Do not confuse with |
| --- | --- | --- |
| Discovery | Reach and follower/non-follower distribution | Views/followers ratio or impressions |
| Attention | Defined views, watch time, retention by timestamp | Unique viewers or inferred drop-offs |
| Conversation | Meaningful external comments, participants, questions answered | Creator replies, spam and keyword totals |
| Sharing | Observed shares and optional share rate | Assumed private send/saves counts |
| Growth | Attributed follows and net follower change | Guaranteed post-level causality |
| Traffic | Actual outbound link clicks | All clicks or reactions |
| Business | Attributable inquiries, qualified leads, conversions | Every DM, correlation, or monetization views |

Only use impressions, saves, profile activity, Story fields, or qualified views
when supplied with definitions. Unknown is null/missing, never zero. Preserve
export names, windows, time zones, and denominator. Reach is not additive unique
reach across posts. A changed metric definition breaks comparability.

## Helper input

`compare.py` in `fb-audit` and `fb-research` accepts UTF-8 CSV or a JSON array
of long-form observations. Required fields:

| Field | Meaning |
| --- | --- |
| account, post_id | Stable identifiers; pseudonyms are acceptable |
| surface, format | e.g. page, video; do not mix unlike formats |
| visibility | public, friends, or private; unknown is excluded |
| distribution | organic or paid; unknown is excluded; paid opt-in stays separate |
| metric, unit, definition | e.g. reactions, count, visible-reactions; units: count/seconds/fraction/percent |
| value | Finite nonnegative number, or empty/null for unknown |
| age_hours | Publication age when counted, not account age |
| source_url | Traceable public URL or authorized file reference |
| observed_at | ISO 8601 capture timestamp including timezone |

Extra columns survive normalization. Never manufacture a definition or timestamp
for an old export. If missing, explain why numerical comparison cannot run.

## Comparison

The helper groups by account, surface, format, visibility, distribution, metric,
unit, definition, and publication-age bucket. Default age buckets are 24 hours:
a disclosed convenience heuristic, not age matching proof. Narrow them with
`--age-window-hours` or supply matched snapshots; inspect edge effects manually.
It excludes each target from its comparison median and requires ten other
observations by default. This is a cautious product minimum, not statistical
significance. No ratio is returned for insufficient/zero baselines.
Publicly visible response multiples are labeled with the observed metric;
they never become reach, algorithm, or lead claims. Paid rows are excluded
unless requested, and then remain separate. Duplicate observations are rejected.
The helper cannot detect hidden boosts, bot activity, mismatched export semantics,
or source accuracy. Its result is descriptive, not predictive or causal.

For rates outside this helper, show numerator/denominator and raw counts. Use
the same definition/window and positive denominator; return unavailable when
missing. Compare both volume and rate because either alone can mislead.
