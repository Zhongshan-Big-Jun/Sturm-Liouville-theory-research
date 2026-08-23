# Re-Audit Report — R-20260823T050000Z-leftdef-o1pld-reaudit

Target run: `R-20260823T030000Z-leftdef-o1pld`
Previous audit: `R-20260823T040000Z-leftdef-o1pld-audit` (REPAIRABLE_GAP)
Auditor: independent adversarial re-auditor (no subagents spawned)
Date/status: 2026-08-23

## Verdict

**PASS**

The repaired STRICT claims are mathematically sound and may be registered as
STRICT partial results. The downgrades are accurately labeled in
`candidate_proof.md`, `final_report.md`, `obligation_graph.md`, and
`tools/leftdef-o1pld-l2-structural.md`. No FATAL_GAP or REPAIRABLE_GAP remains
in the STRICT claims themselves.

A separate, non-blocking documentation inconsistency is noted below: some
non-target run artifacts still retain the pre-repair SUCCEEDED/MET claims for
the cofinite-N theorem.

## Scope covered

- Lemma 1 / Corollary 2 (L^2 finite-support moment rigidity)
- Lemma 3 (Cauchy–Schwarz moment bound and linear-growth non-realizability)
- Theorem 7 / Corollary 8 (parity decomposition)
- Theorem 9 (μ_4 concrete non-density example)
- Accuracy of the downgrades: Claim 4, Theorem 5, Corollary 6, and H^1
  infinite-run inadmissibility

## Claim-by-claim audit

### 1. Lemma 1 / Corollary 2 — STRICT: PASS

The repaired proof now applies the L^p Müntz–Szász theorem on Lebesgue
measure on `(0,1)`, and the even/odd weighted substitutions are correct at the
level needed for the argument.

- Even part: `h(y) = y^{-1/4} f_e(√y) ∈ L^2(0,1)` and
  `∫_{-1}^1 f_e(x)x^{2m} dx = ∫_0^1 h(y)y^{m-1/4} dy`.
- Odd part: `t(y) = y^{1/4} h_o(y) ∈ L^2(0,1)` and
  `∫_{-1}^1 f_o(x)x^{2m+1} dx = ∫_0^1 t(y)y^{m+1/4} dy`.
- The exponent sets
  `{m-1/4 : 2m ∉ F, m ≥ 1}` and `{m+1/4 : 2m+1 ∉ F, m ≥ 0}`
  both have divergent reciprocal sums, even after deleting finitely many
  terms. This satisfies the Müntz–Szász density hypothesis (up to the standard
  equivalent asymptotic formulation of the condition).
- The m=0 even case is not a problem: if the constant monomial is kept, the
  m≥1 exponents alone already form a dense family, so the extra constant
  condition is redundant; if it is deleted, the remaining family is still
  dense.

Minor presentation issues, not gaps:

- The proof of Lemma 1 as written does not explicitly begin with
  "let f be orthogonal to the kept monomials"; the intended argument is
  recoverable from Corollary 2 and is standard.
- In the odd part, the display
  `∫_{-1}^1 |f_o|^2 = (1/2)∫_0^1 |h_o|^2 y^{1/2} dy`
  has an extra factor `1/2`; the correct value is
  `∫_0^1 |h_o|^2 y^{1/2} dy = ∫_0^1 |t|^2 dy`.
  This typo does not affect the conclusion `t ∈ L^2(0,1)` or any later step.

### 2. Lemma 3 — STRICT: PASS

The statement proved is exactly the Cauchy–Schwarz bound
`|M_k| ≤ ||f||_2 √(2/(2k+1))`, together with the true general consequence
that a moment sequence growing linearly along one parity cannot be realized
by an L^2 function. The REMARK in the repaired candidate correctly states that
this fact does **not** by itself identify the obstruction in the s=2 descent,
and all uses of the DensBC O1 two-term run algebra in the L^2/H^1 descent have
been removed. No overclaimed run-inadmissibility remains in the STRICT claim.

### 3. Theorem 7 / Corollary 8 — STRICT: PASS

The proof is the standard Hilbert-space fact that for orthogonal subspaces
`A` and `B`, `closure(A+B) = closure(A) ⊕ closure(B)`. Since even and odd
L^2 spaces are orthogonal and every `q_n` is either even or odd, the parity
decomposition is correct. Corollary 8 is a valid consequence for
parity-invariant `W`.

### 4. Theorem 9 — STRICT: PASS

The concrete non-density example is now correctly based on the actual three-term
q_n recurrences and the SL_h2 odd growth lemma.

- `N = {1} ∪ {2m+1 : m ≥ 2}` is computed correctly:
  - `q_0 = c` gives `μ_4(q_0) = 2c/5 ≠ 0`;
  - every odd `q_n` is in `ker μ_4` by parity;
  - the exact formula
    `μ_4(q_{2m}) = -2(8cm^2+10cm+3c+32m^3+48m^2-80m) / ((m-1)(2m+1)(2m+3)(2m+5))`
    is negative for `c>0`, `m≥2` (verified with the shipped exact-arithmetic
    script; the numerator bracket factors as
    `16m(2m+5)(m-1) + c(8m^2+10m+3) > 0` for `m≥2`).
- The odd-density step is now correct: `q_1` forces `M_1=0`, the odd
  recurrences `m≥2` give `M_{2m+1} = M_3 u_m`, and the SL_h2 odd growth lemma
  gives `u_m ≥ (4/c)^{m-1} m!`. A nonzero `M_3` contradicts the L^2
  Cauchy–Schwarz bound, so all odd moments vanish and the odd sparse family is
  dense in the odd subspace.
- The index set is correctly `m≥2`; the earlier `m≥1` typo is gone.
- The conclusion that the closure is the odd subspace and is strictly smaller
  than `V = ker L` follows from the isometry `K_c: H^2 → L^2` and the fact
  that the even fibre in `V` is a nontrivial infinite-dimensional hyperplane.
  This last point is stated tersely but is immediate from the isometry and
  nonvanishing of `μ_4` on even L^2.

## Accuracy of downgrades

The requested label files are accurate:

- `candidate_proof.md`: Claim 4, Theorem 5, and Corollary 6 are labeled
  NOT-YET-STRICT; H^1 infinite-run inadmissibility is labeled
  EVIDENCE / PLAUSIBLE. The repair log documents the downgrades.
- `final_report.md`: lists Claim 4, Theorem 5, Corollary 6 under
  NOT-YET-STRICT / conditional; lists H^1 infinite-run inadmissibility under
  EVIDENCE / OPEN.
- `obligation_graph.md`: statuses match the candidate and final report.
- `tools/leftdef-o1pld-l2-structural.md`: explicitly marks tail L^2 rigidity
  and cofinite-N theorem as NOT-YET-STRICT, H^1 infinite-run as
  EVIDENCE/plausible, and H^1 finite-run as open.

## Non-blocking note: stale non-target run documents

The following run-root artifacts still contain the pre-repair status and should
be updated before the run is treated as fully synchronized:

- `problem_contract.md` lines 50–54 still mark the cofinite-N density theorem
  as `[MET]`.
- `approach_registry.md` route R4 still says `SUCCEEDED` for the cofinite-N
  density theorem.
- `research_ledger.md` entry 6 still says "Proved cofinite-N density theorem".

These are outside the three-file label scope and do not affect the soundness
of the STRICT claims, but they should be corrected to avoid accidental
registration of a NOT-YET-STRICT claim.

## Structured conclusion

```json
{
  "verdict": "PASS",
  "strict_claims": {
    "L2_finite_support_moment_rigidity": "STRICT, sound",
    "Cauchy_Schwarz_bound": "STRICT, sound and not overclaimed",
    "parity_decomposition": "STRICT, sound",
    "mu4_non_density": "STRICT, sound"
  },
  "downgrades": {
    "tail_L2_rigidity": "NOT-YET-STRICT, correctly labeled",
    "cofinite_N_density": "NOT-YET-STRICT, correctly labeled",
    "proper_V_non_cofinite": "NOT-YET-STRICT, correctly labeled",
    "H1_infinite_run": "EVIDENCE / PLAUSIBLE, correctly labeled"
  },
  "remaining_math_gap_in_strict_claims": "none",
  "non_blocking_doc_issue": "stale problem_contract.md / approach_registry.md / research_ledger.md still carry old SUCCEEDED/MET labels"
}
```

## Registration decision

The four repaired STRICT claims may be registered as STRICT partial results
for the s=2 L^2 descent. Before treating the entire run record as fully
synchronized, update the stale non-target run artifacts noted above.
