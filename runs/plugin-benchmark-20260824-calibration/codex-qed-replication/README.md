# Codex and QED three-arm replication

Status: Arm A completed on 2026-08-24. Arms B and C are pending.

This replication executes the three systems from the original pre-registration with their actual runtimes:

- Arm A: Codex `gpt-5.6-sol`, `xhigh`, `rigorous-open-math-research` v1.6.0, and research subagents.
- Arm B: Codex `gpt-5.6-sol`, `xhigh`, with only the frozen prompt and no task skill, plugin, memory, project instructions, or subagent.
- Arm C: QED at commit `121900964e6572aaf094412d434b5ac2a792a65f`, executed through an offline safe adapter with one proof attempt, one revision, and one decomposition.

This supplements the earlier five-arm DSH calibration in the parent directory. That run used `deepseek-v4-flash-vision-exp` and prompt-level emulations for its external systems. The present replication must therefore be scored separately.

The B3 O3 task is historically contaminated. These results are regression calibration only, not evidence of out-of-distribution generalization.

## Stage protocol

Each arm receives the same frozen task. Solver directories contain no `.git` directory and cannot access the project repository, prior answer, memory, or network. Every candidate is copied to a neutral path and independently reviewed before its arm label is disclosed to the reviewer.

Scored solver usage excludes harness preflights and the post-hoc neutral reviewer. Infrastructure overhead and review outcomes are reported separately.

## Current state

- Arm A: `STRICT`, internal audit `PASS`, external anonymous audit `PASS`.
- Arm B: pending.
- Arm C: pending.

See `arms/a-plugin/stage_report.md` and `arms/a-plugin/metrics.json` for the first stage.
