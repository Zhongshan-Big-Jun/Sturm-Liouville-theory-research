PARTIAL

# Exact layer-coefficient localization of the mass-to-G obstruction

## Input and scope audit

Before use, the five bound inputs were verified against the packet. Their
SHA256 values are, in packet order,

```text
67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3
6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
3bace4993b5a14c55950043322dd410e65f7f0135df5e03c95dde18a5ad6b3dd
```

Work on the complete strict phase system in the bound inputs. In particular,

```text
m>1, 0<c<1, alpha>0, beta>0, theta>0,
sin(alpha)>0, sin(c alpha)>0, s=sin(c theta)>0,
C=cos(theta)>0, X<0, Y=-sX/C>0.
```

The audited spectral, band, and mass-slope equations are assumed. No
numerical statement is used.

## Theorem

Define the positive quadratic phase forms

```text
Q3=alpha(X^2+Z^2)+beta(m Z^2+X^2/m)+theta,
Q2=alpha(Y^2+T^2)+beta(m T^2+Y^2/m)+theta,
```

and the three layer coefficients

```text
A=C^2(Y^2+T^2)-c^2 s^2(X^2+Z^2),
B=C^2(m T^2+Y^2/m)-c^2 s^2(m Z^2+X^2/m),
H=C^2-c^2 s^2.
```

Put

```text
Lalpha=csc(c alpha)^2-c^2 csc(alpha)^2,
mu=m-1/m>0.
```

Then the audited mass-slope equation is losslessly equivalent to each of

```text
C^2 Q2=c^2 s^2 Q3,                                      (1)
alpha A+beta B+theta H=0,                                (2)
(alpha+m beta)Lalpha+theta H/(s^2 X^2)
  =beta mu(1-c^2)>0.                                     (3)
```

Moreover,

```text
A=s^2 X^2 Lalpha,                                        (4)
B=s^2 X^2[m Lalpha-mu(1-c^2)].                           (5)
```

Consequently every mass-admissible phase point has a strictly mixed-sign
coefficient triple `(A,B,H)`: at least one coefficient is positive and at
least one is negative. More quantitatively,

```text
H<=0 implies
Lalpha>=beta mu(1-c^2)/(alpha+m beta)>0,                 (6)

Lalpha<=0 implies
H>=s^2 X^2 beta mu(1-c^2)/theta>0.                       (7)
```

Equality in the first weak inequality in `(6)` occurs exactly when `H=0`.
Equality in the first weak inequality in `(7)` occurs exactly when
`Lalpha=0`. Thus `(6)` and `(7)` retain their equality cases and exclude the
entire quadrant `Lalpha<=0, H<=0`.

This is a strict sufficient reduction for the desired middle/right sign. On
the spectral and band system, it is enough to prove the smaller sign-coherence
lemma

```text
G<0 implies
  (A>0 and B>0 and H>0)
  or
  (A<0 and B<0 and H<0).                                (SC)
```

Indeed, `(SC)` contradicts the proved mixed-sign theorem. Hence `(SC)` would
exclude `G<0` and prove `G>=0`. Combined with
`Xi=X^2 G-r K Dtheta`, `K<0`, and `Dtheta>0`, it would then give `Xi>0`.

## Derivation

The following calculation also independently audits all factors in `(1)`.
For the upper residual, the transfer definitions give

```text
partial_beta X=-m Z,
partial_beta Z=X/m,
partial_theta X=-D,
D Z+X partial_theta Z=1.
```

On `F3=X cos(alpha)-Z sin(alpha)=0`, division by `sin(alpha)>0`
and substitution `cos(alpha)=Z sin(alpha)/X` yield

```text
E3(F3)/sin(alpha)=-Q3/X.                                (8)
```

For the lower residual, temporarily write its arguments as `(A0,B0,H0)`.
The analogous transfer identities are

```text
partial_B0 Y=m T,
partial_B0 T=-Y/m,
partial_H0 Y=N,
N T-Y partial_H0 T=1.
```

On `F2=Y cos(A0)+T sin(A0)=0`, division by `sin(A0)>0` and
substitution `cos(A0)=-T sin(A0)/Y` give

```text
(A0 partial_A0+B0 partial_B0+H0 partial_H0)F2/sin(A0)
=-[A0(Y^2+T^2)+B0(m T^2+Y^2/m)+H0]/Y.
```

At `(A0,B0,H0)=(c alpha,c beta,c theta)`, this is

```text
E2(F2)/sin(c alpha)=-c Q2/Y.                            (9)
```

Insert `(8)` and `(9)` into the audited mass-slope equation

```text
C E2(F2)/sin(c alpha)+c^3 s E3(F3)/sin(alpha)=0.
```

Using `Y=-sX/C` and multiplying by the nonzero factor `sX/c` gives exactly
`(1)`. Expanding `(1)` by the positive phase weights gives `(2)`.

The spectral equations give

```text
Z=X cot(alpha),
T=-Y cot(c alpha),
```

while the band equation gives `C^2Y^2=s^2X^2`. Therefore

```text
A
=C^2Y^2 csc(c alpha)^2-c^2s^2X^2 csc(alpha)^2
=s^2X^2 Lalpha,
```

which is `(4)`. Direct subtraction, without any trigonometric division,
gives

```text
B-mA
=-(m-1/m)C^2Y^2+(m-1/m)c^2s^2X^2
=-mu(1-c^2)s^2X^2.
```

This proves `(5)`. Substitute `(4)` and `(5)` into `(2)` and divide by
`s^2X^2>0`; the result is `(3)`. Its right side is strictly positive because
`beta>0`, `m>1`, and `0<c<1`. The conditional bounds `(6)` and `(7)` now
follow by moving the term of known weak sign to the right. Their stated
equality conditions follow directly from `(3)`.

Finally, `(2)` has positive weights `alpha`, `beta`, and `theta`. If all of
`A,B,H` were nonnegative, or all were nonpositive, `(2)` would force all
three to vanish. But `A=0` and `(5)` imply

```text
B=-mu(1-c^2)s^2X^2<0,
```

a contradiction. Hence the coefficient triple is strictly mixed-sign.

## Division, equality, and boundary audit

- Division by `sin(alpha)` and `sin(c alpha)` is valid on the strict modal
  domain.
- Division by `Y`, `X`, `s`, `C`, `c`, and `s^2X^2` is valid because
  `Y>0`, `X<0`, `s>0`, `C>0`, `c>0`.
- No division by `cos(beta)`, `sin(beta)`, `cos(c beta)`, or
  `sin(c beta)` occurs. All of their zero sets remain covered.
- Multiplication by `sX/c` in an equality is reversible. Its negative sign
  is irrelevant to the equivalence and is not used to infer an inequality.
- The strict positivity on the right of `(3)` uses the finite-interior
  hypotheses `beta>0`, `m>1`, and `c<1`. It degenerates only at excluded
  faces `beta=0`, `m=1`, or `c=1`.
- The theorem makes no assertion on switch-collision or mode-index boundary
  faces excluded by the packet.

## First unresolved step

The layer balance does not itself relate the sign of `G` to the signs of
`A`, `B`, and `H`. The first unresolved load-bearing step is `(SC)`, or any
weaker implication from `G<0` that puts `(A,B,H)` in one closed same-sign
orthant. Without such a propagation statement, neither `G>=0` nor the sharp
lower bound `G>r K Dtheta/X^2` is proved. Therefore `Xi>0`, `PHI-SIGN`, and
`KP-DET` remain open.

decision_delta: The exact mass constraint is localized to a strict mixed-sign balance of three explicit layer coefficients, with sharp conditional bounds (6)-(7); proving G>=0 is reduced to the smaller unresolved sign-coherence implication (SC).
