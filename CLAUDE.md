# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

See `README.md` for the skills table and install commands.

## Skill internals

Each skill dir (`.claude/skills/<skillname>/`) contains:
- `SKILL.md` — YAML frontmatter (`name`, `description`, `allowed-tools`) followed by skill instructions
- `scripts/` — helper scripts the skill invokes
- `reference/` — docs the skill reads at runtime
