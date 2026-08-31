# Closure gate

- Target ID: `KP-DET`.
- Target claim: `det Kp_odd(R)>0` for every finite `R>1` on the prescribed branch.
- First open load-bearing claim: `KP-SCHUR`, the strict sign `S_KP<0`.
- Existing support: audited 2026-08-30 reduction plus `direct_attempt.md`.
- Coordinator direct attempt: proves `gamma_2>b_0` and the global lower-right pivot sign.
- Cheapest falsification probe: exact phase-domain and dependency audit in `direct_attempt.md`.
- Gate decision: `ESCALATE`.
- Spawn trigger: a route must decide or strictly reduce `S_KP=0` using exact branch equations.
- Root obligations: `OPEN`.
- Completion manifest: none.
- Fresh package audit: pending.
- Load-bearing gaps: 1.
- Fast-close decision: `CONTINUE_REQUIRED`.
- Last updated: `2026-08-31T02:19:23Z`.

## Why escalation is earned

The direct attempt changes the frontier from a two-by-two kernel to one
everywhere-defined Schur scalar but does not decide its sign. Two
mechanism-distinct bounded tasks can now change the truth status without
reopening endpoint anchors or broadening the theorem.

## Bounded worker task 1

- Task ID: `W1-TRANSFER-SCHUR`.
- Exact claim: prove, refute, or strictly reduce `S_KP<0` using the exact three-layer transfer and band equations.
- Mechanism: eliminate amplitudes, logarithmic derivatives, and Green coefficients into branch phase variables; audit every phase domain and denominator sign.
- Success deliverable: a complete branch-uniform inequality or an exact branch-realizable equality witness.
- Partial deliverable: one strictly smaller exact trigonometric inequality with proved equivalence and all admissible domains.
- Budget stop: do not open KO-DET, SUP, n greater than 2, non-symmetric roots, or a broad literature search.

## Bounded worker task 2

- Task ID: `W2-JACOBI-FALSIFIER`.
- Exact claim: decide whether the same-sign parity-crossing Jacobi field represented by `S_KP=0` can exist.
- Mechanism: Sturm comparison, quotient variation, transfer transversality, or exact branch-realizable counterexample construction.
- Success deliverable: a contradiction proof or an exact witness satisfying all transfer, band, normalization, and mode-index conditions.
- Partial deliverable: a new necessary condition independent of worker 1 and a precise explanation of its remaining gap.
- Budget stop: no determinant monotonicity through the singular full Jacobian and no numerical-only verdict.

## Control restrictions

- The root owns run manifests, checkpoints, resume receipts, and reconciliation.
- Workers write only their assigned route directories.
- No completion claim may be made before a fresh independent audit of the frozen candidate package.
