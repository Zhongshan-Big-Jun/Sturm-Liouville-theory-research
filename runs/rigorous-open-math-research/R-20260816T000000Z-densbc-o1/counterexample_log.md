# Counterexample / Edge-case Log

Run: R-20260816T000000Z-densbc-o1

## Tested edge cases / structures

### C-O1-001: generic non-coordinate representers (e^x and 1)
- H = L^2([-1,1]); V = {f : <e^x,f>=0, <1,f>=0}.  Kept set N computed via exact
  representer moments <e^x,p_n> and <1,p_n>: N = EMPTY.  Hence Q_sp = empty,
  closure(span Q_sp) = {0} != V (V 2-codimensional).  Density fails trivially.
  This shows generic non-coordinate constraints generically delete the whole kept
  sparse family (Proposition 6).  [EVIDENCE: o1_projection_density.py]

### C-O1-002: single polynomial non-coordinate representer (x - 1/2 x^2)
- H = L^2([-1,1]); V = {f : <x - 1/2 x^2, f> = 0}.  Representer is a polynomial
  (a^{(1)}_k has finite support) but NOT a monomial, so genuinely non-diagonal.
  Kept set N = EMPTY (<x - 1/2x^2, p_n> = 0 never for n tested to 60).  Runs are
  all isolated.  Again Q_sp empty => not dense.  [EVIDENCE: o1_poly_rep_example.py]

### C-O1-003: degenerate V = {0} and r = 0 (V = H)
- V = {0}: closure(span Q_sp) = {0} = V (trivial density).  Consistent with
  Theorem 1 / Theorem A.
- r = 0 (V = H): Q_sp = all p_n; the criterion reduces to the whole-space problem
  (regression to Theorem E with R empty: dense iff beta <= 3/2 in H_beta).
  Consistent.

### C-O1-004: diagonal coordinate reduction
- Coordinate L_j (v_j = coordinate element) reproduces the run graph of Theorem E
  and the corrected ratio M_k = (floor(k/2)/floor(L/2)) M_L (F-densbc-01).  The
  general criterion (Theorems 2-3) reduces to Theorem E (Theorem 4).  No
  contradiction with any audited counterexample (R={2,3}, R={4}).

## Failed/refuted route
- "Numerical finite-rank check closes O1": REFUTED by the honesty rule and by
  Theorem 5 — the realization step is a genuine (possibly infinite) moment
  problem; numerics only corroborate structure (EVIDENCE), never close an
  obligation.
