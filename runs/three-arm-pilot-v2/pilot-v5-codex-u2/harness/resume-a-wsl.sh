#!/usr/bin/env bash
set -euo pipefail

WorkRoot=${1:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2}
SessionId=${2:-01a03b91-c0d3-7792-ab90-c80bb7b40e46}
CodexHome=/home/huangzy/.codex-benchmark/B3-O3-CAL-20260824/arm-a
ProxyUrl=http://172.22.112.1:7898
RemainingSeconds=2036

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

cd "$WorkRoot"

ResumePrompt='Continue the same scored Arm A after the service hard rate limit reset. Preserve the frozen contract and all existing artifacts. Do not restart completed searches. Finish the pending independent route, merge only hash-checked results, perform the required fresh adversarial audit if quota permits, and finalize all required reports. The original 80 minute active wall cap has 2036 seconds remaining.'

timeout --foreground --signal=INT "${RemainingSeconds}s" codex exec resume \
	--ignore-rules \
	--skip-git-repo-check \
	--strict-config \
	--json \
	-m gpt-5.6-sol \
	-c 'model_reasoning_effort="xhigh"' \
	-c 'approval_policy="never"' \
	-c 'sandbox_mode="workspace-write"' \
	-c 'sandbox_workspace_write.network_access=false' \
	-c 'agents.enabled=true' \
	-c 'agents.default_subagent_model="gpt-5.6-sol"' \
	-c 'agents.default_subagent_reasoning_effort="xhigh"' \
	-c 'agents.max_concurrent_threads_per_session=3' \
	-o "$WorkRoot/final_response.md" \
	"$SessionId" \
	"$ResumePrompt" \
	2>> "$WorkRoot/stderr.log" \
	| tee -a "$WorkRoot/events.jsonl"
