INDEPENDENTLY_AUDITED_PROOF

# Independent audit of the R11 conditional global-order lemma and restricted min theorem

## 0. Verdict and immutable bindings

```text
verdict: APPROVE
auditor: /root/r10_max_norm_hessian
author: /root/r10_min_mu2_audit
auditor_distinct_from_author: true
context_id: CTX-DEFAULT

primary_derivation: derivation.md
primary_derivation_bytes: 20003
primary_derivation_sha256:
  sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93

author_self_audit: self_audit.md
author_self_audit_bytes: 9507
author_self_audit_sha256:
  sha256:74779447f7edcd4104482132b856169dc04fa895859be02235661ae8f3655cd0

canonical_blueprint_sha256:
  sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242
canonical_inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f

trusted_local_claim:
  CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10
trusted_local_semantic_sha256:
  semantic-sha256:157a7bf928676b7565e5e08e965909ab0657e48888d37095c43352a228bbbd21
trusted_local_derivation_sha256:
  sha256:44da5f1d76b4d8208366b3d055e4ad5456e372bd2f14077a39e51577a4353f19

external_results: []
computational_certificates: []
```

The file hashes, current canonical hashes, and trusted local proof-package
hash were independently recomputed.  The canonical record for the trusted
local claim states exactly the input used here: at every arbitrary,
possibly asymmetric, premise-complete transverse min root with `n=2` and
`mu=2`, the quotient derivative satisfies `partial_q A_2<0`; it assumes no
reflection and asserts no global order.

The audited package proves two correctly separated results.

1. For either relay orientation and fixed finite `R>1`, `n>=2`, `mu>1`, a
   uniform oriented local derivative sign at all premise-complete roots
   implies continuity and at-most-one of the global common-terminal
   residual, followed by reflection fixing.  This is conditional on that
   local sign.
2. For the min relay, `n=2`, `mu=2`, trusted R10 supplies the sign with
   orientation `sigma=-1`, so the at-most-one and reflection conclusions
   are unconditional, conditional only on a root existing.

All four mandatory audits pass.  No blocking, major, or scope-changing
finding was found.

## 1. Definition audit: PASS

1. The sign convention is uniform.  `rho_-` is the coefficient on `S<0`
   and `rho_+` the coefficient on `S>0`; hence `rho_-=1` for max and
   `rho_-=R` for min.  In particular, the min initial cell, every punctured
   joint-zero neighborhood, and the continued terminal chamber all use
   `R`, not the max coefficient `1`.
2. The global IVP is positively normalized by `U_t(0)=1`,
   `V_t(0)=q>1`.  This is the same permanent-scaling quotient coordinate
   in which trusted R10 states `partial_q A_2<0`.
3. `A_n=T_U^n-T_V^(n+1)` uses indexed positive scalar zeros.  Scalar nodal
   zeros, active relay events, and the terminal simultaneous scalar zero
   are distinguished throughout.
4. A joint zero is not counted as an active switch: it has `S<0` on both
   punctured sides.  A vanishing positive-material event pair may converge
   to it, but the limiting contact has no positive-length cell.
5. `A_n^c` is the smooth fixed-word continuation used only to import the
   local derivative.  The global relay residual `A_n` is constructed
   independently, and equality of their first derivatives is proved rather
   than assumed.
6. The general either-orientation statement is explicitly an implication.
   The package does not promote the local min sign beyond `n=2,mu=2`.
7. Reflection uses a common amplitude denominator `|p|` and independent
   orientation signs.  It gives `U#_t(0)=1`,
   `V#_t(0)=|r|/|p|` and multiplies both squared fields by the same positive
   factor, so the relay law is preserved.

No normalization, index, material label, quotient, or conditional scope is
conflated.

## 2. Logic audit: PASS

### 2.1 Energy, initial material, joint contacts, and global uniqueness

On every constant-material cell,

```text
E=P^2-Q^2+rho S=1-q^2<0.
```

The value glues across relay events because `S=0` there.  At a nonjoint
zero, tangency would imply `U=epsilon mu V` and
`P=epsilon mu Q`, hence `E=(mu^2-1)Q^2>=0`, a contradiction.  Every such
zero is therefore transverse.

At a joint zero, `P^2-Q^2<0` implies

```text
P^2-mu^2Q^2<0,
S(t_0+h)=(P^2-mu^2Q^2)h^2+o(h^2)<0.
```

Only `C^1` state regularity is needed for this expansion; no unjustified
second derivative across a switch is used.  The same calculation at
`t=0`, with slopes `(1,q)`, forces the initial punctured material to be
`rho_-`, hence `R` in the min theorem.

The cellwise construction therefore has a unique outgoing material at
every zero.  A finite accumulation would have a limiting zero with
`S_t=0`.  The limit cannot be nonjoint by the energy contradiction and
cannot be joint because the displayed strict punctured neighborhood is
zero-free.  Thus there is no finite Zeno accumulation, and the a.e.-labelled
relay IVP is global and unique.

### 2.2 Continuous dependence and indexed zero times

For `q_k->q` on a compact `q`-set and a finite time horizon, bounded
coefficients give uniform state bounds and equicontinuity.  In a uniformly
convergent subsequence, the energy identity at a limiting zero survives as

```text
P(t)^2-Q(t)^2=1-q^2,
```

because `rho_k(t)S_k(t)->0`.  The preceding zero classification therefore
makes the limiting zero set finite before the limit relay equation is
invoked.  Away from that finite set the signs of `S_k` stabilize; dominated
convergence in the Volterra equations identifies the limit as the unique
relay solution at `q`.  Uniqueness upgrades subsequential convergence to
full continuous dependence without fixing an event word.

For either component `y`, the lifted phase satisfies

```text
theta_t=(y_t^2+a(t)y^2)/(y^2+y_t^2)>=1,
```

with `a=rho` for `U` and `a=mu^2rho` for `V`.  Hence every required indexed
positive zero exists on a uniform finite horizon.  Scalar zeros are simple;
uniform convergence of both position and velocity therefore makes their
indexed times continuous.  This proves that `A_n(mu,.)` is one continuous
function on the connected interval `q>1`, not a collection of chamberwise
branches.

### 2.3 Every global zero is automatically premise complete

If `A_n(mu,q_0)=0` at length `L`, then `U` and `V` are respectively the
`n`-th and `(n+1)`-st Dirichlet modes for the same positive weight on
`(0,L)`.  Consecutive-mode strict interlacing places one zero of `V` in
each of the `n` nodal cells of `U`.

For

```text
W=V_tU-VU_t,
W_t=-(mu^2-1)rho UV,
```

the two modes have the same sign before that `V` zero and opposite signs
after it.  At each interior `U` zero, `V` and the outgoing `U_t` have the
same sign, so `W=-VU_t<0`; at the two outer endpoints `W=0`.  Cell by cell,
`W` first decreases and then increases, proving `W<0` on `(0,L)`.  Thus
`V/U` strictly decreases on every `U` nodal cell.

The terminal slopes have opposite nodal parity, while energy gives
`|V_t(L)|>|U_t(L)|`; consequently their ratio is `<-1`.  The quotient
ranges are therefore

```text
q_0 -> -infinity,
+infinity -> -infinity,
...,
+infinity -> V_t(L)/U_t(L)<-1.
```

Since `q_0>1>1/mu`, each cell crosses `+1/mu` and `-1/mu` exactly once.
These are exactly the simple zeros of `S`, so every residual zero has
exactly `2n` separated transverse active events.  For `n=2` this gives
exactly four events before R10 is applied.  The first and last punctured
cells have `S<0`, and strict interlacing excludes any interior joint zero.
There is no hidden premise-completeness or reflection assumption.

### 2.4 Terminal event-pair softness

At the terminal joint zero, the base quadratic coefficient
`p^2-mu^2r^2` is strictly negative and
`partial_q S^c(q_0,L)=0` because both base positions vanish.  Smoothness of
the retained final `rho_-` chamber therefore gives

```text
S^c(q,L+x)<=-c x^2+C(|delta||x|+delta^2),
delta=q-q_0.
```

Choosing `K` large makes the chamber sign strictly negative outside the
window `|x|<K|delta|`.  Transverse internal events persist, so the actual
relay and chamber trajectories agree up to the left edge of that window.
Inside it, positions are `O(|delta|)`.  Even an `O(1)` material mismatch is
therefore multiplied by `U,V=O(|delta|)` for only `O(|delta|)` time.
Variation of constants/Gronwall gives velocity error `O(delta^2)` and
position error `O(|delta|^3)`.

The nonzero terminal slopes keep each component monotone through the
window.  Taking `K` strictly larger than the uniform first-order zero-time
displacement bounds leaves the chamber boundary values of order
`|delta|`, so the cubic position error preserves their signs and the scalar
zero indices.  Hence each actual zero differs from its chamber zero by at
most `O(delta^2)` (indeed the estimates allow the stronger cubic order),
and

```text
A_n(mu,q)=A_n^c(mu,q)+O((q-q_0)^2).
```

Thus their first derivatives agree even when a terminal positive-material
event pair is born or dies.  The argument uses the min terminal material
`rho_-=R` in the restricted theorem and is not an unsupported generic
hybrid-flow smoothness assertion.

### 2.5 Negative orientation, at-most-one, and reflection

The oriented-zero lemma is correct for either sign.  Applying it to
`g=sigma A_n`, a positive derivative at each zero forces `g<0` immediately
to the left and `g>0` immediately to the right; two such oriented zeros on
one interval are impossible.  For the restricted min theorem, trusted R10
gives `partial_q A_2^c<0`, terminal softness transfers the derivative to
the global map, and `sigma=-1` gives the required positive orientation.

For a root with terminal slopes `p,r`, nodal parity and energy give
`r/p<-1`, so `q#=|r|/|p|>1`.  The positively reoriented time reflection
has the same relay sign, the same nodal indices, and hence produces another
zero of the same global residual.  At-most-one forces `q#=q`; global IVP
uniqueness then fixes the whole reflected trajectory.  Reflection is used
only after, not inside, the local-sign or completeness proof.

## 3. Boundary audit: PASS

- Every finite `R>1` is covered.  The strict boundaries `R=1`, `mu=1`, and
  `q=1` are explicitly excluded.
- The unconditional statement is restricted to min `n=2,mu=2`; arbitrary
  `n,mu` and either orientation occur only in the conditional implication.
- The `n=2` endpoint case uses two genuine `U` nodal cells and yields four
  crossings directly; it invokes no nonexistent middle-cell induction.
- Nonzero grazing and sliding are excluded by negative energy.  Interior
  joint collisions and terminal pair closures are retained as negative-side
  contacts rather than silently discarded.
- No root existence, endpoint sign as `q->1+` or `q->infinity`, equal-norm
  conclusion, general min twist, `n>2` min result, or O3a conclusion is
  claimed.
- Arbitrary asymmetric roots lie in the proof and in trusted R10's scope;
  reflection is a derived conclusion.

## 4. Adversarial audit: PASS

- **Wrong min material:** the proof uses `rho_-` at the initial and terminal
  contacts and specializes it to `R`; no max-law label is imported.
- **Invalid global zero:** Sturm indexing and the strict quotient argument
  independently force all four transverse events before R10 is used.
- **Fixed-word globalization:** compactness and relay uniqueness construct
  the global map; a fixed chamber enters only for the derivative at a root.
- **Closure derivative:** the `O(delta^2)` comparison proves, rather than
  presumes, equality of the global and chamber first derivatives.
- **Derivative sign reversal:** the proof applies the zero lemma to
  `-A_2`; it never reuses the positive max orientation.
- **Reflection circularity:** neither the R10 input nor automatic premise
  completeness assumes reflection.
- **Scaling mismatch:** the reflected pair has common scale `|p|^-1`, so
  `S` is multiplied by one positive factor and the initial slope quotient
  is exactly `q#`.
- **Scope inflation:** the arbitrary-`n,mu` result remains conditional and
  no existence or equal-integral statement is inferred.

The author self-audit was used only as a checklist after the derivation was
independently rederived.  It contains no extra premise needed to repair the
proof.

## 5. Obligation map and final verdict

```text
either-orientation global relay IVP and continuity:       PASS
automatic 2n-event completeness of every residual zero:  PASS
terminal first-variation transfer:                        PASS
oriented-zero lemma for either derivative sign:           PASS
conditional fixed-mu global order and reflection:         PASS

restricted min n=2, mu=2 local negative twist:            TRUSTED INPUT
restricted min n=2, mu=2 global at-most-one:               PASS
restricted min n=2, mu=2 reflection fixing:               PASS

definition audit:                                         PASS
logic audit:                                              PASS
boundary audit:                                           PASS
adversarial audit:                                        PASS
blocking_findings:                                        []
major_findings:                                           []
verdict:                                                   APPROVE
```

The proof package is suitable for a proposal carrying exactly the two
candidate statements frozen in the derivation.  This audit does not itself
submit, integrate, or mutate canonical files.
