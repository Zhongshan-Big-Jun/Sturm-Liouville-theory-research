#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828}
PacketRoot='/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v6-hs-domain'
SourceRoot='/mnt/f/LaTeX/BVE research/_xsoc1_work'
CodexHome="$BenchRoot/codex-home-a"
WorkRoot="$BenchRoot/arm-a-plugin-v17-run1"
CodexBin='/mnt/c/Program Files/WindowsApps/OpenAI.Codex_26.818.8289.0_x64__2p2nqsd0c76g0/app/resources/codex'

if [ -e "$CodexHome" ] || [ -e "$WorkRoot" ]
then
	echo 'Refusing to reuse Arm A home or work root.' >&2
	exit 2
fi

mkdir -p "$CodexHome" "$WorkRoot"
ln -s /mnt/c/Users/HuangZY/.codex/auth.json "$CodexHome/auth.json"
cp "$PacketRoot/arm-a-prompt.md" "$WorkRoot/PROMPT.md"

export CODEX_HOME="$CodexHome"
"$CodexBin" plugin marketplace add "$SourceRoot" --json
"$CodexBin" plugin add rigorous-open-math-research@math-research --json
"$CodexBin" plugin list > "$WorkRoot/plugin-list.txt"
sha256sum "$PacketRoot/frozen_task.md" > "$WorkRoot/frozen-task.sha256"
sha256sum "$WorkRoot/PROMPT.md" > "$WorkRoot/prompt.sha256"
sha256sum "$CodexBin" > "$WorkRoot/codex-cli.sha256"
sha256sum "$CodexHome/plugins/cache/math-research/rigorous-open-math-research/1.7.0/skills/rigorous-open-math-research/SKILL.md" > "$WorkRoot/plugin-skill.sha256"
git -C "$SourceRoot" rev-parse HEAD > "$WorkRoot/plugin-commit.txt"
