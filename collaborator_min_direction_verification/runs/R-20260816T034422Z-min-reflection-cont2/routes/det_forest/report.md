RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-A: signed rooted-forest expansion for the minimum determinant

## 0. Calibrated outcome

This route is bound to `CTX-DEFAULT` at

```text
blueprint_sha256:
  sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
target:
  OBL-NGE2-MPO3A-MIN-DET-H-POSITIVE-R35
  semantic-sha256:3f22913f6cf51e3d6615a1f6469744d142608c70fb6bd73422d725fedaf175fd
```

It proves two exact all-`n` determinant expansions and a physical scaling
identity, but it does not orient the determinant.

1. `H` is exactly a path Laplacian plus signed vertex charges.  Its
   determinant is a rooted-forest/interval-partition polynomial whose edge
   weights are strictly positive and whose only uncontrolled factors are
   sums of charges over intervals.
2. After scaling by the canonical positive negative-cell jump vector, those
   charges are exact contractions of the time-translation forcing.
3. At the first coupled dimension, `n=3`, the connected-tree coefficient is
   the total charge `q_1+q_2`.  An exact rational reduced witness has all
   positive-block algebra, alternating event signs, and the exact `mu=2`
   phase-fraction forcing, yet `q_1=q_2=-1` and `det(H)=-2`.  The witness is
   rigorously nonphysical because two positive cells demand different values
   of the one shared contrast `(R-1)^2`.

Consequently coefficientwise positivity, phase separation, and the scalar
time-translation forcing do not prove the target.  The first missing
physical step is a **shared-contrast/common-terminal interval-charge
compensation inequality**, stated exactly in Section 7.  No physical
counterexample and no reflection theorem are claimed.

## 1. Trusted input and complete matrix definitions

Fix finite `R>1`, an integer `n>=2`, and an arbitrary possibly asymmetric
premise-complete event-transverse common-terminal minimum-law root.  Put

```text
N=n-1.
```

The trusted determinant-parity claim supplies

```text
H=C P^(-1) C^T-W,                                  (1.1)
```

where `W=diag(W_1,...,W_N)>0`, and `P` is the direct sum of `n`
positive two-by-two odd-edge blocks.  The definitions and sign split are
also reconstructed in the allowed package

```text
runs/R-20260815T181317Z-min-reflection/
  routes/event_inertia/determinant_parity_proof.md
sha256:2e4619ac52392aadf00369e8c9afdea3ddf76ec5e3d00452dc44a258ee8de40b.
```

For block `j`, write

```text
P_j^(-1)=[ ell_j  s_j ],
          [  s_j   r_j ],                           (1.2)
```

with `ell_j>s_j>0` and `r_j>s_j>0`.  More explicitly, if

```text
c_j=1/K_(2j-1)>0,
Delta_j=a_(2j-1)a_(2j)+c_j(a_(2j-1)+a_(2j)),
```

then

```text
ell_j=(a_(2j)+c_j)/Delta_j,
r_j  =(a_(2j-1)+c_j)/Delta_j,
s_j  =c_j/Delta_j,                                  (1.3)
```

so

```text
ell_j-s_j=a_(2j)/Delta_j>0,
r_j-s_j=a_(2j-1)/Delta_j>0.                         (1.4)
```

Taking row `i` of `C` to be `e_(2i+1)-e_(2i)`, direct multiplication gives

```text
H_(i,i)=d_i=r_i+ell_(i+1)-W_i,       1<=i<=N,
H_(i,i+1)=H_(i+1,i)=-s_(i+1),        1<=i<N.        (1.5)
```

No reflection, determinant sign, complementary inertia, or uniqueness is
used in (1.1)--(1.5).

## 2. Exact path-Laplacian decomposition

For the dual edge joining vertices `i` and `i+1`, put

```text
tau_i=s_(i+1)>0,                         1<=i<N.     (2.1)
```

Define signed ground charges by subtracting the incident path
conductances from the diagonal:

```text
z_i=d_i-1_(i>1)s_i-1_(i<N)s_(i+1).                  (2.2)
```

Thus, when `N>=2`,

```text
z_1=r_1+(ell_2-s_2)-W_1,
z_i=(r_i-s_i)+(ell_(i+1)-s_(i+1))-W_i,  1<i<N,
z_N=(r_N-s_N)+ell_(N+1)-W_N.                        (2.3)
```

For `N=1`, there is no path edge and

```text
z_1=d_1=r_1+ell_2-W_1.                              (2.4)
```

Let `L_tau` be the weighted path Laplacian on `{1,...,N}` with edge
conductances `tau_i`.  Equations (1.5) and (2.2) give the exact identity

```text
H=L_tau+diag(z_1,...,z_N).                           (2.5)
```

The positive terms in (2.3) come from the two adjacent odd-edge blocks;
the negative term is the intervening even-edge magnitude.  The trusted
phase theorem fixes which edges are positive and negative, but it supplies
no inequality between these three magnitudes.

## 3. Signed rooted-forest theorem

For a set `E` of retained path edges, let `Comp(E)` be the interval
components of the forest `({1,...,N},E)`, and put

```text
Z_I=sum_(i in I) z_i.                                (3.1)
```

Then, for every real choice of the charges and every positive choice of the
conductances,

```text
det(H)
 =sum_(E subset {1,...,N-1})
    [ product_(i in E) tau_i ]
    [ product_(I in Comp(E)) Z_I ].                  (3.2)
```

Equivalently, sum over all partitions `pi` of `{1,...,N}` into consecutive
intervals:

```text
det(H)
 =sum_pi
    [ product_(I in pi) Z_I ]
    [ product_(i: i and i+1 lie in the same block of pi) tau_i ]. (3.3)
```

### Proof

Adjoin a root vertex `0`.  Connect `i` to `0` with formal weight `z_i`, and
retain the path edge `i--(i+1)` with weight `tau_i`.  The reduced weighted
Laplacian obtained by deleting the row and column of `0` is exactly (2.5).
The matrix-tree determinant polynomial is the sum of the weights of all
spanning trees of the augmented graph.  After removing `0`, such a tree is
a path forest, and each of its components has exactly one edge to `0`.
For a fixed forest, summing the possible root edge in component `I` gives
`sum_(i in I)z_i=Z_I`.  Multiplying over components and then summing the
path forests proves (3.2).  Every path-forest component is an interval, so
(3.3) is the same formula.

The usual matrix-tree statement is often presented for positive weights,
but its proof is a polynomial identity with integer coefficients.  Hence it
holds for the signed formal weights `z_i` without a positivity assumption.
This also gives a direct algebraic proof on every charge chamber and its
closure.

For orientation, the first cases are

```text
N=1: det(H)=z_1,

N=2: det(H)=z_1 z_2+tau_1(z_1+z_2),                 (3.4)

N=3: det(H)=z_1z_2z_3
       +tau_1(z_1+z_2)z_3
       +tau_2 z_1(z_2+z_3)
       +tau_1tau_2(z_1+z_2+z_3).                   (3.5)
```

Thus the forest mechanism produces a positive sum only if new physical
information signs or quantitatively compensates the interval sums `Z_I`.
Neither `P>0` nor `W>0` does so.

## 4. Independent Cauchy--Binet coefficient audit

Put

```text
G=C P^(-1)C^T>0.                                    (4.1)
```

Multilinearity in the diagonal entries of `W` gives

```text
det(G-W)
 =sum_(S subset {1,...,N}) (-1)^|S|
    [product_(i in S)W_i] det(G_(S^c,S^c)),         (4.2)
```

where the empty principal minor equals one.  Since `G` is positive
definite, every principal minor in (4.2) is strictly positive.  Therefore
the coefficients in the raw `W` variables have unavoidable alternating
sign.  A Cauchy--Binet or matrix-tree proof cannot become coefficientwise
positive without substituting additional physical relations among `W` and
the odd blocks.  This is an exact obstruction, not a failed numerical
search.

## 5. Canonical positive-jump scaling and forced charges

Let `gamma_i` be the time-translation event values.  Transversality and the
alternating crossing orientation give

```text
gamma_(2i)<0<gamma_(2i+1).
```

Define the canonical positive negative-cell jumps

```text
v_i=(gamma_(2i+1)-gamma_(2i))/W_i>0,       1<=i<=N. (5.1)
```

Let `f=M gamma` (this is a definition, so no unaccepted forcing theorem is
needed here).  Since

```text
M=P-C^T W^(-1)C,
v=W^(-1)C gamma,
```

we have

```text
P gamma-C^T v=f.
```

Multiplying by `C P^(-1)` and using `C gamma=Wv` yields

```text
H v=-C P^(-1)f.                                     (5.2)
```

Put

```text
q_i=v_i(Hv)_i=-v_i(CP^(-1)f)_i,                     (5.3)
e_i=s_(i+1)v_i v_(i+1)>0.                           (5.4)
```

With `V=diag(v_1,...,v_N)`, a componentwise calculation gives

```text
V H V=L_e+diag(q_1,...,q_N),                        (5.5)
det(VHV)=(product_i v_i^2)det(H).                    (5.6)
```

Applying (3.2) to (5.5) proves the physical-charge forest identity

```text
(product_i v_i^2)det(H)
 =sum_E [product_(i in E)e_i]
        [product_(I in Comp(E)) Q_I],
Q_I=sum_(i in I)q_i.                                (5.7)
```

This formula uses the full physical matrix and the positive event-jump
vector but does not assume `Hv>0`.  It is strictly calibrated to the final
determinant: mixed signs of individual `q_i` are allowed.

### 5.1 Exact block-response form and the failed telescoping point

Split `f` into the same positive blocks as `P` and define

```text
(L_j,R_j)^T=P_j^(-1)(f_(2j-1),f_(2j))^T.            (5.8)
```

Because row `i` of `C` is `e_(2i+1)-e_(2i)`, (5.3) becomes

```text
q_i=v_i(R_i-L_(i+1)).                               (5.9)
```

Hence every interval charge has the exact boundary/mismatch form

```text
Q_[a,b]
 =v_a R_a-v_b L_(b+1)
  +sum_(j=a+1)^b [v_j R_j-v_(j-1)L_j].             (5.10)
```

This is where an attempted time-translation telescoping stops.  The
interior block `j` is hit with two generally different jump weights
`v_(j-1),v_j`, and its two responses `L_j,R_j` are different positive-block
linear combinations of the two entries of `f`.  Alternating signs of the
physical forcing do not sign either response because `P_j^(-1)` has all
positive entries.  A shared value of `R` constrains the block coefficients,
but does not algebraically set `v_(j-1)=v_j` or `L_j=R_j`.  Terminal closure
fixes only the two outer trajectories; it does not remove the interior
sum in (5.10).  The exact witness in Section 6 realizes this mismatch at
the reduced level, while its contrast failure shows precisely which full
physical relation is still absent.

### 5.2 Reflection covariance excludes identification with the C2-D drift

The sibling C2-D route proposes the exact candidate identities

```text
D=(R-1)(q_left^2-1) sum_a Phi_mu(theta_(2a-1),z_(2a-1)),
Phi_mu(theta,1/z)=-Phi_mu(theta,z),
D/I = common spectral translation speed.            (5.11)
```

They were independently replayed here from the checkpoint artifacts

```text
runs/R-20260816T034422Z-min-reflection-cont2/
  routes/defect_amplitude/report.md
checkpoint sha256:beddd4a275a5ee08881ba5d6cd12cb04c0daac54aa8b536d5741334bccbc6b47

routes/defect_amplitude/exact_checker.py
checkpoint sha256:5cffe28a45cd0d0e6738e1b514f86701616e543e0b6dd2a86f22c2b80db46d16.
```

These sibling artifacts are candidate run state, not canonical premises;
the covariance comparison below is reproduced directly.

Let `p` be the nonzero terminal low-frequency slope and let `R_m,R_N` be
the event and dual-vertex reversal matrices.  Normalized reflection gives

```text
a_i^#=a_(2n+1-i)/p^2,
K_i^#=p^2 K_(2n-i),
gamma^#=-R_m gamma.                                 (5.12)
```

Consequently

```text
P^#=p^(-2)R_m P R_m,
W^#=p^2 R_N W R_N,
C^#=-R_N C R_m,
H^#=p^2 R_N H R_N.                                 (5.13)
```

Equations (5.1), (5.3), and (5.4) then give

```text
v^#=p^(-2)R_N v,
q^#=p^(-2)R_N q,
e^#=p^(-2)R_(N-1)e.                                (5.14)
```

In particular, for the reflected interval `I^#`,

```text
Q_(I^#)^#=p^(-2)Q_I.                               (5.15)
```

There is no sign reversal.  In contrast, the endpoint defect and the C2-D
cell drifts obey

```text
D^#=-D/p^2,
Phi(theta,1/z)=-Phi(theta,z).                       (5.16)
```

Also `I^#=I/p^2`, so the translation speed satisfies

```text
(D/I)^#=-D/I.                                      (5.17)
```

Thus neither an interval charge nor the total charge can equal a positive,
reflection-even multiple of the positive-cell drift sum, `D`, or the
first-order translation speed.  Their reflection parities are opposite.
Shared contrast and unoriented terminal closure are reflection-even and
cannot repair this mismatch by themselves.  An additional reflection-odd
oriented factor would be required.

This is the exact cross-route mapping failure point.  Their parity does not
rule out a **translation curvature/second-variation** quantity, but no such
identity is proved here and the current C2-D first-order identity does not
provide it.  Accordingly the two routes meet only at the new restart
question:

```text
derive a second-variation identity whose block boundary terms are exactly
the mismatches in (5.10), or prove their terminal forest compensation
directly from the full momentum and norm equations.                    (5.18)
```

## 6. First uncontrolled coefficient and exact reduced obstruction

The first coupled case is `n=3`, so `N=2`.  Formula (5.7) is exactly

```text
v_1^2 v_2^2 det(H)=q_1q_2+e_1(q_1+q_2).             (6.1)
```

The coefficient of the connected spanning tree is the total forced charge

```text
Q_[1,2]=q_1+q_2=-v^T C P^(-1)f.                    (6.2)
```

It is the first coefficient not signed by the accepted phase separation or
the positive-block algebra.

Here is an exact reduced witness.  Take

```text
P_1^(-1)=[1   1/2],
          [1/2 5/4],

P_2^(-1)=[103/52 3/2],
          [3/2 103/52],

P_3^(-1)=[5/4 1/2],
          [1/2 1],

W_1=W_2=71/26.                                      (6.3)
```

Inverting the three blocks gives exactly

```text
(a_1,...,a_6)=(3/4,1/2,52/181,52/181,1/2,3/4)>0,
(K_1,K_3,K_5)=(2,4525/4056,2)>0,                    (6.4)
```

so every block has the exact accepted odd-edge algebraic form.  With the
negative edges `K_2=K_4=-71/26`,

```text
H=[ 1/2 -3/2],       det(H)=-2.
  [-3/2  1/2]                                       (6.5)
```

Choose

```text
gamma=(28/5,-1,45/26,-45/26,1,-28/5)^T.            (6.6)
```

Then (5.1) gives `v=(1,1)^T`, and

```text
q=diag(v)Hv=(-1,-1)^T,
e_1=3/2,
q_1q_2+e_1(q_1+q_2)=1-3=-2.                        (6.7)
```

The witness also retains the exact scalar time-translation forcing.  With

```text
beta^2=17/2,
q_left^2=r_right^2=19/2,
chi=(2,24/5,11/5,24/5,2),                          (6.8)
```

direct rational multiplication gives

```text
M gamma=(15/2,-14/5,13/5,-13/5,14/5,-15/2)^T,
```

which equals the endpoint/difference word determined by (6.8).  For
`mu=2`, `chi_i/beta^2=1/(1+4cos(theta_i))`; the exact cosines

```text
(13/16,37/192,63/88,37/192,13/16)                  (6.9)
```

put every odd phase strictly below `pi/3` and every even phase strictly
between `pi/3` and `pi/2`.  Thus positive-block shape, alternating event
signs, the exact phase chambers, and the exact phase-fraction forcing do not
fix either `Q_[1,2]` or `det(H)`.

This is **not** a physical relay counterexample.  If one shared contrast
realized the displayed first and middle positive cells, the canonical event
definitions on a material-one positive cell would give

```text
a_i |gamma_i|=(R-1)u_i^2,
K_i=Q(theta_i)/(u_i u_(i+1)),
Q(theta)=sin(theta)+2sin(2theta).
```

Eliminating the endpoint amplitudes therefore gives the exact cell identity

```text
(R-1)^2
 =K_i^2 a_i a_(i+1)|gamma_i gamma_(i+1)|/Q(theta_i)^2.
```

For the first and middle positive cells this identity would demand,
respectively,

```text
(R-1)^2=57344/41905,
(R-1)^2=52707600/1246373479,                         (6.10)
```

which are unequal.  The witness therefore fails oscillator realization
before terminal closure.  Its only logical use is to refute a proof from
the reduced premises just listed.

## 7. Exact restart condition

The new route-level restart object is not `H>0`.  It is the terminal signed
forest polynomial in physical forced charges.  Define

```text
F_0=1,
F_k=sum_(j=1)^k F_(j-1)
      [product_(r=j)^(k-1)e_r] Q_[j,k],
Q_[j,k]=sum_(i=j)^k q_i.                            (7.1)
```

Decomposing an interval partition by its last block proves exactly

```text
F_N=(product_i v_i^2)det(H).                         (7.2)
```

Therefore a mechanism-distinct restart must derive from the **shared
contrast, both momentum matches, and common-terminal equations** a
quantitative compensation inequality making `F_N>0`.  At `n=3`, the first
required inequality is precisely

```text
q_1q_2+e_1(q_1+q_2)>0.                              (7.3)
```

For larger `n`, the required data are the interval contractions
`Q_[j,k]`, not merely the signs of single diagonal entries or the stronger
positivity of all leading pivots.  A useful next attempt would derive each
`Q_[j,k]` directly from a truncated physical relay with its two inherited
boundary momenta, and then use the actual endpoint equations only in the
last-block recursion (7.1).  The reduced witness proves that omitting the
shared-contrast/momentum constraints cannot succeed.

This restart is genuinely weaker in target than complementary inertia:
only `F_N`, not all prefix `F_k`, must be positive.  Requiring every prefix
positive would silently return to `H>0` and is not proposed.

## 8. Boundary and adversarial audit

- **`n=2`: PASS/calibrated.**  `N=1`, so the forest formula is the scalar
  identity `det(H)=z_1`.  It neither strengthens nor weakens the known
  scalar problem.
- **`n>=3`: PASS.**  Equations (3.2), (4.2), and (5.7) hold for every
  dimension and retain arbitrary asymmetry.
- **Determinant zero: PASS as an identity, OPEN as an exclusion.**  No
  inverse of `H`, pivot, or determinant is taken.  At a q-Jacobi singular
  root, (3.2) and (5.7) state exactly that the signed forest terms cancel to
  zero.  The route neither divides by that cancellation nor excludes it.
- **All relay chambers: PASS for the identity, OPEN for sign.**  The proof
  uses only the accepted odd/even split and positive block coefficients, so
  it is chamber-uniform.  It supplies no chamberwise sign inequality.
- **Terminal soft-pair limit: algebraic closure only.**  After clearing the
  positive block denominators, (3.2) is polynomial and extends to any finite
  fixed-dimension coefficient limit.  The scaled formula (5.7), however,
  contains the positive factor `product_i v_i^2`; if the newborn terminal
  jump tends to zero or infinity, both the charges `q_i` and conductances
  `e_i` acquire compensating singular scales.  No sign can be passed to the
  lower-dimensional word without exact rates for that last `v`, `q`, and
  `e`.  A word-dimension change, vanishing event margin, or unbounded
  coefficient at a terminal birth therefore still needs a separate physical
  soft-pair asymptotic; no positivity is asserted there.
- **Coefficientwise positivity attack: REFUTED.**  Formula (4.2) has strict
  alternating coefficient signs.
- **Phase-forcing-only attack: REFUTED EXACTLY.**  Equations (6.3)--(6.10)
  give a rational obstruction and identify its precise physical failure.
- **Physical counterexample: NONE.**  The reduced witness fails shared
  contrast and terminal closure and is not used against the target.

## 9. Status

```text
exact all-n signed forest expansion:                 PROVED
exact all-n positive-jump/forced-charge scaling:     PROVED
raw W coefficient alternation:                       PROVED
phase/block/forcing-only implication det(H)>0:       REFUTED EXACTLY
fully physical det(H)<=0 root:                       NONE
det(H)>0 for every physical minimum root:            OPEN
global minimum reflection symmetry:                  OPEN
first uncontrolled object:
  interval forced-charge sums Q_[j,k], beginning with
  Q_[1,2]=q_1+q_2 at n=3
restart evidence:
  derive shared-contrast, two-momentum, terminal compensation in (7.1)
unresolved_obligations_for_the_exact_expansion:       []
unresolved_obligations_for_the_research_target:
  [OBL-NGE2-MPO3A-MIN-DET-H-POSITIVE-R35]
```

The universal determinant and reflection targets remain open.

```text
novelty_status: unknown; no literature-priority claim is made
confidence_exact_algebra_and_combinatorics: high
confidence_physical_target_completeness: low; the sign target is open
confidence_reproducibility: high
```
