# Counterexample Log — R-20260816T120000Z-leftdef-density

## CE-1 (STRICT, used in Theorem L5)
- Setting: H = H^2[-1,1], c > 0, V = ker(Delta), Delta f = f(1)-f(-1).
- Claim refuted: "closure(span{p_n : p_n in V}) = V".
- Witness: q = p_5 - 2 p_7 = -2x^7 + 4x^5 - 2x^3.
  - q odd, q(1) = 0 => Delta q = 0 => q in V.
  - q nonzero, q in H^2 (combination of sparse polys).
  - Q_sp = {p_0} ∪ {p_{2n} : n>=2} (even sparse family; odd p_n not in V).
  - q ⊥ Q_sp (parity-orthogonality of the H^2 inner product, exact-verified).
  - Hence q in V ∩ Q_sp^perp, q != 0 => closure(span Q_sp) != V.
- Status: STRICT (proof in candidate_proof.md Theorem L5; exact-arithmetic
  corroboration in reproducibility/ld_counterexample.py).
- Mechanism: constraint excludes one parity (odd) from Q_sp; the excluded odd
  subspace is parity-orthogonal and contains nonempty constrained elements
  (q), which are never recaptured.

## CE-2 (EVIDENCE / structural)
- x^k notin H^2 for all k >= 2 (Krein BC check).  This is NOT a density
  counterexample; it is the structural fact S1 that DensBC O1 (H1) fails.
- Status: EVIDENCE (exact arithmetic) + documented in SL_h2 (Lemma 1).

## Tested edge cases (no counterexample found / consistent)
- V = H^s: density holds (L1).
- V = {0}: trivial.
- N empty (generic non-coordinate in abstract DensBC): density fails unless
  V = {0} (DensBC Lemma 6.1) - inherited, not re-derived.
- V = ker(Delta) is the only concrete constrained instance tested to non-density;
  no attempt was made to claim density for other V (O1'LD open).
