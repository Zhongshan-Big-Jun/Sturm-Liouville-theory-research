RIGOROUS_PARTIAL_RESULT

# Compact-contrast exclusion strip for asymmetric minimum roots near `mu=2`

## 0. Theorem

Fix a compact finite-contrast interval

```text
K=[1+eta,M],                 eta>0, M<infinity.       (0.1)
```

For the minimum saturation law the following hold.

1. There is `delta_2(K)>0` such that, for every `R in K`, every
   premise-complete min-self-consistent four-switch point whose relay
   frequency satisfies `|mu-2|<delta_2(K)` is reflection invariant.
2. For every fixed integer `n>=3`, there is `delta_n(K)>0` such that no
   premise-complete min-self-consistent `2n`-switch point with `R in K`
   satisfies `|mu-2|<delta_n(K)`.

No existence or uniqueness assertion is made.  The widths may depend on
`n,eta,M`; no effective lower bound is claimed.

The physical theorem is a specialization of the following reusable anchor
lemma.  Fix `n`, one relay sign, `K`, and `mu_0>1`.  If every
self-consistent root over `K` with frequency `mu_0` is reflection fixed and
has `partial_q A_n!=0`, then some uniform neighborhood of `mu_0` contains
only reflection-fixed self-consistent roots.  If there is no root at
`mu_0`, some uniform neighborhood contains no self-consistent root.

## 1. Trusted inputs and continuity facts

The proof uses exactly these accepted results.

- `CLM-NGE2-MPO3A-PROPERNESS`: for fixed `n` and `K`, the full set of
  min-self-consistent switch vectors is compact in the open switch simplex,
  with every cell length uniformly positive.
- `CLM-NGE2-MPO3A-FULL-RELAY`: each such point has continuous relay
  coordinates `(mu,q,L)` and a premise-complete event-transverse
  common-terminal trajectory.
- `CLM-NGE2-MPO3A-SYMPLECTIC-NESTED`: reflection preserves `R,mu,L`, norm
  equality, event count, and the minimum sign class, sends `q` to
  `q^sharp`, and has `q^sharp=q` exactly at a reflection-fixed trajectory
  after positive reorientation.
- `CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10`: at every `n=2,mu=2`
  premise-complete common-terminal minimum root, `partial_q A_2<0`.
- `CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11`: at fixed finite `R` and
  `mu=2`, the global common-terminal residual has at most one root, and that
  root is reflection fixed.
- `CLM-NGE2-MPO3A-MIN-MU2-NGE3-NONEXISTENCE-R15`: for `n>=3` there is no
  premise-complete minimum common-terminal root at `mu=2`, even before norm
  equality is imposed.

For completeness, the continuity used below is internal to these inputs.
On the open switch simplex, simple Sturm eigenvalues, normalized modes, their
endpoint derivatives, and hence `(mu,q,L)` depend analytically on `(R,x)`.
Over the compact self-consistent set, the nonzero oriented endpoint
derivative used in the `q` normalization is bounded away from zero, so `q`
is continuous and bounded along every sequence used below.
At an event-transverse relay root the event word is locally constant and
`A_n(R,mu,q)` is analytic.  Properness prevents the limiting sequence below
from reaching a switch collision or endpoint cell of zero length.

## 2. General compact anchor-slice lemma

Suppose first that every self-consistent root over `K` on the slice
`mu=mu_0` is reflection fixed and has `partial_q A_n!=0`.  If no uniform
reflection strip existed, asymmetric roots `(R_k,x_k)` with
`mu_k->mu_0` could be chosen.  Properness gives an interior
self-consistent limit `(R_*,x_*)` on the anchor slice.  By hypothesis it is
reflection fixed and its local common-terminal residual has nonzero
`q` derivative.  The implicit-function theorem therefore gives at most one
nearby common-terminal `q` root for each `(R,mu)` (in the relative
`R>1` parameter neighborhood if `R_*` is an endpoint of `K`).  But an asymmetric
`x_k` and its reflection have the same `(R_k,mu_k)`, distinct `q`
coordinates, and both converge to the fixed root's `q` coordinate.  This is
a contradiction.

If the anchor slice contains no self-consistent root and roots with
`mu_k->mu_0` existed, properness would directly produce a root on the
anchor slice, also a contradiction.  This proves both forms of the general
lemma.  Notice that the derivative hypothesis is only imposed at
self-consistent anchor roots, not at every common-terminal root away from
the slice.

## 3. The `n=2` reflection strip

Assume the first assertion is false.  Then for every positive integer `k`
there is an asymmetric min-self-consistent four-switch point `x_k` such that

```text
R_k in K,                  |mu_k-2|<1/k.             (2.1)
```

Properness gives a subsequence, not relabeled, with

```text
R_k -> R_* in K,          x_k -> x_*                 (2.2)
```

inside the open switch simplex.  Closedness of the analytic
self-consistency equations and continuity of relay coordinates show that
`x_*` is a premise-complete min-self-consistent point with `mu_*=2`.

Let its relay coordinate be `q_*`.  Trusted R11 says that the
`n=2,mu=2` common-terminal root at `R_*`, if present, is unique and
reflection fixed.  Thus `x_*` is reflection invariant.  Trusted R10 gives

```text
partial_q A_2(R_*,2,q_*)<0.                          (2.3)
```

Transversality fixes one local relay chamber, so the implicit-function
theorem applied to (2.3) gives a neighborhood `N` of `(R_*,2,q_*)` in which
the common-terminal equation

```text
A_2(R,mu,q)=0                                         (2.4)
```

has at most one `q` for each nearby pair `(R,mu)`.

Reflect `x_k`.  By trusted `CLM-NGE2-MPO3A-SYMPLECTIC-NESTED`, asymmetry
implies that its reflected relay coordinate `q_k^sharp` differs from `q_k`;
reflection preserves `R_k,mu_k`, the common terminal, norm equality, and all
premise predicates.  From (2.2) and reflection continuity,

```text
q_k -> q_*,                 q_k^sharp -> q_*.         (2.5)
```

For large `k`, both distinct roots `(R_k,mu_k,q_k)` and
`(R_k,mu_k,q_k^sharp)` lie in `N`, contradicting local uniqueness in (2.4).
This proves the first assertion.

## 4. The `n>=3` empty strip

Fix `n>=3` and suppose the second assertion is false.  There are
min-self-consistent `2n`-switch points `x_k` with `R_k in K` and
`mu_k->2`.  Properness again gives an interior limit `(R_*,x_*)` in the
same complete self-consistent class.  Relay-coordinate continuity makes
`x_*` a premise-complete minimum common-terminal root with `mu=2`.  This
contradicts trusted R15, which excludes such a root even without the norm
equation.  Therefore `delta_n(K)>0` exists.

## 5. Consequence for the global reflection frontier

For every fixed `n>=2` and compact finite-contrast interval `K`, every
asymmetric min-self-consistent point is uniformly separated from `mu=2`:

```text
|mu-2| >= delta_n(K)>0.                              (4.1)
```

For `n=2`, points inside the excluded asymmetric strip may exist but are
forced to be reflection invariant.  For `n>=3`, the entire root set is
absent there.  Thus a counterexample, disconnected asymmetric component,
or symmetry-breaking bifurcation at bounded contrast must occur away from
`mu=2`; it cannot accumulate onto the trusted `mu=2` locus.

This does not settle arbitrary `mu`, does not make `delta_n` uniform in
`n`, and does not control `R->1+` or `R->infinity`.

## 6. Definition, logic, boundary, and adversarial audits

- **Definition audit: PASS.**  The compact set contains only exact
  min-self-consistent points with `2n` effective switches, hence `2n+1`
  positive-length cells, and all relay/norm predicates.  R15 is used on its
  larger common-terminal scope.
- **Logic audit: PASS.**  Compactness is used only to extract an interior
  limit.  The `n=2` contradiction uses a nonzero local `q` derivative plus
  the distinct reflected partner; it does not promote local uniqueness to
  global uniqueness.
- **Boundary audit: PASS.**  `R=1`, unbounded `R`, varying `n`, `mu=1`,
  collapsed cells, and nontransverse words are not included.  The theorem
  is uniform only on (0.1) for one fixed `n`.
- **Adversarial audit: PASS.**  A disconnected asymmetric component is not
  assumed connected to the small-contrast branch.  If such components
  approached `mu=2`, properness would still produce the forbidden/local-
  uniqueness limit, which is why the argument covers them.
- **Vacuity audit: PASS.**  The `n=2` statement is conditional on roots and
  may be vacuous for some `R,mu`; the `n>=3` assertion is genuine uniform
  nonexistence.  Neither is presented as a full global-reflection proof.

```text
general compact anchor-slice lemma:    PROVED
n=2 compact-contrast reflection strip: PROVED
n>=3 compact-contrast empty strip:      PROVED
effective strip width:                  NOT PROVIDED
arbitrary-mu global reflection:         OPEN
unresolved_obligations:                 []
```
