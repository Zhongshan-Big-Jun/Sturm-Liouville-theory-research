REPAIRED

# Uniform near-one positivity of G away from left collision

## Input audit

Every frozen input was verified before use.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-04-mass-g-wave/falsifier_result.md                      03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9
route-04-mass-g-wave/audit/independent_audit.json             7e56fc988a361efa5aeec7d232fb43b03b7889dacfc8ebc3d4afd6a02231c175
```

## Theorem

Fix `0<eta<pi/2`. There exists `epsilon_eta>0` such that every complete
admissible tuple in the frozen finite-interior symmetric `n=2` INF system
satisfying

```text
1<m<1+epsilon_eta,
eta<=alpha<=pi-eta
```

obeys

```text
G=Dtheta(D-c s N/C)+X Ttheta^2/C^2>0.
```

The quantifier is uniform over both moving switches. No branch-continuity or
fixed-switch assumption is required.

## 1. Compact phase closure

The strict modal domain gives

```text
0<c<1,
0<alpha<pi,
0<theta<pi/2.
```

Moreover,

```text
delta_3=atan(C/(mS)) in (0,pi/2),
delta_3<beta<delta_3+pi.
```

Consequently

```text
0<beta<3pi/2.                                      (1)
```

Thus any sequence of complete tuples with `m->1+` and
`eta<=alpha<=pi-eta` has a subsequence on which

```text
(c,alpha,beta,theta)->(c_0,alpha_0,beta_0,theta_0)
```

in the compact set

```text
[0,1] x [eta,pi-eta] x [0,3pi/2] x [0,pi/2].       (2)
```

This is the compactness needed below. In particular, switch motion cannot
make the middle phase unbounded.

## 2. Switch-uniform spectral convergence and phase scales

Let `rho_m` be the three-layer density. It takes only the values `1` and
`m^2`, independently of the switch locations. Hence

```text
1<=rho_m<=m^2,
||rho_m-1||_infinity<=m^2-1.                        (3)
```

For either the Dirichlet-Dirichlet or Dirichlet-Neumann form domain, the
Rayleigh quotient is

```text
R_rho[u]=int_0^L |u'|^2 dx / int_0^L rho |u|^2 dx.
```

Inequality `(3)` and the min-max principle give, for every eigenvalue with
the same boundary conditions and index,

```text
lambda_k(1)/m^2<=lambda_k(rho_m)<=lambda_k(1).       (4)
```

The estimate is uniform in `a` and `b`. On `L=1/2`, the first DD and second
DN uniform eigenvalues are respectively

```text
lambda_DD,1(1)=4pi^2,
lambda_DN,2(1)=9pi^2.
```

The frozen mode labels identify these with `lambda_2` and `lambda_3`.
Therefore, uniformly over the moving-switch family,

```text
lambda_2->4pi^2,
lambda_3->9pi^2,
c=sqrt(lambda_2/lambda_3)->2/3.                     (5)
```

The phase definitions contain an important factor of `m` on the middle
layer:

```text
alpha+m beta+theta=pL=m sqrt(lambda_3)L,
c(alpha+m beta+theta)=cpL=m sqrt(lambda_2)L.         (6)
```

Using `(1)`, `(5)`, and `(6)` gives the two independent total-phase limits

```text
alpha+m beta+theta->3pi/2,
c(alpha+m beta+theta)->pi,                           (7)
```

and, because `(m-1)beta->0`, also

```text
alpha+beta+theta->3pi/2,
c(alpha+beta+theta)->pi.                             (8)
```

Every convergence statement in `(5)-(8)` is uniform: otherwise an offending
sequence would contradict the switch-independent bounds `(1)` and `(4)`.

## 3. Uniform norm limits

For all sufficiently large indices in a sequence with `m->1`, equation
`(5)` gives, for example,

```text
1/2<=c<=5/6.
```

Together with `eta<=alpha<=pi-eta`, this keeps both `sin(alpha)` and
`sin(c alpha)` uniformly away from zero. Hence every term in the exact norm
formulas is continuous on the compact subsequential domain `(2)`.

Consider a convergent phase subsequence. At its `m=1` limit, `(8)` gives

```text
c_0=2/3,
alpha_0+beta_0+theta_0=3pi/2,
c_0(alpha_0+beta_0+theta_0)=pi.                     (9)
```

The transfer quantities reduce to

```text
X_0=cos(beta_0+theta_0)=-sin(alpha_0),
Y_0=sin(c_0(beta_0+theta_0))=sin(c_0 alpha_0).       (10)
```

Using the integral meaning of `Js`, `Jc`, and `J`, the exact formulas pass
continuously to

```text
I3hat_0
=Js(alpha_0)
 +int_0^beta_0 cos(theta_0+u)^2 du
 +Jc(theta_0)
=Js(alpha_0)+Jc(beta_0+theta_0)
=Js(alpha_0)+Jc(3pi/2-alpha_0)
=3pi/4,                                             (11)
```

and

```text
I2hat_0
=Js(c_0 alpha_0)
 +int_0^(c_0 beta_0) sin(c_0 theta_0+u)^2 du
 +Js(c_0 theta_0)
=Js(c_0 alpha_0)+Js(c_0(beta_0+theta_0))
=Js(c_0 alpha_0)+Js(pi-c_0 alpha_0)
=pi/2.                                              (12)
```

The scale factors agree with the frozen convention: `I3hat=p I3` and
`I2hat=cp I2`. At the uniform limits, `pL=3pi/2` and `cpL=pi`, so `(11)`
and `(12)` also equal `p` and `cp` times the corresponding half-interval
norms.

Because every convergent phase subsequence has the same limits `(11)-(12)`,
compactness proves the uniform statements

```text
I3hat->3pi/4,
I2hat->pi/2                                         (13)
```

over the entire moving-switch family under consideration.

## 4. Limiting mass equation and uniform theta separation

Pass the exact equation

```text
C^2 I2hat=c^3 s^2 I3hat
```

to any convergent subsequence using `(5)` and `(13)`. Its limit is

```text
cos(theta_0)^2 pi/2
=(2/3)^3 sin(2theta_0/3)^2 3pi/4.
```

Thus

```text
cos(theta_0)^2=(4/9)sin(2theta_0/3)^2.
```

Both sides have nonnegative square roots on `0<=theta_0<=pi/2`, so

```text
cos(theta_0)=(2/3)sin(2theta_0/3).                  (14)
```

At `theta_0=0`, equation `(14)` reads `1=0`. At `theta_0=pi/2`, it reads
`0=sqrt(3)/3`. Both are impossible. Sequential compactness now upgrades
this exclusion to a uniform one: there are `delta_eta>0` and
`epsilon_1>0` such that every complete tuple with

```text
1<m<1+epsilon_1,
eta<=alpha<=pi-eta
```

satisfies

```text
delta_eta<=theta<=pi/2-delta_eta.                   (15)
```

Indeed, failure of `(15)` would produce an admissible sequence with a
subsequence converging to one of the two excluded endpoints.

## 5. Uniform positivity and divergence

Along a convergent subsequence, equations `(8)-(10)` give

```text
D_0=sin(beta_0+theta_0)=-cos(alpha_0),
N_0=cos(c_0(beta_0+theta_0))=-cos(2alpha_0/3).       (16)
```

Equation `(14)` is exactly

```text
c_0 sin(c_0 theta_0)/cos(theta_0)=1.                (17)
```

Therefore

```text
U=D-c s N/C
 ->cos(2alpha_0/3)-cos(alpha_0).                    (18)
```

Since cosine is strictly decreasing on `(0,pi)`, the continuous function

```text
h(alpha)=cos(2alpha/3)-cos(alpha)
```

has a strictly positive minimum `u_eta` on
`[eta,pi-eta]`. If `U>=u_eta/2` failed arbitrarily close to `m=1`, an
offending sequence and `(18)` would contradict this minimum. Hence, after
possibly decreasing `epsilon_1`,

```text
U>=u_eta/2>0                                        (19)
```

uniformly.

Now set

```text
P=tan(theta)+c cot(c theta).
```

For `m` sufficiently close to `1`, equations `(5)` and `(15)` put
`(c,theta)` in a compact subset of `(0,1)x(0,pi/2)`. In particular,

```text
P>=tan(delta_eta)>0,
|Ttheta|<=1,
r=m^2/(m^2-1)->+infinity.
```

Consequently

```text
Dtheta=rP-Ttheta->+infinity                         (20)
```

uniformly. Equations `(19)-(20)` imply

```text
Dtheta U->+infinity                                 (21)
```

uniformly.

Finally, `(15)` gives `C>=sin(delta_eta)`. Also

```text
|X|=|C cos(beta)-mS sin(beta)|<=1+m,
|Ttheta|<=1.
```

Thus, for `m<2`,

```text
|X Ttheta^2/C^2|<=3/sin(delta_eta)^2.               (22)
```

The remainder is uniformly bounded, while `(21)` diverges positively.
Combining `(21)` and `(22)` proves the theorem.

## Denominator and boundary audit

- The modal inequality gives the switch-independent bound `beta<3pi/2`.
- The min-max estimate uses only `1<=rho_m<=m^2` and is uniform over all
  moving interfaces.
- The assumptions on `alpha`, together with `c->2/3`, keep
  `sin(alpha)` and `sin(c alpha)` uniformly nonzero in the norm formulas.
- The limiting mass equation excludes both `theta` endpoints before any
  division by `C`, `s`, or `cot(c theta)` is used.
- Uniform separation `(15)` then makes `C`, `s`, and `c theta` uniformly
  nonzero and all terms in `G` uniformly defined.
- The theorem remains strictly inside the finite-interior modal component.
  It makes no claim on the excluded switch-collision face `alpha=0`.

## Remaining scope

This repair establishes only a branch-uniform near-one theorem under the
fixed separation `eta<=alpha<=pi-eta`. It does not control a simultaneous
limit `alpha->0`, does not prove `G>=0` for arbitrary finite `R`, and does not
close `PHI-SIGN` or `KP-DET`.

decision_delta: The previously downgraded near-one claim is repaired uniformly over moving switches: for each fixed eta>0, complete admissible tuples with eta<=alpha<=pi-eta have G>0 when m-1 is sufficiently small; left collision, global G-sign, PHI-SIGN, and KP-DET remain open.
