RIGOROUS_PARTIAL_RESULT

# R9 min complementary-inertia problem contract

## Frozen target

Fix finite `R>1`, integer `n>=2`, and an arbitrary possibly asymmetric
premise-complete transverse common-terminal **min** full-relay trajectory with
`m=2n` events.  For its accepted physical event matrix

```text
M=D+B^T K^(-1)B,
D=diag(a_1,...,a_m)>0,
sign K_i=(-1)^(i+1),  1<=i<m,
```

prove or refute

```text
n_-(M)>=n-1.                                           (T)
```

The accepted one-sided estimate `n_-(M)<=n-1` then makes `(T)` equivalent to
`In(M)=(n+1,n-1,0)`, hence to `det(L_-)>0`, `J<0`, and negative fixed-`mu`
local min twist.  This contract does not claim global root order or O3a.

## Quantifiers and boundary cases

The order is: every finite `R>1`; every integer `n>=2`; every complete
transverse min root, including asymmetric roots and every premise-complete
relay chamber.  The proof must cover `n=2` and both terminal cells.  Grazing,
colliding events, `R=1`, `mu=1`, incomplete relay words, and non-simple
terminal zeros are outside this local theorem and require separate closure
arguments.

## Bound canonical snapshot and trusted inputs

```text
context_id: CTX-DEFAULT
blueprint_sha256:
  sha256:1c4c526e88a8f1e86940619859eb02dbb4fc6bca695f55e0bd29c5935c88c5b7
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f

HYP-NGE2-DOMAIN
  semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5
CLM-NGE2-MPO3A-STRUCTURE
  semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-CELL-PHASE-R6
  semantic-sha256:34ddfc0ec931503621e7658d7186318b41b3f910214000e23c55bae7aaac040e
CLM-NGE2-MPO3A-HYBRID-TWIST-R6
  semantic-sha256:6e2749fd147662212ade344e6dec0a715a83e76cb954e031134748a99a134b7b
CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7
  semantic-sha256:5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee
```

## Candidate-only input and forbidden substitutes

`../r8_phase_variation/derivation.md` is an independently audited but, at
route start, not-yet-canonical R8 candidate.  Its internal threshold

```text
odd i: theta_i<pi/(mu+1),
even i: theta_i>pi/(mu+1)
```

may be used only as an explicitly conditional candidate premise until a new
snapshot shows deterministic integration.  Finite positive pivots, symmetric
samples, coefficient signs, palindromy, and a lemma equivalent to `(T)` are
forbidden proof substitutes.

## Completion conditions

Return one of: (i) a complete exact proof of `(T)` with definitions, logic,
boundary, and adversarial audits; (ii) a premise-complete certified physical
root violating `(T)`; or (iii) a precise strictly weaker lemma, first invalid
step, and minimal restart condition.  Only new route artifacts may be written;
no proposal or canonical file is changed here.

## Snapshot transition after deterministic R8 integration

During this route the bound snapshot became stale because the independently
reviewed R8 proposal was deterministically integrated.  All later retrievals
are rebound to

```text
blueprint_sha256:
  sha256:89e3f916c86cc81ec53b49b528260f001b9784204e0fe986314acb06c7908429
inventory_sha256:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

At this snapshot `CLM-NGE2-MPO3A-INTERNAL-PHASE-R8` is established and is
therefore a legal trusted premise, with semantic hash
`semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702`.
The route retains the earlier snapshot only as chronological provenance and
does not mix query results across the two snapshots.
