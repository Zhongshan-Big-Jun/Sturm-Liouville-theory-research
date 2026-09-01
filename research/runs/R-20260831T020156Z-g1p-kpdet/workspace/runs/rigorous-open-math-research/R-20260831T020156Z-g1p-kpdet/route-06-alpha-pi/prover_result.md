PROVED

# Exact exclusion of the near-one alpha-pi endpoint

## Input audit

All frozen inputs were verified before use.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-04-mass-g-wave/accepted_package.md                      cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-04-mass-g-wave/repair/near_one_repair.md                8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314
route-05-alpha-collision/accepted_package.md                  49d1691a384a6b7d550d8b547dfc25de5daf14fd575d6018462417b04e7257ba
```

## Theorem

There is no sequence of complete admissible tuples in the frozen phase
system such that

```text
m_j->1+,
alpha_j->pi.
```

Equivalently, there are `epsilon_pi>0` and `delta_pi>0` for which the
complete phase system has no tuple satisfying

```text
1<m<1+epsilon_pi,
pi-delta_pi<alpha<pi.
```

More precisely, let `d=pi-alpha` and temporarily impose every strict modal,
spectral, and band constraint, but not the mass equation. Along every
sequence with `m->1+` and `alpha->pi`, the constraints force

```text
c->2/3,
theta->pi/2,
beta->0,
X/d->-1,
C/d->1,
(pi/2-theta)/d->1,
beta/d->2,
I3hat->3pi/4,
I2hat->pi/2.
```

For the exact mass residual

```text
Delta_M=C^2 I2hat-c^3 s^2 I3hat,
```

one then has

```text
Delta_M->-pi/6.
```

Thus the exact equation `Delta_M=0` is impossible in this endpoint regime.

## Proof

### 1. Uniform spectral limits and the two total phases

The modal inequality

```text
delta_3<beta<delta_3+pi,
0<delta_3<pi/2
```

gives the switch-independent bound

```text
0<beta<3pi/2.                                      (1)
```

The density satisfies `1<=rho_m<=m^2` for every switch pair. The min-max
principle, uniformly over the moving interfaces, therefore gives

```text
lambda_2->4pi^2,
lambda_3->9pi^2,
c=sqrt(lambda_2/lambda_3)->2/3.                    (2)
```

Both exact total-phase identities are

```text
alpha+m beta+theta=m sqrt(lambda_3)L,
c(alpha+m beta+theta)=m sqrt(lambda_2)L,
L=1/2.                                             (3)
```

Consequently,

```text
alpha+m beta+theta->3pi/2,
c(alpha+m beta+theta)->pi.                         (4)
```

By `(1)`, `(m-1)beta->0`, so `(4)` also yields

```text
alpha+beta+theta->3pi/2,
c(alpha+beta+theta)->pi.                           (5)
```

Since `alpha->pi`, equations `(2)` and `(5)` imply

```text
beta+theta->pi/2,
c(beta+theta)->pi/3.                               (6)
```

### 2. Transfer and band limits

The exact transfer expressions may be compared directly with the uniform
trigonometric addition formulas:

```text
X=cos(beta+theta)-(m-1)S sin(beta),
Z=sin(beta+theta)+(1/m-1)C sin(beta),
Y=sin(c(beta+theta))+(m-1)Cc sin(c beta),
T=cos(c(beta+theta))+(1-1/m)s sin(c beta),
D=sin(beta+theta)+(m-1)C sin(beta),
N=cos(c(beta+theta))-(m-1)s sin(c beta).
```

All coefficients are bounded on the strict modal domain. Hence `(6)` gives

```text
X->0,
Z->1,
Y->sqrt(3)/2,
T->1/2,
D->1,
N->1/2.                                           (7)
```

Use the band equation in its undivided form

```text
C Y=-s X.                                          (8)
```

No passage through `1/C` is made. From `(7)`, the limit of `(8)` is
`C_0 sqrt(3)/2=0`; since `0<theta<pi/2`, this forces

```text
C->0,
theta->pi/2.                                       (9)
```

Equation `(6)` then forces `beta->0`, and `(2)` and `(9)` give

```text
s=sin(c theta)->sin(pi/3)=sqrt(3)/2.               (10)
```

The sign in `(8)` is essential and agrees with `X<0<Y`, `C>0`, and `s>0`.

### 3. Exact first-order endpoint scales

For all sufficiently late terms, `cos(alpha)` is nonzero. The exact DN
spectral equation gives

```text
X=Z tan(alpha)=-Z tan(d).
```

Using `(7)` therefore yields

```text
X/d->-1.                                           (11)
```

Divide `(8)` by `d`, not by `C`. Equations `(7)`, `(10)`, and `(11)` give

```text
(C/d)Y=s(-X/d),
C/d->1.                                            (12)
```

If `e=pi/2-theta`, then `C=sin(e)`, so `(12)` implies

```text
e/d->1.                                            (13)
```

Finally, the exact formula for `X` gives

```text
m S sin(beta)=C cos(beta)-X.
```

After division by `d`, equations `(9)`, `(11)`, and `(12)` give
`sin(beta)/d->2`. Since `beta->0`,

```text
beta/d->2.                                         (14)
```

### 4. Exact removal of both apparent norm denominators

Before passing to the limit, use both exact spectral equations. For all
sufficiently late terms, `cos(alpha)` and `cos(c alpha)` are nonzero, and

```text
X^2/sin(alpha)^2=Z^2/cos(alpha)^2,
Y^2/sin(c alpha)^2=T^2/cos(c alpha)^2.              (15)
```

Thus the norm formulas become the exact nonsingular identities

```text
I3hat=
  m^2 Z^2 Js(alpha)/cos(alpha)^2
  +m J(C,-m S;beta)
  +m^2 Jc(theta),                                  (16)

I2hat=
  m^2 T^2 Js(c alpha)/cos(c alpha)^2
  +m J(s,m Cc;c beta)
  +m^2 Js(c theta).                                (17)
```

Here `cos(alpha)->-1` and `cos(c alpha)->cos(2pi/3)=-1/2`; neither new
denominator vanishes. Using `(2)`, `(7)`, `(9)`, and `beta->0`, the middle
terms in `(16)-(17)` tend to zero and

```text
I3hat->Js(pi)+Jc(pi/2)=pi/2+pi/4=3pi/4,            (18)

I2hat->Js(2pi/3)+Js(pi/3)=pi/2.                    (19)
```

The cancellation in `(19)` is exact:

```text
Js(2pi/3)=pi/3+sqrt(3)/8,
Js(pi/3)=pi/6-sqrt(3)/8.
```

### 5. Mass contradiction

Equations `(9)`, `(10)`, `(18)`, and `(19)` give

```text
C^2 I2hat->0,
c^3 s^2 I3hat
 ->(2/3)^3 (sqrt(3)/2)^2 (3pi/4)
 =pi/6.                                            (20)
```

Therefore

```text
Delta_M=C^2 I2hat-c^3 s^2 I3hat->-pi/6.            (21)
```

A complete tuple satisfies the exact mass equation `Delta_M=0`, contradicting
`(21)`. This proves the sequential exclusion.

## Uniform quantifier upgrade

The argument proves a stronger uniform residual statement. There exist
`epsilon_pi>0` and `delta_pi>0` such that every tuple satisfying the strict
modal, spectral, and band constraints in

```text
1<m<1+epsilon_pi,
pi-delta_pi<alpha<pi
```

obeys, after decreasing the constants if necessary,

```text
Delta_M<-pi/12.                                    (22)
```

Otherwise one could choose a sequence with `m_j<1+1/j`,
`alpha_j>pi-1/j`, and `Delta_M>=-pi/12`; equation `(21)` would contradict
that choice. Since a complete tuple has `Delta_M=0`, `(22)` gives the stated
uniform empty wedge.

Combining this wedge with the accepted alpha-zero wedge and the accepted
fixed-separation near-one theorem closes the complete alpha interval near
`m=1`: for some `epsilon_*>0`, every complete admissible tuple with
`1<m<1+epsilon_*` lies in the fixed-separation region and satisfies `G>0`,
hence also `Xi>0` and `Phi<0` by the accepted reduction.

## Norm, denominator, and boundary audit

- The only modal estimate used for compactness is the exact one-zero bound
  `beta<3pi/2`; no fixed-switch assumption occurs.
- Both total-phase identities in `(3)` retain the middle-layer factor `m`.
- The band sign is used as `C Y=-s X`; this avoids dividing by the vanishing
  quantity `C` and is compatible with `X<0<Y`.
- The DN and DD spectral equations are applied before taking norm limits,
  producing `(15)`. The resulting denominators tend to `1` and `1/4` in
  square, respectively.
- The nonzero limiting factors are `Y,s->sqrt(3)/2`, `Z->1`,
  `I3hat->3pi/4`, and `I2hat->pi/2`.
- The mass right side tends to the strictly positive exact value `pi/6`.
- Every tuple remains strictly inside `0<alpha<pi`, `0<theta<pi/2`, and the
  modal component. Only its hypothetical limit lies on the excluded endpoint
  face.

## Exact remaining gap

The near-one alpha-pi endpoint is closed, and together with the two accepted
near-one packages it removes the last alpha-boundary gap in the near-one
`G>0` mechanism. This does not prove `G>=0`, `PHI-SIGN`, or `KP-DET` for
arbitrary finite `m>1`; those global finite-contrast obligations remain open.

decision_delta: Exact spectral and band constraints force C/(pi-alpha)->1 and finite norm limits, while the mass residual tends to -pi/6; hence a uniform complete-system empty wedge exists near (m,alpha)=(1,pi), closing the last alpha gap in the near-one G>0 mechanism but not the arbitrary finite-m KP-DET problem.
