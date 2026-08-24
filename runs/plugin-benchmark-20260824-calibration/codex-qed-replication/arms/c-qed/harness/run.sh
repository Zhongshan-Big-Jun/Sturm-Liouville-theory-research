#!/usr/bin/env bash
set -euo pipefail

RunRoot=/mnt/f/benchmark/B3-O3-CAL-20260824/arm-c-qed-run1
QEDSource=$RunRoot/qed
OutputRoot=$RunRoot/output
SafeBin=/mnt/f/benchmark/B3-O3-CAL-20260824/harness/qed-safe-bin
QEDCodexHome=/home/huangzy/.codex-benchmark/B3-O3-CAL-20260824/arm-c

export PATH="$SafeBin:/usr/bin:/bin:/home/huangzy/.local/bin"
export PYTHONDONTWRITEBYTECODE=1
export CODEX_HOME="$QEDCodexHome"
export CODEX_PERMISSION_PROFILE=:workspace
export QED_MODEL_PROXY_URL
QED_MODEL_PROXY_URL=$(cat /mnt/f/benchmark/B3-O3-CAL-20260824/harness/selected-proxy.txt)
export QED_WRAPPER_LOG=$RunRoot/wrapper.log
export QED_QUOTA_STOP_USED_PERCENT=75
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy || true
unset CODEX_SESSION_ID CODEX_THREAD_ID CODEX_INTERNAL_ORIGINATOR_OVERRIDE || true

cd "$QEDSource"
timeout --signal=INT --kill-after=30s 2700s \
	python3 code/pipeline.py \
	--input "$OutputRoot/problem.tex" \
	--output "$OutputRoot" \
	--config "$RunRoot/config.safe.yaml" \
	2>&1 | tee "$RunRoot/pipeline.log"
