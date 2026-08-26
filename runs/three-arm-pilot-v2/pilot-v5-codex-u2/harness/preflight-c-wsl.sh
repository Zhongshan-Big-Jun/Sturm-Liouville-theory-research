#!/usr/bin/env bash
set -euo pipefail

RunRoot=${1:-/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-c-qed-run1}
QEDSource=$RunRoot/qed
OutputRoot=$RunRoot/output

test -f "$QEDSource/code/pipeline.py"
test -f "$QEDSource/code/model_runner.py"
test ! -e "$QEDSource/.git"
test -f "$OutputRoot/problem.tex"
test ! -e "$OutputRoot/AGENTS.md"
test "$(sha256sum "$OutputRoot/problem.tex" | cut -d ' ' -f 1)" = '6859e0af922ba8454758e2195fcefcfe8fa164a40e2c23022ec7ebb2da228943'
bash -n /mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/qed-safe-bin/codex
bash -n '/mnt/f/LaTeX/BVE research/runs/three-arm-pilot-v2/pilot-v5-codex-u2/harness/run-c-wsl.sh'
export PYTHONPYCACHEPREFIX=/tmp/qed-pilot-v5-pyc
python3 -m py_compile "$QEDSource/code/pipeline.py" "$QEDSource/code/model_runner.py" "$QEDSource/code/decomposition_prover.py"
echo 'PASS: pinned content export, frozen task, and safe adapter preflight'
