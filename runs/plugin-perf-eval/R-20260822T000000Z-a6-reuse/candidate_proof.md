# Candidate proof: no rational ratio of degree > 2 on the root-1 branch

Status: RIGOROUS_PARTIAL_RESULT (a new STRICT sub-result for A6; not a solution
of the whole A6 node because the root-0/minimal branch remains open).

## Statement

Let `p in {e,o}` and `c > 0`.  Let `E_j = prod_{k=1}^j e_k` be a product
solution of the z-scaled third-order recurrence, with `e_j` a rational function
of `j` and `e_j -> 1` as `j -> infinity`.  Then the reduced degree of `e_j`
(numerator and denominator) is at most 2, and `e_j` is one of the known
rational ratios from Theorem 6.3 of
`docs/SL_third_order_recurrence_theory.tex`:
the `E^(tau)` family plus the rigid solution `E^-`.

Equivalently, no higher-degree (degree greater than 2) rational product ratio
exists on the root-1 branch, for either parity.

## Notation and setup

Write `j = 1/t` and, for a coefficient function `a_i(j)`, set
`A_i(t) = a_i(1/t)`.  For a formal solution with `e_j -> 1`, write

    E(t) = e_{1/t} = 1 + u t + x_2 t^2 + x_3 t^3 + ...,

where `u = lim_j j(e_j - 1)`.

The fixed-point identity is

    E(t) E(t/(1-t)) E(t/(1-2t))
      = A_1(t) E(t/(1-t)) E(t/(1-2t))
        + A_2(t) E(t/(1-2t))
        + A_3(t).

Define the residual

    G(t) = E(t) E(t/(1-t)) E(t/(1-2t))
           - A_1(t) E(t/(1-t)) E(t/(1-2t))
           - A_2(t) E(t/(1-2t))
           - A_3(t).

The identity is `G(t) = 0` as a formal power series.

The exact coefficient functions have the following expansions in `t`:

Even (`p = e`):

    A_1(t) = 2 - t + (c/4) t^2 + O(t^3)
    A_2(t) = -1 + t + (1/4 - c/2) t^2 + O(t^3)
    A_3(t) = (c/4) t^2 + O(t^3)

Odd (`p = o`):

    A_1(t) = 2 + t + (c/4) t^2 + O(t^3)
    A_2(t) = -1 - t + (-3/4 - c/2) t^2 + O(t^3)
    A_3(t) = (c/4) t^2 + O(t^3)

These are obtained by direct simplification of the formulas in the source
document (they are used in the exact symbolic script in
`reproducibility/verify_diagonal_coefficient.py`).

## Lemma 1 (leading cancellation of the next unknown)

In the coefficient of `t^(m+1)` in `G(t)`, the unknown `x_(m+1)` cancels
identically; its coefficient is zero.

Proof.  At order `t^(m+1)`, each factor contributes the coefficient `x_(m+1)`
only through the leading power of its shift.  The linear coefficient from the
positive product `E E1 E2` is `+1` for `x_(m+1)` appearing in `E`, `+1` for it
appearing in `E1`, and `+1` for it appearing in `E2`.  The negative term
`-A_1 E1 E2` contributes `-A_1(infinity) = -2` for each of `E1` and `E2`.  The
negative term `-A_2 E2` contributes `-A_2(infinity) = +1` for `E2`.  The total
is `1 + 1 + 1 - 2 - 2 + 1 = 0`.  QED.

## Lemma 2 (diagonal coefficient)

For every `m >= 2`, the coefficient of `x_m` in the coefficient of `t^(m+1)`
of `G(t)` is

    even: D_m = 2u - (m-1)
    odd:  D_m = 2u - (m+1)

and it is independent of all `x_k`.

Proof.  Differentiate `G` with respect to `x_m`.  Using the chain rule and the
first-order parts

    E(t) = 1 + u t + ...,   E(t/(1-t)) = 1 + u t + ...,
    E(t/(1-2t)) = 1 + u t + ...,
    (t/(1-t))^m = t^m (1 + m t + ...),
    (t/(1-2t))^m = t^m (1 + 2m t + ...),

the coefficient of `t^(m+1)` in `dG/dx_m` has the following contributions.

The three positive product terms give

    t^m E1 E2                       ->  2u
    E (t/(1-t))^m E2                ->  2u + m
    E E1 (t/(1-2t))^m               ->  2u + 2m

so the positive sum is `6u + 3m`.

Write `A_1(t) = alpha0 + alpha1 t + O(t^2)` and
`A_2(t) = beta0 + beta1 t + O(t^2)`, with `alpha0 = 2`, `beta0 = -1`.
The negative term `-A_1(... )` contributes

    -[2(m+u) + alpha1] - [2(u+2m) + alpha1]
      = -6m - 4u - 2 alpha1.

The negative term `-A_2(t/(1-2t))^m` contributes

    -beta0 * 2m - beta1 = 2m - beta1

because `-beta0 = 1`.

Adding,

    D_m = (6u + 3m) + (-6m - 4u - 2 alpha1) + (2m - beta1)
        = 2u - m - 2 alpha1 - beta1.

Finally, from the expansions above, the first-order coefficients are

    even: alpha1 = -1, beta1 = 1, so D_m = 2u - m + 1 = 2u - (m-1);
    odd:  alpha1 = +1, beta1 = -1, so D_m = 2u - m - 1 = 2u - (m+1).

This is independent of `x_k` for all `k`, of `c`, and of the lower-order
coefficients.  QED.

## Theorem (root-1 high-degree no-go)

Proof.  By Theorem 6.1 of the source, `u` belongs to
`{-1/2, 1/2}` for even parity and `{1/2, 3/2}` for odd parity.

Use Lemmas 1 and 2 to solve the formal coefficient equations `G(t) = 0`
order by order.  At order `t^(m+1)`, the equation is affine linear in `x_m`
with coefficient `D_m`, and does not contain `x_(m+1)`.

Rigid branches:

- even `u = -1/2`: `D_2 = -2`, and for `m >= 3`, `D_m = -m != 0`.
- odd `u = 1/2`: `D_2 = -2`, and for `m >= 3`, `D_m = -m != 0`.

Thus `x_2 = 0`, and by induction `x_m = 0` for all `m >= 3`.  The only formal
solution is `e_j = 1 + u/j`, which is the known rigid solution `E^-`.

Free branches:

- even `u = 1/2`: `D_2 = 0`, so `x_2` is free; for `m >= 3`, `D_m = 2 - m != 0`.
- odd `u = 3/2`: `D_2 = 0`, so `x_2` is free; for `m >= 3`, `D_m = 2 - m != 0`.

Thus each `x_m` for `m >= 3` is uniquely determined by `u` and `x_2`.

To justify that `x_2` is genuinely free, not merely not determined by the
linear coefficient, substitute the allowed free `u` into the full `t^3`
coefficient of the residual. For even `u = 1/2` and odd `u = 3/2`, that
coefficient is identically zero as a polynomial in `x_2`; equivalently, the
known `E^(tau)` family below realizes every value of `x_2`, so every choice
of `x_2` gives a formal solution. Hence the free branch really has one free
parameter.

Therefore the entire formal Laurent expansion of a solution is uniquely
determined by `(u, x_2)` (or by `u` alone in the rigid case).

Now compare with the known rational families:

- Even free `u = 1/2`:  `E^(tau)` has
    `e^(tau)_j = (1 - 1/(2j))(j + tau + 1)/(j + tau)`
  and its expansion at infinity is
    `1 + (1/2)t - (tau + 1/2)t^2 + (tau^2 + tau/2)t^3 - ...`.
  Hence `x_2 = -(tau + 1/2)`.

- Odd free `u = 3/2`:  `E^(tau)` has
    `e^(tau)_j = (1 + 1/(2j))(j + tau + 1)/(j + tau)`
  and its expansion at infinity is
    `1 + (3/2)t + (1/2 - tau)t^2 + (tau^2 - tau/2)t^3 - ...`.
  Hence `x_2 = 1/2 - tau`.

Thus, for every free-branch solution with parameter `x_2`, there is a unique
`tau` so that the known rational `E^(tau)` has the same asymptotic expansion.
For the rigid branch, `E^-` has the expansion.

Let `e_j` be any rational solution on the root-1 branch.  Its Laurent
expansion at infinity is one of the expansions above.  If a rational function
and another rational function have the same Laurent expansion at infinity,
their difference is a rational function whose expansion at infinity is
identically zero, hence the difference is the zero rational function.
Therefore `e_j` is exactly one of the known rational ratios `E^(tau)` or
`E^-`.  These have reduced numerator and denominator degree at most 2
(after cancelling common factors; the generic reduced form is a ratio of two
quadratic polynomials).

Consequently, no rational product ratio on the root-1 branch has reduced
degree greater than 2.  QED

## Verification performed

- Exact symbolic computation of the coefficient expansions of `A_1, A_2, A_3`
  for both parities.
- Exact symbolic verification of the diagonal-coefficient formula
  `D_m = 2u - (m-1)` (even) and `D_m = 2u - (m+1)` (odd) for `m = 2..8`,
  by direct differentiation, both parities and all four allowed `u` values.
- Re-run of the baseline exact script
  `runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline/reproducibility/verify_asymptotic_no_go.py`
  which confirms `f1 = -2` (free) and `f1 = 0` (rigid) for its alternate
  formulation.
- The verification is symbolic; it is not treated as the proof.  The proof
  above is the derivation.

## Remaining gaps

- The root-0 / minimal-solution branch (`e_j -> 0`) is not covered.
  The source's evidence for non-rationality there is numerical plus a formal
  uniqueness argument, not a complete rational-injection theorem.
- The asymptotic classification Theorem 6.1 is used as a STRICT known result
  from the source; it is not reproved here.
- The Petkovsek / hypergeometric-solution route remains an unexecuted
  independent cross-check.
