---
name: fb-video
description: Write Facebook short or long video and Reel scripts, openings, visual beats, captions, cover briefs, or Live run-of-shows. Does not render videos or broadcast.
---

# Facebook video

Read [runtime](references/runtime.md), [surface checks](references/surfaces.md)
when selecting format, and [video modes](references/video-modes.md) for the
chosen mode. Read [growth](references/growth.md) for audience-growth work and
[privacy](references/privacy.md) for footage/source rights or personal stories.

## Intake and concept

Use the idea, actual experience, transcript, assets, target audience, objective,
and requested length. Distinguish scripting from editing or generation. A
transcript without timecodes cannot support exact clip in/out points. Footage
described by the user is not footage inspected by the agent.

Choose short, longer explanation/story, or Live preparation. Facebook's Reels
label does not force everything into a short vertical format. Honor the user's
constraints and verify current upload requirements separately from creative
recommendations. Develop distinct accurate openings if alternatives are useful:
recognizable problem, real consequential decision, demonstration, or supported
result. Choose an opening whose promise the footage/script can fulfill.

## Write and review

Write a full spoken body, not an outline labeled as a script. Mark visual
actions, on-screen text, and spoken lines separately. Each beat should add
evidence, context, progress, or payoff. Plan transitions where comprehension
needs them; do not insert a prescribed surprise every fixed number of seconds.
Support accessibility through readable overlays and useful caption directions.
Avoid overlay text that competes with the demonstration or repeats every word.

Estimate speech duration with [timing helper](scripts/timing.py) if available:
`python3 /resolved/fb-video/scripts/timing.py script.txt --wpm 150`.
Supply spoken text only. The estimate excludes pauses, demonstrations and edits;
state that limitation. Never call a timing estimate measured runtime or predict
retention without an actual retention dataset.

## Output and handoffs

Deliver the spoken script or Live agenda, opening rationale, visual beat sheet,
appropriate caption and cover brief, and rights/production questions. Include
a real payoff and optional reason to return. For existing footage, include
verified timestamps only; otherwise suggest re-recording or locating the clip.
Use `fb-repurpose` for a multi-format extraction plan, `fb-human` for explicit
voice revision, and `fb-audit` for measured drop-offs. No rendering, downloads,
paid generation, uploads, or broadcasting are authorized by this skill.
