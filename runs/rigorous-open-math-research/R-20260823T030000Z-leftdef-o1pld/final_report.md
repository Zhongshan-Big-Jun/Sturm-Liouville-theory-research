# Final Report — R-20260823T030000Z-leftdef-o1pld

## Status label
**RIGOROUS_PARTIAL_RESULT**

O1'LD is not solved.  After the independent audit and repair, this run adds
new STRICT structural theorems for the s = 2 (L^2 descent) subclass, a STRICT
concrete non-density example, and honest remaining gaps for s = 3.  The
cofinite-N theorem is no longer claimed as STRICT; it is NOT-YET-STRICT and
conditional on a tail-rigidity claim that is not fully proved.

## Exact theorem / result produced

### STRICT
1. **L^2 finite-support moment rigidity.**  If f ∈ L^2(-1,1) has only finitely
   many nonzero moments (f,x^k), then f = 0.  Proof uses the L^p Müntz-Szász
   theorem for Lebesgue measure, via explicit even/odd weighted substitutions
   to L^2(0,1).  (Lemma 1 / Corollary 2)
2. **Cauchy-Schwarz moment bound.**  |(f,x^k)| ≤ ||f||_2 sqrt(2/(2k+1));
   consequently a linearly growing moment sequence is not L^2-realizable.
   (Lemma 3)
3. **Parity decomposition.**  For any closed W ⊆ L^2,
   closure(span{ q_n : n ∈ N }) = closure(span{ q_n : n ∈ N_e })
   ⊕ closure(span{ q_n : n ∈ N_o }).  (Theorem 7 / Corollary 8)
4. **Concrete non-density (μ_4).**  Let V = {f ∈ H^2 : ∫ (K_c f)(x) x^4 dx = 0}.
   Then N = {1} ∪ odd sparse indices {2m+1 : m ≥ 2}, closure(span Q_sp) = odd
   subspace of H^2, and density fails.  The kept-set calculation is exact; the
   formula
   μ_4(q_{2m}) = -2(8cm^2+10cm+3c+32m^3+48m^2-80m) /
   ((m-1)(2m+1)(2m+3)(2m+5))
   is negative for c>0, m≥2.  The odd-density step uses the SL_h2 odd growth
   lemma and M_1=0 from q_1.  (Theorem 9)
5. **H^1 polynomial moment bound** (prior result, retained STRICT):
   |M_k| ≤ C(c, ||w||_{H^1}) sqrt(k).

### NOT-YET-STRICT / conditional
6. **Tail L^2 rigidity (Claim 4).**  If tail q_n recurrences hold for m ≥ m0,
   then nonzero L^2-realizable moment solutions should vanish.  The dominant
   factorial-growth case is classical, but the exceptional minimal
   (polynomially decaying) solution is not fully excluded in this repair; hence
   not strict.
7. **Cofinite-N density theorem for s = 2 (Theorem 5).**  If N ⊆ D is cofinite,
   then span{q_n : n ∈ N} is dense in L^2.  The proof is rewritten to use the
   actual three-term q_n recurrences and the tail rigidity Claim 4.  Because
   Claim 4 is not strict, Theorem 5 is NOT-YET-STRICT.
8. **Proper-V non-cofinite corollary (Corollary 6).**  Conditional on Theorem 5;
   NOT-YET-STRICT.

### EVIDENCE / OPEN
9. **s = 3 (H^1 descent): infinite-run inadmissibility.**  Downgraded from
   STRICT to EVIDENCE/PLAUSIBLE.  The prior H^1 moment bound is STRICT, but it
   does not by itself prove tail-recurrence inadmissibility; no precise proof
   is supplied.
10. **H^1 finite-run realizability.**  OPEN (EVIDENCE only, no proof).

## Proof or construction
See candidate_proof.md (sections 1-7) and the appended Repair log.  No numerical
evidence is used in the STRICT proofs; the only numerical material is labeled
EVIDENCE in section 6.

## Verification performed
- Independent audit report R-20260823T040000Z-leftdef-o1pld-audit identified
  the errors; this repair removed the DensBC O1 run algebra from the L^2/H^1
  descent, fixed the Müntz weighted substitution, and repaired the μ_4
  odd-density argument.
- Exact sympy verification of the μ_4 formula remains.
- The tail-rigidity minimal-solution case was not fully derived; hence Claim 4,
  Theorem 5 and Corollary 6 remain NOT-YET-STRICT.

## Remaining gaps
- General O1'LD for arbitrary W ⊆ L^2: characterize the closure of kept even and
  odd q_n subfamilies.
- Prove the tail L^2 rigidity Claim 4; then Theorem 5/Corollary 6 can be
  upgraded to STRICT.
- H^1 finite-run realizability, the s=3 infinite-run inadmissibility (currently
  EVIDENCE/plausible), and the s=3 general criterion.
- The general left-definite constrained-density problem for other s/constraint
  classes.

## Failed / blocked routes
- Direct transfer of H_beta/H_lambda finite-rank criterion to L^2: the current
  repair no longer claims cofinite-N impossibility as STRICT; it would follow
  from Claim 4.
- The DensBC O1 two-term run/recursion algebra is NOT applicable to the L^2/H^1
  q_n moment recurrences; all uses in the descent were removed.
- H^1 finite-support rigidity: blocked/open (EVIDENCE inconclusive).

## Novelty status
POTENTIALLY_NEW for the STRICT L^2 finite-support moment rigidity, parity
decomposition, and the μ_4 example.  The cofinite-N theorem is likely true but
not-yet-strict; the general O1'LD remains open; no claim of resolution.

## Human/model/tool contributions
- Model (this subagent) performed derivation, proof, exact computation, and
  write-up.  No nested subagents were spawned, per instruction.

## Artifacts
- problem_contract.md
- status_and_literature.md
- approach_registry.md
- research_ledger.md
- obligation_graph.md (updated)
- candidate_proof.md (updated)
- escalation_ladder.md
- audit_report.md
- performance_log.md
- reuse_summary.md
- final_report.md (updated)
- reproducibility/o1pld_l2_mu4.py
- reproducibility/O1pLD_L2_Scaffold.lean

## Confidence by axis
- Semantic fidelity: HIGH (uses exact prior definitions; no silent domain change).
- Mathematical correctness: HIGH for the listed STRICT theorems; Müntz-Szász
  citation now explicit for Lebesgue L^2.  Claim 4 and the cofinite-N theorem
  are honestly NOT-YET-STRICT.
- Completeness: PARTIAL (O1'LD open).
- Novelty: MEDIUM (structural theorems + explicit example).
- Reproducibility: HIGH (exact script, documented).
