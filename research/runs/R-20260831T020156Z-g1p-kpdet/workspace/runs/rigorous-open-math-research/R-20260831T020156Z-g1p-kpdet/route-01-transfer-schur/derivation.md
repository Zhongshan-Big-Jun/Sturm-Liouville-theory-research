RIGOROUS_PARTIAL_RESULT

# Exact three-layer phase reduction of the KP Schur margin

## 1. Scope and result

Work only on the prescribed finite-interior, symmetric, n=2 INF half-string.
The density on `[0,L]`, `L=1/2`, is `(R,1,R)` with switches

```text
0<a<b<L.
```

The calculation below proves an exact equivalence

```text
S_KP<0  if and only if  Phi<0,                         (1)
```

where `Phi` is an explicit elementary trigonometric expression on the exact
spectral and band constraint set. It removes every Green kernel, Wronskian,
and normalization amplitude from the remaining obligation. It does not prove
the sign of `Phi`, so KP-DET remains open.

## 2. Phase coordinates and modal domain

Put

```text
m=sqrt(R)>1,
p=sqrt(lambda_3 R),
q=p/m,
c=sqrt(lambda_2/lambda_3) in (0,1),
alpha=p a,
beta=q(b-a),
theta=p(L-b).
```

The corresponding lambda_2 phases are `c alpha`, `c beta`, and `c theta`.
Use the abbreviations

```text
S=sin(theta),       C=cos(theta),
s=sin(c theta),     Cc=cos(c theta).
```

This is exactly the accepted parent phase convention under

```text
eps=1/m,
p1=c alpha,
p2=c beta,
p3=c theta,
tau_parent=1/c,
(p1t,p2t,p3t)=(alpha,beta,theta).
```

Thus the present transfer system is a change of notation, not a different
three-layer model.

The mode indices and the switch signs imply the strict phase domain

```text
0<alpha<pi,
0<c alpha<pi,
0<theta<pi/2,
0<c theta<pi/2.                                      (2)
```

The lambda_3 mode has exactly one zero in `(a,b)`. Its right-Neumann
middle-layer shape is

```text
u -> C cos(u)-m S sin(u),  0<=u<=beta.
```

If

```text
delta_3=atan(C/(m S)) in (0,pi/2),
```

then the exact one-zero condition is

```text
delta_3<beta<delta_3+pi.                              (3)
```

The positive first Dirichlet mode has no middle-layer zero. Its right-Dirichlet
middle shape is

```text
u -> s cos(u)+m Cc sin(u),  0<=u<=c beta.
```

Thus, with

```text
delta_2=pi-atan(s/(m Cc)) in (pi/2,pi),
```

the exact no-zero condition is

```text
0<c beta<delta_2.                                     (4)
```

These statements use only the two half-mode indices. In particular, they do
not assume the desired Hessian sign.

## 3. Exact transfer shapes

Normalize two right boundary shapes by

```text
phi_3(L)=1,       phi_3'(L)=0,
phi_2(x)=sin(c p(L-x)) on [b,L].
```

Backward propagation through the middle layer gives

```text
X=C cos(beta)-m S sin(beta),
Z=S cos(beta)+(C/m) sin(beta),
D=S cos(beta)+m C sin(beta),                         (5)

Y=s cos(c beta)+m Cc sin(c beta),
T=Cc cos(c beta)-(s/m) sin(c beta),
N=Cc cos(c beta)-m s sin(c beta).                    (6)
```

Here

```text
phi_3(a)=X,                 phi_3'(a)=p Z,
phi_2(a)=Y,                 phi_2'(a)=-c p T.
```

The two exact spectral equations are therefore

```text
X cos(alpha)-Z sin(alpha)=0,                         (E_DN)
Y cos(c alpha)+T sin(c alpha)=0.                     (E_DD)
```

Let the half-normalized eigenfunctions be

```text
w=A phi_3,   A<0,
v=Bv phi_2,  Bv>0.
```

The band equations `w(a)=c v(a)` and `w(b)=-c v(b)` give

```text
A/Bv=-c s/C,
Y=-s X/C.                                            (E_band)
```

Consequently

```text
X<0,  Y>0.                                           (7)
```

For completeness, the normalization part of the band system is also
elementary. Define

```text
Js(t)=t/2-sin(2t)/4,
Jc(t)=t/2+sin(2t)/4,
J(A0,B0;t)=A0^2 Jc(t)+B0^2 Js(t)+A0 B0 sin(t)^2.
```

Then

```text
I3hat=
  m^2 X^2 Js(alpha)/sin(alpha)^2
  +m J(C,-m S;beta)
  +m^2 Jc(theta),

I2hat=
  m^2 Y^2 Js(c alpha)/sin(c alpha)^2
  +m J(s,m Cc;c beta)
  +m^2 Js(c theta).                                  (8)
```

Indeed, the half masses of `phi_3` and `phi_2` are

```text
I3=I3hat/p,
I2=I2hat/(c p).
```

Since `A=-I3^(-1/2)` and `Bv=I2^(-1/2)`, the band equation at `b` is
equivalent to the exact mass identity

```text
C^2 I2hat=c^3 s^2 I3hat.                             (E_mass)
```

Equations `(E_DN)`, `(E_DD)`, `(E_band)`, and `(E_mass)`, together with
the strict mode domain `(2)-(4)`, are the complete phase constraints used
below. The physical variables are reconstructed by

```text
p=(alpha+m beta+theta)/L,
a=alpha/p,
b=(alpha+m beta)/p,
lambda_3=p^2/R,
lambda_2=c^2 p^2/R.
```

## 4. Audit of the direct theorem gamma_2>b_0

Let `Q=w/v`. On the final layer,

```text
Q(b)=-c,
Q'(b)=-c p[tan(theta)+c cot(c theta)].                (9)
```

The Wronskian in the sector formula is the Wronskian of the whole-string
normalized modes. Since `v=sqrt(2)u_2` on the half-string,

```text
W=u_2^2 Q'=v^2 Q'/2.
```

Therefore the factor in the penalty is exactly

```text
gamma_2=2c |Q'(b)|/[lambda_2(R-1)v(b)^2].             (10)
```

There is no missing factor of `2`. Also

```text
lambda_2=c^2 p^2/R,
v(b)=Bv s.
```

Set

```text
r=R/(R-1)=m^2/(m^2-1),
Ttheta=S C+c s Cc,
Dtheta=r[tan(theta)+c cot(c theta)]-Ttheta.           (11)
```

The exact right-switch formulas are

```text
b_0=2 Ttheta/(Bv^2 p s^2),
gamma_2-b_0=2 Dtheta/(Bv^2 p s^2).                   (12)
```

Every denominator in `(12)` is strictly positive. Moreover,

```text
tan(theta)-S C=S^3/C>0,
cot(c theta)-s Cc=Cc^3/s>0,
r>1.
```

Hence

```text
Dtheta>0,
gamma_2>b_0>0.                                       (13)
```

This reproduces the new direct theorem and audits both its factor of `2` and
its phase domain.

## 5. Left-switch Green and penalty formulas

Let `r_D` be the right-Dirichlet solution at `lambda_3`, normalized by

```text
r_D(x)=sin(p(L-x))/p on [b,L].
```

Formula `(5)` gives `p r_D(a)=D`. The Wronskian at `L` then yields

```text
G_D(a,a;lambda_3)=X D/p.                             (14)
```

Let `r_N` be the right-Neumann solution at `lambda_2`, normalized by

```text
r_N(x)=cos(c p(L-x)) on [b,L].
```

Formula `(6)` gives `r_N(a)=N`. Since
`phi_2'(L)=-c p`, the same Wronskian convention yields

```text
G_N(a,a;lambda_2)=-Y N/(c p).                        (15)
```

Thus, using `u_2(a)^2=v(a)^2/2=Bv^2Y^2/2`, the first Green coefficient is

```text
a_0=2[X D+c Y N]/(Bv^2 p Y^2).                       (16)
```

On the left outer layer,

```text
Q'(a)=c p[cot(alpha)-c cot(c alpha)].                 (17)
```

The function `t cot(t)` is strictly decreasing on `(0,pi)`. From `(2)`,

```text
c cot(c alpha)-cot(alpha)>0.
```

Define

```text
Dalpha=r[c cot(c alpha)-cot(alpha)]>0.                (18)
```

Using the same Wronskian and half-normalization audit as in `(10)`,

```text
gamma_1=2 Dalpha/(Bv^2 p Y^2),
a_0-gamma_1=
  2[X D+c Y N-Dalpha]/(Bv^2 p Y^2).                  (19)
```

## 6. Exact amplitude-free Schur reduction

Put

```text
K0=2/(Bv^2 p)>0,
Aalpha=X D+c Y N-Dalpha.
```

Equations `(12)` and `(19)` give

```text
S_KP
=a_0-gamma_1+b_0^2/(gamma_2-b_0)
=K0[Aalpha/Y^2+Ttheta^2/(s^2 Dtheta)].                (20)
```

All quantities divided out in `(20)` are strictly positive. Multiplying by
`Y^2 Dtheta/K0` and using `Y=-sX/C` proves the equivalence `(1)`, where

```text
Phi
=Dtheta[X D+c Y N-Dalpha]+X^2 Ttheta^2/C^2

=Dtheta[X(D-c s N/C)-Dalpha]+X^2 Ttheta^2/C^2.        (21)
```

Every symbol in `(21)` is the elementary function of
`(m,c,alpha,beta,theta)` defined in `(5)`, `(6)`, `(11)`, and `(18)`.
No eigenfunction amplitude, mass, Green kernel, regularized resolvent, or
Wronskian remains in `Phi`.

## 7. Equality cases and no-loss statement

On the admissible branch set,

```text
K0>0,
Y^2>0,
s^2>0,
C^2>0,
Dtheta>0.
```

Therefore no equality was introduced or removed in passing from `(20)` to
`(21)`. The exact interior equality cases are precisely the tuples

```text
(m,c,alpha,beta,theta)
```

which satisfy `(2)-(4)`, `(E_DN)`, `(E_DD)`, `(E_band)`, `(E_mass)`, and

```text
Phi=0.                                                (22)
```

Such a tuple reconstructs an exact finite-interior branch point and gives
`S_KP=0`, hence `det Kp_odd=0`. Conversely, every branch-realizable equality
`S_KP=0` maps to exactly such a tuple. The corresponding normalized kernel is
the already audited same-sign vector proportional to

```text
(gamma_2-b_0,b_0).
```

The faces `alpha=0,pi`, `theta=0,pi/2`, `c beta=delta_2`, and
`beta=delta_3,delta_3+pi` are not equality cases of this theorem. They are
switch-collision or mode-index boundary faces excluded by the problem
contract.

## 8. Exact remaining gap

KP-DET is now equivalent to the single elementary constrained inequality

```text
Phi(m,c,alpha,beta,theta)<0                           (23)
```

on the phase system stated above. The present derivation does not supply an
inequality from `(E_mass)` strong enough to dominate the positive final term
`X^2 Ttheta^2/C^2` in `(21)`. Therefore claiming `(23)` would be circular.

This is a strict reduction rather than a renaming of `S_KP`: all spectral
Green data and all normalization amplitudes have been eliminated, the exact
finite phase domain is explicit, and the only remaining use of normalization
is the elementary equation `(E_mass)`. It gives a concrete target for a
future exact interval certificate, analytic monotonicity proof, or formal
trigonometric audit without reopening KO-DET or any global branch question.
