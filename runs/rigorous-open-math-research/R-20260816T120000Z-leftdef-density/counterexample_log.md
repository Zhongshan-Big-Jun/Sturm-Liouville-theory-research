# Counterexample Log — R-20260816T120000Z-leftdef-density

## CE-1 (STRICT, used in Theorem L5)
- Setting: H = H^2[-1,1], c > 0, V = ker(Delta), Delta f = f(1)-f(-1).
- Claim refuted: "closure(span{p_n : p_n in V}) = V".
- Witness: q = p_5 - 2 p_7 = -2x^7 + 4x^5 - 2x^3.
  - q odd, q(1) = 0 => Delta q = 0 => q in V; q nonzero, q in H^2.
  - Q_sp = {p_0} ∪ {p_{2n} : n>=2} (even sparse family; odd p_n not in V).
  - q ⊥ Q_sp (parity-orthogonality, exact).
  - Hence q in V ∩ Q_sp^perp, q != 0 => closure(span Q_sp) != V.
- Status: STRICT (airtight per independent audit).  Mechanism: constraint
  excludes one parity from Q_sp; excluded odd subspace orthogonally silent,
  contains nonzero constrained elements never recaptured.

## CE-2 (EVIDENCE / structural: x^k absent in H^2)
- x^k notin H^2 for all k >= 2 (Krein BC).  Structural fact S1a/14a.
- Status: EVIDENCE (exact) + documented SL_h2 Lemma 1.

## CE-3 (DECISIVE structural finding; STRICT via exact check, used in L1'')
- Claim refuted: "the sparse polynomials p_n (n >= 4) lie in H^s for all integer
  s >= 1 [so span{p_n} recovers H^s for all s]".
- Witness: p_4 and H^4 = D(K_c^2).
  - K_c p_4 = c x^4 - (2c+12)x^2 + 4.
  - (K_c p_4)'(+1) = -24, (K_c p_4)'(-1) = +24, but
    (K_c p_4)(1) - (K_c p_4)(-1) = 0.  The Krein BC requires derivative at +1/-1
    equal to half the endpoint difference (=0); it fails (values -24, +24).
  - Hence K_c p_4 notin H^2, so p_4 notin H^4 = D(K_c^2).  (exact)
  - Same for p_5..p_8 (exact check); p_0=1, p_1=x are in every H^s.
- Consequence: for s >= 4 (operator-domain H^s = D(K_c^{s/2})),
  H^s ∩ C[x] = span{1,x}; the sparse family is NOT a subset of H^s; whole-space
  Q_sp = {1,x} and closure(span Q_sp) = span{1,x} != H^s (density fails, L1'').
- Status: exact-arithmetic + STRICT deduction (L1'' proof).  This corrects the
  packet's Q3 premise for s >= 4.

## Tested edge cases (no counterexample found / consistent)
- s in {1,2,3}, V = H^s: density holds (L1').  V = {0}: trivial.
- N empty: density fails unless V = {0} (DensBC Lemma 6.1) - inherited.
- V = ker(Delta) at s=2: non-density (CE-1).
- s >= 4 whole-space: non-density for the sparse family (CE-3); the SL_hs
  orthogonal system {Q_n^{(s)}} is a DIFFERENT complete family whose membership
  in D(K_c^{s/2}) for s >= 4 is flagged open.
