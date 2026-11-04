#!/bin/sh
# Safe installer for Nepal SEO Expert. Copies the complete skill without .git.
set -eu

usage() {
  cat <<'EOF'
Usage: sh install.sh <claude|opencode|codex|agents> <global|project>

Examples:
  sh install.sh codex global
  sh install.sh opencode project

The installer never overwrites an existing skill folder.
EOF
}

if [ "$#" -ne 2 ]; then
  usage >&2
  exit 2
fi

tool=$1
scope=$2
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "error: SKILL.md was not found beside install.sh" >&2
  exit 1
fi

case "$tool:$scope" in
  claude:global) parent=${HOME:?HOME is required}/.claude/skills ;;
  claude:project) parent=.claude/skills ;;
  opencode:global) parent=${HOME:?HOME is required}/.config/opencode/skills ;;
  opencode:project) parent=.opencode/skills ;;
  codex:global) parent=${HOME:?HOME is required}/.codex/skills ;;
  codex:project) parent=.codex/skills ;;
  agents:global) parent=${HOME:?HOME is required}/.agents/skills ;;
  agents:project) parent=.agents/skills ;;
  *)
    usage >&2
    exit 2
    ;;
esac

target=$parent/nepal-seo-expert
if [ -e "$target" ]; then
  echo "error: $target already exists; it was not changed" >&2
  exit 1
fi

mkdir -p "$parent"
mkdir "$target"

for item in "$source_dir"/.[!.]* "$source_dir"/*; do
  [ -e "$item" ] || continue
  name=${item##*/}
  case "$name" in
    .git|.DS_Store|__pycache__) continue ;;
  esac
  cp -R "$item" "$target/"
done

if [ ! -f "$target/SKILL.md" ]; then
  echo "error: install did not finish; remove $target and try again" >&2
  exit 1
fi

printf 'Installed Nepal SEO Expert in %s\n' "$target"
printf 'Start a new session and ask: Use the nepal-seo-expert skill to audit this site.\n'
