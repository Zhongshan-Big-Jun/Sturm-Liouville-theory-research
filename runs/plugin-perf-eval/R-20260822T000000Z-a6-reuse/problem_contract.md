# Problem contract

Run: R-20260822T000000Z-a6-reuse (REUSE-GATE variant)
Problem node: A6 (third-order recurrence theory), open sub-problem "higher-degree
rational product solutions".

## Objects and definitions

For fixed `c > 0` and parity `p in {e, o}`, let the z-scaled third-order
recurrence be

    z_j = a_1(j) z_{j-1} + a_2(j) z_{j-2} + a_3(j) z_{j-3},   j >= 3,

with exact rational coefficients `a_i(j)` from
`docs/SL_third_order_recurrence_theory.tex` (even and odd variants).  The
limits are `(a_1, a_2, a_3) -> (2, -1, 0)`, so the characteristic polynomial
is `rho^3 - 2 rho^2 + rho = rho (rho-1)^2`.

A product solution is `E_j = prod_{k=1}^j e_k`, `E_0 = 1`, with ratio
`e_j = E_j / E_{j-1}`.  By Lemma 3.1 of the source, `E` solves the recurrence
for `j >= 3` iff

    e_j = a_1(j) + a_2(j)/e_{j-1} + a_3(j)/(e_{j-1} e_{j-2}),   j >= 3.

## Hypotheses

- `p in {e, o}` is fixed.
- `c > 0` is fixed.
- `e_j = P(j)/Q(j)` is a rational function of `j`, in reduced terms, with
  `deg P = deg Q = d` and `e_j -> 1` as `j -> infinity` (the root-1 / free or
  rigid asymptotic branch).  The problem only concerns rational ratios on this
  branch; the root-0 (minimal-solution) branch is recorded as a separate gap.

## Target conclusion

Prove that every such rational ratio has reduced degree `d <= 2`, and that the
possibilities are exactly the known families in Theorem 6.3 of the source:
`E^(tau)` plus the rigid solution `E^-`.  Equivalently, no rational product
ratio with reduced numerator/denominator degree strictly greater than 2 exists
on the root-1 branch.

## Quantifiers and dependency of constants

- The conclusion is uniform in `c > 0` and in parity `e` or `o`.
- The parameter `tau` is allowed to depend on `c` and on the branch; it is not
  expected to be universal.
- No other free constants are introduced.

## Equivalent formulations

The following are equivalent and used in the proof:

1. Product-solution form: `E_j = prod e_k` solves the linear recurrence.
2. Ratio fixed-point form: `e_j = F_j(e_{j-1}, e_{j-2})`.
3. Formal asymptotic form: the Laurent expansion of `e_j` in powers of `1/j`
   satisfies the fixed-point identity to all orders.

## Boundary and degenerate cases

- `j = 1, 2`: the product-solution identity is only required for `j >= 3`,
  so early terms do not enter the asymptotic classification.
- `tau = -1` causes a pole in the naive `E^(tau)` notation; it corresponds to
  the `E^+`/other limiting representative in the known family and is handled by
  the exact rational-ratio classification already in the source.
- Degenerate degree reductions (`d < 2`, e.g. `d = 1` with cancellation) are
  included in the known family; our theorem only claims degree `<= 2` after
  reducing common factors.
- Rigid branch (`u = -1/2` even, `u = 1/2` odd): the only rational solution is
  `E^-`, already known.

## Permitted outcomes

- affirmative proof: `RIGOROUS_PARTIAL_RESULT` (root-1 higher-degree no-go).
- negative proof / counterexample: not obtained for root-1.
- independence or inconsistency: not applicable.
- The root-0/minimal-solution branch may remain open; a rational `e_j -> 0`
  solution is not classified here.

## Completion criteria

The run is complete for its stated scope when:

1. The diagonal-coefficient lemma is stated with an exact proof.
2. It is shown that the formal asymptotic expansion is uniquely determined by
   `u` and (for free branches) by `x_2`.
3. It is shown that the known degree-2 rational families realize those exact
   asymptotic expansions.
4. It is concluded that any rational root-1 solution must be one of them.

## Results that do not count as completion

- A finite symbolic check for `d <= 8` or `m <= 10` does not by itself prove the
  general no-go; it is only reinforcement.
- Numerical fitting of the minimal branch is not a proof of non-rationality.
- Repeating the existing degree-2 classification is not progress on the open
  higher-degree gap unless it also excludes degree > 2.

## Tool, citation, and search constraints

- Work directly; no subagents.
- No external literature beyond the project document was required.
- Symbolic computations use sympy; all computations used here are exact
  rational/symbolic, not floating point.

## Ambiguities or competing interpretations

- "Degree > 2" is interpreted as the reduced degree of the rational ratio
  `e_j` after cancellation of common factors.  A non-reduced representation can
  have higher formal degree while simplifying to the known degree-2 family.
- "Both even and odd recurrences" is covered by the theorem.

## Contract audit

This contract was reviewed against `PROBLEM-A6-RATIONAL.md` and
`docs/SL_third_order_recurrence_theory.tex` section 6.  The scope is narrowed
to the root-1 branch because the source explicitly separates the root-0/minimal
branch and only the root-1 branch has a known degree-2 classification.
