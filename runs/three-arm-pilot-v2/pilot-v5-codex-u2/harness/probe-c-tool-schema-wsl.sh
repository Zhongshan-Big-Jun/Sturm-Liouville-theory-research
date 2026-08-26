#!/usr/bin/env bash
set -euo pipefail

WorkRoot=${1:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/tool-schema-probe-c}
CodexHome=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-c
ProxyUrl=http://172.22.112.1:7898
Prompt='Do not call any tool. Inspect the actual callable tool schemas visible in this turn. Return one compact JSON object with keys all_tool_names and internet_capable_tool_names. Use exact callable names. Do not infer from prose instructions.'

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

timeout --foreground --signal=INT --kill-after=30s 300s codex exec \
	--ignore-rules \
	--skip-git-repo-check \
	--strict-config \
	--json \
	--color never \
	-m gpt-5.6-sol \
	-c 'model_reasoning_effort="low"' \
	-c 'approval_policy="never"' \
	-c 'sandbox_mode="workspace-write"' \
	-c 'sandbox_workspace_write.network_access=false' \
	-c 'agents.enabled=false' \
	-c 'features.code_mode_host=false' \
	-s workspace-write \
	-C "$WorkRoot" \
	-o "$WorkRoot/final_response.md" \
	"$Prompt" \
	2> "$WorkRoot/stderr.log" \
	| tee "$WorkRoot/events.jsonl"
