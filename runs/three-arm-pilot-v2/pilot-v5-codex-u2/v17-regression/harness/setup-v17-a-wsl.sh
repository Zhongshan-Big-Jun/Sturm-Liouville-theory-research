#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V5-V17-U2-20260827}
SourceRoot=${2:-/mnt/f/LaTeX/BVE\ research/_xsoc1_work}
PacketRoot=${3:-/mnt/f/LaTeX/BVE\ research/runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression}
CodexHome="$BenchRoot/codex-home"
WorkRoot="$BenchRoot/arm-a-plugin-v17"

if [[ -e "$BenchRoot" ]]
then
	echo "Refusing to reuse existing benchmark root: $BenchRoot" >&2
	exit 2
fi

mkdir -p "$CodexHome" "$WorkRoot"
ln -s /mnt/c/Users/HuangZY/.codex/auth.json "$CodexHome/auth.json"
cp "$PacketRoot/PROMPT.md" "$WorkRoot/PROMPT.md"

export CODEX_HOME="$CodexHome"
codex plugin marketplace add "$SourceRoot" --json
codex plugin add rigorous-open-math-research@math-research --json
codex plugin list > "$WorkRoot/plugin-list.txt"
sha256sum "$WorkRoot/PROMPT.md" > "$WorkRoot/prompt.sha256"
sha256sum "$CodexHome/plugins/cache/math-research/rigorous-open-math-research/1.7.0/skills/rigorous-open-math-research/SKILL.md" > "$WorkRoot/plugin-skill.sha256"
