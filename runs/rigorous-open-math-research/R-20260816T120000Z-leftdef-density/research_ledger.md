# Research Ledger — R-20260816T120000Z-leftdef-density

Chronological record of work.

## Entry 1 (struct facts, EVIDENCE exact)
Ran reproducibility/ld_struct_facts.py.  Confirmed:
- H^1 moment matrix <x^i,x^k>_1 NON-diagonal (F1; e.g. <x^1,x^3>_1 = 2c/5 != 0).
- All p_n (n in D) satisfy Krein BC => in H^2 (F2).
- x^2, x^3 do NOT satisfy Krein BC => not in H^2 (F3).
- <w,p_4>_2 = M_4 - 2 M_2 is NOT a valid moment decomposition (M_2 undefined) (F4).
- F5 (AUDIT-CORRECTED): H^2 has only monomials 1,x present (x^k absent for
  k>=2); (1,x)_2 = 0, so the H^2 monomial block is vacuous/trivial.  The
  non-diagonal matrix that blocks DensBC O1 finiteness lives in H^1 (F1).
Decision: DensBC O1 (H1) hypothesis fails for H^s, s>=2; need structural audit.

## Entry 2 (stronger structural fact)
Checked which monomials are in H^2 via Krein BC: ONLY x^0=1 and x^1=x pass;
x^k for ALL k>=2 fail.  So H^2 ∩ C[x] = span{p_n} (sparse family), and the only
monomials in H^2 are 1, x.  This sharpens the packet's "x^2,x^3 absent" to
"all x^k (k>=2) absent."  (EVIDENCE exact; higher s by H^s ⊂ H^2.)

## Entry 3 (counterexample, exact)
Ran reproducibility/ld_counterexample.py.  For V = ker(Delta) in H^2:
- Q_sp = {p_0} ∪ {even p_{2n}} (even sparse family only).
- q = p_5 - 2 p_7 = -2x^7+4x^5-2x^3 is odd, in V (Delta q = 0), nonzero, in H^2,
  and orthogonal (exact) to every kept even p_n.
- Hence q in V ∩ Q_sp^perp, q != 0 => closure(span Q_sp) != V (DensBC Theorem A).
Decision: first concrete left-definite STRICT non-density instance (Theorem L5).

## Entry 4 (transfer descent)
Formalized Theorem L3: K_c isometry H^t -> H^{t-2} maps constrained density
problem down to H^{s'} (s' in {0,1}); the clean 3-term jump base is available at
a single descent r=1 (s=2,3); for s>=4 the iterate is higher-order (audit-
corrected after subagent review).  STRICT (proof in candidate_proof.md).

## Entry 5 (whole-space recovery, Q2/Q3)
Theorem L1: V = H^s => density holds for all integer s >= 1; no first
obstruction survives (s=1: M_2,M_3 killed by growth; s>=2: M_2,M_3 undefined).
STRICT (proof later repaired per audit, see Entry 9).

## Entry 6 (literature sweep)
4 web queries (2026-08-16).  No external exact constrained-density criterion
surfaced; closest: Krein-Sobolev (Axioms 2025), exceptional OPS completeness,
moment-problem char.  Novelty: POTENTIALLY_NEW (not claimed open as a fact).

## Entry 7 (routes + status)
Routes A-D PROVED; E PARTIAL (O1'LD open); F inherited open.  O1'LD named and
no closed form claimed.  Reduced core (O1'LD) recorded honestly.

## Entry 8 (independent adversarial audit COMPLETED: REPAIRABLE_GAP)
Fresh-context subagent 023d145f returned verdict REPAIRABLE_GAP with no critical
errors.  Findings:
  G1 (primary): L1's density proof cited SL_denseness_criteria Theorem 8
    step(i)/Lemma 7 for s>=2, which uses undefined moments (x^k, K_c p_{2m}
    notin H^s); "a fortiori" remark was a non-sequitur.  TRUE result, unsound
    proof for s>=2 (s>=4).
  G2: L3 remark overclaimed the 3-term jump recursion for iterates (s>=4);
    correct only for r=1 (s=2,3); s'=1 moments clarified.
  G3: L6(3) wrongly said non-diagonal "for H^1 and H^2"; H^2 monomial block is
    vacuous (only 1,x); non-diagonality genuine in H^1.
  Bottom line: L5 airtight; S1, L2, L3-core, L4 correct; L1 density is the
  single genuine blocker, repairable.

## Entry 9 (repairs applied, per revision policy)
- L1 repaired (STRICT): density of span{p_n} in H^s proved uniformly WITHOUT
  undefined H^s-moments — s=1 by first-moment criterion; s=2 by SL_h2 L^2-descent
  (L^2-moments); s=3 by SL_h3 H^1-moment argument; s>=4 via S1 + explicit
  complete orthogonal system {Q_n^{(s)}} of SL_hs (Q_n^{(s)} in span{p_n}, dense).
  Replaced the "a fortiori" remark with a correct statement.
- L3 remark corrected: 3-term jump restricted to r=1 (s=2,3); s>=4 higher-order.
- L6(3) corrected: non-diagonality stated for H^1 only; H^2 monomial block
  vacuous.  ld_struct_facts.py F5 corrected accordingly.
- A fresh re-verification subagent (ed2a5348) launched to re-check the repaired
  points (L1 proof, L3 remark, L6(3)).

## Entry 10 (DECISIVE re-verifier finding: FATAL_GAP on L1 s>=4, corrected)
Re-verifier ed2a5348 returned FATAL_GAP: my L1 s>=4 repair was itself wrong. Exact
checks (this run, sympy) confirm:
- p_4 NOT in H^4 = D(K_c^2): K_c p_4 = c x^4-(2c+12)x^2+4 has (K_c p_4)'(+1)=-24,
  (K_c p_4)'(-1)=+24, while (K_c p_4)(1)-(K_c p_4)(-1) = 0; so K_c p_4 fails the
  Krein BC => K_c p_4 notin H^2 => p_4 notin H^4.
- p_n (n=4..8) all fail H^4 and H^6; p_0=1, p_1=x are in every H^s.
- Hence for s >= 4 (operator-domain H^s = D(K_c^{s/2})):
  H^s ∩ C[x] = span{1,x}, and the sparse family is NOT a subset of H^s.
- Consequences: (a) S1's equality is FALSE for s>=4; the correct fact is
  H^s ∩ C[x] = span{1,x} for s>=4 (and p_n in H^s only for s in {1,2,3}).
  (b) L1 whole-space recovery via the sparse family holds only for s in {1,2,3};
  for s>=4, Q_sp = {1,x} and closure(span Q_sp) = span{1,x} != H^s (density FAILS).
  (c) The packet's Q3 premise ("H^s complete for all integer s>=1 [via sparse
  family]") is FALSE for s>=4 under the operator-domain reading; full-space
  completeness there is via the SL_hs system {Q_n^{(s)}} (whose membership in
  D(K_c^{s/2}) for s>=4 is itself flagged open/ambiguous).
Decision: scope all STRICT whole-space results to s in {1,2,3}; record the s>=4
negative finding (L1'') as a decisive correction.

## Entry 11 (correction materialized + integrity)
candidate_proof.md rewritten (write) to scope L1/L2/L4/L6 to s in {1,2,3} with the
exact s>=4 negative finding L1''; S1 corrected to S1a-S1d; problem_contract,
obligation_graph, status_and_literature, final_report, counterexample_log,
ld_struct_facts.py updated (write tool only; do NOT use str_replace_editor — it
drops content).
The str_replace_editor was found to silently drop replacement content in several
files (candidate_proof.md, ld_struct_facts.py, research_ledger.md).  All affected
files were fully rewritten from scratch with the `write` tool and re-verified for
integrity (all sections/theorems present).  This ledger is the rewritten, complete
version.
