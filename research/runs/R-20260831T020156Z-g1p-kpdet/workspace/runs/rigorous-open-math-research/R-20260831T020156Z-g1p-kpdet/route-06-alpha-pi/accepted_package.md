STRICT

# Accepted alpha-pi exclusion and complete near-one mechanism

## Audit bindings

- W8 SHA256:
  `b0f66b3090280f946d2ec4d49df54eed942ae56913aa77d286e1ce8e028881cb`.
- W9 SHA256:
  `ece86c1ff05afa17a3fdb6f9bab94e31b69cbdf38190e2a6c1d1b77a10e5b514`.
- Joint audit SHA256:
  `6cf59c106103464c8704ab4aafea8c1833d9437199472b4411727ccc956fc514`.

## P8. Exact alpha-pi empty wedge

There is no complete admissible sequence with

```text
m->1+,
alpha->pi.
```

Equivalently, there exist `epsilon_pi,delta_pi>0` such that no complete tuple
lies in

```text
1<m<1+epsilon_pi,
pi-delta_pi<alpha<pi.
```

The spectral and band system forces

```text
theta->pi/2,
beta->0,
X/(pi-alpha)->-1,
C/(pi-alpha)->1,
beta/(pi-alpha)->2,
I3hat->3pi/4,
I2hat->pi/2.
```

The exact mass residual therefore satisfies

```text
Delta_M=C^2 I2hat-c^3 s^2 I3hat->-pi/6.
```

After shrinking the wedge, one has the uniform strict bound
`Delta_M<-pi/12`, which excludes the complete equation `Delta_M=0`.

## P9. Complete near-one phase-sign mechanism

Let the accepted alpha-zero wedge have constants `epsilon_0,delta_0`, and
let the accepted alpha-pi wedge have `epsilon_pi,delta_pi`. Choose

```text
eta=min(delta_0,delta_pi,pi/4)/2
```

and let `epsilon_eta` be the constant from the accepted fixed-strip theorem.
Then

```text
epsilon_*=min(epsilon_0,epsilon_pi,epsilon_eta)>0
```

has the following property: every complete admissible tuple with

```text
1<m<1+epsilon_*
```

lies in `eta<=alpha<=pi-eta` and satisfies `G>0`. The exact identity

```text
Phi=X G-Dtheta Dalpha
```

and the strict signs

```text
X<0,
Dtheta>0,
Dalpha>0
```

give `Phi<0`, hence the branch-local KP determinant sign in this near-one
neighborhood.

This is a new exact mechanism and quantifier assembly. It is compatible with
the previously accepted near-one negative-inertia premise and does not claim
new branch existence.

## Exact remaining gap

The result is local in `m`. Arbitrary finite `m>1`, global `G>=0`, global
`Xi>0`, global `PHI-SIGN`, and complete KP-DET remain open.
