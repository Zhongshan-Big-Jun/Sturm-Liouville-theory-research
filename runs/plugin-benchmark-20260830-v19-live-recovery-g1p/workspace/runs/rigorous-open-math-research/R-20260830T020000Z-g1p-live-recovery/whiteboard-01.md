# Whiteboard sequence 01

- **Run ID:** `R-20260830T020000Z-g1p-live-recovery`
- **Task packet ID:** `Q-20260830-g1p-live-recovery`

## Current plan

Workers W1 and W2 are ingested as `PARTIAL`. Seal checkpoint sequence 01, then
run a fresh independent audit of the merged candidate partial package.

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
- `W2-KP-FIRSTZERO-JACOBI` `[PARTIAL]`: reconciled as `INGESTED` after
  checkpoint sequence 00. Exact Jacobi and transfer realization, strict
  off-diagonal positivity, and a nonsingular-Ko branch chart were obtained.
  Evidence: `route-02-firstzero-jacobi/route_report.md` and
  `reconciliation-w2.md`.

## Ideas to return to

- Combine the W1 scalar equality with the W2 Jacobi crossing form.
- Treat simultaneous odd/even sector singularity without inverting either
  singular matrix.
- Attack `KO-DET` only after the odd-sector frontier is terminal.

## Open obligations

1. Exclude the one-dimensional same-sign Jacobi kernel, equivalently the W1
   positive-cone branch equality.
2. Treat possible simultaneous singularity of `Kp_odd` and `Ko`.
3. Prove or refute `KO-DET`.

## Key artifacts

- `problem_contract.md`.
- `candidate_proof.md`.
- `route-01-spectral-coercivity/route_report.md`.
- `route-02-firstzero-jacobi/route_report.md`.
- `reconciliation-w2.md`.
- `closure_gate-01.md`.
