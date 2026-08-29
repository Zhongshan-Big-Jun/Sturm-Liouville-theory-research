# Recovery drill contract

## Exact task

Apply the released v1.9 deterministic quota checkpoint protocol to a
files-only reconstruction of the v1.7 U2 regression boundary.

## Required behavior

- Preserve run, task, arm, workspace, prompt, harness, source, and hidden-gold
  identity across segments.
- Preserve the historical `RIGOROUS_PARTIAL_RESULT` label.
- Reconcile the recorded incomplete Route B worker before any continuation.
- Carry cumulative historical metrics without charging drill overhead.
- Read only the checkpoint receipt's minimal read set.

## Forbidden behavior

- No new model, sub-agent, network, proof, audit, or mathematical computation.
- No transcript or event-log replay.
- No retry of Route A, Route B, Route C, or the frozen `O3` target.
- No edits to the historical v1.7 run.

## Completion

Both numbered checkpoints verify `READY`, the predecessor lineage is valid,
Route B has a hash-bound `NO_RETURN` reconciliation, and the drill report gives
measured local overhead separately from scored historical metrics.
