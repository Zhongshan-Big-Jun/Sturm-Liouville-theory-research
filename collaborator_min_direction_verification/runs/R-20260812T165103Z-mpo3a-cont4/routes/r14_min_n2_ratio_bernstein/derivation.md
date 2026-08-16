RIGOROUS_PARTIAL_RESULT

# R14: phase-ratio monotonicity and a four-coefficient Bernstein frontier

## 1. Scope and notation

Fix `mu>1`.  For a phase angle

```text
0 < theta < pi/mu
```

put

```text
s=sin(theta),       S=sin(mu theta),
c=cos(theta),       C=cos(mu theta),
U=1/s+mu/S,         V=c/s-mu C/S,
Q=s+mu S,
x=V/U,              p=Q/U,
rho=(mu/s+1/S)/U,
e=(mu^2-1)sS(c+C)/(S+mu s)^2,
kappa=mu sS(c+C)^2/(S+mu s)^2.
```

The identity

```text
kappa=1-x^2-p                                             (1.1)
```

will be used below.  A subscript `+` means

```text
0<alpha<pi/(mu+1),
```

and a subscript `-` means

```text
pi/(mu+1)<beta<pi/mu.
```

Write

```text
lambda=U_+/U_-,       d=rho_+-rho_->0,       eta=-e_->0,
delta=r^2-1,
w=(e_+-r eta/lambda)/d,
u=x_++w,
A0=1-x_+u,
g=lambda^2 p_+/p_-.
```

The strict physical interval ends at

```text
r_B=lambda e_+/(eta+d x_-),                              (1.2)
```

and is nonempty only when `r_B>1`.  On that interval

```text
w>0,  u>0,  A0>0,  lambda w/r-x_->0.                    (1.3)
```

The accepted R11 reduction is

```text
Phi=[lambda^2 w^2+r^2 kappa_-+p_-]
       [A0+delta p_+u^2]-delta p_- w u^3,                (1.4)
```

and the following positive submargin is sufficient:

```text
Psi=lambda^2 w^2 A0
    +delta u^2[p_+lambda^2w^2+p_-p_+-p_-wu].             (1.5)
```

Every claim below is exact.  Decimal searches mentioned in the audit are
not used as premises.

## 2. The apparent `r_A>1` branch is empty

Let

```text
F=sin(mu theta)/sin(theta),       K=(1-x^2)/x.
```

On the positive phase, direct reduction using

```text
C^2=1-F^2+F^2c^2
```

gives

```text
(rho-1)K-e
 =F(mu-1)^2[1+cos((mu+1)theta)]
   /[(F+mu)(Fc-mu C)] >0.                                (2.1)
```

Here `Fc-mu C=(F+mu)x>0`, and
`0<(mu+1)theta<pi`, so every factor on the right is strict.
Since `rho_-<1`,

```text
d=rho_+-rho_->rho_+-1.
```

Consequently

```text
e_+-d(1-x_+^2)/x_+<0,
r_A=lambda[e_+-d(1-x_+^2)/x_+]/eta<0.                   (2.2)
```

Thus the only physical contrast interval that needs consideration is

```text
1<r<r_B.                                                  (2.3)
```

## 3. A strict positive-phase lemma

For the positive angle `alpha`, abbreviate

```text
s=sin(alpha), S=sin(mu alpha), c=cos(alpha), C=cos(mu alpha),
Q0=s+mu S, D0=S+mu s.
```

Substitution shows that

```text
p_+(rho_+-1)>x_+e_+                                      (3.1)
```

is equivalent, with no reversal of sign, to

```text
Q0 D0(S-s)>(mu+1)(Sc-mu sC)(c+C).                        (3.2)
```

Indeed all cancelled denominators are positive.  Put

```text
A=(mu+1)alpha/2 in (0,pi/2),
B=(mu-1)alpha/2 in (0,A),
k=B/A=(mu-1)/(mu+1) in (0,1).
```

After the sum-and-difference identities, (3.2) is exactly

```text
k tan(A)>tan(B)[cos(B)^2+k^2 sin(B)^2].                  (3.3)
```

The square bracket is strictly below one.  Moreover `tan(t)/t` is
strictly increasing on `(0,pi/2)`, because

```text
d/dt[tan(t)/t]
 =[t sec(t)^2-tan(t)]/t^2>0,
```

and the numerator has derivative `2t sec(t)^2 tan(t)>0` and vanishes at
zero.  Hence

```text
tan(B)<(B/A)tan(A)=k tan(A),
```

which proves (3.1).

For every physical `r>=1`, (3.1) gives the following useful strict margin:

```text
p_+-x_+w
 ={p_+d-x_+e_++x_+r eta/lambda}/d>0.                    (3.4)
```

## 4. Exact closure when `F_+F_- >= 1`

The identity `p=Q/U` gives

```text
g=lambda^2p_+/p_-=G(F_+)/G(F_-),
G(F)=1+mu^2+mu(F+F^{-1}).                                (4.1)
```

Also

```text
G(F_+)-G(F_-)
 =mu(F_+-F_-)(F_+F_--1)/(F_+F_-).                        (4.2)
```

Since `F_+>F_->0`,

```text
g>=1  iff  F_+F_->=1.                                    (4.3)
```

Using `u=x_++w`, (1.5) becomes exactly

```text
Psi=lambda^2w^2A0
    +delta p_-u^2[(g-1)w^2+(p_+-x_+w)].                  (4.4)
```

Equations (1.3), (3.4), and (4.3) prove `Psi>0`, hence `Phi>0`, on the
entire half-domain `F_+F_->=1`.

## 5. A new exact monotonicity theorem

Define, for fixed `mu`,

```text
R(theta)=p(theta)/x(theta)^2,       0<theta<pi/mu.        (5.1)
```

Then `R` is strictly decreasing on its full interval.

To prove this, put

```text
Ahat=csc(theta),       Bhat=mu csc(mu theta),
zeta=Bhat/Ahat=mu sin(theta)/sin(mu theta),
a=cot(theta),          b=mu cot(mu theta).
```

The strict decrease of `sin(t)/t` on `(0,pi)` gives `zeta>1`.  Also

```text
V=a-b>0,               zeta'=zeta V,
V'=Bhat^2-Ahat^2=Ahat^2(zeta^2-1).                       (5.2)
```

For completeness, `V>0` follows because `t cot(t)` is strictly decreasing
on `(0,pi)`.

Now

```text
R=QU/V^2=G(zeta)/V^2,
G(zeta)=(zeta+1)(zeta+mu^2)/zeta.                        (5.3)
```

Therefore

```text
(log R)'=[zeta G_zeta/G]V-2V'/V.                         (5.4)
```

If `1<zeta<=mu`, then `zeta G_zeta/G<=0`, while `V'>0`, so (5.4) is
strictly negative.  If `zeta>mu`, the identities

```text
|a|<Ahat,       |b|<Bhat,
```

because `|cot(t)|<csc(t)` for every `t in (0,pi)`.  These absolute-value
bounds do not require either cotangent to be positive.  They give
`0<V<Ahat(1+zeta)` and hence

```text
2V'/V^2>2(zeta-1)/(zeta+1).                              (5.5)
```

On the other hand,

```text
zeta G_zeta/G
 =(zeta^2-mu^2)/[(zeta+1)(zeta+mu^2)]
 <(zeta-1)/(zeta+1),                                    (5.6)
```

because the difference between the last two fractions is

```text
(mu^2-1)zeta/[(zeta+1)(zeta+mu^2)]>0.
```

Combining (5.4)--(5.6) again gives `(log R)'<0`.

Since `alpha<beta`, (5.1) yields

```text
p_+/x_+^2>p_-/x_-^2.                                    (5.7)
```

In the remaining case `g<1`, namely `lambda^2p_+<p_-`, (5.7) implies

```text
lambda^2 x_+^2 R(alpha)
 <x_-^2 R(beta),       R(alpha)>R(beta)>0,
lambda x_+<x_-.                                          (5.8)
```

At `r=r_B`, equality holds in the last inequality of (1.3), so

```text
w_B=r_Bx_-/lambda>x_+.                                   (5.9)
```

Since `w` decreases with `r`, (5.9) proves

```text
w>x_+   for every 1<=r<=r_B.                             (5.10)
```

## 6. The corrected retained margin

Set

```text
M_+=p_+(rho_+-1)-x_+e_+>0.
```

Equation (3.4) refines exactly to

```text
p_+-x_+w
 ={M_++p_+(1-rho_-)+x_+r eta/lambda}/d.                  (6.1)
```

Since `A0=kappa_++p_+-x_+w`, define

```text
Knew=kappa_+ + p_+(1-rho_-)/d.                           (6.2)
```

Then

```text
A0-Knew=(M_++x_+r eta/lambda)/d>0.                       (6.3)
```

This is the term that the false replacement `A0 -> kappa_+` omitted.
Let

```text
h=x_++(1-g)w,
E   =g w A0-delta p_+u^2h,
Enew=g w Knew-delta p_+u^2h.                             (6.4)
```

Thus `E>Enew`.  The accepted identity

```text
Psi=(p_-w/p_+)E+delta p_-p_+u^2                         (6.5)
```

shows that `Enew>0` would finish the remaining half-domain.

## 7. A closed quadratic bridge and one open quartic

Define

```text
J=w[2h+(1-g)u]-uh
 =2(1-g)w^2+x_+w-x_+^2.                                 (7.1)
```

By (5.10), `x_+w-x_+^2>0`; hence

```text
J>0.                                                      (7.2)
```

Next define the quartic-in-`r` margin

```text
D(r)=gKnew-delta p_+u[2h+(1-g)u].                        (7.3)
```

If `D(r)>0`, then (7.1) gives

```text
gKnew w
 >delta p_+u w[2h+(1-g)u]
 >delta p_+u^2h,
```

so `Enew(r)>0`.  The same margin controls the derivative.  With

```text
c0=eta/(lambda d)>0,       w'=u'=-c0,
h'=-(1-g)c0,
```

one has the exact identity

```text
Enew'(r)=-c0D(r)-2r p_+u^2h.                             (7.4)
```

Thus a proof of `D>0` would simultaneously prove `Enew>0` and strict
decrease of `Enew`.

## 8. Exact Bernstein coefficients of the remaining quartic

Map `r in [1,r_B]` to `t in [0,1]` by

```text
r=1+s t,       s=r_B-1,
q=c0s,
w=w_0-qt.
```

Let endpoint subscripts `0,1` mean `r=1,r_B`, respectively, and put

```text
u_i=x_++w_i,
h_i=x_++(1-g)w_i,
ell_i=2h_i+(1-g)u_i,
Delta_B=r_B^2-1=s(s+2).
```

The degree-two Bernstein coefficients of `delta` are

```text
(0,s,Delta_B),
```

while those of `u` and `ell` are `(u_0,u_1)` and
`(ell_0,ell_1)`.  The product rule for Bernstein bases therefore gives
the degree-four coefficients of `delta u ell`:

```text
N_0=0,
N_1=s u_0 ell_0/2,
N_2={2s(u_1ell_0+u_0ell_1)+Delta_B u_0ell_0}/6,
N_3={2s u_1ell_1+Delta_B(u_1ell_0+u_0ell_1)}/4,
N_4=Delta_B u_1ell_1.                                   (8.1)
```

Consequently the five Bernstein coefficients of `D` are exactly

```text
B_i=gKnew-p_+N_i,       i=0,...,4.                       (8.2)
```

Their current rigorous status is:

```text
B_0=gKnew>0                                      PROVED;
B_1=gKnew-(p_+/2)s u_0ell_0                     OPEN;
B_2=gKnew-(p_+/6)[2s(u_1ell_0+u_0ell_1)
                  +Delta_Bu_0ell_0]             OPEN;
B_3=gKnew-(p_+/4)[2s u_1ell_1
                  +Delta_B(u_1ell_0+u_0ell_1)]  OPEN;
B_4=gKnew-p_+Delta_Bu_1ell_1                    OPEN.
```

This is the exact remaining frontier.  Positivity of `B_1,...,B_4`
would imply `D>0` by the convex-hull property of the Bernstein basis, then
`Enew>0`, `E>0`, `Psi>0`, and finally `Phi>0`.

No sign for these four coefficients is asserted here.

## 9. A strict rational envelope for the common tangent scale

For future coefficient work put

```text
k=(mu-1)/(mu+1),       T0=tan(pi k/2).
```

Then the exact rational envelope

```text
k<T0<2k/(1-k^2)                                         (9.1)
```

holds.  The lower bound follows from `tan x>x` and `pi/2>1`.  For the
upper bound let `t=pi(1-k)/2` and

```text
f(t)=sin t-t+t^2/pi.
```

Here `f'(0)=f'(pi/2)=0` and `f''(t)=2/pi-sin t` is strictly decreasing
through one zero.  Thus `f'>0` in the open interval and

```text
cos(pi k/2)=sin t>t-t^2/pi=pi(1-k^2)/4.
```

Together with `sin(pi k/2)<pi k/2`, this proves the upper bound in (9.1).

The weaker relaxation that retains only an unspecified common `T` is not
valid for this proof problem: the exact rational counterexample frozen in
`../r13_min_n2_cross_relaxation_no_go/` has `E<0` and `Enew<0` while
satisfying the cross-only constraints.  It violates (9.1).  Therefore any
future semialgebraic certificate must retain the fixed `T0` relation or a
proved envelope such as (9.1).

## 10. Result and exact gap

This route proves:

1. `r_A<0`, so there is no `r_A>1` branch;
2. `Phi>0` whenever `F_+F_->=1`;
3. `R(theta)=p(theta)/x(theta)^2` is strictly decreasing;
4. in the remaining half-domain, `w>x_+` and the bridge `J>0`;
5. the complete unresolved problem is reduced to the four explicit
   coefficient inequalities `B_1,...,B_4>0` in (8.2).

The route remains a rigorous partial result until those four signs are
proved on the true common-angle domain (or on a rigorously proved
superdomain containing it).
