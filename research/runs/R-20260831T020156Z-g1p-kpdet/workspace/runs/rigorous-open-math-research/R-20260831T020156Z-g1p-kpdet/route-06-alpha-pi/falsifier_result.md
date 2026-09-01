REFUTED

# Exact exclusion of the near-one alpha-pi face

## Input audit

All five bound inputs were verified before use.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-04-mass-g-wave/accepted_package.md                      cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-04-mass-g-wave/repair/near_one_repair.md                8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314
route-05-alpha-collision/accepted_package.md                  49d1691a384a6b7d550d8b547dfc25de5daf14fd575d6018462417b04e7257ba
```

## Exact finding

There is no sequence of complete admissible tuples satisfying

```text
m_j->1+,
alpha_j->pi.
```

Equivalently, there are `epsilon_pi>0` and `delta_pi>0` for which the complete
phase system has no tuple in

```text
1<m<1+epsilon_pi,
pi-delta_pi<alpha<pi.
```

This excludes the complete face itself. It is not merely the failure of a
chosen scaling ansatz.

## Proof

Assume that such a sequence exists. The switch-uniform min-max bounds from the
exact three-layer density give

```text
c->2/3,
alpha+m beta+theta=pL->3pi/2.
```

Because all phases are positive and `m->1`, this implies that `beta` is
bounded and

```text
beta+theta->pi/2.                                    (1)
```

Pass to an arbitrary convergent subsequence of `(beta,theta)`, with limit
`(beta_0,theta_0)`. At `m=1`, `c=2/3`, and using `(1)`, the exact transfer
quantities have the limits

```text
X_0=cos(beta_0+theta_0)=0,
Z_0=sin(beta_0+theta_0)=1,
Y_0=sin((2/3)(beta_0+theta_0))=sqrt(3)/2,
T_0=cos((2/3)(beta_0+theta_0))=1/2.
```

Do not divide by the vanishing candidate `C`. Multiply the exact band equation
by `C` and pass to the limit:

```text
C Y+s X=0
```

gives

```text
cos(theta_0) sqrt(3)/2=0.
```

Thus every convergent subsequence has

```text
theta_0=pi/2,
beta_0=0.
```

Consequently the whole sequence satisfies

```text
theta->pi/2,
beta->0.                                             (2)
```

The coupled scaling is also forced exactly. Put `e=pi-alpha`. The spectral
equation `X cos(alpha)=Z sin(alpha)` and `(2)` give

```text
X/e=(Z/cos(alpha))(sin(alpha)/e)->-1.
```

Dividing the non-singular identity `C Y=-s X` by `e`, and using
`Y->sqrt(3)/2` and `s->sqrt(3)/2`, yields

```text
C/(pi-alpha)->1.                                    (3)
```

Hence any putative complete branch must have the unique leading scaling
`C~pi-alpha`, equivalently
`(pi/2-theta)/(pi-alpha)->1`. Any different constant `k` already violates the
spectral-band subsystem.

It remains to test the unique forced scaling against normalization and mass.
The apparent singularity in the first term of `I3hat` is removable by the
exact spectral equation:

```text
X/sin(alpha)=Z/cos(alpha)->-1.
```

Using `(2)`, boundedness of the transfer coefficients, and
`J(A0,B0;t)->0` as `t->0`, the first norm has the exact limit

```text
I3hat
=m^2 X^2 Js(alpha)/sin(alpha)^2
 +m J(C,-m S;beta)
 +m^2 Jc(theta)
->Js(pi)+Jc(pi/2)
=pi/2+pi/4
=3pi/4.                                             (4)
```

The second norm has no left-layer singularity because
`c alpha->2pi/3`. Since `Y/sin(c alpha)->1`, it satisfies

```text
I2hat
=m^2 Y^2 Js(c alpha)/sin(c alpha)^2
 +m J(s,m Cc;c beta)
 +m^2 Js(c theta)
->Js(2pi/3)+Js(pi/3)
=pi/2.                                              (5)
```

Now pass to the exact mass identity

```text
C^2 I2hat=c^3 s^2 I3hat.
```

By `(2)`, `(4)`, and `(5)`, its two sides have incompatible limits:

```text
C^2 I2hat->0,
c^3 s^2 I3hat
 ->(2/3)^3 sin(pi/3)^2 (3pi/4)
 =pi/6>0.
```

This contradiction proves exact nonexistence. The neighborhood formulation
follows by the standard sequential negation: otherwise one could choose a
tuple with both `m-1<1/j` and `pi-alpha<1/j`.

## Admissibility and denominator audit

- Every member of the assumed sequence lies in the strict modal domain, so
  `0<c<1`, `0<alpha<pi`, `0<theta<pi/2`, `C>0`, `s>0`, and the exact transfer,
  band, norm, and mass formulas apply.
- Positivity of the phases and the bounded total phase already bound `beta`.
  The modal inequalities are compatible with the limiting boundary
  `beta->0`, `theta->pi/2`; they do not themselves create the contradiction.
- The limiting band argument uses `C Y+s X=0`, not division by `C`.
- The only apparent vanishing denominator, `sin(alpha)`, is removed using
  `X/sin(alpha)=Z/cos(alpha)` before taking the limit. Meanwhile
  `sin(c alpha)->sin(2pi/3)>0`.
- Both norm limits are finite and strictly positive: `I3hat->3pi/4` and
  `I2hat->pi/2`.
- No mass-defective isolated point is used. The contradiction applies to every
  hypothetical complete sequence on this face.

The load-bearing chain is spectral data, then band data, then the exact mass
identity with both exact norm limits. Spectral data fix `c` and the total
phase. Band data force the endpoint and the unique constant in `(3)`. Mass
data give the first contradiction. Modal data ensure the strict interior
system but are not the excluding mechanism.

## Effect on G, Xi, and PHI-SIGN

There is no complete family on this near-one face, so no sign of `G` or `Xi`
is required there. Assigning a sign to a mass-defective formal tuple would not
answer the complete-system question.

Together with the accepted alpha-zero empty wedge and the accepted uniform
near-one theorem on every fixed strip `eta<=alpha<=pi-eta`, this result covers
all alpha values for sufficiently small `m-1`. Thus every existing complete
near-one tuple lies in a strip where `G>0`, hence `Xi>0` and `Phi<0`. This
closes the branch-uniform near-one `PHI-SIGN` neighborhood, but it does not
settle arbitrary finite `m`, global `PHI-SIGN`, or global `KP-DET`.

decision_delta: The alpha->pi near-one face is exactly empty; the spectral-band subsystem forces C/(pi-alpha)->1, but the exact mass identity then has limits 0 and pi/6, so combining both empty endpoint wedges with the accepted fixed-strip theorem closes near-one PHI-SIGN while arbitrary finite-R KP-DET remains open.
