#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
codex_root="${SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
skills=("$@")
if [[ ${#skills[@]} -eq 0 ]]; then
  while IFS= read -r skill_path; do skills+=("$(basename "$skill_path")"); done < <(find "$repo_dir/skills" -mindepth 1 -maxdepth 1 -type d | sort)
fi

mkdir -p "$codex_root"

for skill in "${skills[@]}"; do
  skill_source="$repo_dir/skills/$skill"
  skill_target="$codex_root/$skill"
  if [[ ! -f "$skill_source/SKILL.md" ]]; then
    echo "Unknown skill: $skill" >&2
    exit 1
  fi
  if [[ -L "$skill_target" && "$(readlink "$skill_target")" == "$skill_source" ]]; then
    echo "Already installed: $skill_target"
    continue
  fi

  if [[ -e "$skill_target" || -L "$skill_target" ]]; then
    echo "Refusing to replace existing path: $skill_target" >&2
    echo "Move or remove it explicitly, then rerun this installer." >&2
    exit 1
  fi

  ln -s "$skill_source" "$skill_target"
  echo "Installed: $skill_target -> $skill_source"
done
echo "Restart Codex to discover the skill."
