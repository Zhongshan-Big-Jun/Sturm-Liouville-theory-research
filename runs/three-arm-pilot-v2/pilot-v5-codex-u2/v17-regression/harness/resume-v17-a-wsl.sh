#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V5-V17-U2-20260827}
ProxyUrl=${2:-http://172.22.112.1:7898}
SessionId=${3:-01a041fc-0f14-79b3-86b3-aef3d4aa1b8a}
CodexHome="$BenchRoot/codex-home"
WorkRoot="$BenchRoot/arm-a-plugin-v17"
CodexBin='/mnt/c/Program Files/WindowsApps/OpenAI.Codex_26.818.8289.0_x64__2p2nqsd0c76g0/app/resources/codex'
RemainingSeconds=1727

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

ResumePrompt='Continue the same scored v1.7 regression after the service hard-limit reset. Preserve the frozen contract and every existing artifact. Read only this work directory and the already installed plugin cache; do not use the internet or prior benchmark outputs. Do not spawn a new subagent, do not retry Route B, and do not open another research wave. Hash-check and ingest the completed Route A and Route C artifacts, record Route B as an incomplete return, and retain only claims that their written proofs support. Run the required fresh-context convergence check from files only. Finalize the partial candidate proof, obligation graph, ledger, research map, convergence_check.md, audit_report.md, final_report.md, final_response.md, artifact hashes, and reproducibility manifest. The fixed-constant C/sqrt(t) upper bound remains open unless an already written artifact proves it; do not claim completion. The remaining scored root active-wall allowance is 1727 seconds. Stop after writing the honest stopping-boundary package.'

timeout --foreground --signal=INT "${RemainingSeconds}s" "$CodexBin" exec resume \
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
