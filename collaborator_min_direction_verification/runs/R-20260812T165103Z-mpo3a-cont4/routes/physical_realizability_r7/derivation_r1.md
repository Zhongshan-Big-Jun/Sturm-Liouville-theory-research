RIGOROUS_PARTIAL_RESULT

# R7-R1: exact physical continuant reduction on the relative q-Jacobi line

## 0. Revision contract and immutable provenance

This is a scope-corrected proof package for the exact finite-contrast
continuant reduction.  It does not overwrite the frozen exploratory package
`derivation.md` (24,861 bytes,
`sha256:2a2cbd7d22698a9e2e3f545f3623c1baa8ec7f1f5bb76633538882a25bd0ff41`).
An independent audit of that package found that two sentences used
"nonzero Dirichlet Jacobi field" too broadly: the ever-present scaling field
`(U,V)` is a nonzero two-ended Dirichlet field but maps to zero in the
relative variables below.  This revision therefore makes the quotient by
the scaling direction explicit and proves only the statement actually needed
for the distinguished `log(q)` field.

Bound canonical snapshot:

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:3e0839c6d73e194653314ae1c456bbc77899bdc279f171f590089ad9c0f38394
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Trusted proof inputs, each used only in its accepted scope:

```text
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-STRUCTURE
  semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
CLM-NGE2-MPO3A-SYMPLECTIC-NESTED
  semantic-sha256:4c11a291f871bf44dab3d4970f8b6457bbacafcac6842ae950bd9729be4d2c0e
CLM-NGE2-MPO3A-CELL-PHASE-R6
  semantic-sha256:34ddfc0ec931503621e7658d7186318b41b3f910214000e23c55bae7aaac040e
CLM-NGE2-MPO3A-HYBRID-TWIST-R6
  semantic-sha256:6e2749fd147662212ade344e6dec0a715a83e76cb954e031134748a99a134b7b
DEF-NGE2-MPO3A-SELFCONSISTENCY
  semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
```

No open obligation, numerical observation, reflection-fixed property, or
coefficient-only conjecture is used as a proof input.  In particular,
`CLM-NGE2-MPO3A-TRANSFER-OBSTRUCTION` is background route history only and is
not a premise of this proof.

Fix finite `R>1`, integer `n>=2`, `sigma=+1` for max or `sigma=-1` for min,
and an arbitrary, possibly asymmetric, premise-complete transverse
common-terminal full-relay root.  Put `m=2n`, and let
`t_1<...<t_m` be its simple relay events.  The terminal indexed zeros are
simple, so their derivatives `p=U_t(L)` and `r=V_t(L)` are nonzero.

The result proved below is an exact reduction, not the missing sign theorem:

```text
J<0  iff  det(L_sigma)>0  iff  sign(partial_q A_n)=sigma.       (0.1)
```

It does not assert that any of these equivalent conditions always holds.

## 1. Relative event recurrence from the physical relay

Let `zeta=(u,u_t,v,v_t)=q partial_q(U,U_t,V,V_t)` at fixed `mu`, including
the exact saltation terms at every moving event.  On an open cell define the
equal component Wronskian

```text
w=U u_t-U_t u=V v_t-V_t v.                              (1.1)
```

The equality is the zero signed symplectic pairing with the scaling field.
At event `i` put

```text
U_i=U(t_i),
d_i=u(t_i)/U_i-v(t_i)/V(t_i)
   =delta S(t_i)/(2U_i^2).                              (1.2)
```

The event values are nonzero because every event is a transverse quotient
crossing.  Exact relay saltation gives

```text
w_i-w_(i-1)=alpha_i d_i,
alpha_i=-2 Delta(rho_i) U_i^4/S_t(t_i)=-sigma a_i,
a_i=abs(alpha_i)>0.                                    (1.3)
```

Here `Delta(rho_i)` is material after minus material before the event.  The
last sign uses the accepted alternating crossing orientation and the max/min
relay law; it is not an independently assigned coefficient sign.

For the internal cell `(t_i,t_(i+1))`, set

```text
theta_i=sqrt(rho_i)(t_(i+1)-t_i),
phi_i=mu theta_i.
```

The accepted all-cell phase theorem gives
`0<theta_i<phi_i<pi`.  Eliminating the two exact oscillator cell solutions
gives

```text
d_(i+1)-d_i=K_i w_i,
K_i=[sin(theta_i)+mu sin(phi_i)]
    /[sqrt(rho_i) U_i U_(i+1)].                        (1.4)
```

Thus every `K_i` is finite and nonzero.  The accepted nodal allocation also
gives `sign(K_i)=(-1)^(i+1)`, but only nonvanishing is needed for the
continuant identity.

Equations (1.3)--(1.4) describe relative Jacobi data.  The physical scaling
field `(U,V)` has `d_i=w_i=0` for every `i`; hence this coordinate system is
the quotient by that one-dimensional scaling direction.  No statement below
identifies an arbitrary nonzero physical Dirichlet field with a nonzero
relative vector.

## 2. The Dirichlet path operator

From (1.3),

```text
d_i=-sigma (w_i-w_(i-1))/a_i.                          (2.1)
```

Substitution into (1.4) gives, for `i=1,...,m-1`,

```text
(w_i-w_(i-1))/a_i-(w_(i+1)-w_i)/a_(i+1)
  -sigma K_i w_i=0.                                    (2.2)
```

Define the symmetric `(m-1)`-by-`(m-1)` path matrix `L_sigma` by

```text
(L_sigma)_(ii)=1/a_i+1/a_(i+1)-sigma K_i,
(L_sigma)_(i,i+1)=(L_sigma)_(i+1,i)=-1/a_(i+1).        (2.3)
```

For a relative field satisfying `w_0=w_m=0`, (2.2) is precisely
`L_sigma (w_1,...,w_(m-1))^T=0`.  Consequently
`det(L_sigma)=0` is equivalent to an additional nonzero relative Dirichlet
mode, i.e. a mode after quotienting out the ever-present scaling field.  It
is not equivalent to the existence of an arbitrary nonzero physical
Dirichlet field.

Positive definiteness of `L_sigma` would be a useful stronger sufficient
condition.  It is not equivalent to the terminal orientation sought here,
which fixes only the sign of the final determinant.

## 3. Exact continuant identity for the log(q) field

Before the first event, `U` is independent of `q` while the initial `V`
solution scales with `q`.  Therefore the logarithmic field has

```text
w_0=0,        d_1=-1,        w_1=sigma a_1.            (3.1)
```

Let `W=(w_1,...,w_(m-1))^T`.  Applying (2.2) to the actual field, whose
right flux `w_m` is not imposed to vanish, yields the exact inhomogeneous
Dirichlet equation

```text
L_sigma W=(w_m/a_m)e_(m-1).                            (3.2)
```

When `det(L_sigma)` is nonzero, the standard tridiagonal cofactor expansion
gives

```text
(L_sigma^(-1))_(1,m-1)
  =1/[a_2 ... a_(m-1) det(L_sigma)].                   (3.3)
```

Indeed the corner cofactor is the product of the `m-2` off-diagonal
magnitudes; the two sign factors cancel because `m=2n` is even.  Taking the
first component of (3.2), using (3.1), and multiplying by the positive
denominators gives

```text
w_m=sigma (product_(i=1)^m a_i) det(L_sigma).          (3.4)
```

Both sides are polynomial continuants in the matrix entries, so (3.4) also
holds when the determinant vanishes.  Equivalently, it follows directly by
induction from (1.3)--(1.4), avoiding any inverse at singularity.

For the distinguished `log(q)` field, (3.4) has the precise terminal
degeneracy meaning that was too broadly stated in the original package:

```text
det(L_sigma)=0
 iff w_m=0
 iff partial_q U(L)=partial_q V(L)=0.                  (3.5)
```

The second equivalence uses `w_m=-q p partial_q U(L)`, `p!=0`, and the
accepted terminal symplectic identity
`-p partial_q U(L)+r partial_q V(L)=0` with `r!=0`.
It concerns this q-Jacobi line, not the scaling field or every Jacobi field.

## 4. Binding to the causal Green functional

The accepted hybrid-twist identity, with `J` and all moving events normalized
as in `CLM-NGE2-MPO3A-HYBRID-TWIST-R6`, is

```text
p partial_q U(L)=sigma(R-1)J.                          (4.1)
```

Because the recurrence uses `q partial_q`, its terminal Wronskian is

```text
w_m=-q p partial_q U(L)=-q sigma(R-1)J.                (4.2)
```

The accepted symplectic endpoint formula also gives

```text
partial_q A_n
 =(1-q^2) partial_q U(L)/(p r^2)
 =(q^2-1)w_m/(q p^2 r^2).                              (4.3)
```

Every omitted factor in (3.4), (4.2), and (4.3) is strictly positive:
`q>1`, `R-1>0`, `a_i>0`, and `p^2 r^2>0`.  Hence

```text
J<0
 iff sign(w_m)=sigma
 iff det(L_sigma)>0
 iff sign(partial_q A_n)=sigma.                        (4.4)
```

This proves the advertised exact reduction (0.1).

## 5. Boundary and adversarial audit

The derivation covers every finite `R>1`, every integer `n>=2`, both relay
signs, all premise-complete transverse common-terminal chambers, and
asymmetric as well as reflection-fixed roots.  It treats all `m=2n` events;
the endpoint cells enter through `w_0=0`, the initial datum `d_1=-1`, and the
terminal endpoint identities.  The terminal zeros and every event are simple
in the stated scope.

It does not by itself extend through grazing events, switch collisions,
unfinished relay IVPs, or a closure where the accepted simple-root formulas
cease to be defined.  Such a closure requires a separate limiting theorem.
It proves neither `det(L_sigma)>0` nor positive definiteness, complementary
inertia, global fixed-`mu` root order, unique equal-norm crossing, or O3a.

The following tempting shortcuts are explicitly excluded:

```text
1. A nonzero physical Dirichlet field need not give nonzero (d,w):
   the scaling field is the permanent counterexample.
2. Local signs of alpha_i and K_i do not fix the final continuant.
3. Positive definiteness and positivity of all leading pivots are stronger
   than the required sign det(L_sigma)>0.
4. Finite numerical positivity, phase ordering on reflection-fixed samples,
   and a failed supersolution candidate are non-propagating route evidence.
5. A local twist sign, even once proved, still needs global chamber/closure
   order before reflection can yield universal uniqueness.
```

The minimal remaining finite-contrast obligation on this route is therefore

```text
For every premise-complete physical relay word in the stated scope,
prove det(L_sigma)>0, or rigorously certify a physical word with
det(L_sigma)<=0 and supply the additional global bifurcation/distinct-root
predicates required for an O3a refutation.                              (5.1)
```

Status: `RIGOROUS_PARTIAL_RESULT`.  The exact reduction is proved; the
universal determinant sign and universal O3a remain open.
