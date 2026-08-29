# Independent replication report

## Result

Set

```text
u = R^(-1/6)
kappa = (18 pi - 48/pi)^(1/3)
      = 3.455764171408538200241579393...
```

The independently reconstructed branch has

```text
k2 = kappa u + O(u^3)
k3 = kappa u + 16/(pi kappa) u^5 + O(u^7)
p1 = pi/2 + 2/kappa u^2 + O(u^4)
p3 = pi/4 + 1/kappa u^2 + O(u^4).
```

The requested observables are

```text
m3D - m3N = -4/kappa^5 u^4 + O(u^6)
           = -4/kappa^5 R^(-2/3) + O(R^(-1)) < 0,

Chi_up = 3/2 + 4/(pi kappa) + O(u^2) > 0,

det Kp_odd = 128 kappa^2/pi^2 u^20 + O(u^22)
           = 128 kappa^2/pi^2 R^(-10/3) + O(R^(-11/3)) > 0,

det Ko = 2048 kappa^2/pi^4 u^26 + O(u^28)
       = 2048 kappa^2/pi^4 R^(-13/3) + O(R^(-14/3)) > 0.
```

The two determinant coefficients are

```text
128 kappa^2/pi^2  = 154.881098264214048574215070873...
2048 kappa^2/pi^4 = 251.083779199286295433195105027...
```

## Scale classification

Write `k2` as asymptotic to `epsilon^alpha` with `epsilon = R^(-1/2)`. In the finite, nonresonant phase chart, the endpoint correction has scale `epsilon/k2`, while the first internal propagation correction has scale `k2^2`. Nondegenerate compatibility requires

```text
2 alpha = 1 - alpha,
```

so `alpha = 1/3` and `k2` has scale `u = epsilon^(1/3)`. For `alpha < 1/3`, propagation enters first with no same-order geometric cancellation. For `alpha > 1/3`, the endpoint correction enters first with no same-order propagation cancellation. This is a classification inside the declared finite-interior power-law chart, not a global classification of every singular geometry.

The switch geometry satisfies

```text
x1 = pi/(2 kappa) u^2 + O(u^4),
1/2 - x2 = pi/(4 kappa) u^2 + O(u^4).
```

Hence the two interior low-density pieces remain finite while the high-density endpoint and central pieces have width `O(R^(-1/3))`.

## Seed compatibility

The first cascade levels give

```text
A0 kappa = 2,
C0 = 16/(pi kappa).
```

At the next joint level, the coefficient system has rank 3. Its solvability condition reduces to

```text
4 (pi kappa^3 - 18 pi^2 + 48)/(3 pi^2 kappa^2) = 0.
```

The unique positive solution is

```text
kappa^3 = 18 pi - 48/pi,
B0 = 1/kappa.
```

The resulting spectral gap also obeys

```text
lambda3 - lambda2 = 32/pi R^(-1) + O(R^(-4/3)).
```

## Mass difference and upstream scalar

The three mass blocks give

```text
m1D - m1N =  4/kappa^5 u^4 + O(u^6),
m3D - m3N = -4/kappa^5 u^4 + O(u^6),
mLD - mLN = O(u^6).
```

Thus the leading cancellation in `E5` is between the first and third blocks. It does not imply `m3D - m3N = 0`.

Using `B0 kappa = 1` and the cubic relation,

```text
1 + B0 kappa/2 + 3 pi/(2 kappa) - kappa^2/12
= 3/2 + 4/(pi kappa)
> 0.
```

Therefore the upstream scalar is positive and is incompatible with a zero leading value.

## Sector determinants

The run rebuilt the exact switch Jacobian from the full five-layer transfer matrices, exact layer norm integrals, implicit eigenvalue derivatives, jump normalization, and mirror-sector projections.

For `Kp_odd`, after writing `Dp = diag(u^2,u^6)`, the leading matrix is

```text
-1/pi Dp [[kappa^4, -4 kappa^2],[-4 kappa^2,16]] Dp.
```

The bracketed matrix has rank 1, so the nominal `u^16` determinant term vanishes. The `u^18` term also cancels after branch compatibility. The first nonzero term is the positive `u^20` coefficient stated above.

For `Ko`, the leading matrix is

```text
-16/pi u^12 [[1,2],[2,4]],
```

which is again rank 1. The nominal `u^24` determinant term vanishes, and the next matrix layer gives the positive `u^26` coefficient stated above.

The branch variables and normalized sector matrices are even in `u`. Both determinants are therefore even series. The odd candidates

```text
u^21 = R^(-7/2),
u^27 = R^(-9/2)
```

cannot be the first nonzero terms on this branch.

## Verification

The independent implementation supplied three checks:

| Check | Result | Label |
| --- | --- | --- |
| Symbolic cascade and rank-3 compatibility | Reproduced the exact cubic seed, block mass coefficients, and positive scalar | Conditional exact symbolic derivation |
| 140-digit Laurent reconstruction from the full sector system | Reproduced both exponents and coefficients, unchanged under two choices of an unfixed higher jet | VERIFIED_REPLICATION |
| Direct finite-u roots and full switch Jacobian | At `u=0.06`, maximum equation residual was about `6.6e-50`; scaled determinants converged to the closed coefficients | EVIDENCE |

The Laurent truncation was increased from order 30 to order 46 without changing either leading determinant term. An attempted exact coefficient-field implementation was not completed and is not claimed as a certificate in this run.

## Epistemic boundary

This run independently reproduces every headline M3 correction. By itself, it does not prove analytic branch existence, admitted-class exhaustiveness beyond its controlled scale argument, or a uniform remainder bound for every sufficiently large finite R. Those theorem-grade steps are supplied by the accepted Blueprint proof chain, not retroactively attributed to this replication.
