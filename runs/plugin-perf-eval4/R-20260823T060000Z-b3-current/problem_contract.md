# Problem contract: B3 O1/O2

Status label: `RIGOROUS_PARTIAL_RESULT` (overall run; O1/O2 remain open)

Run root: `F:\LaTeX\BVE research\runs\plugin-perf-eval4\R-20260823T060000Z-b3-current`

## Normalized problem

For `R > 1`, `n >= 1`, consider

```
-y''(x) = lambda * rho(x) y(x),  x in (0,1),
y(0) = y(1) = 0,
1 <= rho(x) <= R  a.e.
```

Let `lambda_k(rho)` be the k-th Dirichlet eigenvalue and

```
Lambda_n(rho) = lambda_{n+1}(rho) / lambda_n(rho).
```

Define `c_n(R)` as the ratio of the balanced alternating configuration

```
rho_bal = [1,R,1,...,1]   (2n+1 blocks, 2n switches),
w_1/w_2 = sqrt(R),  w_2 = 1 / ((n+1) sqrt(R) + n).
```

O1 (global extremality in the reduced finite family):
> Prove that among all `[1,R,1,...,1]` bang-bang configurations with exactly
> 2n switches (positive block widths), the supremum of `Lambda_n` is attained
> by the equal-width balanced configuration and its value is `c_n(R)`.

O2 (alternating-family maximum):
> Inside the one-parameter equal-within-type alternating family
> (all 1-blocks equal width `a`, all R-blocks equal width `b`,
> `r = a/b`), prove `Lambda_n` is maximized at `r = sqrt(R)`.

## Known accepted reductions/objects (from round 2 baseline)

1. Every global maximizer over the measurable box is bang-bang
   `[1,R,1,...,1]` with exactly `2n` switches (STRICT, baseline).
2. The balanced alternating secular polynomial `F_n(y)` has exactly
   `2n` simple roots in `(0,pi)` (STRICT, baseline; closes O3).
3. For any maximizer, the ratio energy invariant is `E = 0`, hence
   `q0 = u_{n+1}'(0)/u_n'(0) = 1/c`, `q1 = -1/c`
   with `c = sqrt(lambda_n/lambda_{n+1})`.

## Completion criteria

- O1 closed iff a rigorous proof establishes that every `[1,R,1,...,1]`
  bang-bang configuration with 2n switches has
  `Lambda_n <= c_n(R)`, with equality attained at the balanced configuration.
- O2 closed iff a rigorous proof establishes the same maximum inside the
  one-parameter equal-within-type family.

Neither is claimed closed by this run.

## Status of this run

A new STRICT structural tool for the general equal-within-type alternating
family is produced (Chebyshev secular representation). It does not by itself
close O1 or O2. Numerical evidence for O2 is recorded as EVIDENCE, not proof.
