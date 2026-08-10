# Counterexample log - R-20260806T140000Z-o1revise-2ED02A

Purpose: adversarial tests of the O1 theorem and each subclaim.  No
counterexample to the theorem was found.  Entries: confirmed edge cases,
refuted sub-claims (draft), and failed verification attempts with exact
failure mechanisms.

## C-001 (REFUTED sub-claim): draft Lemma 3 sign formula
The draft's dD/deps = (c_+ - c_-) f(x_j) for a rightward jump is FALSE.
Correct (signed displacement): -(c_+ - c_-) f(x_j).  Numerics: config
[1,4,1], jumps 0.2/0.65, rightward delta = 1e-4: dD = +0.0030839 (predicted
-(R-1) f x delta = +0.0030828); the draft prediction would be -0.0030828.
V4 identity dD/du = -2(R-1)f(u) also refutes the draft sign.  Not a
counterexample to the theorem; the consequence f(x_j) = 0 stands.

## C-002 (tested): constant densities and degenerate family members
rho = 1: D = 3 pi^2 (29.6088132033, match 1e-12); rho = R: D = 3 pi^2 / R
(7.4022033008, match 1e-12); 2-block [1,R] at a=0: 15.4686922495; [R,1]
(b=1): same by reflection.  All inside the closed families; none beats the
barrier max or well min.

## C-003 (tested): precision artifact in draft-run u* record
Contract/ledger u* = 0.45148546584 / 0.451485465757 vs this run's
high-precision zero of f = 0.451485468013; D* matches to 4e-12 in both.
The u* digit difference (~2e-9) has no effect on any obligation.  Recorded
so downstream runs do not treat the ledger digits as exact.

## C-004 (failed verification attempt): spurious Weyl violation
First run of verify_hs_bound reported |1/lambda_1(rho) - 1/lambda_1(sigma)|
> ||S_rho - S_sigma||_HS in 2 of 16 cases.  Root cause: the step-evaluation
helper used np.interp (piecewise LINEAR), so the HS norm and the eigenvalues
were computed for different functions.  Fixed with a true step evaluator;
Weyl holds on all 16 cases.  Audit-internal false alarm (not a theorem
counterexample).

## C-005 (failed verification attempt): smoothed-family derivative stuck
First version of verify_smoothing_r4 smoothed only one of the two jumps of
[1,R,1]; the family converged to the 2-block [1,R] config, so the derivative
matched the wrong problem (2.55 vs 4.37, 22.6 vs 61.05).  Fixed with a
single-jump reference; convergence to the delta limit then confirmed
(rel error 0.8% -> 0.3% as delta -> 0).

## C-006 (failed verification attempt): on-grid zero counting
Symmetric configs have u_2(0.5) = 0 exactly on a grid point; the naive sign
change counter reported "u2 has 0 interior zeros".  Fixed by counting
on-grid zeros (|value| <= margin, opposite signs on both sides).  Not a
theorem counterexample.

## C-007 (failed verification attempt): refinement penalty sign
The barrier refinement for R=50 was attracted to the infeasible region
(a ~ 0.501 > b = 0.5, i.e., the empty barrier) because the infeasibility
penalty had the wrong sign for minimization of -D.  Fixed (+1e6 for both
kinds); R=50 bar_max corrected from 29.54 to 36.852185.  Audit-internal bug.

## C-008 (not found): counterexample to the reduction theorem
300 random configs (2-8 blocks, {1,R} and [1,R] values, R=4) stay below the
barrier max (32.6139836177) and above the well min (6.7844823391).  Combined
with the closed proof of O1, the theorem stands as CANDIDATE_COMPLETE_PROOF
modulo the independent re-audit.
