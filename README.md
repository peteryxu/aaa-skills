# aaa-skills

A personal collection of Claude Code skills. Drop skills here; install them to `~/.claude/skills/` with one command.

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [drawio](drawio/) | Create, read, and modify draw.io diagrams — AWS/Azure/GCP architecture, flowcharts, ERDs, state diagrams, Mermaid, and CSV | ✅ Stable |

## Install

**One command — all skills:**
```bash
git clone https://github.com/peteryxu/aaa-skills.git
cd aaa-skills
./install.sh
```

**Single skill:**
```bash
./install.sh drawio
```

**Preview first:**
```bash
./install.sh --dry-run
```

**Overwrite existing:**
```bash
./install.sh --force
```

**Project-level install** (skill only active in that project):
```bash
./install.sh --target /path/to/your/project
./install.sh drawio --target /path/to/your/project
```

Restart Claude Code after installing to pick up new skills.

## Adding a New Skill

1. Create `.claude/skills/<skillname>/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skillname
   description: One-line description for Claude to match against user requests.
   allowed-tools: Bash, Read, Write
   ---
   ```
2. Add any helper scripts to `.claude/skills/<skillname>/scripts/`
3. Add reference docs to `.claude/skills/<skillname>/reference/`
4. Update the Skills table in this README
5. Run `./install.sh <skillname>` to test locally
