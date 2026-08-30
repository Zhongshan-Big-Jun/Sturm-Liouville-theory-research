# Whiteboard

- **Run ID:** `R-20260830T020000Z-g1p-live-recovery`
- **Task packet ID:** `Q-20260830-g1p-live-recovery`

## Current plan

Worker W1 is ingested as `PARTIAL`. Seal checkpoint sequence 00 while W2 remains
live, then reconcile that exact session before any new dispatch.

## Frozen target

Exact `n=2` symmetric INF branch only. Prove both normalized two-by-two sector matrices negative definite for every finite `R>1`. Do not claim global `G1'`.

## First open load-bearing claim

`KP-DET`: `det Kp_odd(R)>0` for every finite `R>1` on the prescribed branch.

## Why trace is not first

Near `R=1`, `Kp_odd` is strictly negative definite. If its determinant stays positive on the connected continuous branch, its two eigenvalues can never cross zero, hence it remains negative definite and its trace stays negative. The same applies to `Ko`.

## Current exact frontier

Any failure of `KP-DET` is confined to a compact middle interval. At the first loss there is either a nonzero kernel vector satisfying the exact half-Green equation or the exceptional matrix identity `Kp_odd=0`.

## Current gate

`ESCALATE`.

## Decision-changing next actions

1. Prove compact-middle coercivity of the exact `Kp_odd` quadratic form using the signed half-Green spectral split.
2. Independently treat a hypothetical first-zero kernel as a linearized Jacobi field and either contradict Sturm/transversality structure or produce an exact witness.

No worker was dispatched by this planner.

## Route history

- `DIRECT-INERTIA-BRIDGE` `[PARTIAL]`: determinant positivity reduces each
  sector's trace obligation and confines failure to a compact-middle first
  zero. Evidence: `direct_attempt.md`.
- `JINV-MONOTONICITY` `[BLOCKED]`: the recorded branch derivative uses
  `J^(-1)` and is circular at a hypothetical singular point. Evidence:
  `direct_attempt.md`.
- `W1-KP-SPECTRAL-COERCIVITY` `[PARTIAL]`: strict semiseparable reduction,
  `b>0`, and double-zero exclusion. The corank-one branch equality remains.
  Evidence: `route-01-spectral-coercivity/route_report.md`.
- `W2-KP-FIRSTZERO-JACOBI` `[PARTIAL]`: still in flight at checkpoint sequence
  00. Its current files are mutable and are not checkpoint evidence.

## Ideas to return to

- Exact half-Green spectral coercivity for `Kp_odd`.
- A singular-point Jacobi or transfer-matrix transversality argument that does
  not invert the singular branch Jacobian.

## Open obligations

1. `KP-FIRSTZERO`, hence `KP-DET`.
2. `KO-DET`, intentionally deferred by closure-first ordering.
3. Reconcile live worker `W2-KP-FIRSTZERO-JACOBI`, session
   `/root/kp_jacobi`, before any new dispatch.

## Key artifacts

- `problem_contract.md`.
- `direct_attempt.md`.
- `obligation_graph.md`.
- `closure_gate.md`.
- `route-01-spectral-coercivity/route_report.md`.
