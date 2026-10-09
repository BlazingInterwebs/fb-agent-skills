---
name: fb-story
description: Draft Facebook Story sequences with frame copy and visual directions from timely updates and available assets. Does not assume Instagram stickers or publish Stories.
---

# Facebook Stories

Read [runtime](references/runtime.md), [surface checks](references/surfaces.md)
for audience and feature availability, and [privacy](references/privacy.md) for
images, locations, clients, or private replies. For growth briefs, apply
[growth](references/growth.md) without forcing a follow CTA onto every sequence.

## Build a sequence

Identify the actual update, audience, objective, available photos/video, and
verified facts. A Story can show progress, explain one small decision, answer
a real question, or invite a relevant response. Do not require a fixed daily
formula or invent behind-the-scenes activity to fill frames.

Choose as many frames as the idea needs. Give each frame a clear purpose and
minimal legible copy; let the supplied visual carry evidence when it can.
Use a sequence such as situation -> change/demonstration -> payoff when useful,
but one complete frame is also valid. Account for overlays/UI and accessibility
without claiming a current technical pixel-safe zone that has not been checked.

Suggest links, questions, polls, or other interactive tools only if available
in the user's current Facebook composer. Otherwise provide a plain-text
alternative or a natural manual reply invitation. Do not promise automated
DM delivery. Public visibility and reach are not assumed.

## Output

Return a table of frame, visual/asset, exact copy, estimated duration if needed,
and confirmed/conditional interaction. Put feature checks and privacy concerns
outside the copy. Ask before using a private message as a screenshot or quote.
Route an authorized incoming response to `fb-dm` if available; route feed copy
to `fb-post`. No posting, private reply sending, asset generation, or external
transmission is performed by this skill.
