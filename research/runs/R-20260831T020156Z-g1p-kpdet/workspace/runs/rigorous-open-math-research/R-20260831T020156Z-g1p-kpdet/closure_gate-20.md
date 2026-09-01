# Closure gate sequence 13

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

- Historical sequence-06 decision: `AUDIT_REQUIRED`.
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

## Sequence-13 W8/W9 audit boundary

- Verdict: `PASS`.
- Audit responses: 1.
- Critical errors: 0. Gaps: 0.
- Accepted: alpha-pi empty wedge, exact first-order endpoint scales, uniform
  mass residual gap, and common-epsilon near-one `G>0`, `Phi<0` assembly.
- Next wave: one global sign-coherence prover and one complete-system
  falsifier, then seal before audit.
- Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.

## Sequence-14 global sign-coherence boundary

- Research responses: 2.
- W10: `PARTIAL`, unreviewed.
- W11: `PARTIAL`, unreviewed.
- Worker restarts, duplicate dispatches, transcript replays: 0, 0, 0.
- Candidate W10 delta: exact `G` factorization, `B`-to-`H` identity, and
  complete-system chamber exclusion `B<0`.
- Candidate W11 delta: exact negative-`G` spectral-band family trapped in the
  positive coefficient orthant with strict positive mass residual.
- Next action: one fresh independent joint audit, then seal before repair or
  another solver response.
- Global `(SC)`, `G>=0`, `PHI-SIGN`, `Xi>0`, and KP-DET remain open.

## Sequence-15 W10/W11 joint audit boundary

- Verdict: `PASS`.
- Audit responses: 1.
- Critical errors: 0. Gaps: 0.
- Accepted W10 results: exact phase lock, `G` factorization and equality set,
  differential form, `B`-to-`H` identity, and complete-system `B<0`.
- Accepted W11 result: exact open negative-`G` family with strict positive
  coefficient chamber and strict positive mass residual, including W5.
- Next wave: exactly one common-`beta` orientation prover and one orientation
  falsifier, then seal before audit or a third solver.
- `(SC-rem)`, global `(SC)`, complete-system `G>=0`, `Xi>0`, `PHI-SIGN`, and
  KP-DET remain open.

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

## Sequence-16 common-beta orientation boundary

- Research responses: 2.
- W12: `PARTIAL`, unreviewed.
- W13: `EVIDENCE`, unreviewed only as an evidence artifact.
- Worker restarts, duplicate dispatches, transcript replays: 0, 0, 0.
- Candidate W12 delta: branch-safe common-`beta` identity, unique acute
  reconstruction, and strict KP-DET closure for `c alpha<=pi/2`, including
  all complete tuples with `0<c<=1/2`.
- W13 found no bounded numerical counterexample, but supplies no exhaustive
  proof or interval cover.
- Next action: one fresh independent joint audit, then seal before repair or
  another solver response.
- The remaining acute scalar threshold, arbitrary finite-`c` `PHI-SIGN`, and
  global KP-DET remain open.

## Sequence-17 W12/W13 joint audit boundary

- Verdict: `PASS`.
- Audit responses: 1.
- Critical errors: 0. Gaps: 0.
- Accepted: branch-safe unsquared common-`beta` identity, positive square-root
  lock, exact coefficient dictionary, unique acute reconstruction, and strict
  KP-DET chamber `c alpha<=pi/2`.
- Corollary: every complete tuple with `0<c<=1/2` satisfies KP-DET.
- W13 remains `EVIDENCE` only.
- Next wave: exactly one acute-threshold prover and one adversarial threshold
  or degenerate-collar falsifier, then seal before audit.
- Arbitrary finite-`c` `PHI-SIGN` and global KP-DET remain open.

## Sequence-18 acute-threshold boundary

- Research responses: 2.
- W14: `PARTIAL`, unreviewed.
- W15: `PARTIAL`, unreviewed; its bounded searches remain `EVIDENCE`.
- Worker restarts, duplicate dispatches, transcript replays: 0, 0, 0.
- Candidate W14 delta: fully constrained compatibility monotonicity, acute
  branch exclusion for `c<=2/3`, complete KP-DET on that range, and exact
  scalar mass collapse for `c>2/3`.
- Candidate W15 delta: uniform all-`m` collar classification with positive
  threshold margins and strict negative normalized mass residual.
- Next action: one fresh independent joint audit, then seal before repair or
  another solver response.
- Arbitrary finite-`c` `PHI-SIGN` and global KP-DET remain open for `c>2/3`.

## Sequence-19 audit no-return boundary

- Intended audit responses: 1.
- Valid audit responses: 0.
- Outcome: `NO_RETURN`, service usage rejection before mathematics.
- Audit verdict: none.
- Worker restarts, duplicate dispatches, transcript replays: 0, 0, 0.
- W14 and W15 remain immutable and `UNREVIEWED`.
- Next model action after quota recovery: one fresh independent joint audit
  bound to the same W14, W15, and reconciliation hashes.
- No solver or repair is authorized before that audit.
