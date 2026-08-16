FINITE_COMPUTATIONAL_RESULT

# MIN-REFL-C2-L: finite certificate for the C2-E compensating chart

## 1. Exact rational chart

Put `c=pi/2` and use

```text
h=c-Aplus,
k^2=kappa h,
eta=Aminus-c=h+beta h^2.
```

The certified rectangular chart is

```text
0 <= h <= 2^-16,
0 <= kappa <= 3/8,
-3/2 <= beta <= 0.                                     (1.1)
```

It contains the complete limiting retained triangle from C2-E.  This route
certifies (1.1) itself; it does not assert that every finite prelimit retained
point outside (1.1) is empty.

Define the exact regularized quantities

```text
q=tan(k(c-h))/k,
sigma=tan(k(c+eta))/k,
A=a/h=q tan(h)/h,
B=b/h=sigma(1+beta h) tan(eta)/eta.
```

Every apparent zero at `h=0` is evaluated through `sinc/cos`.  In
particular `u=A/B` and the inverse Jacobian is evaluated as

```text
J_E=u { h/[theta sinc(k theta)cos(k theta)]
        +1/[(1+beta h)sinc(eta)cos(eta)] }.             (1.2)
```

## 2. Stable R17 ratios

Write `D=h Dhat`.  The checker cancels every required power of `h` before
interval evaluation.  The only nontrivial divided difference is

```text
E=[tan(h)/h-(1+beta h)tan(eta)/eta]/h.
```

Since `beta<=0` and `0<=eta<=h`, the mean-value identity gives

```text
E=(-beta){tan(eta)/eta+h f'[xi]},
f(x)=tan(x)/x,       eta<=xi<=h.
```

The exact integral formula

```text
f'(x)=integral_0^1 2t sec^2(tx)tan(tx) dt
```

implies the directed enclosure

```text
0<=f'[xi]<=sec^2(h)tan(h).                              (2.1)
```

Likewise

```text
[sigma-q]/h=(2+beta h) sec^2(k xi),
c-h<=xi<=c+eta,                                        (2.2)
```

so monotonic endpoint evaluation encloses the second divided difference.

Equations (2.1)-(2.2) give a stable exact enclosure of

```text
S=(rB-1)/h.
```

The checker then cancels `h` from `W_0,W_1,U_i` and from all four Bernstein
numerators.  It evaluates exactly

```text
rho_i/h^2 = Pplus (Nhat_i/h^2)/(g Knew cp^4).
```

The ratio `b/(a+b)` in `Knew` is replaced by the exact regular form
`B/(A+B)`; without this cancellation the exact boundary would be `0/0`.

## 3. Finite tensor certificate

At 256-bit Arb precision, partition

```text
kappa: 24 cells of width 1/64,
beta:  96 cells of width 1/64,
h:     the single closed interval [0,2^-16].
```

There are exactly 2,304 boxes.  A box is discarded only if its directed
upper endpoint proves `b<=a` or `S<=0`, hence it has no strict retained
point.  Every other box is checked with no recursive subdivision.

The exact predicates pass on all 993 nondiscarded boxes:

```text
J_E > 999/1000,
rho_i/h^2 < 5,       i=1,2,3,4.                        (3.1)
```

The remaining 1,311 boxes are discarded, and there are zero singular or
failed evaluations.  Since `h<=2^-16`, (3.1) proves

```text
rho_i < 5/2^32 < 1.                                    (3.2)
```

Thus all four conditional R17 gaps are strictly positive throughout the
retained part of (1.1).  A valid explicit chart cutoff is

```text
h_*=2^-16.                                              (3.3)
```

This direct normalized-ratio certificate is stronger for sign purposes than
an explicit first-order remainder constant.

## 4. Exact failure of the requested `M_E` extraction

The same box arithmetic does **not** certify

```text
|rho_i/h^2-P_i(kappa,R0)| <= M_E h,
R0=-beta-(pi^2/2)kappa.                                (4.1)
```

The first failing expression is

```text
D_4={rho_4/h^2-4pi^2 R0 kappa}/h.                       (4.2)
```

On the fixed `(kappa,beta)` partition, the directed width of the numerator
in (4.2) is `1.1721` for `h<=2^-16`.  Repeating the same **bounded** tensor
evaluation with `h<=2^-24` leaves width `1.1704`; it does not acquire the
required factor `h`.  Consequently division by `h` creates a spurious
interval pole growing like `2^m` on `[0,2^-m]`.

This is not an analytic pole: C2-E proves the numerator vanishes at `h=0`.
It is the first concrete loss of dependency in plain box arithmetic—the
same `kappa,beta` occur through `S,W_i,U_i,Knew` and again in the subtracted
polynomial, but Arb boxes treat those occurrences independently.  A finite
`M_E` requires either:

1. exact symbolic factorization of the numerator by `h`, or
2. a multivariate affine/Taylor/Bernstein model retaining the
   `(kappa,beta)` correlations.

The direct cutoff (3.3) remains valid and does not rely on (4.1).

## 5. Scope

This is a complete finite certificate only for chart (1.1), conditional on
the frozen R14/R17 reduction.  It does not certify the escape regions
`kappa>3/8` or `beta<-3/2`, the remaining `t=1` annulus, the complete R17
cube, the physical bridge, or canonical reflection symmetry.

