RIGOROUS_PARTIAL_RESULT_WITH_RESTRICTED_THEOREM

# R9 min complementary inertia: dual Schur chain and the exact local gap

## 0. Scope and status

Work at the rebound canonical snapshot

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:89e3f916c86cc81ec53b49b528260f001b9784204e0fe986314acb06c7908429
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

The R8 phase threshold is now a trusted premise:

```text
CLM-NGE2-MPO3A-INTERNAL-PHASE-R8
semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702
```

Fix an arbitrary premise-complete transverse common-terminal min root with
`m=2n` events.  The target is `n_-(M)>=n-1` for

```text
M=D+B^T K^(-1)B,
D=diag(a_1,...,a_(2n))>0,
sign(K_i)=(-1)^(i+1).
```

This package proves an exact dimension-minimal dual reduction, gives its
Jacobi entries and continuant, and reduces `n=2` to a fully explicit
positive-negative-positive three-cell scalar.  It also aligns that scalar
with the physical gamma-jump certificate, eliminates both independent
momenta exactly for `mu=2`, and proves the resulting residual polynomial
strictly positive by an exact tensor-Bernstein certificate.  Consequently it
proves the complementary inertia and local twist theorem in the restricted
case `n=2, mu=2`.  Finally, it gives an exact counterexample to the
tempting weakened claim that the R8 thresholds plus only switch-derivative
matching force the scalar positive.  It does **not** prove the general
`mu>1,n>=2` target and contains no physical counterexample.

## 1. Exact dual Schur reduction

Split the path incidence rows into the positive odd edges and negative even
edges.  Write them as `B_o` and `C`, respectively, and put

```text
K_o=diag(K_1,K_3,...,K_(2n-1))>0,
W=diag(abs(K_2),abs(K_4),...,abs(K_(2n-2)))>0,
P=D+B_o^T K_o^(-1)B_o.
```

The odd edges are disjoint.  Hence `P` is the direct sum of `n` positive
definite two-by-two blocks.  Since the even part of `K` is `-W`, exactly

```text
M=P-C^T W^(-1)C.                                    (1.1)
```

Define the `(n-1)`-by-`(n-1)` dual matrix

```text
H=C P^(-1)C^T-W.                                    (1.2)
```

The sign in the following identity is important.  Apply Schur
complementation in the two orders to

```text
G=[ P   C^T ].
  [ C    W  ]
```

Complementing `W` gives `In(G)=In(W)+In(M)`.  Complementing `P` gives
`In(G)=In(P)+In(W-CP^(-1)C^T)=In(P)+In(-H)`.  Both `P` and `W` are positive
definite, so comparison of the negative and zero counts yields

```text
n_-(M)=n_+(H),              n_0(M)=n_0(H).           (1.3)
```

Because `H` has dimension `n-1`, the missing min inequality is therefore
equivalent to one definite-matrix statement:

```text
n_-(M)>=n-1       iff       H>0.                     (1.4)
```

In particular, the incorrect relation `n_-(M)=n_-(H)` would reverse the
research target; (1.3) fixes that possible sign error.

## 2. Explicit Jacobi entries and continuant

For positive edge `2j-1`, put

```text
c_j=1/K_(2j-1)>0,
Delta_j=a_(2j-1)a_(2j)+c_j[a_(2j-1)+a_(2j)]>0.
```

In the event order `(2j-1,2j)`, the corresponding block and its inverse are

```text
P_j=[ a_(2j-1)+c_j     -c_j       ],
    [     -c_j       a_(2j)+c_j   ],

P_j^(-1)=[ ell_j   s_j ],
          [  s_j   r_j ],                         (2.1)

ell_j=[a_(2j)+c_j]/Delta_j,
r_j  =[a_(2j-1)+c_j]/Delta_j,
s_j  =c_j/Delta_j.
```

Take row `j` of `C` to be `e_(2j+1)-e_(2j)`, and set
`W_j=abs(K_(2j))`.  Direct multiplication in (1.2) gives the irreducible
Jacobi Z-matrix

```text
H_(j,j)=r_j+ell_(j+1)-W_j,             1<=j<n,
H_(j,j+1)=H_(j+1,j)=-s_(j+1),          1<=j<n-1.    (2.2)
```

Thus the leading continuants and pivots obey

```text
Delta^H_0=1,
Delta^H_1=H_(1,1),
Delta^H_j=H_(j,j)Delta^H_(j-1)-s_j^2 Delta^H_(j-2), (2.3)

p_1=H_(1,1),
p_j=H_(j,j)-s_j^2/p_(j-1).                          (2.4)
```

Consequently `H>0` is exactly `Delta^H_j>0` for every `j`, or equivalently
`p_j>0` for every `j`.  A three-cell inequality proves only positivity of
the diagonal in (2.2); the off-diagonal transfer `s_j` is the additional
obstruction when `n>2`.

For any proposed positive weights `v_1,...,v_(n-1)`, with `v_0=v_n=0`, the
exact supersolution residual is

```text
(Hv)_j=(r_j v_j-s_j v_(j-1))
       +(ell_(j+1)v_j-s_(j+1)v_(j+1))-W_jv_j.       (2.5)
```

Equation (2.5) is the appropriate form for a future telescoping proof: each
positive block transports a ratio through its strictly positive off-diagonal
entry.

## 3. Strict positive-cell half-angle block factors

Consider a positive min cell.  Its material is `1`.  Let its left event
value be `u`, its positive amplitude ratio be `z=u_R/u>0`, and put

```text
delta=R-1,
Q=sin(theta)+mu sin(mu theta)>0.
```

Use the R8 normalized endpoint logarithmic momenta

```text
x=(z-cos theta)/sin theta,
y=(-z-cos(mu theta))/sin(mu theta),
x_R=(cos(theta)z-1)/[sin(theta)z],
y_R=(1+cos(mu theta)z)/[sin(mu theta)z].
```

Define the two inward switch derivatives

```text
g=x-mu y=A(theta)[z-k(theta)]>0,
h=-(x_R-mu y_R)=A(theta)[1-k(theta)z]/z>0.           (3.1)
```

Here `A>0`, `0<k<1`, and the strict positive-cell branch is
`k<z<1/k`.  The physical event and cell coefficients are

```text
a_L=delta u^2/g,
a_R=delta u^2 z^2/h,
c=1/K=u^2 z/Q.                                      (3.2)
```

Put

```text
D_*=delta zQ+h+z^2g>0.
```

Substitution of (3.2) into (2.1), with the harmless factor `u^(-2)`
removed, gives the exact strict factorization

```text
u^2 ell =g(delta zQ+h)/(delta D_*),
u^2 r   =h(delta Q+zg)/(delta zD_*),
u^2 s   =gh/(delta D_*).                             (3.3)
```

Every displayed factor in (3.3) is strictly positive.  This is the useful
blockwise consequence of the R8 half-angle analysis; the remaining negative
cell contribution is not hidden inside an unfactored determinant.

## 4. The exact `n=2` three-cell scalar

For `n=2`, let `z_i=u_(i+1)/u_i` be the three internal-cell amplitude
ratios.  Then

```text
z_1>0,             z_2<0,             z_3>0,
theta_1,theta_3<pi/(mu+1)<theta_2<pi/mu.
```

Let `(hat ell_i,hat r_i,hat s_i)` denote (3.3) for positive cell `i` in
its own left-amplitude normalization.  Since the middle cell has material
`R`,

```text
abs(K_2)=-Q_2/[sqrt(R)u_2^2 z_2].
```

The scalar `H` from (2.2) therefore has the exact scale-free form

```text
u_2^2 H
 =z_1^2 hat r_1+z_2^(-2)hat ell_3+Q_2/[sqrt(R)z_2]. (4.1)
```

The first two terms are strictly positive and the last term is strictly
negative.  Formula (4.1), together with (3.3), is the requested exact
positive-negative-positive Schur-block reduction.

There is also an exact partial telescoping across the two material
interfaces.  On the negative middle cell, (3.1) has both signs reversed.
Writing its R8 factors as `A_2,k_2`, physical continuity of the switch
derivative gives

```text
h_1=sqrt(R) A_2(k_2-z_2),
g_3=sqrt(R) A_2(1-k_2z_2)/(-z_2).                    (4.2)
```

Both sides of (4.2) are strictly positive.  However, (4.2) is only one
linear combination of the two independent momentum-matching equations.
The latter are, with `r=sqrt(R)`,

```text
x_2=x_(R,1)/r,        y_2=y_(R,1)/r,
x_3=r x_(R,2),        y_3=r y_(R,2).                 (4.3)
```

The next subsection proves that (4.3), not merely (4.2), is indispensable.

## 5. Exact no-go for a threshold-only block proof

The following exact rational example satisfies all phase thresholds, both
positive-cell amplitude branches, and the two switch-derivative identities
(4.2), but makes the scalar (4.1) negative:

```text
mu=2,             sqrt(R)=6/5,
t_i=tan(theta_i/2)=(1/5,49/50,1/50),
z_2=-1/100,
z_1=175175/1953879,
z_3=16826778/137555.                                 (5.1)
```

For `mu=2`, the threshold is `theta=pi/3`, whose half-angle tangent is
`1/sqrt(3)`.  Thus `t_1,t_3<1/sqrt(3)<t_2<1`, proving the three strict phase
conditions without numerical approximation.  The four branch margins are

```text
z_1-k_1       =323396/25400427>0,
1/k_1-z_1     =25225252/1953879>0,
z_3-k_3       =16826668/137555>0,
1/k_3-z_3     =310371499/275110>0.                   (5.2)
```

Exact substitution in (3.3)--(4.1) gives

```text
u_2^2 H=
-28631724371526853374269606961558602772691167786748224037432491186500
 /392256468455448162251149432130501665881941586956928806198562754029
<0.                                                       (5.3)
```

This is **not** a physical relay counterexample.  It was designed to audit
the precise scope of a weakened proof.  Indeed the gamma combinations in
(4.2) match exactly, but the independent momentum defects in (4.3) are

```text
x_2-x_(R,1)/r =119315789/5390000,
y_2-y_(R,1)/r =119315789/10780000,
x_3-r x_(R,2) =785424183/269500,
y_3-r y_(R,2) =785424183/539000.                    (5.4)
```

Each `x` defect equals `mu=2` times its `y` defect, explaining why (4.2)
still holds.  Equations (5.1)--(5.4) rigorously prove:

```text
R8 phase thresholds + cell branches + gamma-interface matching
do not imply H>0, even for n=2.                       (5.5)
```

Therefore any successful exact blockwise factorization must use the second
interface equation in (4.3), equivalently the independent energy/log-momentum
information.  This is a strictly sharper gap than saying only that a global
supersolution is missing.

The exact checks are executable in `symbolic_n2_reduction.py`.

## 6. Alignment with the gamma-jump certificate

This section aligns (4.1) with the independent exact scalar certificate in
`routes/r9_min_n2_scalar/derivation.md`.  That route is an unintegrated
candidate artifact, so no statement from it is used as a canonical premise;
all identities used here are reproduced directly.

For the middle negative cell, write its amplitude ratio as `z_2=-B`, with
`B>0`, and set

```text
G=-g_2=A_2(B+k_2)>0,
J=-h_2=A_2(1+k_2B)/B>0.                              (6.1)
```

Physical gamma values at its endpoints are

```text
gamma_2=-sqrt(R)G,             gamma_3=sqrt(R)J.     (6.2)
```

Let `w=abs(K_2)=Q_2/[sqrt(R)u_2^2B]` and take the canonical positive scalar

```text
x_*=(gamma_3-gamma_2)/w>0.                           (6.3)
```

The time-translation equation `M gamma=f` and the two positive block
inversions give exactly

```text
H x_*=beta_R G_L+beta_L G_R.                        (6.4)
```

Thus the independent route's weight is `delta_gamma/w`, not the earlier
discovery weight `delta_gamma/w^(3/2)`.  The latter failed local tests and is
not a candidate certificate.  A stronger sufficient split of (6.4) is

```text
E_L=beta_R x_*+gamma_2>0,
E_R=beta_L x_*-gamma_3>0.                            (6.5)
```

Their sum is exactly `H x_*`.  Substituting (3.3), (4.2), and (6.1)--(6.3)
shows that all omitted prefactors are positive and reduces (6.5) to

```text
N_L=R z_1 B(G+J)[delta Q_1+z_1g_1]
    -delta Q_2D_1>0,
D_1=delta z_1Q_1+sqrt(R)G+z_1^2g_1,                 (6.6)

N_R=R(G+J)[delta z_3Q_3+h_3]
    -delta Q_2B D_3>0,
D_3=delta z_3Q_3+h_3+z_3^2sqrt(R)J.                 (6.7)
```

More precisely,

```text
E_L=sqrt(R)G N_L/[delta D_1Q_2],
E_R=sqrt(R)J N_R/[delta D_3BQ_2].                   (6.8)
```

Equations (6.6)--(6.8) are the exact numerator requested by the gamma-jump
alignment before momentum elimination.  In contrast with the weakened
example in section 5, they retain both momentum equations.

## 7. Full two-momentum elimination for `mu=2`

Put

```text
x=tan(theta_+/2),  y=tan(theta_-/2),  r=sqrt(R).
```

The physical phase chamber is

```text
r>1,               0<x<1/sqrt(3)<y<1.               (7.1)
```

At the left interface let `a=z_1>0` and `b=z_2<0`.  Solving the two
independent equations

```text
x_-(y,b)=x_(R,+)(x,a)/r,
y_-(y,b)=y_(R,+)(x,a)/r                             (7.2)
```

gives, exactly,

```text
D_a=3rx^3y^2-rx^3-3rxy^2+rx+x^4y+2x^2y^3-4x^2y+y,
N_b=2rx^3y^2+rxy^4-4rxy^2+rx
    +3x^2y^3-3x^2y-y^3+y,                           (7.3)

a=-y(x-y)(x+y)(1+x^2)/D_a,
b=N_b/[rx(x-y)(x+y)(1+y^2)].                        (7.4)
```

In (7.1), positivity of `a` and negativity of `b` are respectively

```text
D_a>0,                    N_b>0.                     (7.5)
```

For the same pair of phase variables, the time-reversed right-interface
solutions are exactly `a_R=1/a` and `b_R=1/b`.  A physical three-cell word
need not have equal left and right positive phases; this reciprocity is a
local algebraic symmetry, not an assumption of global reflection.  It shows
that each interface is governed by the same polynomial family, as the
direct elimination confirms.

Define `P(x,y,r)` as the primitive numerator of (6.6) after substituting
(7.4) and cancelling common factors.  This definition is frozen by
`symbolic_split_gap_mu2.py`.  The polynomial has

```text
degree_(x,y,r) P=(16,12,6),
number of nonzero monomials=228,
sha256(expanded SymPy string)=
  906da32475eb75bdcac45a5e04b490661722d9d356717301c5915c2c125c8591.
                                                               (7.6)
```

SymPy 1.14's standard factor routine leaves `P` unchanged over the rational
polynomial ring; this is a reproducible factor-search result, not a separate
certificate of absolute irreducibility.  The
two exact rational identities are

```text
N_L=P/[x^3(1+x^2)(1+y^2)^2D_a^3],                  (7.7)

N_R=-rP/[x^2y^2(x-y)(x+y)(1+x^2)^3(1+y^2)N_bD_a]. (7.8)
```

Every denominator factor in (7.7)--(7.8) has known sign under (7.1) and
(7.5); both `N_L` and `N_R` therefore have exactly the sign of `P`.  This
proves that the two apparent split obligations (6.6)--(6.7) collapse to one
minimal residual inequality:

```text
P(x,y,r)>0 on (7.1), (7.5), and the strict first-crossing branches.
                                                               (7.9)
```

One further interface factor can be signed without expansion.  In the
chamber (7.1), the exact decomposition

```text
N_b=y(1-y^2)(1-3x^2)
    -rx[(1-y^2)(3y^2-1)+2y^2(y^2-x^2)]              (7.10)
```

and `N_b>0` imply

```text
rx(3y^2-1)-y(1-3x^2)<0.                             (7.11)
```

This removes a plausible uncontrolled interface factor.  The next section
signs the residual `P` exactly.  The script verifies (7.2)--(7.11) by exact
rational-function arithmetic and emits no numerical conclusion.

## 8. Exact Bernstein closure of the `mu=2` interface lemma

Use the natural variables

```text
X=x^2,       Y=y^2,
kappa=rx(3Y-1)/[y(1-3X)].                            (8.1)
```

Equations (7.1), (7.10), and `N_b>0` give

```text
0<X<1/3,            1/3<Y<1,             0<kappa<1. (8.2)
```

The exact stronger bound is useful for auditing the domain.  Put

```text
C=(3Y-1)(1-Y)>0,
E=C+2Y(Y-X)>C,
kappa_N=C/E<1.                                      (8.3)
```

After (8.1), direct reduction of (7.3) gives

```text
N_b>0       iff       0<kappa<kappa_N.               (8.4)
```

Similarly `D_a/y` becomes

```text
D(X,Y,kappa)
 =1-4X+X^2+2XY+kappa(1-X)(3X-1).                    (8.5)
```

Its `kappa` coefficient is negative, so throughout the coarser box (8.2),

```text
D(X,Y,kappa)>D(X,Y,1)=2X(Y-X)>0.                    (8.6)
```

Thus no denominator or physical branch sign was lost in passing to the
box.  Substituting (8.1) in the primitive residual gives the exact positive
factor identity

```text
P(x,y,r)=Y^2 Q(X,Y,kappa)/(3Y-1)^2
        =y^4 Q(X,Y,kappa)/(3Y-1)^2.                 (8.7)
```

Here `Q` has degree `(10,6,6)` in `(X,Y,kappa)`.  Map the whole closed box
containing the physical domain to the unit cube by

```text
X=u/3,             Y=(1+2v)/3,             kappa=w. (8.8)
```

After removal of the positive rational content `2/2187`, the polynomial
`Q_box(u,v,w)` has 252 nonzero power terms and degree `(10,6,6)`.  Its
same-degree tensor Bernstein expansion contains exactly

```text
539 coefficients:       387 positive, 152 zero, 0 negative.   (8.9)
```

The calculation is entirely over `QQ`.  The exact script also performs the
full inverse transformation from all 539 Bernstein coefficients back to
every power coefficient of `Q_box`, rather than checking only sample
points.  Since every tensor Bernstein basis polynomial is strictly positive
on `(0,1)^3`, (8.9) and the presence of positive coefficients imply

```text
Q_box>0,       Q>0,       P>0                       (8.10)
```

at every physical interface point.  Zero coefficients cause no equality in
the open cube because no basis function vanishes there.

Apply (8.10) first to the **actual left interface**, with its phase pair
`(x_1,y_2)`.  Equations (6.6), (6.8), and (7.7) give `E_L>0`.  Apply the
same local lemma after time reversal to the **actual right interface**, with
its generally different phase pair `(x_3,y_2)`; equations (6.7), (6.8), and
(7.8) give `E_R>0`.  No identity `x_1=x_3` or reflection symmetry is used.

Both applications use the same actual middle cell, hence the same scalar

```text
x_*=(gamma_3-gamma_2)/abs(K_2)>0.                   (8.11)
```

Therefore the exact physical identity (6.4)--(6.5) gives

```text
H x_*=E_L+E_R>0,       hence H>0.                   (8.12)
```

For `n=2`, `H` is scalar.  Combining (8.12) with (1.3) and the trusted R8
one-sided estimate yields

```text
n_-(M)=1=n-1,        n_0(M)=0,
In(M)=(3 positive,1 negative,0 zero).                (8.13)
```

The trusted R7 physical-continuant bridge now gives, at every
premise-complete transverse common-terminal min root in this restricted
case,

```text
det(L_-)>0,        J<0,        partial_q A_2<0.      (8.14)
```

Thus (8.14) is the negative fixed-`mu` local min twist orientation for
`mu=2,n=2`.  It is a local theorem only; no global min root order or
uniqueness is asserted.

## 9. Discovery evidence and falsified certificates

Everything in this section is `NUMERICAL_EVIDENCE`; none is used in the
proofs above.

* Reconstructing 97 premise-checked complete min roots from the frozen R8
  retained set gave `H>0` in all 97 cases.
* A preregistered grid retained 441 locally glued physical three-cell words;
  all had the scalar (4.1) positive.  These words omit the common terminal
  and global index predicates.
* A preregistered longer-word grid retained 72 local words through `n=6`;
  all had `H>0`.
* The candidate weight
  `v_j=(gamma_(2j+1)-gamma_(2j))/abs(K_(2j))^(3/2)` was positive and gave
  `Hv>0` on the 97 complete retained roots, but failed componentwise on 15
  of the 72 longer local words.  It is therefore not a proof from local
  cell gluing or the phase thresholds.  Simple row sums also fail.

These finite checks nominate full physical positivity but cannot establish
it, and the local failures prevent promotion of the displayed weight to an
exact universal certificate.

## 10. Calibrated conclusion and restart condition

The exact status is

```text
dual inertia identity (1.3):                         PROVED
target equivalent to H>0:                            PROVED
explicit H entries and continuant (2.2)--(2.4):      PROVED
strict positive-cell half-angle block factors (3.3): PROVED
n=2 full scalar reduction (4.1):                     PROVED
gamma-jump alignment and split gaps (6.4)--(6.8):    PROVED
mu=2 full-momentum elimination (7.2)--(7.8):         PROVED
mu=2 interface residual P>0 (8.1)--(8.10):           PROVED EXACTLY
mu=2,n=2 inertia/twist (8.11)--(8.14):               PROVED
threshold + gamma matching suffices:                 REFUTED EXACTLY
premise-complete physical min counterexample:        NONE
general mu>1 or n>2 complementary inertia:           OPEN
```

For general `mu>1`, the minimal `n=2` restart lemma is now precise:

```text
FULL THREE-CELL INTERFACE LEMMA.
Under both independent equations at each interface in (4.3), common
negative energy, the strict R8 branches, and the positive-negative-positive
phase thresholds, the scalar in (4.1) is positive.                (10.1)
```

Section 8 proves this lemma for `mu=2`.  It remains open for general `mu`.

For general `n`, one must additionally control the transfer terms `s_j` in
(2.3), for example by an exact positive vector in (2.5) or a direct
continuant factorization.  The route has not found such a vector.  The
strongest safe output is therefore a restricted exact theorem plus a
rigorous partial result for the general R8 obligation.

## 11. Reproducibility additions

Replay the exact full-interface reduction from the project root:

```text
E:\\ai_auto_solve\\O3a_blueprint_v22_research_20260808\\.venv\\Scripts\\python.exe runs\\R-20260812T165103Z-mpo3a-cont4\\routes\\r9_min_complementary\\symbolic_split_gap_mu2.py

E:\\ai_auto_solve\\O3a_blueprint_v22_research_20260808\\.venv\\Scripts\\python.exe runs\\R-20260812T165103Z-mpo3a-cont4\\routes\\r9_min_complementary\\bernstein_mu2_closure.py

E:\\ai_auto_solve\\O3a_blueprint_v22_research_20260808\\.venv\\Scripts\\python.exe runs\\R-20260812T165103Z-mpo3a-cont4\\routes\\r10_min_full_interface\\independent_bernstein_audit.py
```

Both replays completed with Python 3.12.13 and SymPy 1.14.0.  Exact
certificate identifiers are

```text
P expanded-string SHA-256:
  906da32475eb75bdcac45a5e04b490661722d9d356717301c5915c2c125c8591
Q core expanded-string SHA-256:
  622036e509741e9717fdf33a07340379510f642d42160fc8cf7ddd076dcfb247
Q_box expanded-string SHA-256:
  80a3aa1c535e2e47c32a7bf52a872d12c8e0e71dde726610b896c7fdfe49d2f4
Bernstein coefficient-table SHA-256:
  1a38cc16ec05e873e5f7d2fe205e0f0f31e999d2041e506c563d06242c394c7b
independent Bernstein audit JSON byte SHA-256:
  3c3f94f01a641499dc20ee672ed3d31bede1eb7fd6866d4ab7f6e209589aa8ab
```

The final byte hashes of the route files are reported externally after all
author-side edits are frozen, avoiding self-referential digests.

## 12. Scope guard

The exact theorem proved here is

```text
finite R>1, mu=2, n=2, every premise-complete transverse common-terminal
min root: n_-(M)=1, det(L_-)>0, J<0, partial_q A_2<0.
```

Nothing in the Bernstein certificate propagates to `mu!=2` or `n>2`.
Those cases remain open.
