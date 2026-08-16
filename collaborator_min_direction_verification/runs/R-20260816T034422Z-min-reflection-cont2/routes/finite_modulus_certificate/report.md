FINITE_COMPUTATIONAL_RESULT

# MIN-REFL-C2-L final report

A finite exact Arb certificate now replaces the existential C2-E argument
on the explicit stable-coordinate box

```text
0<=h<=2^-16,   0<=kappa<=3/8,   -3/2<=beta<=0.
```

After cancelling every boundary power of `h`, all 2,304 fixed tensor boxes
were evaluated at 256-bit precision.  Exactly 1,311 were rigorously discarded
as nonretained; all 993 remaining boxes prove

```text
J_E>999/1000,          rho_i/h^2<5  (i=1,...,4).
```

Therefore `rho_i<5/2^32<1`, so the four conditional R17 gaps are positive.
The explicit chart cutoff is

```text
h_*=2^-16.
```

The requested Lipschitz remainder constant `M_E` was not obtained.  Its first
interval failure is the removable expression

```text
[rho_4/h^2-4pi^2(-beta-pi^2 kappa/2)kappa]/h.
```

The numerator retains directed width about `1.17` both at `h<=2^-16` and
`h<=2^-24`; plain boxes lose the shared `(kappa,beta)` correlation and create
a spurious `1/h` pole.  Exact factorization by `h` or a multivariate Taylor/
Bernstein model is required to certify `M_E`.  The direct sign cutoff above
is unaffected.

This is not a complete `t=1` collar: the finite escape regions outside the
chosen `(kappa,beta)` rectangle remain to be discharged.  R14/R17 also remain
noncanonical, so no physical or canonical reflection theorem follows.

```text
route_id: MIN-REFL-C2-L
status: finite_computational_result
chart_cutoff: h_*=2^-16
J_E_lower: 999/1000
rho_i_over_h2_upper: 5
M_E_status: not_certified; first dependency pole frozen
propagation_status: non_propagating
formalization_status: not_requested
```

