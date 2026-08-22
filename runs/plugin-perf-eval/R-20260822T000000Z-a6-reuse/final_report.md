# Final report

`RIGOROUS_PARTIAL_RESULT` (root-1 higher-degree rational no-go proved; A6 remains PARTIAL due to root-0/minimal branch).

## Summary

This run proves a new STRICT sub-result for project node A6: on the root-1
branch (`e_j -> 1`), every rational product ratio `e_j = E_j/E_{j-1}` of the
z-scaled third-order recurrence has reduced degree at most 2, for both the
even and odd recurrences and for all `c > 0`.  It is therefore exactly one of
the known `E^(tau)` or `E^-` rational ratios from the source document.  In
particular, no higher-degree (degree > 2) rational product solution exists on
the root-1 branch.

## Proof mechanism

The new exact algebraic mechanism is the diagonal-coefficient lemma for the
formal fixed-point identity in `t = 1/j`:

- even: the coefficient of `x_m` in the `t^(m+1)` residual is `2u - (m-1)`;
- odd: the coefficient of `x_m` in the `t^(m+1)` residual is `2u - (m+1)`.

The `x_(m+1)` coefficient cancels at the same order.  For the four allowed
values of `u` from Theorem 6.1, these diagonal coefficients are nonzero for
every `m >= 3` (and also `m = 2` on the rigid branches).  Hence:

- rigid branches force all higher asymptotic coefficients to vanish, so the
  solution is `E^-`;
- free branches leave exactly one free coefficient `x_2`, and every higher
  coefficient is uniquely determined by `u` and `x_2`.

The known `E^(tau)` rational families realize exactly these expansions.  Since
a rational function is uniquely determined by its Laurent expansion at
infinity, any rational solution must coincide with the known degree-`<= 2`
family.  This closes the root-1 higher-degree gap.

## Verification performed

- Exact symbolic verification of the diagonal-coefficient formula for
  `m = 2..8`, both parities, by direct differentiation: all PASS.
- Confirmation that the next unknown `x_(m+1)` cancels at the same order.
- Re-run of the sibling baseline exact script
  `R-20260822T000000Z-a6-baseline/reproducibility/verify_asymptotic_no_go.py`
  (output matches its own `f1` claims).
- No numerical evidence is used as proof; all verification is exact symbolic.

## Remaining gaps

1. The root-0 / minimal-solution branch (`e_j -> 0`) is not covered by a full
   theorem.  The source's evidence there is high-precision numerical fitting
   plus formal uniqueness of the asymptotic expansion; it is not a complete
   rational-injection proof.
2. The asymptotic classification Theorem 6.1 (allowed `u`) is used as a known
   STRICT result from the project source, not reproved in this run.
3. An independent Petkovsek / hypergeometric-solution cross-check was triaged
   but not executed; it could serve as an alternate verification.

## Failed and blocked routes

- Direct degree-3 symbolic solve timed out; not needed for the final result.
- The sibling baseline run lacked `candidate_proof.md` and `final_report.md`,
  so its claimed root-1 no-go could not be used as a certified proof
  (REUSE_MISS).

## Novelty status

`DIRECT_COROLLARY_OF_KNOWN_RESULT` plus one new local lemma: the degree-2
classification was already known; the novelty is the exact formal
diagonal-coefficient lemma that excludes all higher degrees on the root-1
branch.  No external literature novelty is claimed.

## Artifacts

- `problem_contract.md`
- `status_and_literature.md`
- `approach_registry.md`
- `research_ledger.md`
- `candidate_proof.md`
- `escalation_ladder.md`
- `performance_log.md`
- `final_report.md`
- `reproducibility/verify_diagonal_coefficient.py`

## Confidence by axis

- Semantic fidelity: high (contract narrowed explicitly to root-1 branch and
  stated against the source).
- Mathematical correctness: high (linear diagonal computation is elementary
  and verified symbolically).
- Completeness: partial (root-1 only; root-0 remains open).
- Novelty: small (local lemma; project-level gap closure).
- Reproducibility: high (exact sympy script included and run).
