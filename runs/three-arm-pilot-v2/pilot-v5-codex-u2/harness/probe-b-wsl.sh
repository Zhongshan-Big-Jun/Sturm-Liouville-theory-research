#!/usr/bin/env bash
set -euo pipefail

RunRoot=/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825
WorkRoot=$RunRoot/arm-b-blank-run1
ProbeOutput=$RunRoot/arm-b-prompt-input.json

export CODEX_HOME=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-b
export CODEX_PERMISSION_PROFILE=:workspace
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

cd "$WorkRoot"
codex debug prompt-input 'BENCH_PROBE' > "$ProbeOutput"

printf 'PROMPT_INPUT_SHA256 '
sha256sum "$ProbeOutput" | cut -d ' ' -f 1
for Needle in 'AGENTS.md instructions' 'Available skills' 'rigorous-open-math-research' 'manage-math-research-program' 'math-research-workflow' 'lean-verify' 'plugins_instructions' 'multi_agent_mode' '<recommended_plugins>'
do
	printf '%s=' "$Needle"
	grep -Foc "$Needle" "$ProbeOutput" || true
done

if ! grep -Fq 'BENCH_PROBE' "$ProbeOutput"
then
	echo 'FAIL: probe prompt missing' >&2
	exit 1
fi

for Needle in 'AGENTS.md instructions' 'Available skills' 'rigorous-open-math-research' 'manage-math-research-program' 'math-research-workflow' 'lean-verify' 'plugins_instructions' 'multi_agent_mode' '<recommended_plugins>'
do
	if grep -Fq "$Needle" "$ProbeOutput"
	then
		echo "FAIL: leaked $Needle" >&2
		exit 1
	fi
done

echo 'PASS: blank model context'
