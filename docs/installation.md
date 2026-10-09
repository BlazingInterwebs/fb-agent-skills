# Installation, compatibility and updates

## Local skill folders

Use a checkout of the release you intend to install. Python 3.9+ is required
for bundled helpers and tooling; no pip packages or API keys are needed.

```bash
python3 -B scripts/validate.py
python3 -B scripts/install.py --destination "$HOME/.codex/skills" --dry-run
python3 -B scripts/install.py --destination "$HOME/.codex/skills"
```

`~/.codex/skills` is the compatibility location used for the initial local
installation. Current [OpenAI skills guidance](https://learn.chatgpt.com/docs/build-skills)
also lists user discovery at `~/.agents/skills`. Use the path your actual host
discovers, e.g. the same installer with `--destination "$HOME/.agents/skills"`.
An explicit path avoids silently guessing a host, changing unrelated config,
or installing duplicate definitions into several discovery roots.

Install a subset with `--skills fb-post fb-human`. All target paths are checked
before copying; any existing directory/file/symlink causes refusal. Files are
hash-verified after copying. An interrupted I/O operation can leave a partial
new directory: inspect it before retrying. The installer never deletes existing
skills, rewrites host config, downloads dependencies, or stores brand data.
Manual installation means copying the complete chosen `skills/fb-*` folders,
including references, scripts and license, not just `SKILL.md`.

## Host compatibility

| Host/mode | Intended support | Verification scope |
| --- | --- | --- |
| Local Codex discovered folders | SKILL.md, bundled references, Python helpers when execution exists | Initial local install plus folder/hash/helper tests; actual implicit routing needs a fresh host session |
| ChatGPT/plugin-capable hosts | Same workflows through portable plugin packaging | Manifest supplied; no public directory approval or universal account availability claim |
| Hosts without Python or browsing | Inline composition, supplied sources, manual labeled analysis | No fake helper executions or inferred research access |

The repository includes a root `plugin.json` using the portable Agent Plugins
format. Follow [current packaging requirements](https://developers.openai.com/plugins/build/plugins)
for a local marketplace or a public directory submission. A GitHub URL alone
isn't proof of a plugin install, approval, or execution capabilities. No MCP
server, connector registration, or lifecycle hooks are supplied.

## Invocation and context

Use the skill-selection syntax exposed by your host. Codex supports references
such as `$fb-post`; plugin hosts may use a namespaced or UI-selected skill.
Verify discoverability after installation, restarting/reloading if necessary.
Fill [optional context](../templates/context.md) outside the public project,
or simply supply the relevant details in the task. Never import unrelated
personal memory or other platforms' voice files automatically.

## Updates and uninstall

Pin a version/commit for reproducibility. Review changelog, source and tests;
compare installed folders before changing them. The installer deliberately has
no overwrite/update/delete mode. Back up user-edited files, obtain authorization
for replacement, and use the host's supported installation flow or a reviewed
manual update. Removing a collection is likewise an explicit user action;
uninstall never means deleting personal context or another skill pack.
