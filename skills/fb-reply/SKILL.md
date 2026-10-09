---
name: fb-reply
description: Triage and draft contextual replies to comments under the user's own Facebook posts or videos. Does not delete comments, moderate accounts, or send private messages.
---

# Replies under owned content

Read [runtime](references/runtime.md), [privacy](references/privacy.md), and
[reply triage](references/triage.md). Use actual post and thread context.

Classify questions, useful experiences, disagreement, praise, support problems,
resource requests, and suspected spam/abuse. Prioritize usefulness and urgency,
not presumed algorithm weights. Resolve the comment's real question instead
of ending every reply with another question. A simple acknowledgment, no
reply, or escalation can be the best choice.

Draft concise, individual responses in the user's voice. Don't fabricate a
promised resource, support resolution, personal relationship, or completed DM.
Deliver public answers publicly when appropriate; suggest a private channel
only to protect sensitive detail or meet a legitimate expressed request.
Request/confirm consent before unrelated private outreach; `fb-dm` only drafts.

Return a triage table with comment identifier, recommended action, draft, and
reason if useful. Mark unanswered factual questions for the user rather than
inventing answers. Moderation/escalation entries are recommendations, not
actions taken. Don't manufacture comments, like replies, hide criticism,
automatically delete spam, or claim replying guarantees additional reach.
Use `fb-comment` for participation on other people's posts.
