PARTIAL

# Exact mass-slope propagation and a smaller sufficient residual

## Assumptions

Use exactly the frozen W1 phase system. In particular,

```text
m>1,
0<c<1,
0<alpha<pi,
0<c alpha<pi,
0<theta<pi/2,
0<c theta<pi/2,
X<0,
Y=-sX/C>0,
Dtheta>0.
```

The symbols `X,Z,D,Y,T,N,C,s,r,Ttheta,Dtheta` have the definitions in the
listed W1 derivation, with

```text
r=m^2/(m^2-1),
Ttheta=S C+c s Cc.
```

No quotient-monotonicity premise is used.

## 1. Exact propagation of the mass identity

Define the two spectral residuals

```text
F3(alpha,beta,theta)
 =X cos(alpha)-Z sin(alpha),

F2(A,B,H)
 =[sin(H)cos(B)+m cos(H)sin(B)]cos(A)
  +[cos(H)cos(B)-sin(H)sin(B)/m]sin(A).
```

Thus the spectral equations are

```text
F3(alpha,beta,theta)=0,
F2(c alpha,c beta,c theta)=0.
```

Let

```text
E3=alpha partial_alpha+beta partial_beta+theta partial_theta,
E2=A partial_A+B partial_B+H partial_H.
```

The exact norm formulas admit the derivative-free reformulation

```text
I3hat=-m^2 X E3(F3)/(2 sin(alpha)),                 (M3)
I2hat=-m^2 Y E2(F2)/(2 sin(c alpha)).              (M2)
```

Here is a direct audit. For the right-Neumann shape `y=phi_3`, normalized by
`y(L)=1,y'(L)=0`, differentiation of

```text
-y''=lambda rho y
```

with respect to `lambda` gives

```text
[y y_lambda'-y' y_lambda]_0^L=-int_0^L rho y^2 dx.
```

At the eigenvalue, `y(0)=0`, `y'(0)=pX/sin(alpha)`,
`lambda=p^2/m^2`, and `I3hat=p int rho y^2`. Since changing `p` at fixed
physical switches applies `E3`, this proves `(M3)`.

For the Dirichlet shape use `g=phi_2/(cp)`. Then
`g(L)=0,g'(L)=-1`, `g'(0)=Y/sin(c alpha)`, and changing `cp` at fixed
physical switches applies `E2`. The same Lagrange identity, together with
`I2hat=cp int rho phi_2^2`, proves `(M2)`.

Substitute `(M2)` and `(M3)` into the exact mass equation

```text
C^2 I2hat=c^3 s^2 I3hat
```

and use `Y=-sX/C`. The mass constraint is exactly equivalent to

```text
C E2(F2)/sin(c alpha)
 +c^3 s E3(F3)/sin(alpha)=0.                       (M-slope)
```

Thus every integral `J`, `Js`, and `Jc` in the normalization constraint has
been propagated into radial derivatives of the two exact spectral
residuals. No sign is inferred from `(M-slope)` alone.

## 2. A strictly smaller middle/right residual

Set

```text
U=D-c s N/C,
K=c C T/s-Z,
G=Dtheta U+X Ttheta^2/C^2.                          (G)
```

The two spectral equations give

```text
K=X[c cot(c alpha)-cot(alpha)].                     (K-id)
```

For `f(t)=t cot(t)` on `(0,pi)`,

```text
f'(t)=[sin(t)cos(t)-t]/sin(t)^2<0.
```

Indeed, `t-sin(t)cos(t)` vanishes at zero and has derivative
`2 sin(t)^2>0`. Since `0<c alpha<alpha<pi`, `(K-id)` implies

```text
c cot(c alpha)-cot(alpha)>0,
K<0.                                                (K-sign)
```

Now use the coordinator definitions

```text
Psi=X^2 U-rK,
Xi=Dtheta Psi+X^3 Ttheta^2/C^2.
```

Direct collection gives the exact identity

```text
Xi=X^2 G-r K Dtheta.                                (Xi-split)
```

By `X^2>0`, `r>0`, `Dtheta>0`, and `(K-sign)`, the second summand in
`(Xi-split)` is strictly positive. Consequently the strictly smaller,
non-equivalent sufficient inequality

```text
G>=0                                                (G-sign)
```

would prove `Xi>0`, hence `Phi<0`. Unlike `Xi`, `G` contains neither the
left spectral penalty `K` nor `alpha`; it is a middle/right residual. The
mass constraint is now available in the exact slope form `(M-slope)` for
attacking `(G-sign)`.

## 3. Denominator and boundary audit

- Division by `sin(alpha)` and `sin(c alpha)` is valid because both angles
  lie strictly in `(0,pi)`.
- Division by `C`, `s`, and `X` is valid because `C>0`, `s>0`, and `X<0`.
- `r` is finite and positive because `m>1`.
- `Dtheta>0` is the audited P1 pivot.
- No division by `cos(beta)`, `sin(beta)`, `cos(c beta)`, or
  `sin(c beta)` occurs. Their zero sets remain included.
- The switch-collision and mode-index boundary faces excluded by the frozen
  contract are not reintroduced. The argument makes no assertion on those
  faces.
- No numerical observation is used as proof.

## First unresolved load-bearing step

Prove that the complete spectral, band, modal-domain, and mass-slope system
forces `(G-sign)`, or else determine a sharp negative lower bound for `G`
that is still strictly above `r K Dtheta/X^2`. The present derivation does
not establish either implication. Therefore `PHI-SIGN` and `KP-DET` remain
open.

decision_delta: The normalization equation is reduced exactly to `(M-slope)`, and `PHI-SIGN` is reduced to proving the new sufficient middle/right inequality `G>=0`; the missing mass-to-G sign bridge is the first unresolved step.
