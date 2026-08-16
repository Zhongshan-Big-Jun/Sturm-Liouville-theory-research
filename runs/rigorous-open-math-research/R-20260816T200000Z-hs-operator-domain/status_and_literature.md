# Status and literature — R-20260816T200000Z-hs-operator-domain

## Problem status (as decided by this run)
- Open point from upstream (left-def run, 2026-08-16): whether the SL_hs system
  {Q_n^{(s)}} (s >= 4) lies in the operator domain D(K_c^{s/2}); operator-domain vs
  abstract-completion reading of H^s.
- This run RESOLVES the membership/difference/density questions strictly for s >= 4.
  Status label: RIGOROUS_PARTIAL_RESULT (the load-bearing membership/difference/
  density theorems are STRICT; one auxiliary degree-spectrum lemma stays at the
  EVIDENCE level and is explicitly non-load-bearing).

## Exact known theorems used (verified)
- `K_c` self-adjoint, positive, 0 notin spectrum on D(K_c) with the Krein BC.
  [project convention; standard left-definite operator theory]
- Functional-calculus powers: D(K_c^r) = {f : K_c^j f in D(K_c), j < r};
  D(K_c^{r+1/2}) = {f : K_c^j f in D(K_c), j < r, K_c^r f in D(K_c^{1/2})}.
  [Littlejohn-Wellman, J. Diff. Eq. 181 (2002) 280-339: A general left-definite
  theory; and the abstract left-definite model: Fischbacher-Gesztesy-Hagelstein-
  Littlejohn, arXiv:2408.01514 (2024).]
- Endpoint derivative formula `P_n^{(m)}(1) = (n+m)!/(2^m m! (n-m)!)`.
  [classical, Legendre polynomial; verified against the SL_h2/hs docs]
- Krein-Sobolev polynomials K_n and coefficient recurrence (source (9)/(11)/(12)):
  `K_n = sum_i a_{n-2i}(P_{n-2i} - P_{n-2i-2})`, a_0=a_1=a_2=a_3=1, recurrence for a.
  [Littlejohn-Quintero (Krein-Sobolev OPs); Jones-Littlejohn-Quintero Roba,
  Axioms 14 (2025) 115; SL_hs doc 2026-08-05] — validated against the doc closed
  forms K_0..K_4.
- `{p_n}` sparse family: SL_h2 (s=2) and SL_h3 (s=3) completeness. [project docs]

## New results (this run)
- Theorem MO: Q_n^{(s)} in D(K_c^{s/2}) iff n in {0,1} for s >= 4 (both parities).
- Lemma DE/DO/DM/A-POS/L-KS: positivity/monotonicity of the Krein transport deficit
  (the proof mechanism).
- Theorem SPD: operator domain != abstract completion for s >= 4.
- Theorem ND: span{Q_n^{(s)}} not dense in the operator domain for s >= 4;
  left-definite density criterion does not extend to s >= 4.
- Proposition Q1a: degree spectrum of D(K_c^{s/2}) ∩ Pi = {0,1} U {d >= 2 floor(s/2)+2}
  (structural, exact for r<=3; general lemma EVIDENCE-level).
- Correction: upstream S1d "H^s ∩ C[x] = span{1,x} for s >= 4" is REFUTED (there are
  degree >= 2r+2 polynomials in H_op^s); the upstream L1'' (sparse family not dense)
  STANDS.

## Literature map / novelty
- General left-definite theory: Littlejohn-Wellman 2002 (spectral theory of
  left-definite spaces), Fischbacher et al. arXiv:2408.01514 (abstract model),
  Fleeman-Frymark-Liaw (boundary conditions for general left-definite theory,
  J. Approx. Theory 2019).
- Krein-Sobolev orthogonal polynomials: Littlejohn-Quintero (2025,
  10.1007/978-3-031-90135-5_7), Jones-Littlejohn-Quintero Roba (Axioms 2025).
- These establish the abstract framework and the explicit polynomial systems but do
  NOT settle the specific operator-domain vs abstract-completion membership question
  for the Krein boundary condition at s >= 4. Web sweep (2026-08-16) surfaced no
  source resolving it.
- Novelty classification: POTENTIALLY_NEW (operator-domain membership of the
  transported Q_n^{(s)} failing the level-1 Krein condition for s >= 4, and the
  operator-domain/abstract-completion separation, are not found in the literature
  sweep). The mechanism (transport deficit positivity) is a new proof ingredient for
  this project.

## Significance
- Useful structural theorem + correction: it resolves a prerequisite for the
  left-definite density criterion beyond s = 3, and it corrects an over-reach in the
  upstream run without invalidating its sparse-family conclusion.

## Coverage gaps (for directed reconnaissance)
- No external source was deeply fetched for the exact operator-domain/abstract-
  completion separation in the Krein setting; a deeper targeted literature audit is
  recommended before any strong novelty claim (recorded as residual risk).
