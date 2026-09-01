STRICT

# Accepted mass-to-sign partial package

## Audit bindings

- W4 source SHA256:
  `d55114570d516c69e446f2c228a76fb8827335e596df6c62e3d355a5232f9ffa`.
- W5 source SHA256:
  `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9`.
- Joint audit SHA256:
  `7e56fc988a361efa5aeec7d232fb43b03b7889dacfc8ebc3d4afd6a02231c175`.
- Near-one repair SHA256:
  `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314`.
- Near-one re-audit SHA256:
  `3f88a6ed8cf6da7f7adc41a195776fbfa9f00c8cec97153156a98f773a0c573d`.

This file compiles only statements accepted by the bound independent audits.
It does not add a new proof claim.

## P5. Exact mixed-sign mass balance

On the complete admissible phase system, define

```text
Q3=alpha(X^2+Z^2)+beta(m Z^2+X^2/m)+theta,
Q2=alpha(Y^2+T^2)+beta(m T^2+Y^2/m)+theta,

A=C^2(Y^2+T^2)-c^2 s^2(X^2+Z^2),
B=C^2(m T^2+Y^2/m)-c^2 s^2(m Z^2+X^2/m),
H=C^2-c^2 s^2.
```

Then the exact mass equation is equivalent to

```text
C^2 Q2=c^2 s^2 Q3,
alpha A+beta B+theta H=0.
```

With

```text
Lalpha=csc(c alpha)^2-c^2 csc(alpha)^2,
mu=m-1/m>0,
```

one has

```text
A=s^2 X^2 Lalpha,
B=s^2 X^2[m Lalpha-mu(1-c^2)],

(alpha+m beta)Lalpha+theta H/(s^2 X^2)
 =beta mu(1-c^2)>0.
```

Therefore `(A,B,H)` is strictly mixed-sign. In particular, the exact mass
constraint forbids both closed same-sign orthants. The implication from
`G<0` to either same-sign orthant remains open.

## P6. Exact mass-free obstruction

The exact point

```text
m=sqrt(5), c=4/5, alpha=theta=pi/4, beta=pi
```

satisfies both spectral equations, the band equation, every strict modal
inequality, and strict interior reconstruction. Exact rational interval
arithmetic proves

```text
G<0,
Xi<0.
```

Its exact mass residual satisfies

```text
Delta_M=C^2 I2hat-c^3 s^2 I3hat>0.
```

Thus it is not a complete-system counterexample. It proves that no route
using only spectral, band, modal, or denominator-sign data can establish
`G>=0`; the exact mass equation is load-bearing. It also proves that `U>0`
alone is insufficient.

## P7. Uniform near-one positivity away from left collision

Fix `0<eta<pi/2`. There exists `epsilon_eta>0` such that every complete
admissible tuple with

```text
1<m<1+epsilon_eta,
eta<=alpha<=pi-eta
```

satisfies

```text
G>0.
```

The quantifier is uniform over both moving switches. The proof uses a
switch-independent modal bound on `beta`, min-max spectral convergence,
compact passage through the exact norm formulas, the limiting mass equation
to separate `theta` from both endpoints, uniform positivity of
`cos(2alpha/3)-cos(alpha)`, and divergence of `Dtheta`.

Since

```text
Xi=X^2 G-r K Dtheta,
K<0,
Dtheta>0,
```

this region also has `Xi>0`, hence `Phi<0` and the branch-local KP determinant
sign. This is a new mechanism-level proof compatible with the previously
accepted near-one negative-inertia component.

## Exact remaining gaps

- The simultaneous limit `m->1+`, `alpha->0` is not controlled by P7.
- The global sign-coherence implication from `G<0` to a forbidden orthant is
  open.
- Arbitrary finite `R`, complete `PHI-SIGN`, and complete `KP-DET` remain open.
