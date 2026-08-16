CANDIDATE_COMPLETE_PROOF

# R15 append-only research ledger

## Entry 001: problem freeze and trusted retrieval

The all-`n` target and its strict physical scope were frozen.  A deterministic
snapshot returned canonical SHA-256 values
`0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799` and
`b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
The trusted relay, structure, and internal-phase nodes were retrieved with
snapshot binding.

## Entry 002: transferred candidate and falsification target

The R13-R1 `mu=2,n=3` contraction was treated as a candidate pattern.  The
fast falsification target was whether a left negative-positive interface
uses `a`, `1/a`, `b`, or `1/b` for the positive-cell ratio once actual time
orientation and event indices are restored.

## Entry 003: arbitrary-index reconstruction

Let `z_j=A_(j+1)/A_j`.  A forward positive-negative pair at cells `(j,j+1)`
gives `(z_j,z_(j+1))=(a,b)`.  Reversing a physical negative-positive pair at
cells `(j-1,j)` gives `(1/z_j,1/z_(j-1))=(a,b)`.  Hence every internal odd
cell satisfies

```text
a(x_j,y_(j-1),r)*a(x_j,y_(j+1),r)=1.
```

For `n>=3`, `j=3` is always available.  This identifies a direct general
proof rather than an induction hypothesis.

## Entry 004: boundary and exception check

The argument uses no endpoint-cell phase estimate and no global norm
equation.  They are additional constraints on an already empty internal
system.  The case `n=2` has no odd internal cell with two negative neighbors,
so the argument correctly stops there.  Reflection preserves parity because
`j -> 2n-j`, and global sign reversal leaves every `z_j` unchanged.

## Entry 005: exact certificate

The exact checker independently reconstructs `a,b`, the natural-coordinate
contraction identities, forward and reversed ratio tables, and all indices
for `2<=n<=12`.  The finite index table is an adversarial check only; the
universal conclusion is supplied by the symbolic proof in `derivation.md`.

