# Audit Report — R-20260816T120000Z-leftdef-density

- Audit date: 2026-08-16.
- Audit target: candidate_proof.md (Theorems L1-L6) + problem_contract.md against
  audited upstream results (DensBC Theorems A-H/E, DensBC O1 Theorems 1-5) and the
  left-definite docs (SL_h2/h3/hs/denseness_criteria).

## Audit trail (three stages)

### Stage 1 — Independent adversarial audit (fresh context, subagent 023d145f)
- verdict: **REPAIRABLE_GAP**, critical_errors: [].
- Findings:
  1. **L1 (s>=2):** the density proof cited denseness_criteria Theorem 8, whose
     step (i)/Lemma 7 uses quantities undefined for s>=2 (H^s-moments (w,x^k)_s
     and (w,K_c p_{2m})_s with x^k, K_c p_{2m} notin H^s); "a fortiori" remark was
     a non-sequitur.  L5 airtight; S1(s=2), L2, L4, L3-core correct.
  2. **L3 remark:** 3-term jump overclaimed for iterates (s>=4).
  3. **L6(3):** wrongly said non-diagonal "for H^1 and H^2"; H^2 monomial block is
     vacuous; non-diagonality genuine in H^1.

### Stage 2 — Re-verification of first repair (subagent ed2a5348)
- The initial repair (uniform L1 proof, s=1/2/3 plus s>=4 via S1 + {Q_n^{(s)}})
  was FATAL in its s>=4 branch:
  - **S1's equality is FALSE for s>=4:** p_n (n>=4) are NOT in H^s for s>=4; under
    the operator-domain H^s = D(K_c^{s/2}), H^4 ∩ C[x] = span{1,x}.
  - Exact witness: K_c p_4 = c x^4-(2c+12)x^2+4, (K_c p_4)'(+1)=-24,
    (K_c p_4)'(-1)=+24, endpoint difference 0 => K_c p_4 fails the Krein BC, so
    p_4 notin H^4.  Confirmed by this run's exact script (S1d).
  - Hence "Q_n^{(s)} in span{p_n} via S1" is invalid; the L1 s>=4 density via the
    sparse family is FALSE (Q_sp = {1,x}, closure = span{1,x} != H^s).
  - Points 2 and 3 (L3 remark, L6(3)) were verified CORRECT in the revision.

### Stage 3 — Final correction (this run)
- candidate_proof.md corrected: STRICT results scoped to s in {1,2,3} (L1' for
  whole-space density; L2/L4), plus the decisive negative finding L1''/S1d for
  s >= 4 (sparse family not a subset of H^s; whole-space density fails).  L6
  updated; the packet's Q3 premise for s >= 4 is honestly corrected.  A new open
  point (membership of the SL_hs system {Q_n^{(s)}} in D(K_c^{s/2}) for s>=4;
  operator-domain vs abstract-completion reading) is flagged.
- All corrected changed points were re-derived with exact arithmetic by this run.

## Per-obligation verdict (final, corrected scope)

- S1a/S1b/S1c (s in {1,2,3} structural facts): PASS.
- S1d (s >= 4: sparse p_n (n>=4) notin H^s; H^s ∩ C[x] = span{1,x}): PASS
  (exact witness p_4 notin H^4).
- L1' (s in {1,2,3} whole-space sparse density): PASS (s=1 first-moment; s=2
  SL_h2 L^2-descent; s=3 SL_h3 H^1-moments; all moments well-defined).
- L1'' (s >= 4 negative: Q_sp = {1,x}, density fails): PASS (STRICT deduction).
- L2/L4 (s in {1,2,3}): PASS.  L3 core: PASS.  L3 remark: PASS (r=1; higher-order
  at s>=4; correct moments).  L5: PASS (airtight).  L6: PASS as honest status
  (O1'LD open; DensBC O1 Theorem 5 finiteness not automatic via H^1 non-diagonality;
  H^s monomial block vacuous for s>=2).
- Packet Q3 ("H^s complete for all integer s>=1 via sparse family, V=H"): CORRECTED
  — holds only for s in {1,2,3}; FALSE for s >= 4 (L1'').

## Residual risk

- **O1'LD (open):** general proper closed V ⊆ H^s (s in {1,2,3}; or surviving
  candidates for s>=4) density decision = genuine moment/membership problem; no
  closed form claimed.
- **NEW (open):** whether the SL_hs orthogonal system {Q_n^{(s)}} (s>=4) lies in
  the operator domain D(K_c^{s/2}); reconcile operator-domain vs abstract-completion
  readings of H^s for s >= 4 (this affects the project's s>=4 completeness claims).
- The s = 1 case uses the first-moment criterion (documented); s=2,3 use the
  SL_h2/SL_h3 proofs.  The odd-branch completeness of the SL_hs system (for
  s >= 5, if it is to be used) rests on the cited Krein-Sobolev H^1-completeness
  theorem; note this is not used in the final scoped L1'.
- Independent audits were fresh-context; the final corrected artifact's changed
  points were verified by exact re-derivation in this run.  (A further fresh
  verification of the FINAL corrected artifact is recommended before promotion,
  but the mathematical content has been independently re-derived.)
