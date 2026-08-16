CANDIDATE_COMPLETE_PROOF

# R15 problem contract: minimum-law `mu=2`, all `n>=3`

## Frozen authority and epistemic boundary

Context: `CTX-DEFAULT`.

```text
blueprint sha256:0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799
inventory sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Trusted canonical inputs are limited to:

```text
HYP-NGE2-DOMAIN
  semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5
DEF-NGE2-MPO3A-SELFCONSISTENCY
  semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366
CLM-NGE2-MPO3A-STRUCTURE
  semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-INTERNAL-PHASE-R8
  semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702
```

The frozen candidate route `r13_min_n3_composition_r1` is inspected as
research memory, not treated as canonical truth.  Its one-interface algebra
is rederived and checked in this route.

## Objects and conventions

Fix `R>1`, put `r=sqrt(R)>1`, fix `mu=2`, and let `n>=3` be an integer.
Consider a strict, premise-complete, transverse, common-terminal full-relay
trajectory obeying the minimum saturation law and having exactly `2n`
events.  Write the event times as

```text
tau_1<...<tau_(2n)
```

and the `2n-1` internal cells as `I_j=(tau_j,tau_(j+1))`.  The accepted
allocation is odd-positive/even-negative.  Put

```text
A_i=U(tau_i) != 0,
z_j=A_(j+1)/A_j,                1<=j<=2n-1,
x_j=tan(theta_j/2),             j odd,
y_j=tan(theta_j/2),             j even.
```

The sharp phase theorem gives

```text
0<x_j<1/sqrt(3)<y_j<1.
```

For a physical positive cell followed by a negative cell, define
`a(x,y,r)` and `b(x,y,r)` to be its two consecutive event-amplitude ratios,
with the shared interface amplitude normalized to one.

## Quantified target

Prove:

> For every finite `R>1` and every integer `n>=3`, there is no strict,
> premise-complete, transverse, common-terminal `mu=2` full-relay root obeying
> the minimum law and having `2n` events.

Equivalently, the strict physical premise set for the minimum-law local
inertia/twist assertion is empty for `mu=2,n>=3`.

## Required proof obligations

1. Reconstruct the local positive-negative interface amplitudes from both
   momentum equations and verify the physical contraction `0<a<1`.
2. Check the negative-positive orientation by actual time reversal, not by
   a pictorial symmetry assertion.
3. For an arbitrary `2n-1` internal word, derive the exact amplitude-ratio
   equations with correct indices.
4. Show that at least one internal positive cell is flanked by negative
   cells for every and only `n>=3`, and that its two descriptions are
   incompatible with contraction.
5. Audit the endpoint cells, reflection, global sign, strict boundaries,
   and the exceptional case `n=2`.

## Forbidden substitutes

- finite enumeration in place of the arbitrary-`n` proof;
- treating the R13 candidate package as a canonical premise;
- assuming reflection symmetry;
- changing the minimum law to the maximum law;
- replacing a time-reversed ratio by the same forward ratio without taking
  its reciprocal;
- using endpoint or norm equations to hide an inconsistent internal word;
- floating-point evidence or a bounded no-root search as proof.

## Completion condition

A complete candidate proof must give a symbolic arbitrary-index
compatibility identity and a standalone exact contraction proof, with no
unresolved mathematical obligation.  Promotion beyond candidate status
requires a separate uninvolved four-part audit bound to the frozen package.

