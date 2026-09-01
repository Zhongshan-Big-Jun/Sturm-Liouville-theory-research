PASS

# Fresh re-audit of the W5 near-one repair

Re-audit ID: `REAUDIT-W5-NEARONE-01`.

## Hash verification

All five bound inputs were hashed before review and match the immutable
packet.

| Path | Verified SHA256 |
|---|---|
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-01-transfer-schur/derivation.md` | `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3` |
| `route-04-mass-g-wave/falsifier_result.md` | `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9` |
| `route-04-mass-g-wave/audit/independent_audit.json` | `7e56fc988a361efa5aeec7d232fb43b03b7889dacfc8ebc3d4afd6a02231c175` |
| `route-04-mass-g-wave/repair/near_one_repair.md` | `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314` |

## 1. Compactness and uniform spectral limits

The modal inequality

```text
delta_3<beta<delta_3+pi,
0<delta_3<pi/2
```

implies the switch-independent bound

```text
0<beta<3pi/2.
```

Together with `0<c<1`, `eta<=alpha<=pi-eta`, and
`0<theta<pi/2`, this gives the claimed compact phase closure for every
sequence with `m->1+`.

For either DD or DN boundary conditions,

```text
R_rho[u]=int |u'|^2/int rho|u|^2.
```

Since `1<=rho_m<=m^2`, every trial subspace satisfies

```text
R_1[u]/m^2<=R_rho_m[u]<=R_1[u].
```

Min-max therefore gives, uniformly in both moving switches,

```text
lambda_k(1)/m^2<=lambda_k(rho_m)<=lambda_k(1).
```

The frozen mode labels are the first DD and second DN modes. On `L=1/2`,
their uniform-density eigenvalues are

```text
lambda_DD,1=4pi^2,
lambda_DN,2=9pi^2.
```

Thus

```text
lambda_2->4pi^2,
lambda_3->9pi^2,
c->2/3
```

uniformly over moving switches. This verifies the index identification and
does not require a fixed-interface perturbation theorem.

## 2. Phase lengths and all factors of m

From

```text
alpha=p a,
beta=(p/m)(b-a),
theta=p(L-b),
p=m sqrt(lambda_3),
```

one obtains exactly

```text
alpha+m beta+theta=pL=m sqrt(lambda_3)L,
c(alpha+m beta+theta)=cpL=m sqrt(lambda_2)L.
```

Hence the spectral limits give

```text
alpha+m beta+theta->3pi/2,
c(alpha+m beta+theta)->pi.
```

Because `beta<3pi/2`, the difference `(m-1)beta` tends uniformly to zero,
so

```text
alpha+beta+theta->3pi/2,
c(alpha+beta+theta)->pi.
```

Every factor of `m` in the repair is correct.

## 3. Independent norm-limit calculation

The eigenvalue limit places `c` in a compact subinterval of `(0,1)`. Since
`alpha` stays in `[eta,pi-eta]`, both `sin(alpha)` and `sin(c alpha)` are
uniformly separated from zero. The exact norm formulas may therefore be
passed to every convergent phase subsequence.

At `m=1`, the total-phase identities give

```text
X_0=cos(beta_0+theta_0)=-sin(alpha_0),
Y_0=sin(c_0(beta_0+theta_0))=sin(c_0 alpha_0),
c_0=2/3.
```

Using `Js(t)=int_0^t sin(u)^2 du` and
`Jc(t)=int_0^t cos(u)^2 du`, the upper norm becomes

```text
I3hat_0
=Js(alpha_0)+Jc(beta_0+theta_0)
=Js(alpha_0)+Jc(3pi/2-alpha_0)
=3pi/4.
```

Likewise, the lower norm becomes

```text
I2hat_0
=Js(c_0 alpha_0)+Js(c_0(beta_0+theta_0))
=Js(c_0 alpha_0)+Js(pi-c_0 alpha_0)
=pi/2.
```

The scale convention is also correct. At uniform density, the two physical
half-interval integrals equal `L/2=1/4`, while `p=3pi` and `cp=2pi`.
Therefore

```text
p I3=3pi/4,
cp I2=pi/2,
```

which independently reproduces the same limits. Since every convergent
phase subsequence has these values, compactness upgrades them to uniform
limits over the whole moving-switch family.

## 4. Limiting mass equation and endpoint separation

Passing

```text
C^2 I2hat=c^3 s^2 I3hat
```

to a phase cluster point gives

```text
cos(theta_0)^2 pi/2
=(2/3)^3 sin(2theta_0/3)^2 3pi/4,
```

or

```text
cos(theta_0)=(2/3)sin(2theta_0/3).
```

The nonnegative square root is legitimate on the closed phase interval.
At `theta_0=0`, this equation would give `1=0`; at `theta_0=pi/2`, it
would give `0=sqrt(3)/3`. Thus both endpoints are excluded before dividing
by `C`, `s`, or `sin(c theta)`.

If no uniform endpoint separation existed, an offending sequence would have
a compact subsequence with one of those two endpoint limits, contradicting
the limiting mass equation. The sequential argument therefore does yield
uniform constants `delta_eta>0` and `epsilon_1>0`.

## 5. Uniform positivity of G

At every phase cluster point,

```text
D_0=sin(beta_0+theta_0)=-cos(alpha_0),
N_0=cos(c_0(beta_0+theta_0))=-cos(2alpha_0/3).
```

The limiting mass relation gives

```text
c_0 sin(c_0 theta_0)/cos(theta_0)=1.
```

Consequently

```text
U=D-c s N/C
 ->cos(2alpha_0/3)-cos(alpha_0).
```

For `alpha_0` in `[eta,pi-eta]`, one has
`0<2alpha_0/3<alpha_0<pi`. Strict decrease of cosine and compactness give a
uniform minimum `u_eta>0`, and the sequential contradiction argument
correctly upgrades this to `U>=u_eta/2` for all sufficiently small `m-1`.

Uniform theta separation and `c->2/3` place `(c,theta)` in a compact subset
of `(0,1)x(0,pi/2)`. Thus

```text
P=tan(theta)+c cot(c theta)>=tan(delta_eta)>0,
|Ttheta|<=1,
r=m^2/(m^2-1)->+infinity,
Dtheta=rP-Ttheta->+infinity
```

uniformly. Hence `Dtheta U->+infinity` uniformly. On the other hand,

```text
C>=sin(delta_eta),
|X|<=1+m<3,
|Ttheta|<=1,
```

so

```text
|X Ttheta^2/C^2|<=3/sin(delta_eta)^2.
```

The remainder is uniformly bounded while the leading term diverges
positively. Therefore `G>0` uniformly for the stated near-one region.

## 6. Verdict and scope

The repair closes the sole gap identified by the prior audit. The order of
operations is valid: compactness and norm convergence lead to the mass-limit
equation, both theta endpoints are excluded, and only then are the relevant
denominators used. No unsupported branch-continuity assumption remains.

The theorem fixes `0<eta<pi/2`, so it excludes `alpha->0`. It does not claim
`G>=0` for arbitrary finite `R`, and it does not prove `PHI-SIGN` or
`KP-DET`. Those global obligations remain open.
