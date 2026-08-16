RIGOROUS_PARTIAL_RESULT

# MIN-REFL-B: determinant-only event orientation and five certified `n=2` boundary faces

## 0. Scope, snapshot, and calibrated outcome

This route is bound to

```text
run_id: R-20260815T181317Z-min-reflection
route_id: MIN-REFL-B
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:76346e2fa9f880fd8c1c02bf4b001b38cb66f2f4688c8497c9d764ebb746c7a7
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

The universal minimum-side reflection theorem is **not** proved or refuted.
No premise-complete asymmetric counterexample was obtained.  The route has
three exact outputs:

1. the determinant orientation needed by the R7 bridge is exactly
   `det(H)>0`, which is strictly weaker than complementary inertia `H>0`
   for `n>=3`;
2. the proposed pairwise endpoint order on equal-norm roots is logically
   equivalent to reflection fixing, and a differentiable shooting proof of
   that order re-enters the same R7 continuant sign obstruction;
3. for the unresolved general-`mu`, `n=2` interface inequality, rigorous Arb
   coverings extend the frozen R17 inner-box certificate across five of the
   six single boundary collars (with the other two coordinates kept in the
   old inner interval).  The `t downarrow 0` collar and every collar
   intersection remain open.

The third output is a finite interval certificate on precisely stated boxes,
not an all-parameter proof.

## 1. Exact determinant-only reduction

Fix a premise-complete transverse min relay word with `m=2n` events.  Use the
accepted R8/R9 event notation

```text
M=D+B^T K^(-1)B,
D=diag(a_1,...,a_(2n))>0,
sign(K_i)=(-1)^(i+1),
L_-=K+B D^(-1)B^T.
```

Here `B` is the `(2n-1)`-by-`2n` path incidence matrix and `L_-` is exactly
the R7 relative path matrix.  Split the positive odd and negative even
edges as in the accepted complementary-inertia package:

```text
M=P-C^T W^(-1)C,
P>0, W>0,
H=C P^(-1)C^T-W,
dim(H)=n-1.
```

### Lemma 1 (orientation, without positive definiteness)

For every such word,

```text
sign det(L_-)=sign det(H).                            (1.1)
```

This identity is on the R7 relative quotient; the permanent common-scaling
Jacobi field has already been removed.

### Proof

Sylvester's determinant identity applied to the full incidence form gives

```text
det(M)
 =det(D) det(I+D^(-1)B^T K^(-1)B)
 =det(D) det(I+K^(-1)B D^(-1)B^T)
 ={det(D)/det(K)} det(L_-).                           (1.2)
```

There are exactly `n-1` negative even entries of `K`, so

```text
sign det(K)=(-1)^(n-1).                              (1.3)
```

The dual Schur form independently gives

```text
det(M)
 =det(P) det(I-P^(-1)C^T W^(-1)C)
 ={det(P)/det(W)} det(W-C P^(-1)C^T)
 =(-1)^(n-1){det(P)/det(W)}det(H).                   (1.4)
```

All omitted determinants in (1.2) and (1.4), except the displayed signed
ones, are strictly positive.  Combining (1.2)--(1.4) proves (1.1).  `QED`

### Consequence

The exact missing local orientation can be stated as

```text
det(H)>0.                                             (1.5)
```

By the trusted R7 claim, (1.5) is equivalent to

```text
det(L_-)>0  iff  J<0  iff  partial_q A_n<0.          (1.6)
```

For `n=2`, `H` is scalar, so (1.5) and `H>0` coincide.  For `n>=3`,
`det(H)>0` does **not** imply `H>0`; it fixes only the parity of the negative
index.  Therefore the previous target `n_-(M)>=n-1`, equivalently `H>0`, is
a sufficient but unnecessarily strong substitute for determinant
orientation.  This resolves the parity bookkeeping but does not sign
`det(H)`.

## 2. Exact status of the pairwise endpoint-order bypass

Let `E_mu` be the set of premise-complete equal-norm full roots at fixed
`(R,n,mu)`, labeled by their initial ratio `q>1`.  Accepted full-relay IVP
uniqueness makes this label injective in the indexed root class.  For a root
write

```text
p=U_t(L),
q_sharp=abs(V_t(L))/abs(U_t(L)),
E(q)=(q^2-1)/p^2=q_sharp^2-1.                        (2.1)
```

Reflection preserves `E_mu`, sends `q` to `q_sharp`, and is an involution.
Thus

```text
E(q_sharp)=q^2-1.                                    (2.2)
```

### Lemma 2 (pairwise order is target-equivalent)

The following are equivalent on `E_mu`:

```text
(a) every root is reflection fixed;
(b) q_1<q_2 implies E(q_1)<=E(q_2) for every two roots. (2.3)
```

If (a) holds, then `E(q)=q^2-1`, so (b) is strict.  Conversely, if a root
had `q<q_sharp`, applying (b) to its reflected pair would give

```text
q_sharp^2-1=E(q)<=E(q_sharp)=q^2-1,
```

a contradiction.  The case `q_sharp<q` is identical after exchanging the
pair.  This proves the equivalence.

The order statement is therefore a potentially different mechanism, but it
is not a weaker mathematical assertion on the equal-norm root set.  Its
cross-multiplied form is the exact two-root inequality

```text
(q_1^2-1)p_2^2 <= (q_2^2-1)p_1^2.                   (2.4)
```

A direct proof of (2.4), using both complete roots and never interpolating
through non-roots, could bypass pointwise continuant orientation.  No such
two-root identity was found.  In contrast, every attempted differentiable
shooting/order proof must orient the fixed-`mu` common-terminal residual;
its local condition is exactly (1.6).  Hence that proof family bypasses the
full inertia theorem but **not** `det(L_-)>0`.

The accepted transfer obstruction explains why a cellwise comparison is
insufficient: even in the subcritical chamber the natural two-cell DtN minor
has the sign of an unordered phase difference and takes both signs.  The
accepted shape-Hessian formula gives the parallel continuum obstruction:
the reduced Green remainder has mixed spectral signature.  A restart for
(2.4) must therefore use a genuinely global two-root Picone/action identity
with the equal-norm and terminal conditions retained, rather than multiply
locally oriented cell factors.

## 3. `n=2`, general-`mu`: rigorous five-face extension of R17

### 3.1 Input reduction

The prior, non-canonical R14 route artifact uses

```text
k=(mu-1)/(mu+1),
t=2 Aplus/pi,
y=(Aminus-pi/2)/(pi/(1+k)-pi/2),
0<k,t,y<1.
```

The half-domain `g>=1`, equivalently `F_+F_->=1`, is already closed
analytically by R14.  On the remaining physical subset

```text
g<1, rB>1,                                            (3.1)
```

R14 reduces the split-gap sign to positivity of four explicit Bernstein
coefficients `B_i`.  In the stable R17 normalization their signs are the
signs of

```text
G_i=g Knew cp^4-Pplus Nhat_i,  i=1,2,3,4.            (3.2)
```

The frozen R17 checker proved (3.2) on

```text
I^3,  I=[1/64,63/64].                                (3.3)
```

This route reuses its exact common-angle evaluator and its conditional
positive contractor without changing (3.2).

### 3.2 Stable large-`mu` discard identity

The old expression for `b-a` loses correlation as `k` approaches one.  Put

```text
h=pi(1-k)/[2(1+k)],
Aplus=pi t/2,
Aminus=pi/2+y h,
v=1+k-k y.
```

The exact centered amplitudes obey

```text
A:=k a=tan(k Aplus)/tan(Aplus),
B:=k b=-tan(k Aminus)/tan(Aminus)=tan(yh)/tan(vh).    (3.4)
```

Since `k>0`, `sign(b-a)=sign(B-A)`.  The implemented form

```text
A=k sinc(kAplus)cos(Aplus)/[sinc(Aplus)cos(kAplus)],
B=y sinc(yh)cos(vh)/[v sinc(vh)cos(yh)]              (3.5)
```

extends continuously to `k=1` and contains no `0/0`.  Equations
(3.4)--(3.5) are elementary identities, not interval assumptions.  They
allow rigorous early rejection of boxes disjoint from `g<1`.

### 3.3 Certified boxes

At 128-bit Arb precision with exact 34-bit dyadic endpoints, all leaves in
the following five boxes were either rejected by `g<1`/`rB>1` or certified
to have every `G_i>0`:

| face | box in `(k,t,y)` | visited | outcome | minimum directed lower endpoints `(G1,G2,G3,G4)` |
|---|---|---:|---|---|
| `k downarrow 0` | `[0,1/64] x I x I` | 2,135 | complete | `(0.0548784, 0.00381281, 0.0480570, 0.108571)` |
| `k upward 1` | `[63/64,1] x I x I` | 218,831 | retained subset empty | not applicable |
| `t upward 1` | `I x [63/64,1] x I` | 23,715 | complete | `(0.0483281, 0.00722917, 0.00755813, 0.000502149)` |
| `y downarrow 0` | `I x I x [0,1/64]` | 101 | complete | `(0.269037, 0.215162, 0.240479, 0.370773)` |
| `y upward 1` | `I x I x [63/64,1]` | 36,257 | complete | `(102.633, 100.297, 97.2124, 2.72254)` |

Every run had `singular=0`, `unresolved=0`, an empty final stack, and the
exact binary-tree identity `leaves=splits+1`.  Full counts and unrounded
lower endpoints are frozen in `face_results.json`.

In physical frequency terms, the first box includes the closure
`mu downarrow 1` and all `1<mu<=65/63`, subject to the two inner phase
coordinates.  The second covers `mu>=127` with inner phases and proves that
no point satisfies both retained conditions (3.1) there.  This explicitly
tests both near-coalescent and large-frequency regimes without extrapolating
either result to collar intersections.

### 3.4 What this implies

Let

```text
Omega_cert = I^3
  union ([0,1/64] x I x I)
  union ([63/64,1] x I x I)
  union (I x [63/64,1] x I)
  union (I x I x [0,1/64])
  union (I x I x [63/64,1]).                         (3.6)
```

For every general-`mu` physical positive-negative interface in
`Omega_cert`, the R14 coefficient route proves the split gap.  Consequently,
an `n=2` three-cell word whose actual left interface and time-reversed right
interface both lie in `Omega_cert` has scalar `H>0`, hence
`det(L_-)>0` by Lemma 1.  No reflection of the word and no equality of its
two positive-cell phases is assumed.

This is conditional parameter coverage.  It does not show that every
premise-complete root lies in `Omega_cert`.

## 4. Required adversarial tests and exact failures

### `n=2`, arbitrary asymmetry

All interface formulae retain independent left and right positive phases.
The certificate is applied to each actual interface separately.  No
reflection ansatz is used.

### `mu` near one and large

The certified `k` faces are described in Section 3.3.  Their intersections
with phase collars remain open, so neither is promoted to an unrestricted
frequency theorem.

### Parity and determinant versus inertia

Lemma 1 tracks the `n-1` negative even edges exactly.  It proves that
`det(H)>0`, not `H>0`, is the parity-correct target.  For `n=2` there is no
distinction; for `n>=3` there is.

### Permanent scaling quotient

The R7 recurrence and `L_-` live in relative `(d,w)` variables.  The common
scaling field maps to zero and is not counted as a determinant kernel.
No conclusion here is drawn from the false statement that every nonzero
physical Dirichlet Jacobi field is nonzero in relative variables.

### Endpoint/event-pair softness

The omitted face

```text
t in [0,1/64], k,y in I                              (4.1)
```

did not close under the same unrescaled interval subdivision.  Numerically
the gaps remain positive and become large, but the evaluator contains
quantities of orders `q^(-1)` through `q^(-4)` as the positive phase tends
to zero, so interval dependency prevents a finite cover including `t=0`.
No negative box was produced.  Repeating the same subdivision without first
rescaling this soft event pair is not a viable restart.

Except for shared threshold boundaries already belonging to `I`, the
interiors in which two or more coordinates lie outside `I` are outside the
proven union (3.6).  Single-face certificates cannot be combined by overlap
rhetoric; those collar-intersection interiors require their own normalized
cover or an analytic boundary lemma.

### Discovery-only falsification scans

Two fixed-seed floating scans were used only to attack the conjectured sign:

```text
general-mu physical common-angle interfaces:
  draws=300000, retained=97507, nonpositive Phi or N_left=0

R14 coefficient domain with logistic boundary bias:
  draws=1000000, retained=79019, nonpositive G_i=(0,0,0,0)
```

The first scan included `mu-1` down to `1e-4`, large `mu`, `r-1` from
`1e-5` to `1e5`, and phase-boundary bias.  These local interfaces omit the
common-terminal/equal-norm predicates and are nonpropagating numerical
evidence only.

## 5. First precise failing inequalities and restart conditions

The route stops at three noninterchangeable obligations:

1. **`n=2` soft face and intersections.**  Rescale the R14 coefficient gaps
   by the exact vanishing phase, beginning with `q^4 G_i`, derive their
   continuous `t=0` limits, and certify the rescaled collar together with
   its intersections.  Raw further subdivision is disallowed by the observed
   dependency blow-up.
2. **General `n`, determinant only.**  Prove `det(H)>0` directly from the
   physical Jacobi continuant.  Do not replace it by `H>0`; a valid route may
   allow mixed inertia as long as the determinant remains positive.
3. **Endpoint-order bypass.**  Prove the complete two-root inequality (2.4)
   directly on equal-norm roots.  Any interpolation/one-root derivative
   argument must instead discharge (1.6), so it is not a bypass.

The old relaxed coefficient routes cannot restart the proof: exact accepted
counterexamples already show that phase thresholds plus gamma matching, an
independent-half-angle domain, and a cross-only common-tangent interval are
too weak.  A restart must retain the same-`mu` common-angle scale, both
individual momenta, and (for the pairwise route) both full terminal and norm
closures.

## 6. Reproducibility and artifact bindings

Run from the project root:

```powershell
$env:PYTHONPATH='tmp\r12-flint312'
$env:PATH=(Resolve-Path 'tmp\r12-flint312\python_flint.libs').Path+';'+$env:PATH
$py='E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe'
$s='runs\R-20260815T181317Z-min-reflection\routes\event_inertia\cover_collar.py'
& $py $s k0 --max-boxes 2000000
& $py $s k1 --max-boxes 2000000
& $py $s t1 --max-boxes 2000000
& $py $s y0 --max-boxes 2000000
& $py $s y1 --max-boxes 2000000
```

Frozen inputs and route artifacts:

```text
cover_collar.py
  bytes: 4400
  sha256:6c3a4af844a4730b6df577b28c26ded3ac23e1e86f59538ce824c740708c97c2
face_results.json
  bytes: 3447
  sha256:e169fad11e365ba1764879d0beb6f8bb955bb5232526097a03798476193738ed
upstream R17 exact_checker.py
  bytes: 8097
  sha256:ad1e084f40ed11a80576d2f768fe32c418db391d6d4d98700526a0b4e3b8584b
upstream R14 derivation.md
  bytes: 10721
  sha256:bc991d859eac196b08a719ded874a9208a648d2578ea0ce0320e4a0a5ced1fd3
```

Discovery scripts, not proof certificates:

```text
explore_interface.py
  sha256:1b5ed5797ccb31f09936c47a51cb3435bc280fb5261a1a9987c2878af03d5d34
explore_coefficients.py
  sha256:3a72be8b988fccb97e872d9280c31cbee4858a08e95086901c672922afb1b108
```

Software is Python `3.12.13`, python-flint `0.9.0`, Arb precision `128`
bits.  The proof evaluator inherits the frozen R17 alternating-series sinc
enclosure and exact dyadic partition contract.

## 7. Route registry and confidence

```text
route_id: MIN-REFL-B
target: OBL-NGE2-MPO3A-MIN-COMPLEMENTARY-INERTIA-R8 or weaker orientation
method_family: event matrix, dual Schur Jacobi chain, exact determinant parity,
               common-angle Arb certification
current_status: rigorous_partial_result
proved_results:
  - sign det(L_-)=sign det(H) on the relative quotient
  - pairwise endpoint order iff reflection fixing on the equal-norm root set
  - five single-face finite Arb certificates in Section 3.3
counterexamples: none satisfying the physical full-root premises
first_failing_step:
  - t-down soft face and all collar intersections for n=2
  - det(H)>0 for arbitrary general-n physical words
  - direct full-root two-point inequality (2.4)
restart_conditions:
  - q^4-rescaled soft-face/intersection certificate or analytic limit lemma;
  - determinant continuant invariant not requiring positive definiteness; or
  - global two-root Picone/action comparison retaining equal norm and terminals
```

```text
novelty_status: unknown
formalization_status: not_requested
confidence_semantic_fidelity: high
confidence_exact_linear_algebra: high
confidence_finite_face_certificates: high, pending independent replay/audit
confidence_universal_n2_completion: low; uncovered domains remain
confidence_all_n_completion: low; determinant sign remains open
```

Human contribution: frozen target and eight-hour scope.  Model contribution:
the determinant-only parity lemma, endpoint-order equivalence audit, stable
large-`mu` contractor, domain decomposition, and stopping analysis.  Tool
contribution: deterministic retrieval, exact hashing, directed Arb covering,
and bounded discovery scans.
