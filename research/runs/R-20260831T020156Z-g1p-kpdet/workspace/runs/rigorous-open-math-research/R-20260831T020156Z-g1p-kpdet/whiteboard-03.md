# Whiteboard sequence 03

- **Run ID:** `R-20260831T020156Z-g1p-kpdet`
- **Task packet ID:** `Q-20260831-g1p-kpdet`
- **Result status:** `RIGOROUS_PARTIAL_RESULT`
- **Mathematics audit:** `PASS`
- **Blueprint receipt:** `merged`
- **Lean status:** `SCAFFOLDED`, targeted parse exit code 0

## Current plan

Preserve the audited P1-P4 package and leave `PHI-SIGN` as the sole exact
load-bearing obligation. No additional solve wave is authorized in this run.

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

## Ideas to return to

- Factor constrained `Phi` using the complete spectral and band equations.
- Propagate the exact endpoint ratio through the middle layer.
- Search for an exact admissible equality tuple with `Phi=0`.

## Open obligations

- `PHI-SIGN`: prove `Phi<0` on the full five-phase spectral, band, mass, and
  mode-index constraint set, or construct an exact admissible tuple with
  `Phi=0`.
- Complete `KP-DET`, `KO-DET`, simultaneous sector singularity, non-symmetric
  roots, and global `G1'` remain open.

## Key artifacts

- `candidate_proof.md`.
- `audit/independent_audit.json`.
- `route-01-transfer-schur/derivation.md`.
- `route-02-jacobi-falsifier/derivation.md`.
- `blueprint_integration_record.md`.
- `interruption_checkpoint-02.json` and `resume_receipt-02.json`.
