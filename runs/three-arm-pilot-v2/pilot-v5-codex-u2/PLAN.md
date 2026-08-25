# Pilot v5: Codex U2 three-arm benchmark

Status: preregistered before any pilot v5 solver arm.

## Objective

Run a real Codex three-arm benchmark on the clarified U2 switch-walk-switch problem.
The mathematical output of every arm is retained. Only independently audited results may be
promoted into the project documentation.

## Frozen interpretation

An element of `Z_2 wr Z` is written `(eta,z)`, where `eta` is a finitely supported lamp
configuration and `z` is the base position. Thus `(0,2)` means the all-zero lamp configuration
with base position `2`. This removes the ambiguity that invalidated the strongest U2 candidate
in pilot v4.

## Arms

- Arm A: `gpt-5.6-sol`, `xhigh`, rigorous-open-math-research v1.6.0, research subagents enabled.
- Arm B: `gpt-5.6-sol`, `xhigh`, frozen prompt only, all skills, plugins, memories, and subagents disabled.
- Arm C: QED pinned at commit `121900964e6572aaf094412d434b5ac2a792a65f`, through the previously audited offline-safe Codex adapter.

Arm A and Arm B use the same base model and reasoning effort. Arm C is an advanced-system
comparison, not an ablation of the prompt alone.

## Isolation and pollution

- Each arm receives only `frozen_task.md` in a content-only working directory.
- Network use, repository inspection, git history, prior U2 outputs, project memory, and prior
  answers are forbidden during the blind discovery phase.
- U2 appeared in pilot v4 under DeepSeek. Pilot v5 is therefore a new-model replication, not a
  claim that the mathematical problem has never appeared in the broader project.
- Event logs will be checked for reads outside the arm directory and other protocol violations.
- Candidate files are copied to neutral paths before label-blind review.

## Five-hour usage policy

The account exposes a rolling 300-minute primary window and a 10080-minute secondary window.
At preregistration, the primary window was at 3 percent and the secondary window at 0 percent.

- Use no more than 75 percent of any five-hour window for planned work.
- Reserve the final 25 percent for audit repair, artifact recovery, and user interaction.
- Stop a solver if the primary window reaches 45 percent during Arm A.
- Stop all model-heavy work at 65 percent unless an active turn is already completing.
- Start no new solver after 75 percent.
- Stop the whole benchmark campaign at 70 percent of the weekly window and retain 30 percent.

## Window schedule

### Window 1

1. Freeze and audit the task contract.
2. Run Arm A with a wall cap of 80 minutes and the 45-percent primary-window stop.
3. Run one independent blind audit.
4. Permit at most one targeted repair and one re-audit.
5. Save stage metrics and commit any audited mathematical result.

### Window 2

1. Run Arm B with a wall cap of 45 minutes.
2. Run Arm C with a wall cap of 90 minutes.
3. Apply the same neutral, label-blind review rubric.
4. Produce the final comparison, integrate audited mathematics, commit, and push.

## Scoring

Primary outcome:

- `PASS`
- `REPAIRABLE_GAP`
- `FATAL_GAP`
- `WRONG_PROBLEM`
- `PARTIAL_NOT_COMPLETE`
- `NO_ARTIFACT`

Secondary metrics include wall time, model responses, tool calls, input tokens, cached input,
uncached input, output tokens, reasoning output, artifact bytes, citation fidelity, and protocol
violations. Numerical evidence never counts as a proof.

## Stage reporting

After every arm, report the quota before and after, wall time, token and tool metrics, result
label, strongest exact mathematical claim, audit status, and remaining gap.
