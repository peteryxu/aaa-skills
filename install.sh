#!/usr/bin/env bash
# install.sh — Install Claude Code skills to ~/.claude/skills/ or a project directory
#
# Usage:
#   ./install.sh                                  Install all skills (user-level)
#   ./install.sh drawio                           Install a specific skill (user-level)
#   ./install.sh --target /path/to/project        Install all skills (project-level)
#   ./install.sh drawio --target /path/to/project Install one skill (project-level)
#   ./install.sh --dry-run                        Preview what would be installed
#   ./install.sh --force                          Overwrite existing installs

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/.claude/skills"

DRY_RUN=false
FORCE=false
TARGET_SKILL=""
TARGET_DIR=""

# Parse args (handle --target <value> pair)
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    --force)   FORCE=true; shift ;;
    --target)
      [[ -z "${2:-}" ]] && { echo "ERROR: --target requires a directory path"; exit 1; }
      TARGET_DIR="$2"; shift 2 ;;
    --target=*) TARGET_DIR="${1#--target=}"; shift ;;
    --*)       echo "Unknown flag: $1"; exit 1 ;;
    *)         TARGET_SKILL="$1"; shift ;;
  esac
done

# Resolve destination
if [[ -n "$TARGET_DIR" ]]; then
  SKILLS_DST="$TARGET_DIR/.claude/skills"
else
  SKILLS_DST="$HOME/.claude/skills"
fi

mkdir -p "$SKILLS_DST"

install_skill() {
  local skill_name="$1"
  local src="$SKILLS_SRC/$skill_name"
  local dst="$SKILLS_DST/$skill_name"

  if [[ ! -d "$src" ]]; then
    echo "  ERROR: skill '$skill_name' not found in $SKILLS_SRC"
    exit 1
  fi

  if [[ -d "$dst" && "$FORCE" == false ]]; then
    echo "  SKIP  $skill_name (already installed — use --force to overwrite)"
    return
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo "  DRY   $src → $dst"
  else
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "  OK    $skill_name → $dst"
  fi
}

echo "Installing Claude Code skills to $SKILLS_DST"
echo ""

if [[ -n "$TARGET_SKILL" ]]; then
  install_skill "$TARGET_SKILL"
else
  for skill_dir in "$SKILLS_SRC"/*/; do
    [[ -d "$skill_dir" ]] || continue
    install_skill "$(basename "$skill_dir")"
  done
fi

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run complete. Run without --dry-run to install."
else
  echo "Done. Restart Claude Code to pick up new skills."
fi
