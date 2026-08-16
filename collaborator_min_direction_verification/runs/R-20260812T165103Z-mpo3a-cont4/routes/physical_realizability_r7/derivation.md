RIGOROUS_PARTIAL_RESULT

# R7: physical realizability constraints for the scalar relay Jacobi word

## 0. Frozen problem contract, provenance, and route registry

### Target

Attack `OBL-NGE2-MPO3A-CAUSAL-RESOLVENT-R6` without using any open or
candidate claim as a premise.  Fix finite `R>1`, `n>=2`, one relay sign, and
a premise-complete transverse common-terminal full-relay trajectory.  Derive
the exact constraints imposed on the scalar Jacobi coefficients by one
globally glued `(U,V)` trajectory, one energy, one `(mu,q)`, the prescribed
Sturm indices, and the common terminal zero.  Determine whether these
constraints exclude the exact abstract `n=2` conjugate word

```text
alpha=(-1,-1,-1,-1),       K=(4/3,-1,4/3),
d=(-1,1/3,-1/3,1),         w=(0,1,2/3,1,0).
```

Seek, but do not assume, a signed-square, continued-fraction, or total-
positivity representation of the physical terminal flux.

### Quantifiers and completion/non-completion rules

The universal R6 sign requires every finite `R>1`, every `n>=2`, both relay
signs, every premise-complete transverse chamber, and compatible closures.
A finite scan, an identity whose quadratic form is indefinite, a result only
at reflection-fixed trajectories, or exclusion of the one displayed
abstract word does not prove R6.  A refutation of R6 requires a complete
physical root with all global predicates, not merely locally compatible
event data.

Boundary audit set: `n=2`; max and min; first and last cells; `R->1+`;
arbitrary large finite `R`; asymmetric reflection pairs; phase limits;
switch collision and grazing closures; and simple common terminal zeros.

### Bound canonical snapshot

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:3e0839c6d73e194653314ae1c456bbc77899bdc279f171f590089ad9c0f38394
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
target node: OBL-NGE2-MPO3A-CAUSAL-RESOLVENT-R6
target semantic hash:
  semantic-sha256:4f72acaabfb31921e93d0dc913d771b8b508cbfd855eefc55dc18c04666e3a40
```

Trusted closure inputs used:

```text
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-SYMPLECTIC-NESTED
  semantic-sha256:4c11a291f871bf44dab3d4970f8b6457bbacafcac6842ae950bd9729be4d2c0e
CLM-NGE2-MPO3A-HYBRID-TWIST-R6
  semantic-sha256:6e2749fd147662212ade344e6dec0a715a83e76cb954e031134748a99a134b7b
CLM-NGE2-MPO3A-CELL-PHASE-R6
  semantic-sha256:34ddfc0ec931503621e7658d7186318b41b3f910214000e23c55bae7aaac040e
CLM-NGE2-MPO3A-STRUCTURE
  semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
CLM-NGE2-MPO3A-TRANSFER-OBSTRUCTION
  semantic-sha256:928f897221f1858180464e49eae8843bfb6c68e0e34baf7ed87c15925f0ab716
```

`OBL-NGE2-MPO3A-CAUSAL-RESOLVENT-R6` is open and is used only as the
research target.  No pending submission is read.

### Route registry

```text
route_id: physical-realizability-r7
target: OBL-NGE2-MPO3A-CAUSAL-RESOLVENT-R6
method_family:
  exact two-frequency cell gluing; common-energy hyperbola; event Wronskian;
  continuants; reflection sectors; signed quadratic forms
local_hypotheses:
  the premise-complete transverse common-terminal hypotheses above
forbidden inputs:
  any open/candidate no-conjugate, global twist, uniqueness, or symmetry claim
deliverable:
  a proved physical coefficient constraint and its consequence for the n=2
  abstract word; then a proof, refutation, or exact first remaining lemma for
  a terminal-sign factorization
fast falsification tests:
  recover both relay signs; test n=2; retain endpoint cells; do not infer
  palindromy from reflection unless the trajectory is already fixed
expected bottleneck:
  convert nonlinear base-trajectory gluing into a sign-regular condition on
  the one-dimensional q-Jacobi line
current_status: frozen rigorous partial result
```

### Reproducibility and computation contract

All analytic identities are derived exactly below.  If exploratory
computation is used, it may only (i) simplify exact formulas, (ii) verify an
explicit algebraic identity, or (iii) search for a finite candidate against
the physical constraints.  Its arithmetic model, domain, software, and
limitations will be recorded before the corresponding output.  Numerical
success cannot establish a universal sign.  An alleged counterexample must
be upgraded to exact or interval-certified full-relay data before it can
refute R6.

Chronological ledger:

```text
2026-08-13: bound the requested canonical snapshot and retrieved the trusted
closure plus the exact R6 obligation.
2026-08-13: froze this contract before new physical-realizability algebra.
```

Specific finite scout registered before execution:

```text
object:
  the symmetric (2n-1)-by-(2n-1) path matrix L_phys derived exactly below
validity predicate:
  every Sylvester pivot and eigenvalue is strictly positive
input domain:
  the 32 retained premise-checked binary64 roots already recorded in
  ../discrete_jacobi_twist/coefficient_probe.json (n=2,...,5; sampled finite
  R and both signs where retained)
arithmetic/software:
  IEEE-754 binary64; PowerShell JSON parsing and elementary LDL recurrence;
  no optimizer, no new relay integration, no random seed
adversarial check:
  report the minimum pivot and distinguish a failed pivot from rounding near
  zero; compare both signs and the largest retained n,R
blind spot:
  a finite retained set cannot cover all chambers, closures, n, or R
proof bridge:
  an exact physical discrete-Hardy/Sylvester theorem for every admissible
  relay word; numerical positivity alone proves nothing universal
```

## 1. Exact physical event coordinates and common-energy gluing

Write the `2n` event times as `t_i` and put

```text
u_i=U(t_i),               epsilon_i=mu V(t_i)/U(t_i) in {+1,-1},
p_i=U_t(t_i),             r_i=V_t(t_i),
e=1-q^2<0,                beta=sqrt(q^2-1)>0.
```

The trusted switching order gives

```text
epsilon_i=(-1)^(i+1).                                    (1.1)
```

Index the open cells from `0` through `m=2n`, and define, once and for all,

```text
Delta rho_i=rho_i-rho_(i-1),                             (1.1a)
```

where `rho_(i-1)` is the material immediately before event `i` and `rho_i`
the material immediately after it.  This is exactly `rhos[j+1]-rhos[j]` in
the retained relay implementation.  Since `S<0` immediately to the right of
the initial zero, the crossing orientation and the relay jump obey

```text
sign(S'_i)=epsilon_i=(-1)^(i+1),
sign(Delta rho_i)=sigma epsilon_i,                       (1.1b)
```

with `sigma=+1` for max and `sigma=-1` for min.

The global relay energy evaluated at an event is

```text
p_i^2-r_i^2=e,
r_i^2-p_i^2=beta^2.                                     (1.2)
```

Thus there is a unique real rapidity `h_i` after fixing the sign
`tau_i=sign(r_i)` such that

```text
r_i=tau_i beta cosh(h_i),
p_i=tau_i beta sinh(h_i).                              (1.3)
```

Since

```text
S'_i=2u_i(p_i-epsilon_i mu r_i),                       (1.4)
```

the event coefficient is not free but has the exact physical form

```text
alpha_i
 =-Delta rho_i u_i^3/(p_i-epsilon_i mu r_i)
 =-Delta rho_i u_i^3/
   [tau_i beta(sinh(h_i)-epsilon_i mu cosh(h_i))].     (1.5)
```

The denominator in (1.5) never vanishes because `mu>1` and
`|tanh(h_i)|<1`; this independently recovers event transversality once the
event value is nonzero.  Its sign is

```text
sign(p_i-epsilon_i mu r_i)=-epsilon_i tau_i.          (1.6)
```

Combining (1.4), (1.6), and (1.1b) makes the sign stitching explicit:

```text
tau_i=-sign(u_i),
sign(p_i-epsilon_i mu r_i)=epsilon_i sign(u_i),
sign(alpha_i)=-sigma.                                   (1.6a)
```

Thus the signs of `u_i`, `tau_i`, and `Delta rho_i` cannot be assigned
independently.

On the internal cell `i` of material `rho_i`, let

```text
theta_i=sqrt(rho_i)(t_(i+1)-t_i),
phi_i=mu theta_i,
c_i=cos(theta_i), s_i=sin(theta_i),
C_i=cos(phi_i),   S_i=sin(phi_i).
```

The trusted all-cell phase lemma gives

```text
0<theta_i<phi_i<pi,      s_i>0, S_i>0.               (1.7)
```

Exact propagation of both oscillators, together with
`mu V_i=epsilon_i u_i` and `epsilon_(i+1)=-epsilon_i`, gives the four gluing
relations

```text
u_(i+1)=c_i u_i+s_i p_i/sqrt(rho_i),                  (1.8)
p_(i+1)=-sqrt(rho_i)s_i u_i+c_i p_i,                 (1.9)

-epsilon_i u_(i+1)
 =epsilon_i C_i u_i+S_i r_i/sqrt(rho_i),             (1.10)
r_(i+1)
 =-epsilon_i sqrt(rho_i)S_i u_i+C_i r_i.             (1.11)
```

In particular, eliminating `u_(i+1)` yields the exact *two-frequency event
compatibility equation*

```text
(c_i+C_i)u_i
 +[s_i p_i+epsilon_i S_i r_i]/sqrt(rho_i)=0.          (1.12)
```

Equations (1.2), (1.8)--(1.12), one common `mu`, and the alternating material
word are the first precise description of the physical coefficient image.
They are strictly stronger than the signs of `alpha_i,K_i` and cell
subcriticality.

The cell coefficient remains

```text
K_i=[s_i+mu S_i]/[sqrt(rho_i)u_i u_(i+1)].            (1.13)
```

Combining (1.5), (1.8), and (1.13) shows concretely that adjacent
`alpha_i,K_i,alpha_(i+1)` share the same endpoint amplitudes and momenta;
there is no independent coefficient parametrization.

## 2. The previous displayed phase/amplitude realization is not physical

The earlier abstract construction attempted to realize its three `K` values
with

```text
mu=2, R=4,
theta_1=theta_2=theta_3=pi/6,
(u_1,u_2,u_3,u_4)
 =(1, 3C/8, -8/3, -9C/64),
C=1/2+sqrt(3).
```

It already violates the low-frequency part of physical gluing, before any
choice of energy or high-frequency momentum is considered.  From (1.8),
the first cell would require

```text
p_1=sqrt(4)[u_2-cos(pi/6)u_1]/sin(pi/6)
   =4(3C/8-sqrt(3)/2)
   =3/4-sqrt(3)/2.                                   (2.1)
```

Equation (1.9) would then force

```text
p_2
 =-2 sin(pi/6)u_1+cos(pi/6)p_1
 =-7/4+3sqrt(3)/8.                                   (2.2)
```

But the second cell, whose material is `1`, would require from its endpoint
values

```text
p_2
 =[u_3-cos(pi/6)u_2]/sin(pi/6)
 =-16/3-3sqrt(3)C/8
 =-155/24-3sqrt(3)/16.                               (2.3)
```

The difference between (2.2) and (2.3) is

```text
113/24+9sqrt(3)/16>0.                                (2.4)
```

Therefore no continuously glued low oscillator has those displayed event
amplitudes and phases.  The former claim that the word was compatible with
all coefficient-level local phase constraints remains correct; the new
calculation proves only that this displayed lift of the word is outside the
physical relay coefficient image.

This exclusion concerns that explicit realization, not yet every possible
realization of the same abstract tuple `alpha=(-1)^4`,
`K=(4/3,-1,4/3)` with different `mu,R,theta_i,u_i`.

## 3. Exact path-square/continued-fraction reformulation

Let `m=2n`, `sigma=+1` for max and `-1` for min, and set

```text
a_i=abs(alpha_i)>0,
k_i=sigma K_i.
```

For a hypothetical terminal conjugate field, `w_0=w_m=0`, while the event
recurrence gives

```text
d_i=-sigma (w_i-w_(i-1))/a_i.                        (3.1)
```

The cell equation `d_(i+1)-d_i=K_iw_i` is therefore equivalent to the
symmetric path equation

```text
(w_i-w_(i-1))/a_i-(w_(i+1)-w_i)/a_(i+1)-k_i w_i=0,
                                      i=1,...,m-1.    (3.2)
```

This is the Euler equation of the exact signed-square form

```text
Q_sigma(w)
 =sum_(i=1)^m (w_i-w_(i-1))^2/a_i
  -sum_(i=1)^(m-1) k_i w_i^2,       w_0=w_m=0.       (3.3)
```

Thus the physical no-conjugate problem is precisely nonsingularity of the
tridiagonal matrix `L_sigma` with

```text
(L_sigma)_(ii)=1/a_i+1/a_(i+1)-k_i,
(L_sigma)_(i,i+1)=-1/a_(i+1).                        (3.4)
```

The finite word has no terminal conjugate point if `L_sigma` is positive
definite.  Sylvester elimination gives the exact continued fraction

```text
P_1=1/a_1+1/a_2-k_1,
P_i=1/a_i+1/a_(i+1)-k_i-1/(a_i^2 P_(i-1)),           (3.5)
```

and positivity is equivalent to `P_i>0` for every `i=1,...,m-1`.

For the actual `log(q)` field, more than nonsingularity can be read off from
the same continuant.  Its initial data are `w_0=0,d_1=-1`, hence

```text
w_1=sigma a_1.                                           (3.5a)
```

Solving the last Dirichlet row, or using the endpoint cofactor of the
irreducible tridiagonal matrix, gives the exact identity

```text
(L_sigma^(-1))_(1,m-1)
 =1/[a_2...a_(m-1) det(L_sigma)],
w_m=sigma (product_(i=1)^m a_i) det(L_sigma).            (3.5b)
```

The polynomial identity for `w_m` remains valid when `det(L_sigma)=0`, by
continuity (or directly by the continuant recurrence).  At the common
terminal, if `p=U_t(L)` and `r=V_t(L)`, the accepted endpoint and causal
identities give

```text
partial_q A_n=(q^2-1)w_m/(q p^2 r^2),
w_m=-q sigma(R-1)J.                                      (3.5c)
```

Here the scalar recurrence is normalized with the `log(q)` field
`zeta=q partial_q z`; the positive factor `q` in both identities is
therefore essential.  Explicitly, `w_m=-q p eta_U(L)` and
`p eta_U(L)=sigma(R-1)J`.

Therefore the exact scope is

```text
J<0
 iff det(L_sigma)>0
 iff sign(w_m)=sigma
 iff sign(partial_q A_n)=sigma.                          (3.5d)
```

Positive definiteness of `L_sigma` is a sufficient stronger theorem, not an
equivalent reformulation of the required terminal sign.  For the
distinguished `log(q)` line, terminal conjugacy is `det(L_sigma)=0`;
terminal orientation only fixes the sign of this final continuant and does
not fix the signs of all preceding pivots.  An arbitrary nonzero Dirichlet
Jacobi field exists at the same parameter exactly when this determinant
vanishes.

Because `K_i` alternates `+,-,+,...`, the signs of `k_i` depend on the relay:

```text
max: k_i=+,-,+,-,...,
min: k_i=-,+,-,+,... .                               (3.6)
```

The negative `k_i` cells only increase the diagonal in (3.4).  The exact
remaining threat is concentrated on positive `k_i` cells.  Positive diagonal
entries require the local inequalities

```text
k_i < 1/a_i+1/a_(i+1)   whenever k_i>0.              (3.7)
```

They are necessary for positive definiteness, but they are not sufficient and
are not a diagonal-dominance criterion.  The exact global requirement is
positivity of every continued-fraction pivot (3.5).  Indeed, the earlier
abstract conjugate word *satisfies* (3.7), since `4/3<2`, yet its matrix and
exact LDL pivots are

```text
L=tridiag(diag(2/3,3,2/3),-1),
(P_1,P_2,P_3)=(2/3,3/2,0).                            (3.8)
```

Thus this word is a global continued-fraction saturation, not a local
diagonal failure.  Positive definiteness of `L_sigma` is a strictly stronger
physical conjecture; local (3.7) is far too weak.  No derivation of the global
pivot inequalities (3.5) from the physical gluing equations
(1.2), (1.8)--(1.13) is currently available.

## 4. Finite falsification scout for the path positivity lemma

The pre-registered binary64 scout reconstructed `a_i,K_i` from all 32
retained coefficient-probe records and evaluated the exact LDL recurrence
(3.5) in floating arithmetic.  It found

```text
record count: 32
all retained pivots positive: yes
smallest retained pivot: 0.16312236973746758
case attaining it: n=5, R=100, max
positive-k cells checked against (3.7): 89
violations found: 0
largest retained ratio
  k_i/(1/a_i+1/a_(i+1)): 0.65702041175109716.
```

Status: `NUMERICAL_EVIDENCE`.  This supports (but does not prove) the stronger
conjecture that every physical coefficient word makes `L_sigma` positive
definite; in particular it supports the weaker required determinant sign in
(3.5d).  The scout has no coverage of unretained chambers, closures,
arbitrary `n`, or arbitrary finite `R`.

## 5. Event-value Jacobi matrix and exact inertia duality

There is an equivalent Sturm formulation in the event values `d_i`.  Let
`B` be the `(m-1)`-by-`m` incidence matrix

```text
(Bd)_i=d_(i+1)-d_i,
D=diag(a_1,...,a_m),       K=diag(K_1,...,K_(m-1)).
```

Eliminating the cell fluxes from the two scalar recurrences gives the
`m`-by-`m` symmetric matrix

```text
M=-sigma D+B^T K^(-1)B,                                  (5.1)
M_(i,i+1)=-1/K_i,
M_11=1/K_1+alpha_1,
M_ii=1/K_(i-1)+1/K_i+alpha_i,        1<i<m,
M_mm=1/K_(m-1)+alpha_m.                                  (5.2)
```

For every scalar Jacobi field satisfying the equal-component-Wronskian
reduction, with left and right cell fluxes `w_0,w_m`, the exact boundary
identity is

```text
Md=(-w_0,0,...,0,w_m)^T.                                 (5.3)
```

Consequently terminal conjugacy is exactly `ker(M)!={0}`.  The converse is
literal, not just a dimension count: given `Md=0`, set `w_0=0`, reconstruct
`w_i=w_(i-1)+alpha_i d_i`, and use rows `1,...,m-1` of (5.2) to recover
`d_(i+1)-d_i=K_iw_i`; the last row gives `w_m=0`.  Conversely the two scalar
recurrences with `w_0=w_m=0` give `Md=0`.  Since all `K_i` are nonzero, no
reconstruction step is singular.

The internal edge signs are

```text
kappa_i=sign(K_i)=(-1)^(i+1).
```

Put `eta_1=1`, `eta_(i+1)/eta_i=kappa_i`, and
`E=diag(eta_i)`.  Then

```text
eta=(+,+,-,-,+,+,-,-,...),
M_tilde=EME,
(M_tilde)_(i,i+1)=-1/abs(K_i)<0.                         (5.4)
```

Thus `M_tilde` is an ordinary irreducible Jacobi matrix to which the exact
finite Sturm oscillation theorem applies.

More importantly, the desired inertia is *exactly equivalent* to positivity
of the path matrix in Section 3.  Consider

```text
H=[ -sigma D   B^T ]
  [    B       -K  ].                                   (5.5)
```

Schur complementation in its two invertible diagonal blocks gives

```text
In(H)=In(-K)+In(M)
     =In(-sigma D)+In(sigma L_sigma).                    (5.6)
```

There are `n` positive and `n-1` negative entries of `K`.  Hence
`L_sigma>0` is equivalent to

```text
max: In(M)=(n negative, n positive, 0 zero),
min: In(M)=((n-1) negative, (n+1) positive, 0 zero).      (5.7)
```

For clarity, if `In(L_sigma)=(ell_-,ell_+,ell_0)`, (5.6) reads explicitly

```text
max: In(M)=(n+ell_-, ell_+-(n-1), ell_0),
min: In(M)=(ell_+-n, n+1+ell_-, ell_0).                  (5.8)
```

Because `ell_-+ell_++ell_0=2n-1`, each target in (5.7) forces
`(ell_-,ell_+,ell_0)=(0,2n-1,0)`, and the converse is immediate.  This
checks both directions separately for max and min.

This proves that the proposed Sturm inertia target is the correct one, but
also shows that it is not a weaker route around the continued fraction: it
is precisely the same missing positive-definiteness theorem in Schur-dual
coordinates.  In particular, the positive pivots in the finite scout imply
the target inertia for each retained record, still only as
`NUMERICAL_EVIDENCE`.

## 6. Physical time translation: exact signs and exact forcing

The autonomous time-translation Jacobi field is

```text
zeta=(U_t,V_t).
```

Its relative event value is

```text
gamma_i
 =p_i/u_i-r_i/V_i
 =(p_i-epsilon_i mu r_i)/u_i
 =S'_i/(2u_i^2).                                        (6.1)
```

Since `S` starts negative and crosses transversely with alternating
orientation,

```text
sign(gamma_i)=(-1)^(i+1).                               (6.2)
```

After the normalization (5.4), `g=E gamma` therefore has the exact pattern

```text
sign(g)=(+,-,-,+,+,-,-,+,...),                          (6.3)
```

and exactly `n` sign changes among its `2n` entries.  In particular, with
the convention `eta_(i+1)/eta_i=sign(K_i)` that makes the off-diagonal
entries negative, the normalized pattern is `+--+`, **not** `++--`.
The latter is the pattern of the gauge `eta` itself.

There is a second important caveat.  Time translation is not in the
equal-component-Wronskian subspace used to derive the homogeneous scalar
word.  On cell `i`, define

```text
X_i=U zeta_U'-U' zeta_U=-(U'^2+rho_i U^2),
Y_i=V zeta_V'-V' zeta_V=-(V'^2+mu^2 rho_i V^2).
```

The common relay energy gives, on every cell including the endpoint cells,

```text
X_i-Y_i=q^2-1=beta^2.                                   (6.4)
```

Both Wronskians have the same saltation jump,

```text
X_i-X_(i-1)=Y_i-Y_(i-1)=alpha_i gamma_i,                (6.5)
```

but they are never equal.  This prevents the tempting, but invalid,
argument that the negative oscillator energy is a positive ground state for
`L_sigma`.

The full two-frequency gluing nevertheless gives an exact forcing formula.
Set, for each internal cell,

```text
chi_i
 =beta^2 sin(theta_i)/[sin(theta_i)+mu sin(mu theta_i)]. (6.6)
```

Then the cell variation formula is

```text
gamma_(i+1)-gamma_i=K_i(Y_i+chi_i),                     (6.7)
```

and (6.5) yields

```text
(M gamma)_1=q^2-chi_1,
(M gamma)_i=chi_(i-1)-chi_i,             1<i<m,
(M gamma)_m=-r_L^2+chi_(m-1),                           (6.8)
```

where `r_L=V_t(L)`.  The endpoint signs are strict:

```text
q^2-chi_1>1>0,
-r_L^2+chi_(m-1)<-p_L^2<0,                              (6.9)
```

because `0<chi_i<beta^2` and `r_L^2-p_L^2=beta^2`.

The phase fraction in (6.6) is itself rigid.  For

```text
F_mu(theta)=sin(theta)/[sin(theta)+mu sin(mu theta)],
0<theta<pi/mu,
```

one has

```text
1/(1+mu^2)<F_mu(theta)<1,       F_mu'(theta)>0.          (6.10)
```

Indeed the sign of its derivative is the sign of
`cot(theta)-mu cot(mu theta)`, which is positive because
`x*cot(x)` is strictly decreasing on `(0,pi)`.  Thus every internal forcing
sign in (6.8) is exactly the sign of
`theta_(i-1)-theta_i`; the trusted closure supplies no all-cell ordering of
these phases.

For any hypothetical zero mode `Md=0`, symmetry and (6.8) impose the new
physical orthogonality constraint

```text
q^2 d_1-r_L^2 d_m
 +sum_(i=1)^(m-1) chi_i(d_(i+1)-d_i)=0.                (6.11)
```

For the abstract `n=2` kernel vector from Section 0 this specializes to

```text
4 chi_1-2 chi_2+4 chi_3=3(q^2+r_L^2).                  (6.12)
```

Equation (6.12), the bounds (6.10), and the gluing equations in Section 1
are genuine additional physical-realizability restrictions absent from the
abstract coefficient word.  They do not, from the currently trusted inputs
alone, give a contradiction for every possible `mu,q,p_L`; therefore the
strong claim that *no* physical realization of the same `(alpha,K)` tuple
exists remains open.  What is proved in Section 2 is the failure of the
specific previously displayed phase/amplitude realization.

## 7. Why Sturm/Picone does not yet close, and the minimal missing lemma

For a homogeneous left-boundary solution of a standard Jacobi equation,
node counting determines the signs of leading continuants and hence the
inertia.  The physical comparison field `g=E gamma` is not such a solution:
after conjugation, (6.8) has distributed internal forcing
`eta_i(chi_(i-1)-chi_i)` of uncontrolled sign.  Its `n` nodes therefore do
not by themselves imply either line of (5.7).

The same obstruction appears in a discrete Picone transform.  The effective
cell flux

```text
Y_i+chi_i<0                                               (7.1)
```

is strictly negative because `-Y_i` is the high-frequency cell energy and
exceeds `beta^2>chi_i`.  It makes (6.7) homogeneous at the cell level, but
its event jump is

```text
(Y_i+chi_i)-(Y_(i-1)+chi_(i-1))
 =alpha_i gamma_i+chi_i-chi_(i-1),                       (7.2)
```

so the same uncontrolled phase difference survives.  Dropping this term
would incorrectly turn time translation into the forbidden equal-Wronskian
ground state.

The following two statements are equivalent strong sufficient lemmas:

```text
PHYSICAL-DISCRETE-HARDY:
For every premise-complete relay word and every nonzero x with x_0=x_m=0,
  sum_i (x_i-x_(i-1))^2/a_i
    > sum_i sigma K_i x_i^2.                             (7.3)

PHYSICAL-STURM-INERTIA:
The normalized matrix EME has the inertia in (5.7).        (7.4)
```

By (5.6), (7.3) and (7.4) are equivalent, and either proves no conjugacy.
They are stronger than the R6 target.  By (3.5b)--(3.5d), the *minimal exact
remaining R6 lemma* on this route is only

```text
PHYSICAL-CONTINUANT-ORIENTATION:
det(L_sigma)>0 for every premise-complete physical relay word.              (7.5)
```

It is equivalent to `J<0`, whereas (7.3)--(7.4) also require every leading
continuant to be positive.  A genuinely more geometric sufficient input
would be a global
ordering/variation theorem for the physical phases `theta_i` strong enough
to control all signs in (6.8) and the endpoint Prüfer angle.  Local phase
bounds (1.7), monotonicity (6.10), palindromy of a reflection-fixed orbit,
or the local diagonal inequalities (3.7) do not supply that theorem.

Accordingly this route is a `RIGOROUS_PARTIAL_RESULT`: it verifies the exact
`M` normalization and target inertia, derives the full time-translation
forcing and a new physical orthogonality constraint, and isolates the
global phase-order/Hardy lemma.  It does not prove the all-`n` R6 sign and
does not produce a physical counterexample.
