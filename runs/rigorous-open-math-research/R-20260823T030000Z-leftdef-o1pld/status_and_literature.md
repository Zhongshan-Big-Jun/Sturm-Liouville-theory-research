# Status and Literature — O1'LD run

Run: R-20260823T030000Z-leftdef-o1pld
Repair status: RIGOROUS_PARTIAL_RESULT (after independent audit)

## Current status after this run

O1'LD remains open in general.  New STRICT results for the L^2 descent (s = 2):

1. Finite-support L^2 moment sequences are trivial: finite deletion of
   monomials is total in L^2 via the Lebesgue L^p Müntz-Szász theorem, with
   explicit even/odd weighted substitutions.
2. The Cauchy-Schwarz L^2 moment bound is STRICT; a linearly growing moment
   sequence is not L^2-realizable.
3. The parity decomposition of the L^2 descent:
   closure(span Q_sp) = closure(even kept) ⊕ closure(odd kept).
4. Concrete non-density: W = ker μ_4 in L^2 (i.e. V = ker L with
   L(f)=∫K_c f x^4) has Q_sp = {q_1} ∪ odd sparse family, closure is the odd
   subspace, and density fails.

NOT-YET-STRICT (after audit repair):
- Tail L^2 rigidity (Claim 4): any nonzero L^2-realizable solution of a tail
  q_n recurrence should be zero.  The dominant factorial-growth case is proved
  by the SL_h2 growth lemma, but the minimal (polynomially decaying) solution
  case has not been fully excluded in this repair.
- Cofinite-N density theorem for s = 2 and the proper-V non-cofinite corollary:
  conditional on Claim 4; no longer registered STRICT.

For s = 3 (H^1 descent): the polynomial moment bound |M_k| ≤ C√k is STRICT
(prior result); the infinite-run inadmissibility claim is downgraded to
EVIDENCE/PLAUSIBLE; finite-run realizability is open (EVIDENCE only).

## Known results used
- Prior left-definite run R-20260816T120000Z (L1-L6, transfer descent).
- DensBC O1 Theorems 1-5 (run/recursion algebra) — NOT used in the L^2/H^1
  descent after audit repair.
- DensBC O1p/O1p2/baseline/light-reuse finite-rank criteria for banded and
  weighted shifted spaces.
- SL_h2 completeness proof (including the odd growth lemma), H^1 moment bound.
- Müntz-Szász theorem (classical, Lebesgue L^p form) for finite deletion of
  monomials.

## Novelty
- The finite-support L^2 moment rigidity and the μ_4 non-density example are
  POTENTIALLY_NEW.  The cofinite-N theorem is likely true but NOT-YET-STRICT.
  General O1'LD remains open; no literature search was rerun in this subagent
  (the prior run's sweep is inherited).

## Open remaining
- Tail L^2 rigidity (Claim 4); subsequent cofinite-N density.
- General O1'LD for arbitrary closed W ⊆ L^2 (s = 2).
- H^1 infinite-run inadmissibility (EVIDENCE/plausible) and finite-run
  realizability (s = 3).
- General other s/constraint classes.
