---
name: fb-human
description: Revise Facebook drafts to preserve an individual's real voice and meaning. Offers editorial changes and diagnostics, not banned-word rewriting or AI-detection certification.
---

# Voice-preserving revision

Read [runtime](references/runtime.md) and [voice review](references/voice-review.md).
Use [privacy](references/privacy.md) when facts or source rights are unclear.

## Review against an actual voice

Use supplied draft, audience/surface, relevant voice samples, and explicit
preferences. Without samples, improve clarity conservatively and say that
personal voice matching is provisional. Distinguish spoken samples from feed
writing; ask which matters if the difference changes the result.

Identify specific mismatches: generic staging, inflated certainty, repetitive
cadence, unnecessary abstraction, unnatural formal transitions, or an irrelevant
CTA. Don't treat contractions, errors, slang, emoji, short lines, or numerical
details as universal evidence of humanity. Keep the creator's real terminology
and personality even if it resembles a stock phrase.

Optionally run the review-only helper:
`python3 /resolved/fb-human/scripts/editorial.py draft.txt`.
It returns original text unchanged and contextual flags, not an AI score.
Inspect the flags; meaningful Unicode joiners, quotes, emoji and typography
must not be removed automatically. Protect facts, numbers, quoted text, URLs
and terminology before revising by judgment.

## Output

Return the revised copy and a short explanation of substantive changes. Flag
unverified claims separately rather than inserting fabricated proof. Preserve
the draft's intent, scope, and factual uncertainty. If shortening changes the
meaning, explain the trade-off. For short replies, don't pad the copy to pass
a detector or add an unnecessary question. No 'undetectable' claim or external
detector invocation. Recheck the final artifact, not an earlier draft.
