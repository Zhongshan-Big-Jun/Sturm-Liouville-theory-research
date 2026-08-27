#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828}
PacketRoot='/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v6-hs-domain'
QEDSource='/mnt/f/tools/qed-benchmark'
RunRoot="$BenchRoot/arm-c-qed-run1"
CodexHome="$BenchRoot/codex-home-c"
SafeBin="$RunRoot/safe-bin"
QEDRoot="$RunRoot/qed"
OutputRoot="$RunRoot/output"

if [ -e "$RunRoot" ] || [ -e "$CodexHome" ]
then
	echo 'Refusing to reuse Arm C home or work root.' >&2
	exit 2
fi

mkdir -p "$RunRoot" "$CodexHome" "$SafeBin" "$OutputRoot/related_info"
ln -s /mnt/c/Users/HuangZY/.codex/auth.json "$CodexHome/auth.json"
cp "$PacketRoot/harness/arm-c.config.toml" "$CodexHome/config.toml"
git clone --quiet --no-hardlinks "$QEDSource" "$QEDRoot"
git -C "$QEDRoot" checkout --quiet --detach 121900964e6572aaf094412d434b5ac2a792a65f
cp "$PacketRoot/frozen_task.md" "$OutputRoot/problem.tex"
cp "$PacketRoot/harness/arm-c-qed.config.yaml" "$RunRoot/config.safe.yaml"
cp "$PacketRoot/harness/codex-safe-adapter-c.sh" "$SafeBin/codex"
cp "$PacketRoot/harness/qed-inline-prompt.py" "$SafeBin/qed-inline-prompt.py"
chmod 755 "$SafeBin/codex" "$SafeBin/qed-inline-prompt.py"
printf '%s\n' '# Offline related-work status' '' 'No external literature, repository result, prior answer, citation, or mathematical hint is available in this blind arm. Every theorem used must be proved self-containedly or identified as unverified.' > "$OutputRoot/related_info/related_work.md"
printf '%s\n' '# Neutral difficulty assessment' '' 'The problem has three load-bearing operator-domain and density obligations. No polarity, solution route, or expected answer is supplied.' > "$OutputRoot/related_info/difficulty_evaluation.md"
git -C "$QEDRoot" rev-parse HEAD > "$RunRoot/qed-commit.txt"
sha256sum "$OutputRoot/problem.tex" > "$RunRoot/task.sha256"
