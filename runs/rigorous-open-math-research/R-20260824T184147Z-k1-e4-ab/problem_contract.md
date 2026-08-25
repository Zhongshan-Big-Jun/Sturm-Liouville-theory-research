# Problem Contract - K(1) strict anchor run

Run: `R-20260824T184147Z-k1-e4-ab`
Benchmark: `SL-K1-E4-20260825`
Source repository: `Zhongshan-Big-Jun/Sturm-Liouville-theory-research`
Source commit: `db7e597e4ee9fdd2941c8554b227d93afd935daf`

## Open-problem provenance

The source document `docs/SL_third_order_recurrence_theory.tex` recorded the
even minimal-solution anchor `K(1)=e/4` as numerical evidence only.  The same
document stated that the generating-function ODE had not been solved and
listed the anchor under open work.  The frozen benchmark therefore asked for a
strict proof or strict refutation of the claim below.

## Frozen definition

For `j >= 3`,

```text
P_j = 8 j^2 - 4 j + j/(j-1)
Q_j = 4 j (j-1) (2j-1) (2j-3) + 4 j (2j-3)
R_j = 4 j (j-2) (2j-3) (2j-5)
```

The recurrence is

```text
mu_j = P_j mu_{j-1} - Q_j mu_{j-2} + R_j mu_{j-3}.
```

For `N >= 3`, initialize

```text
mu^(N)_{N+1} = 1,   mu^(N)_N = mu^(N)_{N-1} = 0,
```

and apply the recurrence backwards for `j = N+1, ..., 3`.  Define
`hat_mu^(N)_k = mu^(N)_k / mu^(N)_0` and, when the limit exists,
`mu*_k = lim_(N -> infinity) hat_mu^(N)_k`.

## Completion criteria

1. Prove existence and uniqueness of the normalized minimal branch selected by
   the finite backward construction, including a nonzero normalizer.
2. Prove existence of the asymptotic limit.
3. Prove or refute exactly
   `lim_(j -> infinity) j^3 mu*_j = e/4`.
4. Audit the `j=3` endpoint, terminal indexing, signs, normalization, and all
   infinite-sum or limit interchanges.

Numerical agreement, fitted asymptotics, and unchecked symbolic output do not
count as a complete result.

## Scope boundary

This contract concerns the `c=1` anchor only.  The general constant `K(c)`,
source-term control in the broader third-order program, and general
coefficient-family classification remain open.
