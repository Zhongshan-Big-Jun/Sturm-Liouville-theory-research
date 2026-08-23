# Adversarial Audit Report — R-20260823T030000Z-leftdef-o1pld

Audit run: `R-20260823T040000Z-leftdef-o1pld-audit`
Target run: `R-20260823T030000Z-leftdef-o1pld`
Auditor: independent adversarial auditor (no subagents spawned, as instructed).
Date/status: 2026-08-23

## Verdict

**REPAIRABLE_GAP**

The new statements are mostly plausible and several are true, but the
candidate proof as written contains load-bearing applications of the wrong
recursive model (DensBC O1 run algebra) to the L^2/H^1 descent.  The
finite-support Müntz step also uses an unjustified weighted-measure form.
These are repairable, not fatal to the mathematical outcomes, but the run
cannot be registered as STRICT in its current state.

**First erroneous step:** `candidate_proof.md §3 Theorem 4, step 2` — the
application of the DensBC O1 two-term run algebra to the L^2 q_n moment
system.  This single mis-application cascades into the cofinite-N theorem and
the μ_4 odd-density step.

## Executive summary

The solver's central new tool is the L^2 finite-support moment rigidity.  That
statement is true, but the proof's Müntz application is under-specified.

The claimed cofinite-N density theorem and the μ_4 non-density example are
both likely true, but their proofs invoke the DensBC O1 two-term run
decomposition.  In the s=2 descent, the relevant equations are the **three-term
q_n moment recurrences**

```
c M_{2m}   = A_m M_{2m-2} - B_m M_{2m-4}
c M_{2m+1} = A'_m M_{2m-1} - B'_m M_{2m-3}
```

These are *not* the two-term p_n recursions

```
M_{2m} = (m/(m-1)) M_{2m-2}
```

whose solutions are the linear run formula used in the candidate proof.  The
linear-growth "infinite run" language therefore does not describe the actual
s=2 descent.  The correct replacement is the SL_h2 growth lemma applied to a
tail of the three-term recurrence (a tail version is needed, but it is a minor
extension of the existing proof).

## Claim-by-claim audit

### 1. L^2 finite-support moment rigidity (Lemma 1 / Corollary 2)

- **Statement fidelity:** True.  If f in L^2(-1,1) has finitely many nonzero
  moments, then f=0.
- **Proof issue:** The proof says the L^p Müntz-Szász theorem applies to the two
  finite Borel measures μ_e(dy)=y^{-1/2}dy and μ_o(dy)=y^{1/2}dy on [0,1].
  The standard L^p Müntz-Szász theorem is for Lebesgue measure on (0,1), not
  for an arbitrary finite Borel measure.  The general finite-measure statement
  is false: take μ=δ_0+δ_1; after deleting the constant monomial, the remaining
  monomials {x^k:k≥1} all evaluate to (0,1) on the support, so their span is
  not dense in L^2(μ).
- **Repair:** Replace the one-sentence measure claim by the explicit weighted
  reduction:
  - even part: h(y)=y^{-1/4} f_e(√y) ∈ L^2(0,1), sending x^{2m}→y^{m-1/4};
  - odd part: h(y)=y^{1/4} f_o(√y)/√y?  Use t(y)=y^{1/4}g(y) ∈ L^2(0,1),
    sending x^{2m+1}→y^{m+1/4}.
  Then apply the L^p Müntz-Szász theorem on Lebesgue L^2 to the shifted
  exponent sets {m-1/4:m≥1} and {m+1/4:m≥1}, both of which have divergent
  reciprocal sums.  This gives a rigorous proof.  No part of the final theorem
  is false.

### 2. Infinite runs inadmissible in L^2 (Lemma 3)

- **The raw Cauchy-Schwarz fact is true:**
  |M_k| ≤ ||f||_2 √(2/(2k+1)).
- **But the "consequently" is not proved for the s=2 descent.**  The proof
  asserts that in the run decomposition of the s=2 descent an infinite run with
  base b has M_k = t_b floor(k/2)/floor(b/2), i.e. linear growth.  That formula
  is the solution to the **DensBC O1 two-term p_n run recursion**, not the
  **three-term q_n recursion** that actually describes orthogonality to K_c p_n
  in L^2.
- Concrete discrepancy: for c=1 and the even equations, the q_4 equation is
  M_4 = 14 M_2 - 4 M_0, whereas the DensBC run formula would give M_4 = 2 M_2.
- **Repair:** Use the three-term tail recurrence.  The correct inadmissibility
  is stronger: if all q_{2m} for m≥m0 are kept, any nonzero solution of the
  three-term recurrence grows factorially (or at least is not L^2-realizable),
  so the tail moments must vanish.  A tail version of the SL_h2 growth lemma
  must be added.  The statement "infinite runs inadmissible" is therefore
  plausibly true but not proved by the current argument.

### 3. Cofinite-N density theorem (Theorem 4 / Corollary 5)

- **Statement fidelity:** The statement is likely true, but the submitted proof
  is invalid at step 2.  It again invokes the DensBC O1 run/recursion algebra,
  which is not the correct recursion for {q_n}.
- **Correct proof outline:** Let N be cofinite in D and f⊥{q_n:n∈N}.  Choose R
  such that all n≥R in D are in N.  Then for each parity there is a tail
  m≥m0 for which the three-term recurrence holds.  If the two initial moments
  at the tail are not both zero, the tail growth lemma gives unbounded moments,
  contradicting |M_k|≤||f||_2√(2/(2k+1)).  Hence all moments of both parities
  are zero and f=0.  The cofinite-N conclusion then follows from the Hilbert
  space orthogonal-complement criterion.
- **Corollary 5** (proper V cannot have cofinite N) is a valid consequence of
  a correct Theorem 4.
- The existing proof must be rewritten before this result can be called STRICT.

### 4. Parity decomposition (Theorem 6 / Corollary 7)

- **PASS.**  Even and odd subspaces are orthogonal in L^2, so
  closure(span even kept) ⊕ closure(span odd kept) equals the closure of the
  full span.  The proof is standard and correct.

### 5. Concrete non-density: V = ker μ_4 (Theorem 8)

- **Algebra of the kept set and μ_4(q_{2m}):** Correct.  The exact formula
  reproduces the SymPy output; the numerator bracket is positive for c>0 and
  m≥2, so all even q_{2m} are excluded.  q_0 is excluded, odd q_n are included.
- **Proof issue in step 5:** The odd family is claimed dense in the odd L^2
  subspace because "base M_3 would have to grow linearly, impossible by
  Lemma 3".  This is not the actual q_n behavior.  In the odd q_n equations,
  M_3 is the free parameter and the recurrence gives M_{2m+1}=M_3 u_m with
  u_m ≥ (4/c)^{m-1}m!, i.e. factorial growth, not linear growth.  The
  correct proof is the SL_h2 odd-side growth lemma (M_1=0 from q_1, then
  factorial growth contradicts the L^2 moment bound).
- **Minor typo:** Step 5 says `{q_{2m+1}: m >= 1}`; the sparse family only has
  m≥2, so this should be m≥2 (q_3 does not belong to the family, and the
  index set D excludes 3).
- **Conclusion:** The non-density example is true; the proof needs the corrected
  odd-density argument.

### 6. H^1 descent (s = 3)

- **The bound |M_k| ≤ C√k is a proved prior result** (SL_h3 Lemma 6), so that
  part is STRICT.
- **The transition "therefore infinite runs are never realizable in H^1" is not
  supported as written.**  It again uses the linear-growth run model that does
  not match the actual H^1 q_n moment recurrences.  A precise statement
  requires defining "infinite run" in the H^1 descent and proving the tail
  three-term recurrence has no nonzero H^1-realizable solution.
- **The finite-run H^1 question being left open is consistently labeled
  EVIDENCE; that is honest and correctly not presented as a theorem.**

## Structured verification output

```json
{
  "verdict": "REPAIRABLE_GAP",
  "critical_errors": [
    {
      "location": "candidate_proof.md §3 Theorem 4, step 2 (and §2 Lemma 3 application)",
      "issue": "Applies DensBC O1 two-term run/recursion algebra to the s=2 descent. The actual q_n orthogonality equations are the three-term recurrences c M_{2m}=A_m M_{2m-2}-B_m M_{2m-4} (same for odd), not the two-term p_n recursion whose solution is the claimed linear run formula."
    },
    {
      "location": "candidate_proof.md §5 Theorem 8, step 5",
      "issue": "The odd-family density argument says the base M_3 would have to grow linearly. The actual odd q_n recurrence gives factorial growth; a correct proof must use the SL_h2 growth lemma."
    },
    {
      "location": "candidate_proof.md §1 Lemma 1",
      "issue": "The proof cites the L^p Müntz-Szász theorem for finite Borel measures. The standard theorem is for Lebesgue measure; the general finite-measure version is false (counterexample: μ=δ_0+δ_1 after deleting the constant monomial)."
    }
  ],
  "gaps": [
    {
      "location": "candidate_proof.md §5 Theorem 8, step 5 notation",
      "issue": "Writes {q_{2m+1}: m >= 1}; the sparse family has m >= 2."
    },
    {
      "location": "candidate_proof.md §3 Theorem 4",
      "issue": "A correct repair needs a tail version of the SL_h2 growth lemma: if a tail q_n recurrence holds for m >= m0, then any nonzero initial pair leads to moments that grow faster than the L^2 bound; this must be stated and proved."
    },
    {
      "location": "candidate_proof.md §6 (s=3)",
      "issue": "The 'infinite run grows linearly' premise is not defined/proved for the H^1 descent. The |M_k| <= C sqrt(k) bound is proved, but the inadmissibility conclusion needs a correct tail-recurrence argument."
    },
    {
      "location": "obligation_graph.md",
      "issue": "Theorem 4 dependency is listed as 'Lemma 2'; the actual dependency should be Corollary 2 / Lemma 3."
    },
    {
      "location": "reproducibility/O1pLD_L2_Scaffold.lean",
      "issue": "Scaffold statements are placeholders 'True' with sorry; no Lean verification was performed. This does not affect the informal audit, but the scaffold must not be counted as verification."
    }
  ],
  "repair_hints": "1) Rewrite Lemma 1 with the explicit even/odd substitution to Lebesgue L^2 before applying Müntz-Szász. 2) Delete every use of DensBC O1 run decomposition in the L^2/H^1 descent. Use the actual three-term q_n recurrences and a tail version of the existing growth lemma. 3) Re-prove Theorem 4 by showing the tail recurrences force both initial values of each parity to zero, hence all moments zero. 4) Fix Theorem 8's odd-density step to use the SL_h2 odd growth lemma, and change m>=1 to m>=2. 5) For s=3 either prove a precise tail-recurrence inadmissibility result or downgrade the infinite-run claim to EVIDENCE/plausible.",
  "covered_scope": "Definitions from prior left-definite runs; q_n and μ_4 exact formulas; the parity decomposition; the H^1 moment bound from SL_h3; the exact sympy output for μ_4; the Lean scaffold status; statement fidelity to L1-L6 and DensBC O1.",
  "residual_risk": "The repaired tail growth lemma for arbitrary tail initial data was not fully re-derived in this audit (only the SL_h2 base-case growth lemma was checked). No Lean proof was run. No new literature search on weighted Müntz-Szász was performed beyond a quick check that the standard theorem is Lebesgue-based. The H^1 finite-run question remains open."
}
```

## Registration decision

**Do not register the listed STRICT theorems as strict partial results in the
current state of the candidate proof.**  The run is a valuable partial result,
but two of its main STRICT proofs (cofinite-N density and the μ_4 odd-density
step) rely on an incorrect application of the DensBC O1 run algebra, and the
Müntz application needs a precise weighted-form argument.

After the repairs above are made, the following are expected to be registrable
as STRICT:

- L^2 finite-support moment rigidity (after a correct weighted Müntz proof);
- parity decomposition (already correct);
- μ_4 non-density example (after replacing the linear-growth argument by the
  SL_h2 odd growth lemma and fixing the m≥2 index);
- cofinite-N density theorem / proper-V non-cofinite corollary (after replacing
  the run-algebra step by the tail-recurrence/growth-lemma proof).

The H^1 infinite-run claim should be either proved using the actual tail
recurrence or explicitly labeled as not-yet-strict.  The H^1 finite-run
realizability question remains open.
