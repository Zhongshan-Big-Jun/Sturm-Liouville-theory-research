# Reuse Summary — O1'LD run

Run: R-20260823T030000Z-leftdef-o1pld

## Actual reused items
- Prior left-definite run problem_contract/candidate/final (L1-L6, L3 transfer).
- DensBC O1 run/recursion algebra was initially reused, but the independent
  audit showed it is NOT valid for the L^2/H^1 q_n moment recurrences.  It has
  been removed from the L^2/H^1 descent in this repair.
- DensBC O1p/O1p2 as comparison subclasses; their finite-rank criteria were NOT
  reused as valid in the L^2 descent.
- SL_h2/H3 proofs for q_n coefficients, the SL_h2 growth lemma (including the
  odd branch), and H^1 moment bound.
- Tools: constrained-denseness-runs, left-definite-moment-recurrence,
  denseness-criteria, banded/weighted shift density tools.
- Müntz-Szász theorem (standard, Lebesgue L^p form; now used with explicit
  even/odd weighted substitutions).

## Duplicate work avoided / remaining
- Avoided re-deriving the full Sparsity/BC calculus (S1a-S1d, L1-L6).
- Avoided re-running the whole web novelty sweep (inherited from prior run).
- Remaining: tail L^2 rigidity (Claim 4), cofinite-N density theorem
  (NOT-YET-STRICT conditional on Claim 4), H^1 finite-run realizability, and
  general O1'LD are not closed.

## New methods
- L^2 finite-support moment rigidity using Müntz-Szász (Lebesgue L^p form) with
  explicit weighted even/odd substitutions.
- Parity decomposition of the L^2 descent.
- Concrete μ_4 moment-constraint non-density example with SL_h2 odd growth
  lemma.

## One-line cost assessment
Cheap run (a few sympy/numpy probes, no background jobs) that produced several
STRICT structural theorems plus an exact non-density example; the cofinite-N
theorem and the required tail rigidity remain not-yet-strict; general O1'LD
still open.
