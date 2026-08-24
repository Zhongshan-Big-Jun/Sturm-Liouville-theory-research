# Codex and QED three-arm replication

Status: completed on 2026-08-24. See `RESULTS.md` for the frozen comparison.

This replication executes the three systems from the original pre-registration with their actual runtimes:

- Arm A: Codex `gpt-5.6-sol`, `xhigh`, `rigorous-open-math-research` v1.6.0, and research subagents.
- Arm B: Codex `gpt-5.6-sol`, `xhigh`, with only the frozen prompt and no task skill, plugin, memory, project instructions, or subagent.
- Arm C: QED at commit `121900964e6572aaf094412d434b5ac2a792a65f`, executed through an offline safe adapter with one proof attempt, one revision, and one decomposition. Its Stage 0 role classified the task as Easy and short-circuited before the decomposition and verification roles.

This supplements the earlier five-arm DSH calibration in the parent directory. That run used `deepseek-v4-flash-vision-exp` and prompt-level emulations for its external systems. The present replication must therefore be scored separately.

The B3 O3 task is historically contaminated. These results are regression calibration only, not evidence of out-of-distribution generalization.

## Stage protocol

Each arm receives the same frozen task in a content-only cwd without a `.git` directory. The frozen protocol forbids project-repository, prior-answer, external-memory, and network use. Retained event logs are checked for violations. The filesystem sandbox may still expose generic read-only paths outside the cwd, so isolation claims are based on workspace construction, explicit protocol, and event audit rather than an OS-level claim that every outside path is unreadable. Every candidate is copied to a neutral path and independently reviewed before its arm label is disclosed to the reviewer.

Scored solver usage excludes harness preflights and the post-hoc neutral reviewer. Infrastructure overhead and review outcomes are reported separately.

## Final state

- Arm A: `STRICT`, internal audit `PASS`, external anonymous audit `PASS`.
- Arm B: `STRICT`, external anonymous audit `PASS`.
- Arm C: `STRICT`, external anonymous audit `PASS`; QED internal verification not exercised because of the Easy short circuit.

See `RESULTS.md` for the three-arm table and each arm's `stage_report.md` and `metrics.json` for frozen stage data.
