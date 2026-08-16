RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-G: full two-momentum shared-contrast elimination at `n=3`

## 0. Calibrated result

This route is bound to `CTX-DEFAULT`, Blueprint
`sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0`,
inventory
`sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`,
and target
`OBL-NGE2-MPO3A-MIN-DET-H-POSITIVE-R35`
(`semantic-sha256:3f22913f6cf51e3d6615a1f6469744d142608c70fb6bd73422d725fedaf175fd`).

The assigned forest artifact and checker were independently hash-matched and
replayed:

```text
routes/det_forest/report.md
sha256:858ca18b12bda01334dad53f163e0d4fe1cfd61dc790aedff634582ad7b4e1b2

routes/det_forest/exact_forest_checker.py
sha256:5cbe9aabbcbe53447c20f7109f44f52d78a9095cf84f185cbb862c8f22aaa614

FOREST_IDENTITY_N_1_TO_4=PASS
SCALED_CHARGE_IDENTITY_N_1_TO_4=PASS
SHARED_CONTRAST_MISMATCH=PASS
```

The new exact conclusions are:

1. For arbitrary `mu>1`, both momentum equations at one strict physical
   positive--negative interface give an explicit Möbius amplitude map in the
   one shared contrast `r=sqrt(R)`.
2. For the middle positive cell of an `n=3` word, imposing the same `r` on
   both sides gives one exact quadratic compatibility invariant.  It is a
   necessary physical gluing equation before either endpoint or the norm
   equation is imposed.
3. The relative location of the physical `b=0` boundary and the amplitude
   crossing `a=1` is controlled by a new phase coefficient `Xi`.  If `Xi>=0`
   at an interface, that interface is a strict contraction `0<a<1`.
   Consequently every physical `n=3` word must have `Xi<0` at at least one
   of the two interfaces adjacent to its middle positive cell.  A
   reflection-fixed word must have `Xi<0` in its single parity-reduced
   interface.
4. The complete `P^(-1)f` block reconstruction turns the forest determinant
   into the exact four-margin compensation identity in Section 4.

The coefficient `Xi` is not a reformulation of `det(H)>0`: it contains no
`H`, `P`, `W`, forcing `f`, or endpoint data, and it is already necessary for
the existence of the three internal cells.  However, its sign is not fixed
by the accepted phase chambers for general `mu`.  Thus no determinant sign,
physical counterexample, or reflection theorem is claimed.

## 1. General-`mu` full two-momentum interface map

Let a positive internal cell of lower phase `theta` be followed by a negative
internal cell of lower phase `eta`.  The accepted sharp phase allocation is

```text
0<theta<pi/(mu+1)<eta<pi/mu,       mu>1.             (1.1)
```

Put

```text
c=cos(theta),       s=sin(theta),
C=cos(mu*theta),    S=sin(mu*theta),
d=cos(eta),         t=sin(eta),
D=cos(mu*eta),      T=sin(mu*eta),
r=sqrt(R)>1.                                           (1.2)
```

Let `a` be the forward event-amplitude ratio in the positive cell and `b`
the forward ratio in the following negative cell.  Normalize the common
interface amplitude to one.  The physical position signs are

```text
positive cell:  V_left= U_left/mu,   V_right=-U_right/mu,
negative cell:  V_left=-U_left/mu,   V_right= U_right/mu.
```

Continuity of the two independent momenta at the interface is exactly

```text
(c-1/a)/s = r*(b-d)/t,
-(1/a+C)/S = r*(b+D)/T.                              (1.3)
```

Solving (1.3), define

```text
Delta=t*S-s*T,
A0=t*S*c+s*T*C,             A1=s*S*(d+D),
B0=t*T*(c+C),               B1=t*S*D+s*T*d.          (1.4)
```

Then

```text
a=Delta/(A0+r*A1),
b=-(B0+r*B1)/(r*Delta).                              (1.5)
```

The exact checker substitutes (1.5) back into both equations of (1.3) and
gets identically zero residual.  No gamma-only switch equation is used.

Several signs in (1.4) follow from (1.1), without reflection:

```text
Delta>0,       A1<0,       B0>0,       B1<0.         (1.6)
```

For `Delta`, write `g(x)=sin(mu*x)/sin(x)`.  Since
`x*cot(x)` is strictly decreasing on `(0,pi)`, `g` is strictly decreasing on
`(0,pi/mu)`; hence `Delta=s*t*(g(theta)-g(eta))>0`.
Also

```text
d+D=2*cos((mu+1)eta/2)*cos((mu-1)eta/2)<0,
c+C=2*cos((mu+1)theta/2)*cos((mu-1)theta/2)>0.
```

Finally `D<-d`.  If `d<0`, both terms of `B1` are negative.  If `d>=0`,
`g(theta)>g(eta)` and `D<-d` give
`B1/(s*t)=g(theta)D+g(eta)d<0`.

On the strict physical branch the actual cell ratios obey `a>0>b`.
Equations (1.5)--(1.6) therefore imply

```text
A0+r*A1>0,
0<r<r_N:=B0/(-B1).                                  (1.7)
```

The same formulas apply to a negative--positive interface after time
reversal; the contrast remains the same `r`, while the positive-cell ratio
is inverted.

## 2. Shared-contrast middle-cell invariant

For an `n=3` word, let `theta_3` be the phase of its middle positive cell,
and let `eta_L,eta_R` be the two adjacent negative phases.  Use the data
`Delta_L,A0_L,A1_L` and `Delta_R,A0_R,A1_R` from (1.4), always with the same
`mu`, `theta_3`, and physical `r`.

If `z` is the actual middle-cell amplitude ratio, the right interface and
the time-reversed left interface give

```text
z   =a(theta_3,eta_R;r),
1/z =a(theta_3,eta_L;r).                             (2.1)
```

Thus full internal amplitude gluing is equivalent to

```text
C_mid(r):=
 A1_L*A1_R*r^2
 +(A0_L*A1_R+A1_L*A0_R)*r
 +(A0_L*A0_R-Delta_L*Delta_R)=0.                    (2.2)
```

This is the first exact invariant that the relaxed forest witness omits:
the witness assigns separate cell coefficients, whereas (2.2) forces both
interfaces to use one shared contrast and one actual middle amplitude.  It
is not the determinant target.  In particular, (2.2) is meaningful even
before the endpoint cells, common terminal, equal norm, event Jacobi
matrix, or forced charges have been constructed.

## 3. Exact contraction-boundary coefficient

The crossing `a=1` occurs at

```text
r_a=(A0-Delta)/(-A1),                                (3.1)
```

when this number is positive.  Compare it to the physical `b=0` boundary
`r_N` from (1.7).  Define the regular algebraic phase coefficient

```text
Xi(theta,eta;mu)
 =-d*T/(D*t) -(S/s)*(1-c)/(1+C).                    (3.2)
```

All denominators in (3.2) are nonzero in (1.1), including when
`eta=pi/2`.  Away from that harmless tangent pole it is equivalently

```text
Xi=-tan(mu*eta)/tan(eta)
   -tan(theta/2)*tan(mu*theta/2).                    (3.3)
```

Direct expansion gives the exact factorization

```text
A1*B0-B1*(A0-Delta)
 =s*t*Delta*(1+C)*(-D)*Xi.                          (3.4)
```

Every factor outside `Xi` in (3.4) is strictly positive.  Since

```text
r_a-r_N
 =[A1*B0-B1*(A0-Delta)]/[(-A1)(-B1)],               (3.5)
```

the sign of `Xi` is exactly the relative order of the amplitude crossing
and the physical negative-cell boundary.

**Contraction lemma.**  If a strict physical interface satisfies `Xi>=0`,
then `0<a<1`.

Indeed, `Xi>=0` gives `r_a>=r_N`.  Physicality gives the strict inequality
`r<r_N`; in particular `r_a>0`.  Hence `r<r_a`, so
`A0+r*A1>Delta`, and (1.5) gives `0<a<1`.

Applying the lemma to both sides of (2.1) proves the necessary condition

```text
min{Xi(theta_3,eta_L;mu),Xi(theta_3,eta_R;mu)}<0     (3.6)
```

for every strict physical `n=3` word.  Otherwise both factors in (2.1) lie
strictly below one, contradicting their product one.

In the reflection-fixed subcase `eta_L=eta_R`, the two coefficients agree,
so (3.6) reduces to the strict parity-sector condition

```text
Xi(theta_3,eta_L;mu)<0.                              (3.7)
```

This is an exact, nonvacuous necessary condition, not a proof of determinant
positivity on a symmetric root.  For general `mu`, the accepted phase
chambers alone do not currently orient `Xi`; that is the first remaining
physical coefficient after shared-contrast/two-momentum elimination.

## 4. Reconstruction of `P^(-1)f` and forest compensation

For `n=3`, write the positive-block inverses as

```text
P_j^(-1)=[ell_j s_j; s_j r_j],       j=1,2,3,
```

and let `v=(v_1,v_2)>0`.  From the exact physical identity

```text
P*gamma-C^T*v=f,
```

one obtains, block by block,

```text
P_1^(-1)f_1=(gamma_1+s_1v_1, gamma_2+r_1v_1),

P_2^(-1)f_2=(gamma_3-ell_2v_1+s_2v_2,
             gamma_4-s_2v_1+r_2v_2),

P_3^(-1)f_3=(gamma_5-ell_3v_2, gamma_6-s_3v_2).     (4.1)
```

Define the four adjacent positive-cell response margins

```text
E_1=gamma_2+r_1v_1,       F_2=ell_2v_1-gamma_3,
E_2=gamma_4+r_2v_2,       F_3=ell_3v_2-gamma_5.     (4.2)
```

There is also a useful energy form of the total interval charge.  From
`f=P*gamma-C^T*v` and `P^(-1)f=gamma-P^(-1)C^T*v`, symmetry gives

```text
Q_[1,2]=-v^T C P^(-1)f
       =f^T P^(-1)f-gamma^T f.                       (4.3)
```

Canonical time-translation forcing signs every summand of
`gamma^T f` positively, and `P^(-1)>0` signs `f^T P^(-1)f` positively.
Thus (4.3) is a difference of two positive quantities, not a positive-energy
identity.  The full two-momentum/shared-contrast equations above do not yet
compare those two quantities.

More sharply, (4.1) decomposes their difference into three block deficits:

```text
Q_[1,2]=delta_1+delta_2+delta_3,
delta_1=v_1 E_1,
delta_2=v_1 F_2+v_2 E_2-2s_2v_1v_2,
delta_3=v_2 F_3.                                    (4.4)
```

The first genuinely coupled coefficient is the central loaded
Dirichlet-to-Neumann/Robin matrix

```text
R_2^load=[ F_2/v_1       s_2   ],
         [   s_2       E_2/v_2 ],                   (4.5)

det(R_2^load)=E_2F_2/(v_1v_2)-s_2^2
             =-D_mid/(v_1v_2),
D_mid=s_2^2v_1v_2-E_2F_2.                           (4.6)
```

Therefore `D_mid<=0` is exactly nonnegativity of this local loaded Robin
determinant.  It is strictly localized and is not the full determinant
target.  The shared quadratic (2.2) fixes the middle amplitude and one
contrast, but its current elimination does not orient the two load ratios
`gamma_3/v_1` and `-gamma_4/v_2` in (4.5).  This is the first unresolved
block coefficient after the two positive energy terms in (4.3) are exposed.

Then the forest charges and conductance are exactly

```text
q_1=v_1(E_1+F_2-s_2v_2),
q_2=v_2(E_2+F_3-s_2v_1),
e=s_2v_1v_2>0.                                      (4.7)
```

Substitution into the assigned forest polynomial gives the cancellation

```text
q_1q_2+e(q_1+q_2)
 =v_1v_2{(E_1+F_2)(E_2+F_3)-s_2^2v_1v_2}
 =v_1^2v_2^2 det(H).                                (4.8)
```

Equation (4.8) retains both negative-edge jump weights and all three
positive blocks.  It shows precisely what remains after the internal
shared-contrast invariant (2.2): endpoint/common-terminal/norm information
must prove the strict four-margin compensation

```text
(E_1+F_2)(E_2+F_3)>s_2^2v_1v_2.                    (4.9)
```

Unlike `Xi`, (4.9) is equivalent to the determinant sign and is therefore
recorded as the still-open target, not as a new lemma.

Under reflection, `v_1=v_2=v`, `E_1=F_3`, and `F_2=E_2`.  The two parity
sectors factor (4.4) as

```text
v^2(E_1+F_2-s_2v)(E_1+F_2+s_2v).                   (4.10)
```

Neither factor in (4.10) is signed by (2.2)--(3.7).  Thus the symmetric determinant
subcase remains open; it has not been inflated into a theorem.

## 5. Boundary and adversarial audit

- **Arbitrary asymmetry:** equations (2.2), (3.6), and (4.4) retain
  independent left and right negative phases and jump weights.
- **Shared finite contrast:** one and the same `r=sqrt(R)>1` occurs in both
  factors of (2.1) and every coefficient of (2.2).  No separate-cell
  contrast is permitted.
- **`mu` near one / finite large `mu`:** (1.3)--(4.4) are exact for every
  finite `mu>1`.  No compactness or asymptotic passage is used.  The sign of
  `Xi` remains open uniformly in those regimes.
- **Endpoint cells and common terminal:** the internal compatibility (2.2)
  is necessary before endpoint gluing.  Endpoints and the equal-norm
  equation are not discarded when claiming a root; they are exactly the
  missing inputs needed for (4.5).
- **Central parity:** reflection gives the exact necessary condition (3.7)
  and determinant factorization (4.6), but no sign claim.
- **Determinant zero / q-Jacobi singularity:** no inverse of `H` and no
  division by its determinant occurs.  Equation (4.4) includes equality
  exactly, so singular roots are not excluded.
- **Relay closures:** the algebraic identities extend after clearing the
  displayed positive-cell denominators.  The strict sign conclusions use
  (1.1), transversality, and `a>0>b`; they are not promoted to grazing,
  coalesced, or zero-length closures.
- **Reduced nonphysical witness:** it was replayed only to verify its shared
  contrast failure.  It is not reused as a physical counterexample.
- **Falsification:** the frozen checker output contains exact symbolic
  identities only.  No finite or numerical scan is used as evidence for a
  universal sign.

## 6. Status and restart condition

```text
general-mu two-momentum interface map:                 PROVED
shared-r middle-cell quadratic compatibility:          PROVED
Xi boundary-order factorization:                       PROVED
Xi>=0 implies strict interface contraction:            PROVED
every physical n=3 word has at least one Xi<0:          PROVED
reflection-fixed n=3 word has Xi<0:                    PROVED
full P^(-1)f / four-margin determinant identity:        PROVED
total-charge positive-energy difference identity:       PROVED
central loaded-Robin determinant identity:              PROVED
universal sign of Xi on physical n=3 interfaces:        OPEN
central block sign D_mid<=0:                             OPEN
four-margin endpoint compensation (4.9):                OPEN
det(H)>0 for every physical n=3 minimum root:           OPEN
global minimum reflection symmetry:                     OPEN
physical det(H)<=0 root:                                NONE
```

The precise restart is mechanism-distinct from restating the determinant:

1. orient the localized loaded determinant (4.6), equivalently `D_mid`, by
   substituting the shared-contrast interface map into the two adjacent
   negative-cell load ratios; this can succeed without signing all of `H`;
2. orient `Xi` using a genuinely global physical predicate, or classify the
   `Xi<0` phase region admitted by the shared quadratic (2.2); then
3. use the two endpoint momentum equations and equal-norm generator to sign
   the four-margin surplus in (4.9).

```text
novelty_status: unknown; no priority claim
formalization_status: not_requested
confidence_semantic_fidelity: high
confidence_exact_algebra: high
confidence_sign_criterion: high
confidence_target_completeness: low; determinant and reflection remain open
confidence_reproducibility: high
```
