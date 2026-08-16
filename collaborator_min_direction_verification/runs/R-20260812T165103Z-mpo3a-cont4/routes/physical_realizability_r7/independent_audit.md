REJECT_PENDING_SCOPE_CORRECTION

# Independent audit of the R7 physical-continuant reduction

## 0. Binding, independence, and verdict

Audited artifact:

```text
path:
  runs/R-20260812T165103Z-mpo3a-cont4/routes/
  physical_realizability_r7/derivation.md
bytes: 24861
sha256: 2a2cbd7d22698a9e2e3f545f3623c1baa8ec7f1f5bb76633538882a25bd0ff41
```

Canonical snapshot independently queried for this audit:

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:3e0839c6d73e194653314ae1c456bbc77899bdc279f171f590089ad9c0f38394
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

The auditor did not participate in the R7 derivation and did not use a
pending proposal or candidate claim as a premise.  The relevant canonical
inputs were independently confirmed to be proof-input eligible.  The
continuant, endpoint-sign, Schur-inertia, gluing, and time-translation
calculations were recomputed rather than accepted from the candidate note.

Verdict: **reject pending one blocking scope correction**.  The central
distinguished-`log(q)` theorem is correct, including every factor and sign:

```text
w_m=sigma product_i(a_i) det(L_sigma),
w_m=-q sigma(R-1)J,
J<0 iff det(L_sigma)>0
    iff sign(w_m)=sigma
    iff sign(partial_q A_n)=sigma.
```

However, Sections 3 and 5 overstate what `det(L_sigma)=0` and `ker(M)`
classify.  The homogeneous scaling Jacobi field `z=(U,U_t,V,V_t)` is always
a nonzero field with zero position components at both endpoints, but it has
`d_i=0` and equal Wronskian `w_i=0` everywhere.  It is therefore invisible
to both scalar matrices.  The statements become correct after explicitly
passing to the equal-component-Wronskian relative mode modulo this scaling
line, or after saying “an additional non-scaling Dirichlet Jacobi direction.”
Until that qualification is made in the frozen proof package and proposed
claim, an approval would certify a false literal statement.

The listed `CLM-NGE2-MPO3A-TRANSFER-OBSTRUCTION` is not used in the proof of
the exact continuant reduction.  It is background supporting the warning
against a local total-positivity shortcut and should not be a premise of a
new proved inference unless the proposed conclusion actually includes that
obstruction.

## 1. Blocking issue and exact minimal repair

### B1. Scalar reduction forgets the universal scaling field

The note says:

```text
“An arbitrary nonzero Dirichlet Jacobi field exists ... exactly when this
determinant vanishes.”
“Consequently terminal conjugacy is exactly ker(M)!={0}.”
```

Taken literally for the full four-dimensional hybrid variational system,
both sentences are false.  Homogeneity provides the Jacobi field

```text
xi=z,
xi(0)=(0,1,0,q),
xi(L)=(0,p,0,r),
```

whose position components vanish at both endpoints.  At each event its
relative value and component Wronskians are

```text
d_i=xi_U/U_i-xi_V/V_i=1-1=0,
w_i^U=U_i U_i'-U_i' U_i=0,
w_i^V=V_i V_i'-V_i' V_i=0.
```

Thus it maps to the zero vectors of both `L_sigma` and `M`, regardless of
their determinants.  The scalar word detects a second, relative mode and
not the ever-present scaling line.

Minimal acceptable repair:

```text
det(L_sigma)=0 iff there exists a nonzero scalar relative mode w with
w_0=w_m=0; equivalently, the equal-component-Wronskian hybrid variational
subspace contains an additional Dirichlet Jacobi direction not proportional
to the scaling field.

ker(M)!={0} iff there exists such a nonzero relative event vector d; after
quotienting the Dirichlet Jacobi space by the scaling line, this is exactly
the additional terminal-conjugacy condition relevant to the q direction.
```

For the distinguished `log(q)` field, `d_1=-1`, so it is automatically
non-scaling.  Hence B1 does **not** affect the main identities relating
`w_m`, `det(L_sigma)`, `J`, and `partial_q A_n`.

## 2. Definition and physical-gluing audit

### 2.1 Event signs and `alpha_i`

At an event, `mu V_i=epsilon_i u_i` and

```text
S_i'=2u_i(p_i-epsilon_i mu r_i),
alpha_i=-2 Delta rho_i u_i^4/S_i'
       =-Delta rho_i u_i^3/(p_i-epsilon_i mu r_i).
```

The negative energy `p_i^2-r_i^2=1-q^2=-beta^2` allows

```text
r_i=tau_i beta cosh(h_i),
p_i=tau_i beta sinh(h_i).
```

Since `mu>1`,

```text
sign(p_i-epsilon_i mu r_i)=-epsilon_i tau_i.
```

The accepted crossing order gives `sign(S_i')=epsilon_i`, so from the last
two displays `tau_i=-sign(u_i)`.  Together with
`sign(Delta rho_i)=sigma epsilon_i`, this yields
`sign(alpha_i)=-sigma`.  The factor of two has not been lost: it is exactly
cancelled by the `2u_i` in `S_i'`.

This part passes for max and min.  It requires `u_i!=0`; that is automatic
for a transverse switching event because `U_i=V_i=0` would force
`S_i'=0`.

### 2.2 Two-frequency cell gluing and `K_i`

Direct oscillator propagation gives

```text
u_(i+1)=c_i u_i+s_i p_i/sqrt(rho_i),
p_(i+1)=-sqrt(rho_i)s_i u_i+c_i p_i,

-epsilon_i u_(i+1)=epsilon_i C_i u_i+S_i r_i/sqrt(rho_i),
r_(i+1)=-epsilon_i sqrt(rho_i)S_i u_i+C_i r_i.
```

Eliminating the next event value gives (1.12) exactly.  Subtracting the two
relative endpoint determinant identities, using
`epsilon_(i+1)=-epsilon_i`, gives

```text
K_i=[sin(theta_i)+mu sin(mu theta_i)]/
    [sqrt(rho_i)u_i u_(i+1)].
```

The all-cell phase lemma makes the numerator positive.  The allocated low
zero pattern makes `sign(K_i)=+,-,+,...`.  These formulae pass, including
the first and last internal event cells.  There is no `K_i` on either
outer endpoint cell; the document consistently indexes only the `m-1`
event-to-event cells in the scalar recurrence.

### 2.3 Specific abstract lift

With `C=1/2+sqrt(3)`, direct exact arithmetic gives

```text
p_1=3/4-sqrt(3)/2,
p_2(first-cell)=-7/4+3sqrt(3)/8,
p_2(second-cell)=-155/24-3sqrt(3)/16,
difference=113/24+9sqrt(3)/16>0.
```

Thus the displayed lift fails low-frequency derivative gluing.  The note
correctly limits the conclusion to this lift and does not claim that every
lift of the abstract coefficient tuple is impossible.

## 3. Logic audit of the continuant theorem

Write `alpha_i=-sigma a_i` with `a_i>0`, `k_i=sigma K_i`, and use the
recurrences

```text
w_i-w_(i-1)=alpha_i d_i,
d_(i+1)-d_i=K_i w_i.
```

Eliminating `d_i` gives

```text
(w_i-w_(i-1))/a_i-(w_(i+1)-w_i)/a_(i+1)-k_i w_i=0,
```

which is `L_sigma w_internal=0` under `w_0=w_m=0`.  The diagonal and
off-diagonal entries in (3.4) and the LDL recursion (3.5) are correct.

For the actual `log(q)` field, `w_0=0`, `d_1=-1`, hence
`w_1=sigma a_1`.  The first row of the inhomogeneous Dirichlet system is

```text
L_sigma w_internal=(sigma a_1/a_1,0,...,0)^T
                    =(sigma,0,...,0)^T.
```

The corner cofactor of the `(m-1)`-by-`(m-1)` irreducible tridiagonal
matrix is

```text
(L_sigma^(-1))_(m-1,1)
 =1/[a_2 ... a_(m-1) det(L_sigma)].
```

The last recurrence row then yields

```text
w_m=sigma a_1...a_m det(L_sigma).
```

Checking `m=2` directly gives

```text
w_2=sigma[a_1+a_2-sigma K_1 a_1a_2],
```

which matches the determinant formula and fixes its sign.

Let `eta=partial_q z` and `zeta=q eta`.  At the common terminal,

```text
w_m=-p zeta_U(L)=-q p eta_U(L).
```

The accepted causal identity is
`p eta_U(L)=sigma(R-1)J`; therefore

```text
w_m=-q sigma(R-1)J.
```

Using the accepted endpoint derivative formula gives

```text
partial_q A_n=(q^2-1)w_m/(q p^2r^2).
```

All factors multiplying `det(L_sigma)` or `J` are strictly positive apart
from the displayed `sigma`, so (3.5d) passes.  This audit specifically
confirms both occurrences of the essential factor `q`.

The note also correctly separates:

```text
required theorem: det(L_sigma)>0;
strong sufficient theorem: L_sigma positive definite;
```

and never infers the determinant sign from the finite pivot scout.

The abstract word gives

```text
L=tridiag(diag(2/3,3,2/3),-1),
(P_1,P_2,P_3)=(2/3,3/2,0).
```

In particular `4/3<2`, so it defeats a coefficient-local diagonal test by
global continuant saturation, exactly as stated.

## 4. `M`, bidirectional reconstruction, and Schur inertia

With `(Bd)_i=d_(i+1)-d_i`, `D=diag(a_i)`, and `K=diag(K_i)`, elimination of
the fluxes gives

```text
M=-sigma D+B^T K^(-1)B,
Md=(-w_0,0,...,0,w_m)^T.
```

The entries displayed in (5.2) follow.  Conversely, given a **nonzero
relative event vector** `d` with `Md=0`, define

```text
w_i=w_(i-1)+alpha_i d_i,
w_0=0.
```

The first through penultimate rows recover
`d_(i+1)-d_i=K_iw_i`; the last row recovers `w_m=0`.
All `K_i` are nonzero because their numerators and event amplitudes are
nonzero.  Thus the bidirectional scalar reconstruction is correct.  B1 is
only the missing qualification when this scalar statement is translated
back to the full Jacobi field space.

For

```text
H=[-sigma D  B^T; B  -K],
```

the two Schur complements are exactly `M` and `sigma L_sigma`.  Since `K`
has `n` positive and `n-1` negative entries, the inertia arithmetic gives,
when `L_sigma>0`,

```text
max: In(M)=(n negative,n positive,0 zero),
min: In(M)=(n-1 negative,n+1 positive,0 zero).
```

The expanded formulae (5.8) also recompute correctly and prove both
directions of the claimed equivalence.  This is an equivalence only between
the *strong* positive-definiteness and target-inertia statements; it is not
an equivalence to the weaker required determinant orientation.  The note
makes that distinction correctly.

## 5. Time-translation forcing audit

For `zeta=(U_t,V_t)`,

```text
gamma_i=(p_i-epsilon_i mu r_i)/u_i=S_i'/(2u_i^2),
```

so `sign(gamma_i)=(-1)^(i+1)`.  The gauge determined by
`eta_(i+1)/eta_i=sign(K_i)` is `++--++--...`, hence
`sign(E gamma)=+--++--+...` and has exactly `n` sign changes among `2n`
entries.  These signs pass.

The time-translation Wronskians satisfy

```text
X_i=-(p^2+rho_i U^2),
Y_i=-(r^2+mu^2rho_i V^2),
X_i-Y_i=q^2-1=beta^2,
```

and have the same event jump.  Thus time translation is not in the
equal-Wronskian scalar subspace; the note correctly refuses to use it as a
homogeneous ground state.

Independently propagating the relative logarithmic derivatives across one
cell gives

```text
gamma_(i+1)-gamma_i
 =K_i[Y_i+beta^2 sin(theta_i)/
                (sin(theta_i)+mu sin(mu theta_i))].
```

Therefore, with the displayed `chi_i`, the three lines of (6.8) follow by
applying `M` and telescoping the common Wronskian jumps.  Endpoint energies
are

```text
X_0=-1,
Y_0=-q^2,
Y_last=-r_L^2,
```

which yield the stated forcing endpoints.  Since
`0<chi_i<beta^2`, their signs in (6.9) are strict.

For

```text
F_mu(theta)=sin(theta)/[sin(theta)+mu sin(mu theta)],
```

differentiation gives numerator

```text
mu[cos(theta)sin(mu theta)-mu sin(theta)cos(mu theta)].
```

Its sign is that of `cot(theta)-mu cot(mu theta)`, positive because
`x cot(x)` is strictly decreasing on `(0,pi)`.  The endpoint limits are
`1/(1+mu^2)` and `1`, so (6.10) passes.  Consequently the internal forcing
sign depends on the unavailable ordering of adjacent phases; no hidden
phase-order premise is used.

Multiplying (6.8) by a zero-mode `d`, using symmetry, and summing by parts
gives (6.11).  Substitution of
`d=(-1,1/3,-1/3,1)` gives (6.12) after multiplication by `-3`; the arithmetic
is correct.

## 6. Numerical evidence audit

The finite scout was preregistered and remains explicitly non-propagating.
I independently reconstructed `a_i` and `K_i` from all 32 records in
`../discrete_jacobi_twist/coefficient_probe.json` and reran the LDL recursion
in IEEE-754 binary64.  The reported aggregate values reproduce:

```text
records: 32
pivots: 182
nonpositive pivots: 0
minimum pivot: 0.16312236973746758
minimum case: n=5, R=100, max, pivot 5
positive-k cells: 89
local diagonal violations: 0
maximum local ratio: 0.65702041175109716
```

This is evidence only.  It has no completeness certificate and cannot
establish the universal determinant or positive-definiteness claim.

## 7. Boundary and adversarial audit

* `n=2` was checked explicitly in the continuant identity and in the
  coefficient-level saturation example.
* Both max and min signs were checked in the path recurrence and the Schur
  inertia count.
* The internal matrices use exactly `m=2n` events and `m-1` event-to-event
  cells.  Endpoint cells enter the relay energy and time-translation
  endpoint forcing, but do not create extra `K_i` entries.
* No reflection symmetry or palindromy is assumed.  The formulae apply to
  asymmetric premise-complete roots.
* Finite `R>1`, `q>1`, simple terminal zeros, and transverse interior events
  keep every denominator used in the reduction nonzero.
* At `R->1+`, `alpha_i` tends to zero and `a_i^{-1}` becomes singular; the
  finite-contrast algebra is not claimed to extend by direct substitution
  to `R=1`.
* Grazing events, switch collisions, or non-transverse closure points are
  outside the coefficient formulae as written.  A universal result “with
  compatible closures” still needs a separate limiting/continuation
  argument.  The R7 exact theorem should therefore be claimed only on the
  transverse chamber scope unless such a closure proof is supplied.
* `det(L_sigma)=0` is the relative-mode degeneracy condition, not the
  existence of any Dirichlet Jacobi field; B1 is the only blocking defect.
* The physical Hardy/positive-definiteness lemma is stronger than the
  actual R6 requirement.  The minimum remaining statement is exactly
  `det(L_sigma)>0` for each premise-complete transverse physical word.

## 8. Required disposition

Blocking correction before proposal validation:

1. Replace the two unqualified terminal-conjugacy sentences in Sections 3
   and 5 by the quotient/non-scaling formulation in B1.
2. Ensure the proposed established claim states only the exact transverse
   continuant theorem and does not claim arbitrary closure points.

Nonblocking recommendations:

1. Remove `CLM-NGE2-MPO3A-TRANSFER-OBSTRUCTION` from the proved inference's
   premise list unless the conclusion includes the old obstruction result.
2. Call `L_sigma>0` a stronger sufficient conjecture and keep the canonical
   open obligation at the weaker determinant orientation.
3. Keep the 32-root scout as `NUMERICAL_EVIDENCE` or an attempt record; do
   not make it a premise of the proved inference.

After B1 is corrected in a newly frozen proof package, this auditor expects
the exact transverse distinguished-`log(q)` continuant reduction to be
approvable.  Universal O3a and the finite-contrast determinant sign remain
open.
