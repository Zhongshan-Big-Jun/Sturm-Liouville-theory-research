# Final Report — R-20260816T200000Z-hs-operator-domain

Run: R-20260816T200000Z-hs-operator-domain
Task: Q-20260816-hs-operator-domain-C0D1E2F3
Portfolio problem: O-2026-SL-DENS-BC-A1B2C3
Upstream context run: R-20260816T120000Z-leftdef-density

## Status label
**RIGOROUS_PARTIAL_RESULT**

## Upstream result status (verbatim)
- This run (R-20260816T200000Z-hs-operator-domain): `RIGOROUS_PARTIAL_RESULT`
  (load-bearing membership/difference/density theorems are STRICT; one auxiliary
  degree-spectrum lemma stays at the EVIDENCE level and is explicitly non-load-bearing;
  independent adversarial audit = REPAIRABLE_GAP with two localized, non-load-bearing
  gaps, both repaired/recorded).

## Exact theorem / result proved (strict)
Let `K_c = -d^2/dx^2 + c` on `[-1,1]` with the Krein boundary condition
`f'(1) = f'(-1) = (f(1)-f(-1))/2`, c > 0, and `H^s = D(K_c^{s/2})` under the
OPERATOR-DOMAIN reading. For every integer s >= 4:

- **Theorem MO (STRICT).** The SL_hs orthogonal polynomials lie in the operator
  domain iff n in {0,1}: for even s = 2r (r >= 2), `Q_n^{(s)} = K_c^{-r}P_n in
  D(K_c^r)` iff n in {0,1}; for odd s = 2r+1 (r >= 2), `Q_n^{(2r+1)} = K_c^{-r}K_n in
  D(K_c^{r+1/2})` iff n in {0,1}. For n >= 2, Q_n^{(s)} fails the level-1 Krein
  transport condition (`K_c^{-1}` of the base polynomial is not in D(K_c)); the base
  positivity is proved via the Krein deficit (Lemmas DE/DO/DM/A-POS/L-KS, STRICT).
- **Theorem SPD (STRICT).** The operator domain `H_op^s = D(K_c^{s/2})` and the
  abstract completion `H_abs^s` (of all polynomials under the left-definite inner
  product) are NOT equal for s >= 4: `Q_2^{(s)} in H_abs^s` (a polynomial, hence in
  the dense subspace) but `Q_2^{(s)} notin H_op^s` (MO). The SL_hs doc's completeness
  claim for s >= 4 holds in `H_abs^s`, not in `H_op^s`.
- **Theorem ND (STRICT).** `span{Q_n^{(s)}}` is NOT dense in `H_op^s = D(K_c^{s/2})`
  for s >= 4: only `Q_0, Q_1` (constants/linear, i.e. span{1,x}) lie in the operator
  domain, a 2-dimensional proper closed subspace; `H_op^s` is infinite-dimensional.
  Hence the left-definite density criterion via the SL_hs system does NOT extend to
  s >= 4 under the operator-domain reading.
- **Proposition Q1a (partial + strict correction).** (i)(iii) STRICT: 1, x lie in
  every `H_op^s`; and the upstream auxiliary claim "H^s ∩ C[x] = span{1,x} for s>=4"
  is REFUTED (exact example: `x^2(x^4-5x^2+7) in D(K_3^2) = H^4`, degree 6). (ii)
  EVIDENCE/OPEN (non-load-bearing): `H_op^s ∩ Pi` has degree spectrum
  `{0,1} ∪ {d >= 2 floor(s/2)+2}` (verified exactly for r <= 3, c in {1,3,10}).

## Direct answers to the three packet items
1. **Which polynomials in D(K_c^{s/2}):** 1, x always; polynomials of degrees
   `{d >= 2 floor(s/2)+2}` (structural, exact for r<=3); monomials beyond degree 1
   are NOT in the domain; and the SL_hs Q_n^{(s)} lies in the domain iff n in {0,1}.
2. **Operator-domain vs abstract completion:** they DIFFER for s >= 4. The SL_hs
   orthogonal system is complete in the abstract completion H_abs^s, not in the
   operator domain H_op^s = D(K_c^{s/2}); the mechanism is the failure of the formal
   transport `K_c^{-1}` of the base polynomial to satisfy the Krein BC at level 1.
3. **Density consequence:** `span{Q_n^{(s)}}` is NOT dense in `D(K_c^{s/2})` under
   the operator-domain reading; the left-definite density criterion does NOT extend
   to s >= 4 via the Q_n^{(s)} system.

## Verification performed
- Independent adversarial audit (fresh context subagent 88de280c): verdict
  **REPAIRABLE_GAP**, critical_errors empty. All load-bearing theorems (MO, SPD, ND)
  and lemmas (T, DE, DO, DM, L-KS) verified correct incl. three mandated dual-wire
  ground-truth checks (D_4 = 5(2c+21)/c^2 by two independent means; Q_4^(2) failing
  the Krein condition; x^2(x^4-5x^2+7) in D(K_3^2)). Two non-load-bearing gaps:
  Q1a(ii) every-degree lemma (EVIDENCE-level) and the A-POS literal monotonicity
  claim (false at a_2=a_3 but non-load-bearing). Both recorded/repaired (A-POS
  corrected; Q1a labeled EVIDENCE/OPEN).
- Exact-arithmetic EVIDENCE: 9 sympy scripts under reproducibility/, consolidated in
  evidence/evidence_log.txt (finite exact checks for n <= ~12, c in {1,3,10};
  corroborate, never close a strict obligation).
- Lean scaffold `lean-proof/SL/HsOperatorDomain_Scaffold.lean` builds
  (`lake build`, 8567 jobs, exit 0); all proof bodies `sorry` (scaffold, not verified).

## Remaining gaps
- OPEN (EVIDENCE-level, non-load-bearing): a rigorous general-r proof that
  `D(K_c^r) ∩ Pi` contains a polynomial of every degree >= 2r+2 (and no degree in
  2..2r+1) — i.e. closing Proposition Q1a(ii) for all r. Does not affect MO/SPD/ND.
- INHERITED (open, from upstream): DensBC O1'LD (general proper closed V density),
  O2' (constraints for all c), O3 (fractional window 3/2 <= s < 2).
- The standard functional-calculus facts used in Lemma T (D(K_c^r) characterization,
  D(K_c^{1/2}) form domain, eigenfunctions in every H_op^s) are cited standards,
  not re-proved from scratch.

## Failed / blocked routes
- Upstream auxiliary claim S1d "H^s ∩ C[x] = span{1,x} for s >= 4" REFUTED (over-reach);
  the left-def run's L1'' (sparse family {p_n} not dense for s >= 4) STANDS and is
  reused. No route of this run was blocked.

## Novelty status
POTENTIALLY_NEW — the operator-domain membership of the transported SL_hs system
{failing the level-1 Krein condition for s >= 4} and the operator-domain/abstract-
completion separation are not found in the 2026-08-16 web sweep (left-definite theory:
Littlejohn-Wellman 2002, Fischbacher-Gesztesy-Hagelstein-Littlejohn arXiv:2408.01514;
Krein-Sobolev: Littlejohn-Quintero 2025, Jones-Littlejohn-Quintero Roba Axioms 2025).
A deeper targeted literature audit is recommended before a stronger novelty claim.

## Human/model/tool contributions
- Model performed derivation, normalization, computation, write-up, and the
  adversarial-audit repair. Independent adversarial audit by a fresh-context subagent
  (no shared chain of thought). All EVIDENCE is exact arithmetic except one explicitly
  labeled float probe (wdensity_check.py, non-load-bearing).

## Reproducibility manifest
- repro_manifest.md + evidence/evidence_log.txt + reproducibility/*.py (exact).
- Lean: lean-proof/SL/HsOperatorDomain_Scaffold.lean (builds, sorry scaffold).
- No git commit/push (manager syncs at stage close).

## Confidence by axis
- Semantic fidelity: HIGH (normalized against packet + SL_hs doc + left-def run;
  usage of the operator-domain reading explicit; upstream S1d corrected).
- Mathematical correctness: the load-bearing theorems (MO, SPD, ND) and lemmas are
  STRICT and independently audited (REPAIRABLE_GAP with only non-load-bearing gaps,
  one repaired); Q1a(ii) honestly EVIDENCE/OPEN.
- Completeness: PARTIAL (Q1a(ii) general-r open; inherited O1'LD/O2'/O3 open).
- Novelty: MEDIUM (POTENTIALLY_NEW; deeper literature audit recommended).
- Reproducibility: HIGH (exact-arithmetic scripts, hashed via git-less run root,
  Lean scaffold builds).
