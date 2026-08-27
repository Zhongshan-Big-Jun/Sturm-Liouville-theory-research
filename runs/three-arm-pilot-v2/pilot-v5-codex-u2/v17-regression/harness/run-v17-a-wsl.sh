#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V5-V17-U2-20260827}
ProxyUrl=${2:-http://172.22.112.1:7897}
CodexHome="$BenchRoot/codex-home"
WorkRoot="$BenchRoot/arm-a-plugin-v17"

export CODEX_HOME="$CodexHome"
export CODEX_PERMISSION_PROFILE=:workspace
export HTTP_PROXY="$ProxyUrl"
export HTTPS_PROXY="$ProxyUrl"
export ALL_PROXY="$ProxyUrl"
export http_proxy="$ProxyUrl"
export https_proxy="$ProxyUrl"
export all_proxy="$ProxyUrl"
export NO_PROXY=127.0.0.1,localhost
export no_proxy=127.0.0.1,localhost
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

timeout --foreground --signal=INT 75m codex exec \
	--ignore-rules \
	--skip-git-repo-check \
	--strict-config \
	--json \
	--color never \
	-m gpt-5.6-sol \
	-c 'model_reasoning_effort="xhigh"' \
	-c 'approval_policy="never"' \
	-c 'sandbox_mode="workspace-write"' \
	-c 'sandbox_workspace_write.network_access=false' \
	-c 'agents.enabled=true' \
	-c 'agents.default_subagent_model="gpt-5.6-sol"' \
	-c 'agents.default_subagent_reasoning_effort="xhigh"' \
	-c 'agents.max_concurrent_threads_per_session=3' \
	-s workspace-write \
	-C "$WorkRoot" \
	-o "$WorkRoot/final_response.md" \
	- \
	< "$WorkRoot/PROMPT.md" \
	2> "$WorkRoot/stderr.log" \
	| tee "$WorkRoot/events.jsonl"
