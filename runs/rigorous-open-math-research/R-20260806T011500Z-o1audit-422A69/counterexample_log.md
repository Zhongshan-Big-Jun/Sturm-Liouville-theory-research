# Counterexample log (audit run)

Purpose: adversarial tests of the O1 reduction theorem and its subclaims.
No counterexample to the theorem was found.  All entries below are either
edge cases confirmed, or failed attempts with exact failure mechanisms.

## C-001 (tested): draft Lemma 3 sign formula
Claim under attack: dD/deps = (c_+ - c_-) f(x_j) for a jump moved right.
Result: FALSIFIED (draft statement).  The one-sided right derivative is
-(c_+ - c_-) f(x_j).  Config [1,4,1] with jumps at 0.2, 0.65 (R=4):
right-difference 30.828430 vs corrected prediction 30.828320 vs draft
prediction -30.828320.  Not a counterexample to the theorem; a counterexample
to the draft lemma as written (sign).

## C-002 (tested): constant densities (boundary cases)
- rho = 1: D = 3 pi^2 = 29.6088132033 (matches to 1e-12).
- rho = R: D = 3 pi^2 / R = 7.4022033008 (matches to 1e-12).
Both lie in the closed barrier and well families (empty/full barrier).  No
violation.

## C-003 (tested): degenerate 2-parameter family members
- [1,4] on (0,0.5),(0.5,1) (a = 0): D = 15.4686922495.
- [4,1] (b = 1): D = 15.4686922495 (reflection symmetry of the problem).
- a = b (empty barrier, rho = 1): D = 3 pi^2.
All inside the closed families; none beats SUP 32.6139836 or INF 6.7844823.

## C-004 (tested): f zero-count and interval structure on hostile configs
- 5-block configs with alternating 1/4 values (4 jumps): nzeros_f = 2,
  single positive interval containing z_0, W < 0, v strictly decreasing in
  all 4 tested draws.  No structural violation of O1c found.

## C-005 (tested): off-center / asymmetric candidates (global search)
- 1200 random configs with 2-6 blocks, values in {1,4} or uniform in [1,4]:
  max D = 32.3416 (below SUP 32.6139836), min D = 6.8828 (above INF
  6.7844823).  No off-center maximizer or minimizer found (evidence; search is
  finite and not exhaustive).

## C-006 (failed route): draft proof of O1a via T_rho as written
Attack: does the draft's operator argument prove L^1 continuity?
Result: NO as written - T_rho with kernel G(x,t) rho(t) is not self-adjoint
on L^2(0,1), so Weyl's |mu_k(A) - mu_k(B)| <= ||A - B|| cannot be applied.
This is a gap in the draft, not a counterexample to the statement (statement
is true; repair via S_rho or weighted space, see obligation_graph O1a).

## C-007 (failed route): bang-bang test with a naive "perturbation"
First version of the O1f numeric test replaced the whole density instead of
perturbing locally, producing a meaningless dD > 0 on {f < 0}.  Corrected by
splitting the block containing the perturbed interval (verify_o1_audit3.py);
the corrected local test matches the FH prediction.  Recorded as an
audit-internal false alarm.

## C-008 (not found): no counterexample to the reduction theorem
No density in K with 2-6 blocks beats the barrier-family maximum or the
well-family minimum in the searched sample; combined with the structural
proof of O1 (modulo the two repairs), the theorem stands as REPAIRABLE_GAP.
