# Whiteboard sequence 04

- **Run ID:** `R-20260831T020156Z-g1p-kpdet`
- **Task packet ID:** `Q-20260831-g1p-kpdet`
- **Result status:** `RIGOROUS_PARTIAL_RESULT`
- **Mathematics audit:** `PASS`
- **Blueprint receipt:** `merged`
- **Lean status:** `SCAFFOLDED`, targeted parse exit code 0

## Current plan

The authorized sequence-04 action is complete. Preserve the coordinator safe
elimination and W3 mass-slope package. Seal sequence 04 before any further
research-model call. The next segment begins with one fresh independent audit
of W3, not a solver retry.

## Route history

- `[SUCCEEDED]` Direct route: proved `gamma_2>b_0>0` and the global negative
  lower-right pivot.
- `[PARTIAL]` Transfer route W1: proved
  `KP-DET iff S_KP<0 iff Phi<0` on the exact admissible phase system.
- `[PARTIAL]` Jacobi route W2: proved common projective flux, the unique simple
  downward locking point, and the exact endpoint ratio.
- `[FAILED]` Quotient-only closure: monotonicity alone does not exclude the
  same-sign kernel.
- `[SUCCEEDED]` Independent audit and Blueprint integration: P1-P4 passed and
  the accepted partial theorem entered the canonical graph.
- `[PARTIAL]` Sequence-04 coordinator direct route: proved the lossless safe
  reduction `Phi<0 iff Xi>0`, without tangent-chart exclusions. The exact mass
  identity remains necessary.
- `[PARTIAL]` Route W3: converted the exact mass equation to `(M-slope)`,
  proved `K<0`, and split `Xi=X^2G-rKDtheta`. The sign bridge from mass slope
  to `G` or directly to `Xi` remains open.

## Ideas to return to

- Factor constrained `Phi` using the complete spectral and band equations.
- Propagate the exact endpoint ratio through the middle layer.
- Search for an exact admissible equality tuple with `Phi=0`.

## Open obligations

- `PHI-SIGN`, owner released: prove `Xi>0`, equivalently `Phi<0`, on the full
  exact constraint set, or construct an exact admissible tuple with
  `Xi=Phi=0`.
- `W3-AUDIT`: independently audit the two mass-slope formulas, denominator
  and normalization factors, `K<0`, and the `Xi` split before downstream use.
- Complete `KP-DET`, `KO-DET`, simultaneous sector singularity, non-symmetric
  roots, and global `G1'` remain open.

## Key artifacts

- `candidate_proof.md`.
- `audit/independent_audit.json`.
- `route-01-transfer-schur/derivation.md`.
- `route-02-jacobi-falsifier/derivation.md`.
- `blueprint_integration_record.md`.
- `interruption_checkpoint-02.json` and `resume_receipt-02.json`.
- `route-03-phi-exact/coordinator_direct.md`.
- `route-03-phi-exact/worker_result.md`.
- `route-03-phi-exact/worker/README.md`, labeled `EVIDENCE`.
