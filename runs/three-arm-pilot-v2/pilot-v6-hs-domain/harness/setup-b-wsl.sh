#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828}
PacketRoot='/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v6-hs-domain'
CodexHome="$BenchRoot/codex-home-b"
WorkRoot="$BenchRoot/arm-b-blank-run1"

if [ -e "$CodexHome" ] || [ -e "$WorkRoot" ]
then
	echo 'Refusing to reuse Arm B home or work root.' >&2
	exit 2
fi

mkdir -p "$CodexHome" "$WorkRoot"
ln -s /mnt/c/Users/HuangZY/.codex/auth.json "$CodexHome/auth.json"
cp "$PacketRoot/harness/arm-b.config.toml" "$CodexHome/config.toml"
cp "$PacketRoot/frozen_task.md" "$WorkRoot/TASK.md"
sha256sum "$WorkRoot/TASK.md" > "$WorkRoot/task.sha256"
