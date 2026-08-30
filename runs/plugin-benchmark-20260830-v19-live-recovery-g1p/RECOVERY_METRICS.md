# Recovery metrics

## Functional verdict

`PASS_WITH_USABILITY_FINDINGS`.

The released v1.9 protocol preserved a real in-flight worker, forced
reconciliation before new dispatch, rejected a disappearing obligation, and
maintained the `RIGOROUS_PARTIAL_RESULT` label through two checkpoint segments.

## Segment 00

- Live unresolved worker: `W2-KP-FIRSTZERO-JACOBI`.
- Session ID: `/root/kp_jacobi`.
- Checkpoint ID:
  `sha256:758e11a3080e964e2884c1066447cb1e195644627065de0a9d3cb7064306867f`.
- Verification: `READY`, 5 checked artifacts.
- Receipt first action: `RECONCILE-W2-SEG00`.
- Reconciliation outcome: `INGESTED`.
- Successful receipt command: 164.035 ms.

## Segment 01

- Checkpoint ID:
  `sha256:b31a2c568f5768c296e277da17a7fb9fcefdb93efb01d6211bf2e3de575002fc`.
- Verification: `READY`, 12 checked artifacts.
- Receipt first action: `AUDIT-MERGED-PARTIAL`.
- Complete seal, verify, and receipt chain: 698.159 ms.
- Audit outcome: `PASS` for the strict partial package.

## Replay and duplicate cost

- Worker restarts: 0.
- Duplicate research dispatches: 0.
- Model calls between segment 00 seal and canonical receipt: 0.
- Network calls between segment 00 seal and canonical receipt: 0.
- Transcript or chat replay: 0.
- Mathematical label changes caused by interruption: 0.

## Deterministic input failures

1. Passing a project-prefixed relative state path duplicated the project root.
2. PowerShell's seven-digit fractional ISO timestamp was rejected.
3. Renaming an inherited open obligation in sequence 01 was rejected until the
   predecessor ID and replaced action were preserved.

The first two are usability defects. The third is a successful safety guard.
All three occurred before model dispatch and caused no mathematics loss.
