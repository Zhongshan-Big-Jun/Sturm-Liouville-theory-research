# Problem Contract: A6 Higher-Degree Rational Product Solutions

Run: `R-20260822T000000Z-a6-baseline`
Source: `runs/plugin-perf-eval/PROBLEM-A6-RATIONAL.md`
Project node: A6 (third-order recurrence theory), status PARTIAL.

## Normalized statement

For each parity `p in {e, o}` define the z-scaled third-order recurrence

    z_j = a_1(j) z_{j-1} + a_2(j) z_{j-2} + a_3(j) z_{j-3},   j >= 3,

where `(a_1,a_2,a_3)` are the explicit rational coefficients of
`docs/SL_third_order_recurrence_theory.tex`, section 2 (even and odd variants),
with Poincare limits `(2,-1,0)`.

A **product solution** is a sequence `E_j = prod_{k=1..j} e_k`, `E_0 = 1`,
whose ratio sequence `e_j = E_j/E_{j-1}` satisfies the fixed-point identity

    e_j = a_1(j) + a_2(j)/e_{j-1} + a_3(j)/(e_{j-1} e_{j-2}),   j >= 3.

The ratio sequence is called **rational** if `e_j = P(j)/Q(j)` for polynomials
`P,Q` over the coefficient field (real/rational in `c`). Its **degree** is
`max(deg P, deg Q)` after cancelling common factors and, for the root-1 branch,
`deg P = deg Q`.

The open target is:

1. classify or exclude product solutions whose rational ratio `e_j` has degree
   greater than 2 for both parities;
2. or prove a no-go theorem with an exact algebraic/asymptotic mechanism;
3. or find a new higher-degree family / counterexample.

## Sub-contract used in this run

The known complete classification (source document) already covers:

- the two-parameter family `e_j = 1 + beta/(k + gamma)`;
- all rational ratios whose 4-parameter reduction has degree `<= 2`.

This run therefore focuses on the **root-1 branch** (`e_j -> 1`), where a
rational degree bound is absent. The root-0/minimal branch (`e_j -> 0`) is
recorded as a separate remaining gap.

## Completion criteria (for the root-1 branch)

A rigorous proof of:

> If `e_j` is a rational function of `j`, `e_j -> 1`, and `E_j` is a product
> solution of the recurrence for `j >= 3`, then `e_j` has degree at most 2.
> Equivalently, no high-degree (degree > 2) rational ratio exists on the
> root-1 branch.

The proof must be exact, not numerical. It must handle both even and odd
recurrences and all `c > 0`.

## Out of scope in this run

- Complete root-0/minimal-branch rationality exclusion (currently numerical
  evidence + uniqueness only in the source).
- Closed form of the minimal-solution constant `K(c)`.
- The non-homogeneous box-induction control problem.

## Status after run

`RIGOROUS_PARTIAL_RESULT`: root-1 higher-degree rational exclusion proved;
root-0 rational exclusion remains open.
