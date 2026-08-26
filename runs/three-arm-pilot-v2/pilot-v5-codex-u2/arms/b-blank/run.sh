#!/usr/bin/env bash
set -euo pipefail

WorkRoot=${1:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-b-blank-run1}
CodexHome=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-b
ProxyUrl=http://172.22.112.1:7898

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

timeout --foreground --signal=INT --kill-after=30s 2700s codex exec \
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
	-c 'agents.enabled=false' \
	-s workspace-write \
	-C "$WorkRoot" \
	-o "$WorkRoot/final_response.md" \
	- \
	< "$WorkRoot/TASK.md" \
	2> "$WorkRoot/stderr.log" \
	| tee "$WorkRoot/events.jsonl"
