# Independent audit of the full-interval relay reduction

## Verdict

```text
Forward and reverse scaling/normalization: PASS
Relay energy and q>1: PASS
Sturm indexing and exact 2n simple-event count: PASS; no circularity found
Three-scalar bijection: QUALIFIED by an omitted trajectory-uniqueness convention/proof
Two-scalar zero-time reduction: QUALIFIED by an underspecified relay chamber
Reflection implication: QUALIFIED by omitted independent mode reorientation
Frozen multiphase O3a target: open; neither proved nor refuted
```

The three qualifications are repairable definition/presentation gaps.  They
do not invalidate the central exact reduction once “relay triple” is bound to
a finite-switch relay trajectory and the chamber and reflection conventions
are made explicit.

Reviewed artifact:

```text
derivation.md
  sha256:867f6e57b3d124b88bfb1bc373fbbebb87ee392d7e742a43e6bcb432bfa163f6
```

Snapshot named by its manifest:

```text
Blueprint sha256:2b231a1806abad99631c2fec1075e44c48b43744d256c788f5de3f55415911e6
inventory sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

This audit is independent of the derivation author, uses no numerical
evidence, and does not edit or integrate the Blueprint.

## 1. Definition audit

### 1.1 Objects and a.e. relay law: PASS with one clarification

For fixed `R>1`, sign `e`, and parameters `mu>1`, `q>0`, a relay trajectory
is a `C1` state `(U,V)` with piecewise-`C2` dynamics and an a.e.-merged
finite-step coefficient `rho in {1,R}` satisfying the sign law for

```text
S=U^2-mu^2V^2.
```

Continuity of `S` implies that every effective coefficient jump lies in
`{S=0}`: a jump at a point with nonzero `S` would contradict the fixed
material assignment on a whole neighboring interval.  A zero without sign
change cannot create an effective jump because the material prescribed on
its two sides is the same.  Point values of `rho` at isolated zeros are a.e.
irrelevant.

A positive-length interval with `S=0` is impossible.  On a subinterval where
`V=+/-U/mu`, the two oscillator equations imply
`(mu^2-1)rho U=0`; positivity of `rho` forces `U=V=0`, contradicting the
nonzero initial derivative by uniqueness.  Thus the zero set cannot hide an
arbitrary material interval.

The phrase “relay triple `(mu,q,L)`” is nevertheless ambiguous if it denotes
only three numbers: a discontinuous state-dependent relay need not be
globally single-valued through an unspecified grazing event.  The theorem's
definition initially supplies `(U,V,rho)` as well as the three scalars, so
the mathematically safe object is the equivalence class of a finite-switch
relay trajectory labelled by `(mu,q,L)`.  Section 4 later calls the trajectory
“determined by `(mu,q)`” without proving that convention.  Section 7 gives
the minimal repair.

### 1.2 Prüfer lifts and zero indices: PASS

For `theta_U=atan2(U,U_t)` with continuous lift,

```text
theta_U'=(U_t^2+rho U^2)/(U^2+U_t^2)>0;
```

the analogous expression for `V` contains `mu^2rho` and is also positive.
Hence `Theta_U(L)=n pi` means `U(L)=0` with exactly `n-1` interior zeros,
and `Theta_V(L)=(n+1)pi` means `V(L)=0` with exactly `n` interior zeros.
The endpoint itself is not counted as a relay event.

## 2. Logic audit

### 2.1 Forward scaling and normalization: PASS

Set `L=sqrt(a)`, `t=Lx`, `A=u'(0)>0`, and

```text
U=Lu/A,       V=Lv/A,
mu=sqrt(b/a), q=v'(0)/u'(0).
```

Then `U_t(0)=1`, `V_t(0)=q`, and direct differentiation gives

```text
U_tt=-rho U,        V_tt=-mu^2rho V.
```

Moreover

```text
a u^2-bv^2=A^2(U^2-mu^2V^2),
I_U(L)=L^3/A^2 integral_0^1 rho u^2 dx,
I_V(L)=L^3/A^2 integral_0^1 rho v^2 dx.
```

Thus the relay law and equality `I_U=I_V` follow with all factors of `L`
and `A` correct.  Independent Sturm indexing supplies the two terminal
phases; the accepted structural theorem is used only to describe the forward
event set, not to establish the reverse implication.

### 2.2 Relay energy and q>1: PASS

On each material cell,

```text
E=U_t^2+rho U^2-(V_t^2+mu^2rho V^2)
```

is constant.  Across an effective interface its jump is
`Delta rho*S=0`, so `E` is global and `E(0)=1-q^2`.  The phase equations give
`U(L)=V(L)=0`.  Integration by parts gives

```text
integral U_t^2=I_U,
integral V_t^2=mu^2I_V.
```

If `I_U=I_V=I`, integration of the constant energy over `[0,L]` yields

```text
L(q^2-1)=2(mu^2-1)I>0.
```

Here `I>0` because `rho>0` and the solution `U` is nontrivial.  Consequently
`q>1`; no choice between the positive and negative square roots remains
because the relay definition assumed `q>0`.

At `L`, the same energy gives

```text
V_t(L)^2-U_t(L)^2=q^2-1>0.
```

The derivation's endpoint relation is therefore correctly normalized.

### 2.3 Reverse physical reconstruction: PASS

With

```text
a=L^2, b=mu^2L^2, A^2=L^3/I,
u(x)=A U(Lx)/L, v(x)=A V(Lx)/L,
```

one obtains `-u''=a rho_xu`, `-v''=b rho_xv` and

```text
integral_0^1 rho_xu^2=A^2I/L^3=1,
integral_0^1 rho_xv^2=A^2I/L^3=1.
```

The phase counts from Section 1.2 and regular Sturm oscillation identify
`a=lambda_n(rho_x)` and `b=lambda_{n+1}(rho_x)`.  Thus they are consecutive
indexed eigenvalues rather than merely two characteristic roots.  Reading
the switching-function scale identity backwards supplies precisely the max
or min saturation law.

### 2.4 Wronskian and exact event count: PASS; noncircular

After the Sturm indices have been established, the modes are consecutive.
Strict Sturm interlacing is therefore available independently of any relay
event count.  For

```text
W=V_tU-VU_t,
W'=-(mu^2-1)rho UV,
```

the alternating signs at consecutive zeros and monotonicity between them
give `W<0` on `(0,L)`.  Hence `Q=V/U` decreases strictly on each nodal
interval of `U`.

The left ratio is `q>1>1/mu`.  Nodal parity makes the terminal derivative
ratio negative, and the endpoint energy makes its magnitude greater than
one.  Therefore on the first, every middle, and the last nodal interval,
`Q` crosses both `+1/mu` and `-1/mu` exactly once.  Since `U` has `n` nodal
intervals, `S=U^2(1-mu^2Q^2)` has exactly `2n` interior zeros.  At a crossing,

```text
S'=-2mu^2U^2 Q Q' !=0.
```

Every zero changes sign, so the relay law changes material there; conversely
every effective material jump already lies in `{S=0}`.  Thus these are
exactly the `2n` effective switches.  This reasoning derives the event count
from phase indices, energy, and Sturm theory and does not assume the target's
event count in reverse.  Grazing, inactive extra zeros, and zero intervals
are all excluded a posteriori.

### 2.5 Inverse maps and trajectory uniqueness: QUALIFIED but repairable

The algebraic transformations in the forward and reverse constructions are
literal inverses once a relay trajectory is included in the relay-side
object.  To claim a bijection with the three naked numbers `(mu,q,L)`, one
must additionally show that no two premise-complete relay trajectories share
those numbers.

That missing sentence has a short proof.  For every solution of (3.1), the
energy argument gives `q>1`; hence

```text
S(t)=(1-mu^2q^2)t^2+O(t^4)<0
```

for small positive `t`, so the initial material is forced.  Between relay
events the constant-coefficient IVP is unique.  Section 2.4 proves every
event is a simple sign-changing zero, which forces the next material.  An
induction over the finite `2n` events makes the whole trajectory unique for
fixed `(mu,q,L,R,e)`.  Adding this proof removes the bijection ambiguity
without adding a new mathematical premise.

## 3. Two-scalar zero-time reduction

### 3.1 Equations at a premise-complete branch: PASS

For a selected finite-switch relay trajectory branch, if the indexed simple
zero times exist, `A_n=0` says their common value is `L`.  Then `B_n=0` is
exactly `I_U(L)=I_V(L)`.  The three-scalar theorem yields `q>1`, the indexed
consecutive physical modes, `2n` simple relay events, and the full saturation
law.  Conversely every self-consistent point gives such a zero.  No switch
coordinates or spectral scale remain: `L` is recovered as the common indexed
zero time, while the physical eigenvalue scale is `a=L^2`.

### 3.2 Chamber quantifiers: QUALIFIED

The phrase “finite-switch chamber where these zeros exist, are simple, and
the trajectory depends continuously” does not explicitly say whether
“these zeros” means only the terminal `U,V` zeros or also every switching
zero of `S`.  The latter is essential for `(A_n,B_n)` to be a single-valued
continuous function of `(mu,q)` on a chamber.  A relay grazing can change
the material word even while the indexed mode zeros stay simple.

The exact safe quantifier is:

```text
For each selected relay chamber on which q>0, the finite effective material
word up to max(T_U^(n),T_V^(n+1)) is constant, every encountered S-event is
transverse, no zero-time endpoint coincides with an unresolved grazing, and
the chosen relay IVP branch and indexed simple zero times depend continuously
on (mu,q), define A_n and B_n as above.  The union is taken over all such
premise-complete chambers.  At any common zero, Theorem 3.1 proves q>1 and
all 2n events transverse, so the root lies on a deterministic branch.
```

This chamberwise formulation does not assert a globally smooth relay map
across grazing boundaries.  A uniqueness proof must range over every such
chamber and identify duplicate coordinate descriptions if chamber closures
overlap.  Actual premise-complete roots have only simple events and therefore
are not grazing-boundary artifacts.

Calling the result “two equations in `(mu,q)`” is correct with this union-of-
branches convention; calling it one globally defined two-variable map before
the chamber convention is fixed would be too strong.

## 4. Reflection audit: QUALIFIED but repairable

Let a valid relay trajectory have

```text
p=U_t(L), r=V_t(L).
```

Nodal parity makes `p` and `r` have opposite signs.  A single common signed
rescaling that makes the reversed `U_t(0)=1` would consequently make the
reversed `V_t(0)` negative, contradicting the convention `q>0`.  The source
sentence therefore omits an independent, harmless sign reorientation of the
second eigenmode.

The exact reflected trajectory is

```text
U#(s)=[-sign(p)] U(L-s)/|p|,
V#(s)=[-sign(r)] V(L-s)/|p|,
rho#(s)=rho(L-s),
q#=|r|/|p|>1.                                        (4.1)
```

Independent sign flips of `U` and `V` preserve both oscillator equations,
`S`, the relay law, and the norm integrals.  Equation (4.1) gives
`U#_s(0)=1`, `V#_s(0)=q#>0`, the same `(mu,L)`, equal rescaled integrals,
and the required terminal phases.  Thus reflection maps a valid relay root
to another valid root, possibly in another chamber.

If the two-scalar system has exactly one premise-complete root across all
chambers for fixed `(n,R,e)`, then `(mu,q#)=(mu,q)`.  With the trajectory-
uniqueness clarification in Section 2.5, the relay coefficient equals its
reflection a.e.  More generally, bijection plus at-most-one relay root gives
the desired uniqueness directly, and reflection gives symmetry.  The source
conclusion is sound after adding the independent sign convention.

## 5. Boundary audit

- **`n=2`: PASS.** `U` has two nodal intervals and the quotient proof gives
  exactly four simple events; no middle-interval assumption is needed.
- **`R->1+`: PASS within scope.** Every finite `R>1` has distinct relay
  materials.  At `R=1` the word loses its effective-switch meaning and is
  correctly excluded.
- **Large finite `R`: PASS.** Positivity and finiteness are sufficient; no
  uniform-in-`R` margin or `R=infinity` conclusion is used.
- **Endpoints: PASS.** The common terminal zero is a Dirichlet endpoint, not
  an interior relay event.  The endpoint-cell sign follows from the quotient
  ranges.
- **Grazing and inactive zeros: PASS at actual roots.** Section 2.4 proves all
  `S` zeros simple and active.  Away from roots, chamber boundaries must be
  handled as in Section 3.2.
- **Collapsed/redundant cells: PASS after a.e. merging.** “Finite switch” must
  mean effective changes of material after adjacent equal cells are merged.
- **A.e. zero-set allocation: PASS.** Changing `rho` at the finite simple
  zeros changes neither dynamics nor the reconstructed weight class.
- **Signs/orientations: QUALIFIED only in the reflection sentence.** The
  forward/reverse constructions orient both modes positively; reflection
  requires the separate sign choices in (4.1).

## 6. Adversarial audit

1. **Scaling attack:** independently differentiating `u=A U(Lx)/L` recovers
   eigenvalue `L^2`, and the norm is `A^2I/L^3`; no missing `L` remains.
2. **Energy attack:** integration of a constant over length `L` is retained;
   the proof correctly includes the factor `L` in (3.8).
3. **Index attack:** endpoint phases are used before the quotient count and
   uniquely identify consecutive modes by their interior zeros.  The proof
   does not infer indices from relay events.
4. **Circular event-count attack:** q-dominance comes from energy and norm
   equality; Wronskian negativity comes from already indexed consecutive
   modes; these independently yield exactly `2n` events.
5. **Hidden zero attack:** a zero interval is impossible, and every actual
   zero is simple.  Extra relay switches cannot occur off `{S=0}` under the
   a.e. law.
6. **Hybrid-flow attack:** naked `(mu,q)` coordinates are not automatically a
   global flow through grazing.  This is the real chamber/definition gap and
   is captured by the minimal repair below.
7. **Reflection attack:** common magnitude rescaling is valid, but each mode
   needs its own sign orientation.  Omitting it makes the displayed `q>0`
   convention fail after reversal.
8. **Target-overreach attack:** no injectivity or root-count theorem for
   `(A_n,B_n)` is proved.  A lower-dimensional exact equivalence is not a
   proof of uniqueness, and the artifact correctly keeps the target open.

## 7. Minimal required repairs

Add the following three clarifications; no central formula needs changing.

### Repair 1: relay-side object and scalar uniqueness

After the relay definition, state:

```text
A relay triple means the labelled finite-switch trajectory
(mu,q,L;U,V,rho), modulo a.e. changes of rho and independent global signs of
the two modes consistent with U_t(0)=1 and V_t(0)=q>0.  At a solution of
(3.1), (3.8) gives q>1, S<0 initially, and the quotient proof makes all
events simple.  Cellwise IVP uniqueness and induction across those events
therefore show that fixed (mu,q,L,R,e) supports at most one such oriented
trajectory.  Hence the trajectory-level equivalence descends to the claimed
three-number bijection.
```

### Repair 2: chamber definition

Replace the opening qualifier of Section 4 by the premise-complete chamber
quantifier displayed in Section 3.2 of this audit.  Explicitly require a
fixed effective material word and transverse `S` events up to the relevant
indexed zero times, and quantify over all such chambers.

### Repair 3: reflection orientation

Replace “common rescaling” by formula (4.1), noting that the common scaling
**magnitude** is `1/|U_t(L)|` while the two modes receive independent signs.
Then state that uniqueness is across all premise-complete chambers.

## 8. Final assessment

The relay energy, scaling, normalization, Sturm identification, endpoint
ratio, Wronskian argument, and exact `2n` simple-event count are mathematically
correct and noncircular.  They establish a substantial exact reduction of
the complete asymmetric problem.  The current write-up is **QUALIFIED**, not
failed: it must formalize the hybrid trajectory/chamber object and correct
the reflection orientation sentence before the advertised three-number
bijection and two-variable formulation are proof-package ready.

Even after repair, the result remains `RIGOROUS_PARTIAL_RESULT`.  It may be
proposed as an exact equivalence/reduction, but it cannot change the status of
the universal O3a target until uniqueness across all premise-complete relay
chambers, or a certified distinct pair of roots, is established.

## 9. Repair verification (2026-08-12)

Repaired artifact audited:

```text
derivation.md
SHA256 0e6f919fa94e5f2a3c1c90ee825916346289d0c2c0f5250315a1a7e17da6679f
```

This verification appends to, and does not alter, the independent conclusions
above.

1. **Trajectory uniqueness: VERIFIED.**  Section 2 now defines a relay triple
   as the labelled finite-switch trajectory `(mu,q,L;U,V,rho)`, modulo a.e.
   changes of `rho`, with both initial orientations fixed.  It also supplies
   the missing descent to scalar labels: at a root, `q>1` and the quotient
   argument make every event sign-changing and simple, while cellwise IVP
   uniqueness and induction through the finite event list give at most one
   oriented trajectory for fixed `(mu,q,L,R,e)`.  This is exactly the logical
   bridge requested in Repair 1 and does not assume the target uniqueness.
2. **Premise-complete chamber quantifier: VERIFIED.**  Section 4 fixes the
   finite effective material word through the larger indexed zero time,
   requires every encountered event to be transverse, excludes an unresolved
   endpoint grazing, and requires a continuous selected IVP branch and simple
   indexed zero times.  It takes the union over all such chambers and expressly
   requires a global argument to cover every chamber and identify duplicate
   closure descriptions.  This discharges Repair 2 without deleting grazing
   configurations from the original target: transversality is recovered at
   every actual common zero by Theorem 3.1.
3. **Independent reflection signs: VERIFIED.**  With
   `p=U_t(L), r=V_t(L)`, (5.1) uses the common magnitude `1/|p|` but the
   independent factors `-sign(p)` and `-sign(r)`.  Direct differentiation gives
   `U#_t(0)=1` and `V#_t(0)=|r|/|p|`; the common magnitude preserves `S` and
   norm equality.  Endpoint energy gives `|r|>|p|`, hence `q#>1`.  The final
   uniqueness statement now ranges over all premise-complete chambers.  This
   discharges Repair 3.

**Post-repair verdict: PASS for the advertised exact relay bijection and
two-scalar reduction, with status still `RIGOROUS_PARTIAL_RESULT`.**  All three
earlier qualifications are discharged.  As before, the repaired artifact
proves neither uniqueness of the two-scalar zero nor the full O3a theorem.

## 10. Auxiliary independent audit: Hamiltonian structure and saltation

Artifact audited:

```text
hamiltonian_structure.md
SHA256 21ebf04e5a27ac13d68c1a036456e47ae380579b87441f23f3a18c2dc1770e11
```

### 10.1 Sign and normalization reconstruction

Write the matrix of
`omega=dU wedge dP-dV wedge dQ` as

```text
Omega=diag(J,-J),             J=[[0,1],[-1,0]].
```

Under the convention `i_{X_H} omega=dH`, one has
`X_H=Omega grad H`.  For

```text
H=1/2(P^2-Q^2)+Phi(U^2-mu^2 V^2),   rho=2 Phi'(S),
```

this gives exactly

```text
(U_t,P_t,V_t,Q_t)=(P,-rho U,Q,-mu^2 rho V).
```

Thus the minus sign in the `V,Q` block of `omega` is necessary and correct;
using the all-positive canonical form would give the wrong `V_t` sign for the
indefinite kinetic term.  On a material cell, `2 Phi=rho S`, so `2H` equals
the relay energy.  Also `H_+-H_-=(Delta rho/2)S`, hence the piecewise
Hamiltonian is continuous on `S=0`.

### 10.2 Exact saltation check

For an identity reset across the autonomous guard `S=0`, the standard exact
saltation matrix is

```text
Xi=I+(f_+-f_-) (grad S)^T / ((grad S)^T f_-).
```

The displayed vectors in (1.6) satisfy

```text
a=f_+-f_-=(Delta rho/2) Omega n,
n^T a=0,
Omega a=-(Delta rho/2)n,
d=n^T f_-=S'.
```

Consequently the denominator is nonzero precisely under the stated
transversality hypothesis, `det Xi=1`, and expansion of the rank-one update
gives

```text
Xi^T Omega Xi
= Omega + n a^T Omega/d + Omega a n^T/d
          + n(a^T Omega a)n^T/d^2
= Omega.
```

There is no missing minus sign or factor of two in `Xi`.  Moreover
`n^T a=0` implies `n^T f_+=n^T f_-`, as required by continuity of `S'` at an
event.  Products of the constant-cell Hamiltonian fundamental matrices and
these saltation matrices are therefore symplectic and have determinant one.

### 10.3 Scope and adversarial boundary checks

- The result requires transverse events.  It makes no saltation claim at a
  grazing point where `d=0`.
- The symplectic monodromy is the four-dimensional **state** variational map
  at fixed `(mu,R,e)` (and a fixed selected relay branch).  Parameter
  sensitivities in an augmented `(z,mu,q,...)` Jacobian are not thereby
  symplectic; the note's conclusion must not be propagated to such an
  augmented map.
- Pointwise allocation of `rho` on `S=0` is irrelevant; only the two one-sided
  vector fields enter `Xi`.
- Symplecticity does not imply relay nondegeneracy or exclude conjugate points,
  and the artifact explicitly observes this limitation.

**Auxiliary verdict: PASS.**  The Hamiltonian sign, energy normalization,
saltation matrix, determinant, and symplectic identity are exact.  For maximum
clarity in any later canonical use, state the convention
`i_{X_H}omega=dH` and read “monodromy” as the fixed-parameter 4D state
monodromy; these are scope clarifications, not mathematical repairs.

## 11. Hamiltonian scope-repair verification (2026-08-12)

The scope-only revision is bound to

```text
hamiltonian_structure.md
SHA256 697cb8ffa659095cc48bb78702fc925f31478137f2bd6d361f9335addd6c7f6e
```

It now explicitly states the convention `i_{X_H}omega=dH` and limits the
symplectic conclusion to the fixed-parameter four-dimensional state
monodromy, expressly excluding parameter-augmented sensitivities.  These are
exactly the clarifications requested in Section 10.3.  No formula changed;
the auxiliary **PASS** verdict is unchanged.
