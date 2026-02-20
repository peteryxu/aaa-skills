#!/usr/bin/env bash
# install.sh — Install Claude Code skills to ~/.claude/skills/
#
# Usage:
#   ./install.sh                  Install all skills
#   ./install.sh drawio           Install a specific skill
#   ./install.sh --dry-run        Preview what would be installed
#   ./install.sh --force drawio   Overwrite existing skill

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/.claude/skills"
SKILLS_DST="$HOME/.claude/skills"

DRY_RUN=false
FORCE=false
TARGET_SKILL=""

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --force)   FORCE=true ;;
    --*)       echo "Unknown flag: $arg"; exit 1 ;;
    *)         TARGET_SKILL="$arg" ;;
  esac
done

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
