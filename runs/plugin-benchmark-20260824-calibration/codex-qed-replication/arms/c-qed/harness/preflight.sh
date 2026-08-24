#!/usr/bin/env bash
set -euo pipefail

RunRoot=/mnt/f/benchmark/B3-O3-CAL-20260824/arm-c-qed-run1
QEDSource=$RunRoot/qed
OutputRoot=$RunRoot/output

test -f "$QEDSource/code/pipeline.py"
test -f "$QEDSource/code/model_runner.py"
test ! -e "$QEDSource/.git"
test -f "$OutputRoot/problem.tex"
test ! -e "$OutputRoot/AGENTS.md"
test "$(sha256sum "$OutputRoot/problem.tex" | cut -d ' ' -f 1)" = '1fa717b9a5f195c42ecca97d51e20327cb4eb2c316c936c054f55f7dd7416f16'
bash -n /mnt/f/benchmark/B3-O3-CAL-20260824/harness/qed-safe-bin/codex
bash -n /mnt/f/benchmark/B3-O3-CAL-20260824/harness/run-c.sh
python3 -m py_compile "$QEDSource/code/pipeline.py" "$QEDSource/code/model_runner.py" "$QEDSource/code/decomposition_prover.py"
echo 'PASS: pinned content export, frozen task, and safe adapter preflight'
