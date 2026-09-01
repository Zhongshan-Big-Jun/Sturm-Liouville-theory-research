# Closure gate sequence 12

- Gate decision: OPEN_EXACT_GAP
- Root obligations: OPEN
- Completion manifest: none
- Fresh package audit: PASS
- Load-bearing gaps: 1
- Fast-close decision: CONTINUE_REQUIRED
- Frontier upgrade: none
- Run result: RIGOROUS_PARTIAL_RESULT
- Blueprint integration: merged
- Exact gap: prove `Phi<0` on the complete five-phase system or construct an admissible exact tuple with `Phi=0`

## Sequence-06 boundary

- Gate decision: `AUDIT_REQUIRED`.
- Worker responses: 2.
- W4 status: `PARTIAL`, unreviewed.
- W5 status: `PARTIAL`, unreviewed.
- Worker restarts, duplicate dispatches, transcript replays: 0, 0, 0.
- New exact gap: audit the candidate mixed-sign mass balance and exact
  mass-defective witness. If accepted, attack only the sign-coherence bridge
  from `G<0` to a forbidden coefficient orthant.
- `PHI-SIGN`, `G>=0`, `Xi>0`, and `KP-DET` remain open.
- Stop rule: seal sequence 06 before any audit or third solver response.

## Sequence-07 audit boundary

- Verdict: `REPAIRABLE_GAP`.
- Audit responses: 1.
- Accepted strict partials: W4 equations `(1)-(7)`, the mixed-sign mass
  coefficient theorem, the W5 exact mass-defective witness, and its strict
  `G<0`, `Xi<0`, `Delta_M>0` certificates.
- Downgraded claim: W5 restricted near-one sign theorem.
- First error: uniform moving-switch phase, norm, and endpoint limits were
  used before a compactness and branch-continuity proof.
- Next action: one bounded repair response, then seal before re-audit.
- `G>=0`, `PHI-SIGN`, `Xi>0`, and `KP-DET` remain open.

## Sequence-08 repair boundary

- Repair status: `REPAIRED`, unreviewed.
- Repair responses: 1.
- Claimed repair: uniform near-one `G>0` for fixed
  `eta<=alpha<=pi-eta`, including moving switches.
- Preserved open face: `alpha->0`.
- Next action: one fresh re-audit response, then seal before any central
  solver response.
- Global `G>=0`, `PHI-SIGN`, `Xi>0`, and `KP-DET` remain open.

## Sequence-09 re-audit boundary

- Verdict: `PASS`.
- Re-audit responses: 1.
- Critical errors: 0. Gaps: 0.
- Accepted new strict theorem: for fixed `eta>0`, complete moving-switch
  tuples with `eta<=alpha<=pi-eta` have `G>0` uniformly for `m->1+`.
- Exact next escape face: simultaneous `m->1+`, `alpha->0`.
- Next wave may use exactly one asymptotic prover and one asymptotic
  falsifier, then must seal before audit or a third solver.
- Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.

## Sequence-12 alpha-pi boundary

- Research responses: 2.
- W8: `PROVED`, unreviewed.
- W9: `REFUTED` endpoint-family existence, unreviewed.
- Common candidate: exact uniform empty wedge near
  `(m,alpha)=(1,pi)`.
- Next action: one fresh joint audit, then seal before any global finite-R
  solver response.
- Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.

## Sequence-11 W7 audit boundary

- Verdict: `PASS`.
- Audit responses: 1.
- Critical errors: 0. Gaps: 0.
- Accepted theorem: a uniform empty wedge excludes complete tuples with
  `m->1+` and `alpha->0`.
- Corrected next near-one face: `alpha->pi`, possibly with
  `theta->pi/2`.
- Next wave may use exactly one endpoint prover and one endpoint falsifier,
  then must seal before audit.
- Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.

## Sequence-10 alpha-collision boundary

- Valid research responses: 1.
- W6: `NO_RETURN`, usage rejection, no artifact.
- W7: `PARTIAL`, unreviewed.
- Candidate delta: exact exclusion of every complete sequence with
  `m->1+`, `alpha->0`.
- Next action: one fresh independent audit of W7, then seal before any retry
  or new solver.
- Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.

## Accepted partial boundary

The direct pivot theorem, exact Schur reduction, exact phase reduction, and
Jacobi flux and locking statements passed a fresh independent mathematics
audit. They were integrated into the canonical Blueprint as a partial theorem.

## Open boundary

Complete `KP-DET` is not claimed. The next authorized research segment must
attack only `PHI-SIGN` through an exact global sign mechanism or an exact
admissible equality witness. The completed direct, W1, W2, audit, and Blueprint
waves must not be repeated.

## Sequence-04 direct and spawn gate

The coordinator derived the exact safe reduction `Phi<0 iff Xi>0` in
`route-03-phi-exact/coordinator_direct.md`. The cheapest falsification probe
shows that the spectral and band equations alone do not dominate the remaining
term; the exact mass identity is load-bearing. One worker may therefore attack
only the mass-propagated residual or an exact admissible equality tuple. Its
return must change the frontier by a strict proof, an exact witness, or a
strictly smaller independently auditable blocked reduction. The receipt budget
permits one research-model response in this segment.

## Sequence-04 worker boundary

W3 used the single authorized research-model response and returned a partial
exact package. It rewrites the mass equation as `(M-slope)`, proves `K<0`, and
derives `Xi=X^2G-rKDtheta`. The sufficient middle/right inequality `G>=0` and
the more general mass-slope to `Xi>0` bridge remain open. No global sign or
equality witness is claimed. Sequence 04 stops here and requires a fresh
independent audit before the W3 identities may enter the accepted package.

## Sequence-05 audit boundary

The fresh independent audit bound to the exact W3 and coordinator hashes
returned `PASS`, with zero critical errors and zero gaps in the strict partial
claims. It independently re-derived the Lagrange signs, scale factors,
mass-slope equivalence, `K<0`, and the `Xi` split. It explicitly leaves
`G>=0`, `Xi>0`, `PHI-SIGN`, and KP-DET open. The next gate is therefore an
earned two-role wave: one exact sign prover and one exact falsifier for the
`G>=0` subroute.
