#!/usr/bin/env bash
set -euo pipefail

RunRoot=${1:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run1}
QEDSource=$RunRoot/qed
OutputRoot=$RunRoot/output
SafeBin=/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/qed-safe-bin
ConfigPath=$RunRoot/config.safe.yaml

export PATH="$SafeBin:/usr/bin:/bin:/home/huangzy/.local/bin"
export PYTHONDONTWRITEBYTECODE=1
export CODEX_HOME=/home/huangzy/.codex-benchmark/PILOT-V5-CODEX-U2-20260825/arm-c
export CODEX_PERMISSION_PROFILE=:workspace
export QED_REAL_CODEX=/home/huangzy/.local/bin/codex
export QED_MODEL_PROXY_URL=http://172.22.112.1:7898
export QED_WRAPPER_LOG=$RunRoot/wrapper.log
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy || true
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

cd "$QEDSource"
timeout --foreground --signal=INT --kill-after=30s 5400s \
	python3 code/pipeline.py \
	--input "$OutputRoot/problem.tex" \
	--output "$OutputRoot" \
	--config "$ConfigPath" \
	2>&1 | tee "$RunRoot/pipeline.log"
