# Candidate proof: root-1 high-degree rational product solutions do not exist

Status of the theorem below: **STRICT** (exact symbolic argument, no numerical
steps). The overall run status is `RIGOROUS_PARTIAL_RESULT`, because the
root-0 branch remains open.

## Notation

Fix `p = e` (even) or `p = o` (odd) and `c > 0`. Write

```
a_1(j), a_2(j), a_3(j)
```

for the explicit rational coefficients in
`docs/SL_third_order_recurrence_theory.tex`, section 2 (the formulas reproduced
in `research_ledger.md`). Define the ratio map

```
F_j(x,y) = a_1(j) + a_2(j)/x + a_3(j)/(x y).
```

A product solution `E_j = prod_{k=1}^j e_k`, `E_0=1`, solves the z-recurrence
for `j >= 3` iff

```
e_j = F_j(e_{j-1}, e_{j-2}),   j >= 3.          (FP)
```

For a rational `e_j` with `e_j -> 1`, write its Laurent expansion at
infinity as

```
e_j = 1 + A_1/j + A_2/j^2 + A_3/j^3 + ...,    A_1 = u, A_2 = v.
```

## Lemma 1 (asymptotic classification)

Substitute `j = 1/t`, `e_j = 1 + A_1 t + A_2 t^2 + ...` into
`F - e = 0` and expand in `t`. The first nonzero condition is at `t^2`:

```
even: -(2u-1)(2u+1)/4 = 0,
odd : -(2u-3)(2u-1)/4 = 0.
```

Hence

```
u in {-1/2, 1/2}  (even),      u in {1/2, 3/2}  (odd).
```

The branch `u = -1/2` (even) or `u = 1/2` (odd) is the **rigid branch**; the
branch `u = 1/2` (even) or `u = 3/2` (odd) is the **free branch**.

## Lemma 2 (triangularity of the asymptotic system)

Let `B_j` be an exact rational trajectory of `(FP)` with `B_j -> 1`, and write

```
F_x = ∂F/∂x = -a_2(j)/x^2 - a_3(j)/(x^2 y)
```

evaluated at `(x,y) = (B_{j-1}, B_{j-2})`. Let `f_1` be the coefficient of
`t = 1/j` in the expansion of `F_x`.

Consider a formal expansion `e_j = 1 + sum A_k j^{-k}`. In the residual
`R = F - e`, the coefficient of `t^m` (i.e., of `j^{-m}`) is affine in
`A_{m-1}` with coefficient

```
(m-1) + f_1.
```

**Proof sketch of the slope.** Differentiate the coefficient of `t^m` in
`R` with respect to `A_{m-1}`. The term `e_j` contributes only `t^{m-1}`,
hence nothing to `t^m`. From `F`, the contribution is

```
F_x * (j-1)^{-(m-1)} + F_y * (j-2)^{-(m-1)},
```

where `F_y = -a_3/(x y^2)`. Since `a_3(j) = O(j^{-2})` and hence
`F_y = O(t^2)`, the second term does not contribute to `t^m` for `m >= 3`.
In `t`, `(j-1)^{-(m-1)} = (t/(1-t))^{m-1} = t^{m-1}(1+(m-1)t+O(t^2))`.
With `F_x = 1 + f_1 t + O(t^2)`, the `t^m` coefficient is exactly
`(m-1) + f_1`. The `A_m` term cancels between `e` and the leading part of
`F`, so it does not appear in the `t^m` equation. This proves the slope.

## Lemma 3 (values of `f_1`)

A direct exact expansion of `a_2(j)` gives

```
even: a_2(j) = -1 + 1/j + O(j^{-2}),
odd : a_2(j) = -1 - 1/j + O(j^{-2}).
```

Write `a_2 = -1 + epsilon/j + O(j^{-2})`, so `epsilon = +1` (even) and
`epsilon = -1` (odd). For a base trajectory `B_j = 1 + u/j + O(j^{-2})`,
one has

```
F_x = -a_2/B_{j-1}^2 - a_3/(B_{j-1}^2 B_{j-2})
    = 1 - (epsilon + 2u)/j + O(j^{-2}).
```

Therefore `f_1 = -(epsilon+2u)`.

- Free branch: even `u=1/2`, odd `u=3/2`, so `epsilon+2u = 2`, hence
  `f_1 = -2`.
- Rigid branch: even `u=-1/2`, odd `u=1/2`, so `epsilon+2u = 0`, hence
  `f_1 = 0`.

These values were also verified by the exact symbolic script
`reproducibility/verify_asymptotic_no_go.py`.

## Corollary (formal uniqueness)

- **Rigid branch.** At `m=3`, the slope is `(3-1)+0 = 2`, so `A_2 = 0`.
  For `m >= 4`, the slope is `m-1 >= 3`, so induction gives
  `A_3 = A_4 = ... = 0`. Thus the formal expansion is exactly
  `1 + u/j` with no further terms:
  even `1 - 1/(2j)`, odd `1 + 1/(2j)`.

- **Free branch.** At `m=3`, the slope is `(3-1)-2 = 0`, so `A_2 = v` is a
  free parameter. For `m >= 4`, the slope is `m-3 >= 1`, so `A_{m-1}` is
  uniquely determined by `(A_1,...,A_{m-2})`. Hence for every `v` there is
  exactly one formal power series solution, and its coefficients are:
  ```
  even: A_1=1/2, A_2=v, A_3=v^2+v/2, A_4=v^3+v^2+v/4, ...
  odd : A_1=3/2, A_2=v, A_3=v^2-v/2, A_4=v^3-v^2+v/4, ...
  ```

## Theorem (root-1 high-degree no-go)

For both parities and every `c > 0`, let `E_j = prod_{k=1}^j e_k` be a
product solution of the z-recurrence. Assume that `e_j` is a rational function
of `j` and that `e_j -> 1`. Then `e_j` has degree at most 2. In particular,
there is no rational product ratio of degree `> 2` on the root-1 branch.

**Proof.** Let `u = lim j(e_j-1)` and `v = A_2`. By Lemma 1, `u` is one of
the two allowed values.

If `u` is rigid, Corollary formal uniqueness shows that the Laurent expansion
of `e_j` at infinity is identical to `E^-_j`:
`1 - 1/(2j)` (even) or `1 + 1/(2j)` (odd). Both `e_j` and the rational
function `E^-_j` are rational with the same expansion at infinity, so
`e_j = E^-_j`; the degree is 1.

If `u` is free, define the known rational function

```
even: R_v(j) = (1 - 1/(2j)) * (j + tau + 1)/(j + tau),  tau = -v - 1/2,
odd : R_v(j) = (1 + 1/(2j)) * (j + tau + 1)/(j + tau),  tau = -v + 1/2.
```

This is the `E^(tau)` ratio of the already-proved degree-`<=2` classification
(source document Theorem 6.3); in particular it is an exact solution of `(FP)`
and has the same `u` and `A_2 = v`. By Corollary formal uniqueness, no other
formal solution with these first two coefficients exists. Therefore the
Laurent expansion of `e_j` at infinity equals that of `R_v`. Since both are
rational functions, they are identically equal:

```
e_j = R_v(j).
```

The right-hand side is a rational function of degree at most 2. Hence any
rational root-1 product ratio is one of the known degree-`<=2` ratios, and no
higher-degree rational product ratio exists on the root-1 branch. `QED`

## Remarks and exact scope

- The proof is exact and symbolic; the only computational input is the direct
  expansion of `a_i` and `F_x`, recorded in the ledger and the verification
  script.
- The theorem applies to `c > 0` arbitrary; no numerical specialisation was
  used.
- The theorem does **not** cover the root-0/minimal branch (`e_j -> 0`). That
  branch remains open; the current evidence is high-precision numerical fit
  plus a formal-uniqueness argument, not a completed rational-function
  exclusion.
