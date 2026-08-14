# Counterexample Log

Run: R-20260814T070000Z-densbc-3F8A2C

## C-001 (R-001): Packet example falsified
Claim tested: "V = span{x^2,x^3}^\perp in H_beta, sparse family dense for every beta."
Verdict: FALSE for beta > 3/2.
Counterexample: H_beta diagonal, R = {2,3}.  p_4 = x^4 - (4/3)x^2 has degree 2 in R,
so p_4 NOT in V, and M_4 is NOT locked by the recursion to M_2 (which is pinned=0).
Free parameters: M_4 (even), M_5 (odd).  Define w with
   M_2 = M_3 = 0, M_4 = 1, M_{2m} = (m/2) for m>=2, M_5 = 1, M_{2m+1} = (m/2) for m>=3,
   w_k = M_k (k+1)^{-2 beta}.  Then w in V, ||w||_beta^2 = Sum_m (m/2)^2
   (2m+1)^{-2 beta} x2 which converges iff beta > 3/2, and w orthogonal to every kept p_n.
So the kept sparse family is NOT dense for beta > 3/2.
Evidence: scripts/densbc_v1_verify_free_params.py (bad_ip=0, finite norm for beta>3/2),
scripts/densbc_v3_diagonal_universal.py (R={2,3} confirmed for beta in {1.6,2.0,3.0}).

## C-002 (R-005b): finite-run phenomenon at beta <= 3/2
Claim tested: "constraints restore density at beta <= 3/2."
Verdict: FALSE in general -- a finite run destroys density even at beta <= 3/2.
Counterexample: R = {4}.  Degree 2 is unconstrained and isolated (its upper neighbor
4 is constrained, so p_4 not kept).  M_2 is a FREE finite-run (singleton) parameter.
w = M_2 x^2-normalized with w_2 = 1 * 3^{-2 beta} (finite support).  w in H_beta (any
beta), w in V, orthogonal to every kept p_n (kept p_n involve degrees >= 6).  Not dense.
Similarly R = {2,6}: run [4,4], M_4 free, finite support.  R = {4,8}: run [2,2].
Evidence: scripts/densbc_v4_finite_run_phenomenon.py, densbc_v5_classification_verdict.py.

## C-003: Monomial family always dense in diagonal coordinate space
Claim: the SPARSE family fails, not polynomials.  {x^k : k not in R} is an orthogonal
basis of V in H_beta -> ALWAYS dense.  (Positive, not a counterexample; recorded to
avoid over-reading C-001/002.)

## Search code
- scripts/densbc_v1_verify_free_params.py  (packet example)
- scripts/densbc_v2_diagonal_classify.py   (initial classify)
- scripts/densbc_v3_diagonal_universal.py  (beta>3/2 universal non-density, 12 R)
- scripts/densbc_v4_finite_run_phenomenon.py (finite run)
- scripts/densbc_v5_classification_verdict.py (corrected classification, 11 R)
