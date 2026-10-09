# Synthetic audit example

[observations.csv](observations.csv) contains twelve invented public organic
Page image-post observations at the same 168-hour publication age. Its metric
is visible reactions, not reach. Account and URLs are synthetic fixture labels.
They are not a creator benchmark, testimonial, scraped dataset, or causal study.

```bash
python3 -B skills/fb-audit/scripts/compare.py examples/observations.csv
```

Ten posts have 10 reactions; two have 20 and 200 respectively. The latter has
an 11-post comparison median of 10, excluding itself, and a 20x observed
reaction multiple. That does not establish additional reach, non-follower
distribution, retention, leads, or which creative mechanism caused the result.

If paid status becomes unknown, that row is excluded. If metrics are missing,
they remain unknown. If too few comparable posts remain or their median is
zero, the helper returns no ratio. Different account, format, visibility, metric
definition, distribution, or age bucket creates a separate cohort.

Useful next step: inspect actual source content and alternative explanations,
then design a feasible experiment from what is known. This synthetic fixture
contains no scripts or creative labels, so it cannot support a hook conclusion.
