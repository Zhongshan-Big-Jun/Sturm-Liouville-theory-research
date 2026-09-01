# Whiteboard sequence 18

- **Run ID:** `R-20260831T020156Z-g1p-kpdet`
- **Task packet ID:** `Q-20260831-g1p-kpdet`
- **Result status:** `RIGOROUS_PARTIAL_RESULT`
- **Mathematics audit:** `PASS`
- **Blueprint receipt:** `merged`
- **Lean status:** `SCAFFOLDED`, targeted parse exit code 0

## Current plan

The bounded W14/W15 acute-threshold wave returned two compatible candidate
strict partials. W14 proposes complete `PHI-SIGN` and KP-DET for
`0<c<=2/3`, plus an exact scalar mass collapse for `c>2/3`. W15 proposes a
uniform boundary-collar classification with a strict negative mass residual.
Seal before one fresh joint audit; no repair or third solver is authorized
first.

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
- `[SUCCEEDED]` W7 audit: `PASS`, zero errors and zero gaps. The uniform
  alpha-zero empty wedge is accepted strict mathematics.
- `[PROVED, UNREVIEWED]` W8: candidate uniform alpha-pi empty wedge from
  `Delta_M->-pi/6`.
- `[REFUTED, UNREVIEWED]` W9: independently excludes every complete
  alpha-pi endpoint family by the same mass contradiction.
- `[SUCCEEDED]` W8/W9 audit: `PASS`, zero errors and zero gaps. The common
  alpha-pi wedge and single-epsilon near-one assembly are accepted.
- `[PARTIAL, UNREVIEWED]` W10: candidate exact phase lock, factorization
  `G=X(M Dtheta/P)(q-E)`, `B`-to-`H` identity, and complete-system exclusion
  `B<0`; the common-`beta` orientation remainder is open.
- `[PARTIAL, UNREVIEWED]` W11: candidate exact negative-`G` one-parameter W5
  family in the strict positive coefficient orthant with positive mass
  residual; no complete counterexample was found.
- `[SUCCEEDED]` W10/W11 joint audit: `PASS`, zero errors and zero gaps. P8-P11
  are accepted strict partial mathematics; all global closure claims remain
  open.
- `[PARTIAL, UNREVIEWED]` W12: candidate branch-safe common-`beta` identity,
  coefficient dictionary, unique acute reconstruction, and KP-DET closure
  for `c alpha<=pi/2`.
- `[EVIDENCE]` W13: bounded common-`beta` scan found no mixed-chamber or
  numerically mass-balanced `q>E` tuple; no universal conclusion is claimed.
- `[SUCCEEDED]` W12/W13 joint audit: `PASS`, zero errors and zero gaps. P12-P15
  are accepted strict partial mathematics; W13 remains evidence-only.
- `[PARTIAL, UNREVIEWED]` W14: candidate constrained monotonicity, exclusion
  of the acute branch for `c<=2/3`, and exact scalar mass collapse.
- `[PARTIAL, UNREVIEWED]` W15: candidate uniform all-`m` collar theorem with
  positive threshold margins and negative normalized mass residual.

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
- `ALPHA-PI-ENDPOINT`: decide whether complete tuples can satisfy
  `m->1+`, `alpha->pi`, and classify any forced coupling to
  `theta->pi/2` before claiming mechanism-level near-one coverage.
- `AUDIT-ALPHA-PI`: jointly audit W8 and W9 before combining both endpoint
  wedges with fixed-strip positivity.
- `GLOBAL-SIGN-COHERENCE`: for arbitrary finite `m`, prove or refute the
  implication from `G<0` to a forbidden same-sign orthant of `(A,B,H)` on
  the spectral-band system.
- `AUDIT-W10-W11`: independently rederive the W10 factorization and chamber
  exclusion, and verify the W11 exact family and strict mass-residual sign.
- `COMMON-BETA-ORIENTATION`: use the unsquared reconstruction of the same
  `beta` and `c beta` to prove or refute the remaining implication from
  `q>E`, `B<0` to the forbidden chamber, or directly prove `q<=E` on mass.
- `AUDIT-W12-W13`: independently verify the full W12 branch and sign chain,
  including `c<=1/2`, and enforce W13's evidence boundary.
- `ACUTE-THRESHOLD`: prove or refute the unique-root inequality comparing
  `q-E` with `D-k e max(sin(A)^2,sin(d)^2)` in the remaining acute chamber.
- `AUDIT-W14-W15`: independently verify W14's full constrained derivative and
  W15's compactified uniform asymptotics before strict reuse.
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
- `route-05-alpha-collision/audit/independent_audit.json`.
- `route-05-alpha-collision/audit/independent_audit.md`.
- `route-05-alpha-collision/accepted_package.md`.
- `route-06-alpha-pi/prover_result.md`.
- `route-06-alpha-pi/falsifier_result.md`.
- `route-06-alpha-pi/reconciliation.md`.
- `route-06-alpha-pi/audit/independent_audit.json`.
- `route-06-alpha-pi/audit/independent_audit.md`.
- `route-06-alpha-pi/accepted_package.md`.
- `route-07-global-sign-coherence/prover_result.md`.
- `route-07-global-sign-coherence/falsifier_result.md`.
- `route-07-global-sign-coherence/reconciliation.md`.
- `route-07-global-sign-coherence/audit/independent_audit.json`.
- `route-07-global-sign-coherence/audit/independent_audit.md`.
- `route-07-global-sign-coherence/accepted_package.md`.
- `route-08-common-beta-orientation/prover_result.md`.
- `route-08-common-beta-orientation/falsifier_result.md`.
- `route-08-common-beta-orientation/reconciliation.md`.
- `route-08-common-beta-orientation/audit/independent_audit.json`.
- `route-08-common-beta-orientation/audit/independent_audit.md`.
- `route-08-common-beta-orientation/accepted_package.md`.
- `route-09-acute-threshold/prover_result.md`.
- `route-09-acute-threshold/falsifier_result.md`.
- `route-09-acute-threshold/reconciliation.md`.
