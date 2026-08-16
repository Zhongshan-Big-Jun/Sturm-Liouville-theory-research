CANDIDATE_COMPLETE_PROOF

# C2-J: hash-bound conditional bridge from the full coefficient cube to general-`mu` minimum reflection at `n=2`

## 0. Conditional theorem and current status

Assume a separately frozen exact/certified C2-I artifact proves

```text
G_i(k,t,y)>0, i=1,2,3,4,                             (0.1)
```

at every point of the full strict physical cube `0<k,t,y<1` retained by

```text
g<1, rB>1.                                           (0.2)
```

The quantities in (0.1)--(0.2) must be exactly those defined in Section 6.
Then, for every finite `R>1`, every `mu>1`, and every arbitrary possibly
asymmetric premise-complete transverse common-terminal minimum-law root with
`n=2`,

```text
H>0, det(L_-)>0, and partial_q A_2(mu,q)<0.           (0.3)
```

Consequently the accepted conditional-global-order theorem applies with
orientation sign `sigma=-1`: at each fixed `mu`, the global common-terminal
residual `A_2(mu,.)` has at most one zero across all relay chambers and
compatible closures, and every zero is fixed by reflection after positive
reorientation.  Every minimum self-consistent four-switch point is such a
zero and is therefore reflection invariant.

This proof closes the implication from (0.1) to reflection.  It does not
assert (0.1); until the complete C2-I artifact is hash-bound and reviewed,
the result is conditional and non-propagating.

## 1. Canonical contracts and exact scope

The proof is bound to Blueprint
`b93b42029f95d55489c71e344af329220c3182ff07c2d0b57b9e170b7d4f7056`
and inventory
`b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
It uses these accepted contracts:

```text
CLM-NGE2-MPO3A-FULL-RELAY
  semantic 59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
  proof    0e6f919fa94e5f2a3c1c90ee825916346289d0c2c0f5250315a1a7e17da6679f

CLM-NGE2-MPO3A-INTERNAL-PHASE-R8
  semantic 43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702
  proof    33113ba8623d1e80d065cd17d834739d07adcc5f503c4390000de85f7fd0cb96

CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7
  semantic 5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee
  proof    a949934f6bfb68af9cf87a0b245c868f706d4b15b98de3c7b48a3731b9dede89

CLM-NGE2-MPO3A-MIN-DETERMINANT-PARITY-R35
  semantic bccb84587f0fb907314362677afbcc473037f8f1f26ef1aaa0d2368acf911014
  proof    2e4619ac52392aadf00369e8c9afdea3ddf76ec5e3d00452dc44a258ee8de40b

CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
  semantic 7b14d27f0e1a8dc6f97b2fa60a448497f072490eace29dee2de6785373924c89
  proof    66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93
```

FULL-RELAY supplies the exact arbitrary-asymmetry relay representation.
INTERNAL-PHASE gives every internal positive-negative-positive word the
strict phases

```text
0<alpha_L,alpha_R<pi/(mu+1)<beta<pi/mu.              (1.1)
```

No equal-norm equation, reflection, or equality of `alpha_L` and `alpha_R`
is used in the local sign argument.  Equal norm is needed only when selecting
the self-consistent subset after reflection fixing has already been proved
for all common-terminal roots.

## 2. The strict physical phase cube is exactly `(0,1)^3`

Put

```text
k=(mu-1)/(mu+1),                       0<k<1,
A_+=(mu+1)alpha/2,
A_-=(mu+1)beta/2.                                    (2.1)
```

Then (1.1) is exactly

```text
0<A_+<pi/2,
pi/2<A_-<pi/(1+k).                                  (2.2)
```

Define

```text
t=2A_+/pi,
y=(A_--pi/2)/(pi/(1+k)-pi/2).                        (2.3)
```

Thus `(k,t,y) in (0,1)^3`.  Conversely,

```text
mu=(1+k)/(1-k),
alpha=pi(1-k)t/2,
beta=pi(1-k)/2+y pi(1-k)^2/[2(1+k)].                (2.4)
```

Equations (2.1)--(2.4) are inverse maps.  In particular

```text
beta-pi/(mu+1)
 =y pi(1-k)^2/[2(1+k)],
pi/mu-pi/(mu+1)
 =pi(1-k)^2/[2(1+k)].                               (2.5)
```

Hence a proof on the entire retained open cube covers every strict physical
phase pair and no noncompact phase end is missing.  Boundary faces of the
closed cube represent excluded limits (`mu=1`, `mu=infinity`, or strict phase
equalities); a certificate may use them to close a cover but need not assert
the physical theorem there.

## 3. Both momentum equations and the exact split scalar

For one positive-negative interface put

```text
t_+=tan(alpha/2), T_+=tan(mu alpha/2),
t_-=tan(beta/2),  T_-=tan(mu beta/2), r=sqrt(R).
```

For a cell with amplitude ratio `z`, the two normalized endpoint momenta are

```text
x=(z-cos(theta))/sin(theta),
y=(-z-cos(mu theta))/sin(mu theta),
x_R=(cos(theta)z-1)/(sin(theta)z),
y_R=(1+cos(mu theta)z)/(sin(mu theta)z).              (3.1)
```

Writing the positive ratio as `a>0` and the negative ratio as `b<0`, the
two independent physical matching equations are

```text
x_-(b)=x_R,+(a)/r,        y_-(b)=y_R,+(a)/r.          (3.2)
```

Their exact Cramer solution is

```text
L=T_-t_+(1+t_-^2)(1+T_+^2)
  -T_+t_-(1+t_+^2)(1+T_-^2),

D=2T_+r t_+(T_-^2t_-^2-1)
  +T_+t_-(t_+^2-1)(1+T_-^2)
  +T_-t_+(1+t_-^2)(T_+^2-1),

N=rT_+t_-(1+t_+^2)(T_-^2-1)
  +rT_-t_+(t_-^2-1)(1+T_+^2)
  +2T_-t_-(T_+^2t_+^2-1),

a=L/D,                    b=-N/(rL).                 (3.3)
```

The checker substitutes (3.3) into both equations in (3.2), not merely
their switch-derivative combination.

For a phase `theta` define

```text
F=sin(mu theta)/sin(theta),
U=csc(theta)+mu csc(mu theta),
Q=sin(theta)+mu sin(mu theta),
x=[F cos(theta)-mu cos(mu theta)]/(F+mu),
rho=(mu F+1)/(F+mu), p=Q/U,
e=(mu^2-1)F[cos(theta)+cos(mu theta)]/(F+mu)^2,
kappa=1-x^2-p.                                      (3.4)
```

Use `+` at `alpha` and `-` at `beta`, and put

```text
lambda=U_+/U_-, d=rho_+-rho_->0, eta=-e_->0,
w=(e_+-r eta/lambda)/d, u=x_++w,
A0=1-x_+u, delta=r^2-1.                              (3.5)
```

The Cramer system gives `u=1/a` and

```text
-b=lambda w/r-x_->0,
1<r<rB:=lambda e_+/(eta+d x_-).                      (3.6)
```

Direct exact substitution in the physical split numerator gives

```text
N_left=U_+^2 Phi/(lambda u^3),

Phi=[lambda^2w^2+r^2kappa_-+p_-]
       [A0+delta p_+u^2]-delta p_-w u^3.             (3.7)
```

The positive prefactor makes `sign(N_left)=sign(Phi)`.  Equations
(3.1)--(3.7) were independently rederived in C2-H, whose checker and report
are bound here by SHA-256

```text
checker 2e0590c02109a1eca57382ecc5b5f5fa4f62da5a34a6fe7b9dc7dd104b256c9c
report  32a4aea77442b1980e5d76fbc608b0ac73b034004eef816eaa9e790b2fd262b7.
```

C2-J dynamically replays that checker before checking the remaining chain.

## 4. The `g>=1` half is analytic

The exact positive submargin

```text
Psi=lambda^2w^2A0
 +delta u^2[p_+lambda^2w^2+p_-p_+-p_-wu]            (4.1)
```

satisfies

```text
Phi-Psi
 =r^2kappa_-A0+p_-A0+delta p_+r^2kappa_-u^2>0.      (4.2)
```

Set

```text
g=lambda^2p_+/p_-.
```

The positive-cell response inequality

```text
p_+-x_+w>0                                           (4.3)
```

follows from the exact half-sum proof
`p_+(rho_+-1)-x_+e_+>0`, `d>rho_+-1`, and (3.5).  Using `u=x_++w`,

```text
Psi=lambda^2w^2A0
 +delta p_-u^2[(g-1)w^2+p_+-x_+w].                  (4.4)
```

Therefore `g>=1` implies `Psi>0`, hence `Phi>0`, with no coefficient cover.

Equivalently, if `G(F)=1+mu^2+mu(F+F^(-1))`, then

```text
g=G(F_+)/G(F_-),
G(F_+)-G(F_-)
 =mu(F_+-F_-)(F_+F_--1)/(F_+F_-),                  (4.5)
```

so the analytic half is exactly `F_+F_->=1`.

## 5. The `g<1` half reduces to four Bernstein coefficients

The remaining case is `0<g<1`.  Define

```text
R_phase(theta)=p(theta)/x(theta)^2.                  (5.1)
```

This is strictly decreasing on `0<theta<pi/mu`.  A self-contained proof is
obtained from

```text
zeta=mu sin(theta)/sin(mu theta)>1,
V=cot(theta)-mu cot(mu theta)>0,
zeta'=zeta V,
V'=csc(theta)^2(zeta^2-1),
R_phase=(zeta+1)(zeta+mu^2)/(zeta V^2).              (5.2)
```

Since

```text
(log R_phase)'=[zeta partial_zeta(log G)]V-2V'/V,
G(zeta)=(zeta+1)(zeta+mu^2)/zeta,                    (5.3a)
```

the sign can be checked after division by `V>0`.  For `1<zeta<=mu`, the
logarithmic `zeta` contribution is nonpositive and `V'>0`.  For `zeta>mu`,
the strict elementary bounds `|cot theta|<csc theta` and
`|mu cot(mu theta)|<mu csc(mu theta)` give
`0<V<csc(theta)(1+zeta)`, hence

```text
2V'/V^2>2(zeta-1)/(zeta+1)
 >(zeta^2-mu^2)/[(zeta+1)(zeta+mu^2)],               (5.3c)
```

while

```text
zeta partial_zeta(log G)
 =(zeta^2-mu^2)/[(zeta+1)(zeta+mu^2)].               (5.3b)
```

Thus `(log R_phase)'<0` in both cases, without assuming either cotangent
has a fixed sign.

Because `alpha<beta`, `g<1` and (5.1) imply

```text
lambda x_+<x_-.                                      (5.4)
```

At the branch endpoint, (3.6) gives
`w_B=rB x_-/lambda>x_+`.  Since `w` decreases with `r`,

```text
w>x_+                         for 1<=r<=rB.          (5.5)
```

Put

```text
Knew=kappa_+ +p_+(1-rho_-)/d,
h=x_++(1-g)w,
ell=2h+(1-g)u.                                       (5.6)
```

The strict positive-cell margin refines to

```text
A0-Knew
 ={p_+(rho_+-1)-x_+e_+ +x_+r eta/lambda}/d>0.       (5.7)
```

Define

```text
E=g w A0-delta p_+u^2h,
Enew=g w Knew-delta p_+u^2h,
D(r)=gKnew-delta p_+u ell.                           (5.8)
```

Exact algebra gives

```text
Psi=(p_-w/p_+)E+delta p_-p_+u^2,                    (5.9)

w ell-u h=2(1-g)w^2+x_+w-x_+^2>0.                  (5.10)
```

By (5.7), `E>Enew`.  If `D(r)>0`, then multiplying by `w>0` and using
(5.10) yields

```text
gKnew w>delta p_+u w ell>delta p_+u^2h,
```

so `Enew>0`, then `E>0`, `Psi>0`, and finally `Phi>0`.

Map `r in [1,rB]` affinely by

```text
r=1+s_R z, s_R=rB-1>0, 0<=z<=1.
```

Let subscripts `0,1` denote `r=1,rB`, and

```text
Delta_B=rB^2-1=s_R(s_R+2).
```

The degree-four Bernstein coefficients of `D` are

```text
B_i=gKnew-p_+N_i,                                    (5.11)

N_0=0,
N_1=s_R u_0 ell_0/2,
N_2=[2s_R(u_1ell_0+u_0ell_1)+Delta_Bu_0ell_0]/6,
N_3=[2s_Ru_1ell_1+Delta_B(u_1ell_0+u_0ell_1)]/4,
N_4=Delta_Bu_1ell_1.                                 (5.12)
```

Here `B_0=gKnew>0`.  If `B_1,...,B_4>0`, the Bernstein basis is
nonnegative and sums to one on the closed interval, so `D(r)>0` on
`[1,rB]`.  This includes both interval endpoints and permits repeated roots
of the quartic only outside the positive range; no simple-root assumption
on `D` is used.

## 6. Stable common-angle coordinates and `G_i=cp^4B_i`

For the cube coordinates of Section 2 define positive phase variables

```text
q0=A_+ sinc(kA_+)/cos(kA_+)=tan(kA_+)/k,
a0=sinc(kA_+)cos(A_+)/[cos(kA_+)sinc(A_+)]
   =tan(kA_+)/[k tan(A_+)],

sigma0=A_-sinc(kA_-)/cos(kA_-)=tan(kA_-)/k,
b0=-sinc(kA_-)cos(A_-)/[cos(kA_-)sinc(A_-)]
   =-tan(kA_-)/[k tan(A_-)].                         (6.1)
```

Because `0<kA_+<A_+<pi/2` and
`0<kA_-<pi-A_-<pi/2`,

```text
0<a0<1, 0<kb0<1, q0>0, sigma0>0.                    (6.2)
```

Put

```text
Dtilde=b0(1+k^2a0b0)+k^2(a0+b0)sigma0^2,
rB=a0 sigma0(1-k^2b0^2)/(q0 Dtilde),

ebar=(1-k^2)(b0^2-a0^2)
      /[(1-k^4b0^2)(1-k^2a0^2)],
g=1-k^2 ebar.                                        (6.3)
```

On the retained subset `g<1`, (6.2)--(6.3) give `b0>a0`; in particular
`a0+b0>0`.  On `rB>1`, the positive numerator in (6.3) forces
`Dtilde>0`.  Thus every displayed denominator is nonzero on the retained
physical subset.

Let `cp>0` be defined by

```text
cp^2=(a0^2+q0^2)(1+k^2q0^2)/q0^2.                   (6.4)
```

The cancellation-safe positive-cell variable is

```text
Xbar=[sinc(2kA_+)-sinc(2A_+)]
 /{sin(A_+)cos(kA_+)
   [sinc(A_+)cos(kA_+)-k^2sinc(kA_+)cos(A_+)]},     (6.5)
```

and exact half-sum substitution gives

```text
cp x_+=kXbar.                                        (6.6)
```

The numerator in (6.5) is positive because `sinc` is strictly decreasing
on `(0,pi)`; (6.6) and `x_+>0` fix the denominator sign and exclude a
hidden zero.

Define

```text
Wbar_0=(1-k^2a0^2)
 [a0sigma0-b0q0+k^2a0b0(q0+sigma0)]
 /[q0sigma0(a0+b0)(1-k^2a0)],

Wbar_1=k^2a0(1-k^2a0^2)
 [b0^2+b0+sigma0^2+k^2b0sigma0^2]
 /[q0(1-k^2a0)Dtilde].                              (6.7)
```

Exact substitution of (6.1) into (3.4)--(3.6) gives

```text
cp w_i=Wbar_i/k,
Ubar_i=k^2Xbar+Wbar_i,       cp u_i=Ubar_i/k,
Hbar_i=Xbar+ebar Wbar_i,     cp h_i=kHbar_i,
Lbar_i=2Hbar_i+ebar Ubar_i, cp ell_i=kLbar_i.        (6.8)
```

Physical positivity of `w_i,u_i,h_i,ell_i` therefore also signs the stable
quantities; raw numerator signs in (6.7) are not assumed independently.

Finally,

```text
Pplus=cp^2p_+
 =(1-k^2a0^2)(1+k^2a0)/(1-k^2a0),                   (6.9)

Knew=(1-k^2a0^2)/[(a0^2+q0^2)(1+k^2q0^2)]
 {a0^2(1-k^2)/(1-k^2a0)^2
  +q0^2b0(1+k^2a0)/(a0+b0)}.                       (6.10)
```

Let `Nhat_i` be (5.12) with every product `u_j ell_l` replaced by
`Ubar_j Lbar_l`.  Equation (6.8) gives

```text
Nhat_i=cp^2N_i.                                      (6.11)
```

The stable coefficient gaps are exactly

```text
G_i=gKnew cp^4-Pplus Nhat_i=cp^4B_i.                (6.12)
```

Since `cp>0`, `G_i>0` is equivalent to `B_i>0`.  The exact checker derives
(6.9)--(6.10) from the same-angle half-sum tangents and verifies
(6.8), (6.11), and (6.12) symbolically.

## 7. Retained-domain partition and the only coefficient premise

Every strict physical interface has `rB>r>1`, hence `rB>1`.  It lies in
exactly one of:

```text
g>=1: Phi>0 by Section 4;
g<1:  its cube point satisfies (0.2), so C2-I gives G_1,...,G_4>0.
```

In the second case, (6.12), Section 5, and (4.2) give `Phi>0`.  Thus a
complete C2-I proof of (0.1) on all retained open-cube points proves the
local interface sign for every physical phase pair.  It is not enough to
cover only `[1/64,63/64]^3`, only isolated boundary collars, or a finite
sample.  A valid full cover must have no unresolved boxes and must not
discard a box merely because a dependency enclosure overlaps zero; discard
is permitted only when it proves the retained subset empty.

No positivity is required at a closed-cube face as a mathematical premise,
but every sequence of retained interior points approaching a face must be
captured by the union of the certified regions.

## 8. Independent left/right interfaces imply `H>0`

For the actual positive-negative-positive `n=2` word, write the middle
negative amplitude ratio as `-B`, `B>0`, and its inward switch factors as

```text
G=-g_2>0,                 J=-h_2>0.
```

The physical endpoint gamma values and the scalar dual Schur data are

```text
gamma_2=-rG<0,            gamma_3=rJ>0,
W_2=abs(K_2)>0,
x_*=(gamma_3-gamma_2)/W_2=r(G+J)/W_2>0,
H=beta_R+beta_L-W_2.                                  (8.1)
```

Define the two actual gaps

```text
E_L=beta_R x_*+gamma_2,
E_R=beta_L x_*-gamma_3.                              (8.2)
```

Then, without an inverse or a symmetry assumption,

```text
E_L+E_R=(beta_R+beta_L-W_2)x_*=H x_*.                (8.3)
```

For the left interface, the notation of Section 3 gives the exact Schur
factorization

```text
E_L=rG N_left/(delta D_1Q_-),
D_1=delta aQ_+ +rG+a^2g_+>0,                         (8.4)
```

so (3.7) makes `E_L` a strictly positive factor times `Phi_L`.  For an
original right interface, time reversal sends `z` to `1/z` and swaps
`g<->h`, `G<->J`.  If `a,B` denote the reversed left-orientation ratios,
then the direct right-orientation calculation gives

```text
D_3=D_1/a^2>0,             N_right=N_left/(a^2B),
E_R=rJ_R N_right/(delta D_3B_RQ_-),
B_R=1/B>0.                                           (8.5)
```

All factors in (8.4)--(8.5) are strict positive physical factors.  The
hash-bound C2-H checker replays both momentum equations, every swap, both
Schur factorizations, and (8.3).  Apply Sections 2--7 to the actual left
interface `(alpha_L,beta)` and separately to the reversed actual right
interface `(alpha_R,beta)`.  These are two different cube points in general;
the C2-I premise is universal and covers both.  Therefore `E_L,E_R>0`, and
(8.1)--(8.3) give

```text
H>0.                                                  (8.6)
```

No palindromy, equality of positive phases, or reflection is used in this
step.

## 9. Canonical matrix and global-order propagation

For `n=2`, the R35 dual matrix `H` has dimension one.  Its accepted parity
identity includes the zero case and gives

```text
sign det(L_-)=sign H.                                (9.1)
```

Thus (8.6) implies `det(L_-)>0`.  The accepted R7 physical-continuant
identity, in the quotient by the permanent scaling field, is

```text
J<0 iff det(L_-)>0 iff partial_q A_2<0.              (9.2)
```

R7 derives the terminal continuant polynomially and explicitly includes a
singular q-Jacobi field: `det(L_-)=0` iff the distinguished terminal
q-Jacobi position pair vanishes.  No inverse is used at singularity.
Strict (8.2) excludes that case, so there is no unhandled zero determinant
or repeated q-root in the local step.

Because Sections 2--8 apply at every arbitrary premise-complete transverse
common-terminal minimum root, (9.2) supplies the uniform orientation
`sigma=-1` required by the accepted conditional-global-order theorem.  That
theorem already audits:

```text
- global relay IVP existence and word-independent continuity on q>1;
- automatic premise completeness of every global A_2 zero;
- terminal event-pair birth/death and first-order derivative softness;
- compatible chamber closures;
- reflection producing a second zero of the same global residual.
```

Hence `A_2(mu,.)` has at most one zero and every zero is reflection fixed.
The full self-consistent system also requires the equal-norm residual
`B_2=0`, but every such solution is already an `A_2` zero and therefore
inherits reflection.  Existence and equal-norm orientation are not asserted.

## 10. Exact checker, package boundary, and remaining input

Replay:

```text
E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe runs/R-20260816T034422Z-min-reflection-cont2/routes/r14_r17_bridge_rebind/exact_checker.py
```

The checker dynamically replays the hash-bound full Cramer/Phi reduction and
then verifies the cube inverse map, (4.2)--(4.4), (5.9)--(5.12), the stable
scalings, (6.9)--(6.12), and the exact common-angle formulas for `g` and
`Knew`.

The conditional proof has one and only one missing input:

```text
A complete immutable C2-I artifact proving G_1,...,G_4>0 at every retained
g<1,rB>1 point of the full open cube, with exact evaluator binding, complete
boundary/intersection coverage, and no unresolved boxes.                (10.1)
```

Until (10.1) is supplied, this bridge must not be promoted to an
unconditional general-`mu` theorem.

```text
coordinate bijection:                         PROVED
physical Cramer and Phi bridge:                PROVED AND HASH-BOUND
g>=1 analytic half:                            PROVED
g<1 G_i=>B_i=>D=>Phi chain:                    PROVED
stable G_i=cp^4 B_i equivalence:               PROVED
asymmetric two-interface H>0 bridge:           PROVED CONDITIONALLY
H>0=>partial_q A_2<0=>reflection:              PROVED CONDITIONALLY
full coefficient cube premise:                 OPEN / C2-I
general-mu n=2 reflection theorem:             NOT YET PROPAGATING
formalization_status:                          not_requested
```
