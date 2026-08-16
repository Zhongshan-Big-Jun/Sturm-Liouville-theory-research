BLOCKED_REDUCTION

# MIN-REFL-C2-B: exact two-root Picone transport and the unavoidable skew-polarization obstruction

## 0. Route registry

```text
route_id: MIN-REFL-C2-B
target_inference_or_goal: minimum-side global reflection fixing at fixed (R,n,mu)
method_family: two-root Green/Picone identities, endpoint norming transport, relay Minty monotonicity, reflection-sector decomposition
local_hypotheses: two premise-complete physical minimum-law roots; no reflection, uniqueness, endpoint order, or q-Jacobi regularity
allowed_trusted_inputs:
  HYP-NGE2-DOMAIN semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5
  DEF-NGE2-MPO3A-SELFCONSISTENCY semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
  CLM-NGE2-MPO3A-STRUCTURE semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
  CLM-NGE2-MPO3A-FULL-RELAY semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
  CLM-NGE2-MPO3A-SYMPLECTIC-NESTED semantic-sha256:4c11a291f871bf44dab3d4970f8b6457bbacafcac6842ae950bd9729be4d2c0e
  CLM-NGE2-MPO3A-DEFECT semantic-sha256:1421c349587987174e25d68a2f4f101bbe2ddd0a342e1c5f134c8dbd6f80032f
  CLM-NGE2-MPO3A-PARAMETER-ACTION-R1 semantic-sha256:e7b57c2609991baea373a087ffc72da945e4a8b018d4bf33559908d09167ab06
  CLM-NGE2-MPO3A-INTERNAL-PHASE-R8 semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702
forbidden_open_inputs: reflection, endpoint order, uniqueness, det(H)>0, a sign for mixed polarization, or a nonphysical separation model as a physical counterexample
current_status: blocked after exact endpoint transport, a signed same-mode identity, and a full-rank no-go for linear Green/Pohozaev elimination
proved_results:
  - arbitrary-two-root endpoint-determinant transport formula (3.8)
  - same-length minimum-relay Minty identity (4.3)
  - exact reflection-sector mismatch identity (5.8)
  - full-rank persistence of a cross-mode skew term under all fixed linear combinations of scalar cross Green/energy transports
candidate_results: none
counterexamples: exact local sign witnesses only; no global physical counterexample
first_failing_step: the relay sign controls a same-mode polarization, while endpoint order requires a linearly independent cross-mode skew polarization
precise_gap: obtain a new cross-root projective cone, null-event interlacing, or spectral-sector theorem that controls the skew polarization globally
gap_strength: the endpoint formula itself is equivalent to endpoint order and is not progress toward the target; the rank/no-go is a strictly weaker reusable failure result
restart_conditions:
  - a componentwise two-root ordering of the zeros of u+mu v and u-mu v that signs the skew interface flux before endpoint data are used; or
  - an independently proved reflection-sector spectral localization theorem for the symmetric averaged coefficient
next_action: do not repeat Green/Picone/Pohozaev linear recombination without one of those new inputs
```

No canonical Blueprint file, submission, review, or receipt is modified by this route.

## 1. Snapshot and scope

All canonical retrievals were bound to

```text
context: CTX-DEFAULT
blueprint: sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory: sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Fix finite `R>1`, integer `n>=2`, and `mu>1`.  Root `j` is an arbitrary
premise-complete minimum-law full-relay root on `[0,L_j]`, with initial and
terminal slopes

```text
(U_j',V_j')(0)=(1,q_j),
(U_j',V_j')(L_j)=(p_j,r_j).
```

It has `2n` transverse events and equal norms.  Put

```text
h_j=abs(r_j)/abs(p_j).
```

The ordered-reflection bridge requested by the parent route is

```text
q_1<q_2  =>  h_1<=h_2.                               (1.1)
```

No differentiability of a root sheet is assumed, so every identity below
also applies at a singular `q`-Jacobi root.

## 2. Put arbitrary roots on one interval

Set `a_j=L_j^2` and, for `0<=x<=1`,

```text
u_j(x)=U_j(L_j x)/L_j,
v_j(x)=V_j(L_j x)/L_j,
rho_j(x)=rho_j(L_j x).                                (2.1)
```

Then

```text
-u_j''=a_j rho_j u_j,
-v_j''=mu^2 a_j rho_j v_j,                           (2.2)
u_j(0)=v_j(0)=u_j(1)=v_j(1)=0,
(u_j',v_j')(0)=(1,q_j),
(u_j',v_j')(1)=(p_j,r_j).                            (2.3)
```

The sign of the switching function is unchanged:

```text
S_j=u_j^2-mu^2 v_j^2,
rho_j=R on {S_j<0}, rho_j=1 on {S_j>0}.               (2.4)
```

Writing

```text
J_j=integral rho_j u_j^2=integral rho_j v_j^2,
```

the global relay energy gives

```text
q_j^2-1=2 a_j (mu^2-1)J_j,
p_j^2-r_j^2=1-q_j^2.                                 (2.5)
```

Sturm parity fixes

```text
p_j=(-1)^n P_j, r_j=(-1)^(n+1) R_j,
P_j=abs(p_j), R_j=abs(r_j).                          (2.6)
```

## 3. Exact cross-Picone endpoint transport

### Lemma 3.1 (matrix cross-energy identity)

Let

```text
X_j=(u_j,v_j)^T,
D=diag(1,mu^2),
A_j=a_j rho_j,
C=an arbitrary constant 2 by 2 matrix.               (3.1)
```

On a cell of the common refinement of the two switch partitions, define

```text
M_C=(A_1 D C+A_2 C D)/2,
K_C=A_1 D C-A_2 C D,
E_C=X_1'^T C X_2'+X_1^T M_C X_2.                    (3.2)
```

Then

```text
E_C'=[X_1'^T K_C X_2-X_1^T K_C X_2']/2.             (3.3)
```

At a switch of root 1 or root 2, respectively,

```text
Delta E_C=(Delta A_1/2)X_1^T D C X_2,
Delta E_C=(Delta A_2/2)X_1^T C D X_2.                (3.4)
```

#### Proof

Differentiate (3.2) on a common-refinement cell and substitute
`X_j''=-A_j D X_j`.  The two coefficients of `X_1'` and `X_2'` are
`K_C/2` and `-K_C/2`, which proves (3.3).  The states and first derivatives
are continuous at every relay event; only `M_C` jumps.  Its root-1 and
root-2 jumps are `Delta A_1 D C/2` and `Delta A_2 C D/2`, proving (3.4).
At both endpoints `X_j=0`, so integration gives the endpoint derivative
bilinear without additional boundary terms.  QED.

Take the skew matrix

```text
J_0=[[0,1],[-1,0]].                                  (3.5)
```

The endpoint bilinear is the oriented slope determinant.  Lemma 3.1 gives

```text
p_1 r_2-r_1 p_2=(q_2-q_1)+Psi_12-Psi_21,            (3.6)
```

where

```text
Psi_12=
  (1/2) integral (A_1-mu^2 A_2)(u_1'v_2-u_1v_2') dx
  +sum Delta[(A_1+mu^2 A_2)/2] u_1v_2,

Psi_21=
  (1/2) integral (mu^2 A_1-A_2)(v_1'u_2-v_1u_2') dx
  +sum Delta[(mu^2 A_1+A_2)/2] v_1u_2.               (3.7)
```

By (2.6), the left side of (3.6) is
`P_1P_2(h_1-h_2)`.  Thus the exact two-root bridge is

```text
P_1P_2(h_1-h_2)=q_2-q_1+Psi_12-Psi_21.              (3.8)
```

For `q_1<q_2`, (1.1) is equivalent to

```text
Psi_12-Psi_21<=-(q_2-q_1).                           (3.9)
```

Consequently (3.8) is an exact diagnostic, not a weaker theorem.  It must
not be promoted as progress toward reflection.

## 4. What the minimum relay law actually signs

When `a_1=a_2=a` (in particular for a root and its reflection), put
`bar(rho)=(rho_1+rho_2)/2`, `delta u=u_1-u_2`, and similarly for `v`.
Subtracting (2.2), testing by the differences, and integrating gives

```text
Q=
 integral [(delta u')^2-(delta v')^2
           -a bar(rho)((delta u)^2-mu^2(delta v)^2)] dx
 =a/2 integral (rho_1-rho_2)(S_1-S_2) dx.            (4.1)
```

The minimum relay graph is antitone, hence pointwise

```text
(rho_1-rho_2)(S_1-S_2)<=0,                           (4.2)
```

and therefore

```text
Q<=0.                                                (4.3)
```

This is the complete signed two-root identity supplied by relay
monotonicity.  It is a same-mode quadratic form.  It contains neither slope
determinant in (3.8) nor either cross-mode product `u_1v_2`, `v_1u_2`.

If the terminal lengths differ, the same calculation with
`A_j=a_j rho_j` contains

```text
(1/2) integral (A_1-A_2)(S_1-S_2)
 =bar(a)/2 integral (rho_1-rho_2)(S_1-S_2)
  +(a_1-a_2)/2 integral bar(rho)(S_1-S_2),            (4.4)
```

where `bar(a)=(a_1+a_2)/2`.  Only the first term has a relay sign.  The
second scale term is not removed by the two separate equal-norm equations;
they contain no cross-weight integrals.  Thus unequal lengths add an
obstruction, but are not the first obstruction: Section 6 shows failure
even when `a_1=a_2`.

## 5. Exact reflection-sector form of the signed identity

This section records the strongest favorable specialization.  It still does
not orient (3.8).

For one root, let `s=sign(p)=(-1)^n`, `P=abs(p)`, and let `#` denote its
positively oriented reflection.  Define symmetrically scaled fields

```text
f=U/sqrt(P),       f#=sqrt(P) U#=-s f(L-t),
g=V/sqrt(P),       g#=sqrt(P) V#= s g(L-t).           (5.1)
```

Put

```text
d_U=f-f#, e_U=f+f#,
d_V=g-g#, e_V=g+g#,
rho_0=(rho+rho#)/2, rho_a=(rho-rho#)/2.               (5.2)
```

Their reflection parities are

```text
d_U: s, e_U: -s, d_V: -s, e_V: s.                   (5.3)
```

Subtracting the reflected equations yields

```text
-d_U''=rho_0 d_U+rho_a e_U,
-d_V''=mu^2(rho_0 d_V+rho_a e_V).                    (5.4)
```

All four functions are Dirichlet at both ends.  Therefore

```text
 integral [d_U'^2-d_V'^2-rho_0(d_U^2-mu^2d_V^2)]
 =integral rho_a(d_Ue_U-mu^2d_Ve_V).                 (5.5)
```

With

```text
T=f^2-mu^2g^2, T#=f#^2-mu^2g#^2=T(L-t),             (5.6)
```

the last integrand is `(rho-rho#)(T-T#)/2`.  Since the minimum word is
`R` on the negative cone and `1` on the positive cone,

```text
Q_reflection
 =-(R-1)/2 integral_M abs(T-T#) dt <=0,              (5.7)
M={t:T(t)T#(t)<0}.
```

Transversality makes zero sets negligible.  Hence

```text
Q_reflection<0 exactly when rho differs from rho# on positive measure.
                                                               (5.8)
```

This is a useful spectral signature of any asymmetric root, but its
vanishing criterion is equivalent to reflection and is not itself a proof.

For completeness, the initial derivatives satisfy

```text
d_U'=(1-P)/sqrt(P), e_U'=(1+P)/sqrt(P),
d_V'=(q-Ph)/sqrt(P), e_V'=(q+Ph)/sqrt(P),             (5.9)
d_U'e_U'=d_V'e_V'.                                  (5.10)
```

Equation (5.10) is just the terminal relay energy
`q^2-1=P^2(h^2-1)`; it adds no sign for the mixed term below.

## 6. The first uncontrolled term

At a switch belonging only to root 1, the jump contribution in (3.8) is

```text
(a_1 Delta rho_1/2)(u_1v_2-mu^2v_1u_2).             (6.1)
```

At a switch belonging only to root 2 it is

```text
(a_2 Delta rho_2/2)(mu^2u_1v_2-v_1u_2).             (6.2)
```

These are cross-mode **skew polarizations**.  The relay law controls the
self polarizations `S_j`; the earlier cross-Wronskian route encountered the
symmetric Minkowski polarization `u_1u_2-mu^2v_1v_2`.  Neither controls
(6.1) or (6.2).

The same distinction appears in the reflection-sector equations.  The
signed Minty term is

```text
A=d_Ue_U-mu^2d_Ve_V=T-T#,                            (6.3)
```

whereas the cross-Picone Wronskian of `d_U,d_V` contains

```text
M=e_Ud_V-mu^2e_Vd_U.                                 (6.4)
```

As linear forms in `(e_U,e_V)`, their coefficient matrix has determinant

```text
det [[d_U,-mu^2d_V],[d_V,-mu^2d_U]]
 =mu^2(d_V^2-d_U^2).                                 (6.5)
```

It is generically full rank.  A sign for `A` therefore leaves `M` free.

### Exact same-quadrant witnesses

Take `mu=2` and suppose root 1 is at the positive null event

```text
(u_1,v_1)=(2,1).
```

Keep root 2 in the same positive nodal quadrant and on the same minimum
material side `S_2<0`.  The two exact choices

```text
(u_2,v_2)=(1/4,1): S_2=-63/16, (6.1)-polarization=+1,
(u_2,v_2)=(1,1):   S_2=-3,     (6.1)-polarization=-2                (6.6)
```

have opposite skew signs.  Choosing `(u_1',v_1')=(0,-1)` gives
`S_1'=8>0` and signed relay energy `u_1'^2-v_1'^2=-1<0`, so both are
compatible with the same transverse minimum-law event direction and the
physical `q>1` energy sign for any fixed finite `R>1`.  Taking zero
derivatives for root 2 also gives negative energy `R S_2<0`.  Local IVP
existence supplies piecewise-classical relay jets.  These are not asserted
to extend to global common-terminal roots.

The reflection-sector freedom persists with all four values positive and
the same mismatch direction `T<0<T#`:

```text
(f,f#,g,g#)=(8,7,5,3): T=-36,  T#=13, A=-49,  M=-2,
(f,f#,g,g#)=(8,7,8,3): T=-192, T#=13, A=-205, M=31.                 (6.7)
```

Thus even strict Minty negativity does not sign the first Picone skew term.

## 7. Full-rank no-go for linear Green/Pohozaev elimination

It remains to check that equal norm, same-mode Green identities, or
Pohozaev weights cannot linearly remove (6.1)--(6.2).

For each root separately, equal norm and the exact weighted virials are

```text
J_j=integral rho_j u_j^2=integral rho_j v_j^2,
p_j^2=2a_jJ_j+a_j sum_x x Delta rho_j u_j(x)^2,
r_j^2=2mu^2a_jJ_j+mu^2a_j sum_x x Delta rho_j v_j(x)^2.  (7.1)
```

At its own events `u_j^2=mu^2v_j^2`, so the two jump moments in (7.1)
are the same.  Thus every term in (7.1) is a self monomial of root `j`;
neither identity supplies `u_1v_2` or `v_1u_2`.

Lemma 3.1 already represents every fixed linear combination of the four
scalar cross-energy transports by one matrix `C`.  At a root-1 event its
cross jump is

```text
(Delta A_1/2)X_1^T D C X_2.                          (7.2)
```

The alternating event rays are

```text
X_1=c(+mu,1)^T and X_1=c(-mu,1)^T.                   (7.3)
```

For (7.2) to lose all free cross dependence on `X_2` at both event types,
one must have

```text
[[mu,mu^2],[-mu,mu^2]] C=0.                          (7.4)
```

The left matrix has determinant

```text
2mu^3 !=0,                                           (7.5)
```

so (7.4) forces `C=0`.  The same conclusion follows from root-2 events.
In particular the nonzero endpoint-determinant matrix `J_0` necessarily
leaves a skew cross term.

The two self norm and self Pohozaev identities add only monomials belonging
to one root.  They cannot cancel a bilinear expression in `X_1,X_2` for all
`X_2` in an open material cone.  Unweighted Green identities can redistribute
bulk same-mode terms but have no coefficient-jump term and do not change
(7.4).  Root-dependent global scalar weights likewise do not change the
rank.  Therefore no fixed linear combination of the available two-root
Green identities and the two separate equal-norm/Pohozaev identities can
rewrite the endpoint determinant correction as
`(rho_1-rho_2)(S_1-S_2)` or as a sum of signed squares.

The bulk part of (3.7) is also unsignable pointwise: the material law fixes
positions through `S_j`, while the two cross-mode Wronskians can take either
sign under locally admissible derivative data.  The interface rank
obstruction already suffices; no bulk cancellation can repair a
noncoincident event jump.

This is a no-go for the proposed **linear Picone/Green/Pohozaev mechanism**.
It does not rule out a nonlinear global theorem correlating all events of
two complete roots.

## 8. Non-equivalent restart conditions

Rearranging (3.8), (4.1), or the individual Pohozaev identities is exhausted.
The route may be reopened only after a new structural input, for example:

1. **Null-event interlacing and cone invariance.**  Before using endpoint
   slopes, prove a componentwise order for the zeros of `u+mu v` and
   `u-mu v` between two ordered roots, together with a common-refinement
   projective cone that signs `X_1^T D J_0X_2`, `X_1^T J_0D X_2`, and the
   corresponding bulk Wronskian on every mismatch component.  This is a
   trajectory-level crossing theorem, not endpoint order in disguise.
2. **Reflection-sector spectral localization.**  For the symmetric average
   `rho_0`, prove from nodal or orthogonality data that the forced parity
   component `d_U` lies in the nonnegative spectral sector of the quadratic
   form at frequency `1`, while `d_V` lies in the nonpositive sector at
   frequency `mu^2`, with a strict alternative for a nonzero pair.  This is
   an independently falsifiable spectral-projection statement; it would
   oppose (5.8) without assuming endpoint order.
3. **A fully physical pair.**  Certify two distinct equal-norm minimum roots,
   including all indexed phases, events, and residuals.  The local witnesses
   in Section 6 are not such a pair.

Merely postulating the sign or total size of `Psi_12-Psi_21` is not a restart:
by (3.8) that postulate is exactly the endpoint-order target.

## 9. Boundary audit

- **`n=2`.**  Four events include both null rays in (7.3), so the rank
  obstruction is already present in the smallest mandatory case.
- **`n>=3`.**  The proof is independent of event count beyond the presence
  of both alternating event types.
- **Different chambers and switching patterns.**  Lemma 3.1 uses their
  common refinement.  Simultaneous events contribute the sum of (6.1) and
  (6.2); noncoincident events are explicitly retained.
- **Equality.**  All identities are non-strict and remain valid when two
  roots or event locations coincide.  No division by `q_2-q_1` is used.
- **`R` down to `1`.**  Every statement assumes `R>1`.  The local sign
  freedom holds for every finite `R>1`; no uniform nonzero jump margin is
  asserted as `R` tends to `1`.
- **Large finite `R`.**  No bounded-contrast estimate is used.
- **Unequal terminal lengths.**  They are covered by (2.1)--(3.8), with the
  additional unsigned scale term (4.4).
- **Reflection pair / equal length.**  The scale term vanishes, yet Sections
  5--7 retain the skew obstruction.
- **Singular `q`-Jacobi roots.**  The proof is finite-difference and uses no
  parameter derivative, so singular roots are included.
- **Global counterexample status.**  No asymmetric or singular physical
  root is claimed.  Section 6 proves only local algebraic sign freedom of
  the comparison mechanism.

## 10. Reproducibility and calibration

The exact checker verifies the cellwise derivative identity, both event
skew formulas, the determinant `2mu^3`, the reflection-sector rank, and all
rational witnesses:

```text
E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe
  runs\R-20260816T034422Z-min-reflection-cont2\routes\cross_picone\exact_checker.py
```

Expected output:

```text
PASS: scalar identity, full-rank event obstruction, and rational sign witnesses
```

No random sampling, floating arithmetic, literature import, or Lean
formalization is used.

```text
target reflection claim: OPEN
endpoint-order bridge: exact but equivalent to the target on the root set
same-length Minty identity: PROVED
reflection-sector mismatch identity: PROVED
linear Picone/Green/Pohozaev route: AUDITED FAILURE at a full-rank skew term
formalization_status: not_requested
novelty_status: unknown
```

Contributions:

```text
human: selected the minimum-side global-reflection target and continuation budget
model: derived and boundary-audited the identities and rank obstruction
tool: SymPy checked exact polynomial identities, ranks, and rational witnesses
external sources: none
```

Confidence:

```text
semantic fidelity: high
correctness of displayed identities and no-go: high
completeness for global reflection: low (target remains open)
novelty: unknown
reproducibility: high
```
