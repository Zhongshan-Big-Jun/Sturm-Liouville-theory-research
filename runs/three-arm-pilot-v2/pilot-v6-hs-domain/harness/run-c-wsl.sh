#!/usr/bin/env bash
set -euo pipefail

BenchRoot=${1:-/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828}
RunName=${2:-arm-c-qed-run1}
CodexHomeName=${3:-codex-home-c}
ProxyUrl=${4:-http://172.22.112.1:7898}
RunRoot="$BenchRoot/$RunName"
QEDRoot="$RunRoot/qed"
OutputRoot="$RunRoot/output"
SafeBin="$RunRoot/safe-bin"
CodexHome="$BenchRoot/$CodexHomeName"
CodexBin='/mnt/c/Program Files/WindowsApps/OpenAI.Codex_26.818.8289.0_x64__2p2nqsd0c76g0/app/resources/codex'

export PATH="$SafeBin:/usr/bin:/bin:/home/huangzy/.local/bin"
export PYTHONDONTWRITEBYTECODE=1
export CODEX_HOME="$CodexHome"
export CODEX_PERMISSION_PROFILE=:workspace
export QED_CODEX_HOME="$CodexHome"
export QED_REAL_CODEX="$CodexBin"
export QED_MODEL_PROXY_URL="$ProxyUrl"
export QED_WRAPPER_LOG="$RunRoot/wrapper.log"
export QED_PROMPT_ADAPTER="$SafeBin/qed-inline-prompt.py"
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy || true
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

cd "$QEDRoot"
timeout --foreground --signal=INT --kill-after=30s 5400s \
	python3 code/pipeline.py \
	--input "$OutputRoot/problem.tex" \
	--output "$OutputRoot" \
	--config "$RunRoot/config.safe.yaml" \
	2>&1 | tee "$RunRoot/pipeline.log"
