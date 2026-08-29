# Valuation and exhaustiveness audit

## Admitted asymptotic class

Let `u -> 0+`, `v=u^2`, and let an exact real zero branch of the frozen
four-equation map satisfy, eventually,

```text
K in a compact subset of (0,infinity),
p1 = pi/2 + A*u^2 -> pi/2,
p3 = pi/4 + B*u^2 -> pi/4,
r := k3/k2 = 1 + C*u^4/K -> 1,
sin(p3), cos(p3*r), sin(p1*r) bounded away from zero.
```

No ordinary-series hypothesis is imposed. The admitted corrections may be
ordinary integer powers, rational Puiseux powers, powers times finite
polynomials in `log u`, inverse powers of `log u`, well-ordered products of
those scales, or flat corrections. An exact branch is admitted whenever it
has the displayed limits, even if it has no transseries at all. This is the
finite, nonzero, interior limiting geometry selected by the frozen
normalization.

The following are separate singular geometries, not members of this class:
`K -> 0`, `K -> infinity`, a nonunit limiting ratio `r`, or limits in which
`sin(p3)`, `cos(p3*r)`, or `sin(p1*r)` vanish. They are not used to establish
the target branch and are not globally refuted here.

## Blow-up and valuation table

Put `q=(A*K-2)/v`. Exact parity under `u -> -u` makes `E1,E2,E5` even and
`E6` odd. In the interior chart the exact divisibilities and faces are:

| Residual | Divisor | First face | Status |
| --- | --- | --- | --- |
| `E1` | `u^2` | `F1=-sqrt(2)(K^3+6Kq-18pi+24)/(24K)` | independent |
| `E2` | `u^2` | `F2=sqrt(2)(3piCK+K^3+6Kq-18pi-24)/(24K)` | independent |
| `E6` | `u^5` | `F6=-(3piCK+2K^3+12Kq-36pi)/(12K)` | dependent on `F1,F2` |
| `E5` | `u^4` | `F5`; `F5=0` after `F1=F2=0` | dependent; the old hard term is false |
| reduced `E6` | one further `v` | `H6=8(BK-1)/K^2` | independent secondary face |
| reduced `E5` | one further `v` | `H5=2(6pi^2BK+piK^3-24pi^2+48)/(3piK^6)` | independent secondary face |

The first face has determinant

```text
det d(F1,F2)/d(q,C) = -pi/16 != 0.
```

It fixes

```text
q0=(18*pi-24-K^3)/(6*K),  C0=16/(pi*K).
```

The secondary face fixes

```text
B0*K0=1,
K0^3=18*pi-48/pi.
```

The unique positive seed and its remaining leading data are

```text
K0=(18*pi-48/pi)^(1/3) = 3.45576417140853820024...,
A0=2/K0,
B0=1/K0 = 0.28937159782879774762...,
C0=16/(pi*K0) = 1.47375744591530014160...,
q0=(8/pi-4)/K0 = -0.42060766835754091967....
```

On the seed,

```text
det d(H6,H5)/d(B,K) = 16/K0^5 != 0.
```

## Puiseux, logarithmic, inverse-logarithmic, mixed, and flat scales

The two invertible faces desingularize the exact analytic residual in two
ordinary implicit-function steps with parameter `v=u^2`. Hence there is one
local solution germ analytic in `v`, and every exact branch in the admitted
class eventually lies in the uniqueness neighborhood and equals that germ.
This gives an exhaustive conclusion for the admitted class:

- rational fractional powers cannot be the first correction;
- positive or negative logarithmic factors cannot be the first correction;
- mixed power-log cross terms cannot introduce a distinct branch;
- a flat addition cannot produce a second exact branch;
- odd powers of `u` vanish, because the unique germ is analytic in `u^2`.

Thus the correct branch does not need a noninteger or logarithmic rescue. The
previous appearance of such a need came from the D-mass bookkeeping defect.

## Rescaled phase check

To test whether `B~u^(-2)` hides the same branch under an `O(1)` leading
shift, set `p3 -> theta` with `0<theta<pi/2`, retain `r->1`, and replay the
exact closed residual. The three leading equations eliminate `q,C` and give

```text
C = 8/(pi*K*sin(theta)*cos(theta)),
C = 16*tan(theta)/(pi*K).
```

Therefore `sin(theta)^2=1/2`, and the interior phase box forces
`theta=pi/4`. An interior `O(1)` coordinate shift is not a distinct balance.
The endpoints `theta=0,pi/2` make one of the mass denominators singular and
belong to the separately declared boundary class.

## Original-variable valuations and remainder target

The analytic germ has

```text
K=K0+O(u^2),  A=A0+O(u^2),
B=B0+O(u^2),  C=C0+O(u^2),
k2=K0*u+O(u^3),
k3=K0*u+O(u^3),
k3-k2=C0*u^5+O(u^7),
p1=pi/2+A0*u^2+O(u^4),
p3=pi/4+B0*u^2+O(u^4).
```

Every omitted Taylor monomial has strictly larger `v` valuation after the
two exact blow-ups. This is the no-equal-or-lower-valuation predicate used by
the classification.

