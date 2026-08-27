#!/usr/bin/env bash
set -euo pipefail

CodexHome=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-c
AuthSource=/mnt/c/Users/HuangZY/.codex/auth.json
ConfigSource='/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v5-codex-u2/harness/arm-c.config.toml'
HarnessRoot='/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v5-codex-u2/harness'
SafeBin=/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/qed-safe-bin

mkdir -p "$CodexHome"
chmod 700 "$CodexHome"

if [ ! -e "$CodexHome/auth.json" ]
then
	ln -s "$AuthSource" "$CodexHome/auth.json"
fi

cp "$ConfigSource" "$CodexHome/config.toml"
mkdir -p "$SafeBin"
cp "$HarnessRoot/codex-safe-adapter-c.sh" "$SafeBin/codex"
cp "$HarnessRoot/qed-inline-prompt.py" "$SafeBin/qed-inline-prompt.py"
chmod 755 "$SafeBin/codex" "$SafeBin/qed-inline-prompt.py"
CODEX_HOME="$CodexHome" codex login status
