# Explicit-modulus contract and exact unsigned objects

## C2-E compensating corner

Let `c=pi/2`, `h=c-z`, `k^2=kappa h`, and
`eta=theta-c=h+beta h^2`.  Define the exact retained coordinate

```text
u = tan(kz)tan(h)/[tan(k theta)tan(eta)],
alpha=(1-u)/h.
```

The exact inverse Jacobian is

```text
J_E = partial_beta alpha
    = h u { k/[sin(k theta)cos(k theta)]
            +1/[sin(eta)cos(eta)] },                   (E.1)
```

and `J_E->1`.  The frozen C2-E replay used only the formal inverse
`beta=alpha-4/pi+O(h)`; it did not certify a rational box on which

```text
0 < m_E <= J_E <= M_J.                                  (E.2)
```

Nor did it evaluate the exact off-boundary `rho_i` after solving (E.1).
On the retained boundary triangle the four leading polynomials have the
exact common bound

```text
max_i P_i <= 32/pi^2 < 4.                               (E.3)
```

Therefore a machine certificate of

```text
|rho_i/h^2-P_i| <= M_E h                               (E.4)
```

would immediately yield the chart-local rational cutoff

```text
h <= min(h0, 1, 1/sqrt(4+M_E))  =>  rho_i<1.            (E.5)
```

For rational output one may replace the square root in (E.5) by any smaller
dyadic.  At present `M_E` and the validated domain `h0` are absent.

## C2-C low and high charts

The exact negative-phase inverse equations have boundary derivatives

```text
partial_sigma F0 -> 1,
partial_tau   F1 -> -pi^2/8.
```

Their signs at the boundary are not the problem.  The missing effective
quantities are the finite-chart derivative bounds and the suprema

```text
M_0 >= sup Psi_0,
M_1 >= sup Psi_1,                                       (C.1)
```

where the C2-C factorizations are

```text
rho_i <= k^2 epsilon Psi_0,
rho_i <= (1-k)^4 v Psi_1.
```

The replay treats the normalized endpoint sums and `Knew` only through
their boundary limits.  In particular it does not encode full finite-chart
expressions for `SU0/k`, `SL0/k`, `SU1`, `SL1`, or a quantitative lower
bound for the denominator

```text
D0^2 Knew C^2(1-a^2k^4)                                (C.2)
```

and its high-chart analogue `Knew C^2 D2^2 A4`.

Even bounds for the two triple charts would not yet give a global `t_*`:
the complementary `t=0` strata are covered in the frozen proof only by a
finite-subcover argument with no listed radii.  An effective Lebesgue number
for that cover is a separate required input.

## Why leading limits cannot supply a cutoff

For arbitrary `M>0`, the analytic families

```text
rho_E(h)=h^2[P+Mh],
rho_C(lambda,r)=lambda[P+Mr]
```

have exactly the same normalized boundary limits as the frozen replays.
Their safe collar radii shrink like a negative power of `M`.  Thus no
positive rational cutoff follows from the leading limits and continuity
alone.  A derivative/majorant certificate such as (E.2)-(E.4) and (C.1)-
(C.2) is logically necessary.

