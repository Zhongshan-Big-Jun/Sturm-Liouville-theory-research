# Audit Report — R-20260816T120000Z-leftdef-density

- Audit date: 2026-08-16.
- Audit target: candidate_proof.md (Theorems L1-L6) against problem_contract.md
  and the audited upstream results (DensBC Theorems A-H/E, DensBC O1 Theorems 1-5).

## Independent adversarial audit (fresh context) — COMPLETED

A fresh spawn-provider subagent (no shared chain-of-thought) audited the entire
artifact set as a first-time proof.  It returned:

- **verdict: REPAIRABLE_GAP**
- **critical_errors: []**  (no fatal / wrong-problem / circularity errors)

### Gaps found (verbatim summary)

1. **L1 (primary blocker, s>=2):** The proof of "span{p_n} dense in H^s" cited
   SL_denseness_criteria Theorem 8.  That theorem's step (i)/Lemma 7 uses
   quantities undefined for s>=2: H^s-moments (w,x^k)_s with x^k notin H^s
   (k>=2) and inner products (w, K_c p_{2m})_s with K_c p_{2m} notin H^s (e.g.
   K_c p_4 fails the Krein BC: (K_c p_4)'(1) = -24 != 0).  The "a fortiori"
   remark was a non-sequitur.  For s>=4 no valid proof of span{p_n}-density was
   present.  (Result is TRUE, but the written proof was unsound for s>=2.)
2. **L3 remark (moment base):** The 3-term jump recursion c N_{2m} = A_m
   N_{2m-2} - B_m N_{2m-4} was claimed for "{K_c p_n} or its iterate".  It is
   clean only for a single descent r=1 (s=2,3); for r>=2 (s>=4) K_c^r p_{2m}
   has >=4 monomial terms (higher-order recursion); for s'=1 the correct moments
   are L^2-moments (w,x^k)_L2, not (w,x^k)_1 as written.  Core L3 equivalence is
   correct.
3. **L6(3)/contract:** "non-diagonal Krein moment matrix verified for H^1 and
   H^2" is wrong for H^2: only monomials 1,x have defined moments and (1,x)_2 =
   (K_c 1, K_c x)_L2 = c^2 int x = 0, so the H^2 monomial block is diagonal.
   Non-diagonality is genuine for H^1 (e.g. (p_4,p_6)_1 = 128/105 + 181c/693
   != 0).

### Audited-good items (as reported by the verifier)
L5: PASS (airtight).  S1: PASS.  L2, L4: PASS given density.  L3 core: PASS.
L6: honest status (once L1/L6(1) and L6(3) are repaired).

## Repairs applied (per revision policy, Phase 9)

1. **L1 repaired (STRICT):** density of span{p_n} in H^s is now proved uniformly
   WITHOUT any undefined H^s-moment:
   - s=1: first-moment criterion (all moments (w,x^k)_1 defined, beta=1/2<1).
   - s=2: SL_h2 sound L^2-descent (K_c: H^2 -> L^2 isometry; L^2-moment jump
     recursion + growth lemma + polynomial bound).
   - s=3: SL_h3 H^1-moment argument (K_c: H^3 -> H^1 isometry; H^1-moments all
     defined; jump recursion + growth + |M_k| <= C sqrt(k)).
   - s>=4: S1 (H^s ∩ C[x] = span{p_n}) + the explicit complete orthogonal
     polynomial system {Q_n^{(s)}} of SL_hs: each Q_n^{(s)} is a polynomial in
     H^s, hence lies in span{p_n}, and span{Q_n^{(s)}} is dense in H^s, so
     span{p_n} is dense.
   The "a fortiori" remark was replaced with a correct statement.
2. **L3 remark corrected:** the 3-term jump recursion is restricted to a single
   descent r=1 (s=2,3, with the correct moment base: L^2 in s=2, H^1 in s=3);
   for s>=4 the iterated family K_c^r p_n is higher-order and the honest
   recursion in H^{s'} is stated as part of O1'LD.
3. **L6(3) corrected:** non-diagonality stated for H^1 only (e.g.
   <x^1,x^3>_1 = 2c/5 != 0); the H^2 monomial block is vacuous (only 1,x,
   (1,x)_2 = 0).  reproducibility/ld_struct_facts.py F5 corrected so it no
   longer lists x^4..x^7 as "in H^2".

## Status after repairs

- The single genuine blocker (L1 density for s>=2) has a sound replacement proof;
  the repaired candidate_proof.md must be re-verified at the changed points
  (L1 proof, L3 remark, L6(3)).  Per skill discipline, the reviser cannot
  self-certify closure; a fresh verifier re-check of the changed points is the
  next step before this run may be treated as independently audited PASS.
- O1'LD remains OPEN (genuine moment/membership problem); no closed form claimed.

## Residual risk

- **L1's s=1 case** uses the first-moment criterion (documented); **s=2,3**
  cases use the SL_h2/SL_h3 proofs whose internal steps are documented and
  exact-verified in the project corpus.  **s>=4** case (orthogonal-system
  route) rests on the SL_hs theorem; its ODD branch rests on the cited
  literature theorem "{K_n} complete in H^1" (Jones--Littlejohn--Quintero Roba),
  which is a KNOWN primary source but not re-derived inside this artifact set.
- L6 inherits DensBC O1 Theorem 5 from upstream (not contained in this artifact
  set); its conclusion (O1'LD open) is honest regardless.
- Independent subagent audit completed with REPAIRABLE_GAP; the repaired changed
  points still need an independent re-check to reach an audited-PASS level.
