# Five-arm calibration benchmark (B3 O3)

Status: executed on 2026-08-24. This is a contaminated regression calibration.

The B3 O3 problem was used in earlier plugin work, and plugin v1.6.0 was optimized with knowledge of that history. Results from this calibration must not be used as evidence of out-of-distribution generalization.

## Frozen objects

- Calibration problem source commit: `613cf5f1e103c99563987d01d5d2a43adca93746`.
- Historical gold commit, hidden from solvers: `e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f`.
- Frozen task: `frozen_task.md`.
- Model requested by pre-registration: `gpt-5.6-sol` with `xhigh` reasoning.
- Actual runtime model (all arms): `deepseek-v4-flash-vision-exp` with `high` reasoning, as recorded in DSH session descriptors. This is a protocol deviation from the pre-registered model and must be noted in any scoring interpretation.
- Network and external research: forbidden for every arm.

## Arms

- **Arm A — our-plugin v1.6.0**: `rigorous-open-math-research` v1.6.0, parent plugin commit `88e1c97`, DSH repo `0cc9961`, skills enabled, no nested subagents spawned by the arm.
- **Arm B — blank control**: plain model with only the frozen task prompt; skills/plugins/memories/subagents disabled by instruction.
- **Arm C — Rethlas methodology**: prompt-level emulation of Rethlas-style memory/branch/counterexample traces; the original external repository is not executed as a full verified service.
- **Arm D — Danus methodology**: prompt-level emulation of Danus-style orchestrator/worker/verifier-gate fact graph; the original external repository is not executed as a full verified service.
- **Arm E — MMath/MMAT methodology**: prompt-level emulation of MechMath MMAT-style obligation-decomposition/verification roles; the original external solver is not executed as a full verified service.

External arms are methodology-inspired single-session emulations, not complete reproductions of the upstream systems. They receive the same frozen task and isolation rules, and they emulate the public workflow shape (memory, fact gates, obligation graphs) inside their own arm directories.

## Isolation

Each solver receives only `frozen_task.md` in a content-only directory without `.git`. Solver prompts forbid repository, memory, internet, and prior-solution inspection. Raw tool logs are retained and audited for path or network leakage. A run that reads forbidden material is marked contaminated and excluded.

Forbidden material includes the full historical `runs/plugin-perf-eval2/` tree, the known Chebyshev and Jacobi root-count tools, current project state files, current `AGENTS.md`, all git metadata, and all network sources.

## Resource policy

- Arm A may use at most 3 concurrent research subagents (it spawned none).
- Arm B may not spawn subagents.
- External-methodology arms are single-session prompt-level emulations; they may use memory/fact/verifier artifacts but not nested fresh agents.
- No arm receives project-local helper scripts or literature.
- A run stops at 60 minutes if it has not already returned a result (all arms returned within this cap).

## Captured metrics

- Wall-clock time.
- Total input tokens, cached input tokens, and output tokens when exposed by the runtime.
- Model calls, tool calls, steps, and subagent count.
- Output artifact bytes.
- Leakage and protocol violations.
- Independent mathematical evaluation.

Metrics are in `metrics.json` (or the equivalent table in `RESULTS.md`).

## Independent mathematical evaluation

Every candidate is copied to a neutral identifier and reviewed without the arm label. The reviewer checks statement fidelity, recurrence or equivalent reduction, complete root count, interval endpoints, simplicity, `n=1`, `y=0`, `y=pi`, `y=pi/2`, and the `R=1` boundary. Labels are `PASS`, `REPAIRABLE_GAP`, or `FATAL_GAP`. Numerical evidence never upgrades a theorem to `STRICT`.

Only audited mathematical content is integrated into the project. A correct result that duplicates known mathematics is retained as a benchmark reproduction, not claimed as a novel theorem.
