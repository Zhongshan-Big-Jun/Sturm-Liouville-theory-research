PASS

# Fresh independent audit of W7 alpha-collision exclusion

Audit ID: `AUDIT-W7-ALPHA-COLLISION-01`.

## Hash verification

All five packet-bound inputs were hashed independently before review, and every SHA256 value matched.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-04-mass-g-wave/repair/near_one_repair.md                8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314
route-04-mass-g-wave/repair/reaudit.json                      3f88a6ed8cf6da7f7adc41a195776fbfa9f00c8cec97153156a98f773a0c573d
route-05-alpha-collision/falsifier_result.md                  191b0a1cd621b8f8451647a5273a2f79efd0d57b71e3a7ba570e8644cae6e044
```

## Independent algebra

Assume a sequence of complete admissible tuples with `m_j->1+` and `alpha_j->0`. The one-zero condition gives

```text
0<beta_j<delta_3,j+pi<3pi/2.
```

Thus `(c_j,beta_j,theta_j)` has a compactly convergent subsequence. Since `1<=rho_j<=m_j^2`, the min-max principle gives, uniformly in both switch positions,

```text
lambda_k(1)/m_j^2<=lambda_k(rho_j)<=lambda_k(1).
```

The frozen mode labels are the first DD and second DN half modes, so

```text
lambda_2,j->4pi^2,
lambda_3,j->9pi^2,
c_j->2/3.
```

The exact phase identity contains the required middle-layer factor:

```text
alpha_j+m_j beta_j+theta_j=p_j L=m_j sqrt(lambda_3,j)L->3pi/2.
```

Because `(m_j-1)beta_j->0` and `alpha_j->0`, this yields

```text
beta_j+theta_j->3pi/2,
c_j(beta_j+theta_j)->pi.
```

The two apparent left-layer singularities are exactly removable. The spectral equations imply, eventually with both cosines nonzero,

```text
X_j=Z_j tan(alpha_j),
Y_j=-T_j tan(c_j alpha_j).
```

Hence the two terms are exactly

```text
m_j^2 X_j^2 Js(alpha_j)/sin(alpha_j)^2
=m_j^2 Z_j^2 Js(alpha_j)/cos(alpha_j)^2,

m_j^2 Y_j^2 Js(c_j alpha_j)/sin(c_j alpha_j)^2
=m_j^2 T_j^2 Js(c_j alpha_j)/cos(c_j alpha_j)^2.
```

Here `Z_j` and `T_j` are bounded by the exact transfer formulas, `m_j->1`, `c_j->2/3`, and

```text
Js(t)=t^3/3+O(t^5).
```

Therefore both terms tend to zero. This calculation retains every factor of `m`, keeps `c` inside the second phase, and introduces no missing factor of `c` in `I2hat`.

Using the integral definition

```text
J(A,B;t)=integral_0^t (A cos(u)+B sin(u))^2 du,
```

the remaining terms converge as follows:

```text
I3hat_j
->integral_0^beta_0 cos(theta_0+u)^2 du+Jc(theta_0)
=Jc(beta_0+theta_0)
=Jc(3pi/2)
=3pi/4,

I2hat_j
->integral_0^((2/3)beta_0) sin((2/3)theta_0+u)^2 du
  +Js((2/3)theta_0)
=Js((2/3)(beta_0+theta_0))
=Js(pi)
=pi/2.
```

These are full `I3hat` and `I2hat` limits, not only limits of selected layers.

Let `theta_j->theta_0`, `C_0=cos(theta_0)`, and `s_0=sin(2theta_0/3)`. The exact mass equation gives

```text
C_0^2 pi/2=(2/3)^3 s_0^2 3pi/4,
C_0^2=(4/9)s_0^2.
```

On `0<=theta_0<=pi/2`, both `C_0` and `s_0` are nonnegative, so the correct square-root choice is

```text
C_0=(2/3)s_0.
```

The endpoints are impossible: `theta_0=0` gives `1=0`, while `theta_0=pi/2` gives `0=(2/3)sin(pi/3)`. Thus `C_0>0`, `s_0>0`, and

```text
s_0/C_0=3/2.
```

The exact transfer equations independently give

```text
Z_j->sin(beta_0+theta_0)=sin(3pi/2)=-1,
T_j->cos((2/3)(beta_0+theta_0))=cos(pi)=-1.
```

Since every `alpha_j>0`, the spectral equations then yield

```text
X_j/alpha_j=Z_j tan(alpha_j)/alpha_j->-1,
Y_j/alpha_j=-T_j tan(c_j alpha_j)/alpha_j->2/3.
```

Finally, divide the exact band equation `Y_j=-s_j X_j/C_j` by `alpha_j`. The mass equation has already established `C_0>0`, so passage to the limit is valid and gives

```text
2/3=s_0/C_0=3/2,
```

a contradiction. The signs in this last step are correct: the two minus signs from the band equation and `X_j/alpha_j->-1` cancel.

## Quantifiers and scope

The sequential statement is equivalent to a uniform empty wedge. If no pair `(epsilon_0,delta_0)` existed, choosing a complete tuple with

```text
1<m_j<1+1/j,
0<alpha_j<1/j
```

would produce the excluded sequence. Conversely, an empty wedge excludes every such sequence. This reasoning quantifies only over complete admissible tuples and assumes no branch existence or continuation.

The ratio claim also follows from the wedge and needs no downgrade. Along any complete sequence with `m_j->1+`, eventually `alpha_j>=delta_0`, hence

```text
alpha_j/(m_j-1)>=delta_0/(m_j-1)->+infinity.
```

This assertion is conditional on such complete tuples existing; it does not prove their existence.

The theorem excludes only the simultaneous near-one left-collision regime. It proves no sign for `G`, `Xi`, or `Phi` at arbitrary finite `R`, and it does not prove `PHI-SIGN` or `KP-DET`.

## Verdict

`PASS`. No critical error or repairable load-bearing gap was found. The spectral compactness, both removable norm singularities, both full norm limits, the mass-equation sign choice, the endpoint exclusions, the transfer limits, the band contradiction, and the uniform quantifier upgrade all check independently.

decision_delta: The simultaneous regime `m->1+`, `alpha->0` is rigorously excluded, equivalently by a uniform empty wedge. The result does not extend to arbitrary finite `R` and leaves `G`, `Xi`, `PHI-SIGN`, and `KP-DET` open outside that wedge.
