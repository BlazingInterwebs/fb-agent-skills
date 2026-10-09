# Facebook Agent Skills

Facebook-native agent skills for useful content, audience growth, genuine
conversations, and evidence-led improvement.

Turn an idea into a post people can understand and care about. Extract
standalone content from a long source. Build a coherent series. Learn from
the performance you can actually measure, without guessing hidden analytics.

**13 modular skills. Free, MIT-licensed, independently authored.** Designed
for creators, consultants, coaches, entrepreneurs, service and small businesses,
and personal brands. Supply your own context; no personal brand is built in.

## Start with a real situation

```text
Use $fb-post. Write a public Facebook Page post for small business owners.
Our onboarding test had eleven fields. Three testers couldn't tell which
were required. We marked those fields and are testing again. No conversion
results yet. Keep it conversational and give readers a useful takeaway.
```

The workflow develops a recognizable situation, accurate opening, and complete
payoff. It doesn't invent a conversion win or insist on a follow/comment CTA.
See the [worked example](examples/onboarding.md).

## Choose the job

| Skill | Use it for |
| --- | --- |
| [fb-post](skills/fb-post/SKILL.md) | Text, image sequences, links, stories, education, observations, experiments and offers |
| [fb-video](skills/fb-video/SKILL.md) | Short/long video and Reels scripts, visual beats, caption/cover briefs, Live preparation |
| [fb-story](skills/fb-story/SKILL.md) | Frame-by-frame Facebook Stories with available-feature checks |
| [fb-research](skills/fb-research/SKILL.md) | Traceable examples, account-relative comparisons, original concept briefs |
| [fb-repurpose](skills/fb-repurpose/SKILL.md) | Native standalone ideas extracted from complete source material |
| [fb-human](skills/fb-human/SKILL.md) | Voice-preserving revision, not universal banned words or AI-detector claims |
| [fb-plan](skills/fb-plan/SKILL.md) | Sustainable calendars, recurring series, audience-growth experiments |
| [fb-comment](skills/fb-comment/SKILL.md) | Useful contributions on other people's content |
| [fb-reply](skills/fb-reply/SKILL.md) | Triage and answers under your own content |
| [fb-dm](skills/fb-dm/SKILL.md) | Individual Messenger drafts and authorized small-batch triage |
| [fb-presence](skills/fb-presence/SKILL.md) | Profile, professional-mode and Page clarity, appropriate fields and privacy |
| [fb-group](skills/fb-group/SKILL.md) | Rule-aware member contributions and admin material |
| [fb-audit](skills/fb-audit/SKILL.md) | Published performance, growth evidence, limitations and next experiments |

`fb-video` deliberately isn't Reels-only: Facebook's announced video changes
include longer videos. `fb-research` doesn't promise virality. Multi-image feed
content lives in `fb-post`, without assuming Instagram or LinkedIn mechanics.
See [platform evidence and limitations](shared/evidence.md).

## Audience growth is a core objective

Audience need -> original concept -> strong opening -> satisfying payoff ->
reason to return -> measured iteration.

Research informs topics. Composition delivers attention and value. Planning
builds recognizable themes/series. Presence clarifies why someone should follow.
Replies support real relationships. Audits inform the next cycle using
available discovery, attention, share and follower evidence. No guaranteed
growth, fake controversy, copied stories, or mandatory engagement bait.

## Install

Clone this public repository into a location you choose:

```bash
git clone https://github.com/BlazingInterwebs/fb-agent-skills.git
cd fb-agent-skills
python3 -B scripts/validate.py
```

For this collection's tested Codex compatibility location:

```bash
python3 -B scripts/install.py --destination "$HOME/.codex/skills" --dry-run
python3 -B scripts/install.py --destination "$HOME/.codex/skills"
```

Hosts can discover different paths; current OpenAI documentation also describes
`~/.agents/skills`. Select the actual destination for your host. The installer
requires an explicit path and **refuses all existing target paths**. Install a
subset with `--skills fb-post fb-video`, or manually copy complete skill folders.
Restart/reload the host if the new skills do not appear. Never copy only SKILL.md.
See [installation, update and compatibility details](docs/installation.md).

The portable `plugin.json` packages the same skills for plugin-capable hosts.
Publishing this GitHub repository does **not** approve or list a plugin in the
OpenAI directory. Follow current host distribution requirements separately.

## Context, capabilities, and privacy

Use runtime briefs or the optional [context template](templates/context.md).
Store your filled context and exports outside this public repository. It needs
no personal voice clone, connector, API key, or Jake skill pack. Python helpers
need Python 3.9+ with the standard library; without execution, skills provide
explicitly labeled manual review/calculations rather than fake tool receipts.

Ordinary profiles, professional mode, Pages, and Groups are different contexts.
Available Story tools and analytics are checked, not assumed. Public reactions
aren't private reach; views aren't leads. Unknown metrics stay unknown. Read
the [metric schema](shared/metrics.md) and [safety rules](shared/privacy.md).

**V1 drafts and analyzes.** It does not publish, send messages, scrape, change
accounts, render media, moderate live groups, or automate keyword funnels.
Permission to view private content isn't permission to publish it.

## Examples and helpers

- [Standalone repurposing and a growth plan](examples/onboarding.md)
- [Audit a synthetic dataset](examples/audit.md)
- [Behavioral evaluation scenarios](tests/behavioral-cases.md)

```bash
python3 -B skills/fb-audit/scripts/compare.py examples/observations.csv
python3 -B skills/fb-human/scripts/editorial.py examples/draft.txt
python3 -B skills/fb-video/scripts/timing.py examples/spoken.txt --wpm 150
```

Comparisons are descriptive, age-bucketed, same-account/metric baselines that
exclude the target. Insufficient and zero baselines produce no multiple. The
editorial helper **never rewrites** text or assigns an AI score. Timing is an
estimate of supplied spoken text, not measured runtime or retention.

## Development and status

```bash
python3 -B scripts/sync_resources.py --check
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
```

Shared references/helpers are bundled into self-contained skills. After editing
canonical shared files, run `python3 -B scripts/sync_resources.py` and retest.
See [architecture](docs/architecture.md), [contributing](CONTRIBUTING.md), and
[changelog](CHANGELOG.md). Version 0.1.0 is a pilot: automated validation does
not establish real-world growth effectiveness or universal host compatibility.

All core functionality remains free. Optional installation, voice configuration,
training, consulting or integrations can add expertise without withholding
essential skills. [Roadmap](docs/roadmap.md).

## License and acknowledgments

[MIT](LICENSE). Architectural inspiration from Jake Schincariol's modular skill
systems; this is not a port or copy of his content. [Acknowledgments](ACKNOWLEDGMENTS.md).
Not affiliated with or endorsed by Meta, OpenAI, or Jake Schincariol.
