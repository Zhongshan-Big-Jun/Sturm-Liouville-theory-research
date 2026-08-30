# v1.9 live in-flight recovery benchmark

## Classification

- Mode: `PROGRAM_AND_DELEGATE`.
- Run ID: `R-20260830T020000Z-g1p-live-recovery`.
- Task ID: `Q-20260830-g1p-live-recovery`.
- Status: `PREREGISTERED`.
- Scoring: functional recovery drill, not an efficiency arm.
- Experiment integrity metrics: disabled in the checkpoint schema because
  collaboration-agent token and cost counters are not available as auditable
  measurements.

## Mathematical target

Prove or refute all-finite-R negative definiteness of the two normalized n=2
symmetric INF sector matrices. Use the strict near-one and accepted large-R
anchors. Do not extend the claim to non-symmetric roots or global G1 prime.

## Recovery protocol

1. Pass the isolated workspace pipeline gate.
2. Run one closure-first planner with no child delegation.
3. Only after an explicit `ESCALATE`, dispatch two distinct bounded workers.
4. Ingest the first completed worker and leave the second genuinely in flight.
5. Freeze and seal segment 00 with that worker's exact session ID.
6. After sealing, make no new research call in segment 00.
7. Verify the checkpoint and create one canonical resume receipt.
8. Segment 01 starts with `RECONCILE_INFLIGHT` and no new dispatch.
9. Record the worker as `INGESTED`, `INTERRUPTED`, or `NO_RETURN`.
10. Audit the strongest merged package and preserve every open obligation.

## Pass criteria

- The scoped pipeline gate passes before dispatch.
- The segment 00 checkpoint verifies `READY` and names a live worker/session.
- The resume receipt selects `RECONCILE_INFLIGHT` with a minimal read set.
- Segment 01 reconciles the same worker before any new dispatch.
- Completed action IDs are not repeated.
- Mathematical labels survive recovery without inflation.
- Checkpoint overhead is measured separately from research wall time.

## Stop condition

Stop after segment 01 reconciliation, independent mathematical audit, scoped
validation, parent repository commit, and pushes to origin then fork.
