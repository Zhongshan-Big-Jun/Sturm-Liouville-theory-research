# Unpolluted OOD benchmark: exponential mixing by bounded shear

Status: preregistered 2026-08-24, not yet scored.

This benchmark is deliberately outside the project's Sturm-Liouville plugin history. The frozen problem is a hard PDE/Fourier-analysis problem from the QED benchmark set (problem 3, analysis-Apr-24-2026), but no reference solution is made available to solver arms. It is used only to test the actual Rethlas, Danus, and MMAT systems against the local plugin v1.6.0 and a blank control on a new domain.

## Frozen objects

- Task: `frozen_task.md`
- Source problem: QED benchmark `proved_statements/analysis-Apr-24-2026/problem-3.md` (correct proof withheld from arms).
- Model: all actual external arms run through Codex CLI backed by DeepSeek `deepseek-chat` via Responses API (locally configured).
- Pre-registered model for local plugin/blank arms: default DSH DeepSeek model.
- Network/repository access: prohibited for every arm. Each arm works only inside its own arm directory.

## Arms

- A: local plugin `rigorous-open-math-research` v1.6.0 (DSH subagent)
- B: blank control (plain prompt, no skills/memory/plugins/subagents)
- C: Rethlas actual deployment (Codex generation + verification service)
- D: Danus actual codex-branch deployment (worker/verifier fact-graph pipeline)
- E: MMAT actual NL-Prover deployment (Codex hub-and-spoke harness)

## Metric plan

- Wall-clock time.
- Codex/DSH model responses, tool calls, subagents, tokens.
- Output artifacts and status (proof/partial/no progress).
- Independent neutral mathematical review of each candidate.
- Leakage audit.

## Deployment locations

- Rethlas: `F:\tools\rethlas-clone\Rethlas`
- Danus: `F:\tools\danus-clone\Danus` (codex branch)
- MMAT: `F:\tools\mmat-agent-team`
- Codex CLI: `F:\tools\codex-cli` (DeepSeek Responses API)
