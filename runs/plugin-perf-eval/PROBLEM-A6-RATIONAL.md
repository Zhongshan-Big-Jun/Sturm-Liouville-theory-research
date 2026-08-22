# Performance benchmark problem: A6 higher-degree rational product solutions

Project: Sturm-Liouville spectral optimization (MRP-20260731-BVE-SL)
Local root: F:\LaTeX\BVE research

## Why this problem

This is an unsolved sub-problem in the project's third-order recurrence theory
(problem node A6, status PARTIAL). It is small, self-contained, has an existing
tool library and scripts, and is suitable for a bounded two-agent performance
experiment.

## The open problem

Source of the open item: `docs/SL_third_order_recurrence_theory.tex`, section 8,
item "Higher-degree rational function exclusion" / "高次有理函数排除".

The recurrence (after z-scaling) is

    z_j = a_1(j) z_{j-1} + a_2(j) z_{j-2} + a_3(j) z_{j-3},   j >= 3,

with Poincare limits a_1 -> 2, a_2 -> -1, a_3 -> 0. There are even and odd
versions with explicit rational coefficients shown in the source document.
A product solution has the form

    E_j = prod_{k=1..j} e_k,   e_j = E_j / E_{j-1}.

The known complete classification (Theorem full in the document) covers:

- the two-parameter family e_j = 1 + beta/(k + gamma), and
- all rational ratios whose 4-parameter reduction has degree <= 2.

The open target is:

- classify or exclude product solutions whose ratio e_j is a rational function
  of j of higher degree (numerator/denominator degree > 2), or
- prove a no-go theorem with an exact algebraic mechanism, or
- find a new higher-degree family / counterexample.

Work on both the even and odd recurrences. Honest partial progress is a
valuable result.

## Required project context to read

- `docs/SL_third_order_recurrence_theory.tex`
- `tools/third-order-recurrence.md`
- `tools/README.md` (tool library index)
- `research_map.md` (project-wide map)
- `scripts/d4_third_order_theory.py`, `scripts/d4_verify2.py`,
  `scripts/d4_verify3.py`, `scripts/d4_verify4.py`
- `scripts/op13_general_product_classify.py`, `scripts/op13_tail_check.py`
  (if present)

## Output requirements for each run

Write under the run root at least:

- `problem_contract.md`
- `status_and_literature.md`
- `approach_registry.md`
- `research_ledger.md`
- `candidate_proof.md` (if any mathematical result is obtained)
- `escalation_ladder.md`
- `performance_log.md`
- `final_report.md` (one-line status label plus exact remaining gaps)

Status labels must follow the rigorous-open-math-research output protocol.
Numerical evidence must never be presented as a proof.
