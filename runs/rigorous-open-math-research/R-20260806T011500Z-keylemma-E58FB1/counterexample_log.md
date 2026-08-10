# Counterexample log

Run: R-20260806T011500Z-keylemma-E58FB1
Every item here is a concrete falsification of a candidate lemma, with witness values.
None of these items falsifies the KEY LEMMA itself; all recorded target inequalities
(G2 - G1 > 0, F~' < 0) remain numerically true on the whole domain.

## C1 (inherited, re-confirmed): the two "equivalent forms" are not logically equivalent
- Claim attacked: (d/dc) log(M1/M2) < 0  <=>  F'(c) < 0.
- Why false: F' = M1 G1 - M2 G2 = M1 M2 (G1/M2 - G2/M1), not proportional to G1 - G2.
- Witness: at (q=1.1, c=0.05): F' = -2.67639, G1 - G2 = -38.8661.  The ratio
  (M1 G1 - M2 G2)/(G1 - G2) varies over the domain (it is not constant), so the sign
  equivalence has no basis.  Both inequalities are separately true and are proven by the
  same reduction (each needs its own proof).

## C2 (inherited): itemwise q-monotonicity of B-D is FALSE
- Decomposition from tools/key-lemma-decomposition.md: G2 - G1 = (A - C) + (B - D).
- Claim attacked: B - D monotone in q.
- Witness: c = 0.01; q: 5000 -> 20000 gives B - D: 199.79 -> 193.99 (decreasing).
- Consequence: any route relying on itemwise q-monotonicity of the decomposition is
  discarded.

## C3 (inherited): F~' is not monotone in q
- Claim attacked: -F~'(q, c) increasing in q (i.e., F~' decreasing in q).
- Witness: at small c, -F~' is smaller for larger q; F~' is non-monotone in q.
- Consequence: the F~' form cannot be closed by a q-monotonicity argument alone.

## C4 (inherited): G2 is not monotone in c globally
- Claim attacked: G2(c; q) decreasing in c for all q.
- Witness: q = 100: G2 has an interior minimum at c ~ 0.2546 (value ~12.368), then
  increases to G2(0.5) ~ 18.34.  So G2(0.25) < G2(0.35) even though c increased.
- Consequence: R1 cannot be proven by "G2 decreasing in c" for large q; the boundary
  reduction must use dG2/dq >= 0 instead (Route C), or the direct B >= 0 argument.

## C5 (new): extended-box q-monotonicity of B is FALSE
- Claim attacked: B(gamma; q) := A(q + c Phi) - 2T(q^2-1) sin gamma cos gamma increasing
  in q on gamma in (0, alpha0(2)] for q >= 2.
- Witness: q = 100, gamma = 0.8369: B = -11091.3 (vs B(gamma; 2) ~ +0.29).
- Why it fails: for q = 100 the admissible gamma satisfies gamma <= alpha0(100) ~ 0.14;
  the extended box reaches gamma ~ 0.84 which is spurious for large q.
- Consequence: monotonicity comparisons must respect the per-q domain gamma <= alpha0(q).

## C6 (new): corner-envelope bound is FALSE
- Claim attacked: B(gamma; q) >= B(gamma; q(gamma)) where q(gamma) solves alpha0(q) = gamma.
- Witness: q = 1000, gamma = 0.00045: B(gamma;q) - B(gamma;q(gamma)) ~ -1.4e11.
- Consequence: the c = 1/2 corner curve is not a lower envelope for B in (gamma, q).

## C7 (new): naive tail bound for R1 is FALSE
- Claim attacked: A(alpha0(q)) * q >= pi (q^2 - 1) alpha0(q) (the "L(q) >= 0" bound).
- Witness: L(q) < 0 for every q >= 2 (e.g., L(100) = -490.9, L(1e6) = -4.999e6).
- Why it fails: the bound drops the c Phi term (q + c Phi ~ q^2 at the corner, not q)
  and overestimates T by pi/2 simultaneously; the slack at (2, 1/2) is only ~8%.
- Consequence: a proof of R1 must reproduce the exact c = 1/2 balance.

## C8 (new): G2(1/2; q) does not decay to 0 for large q (correction of an earlier guess)
- Claim attacked (earlier hypothesis): G2(1/2; q) -> 0+ as q -> inf.
- Correct behavior: G2(1/2; q) ~ (pi / sqrt 2) sqrt q -> +inf.
- Witness: G2(1/2; 100) ~ 18.29, G2(1/2; 10000) ~ 218.15.
- Consequence: R1's difficult region is a bounded q-interval (q in [2, ~10]); large-q
  evidence is strongly positive (G2 grows).

## No counterexamples found
- To the KEY LEMMA itself: G2 - G1 > 0 and F~' < 0 held on every sampled point
  (q in [1.001, 1e6], c in [1e-8, 0.5)) and on all boundary families (q = 1 limit,
  c = 0 limit, c = 1/2, q -> inf).
- To L4box / L5box: H' < 0 and F~'' > 0 on every sampled point of (1,2] x [0.4, 0.5].
- To R1/R2: G2 >= 0 on every sampled point of {q >= 2} and of {c <= 0.4}.
- To Q1 (dG2/dq >= 0): every sampled point, including extreme regimes.
- This is evidence, not a proof (see status_and_literature.md).

## Note on vanishing margins at large q (not a counterexample)
At q = 10000, c = 0.230: F~'(q,c) = -1.7929495737e-10, so -F~' is tiny there (M~ ~ 1/q^3).
The inequality F~' < 0 still holds; the proof handles q >= 2 via region A (R1 + L1 + L2),
which needs no margin.  This explains why "global margins" must be quoted with their q-range.
