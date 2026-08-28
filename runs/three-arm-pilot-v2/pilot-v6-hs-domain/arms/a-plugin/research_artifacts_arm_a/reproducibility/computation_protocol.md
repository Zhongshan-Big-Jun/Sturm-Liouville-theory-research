# Exact computation protocol

- **Mathematical object returned:** formal inverse powers
  \((c-D^2)^{-r}P_n\) for \(0\le n\le8,1\le r\le4\), and the exact resolvent
  solution for \(x^2\).
- **Property checked exactly:** polynomial inversion identities, both Krein
  boundary residuals, the low-degree iff pattern, and the hyperbolic boundary
  correction for \(K_c^{-1}x^2\).
- **Objective/score:** falsification only; there is no optimization score.
- **Penalty for invalidity:** any failed symbolic assertion exits nonzero.
- **Parameter domain:** symbolic \(c>0\) (written \(c=k^2,k>0\) for the
  hyperbolic check), finite degrees/ranks as above.
- **Arithmetic:** exact symbolic algebra; no floating point.
- **Limits:** replay under a 30-second wall clock; negligible memory expected.
- **Random seeds:** not applicable; deterministic.
- **Certificate:** printed exact boundary residuals and `ALL_EXACT_CHECKS_PASS`.
- **Proof bridge:** none is inferred from the finite range.  The uniform bridge
  is Lemmas 1, 3, and 4 of `candidate_proof.md`.
- **Known blind spots:** the degree bound is finite; the script does not build
  the odd form-orthogonal \(R_n\); symbolic simplification is not a proof of the
  analytic representation theorem.
