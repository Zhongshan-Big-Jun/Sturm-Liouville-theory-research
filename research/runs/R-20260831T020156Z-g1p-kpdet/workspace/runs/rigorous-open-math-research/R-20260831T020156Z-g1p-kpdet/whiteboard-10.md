# Whiteboard sequence 10

- **Run ID:** `R-20260831T020156Z-g1p-kpdet`
- **Task packet ID:** `Q-20260831-g1p-kpdet`
- **Result status:** `RIGOROUS_PARTIAL_RESULT`
- **Mathematics audit:** `PASS`
- **Blueprint receipt:** `merged`
- **Lean status:** `SCAFFOLDED`, targeted parse exit code 0

## Current plan

The sequence-10 alpha-collision wave produced one quota-bound `NO_RETURN`
from W6 and one valid W7 `PARTIAL`. W7 gives an exact candidate exclusion of
every complete sequence with `m->1+`, `alpha->0`. Seal before one fresh audit;
do not retry W6 before the audit.

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
- `[SUCCEEDED]` W3 fresh audit: `PASS`, zero critical errors and zero gaps in
  the claimed partial identities. `PHI-SIGN` and KP-DET remain open.
- `[PARTIAL, UNREVIEWED]` W4: localized the exact mass equation to a candidate
  strict mixed-sign balance of three explicit layer coefficients and isolated
  the open sign-coherence implication `(SC)`.
- `[PARTIAL, UNREVIEWED]` W5: constructed a candidate exact mass-defective
  point with `G<0` and `Xi<0`, excluding mass-free shortcuts while preserving
  the complete `PHI-SIGN` question.
- `[SUCCEEDED]` Joint W4/W5 audit: accepted all W4 identities and the strict
  mixed-sign theorem; accepted the W5 exact mass-defective witness and sign
  certificate; returned one repairable gap in the W5 near-one uniformity
  argument.
- `[REPAIRED, UNREVIEWED]` W5 near-one repair: for fixed `eta>0`, claims
  uniform `G>0` as `m->1+` on complete tuples with
  `eta<=alpha<=pi-eta`.
- `[SUCCEEDED]` Near-one re-audit: `PASS`, zero errors and zero gaps. The
  moving-switch compactness gap is closed.
- `[NO_RETURN]` W6: service usage rejection before mathematics or artifact.
- `[PARTIAL, UNREVIEWED]` W7: candidate exact contradiction excluding the
  simultaneous near-one left-collision face.

## Ideas to return to

- Factor constrained `Phi` using the complete spectral and band equations.
- Propagate the exact endpoint ratio through the middle layer.
- Search for an exact admissible equality tuple with `Phi=0`.

## Open obligations

- `PHI-SIGN`, owner released: prove `Xi>0`, equivalently `Phi<0`, on the full
  exact constraint set, or construct an exact admissible tuple with
  `Xi=Phi=0`.
- `MASS-TO-SIGN`: use the audited mass-slope system to prove `G>=0`, prove a
  sharp lower bound sufficient for `Xi>0`, or exactly falsify the `G>=0`
  subroute while preserving the direct `Xi` target.
- `AUDIT-W4-W5`: independently audit the layer-coefficient identities, the
  mixed-sign theorem, the mass-defective exact witness, and the restricted
  near-one statement before reuse.
- `REPAIR-W5-NEARONE`: supply the explicit compactness, uniform spectral
  convergence, norm-limit, and endpoint-separation chain, or permanently
  downgrade the near-one statement to a conditional observation.
- `REAUDIT-W5-NEARONE`: independently verify the repaired uniform theorem,
  especially the phase definitions, norm limits, mass-limit endpoint
  equation, and uniform divergence estimate.
- `ALPHA-COLLISION`: decide the simultaneous near-one scaling
  `m->1+`, `alpha->0`, or derive the exact blow-up variables needed to decide
  it without reopening the fixed-eta region.
- `AUDIT-ALPHA-COLLISION`: independently check W7 before combining it with
  the fixed-eta theorem.
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
- `route-03-phi-exact/audit/independent_audit.json`.
- `route-03-phi-exact/audit/independent_audit.md`.
- `route-04-mass-g-wave/prover_result.md`.
- `route-04-mass-g-wave/falsifier_result.md`.
- `route-04-mass-g-wave/reconciliation.md`.
- `route-04-mass-g-wave/audit/independent_audit.json`.
- `route-04-mass-g-wave/audit/independent_audit.md`.
- `route-04-mass-g-wave/repair/near_one_repair.md`.
- `route-04-mass-g-wave/repair/reaudit.json`.
- `route-04-mass-g-wave/repair/reaudit.md`.
- `route-04-mass-g-wave/accepted_package.md`.
- `route-05-alpha-collision/falsifier_result.md`.
- `route-05-alpha-collision/reconciliation.md`.
