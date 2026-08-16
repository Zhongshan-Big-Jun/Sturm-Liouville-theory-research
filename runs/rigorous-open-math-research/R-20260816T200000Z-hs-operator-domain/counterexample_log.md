# Counterexample log — R-20260816T200000Z-hs-operator-domain

## CE-1: Refutation of the upstream auxiliary claim S1d "H^s ∩ C[x] = span{1,x} for s >= 4"
- Claim attacked: left-def run S1d asserted every polynomial of degree >= 2 fails the
  iterated Krein condition at the K_c level, hence H^4 ∩ C[x] = span{1,x}.
- Counterexample (exact, c = 3): f(x) = x^2(x^4 - 5x^2 + 7) = x^6 - 5x^4 + 7x^2.
  - f even, f'(x) = 6x^5 - 20x^3 + 14x, f'(1) = 0  => f in D(K_c).
  - K_c f = 3f - f'' = 3x^6 - 45x^4 + 81x^2 - 14; (K_c f)'(x) = 18x^5 - 180x^3 + 162x,
    (K_c f)'(1) = 0 => K_c f in D(K_c).
  - Hence f in D(K_c^2) = H^4, deg f = 6 >= 4, f notin span{1,x}.
  - General c: the rational-coefficient example exists for all c > 0 (structure is
    c-independent; see reproducibility scripts).
- Consequence: S1d over-reached. The degree spectrum of D(K_c^2) ∩ Pi is
  {0,1} U {d >= 6}, not {0,1}.
- IMPORTANT: This does NOT affect the left-def run's L1'' (sparse family): p_n (n >= 4)
  is genuinely not in H^4 (K_c p_4 fails the Krein condition, exact), so for the sparse
  family Q_sp = {1,x} and density fails. S1d and L1'' are independent.

## CE-2: The Q_n^{(s)} are NOT in H_op^s for n >= 2 (the task's central negative)
- Tried to place Q_n^{(s)} = K_c^{-r}P_n (even) / K_c^{-r}K_n (odd) in D(K_c^{s/2}).
- Falsification (exact, n=4, s=4): Q_4^{(4)} = K_c^{-2}P_4 requires K_c^{-1}P_4 in D(K_c);
  but D_4 = f_4'(1) = 5(2c+21)/c^2 > 0, so K_c^{-1}P_4 notin D(K_c). Hence Q_4^{(4)}
  notin D(K_c^2).
- The SL_hs doc's completeness claim for s >= 4 therefore holds in H_abs^s (abstract
  completion), not in H_op^s = D(K_c^{s/2}).

## Search code
- reproducibility/boundary_facts.py, domain_poly_span.py, degree_structure.py,
  genericity_check.py, krein_sobolev_membership.py, odd_proof_data.py,
  monotonicity_data.py, krein_sobolev_deficit_fixed.py (all exact sympy).
