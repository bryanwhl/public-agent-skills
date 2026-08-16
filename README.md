# Personal Agent Skills

A personal collection of portable [Agent Skills](https://openagentskills.dev/docs/specification) for Codex and other coding agents that understand `SKILL.md` packages.

## Included skills

### `research-to-interactive-deck`

Researches an unfamiliar topic from first principles and produces a concise, source-grounded, interactive HTML learning deck. It uses simple English for beginners and people who are not fluent in English. The deck includes expandable explanations and clickable definitions for technical words, and is saved under `~/Projects/personal` by default.

Example prompt:

> Use `$research-to-interactive-deck` to teach me how transformer attention works. Assume I know basic Python but no machine learning.

## Install for Codex

Clone this repository, then run:

```bash
./install.sh
```

The installer creates symlinks in `${CODEX_HOME:-$HOME/.codex}/skills`, so repository updates are available immediately. Pass skill names to install only those skills, or set `SKILLS_DIR` to target another agent's supported directory. Restart Codex after first installation so it discovers the skill.

To install one skill manually:

```bash
ln -s "$(pwd)/skills/research-to-interactive-deck" \
  "${CODEX_HOME:-$HOME/.codex}/skills/research-to-interactive-deck"
```

To uninstall the symlink without touching this repository:

```bash
unlink "${CODEX_HOME:-$HOME/.codex}/skills/research-to-interactive-deck"
```

## Use with other coding agents

Each folder under `skills/` follows the open Agent Skills layout and can be copied or symlinked into an agent's supported personal or project skill directory. If an agent does not auto-discover skills, point it directly to the relevant `SKILL.md` and ask it to follow that workflow.

## Repository layout

```text
skills/
  research-to-interactive-deck/
    SKILL.md
    agents/openai.yaml
    assets/deck-template.html
    references/
    scripts/
```

## Safety

Review skills before installing them. Skills can direct an agent to run scripts and use the permissions already granted to that agent. This repository's scripts use only the Python standard library and do not make network requests.
