# Three-arm calibration benchmark

Status: preregistered, not yet scored.

This run is a contaminated regression calibration. The B3 O3 problem was used in earlier plugin work, and plugin v1.6.0 was optimized with knowledge of that history. Results from this calibration must not be used as evidence of out-of-distribution generalization.

## Frozen objects

- Calibration problem source commit: `613cf5f1e103c99563987d01d5d2a43adca93746`.
- Historical gold commit, hidden from solvers: `e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f`.
- Arm A: `rigorous-open-math-research` v1.6.0, parent plugin commit `88e1c97`, with subagents.
- Arm B: plain Codex with only the frozen task prompt, with skills, plugins, memories, and multi-agent disabled.
- Arm C: `proofQED/QED` at commit `121900964e6572aaf094412d434b5ac2a792a65f`.
- Model for every model call: `gpt-5.6-sol` with `xhigh` reasoning.
- Network and external research: forbidden for every arm.
- Run order: A, then B, then C. Each arm is gated by the live quota check after the preceding arm.

## Isolation

Each solver receives only `frozen_task.md` in a content-only directory without `.git`. Solver prompts forbid repository, memory, internet, and prior-solution inspection. Raw tool logs are retained and audited for path or network leakage. A run that reads forbidden material is marked contaminated and excluded.

Forbidden material includes the full historical `runs/plugin-perf-eval2/` tree, the known Chebyshev and Jacobi root-count tools, current project state files, current `AGENTS.md`, all git metadata, and all network sources.

## Resource policy

- Arm A may use at most 3 concurrent research subagents.
- Arm B may not spawn subagents.
- Arm C uses its native orchestration with `max_proof_attempts=1`, `max_revisions=1`, and `max_decompositions=1`.
- No arm receives project-local helper scripts or literature.
- A run stops at 60 minutes if it has not already returned a result.

## Captured metrics

- Wall-clock time.
- Total input tokens, cached input tokens, and output tokens when exposed by the runtime.
- Model calls, tool calls, and subagent count.
- Output artifact bytes.
- Live weekly quota percentage before and after each arm.
- Leakage and protocol violations.

## Independent mathematical evaluation

Every candidate is copied to a neutral identifier and reviewed without the arm label. The reviewer checks statement fidelity, recurrence or equivalent reduction, complete root count, interval endpoints, simplicity, `n=1`, `y=0`, `y=pi`, `y=pi/2`, and the `R=1` boundary. Labels are `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. Numerical evidence never upgrades a theorem to `STRICT`.

Only audited mathematical content is integrated into the project. A correct result that duplicates known mathematics is retained as a benchmark reproduction, not claimed as a novel theorem.

