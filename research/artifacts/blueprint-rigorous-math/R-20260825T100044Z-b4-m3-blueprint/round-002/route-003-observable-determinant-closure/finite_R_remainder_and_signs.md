CANDIDATE_COMPLETE_PROOF

# Uniform finite-R remainder and sign bridge

## 1. Analytic domain

Let `v=u^2` and let `z(v)=(K,B,X,Y)` be the locally unique exact analytic
branch supplied by the corrected third blow-up. Choose `rho>0` smaller than
its analytic radius so that, on `0<=v<=rho`, all of the following hold:

1. `K`, `Cbr`, all three half-widths, `ID`, and `IN` are positive.
2. `sin(p1)`, `sin(p1t)`, `sin(p3)`, `cos(p3t)`, and the divided small-phase
   functions `sin(p2)/u`, `sin(p2t)/u` are nonzero.
3. The two ordinary half-stiffness determinants used in `GD` and `GN` are
   nonzero after their displayed removable powers of `u` are extracted.
4. The half-eigenvalues are simple, so the derivative determinants `D1` in the
   two reduced-Green formulas are nonzero after removable powers are extracted.
5. `Wraw_j/u^6<0` for `j=1,2`.

Such a `rho` exists. At `v=0`, the relevant limits are

```text
K=kappa>0,
Cbr=16/(pi kappa)>0,
sin(p1)=1,
sin(p3)=cos(p3)=1/sqrt(2),
sin(p2)/u=kappa/2,
ID=IN=pi/(4 kappa^3)>0,
Wraw_j/u^6=-8/kappa^3<0.
```

The ordinary inverses and reduced finite parts have exact Laurent expansions
with nonzero leading denominators in the replay certificate. Continuity after
the stated removable powers are extracted supplies items 3 and 4. The
round-001 branch theorem supplies exact finite-R correspondence, positive
widths, eigenvalue indexing, and INF band signs on a possibly smaller
interval; decrease `rho` once to include those conditions.

## 2. Analytic normalized observables

Exact parity under `u->-u` is as follows. `K,B,X,Y,p1,p3,p1t,p3t` are even;
`eps,k2,k3,p2,p2t` are odd. In every mass and stiffness entry, the odd factors
occur in parity-preserving ratios. After `|Wraw_j|` is replaced by
`-Wraw_j` on the fixed local sign branch, all four target objects are even.

The coefficient cancellations proved by exact arithmetic therefore define
the following analytic functions on `0<=v<=rho`:

```text
Fm(v)  = u^(-4)  (m3D-m3N),
Fchi(v)= Chi_up,
Fp(v)  = u^(-20) det Kp_odd,
Fo(v)  = u^(-26) det Ko.
```

Their endpoint values are exactly

```text
Fm(0)  = -am,  am=4/kappa^5>0,
Fchi(0)= achi, achi=3/2+4/(pi kappa)>0,
Fp(0)  = ap,  ap=128 kappa^2/pi^2>0,
Fo(0)  = ao,  ao=2048 kappa^2/pi^4>0.
```

This is more than a formal asymptotic assertion: each normalized quotient has
a removable endpoint singularity and extends analytically in the actual
finite-`u` branch parameter `v`.

## 3. Genuine uniform remainder constants

Because the four extended functions are continuously differentiable on the
compact interval `[0,rho]`, the finite constants

```text
Mm   = sup_[0,rho] |Fm'(v)|,
Mchi = sup_[0,rho] |Fchi'(v)|,
Mp   = sup_[0,rho] |Fp'(v)|,
Mo   = sup_[0,rho] |Fo'(v)|
```

exist. The mean-value theorem gives, uniformly for `0<=u^2<=rho`,

```text
|m3D-m3N+am u^4|       <= Mm u^6,
|Chi_up-achi|           <= Mchi u^2,
|det Kp_odd-ap u^20|    <= Mp u^22,
|det Ko-ao u^26|        <= Mo u^28.
```

These are actual branch-uniform bounds. They are not an interpretation of
big-O notation and do not use numerical continuation.

Use the convention `a/(2M)=+infinity` when `M=0`, and define

```text
vstar=min(rho, am/(2Mm), achi/(2Mchi), ap/(2Mp), ao/(2Mo)),
ustar=sqrt(vstar),
R0=max(1,ustar^(-6)).
```

If necessary, replace `vstar` by a smaller positive number so the strict
branch inequalities in Section 1 hold at the endpoint as well. Then for every
finite `R>R0`, with `u=R^(-1/6)`, the exact branch exists and

```text
m3D-m3N <= -(am/2)u^4<0,
Chi_up   >=  (achi/2)>0,
det Kp_odd >= (ap/2)u^20>0,
det Ko     >= (ao/2)u^26>0.
```

Also `Cbr(u)>0` after adding its positive endpoint value to the same compact
derivative-supremum construction.

## 4. Translation to R

Since `u=R^(-1/6)`, the exact uniform remainders become

```text
m3D-m3N = -(4/kappa^5)R^(-2/3)+O(R^(-1)),
Chi_up  = 3/2+4/(pi kappa)+O(R^(-1/3)),
det Kp_odd = (128 kappa^2/pi^2)R^(-10/3)+O(R^(-11/3)),
det Ko = (2048 kappa^2/pi^4)R^(-13/3)+O(R^(-14/3)).
```

Every big-O here abbreviates the explicit uniform constants above and is valid
for all `R>R0` on the exact finite branch. An effective decimal value of `R0`
is not needed for the existential theorem and is not claimed.

## 5. Boundary audit

- `u=0` is used only after analytic removal; no endpoint singular matrix is
  evaluated directly.
- All asserted signs concern finite `R>R0`, not only the limiting point.
- The fixed Wronskian sign justifies the absolute-value branch uniformly.
- The branch theorem prevents local branch switching on this interval.
- The bridge is conditional on independent acceptance of the hash-bound
  branch theorem, exactly as allowed by the route contract.
- No uniform statement is made outside the `n=2` symmetric INF germ.
