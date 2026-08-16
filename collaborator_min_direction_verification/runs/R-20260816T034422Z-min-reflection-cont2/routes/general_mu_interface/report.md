RIGOROUS_PARTIAL_RESULT

# C2-H: an explicit all-`mu` weak-contrast collar for the full `n=2` minimum interface

## 0. Exact result and scope

Fix any finite `mu>1` and a strict physical positive-negative interface with

```text
0<alpha<pi/(mu+1)<beta<pi/mu,
```

common negative energy, both independent momentum matches, and the strict
first-crossing amplitude branch.  This route proves an explicit positive
threshold `tau(alpha,beta,mu)>0` such that the exact left split gap is
strictly positive whenever

```text
R-1<tau(alpha,beta,mu).                                (0.1)
```

The same statement applies after time reversal at the right interface.  For
an arbitrary asymmetric positive-negative-positive three-cell word, if
`tau_L,tau_R` are computed from its actual two interface phase pairs, then

```text
R-1<min(tau_L,tau_R)                                   (0.2)
```

implies both split gaps are positive and hence the scalar dual Schur
complement `H>0`.  No equality of the left and right positive phases and no
reflection hypothesis is used.

The threshold is pointwise in the phases.  No positive infimum over all
physical phase pairs is proved, so this does not complete the general-`mu`,
all-finite-contrast interface lemma or global reflection symmetry.

## 1. Exact common-angle reduction

For `0<theta<pi/mu` put

```text
s=sin(theta), S=sin(mu theta), c=cos(theta), C=cos(mu theta),
F=S/s,                    U=1/s+mu/S,
Q=s+mu S,
x=(F c-mu C)/(F+mu),      rho=(mu F+1)/(F+mu),
p=Q/U,
e=(mu^2-1)F(c+C)/(F+mu)^2,
kappa=1-x^2-p.
```

Use `+` at `alpha` and `-` at `beta`.  The strict phase theorem gives

```text
x_+,x_-,p_+,p_-,kappa_+,kappa_->0,
rho_+>1>rho_-,            e_+>0>e_-.
```

Set

```text
lambda=U_+/U_->0,         d=rho_+-rho_->0,
eta=-e_->0,               delta=r^2-1=R-1,
w=(e_+-r eta/lambda)/d,   u=x_++w,
A0=1-x_+u.                                            (1.1)
```

Solving the two momentum equations as one two-dimensional Cramer system
gives (1.1), while the negative-cell amplitude margin is

```text
B0=lambda w/r-x_->0.
```

Thus the strict branch has

```text
1<r<rB,     rB=lambda e_+/(eta+d x_-).                (1.2)
```

Direct substitution in the switch-derivative split gives

```text
N_left=U_+^2 Phi/(lambda u^3),                         (1.3)

Phi=(lambda^2w^2+r^2kappa_-+p_-)
       (A0+delta p_+u^2)-delta p_-w u^3.              (1.4)
```

All factors in the prefactor in (1.3) are positive.  Equations (1.1)--(1.4)
are the exact normalized form of the simultaneous two-momentum interface
calculation; no gamma-only relaxation is used.

## 2. Reproof of the strict positive-cell margin

The one-cell inequality needed below is

```text
p_+(rho_+-1)-x_+e_+>0.                                (2.1)
```

For the positive phase abbreviate

```text
D=S+mu s, Q=s+mu S, N=S c-mu s C.
```

Exact reduction gives

```text
p(rho-1)-xe
=(mu-1)sS/D^3 {QD(S-s)-(mu+1)N(c+C)}.                 (2.2)
```

Let

```text
A=(mu+1)alpha/2, B=(mu-1)alpha/2, q=B/A=(mu-1)/(mu+1).
```

Then `0<B<A<pi/2`, and the brace in (2.2) is exactly

```text
2(mu+1)^2 cos(A)^3 cos(B)
 {q tan(A)-tan(B)[cos(B)^2+q^2 sin(B)^2]}.             (2.3)
```

Since `tan(t)/t` is strictly increasing,
`tan(B)<q tan(A)`.  Since `0<q<1`, the square bracket multiplying
`tan(B)` is strictly below one.  Hence (2.3), (2.2), and (2.1) are strict.

Because `d>rho_+-1`, formula (1.1) yields, for every `r>=1`,

```text
p_+-x_+w
 ={p_+d-x_+e_++x_+r eta/lambda}/d>0,

A0=kappa_++p_+-x_+w>kappa_+>0.                        (2.4)
```

This rederives the required positive margin on the exact common-angle curve.

## 3. A new three-positive-block decomposition

Using `r^2=1+delta`, (1.4) has the exact identity

```text
Phi
=p_-[A0-delta w u^3]
 +(lambda^2w^2+(1+delta)kappa_-)A0
 +delta p_+u^2[lambda^2w^2+(1+delta)kappa_-+p_-].     (3.1)
```

The last two lines are strictly positive.  Therefore

```text
Lambda:=A0-delta w u^3>0       implies       Phi>0.   (3.2)
```

A second decomposition completes the square in three terms of (1.4):

```text
lambda^2 A0 w^2+delta p_+p_-u^2-delta p_-w u^3

=lambda^2A0[w-delta p_-u^3/(2lambda^2A0)]^2
 +delta p_-u^2 Xi/(4lambda^2A0),                      (3.3)

Xi=4lambda^2p_+A0-delta p_-u^4.
```

All omitted terms of `Phi` are strictly positive, so

```text
Xi>0       implies       Phi>0.                       (3.4)
```

These are direct analytic dominations, not interval subdivision or a
Bernstein cover.

## 4. Explicit phase-only collar

Evaluate (1.1) at the formal contrast endpoint `r=1`:

```text
w0=(e_+-eta/lambda)/d,   u0=x_++w0,
A00=1-x_+u0.                                            (4.1)
```

If the physical branch is nonempty, then `rB>1` and `w0>0`; also `u0>0`
and (2.4) gives `A00>kappa_+>0`.  With

```text
c0=eta/(lambda d)>0,
```

the exact contrast dependence is

```text
w=w0-c0(r-1),   u=u0-c0(r-1),
A0=A00+x_+c0(r-1).                                    (4.2)
```

Hence on the strict physical branch

```text
0<w<w0,       0<u<u0,       A0>A00.
```

Define two positive phase-only thresholds

```text
tau_1=A00/(w0 u0^3),
tau_2=4lambda^2p_+A00/(p_-u0^4),
tau=max(tau_1,tau_2)>0.                               (4.3)
```

If `delta=R-1<tau_1`, then

```text
delta w u^3<delta w0u0^3<A00<A0,
```

so (3.2) proves `Phi>0`.  If instead `delta<tau_2`, then

```text
delta p_-u^4<delta p_-u0^4
 <4lambda^2p_+A00<4lambda^2p_+A0,
```

so (3.4) proves `Phi>0`.  Thus `delta<tau` is sufficient.  Equivalently,
the complete local contrast interval certified by this route is

```text
1<R<min(rB^2,1+tau).                                  (4.4)
```

Both upper endpoints in (4.4) exceed one, so this interval is strictly
nonempty for every finite `mu>1` and every phase pair with a nonempty
physical branch.

## 5. Arbitrary asymmetric three-cell corollary

This section derives the gluing rather than treating it as an imported
identity.  For any cell write

```text
g=x-mu y,             h=-x_R+mu y_R,
Q=sin(theta)+mu sin(mu theta).                       (5.1)
```

At a positive-negative interface let the positive amplitude ratio be
`a>0`, write the negative ratio as `-B` with `B>0`, and put

```text
g_+,h_+>0,             G=-g_->0,       J=-h_->0.
```

The physical gamma match is `h_+=rG`.  With `delta=r^2-1`, define

```text
D_1=delta a Q_+ +rG+a^2g_+>0,

N_L=r^2aB(G+J)(delta Q_+ +a g_+)-delta Q_-D_1.       (5.2)
```

The exact elimination in Section 1 is precisely

```text
N_L=U_+^2 Phi/(lambda u^3).                          (5.3)
```

To expose the Schur factors, use homogeneity to normalize the middle-cell
scale by `u_2^2=1`.  Then

```text
abs(K_2)=Q_-/(rB)>0,
x_*^L=r(G+J)/abs(K_2),

beta_R=a h_+(delta Q_+ +a g_+)/(delta D_1),
E_L=beta_R x_*^L-rG
   =rG N_L/(delta D_1Q_-).                           (5.4)
```

Every factor multiplying `N_L` in (5.4) is strictly positive.  Restoring
an arbitrary nonzero middle-cell scale multiplies numerator and denominator
homogeneously and does not change the sign.

For the original negative-positive orientation at a right interface, time
reversal sends every amplitude ratio `z` to `1/z` and exactly interchanges
`g` and `h`.  Thus, putting

```text
c=1/a, B_R=1/B,
g_R=h_+, h_R=g_+, G_R=J, J_R=G,                     (5.5)
```

both right-interface momentum equations are the reversals of the two
equations checked in Section 1.  Moreover

```text
D_3=delta cQ_+ +h_R+c^2rJ_R=D_1/a^2>0,

N_R=r^2(G_R+J_R)(delta cQ_+ +h_R)-delta Q_-B_RD_3
   =N_L/(a^2B),                                      (5.6)

beta_L=g_R(delta cQ_+ +h_R)/(delta D_3B_R^2),
E_R=beta_L x_*^R-rJ_R
   =rJ_R N_R/(delta D_3B_RQ_-),
x_*^R=r(G_R+J_R)/(Q_-/(rB_R)).                       (5.7)
```

Hence time reversal preserves the strict sign: both `N_R/N_L=1/(a^2B)`
and the prefactor in (5.7) are positive.  The checker verifies the two
right momentum equations, all four swaps in (5.5), and (5.4)--(5.7)
exactly.  This is a local reciprocity statement, not an assumption that the
two positive cells of a three-cell word agree.

Now take the actual middle negative cell of a possibly asymmetric
positive-negative-positive word.  In one common physical normalization,

```text
gamma_2=-rG<0,                  gamma_3=rJ>0,
W=abs(K_2)>0,
x_*=(gamma_3-gamma_2)/W=r(G+J)/W>0,
H=beta_R+beta_L-W.                                    (5.8)
```

The two split gaps are

```text
E_L=beta_R x_*+gamma_2,
E_R=beta_L x_*-gamma_3,

E_L+E_R=(beta_R+beta_L-W)x_*=H x_*.                  (5.9)
```

Run Sections 1--4 on the actual left phase pair and, using (5.5)--(5.7),
on the time reversal of the actual right phase pair.  Call the independently
computed thresholds `tau_L,tau_R`.  Equations (5.3)--(5.9) show

```text
R-1<min(tau_L,tau_R)  => E_L,E_R>0 => Hx_*>0 => H>0. (5.10)
```

This is genuinely left/right asymmetric: no phase or amplitude equality is
used, and the two local positive prefactors need not be equal.

## 6. Exact no-go for extending these two factors globally

Neither `Lambda>0` nor `Xi>0` is a valid all-contrast intermediate lemma.
The checker constructs the exact same-angle physical local interface

```text
mu=2,
tan(alpha/2)=1/100,
tan(beta/2)=3/5,
rB=4798560/38791,
r=4837351/77582=(1+rB)/2.                             (6.1)
```

The strict phase thresholds follow from
`3(1/100)^2<1<3(3/5)^2`, and `3/5<1`.  Double-angle formulas impose the
common-angle equations exactly.  Exact rational arithmetic verifies

```text
1<r<rB, w>0, u>0, A0>0, B0>0,
Lambda<0, Xi<0, but Phi>0.                             (6.2)
```

Thus (6.1) is not a counterexample to the interface lemma; it is an exact
physical counterexample only to global positivity of the two new sufficient
factors.  Beyond (4.4), this direct decomposition requires a new
redistribution of the remaining positive blocks in (3.1)--(3.3), or a
different common-angle curvature invariant.  Merely asserting `Lambda>0`
or `Xi>0` cannot close full contrast.

## 7. Boundary and non-duplication audit

- `n=2`: the conclusion is only the scalar three-cell Schur complement.  It
  does not control transfer terms for `n>2`.
- `R->1+`: at `R=1`,
  `Phi=(lambda^2w0^2+kappa_-+p_-)A00>0`; (4.4) makes the
  one-sided collar quantitative.  `R=1` itself is outside the bang-bang
  problem.
- `mu->1+`: every fixed `mu>1` is covered.  The interface normalization
  degenerates at `mu=1`, and no lower bound for `tau` uniform as `mu->1+`
  is asserted.
- `mu->infinity`: every finite `mu` and strict phase pair is covered, but
  phases shrink with `mu` and no uniform large-`mu` threshold is asserted.
- Phase and amplitude boundaries: `alpha=0`, either phase threshold,
  `beta=pi/mu`, `B0=0`, and grazing are excluded.  Limits may make `tau`
  tend to zero; no closed-boundary claim is made.
- Empty branch: if `rB<=1`, there is no strict physical contrast to which
  the local claim applies.
- Left/right asymmetry is explicit in section 5.
- The canonical theorem `CLM-NGE2-MPO3A-SMALL-CONTRAST` states fixed-`n`
  existence, uniqueness, and reflection for some non-effective global
  `epsilon_n`.  The present result neither reproves nor weakens that theorem:
  it is a conditional local inertia/interface statement with an explicit
  phase-dependent threshold, does not prove uniqueness or reflection, and
  does not supply a uniform infimum over all roots.  Conversely, uniqueness
  alone does not imply the Schur sign `H>0`.
- At `mu=2`, the canonical full-contrast theorem
  `CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10` is stronger.  The new content is the
  arbitrary-`mu` collar, especially `mu!=2`.

## 8. Exact verification, provenance, and calibrated status

Replay:

```text
E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe runs/R-20260816T034422Z-min-reflection-cont2/routes/general_mu_interface/exact_checker.py
```

The checker uses Python 3.12.13 and SymPy 1.14.0.  It independently solves
both momentum equations, verifies the normalized Cramer coordinates and
the full bridge (1.3)--(1.4), and then verifies (2.2)--(2.3), (3.1), (3.3),
(4.2), and the exact physical no-go witness (6.1)--(6.2).
Its main decomposition hash is

```text
ff4c0cacb11e7e442006a255ff7556de0c33d0d280a6aa134c94e18920b8f63c.
```

Human contribution: target and continuation constraints.  Model
contribution: the positive-block decomposition, square completion, explicit
collar, asymmetric gluing, and exact factor no-go.  Tool contribution: exact
rational-function identities, exact rational witness verification, and
content hashing.

```text
new exact result: arbitrary-mu, asymmetric n=2 weak-contrast H>0 collar
general-mu all-finite-contrast interface: OPEN
global minimum reflection: OPEN outside already trusted scopes
physical counterexample to Phi or H positivity: NONE
novelty_status: unknown
confidence_semantic_fidelity: high
confidence_proof_correctness: high before independent review
confidence_target_completeness: low
confidence_reproducibility: high
formalization_status: not_requested
```
