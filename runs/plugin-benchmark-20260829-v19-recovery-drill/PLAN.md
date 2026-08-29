# v1.9 quota recovery drill

## Classification

- Mode: `PROGRAM_ONLY`.
- Run ID: `R-20260829T014000Z-v19-recovery-drill`.
- Status: `PREREGISTERED_FILES_ONLY_DRILL`.
- Mathematical research: none.
- Model, sub-agent, and network calls: forbidden.

## Objective

Exercise the released v1.9 checkpoint protocol against the frozen, audited
v1.7 U2 regression package that previously crossed a five-hour quota boundary.
The drill must preserve the original `RIGOROUS_PARTIAL_RESULT` label and scored
metrics while proving that deterministic recovery needs no transcript replay or
new research call.

## Frozen inputs

- Project source commit: `0d25f52c8f40e590dde7e285e7b367064f2a0f0f`.
- Recovery implementation: local Codex
  `math-research-workflow/1.9.0/scripts/checkpoint_resume.py`.
- Implementation SHA256:
  `be6e1d6cad3089451c9213c6f81b3a4ec962d9c939de5aa71fd63f5a7ab9dc1a`.
- Historical benchmark:
  `runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/`.
- Historical solver label: `RIGOROUS_PARTIAL_RESULT`.
- Historical open target: fixed-constant `C/sqrt(t)` upper bound at `O3`.

## Frozen reconstruction

Segment 00 reconstructs the first quota boundary from recorded session data:

- model responses: 56;
- tool calls: 44;
- uncached input tokens: 211820;
- cached input tokens: 1702912;
- output tokens: 101940;
- root wall seconds: 1311.844;
- cost proxy: USD 3.5672448;
- unresolved worker: Route B session
  `01a04203-2e61-7293-b637-4a6f4a313c06`.

Segment 01 reconciles Route B as `NO_RETURN`, binds the predecessor checkpoint
and receipt, and records the final historical cumulative metrics. It performs
no new proof, audit, or scored computation.

## Pass criteria

1. Segment 00 seals, verifies `READY`, and creates exactly one canonical receipt.
2. The receipt selects `RECONCILE_INFLIGHT` and exposes only the task contract
   and reconstructed whiteboard as its minimal read set.
3. Segment 01 records the same worker/session as `NO_RETURN`, carries all
   completed and do-not-repeat IDs, preserves the result label, and uses
   non-decreasing cumulative metrics.
4. Segment 01 seals and verifies `READY`; the full predecessor chain is valid.
5. Deterministic overhead is measured separately and excluded from historical
   scored metrics.
6. No historical benchmark artifact is edited.

## Stop condition

Stop immediately after the segment 01 `READY` verdict, deterministic report,
project validation, and repository sync. Do not start a mathematics arm.
