# Audit Report — R-20260816T200000Z-hs-operator-domain

- Audit date: 2026-08-16.
- Audit target: candidate_proof.md (Theorems MO, SPD, ND; Lemmas DE/DO/DM/A-POS/L-KS;
  Proposition Q1a; Lemma T) + problem_contract.md v1.1, against the task packet and
  the SL_hs doc, under the operator-domain reading.
- Auditor: independent fresh-context subagent (88de280c-af61-482a-b1b1-aeb991d0df4a),
  first-time-submission standard, counterexample-only elimination, dual-wire checks.

## Verdict (upstream, verbatim from auditor)
**REPAIRABLE_GAP** — critical_errors: [].

## Gaps (verbatim, from auditor)
1. **Q1a(ii)** — the claim that `H_op^s ∩ Pi` has degree spectrum
   `{0,1} ∪ {d ≥ 2 floor(s/2)+2}` is not strictly proved: the "no degree in 2..2r+1"
   part is asserted ("the minimal surviving degree is exactly 2r+2") without a
   derivation, and the "every degree >= 2r+2 present" part is explicitly EVIDENCE-level
   (finite checks r<=3, c in {1,3,10}). This is a strict-claim gap but is
   NON-LOAD-BEARING for MO/SPD/ND.
2. **A-POS** — the literal statement "a_m is strictly increasing for m>=2" is false
   (a_2 = a_3 = 1, so not strictly increasing at m=2->3); the induction as written
   establishes same-parity monotonicity only. The load-bearing claim a_m > 0 is
   correctly proved (and is all L-KS needs).

## What the auditor verified as CORRECT (verbatim summary)
- Parity Krein conditions: even f ∈ D(K_c) ⟺ f'(1) = 0; odd f ∈ D(K_c) ⟺ f'(1) = f(1).
- Formal inverse K_c^{-1} telescopes correctly.
- Lemma T direction (iff; contrapositive used for n>=2) correct; odd case adds
  K_n ∈ D(K_c^{1/2}) (automatic for smooth polynomials).
- Lemma DE/DO: endpoint formulas and positivity brackets correct.
- Lemma DM: both termwise comparison directions verified (B-A = G[1-1/(2K+1-2j)] > 0;
  A_{K+1,j}-B_{K,j} by numerator 4Kj+4j^2+2K+8j+3 > 0 plus the extra j=K term).
- Lemma L-KS: linearity + a_m>0 + D_m strictly increasing ⟹ L_n > 0 for n >= 2.
- Theorem MO, SPD, ND: logic sound, no circularity; SPD matches the contract's
  acceptance criterion (Q_2^{(s)} in H_abs^s \ H_op^s).
- Boundary cases: n=0,1 in; n>=2 out; c>0; s=4,5 minimal; s large.
- Dual-wire ground-truth checks (all performed independently by the auditor):
  D_4 = 5(2c+21)/c^2 (two independent means); Q_4^{(2)} fails the Krein condition;
  x^2(x^4-5x^2+7) ∈ D(K_3^2) = H^4 (refutes upstream S1d, preserves L1'').

## Repair applied (this run, from the exact gap list)
- A-POS corrected in candidate_proof.md: statement now reads "a_m > 0 for all m; each
  same-parity subsequence strictly increasing", with a remark that the literal
  "strictly increasing for m>=2" is FALSE (a_2=a_3) and non-load-bearing (L-KS uses
  only a_m > 0). Proof of a_m > 0 is the same induction.
- Q1a(ii) is already labeled EVIDENCE/OPEN in candidate_proof.md §5 and §10 and in the
  obligation graph (PARTIAL); it is explicitly non-load-bearing. No MO/SPD/ND change
  was needed (the auditor found them correct).

## Re-verification after repair
- The repair changed only the A-POS statement (a strict-claim wording correction that
  WEAKENS a claim and removes a false statement); no downstream obligation depends on
  the removed monotonicity claim (L-KS depends on a_m > 0 only). MO/SPD/ND are
  unchanged and were already verified correct. Q1a unchanged (already EVIDENCE/OPEN).
- Lean scaffold SL/HsOperatorDomain_Scaffold.lean builds successfully
  (`lake build SL.HsOperatorDomain_Scaffold`, 8567 jobs, exit 0); all proof bodies
  are `sorry` (scaffold, not a verified artifact) as required by the skill.

## Per-obligation final verdict
- Lemma T: PASS. DE: PASS. DO: PASS. DM: PASS. A-POS (a_m>0): PASS after correction;
  (literal stricter monotonicity): corrected statement. L-KS: PASS. MO: PASS. SPD: PASS.
  ND: PASS. Q1a (i),(iii): PASS (1,x and the refutation, exact). Q1a (ii): PARTIAL /
  EVIDENCE (every-degree lemma open for general r; explicitly non-load-bearing).

## Residual risk
- The standard functional-calculus facts (D(K_c^r) characterization, D(K_c^{1/2}) as
  the form domain containing all polynomials, eigenfunctions of K_c in every H_op^s)
  are cited standards, taken as given rather than re-proved from scratch.
- The every-degree lemma (Q1a general r) is EVIDENCE/OPEN; a rigorous leading-coefficient
  / triangularity induction would close it, but it does not affect the strict conclusions.
- Auditor did not re-run sympy; relied on the evidence log plus independent manual
  (algebraic) re-derivation, which matched.
