# Research ledger

Run: R-20260822T000000Z-a6-reuse
All times approximate UTC; the environment did not provide a per-step timestamp.

## 2026-08-22T13:2xZ (start)

- Read `PROBLEM-A6-RATIONAL.md`, `docs/SL_third_order_recurrence_theory.tex`
  (sections 1-8), `tools/third-order-recurrence.md`, `tools/README.md`,
  `research_map.md`, `lean-proof/LEMMA_INDEX.md`.
- Read `scripts/op13_general_product_classify.py`,
  `scripts/op13_tail_check.py`, `scripts/op13_4param_reduced.py`,
  `scripts/op13_degtest.py`, `scripts/op13_degtest2.py`.
- Checked the sibling baseline run `R-20260822T000000Z-a6-baseline`.  It claims a
  root-1 no-go but has no `candidate_proof.md` or `final_report.md`; only a
  verification script and status/ledger files exist.  REUSE pre-scan recorded.

## 2026-08-22T13:26Z

- Ran `scripts/op13_degtest.py` and `scripts/op13_degtest2.py`; both timed out
  after 120s.  Recorded that direct degree-3 symbolic solve is too heavy for a
  bounded run.

## 2026-08-22T13:28Z

- Derived the exact simplified coefficients `a_1, a_2, a_3` for both parities:
  even a1 = `(c/4 + (j-1)(2j-1))/(j(j-1))`,
  a2 = `-(c + (j-1)(2j-1))(2j-3)/(4j(j-1)^2)`,
  a3 = `c(2j-5)(2j-3)/(16j(j-2)(j-1)^2)`;
  odd a1 = `(c/4 + (j-1)(2j+1))/(j(j-1))`,
  a2 = `-(c + (j-1)(2j+1))(2j-1)/(4j(j-1)^2)`,
  a3 = `c(2j-3)(2j-1)/(16j(j-2)(j-1)^2)`.
- Built a formal power-series framework with `t = 1/j` and wrote an exploratory
  script to expand the fixed-point residual (see `/tmp/asym_series.py`).
- Observed the asymptotic equations: for the free branches the first
  non-trivial relation leaves `x_2` free and determines later coefficients;
  this matches the baseline route A idea.

## 2026-08-22T13:30Z

- Ran the baseline exact script
  `R-20260822T000000Z-a6-baseline/reproducibility/verify_asymptotic_no_go.py`.
  Output: `f1 = -2` for both free branches and `f1 = 0` for both rigid branches.
- Noticed that the baseline's proof file is missing, so it could not be used as
  a verified result.

## 2026-08-22T13:31Z

- Derived the exact diagonal-coefficient formula by differentiating the residual
  with respect to `x_m`:
  - even: `D_m = 2u - (m-1)`
  - odd:  `D_m = 2u - (m+1)`
- Verified symbolically for `m = 2..8` (both parities, all allowed `u`), and
  confirmed that `x_(m+1)` does not appear at the same order.
- This gives the formal uniqueness proof: for free branches `x_2` is the only
  free asymptotic coefficient and all higher coefficients are uniquely
  determined; for rigid branches all higher coefficients vanish.
- Compared with the known `E^(tau)` families and confirmed their expansions
  realize exactly the possible `x_2` values.

## 2026-08-22T13:32Z

- Wrote run artifacts:
  - `problem_contract.md`
  - `status_and_literature.md`
  - `approach_registry.md`
  - `research_ledger.md`
  - `candidate_proof.md`
  - `escalation_ladder.md`
  - `performance_log.md`
  - `final_report.md`
  - `reproducibility/verify_diagonal_coefficient.py`
- Ran `reproducibility/verify_diagonal_coefficient.py`; all diagonal-coefficient
  checks PASS and the known-family expansions were printed.

## Adversarial self-audit (single-agent fallback)

Per the skill, an independent verifier is normally used.  Since no subagents
are allowed in this run, I performed a deliberate adversarial pass on the
candidate proof:

- Checked the diagonal-coefficient formula for dependence on lower-order
  terms: the derivative is taken with respect to `x_m` and the other factors at
  order `t^(m+1)` only use their first-order base, so lower `x_k` do not affect
  the `D_m` formula. PASS.
- Checked that `x_(m+1)` cancels at the same order (verified symbolically to
  m=8 and by the leading-cancellation count in Lemma 1). PASS.
- Checked the induction measure: at each order `t^(m+1)`, `x_m` appears with
  non-zero coefficient and no higher unknown appears. PASS.
- Checked the rational-injection step: two rational functions with identical
  Laurent expansion at infinity are equal. PASS.
- Checked boundary cases: rigid branches, degenerate `tau`, reduced-degree
  interpretation. PASS.
- Remaining non-obvious dependency: Theorem 6.1 (allowed `u`) is used as a
  known STRICT result, not reproved. This is a dependency but not a gap.
- Verdict: `PASS` for the root-1 theorem as scoped.  The root-0/minimal branch
  is explicitly outside the theorem and remains open.

## Decisions

- Route A (asymptotic uniqueness + rational injection) selected and completed for
  the root-1 branch.
- Route B (Petkovsek/hypergeometric theory) not pursued: heavy for a bounded run.
- Route C (direct polynomial degree comparison) not pursued: the asymptotic
  route is cleaner.
- Root-0/minimal branch left open, with exact gap recorded.

## Failed or blocked routes

- Direct symbolic solve of degree-3 rational systems timed out (routes E).
  Not needed for the final theorem.
- Baseline run had no proof artifact; its claimed result could not be used as a
  certified proof (REUSE_MISS).
- Root-0 non-rationality remains a numerical + formal-uniqueness result rather
  than a complete theorem.
