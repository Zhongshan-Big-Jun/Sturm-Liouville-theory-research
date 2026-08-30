---
title: n=2 symmetric INF odd-sector first-zero reduction
status: STRICT partial, independently audited PASS
source_run: R-20260830T020000Z-g1p-live-recovery
---

# n=2 symmetric INF odd-sector first-zero reduction

## Status

`RIGOROUS_PARTIAL_RESULT`. The structural statements below passed a fresh
independent audit. `KP-DET`, `KO-DET`, and global `G1'` remain open.

## Strict reduction

On the prescribed finite-interior n=2 symmetric INF branch, the normalized odd
sector admits an exact two-point Green reduction. With the notation of the run,

```text
U^(-1) H U^(-1) = [[a,b],[b,b]],
b>0.
```

After the diagonal-penalty congruence, the sector is controlled by

```text
M = [[a-gamma_1,b],[b,b-gamma_2]].
```

A first determinant zero cannot be a double zero. Its only remaining scalar
alternative is

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b).
```

The associated kernel vector has entries of the same sign.

## Jacobi realization

For a reflection-transverse switch displacement `y`, the exact half-string
Jacobi response satisfies

```text
dot(F)_trans = -tau Kp_odd y,
D_(p,q) A = -tau Kp_odd E.
```

Thus the remaining first zero is exactly a one-dimensional Jacobi kernel with
two moving-level conditions. The strict off-diagonal sign
`(Kp_odd)12>0` excludes `Kp_odd=0`. If `Ko` is nonsingular, the symmetric branch
can be parameterized through an odd-sector singularity by

```text
D_(a,b) S = -tau E Ko,
```

without using the singular full Jacobian inverse.

## Applicability

- Exact n=2 symmetric INF branch with finite interior switches.
- Compact-middle first-zero analysis between the strict near-one and accepted
  large-R anchors.
- Useful for combining spectral Green estimates with branch transversality.

## Non-applicability and open obligations

- Does not treat non-symmetric roots or global branch construction.
- Does not exclude the remaining one-dimensional same-sign Jacobi kernel.
- Does not treat simultaneous singularity of `Kp_odd` and `Ko`.
- Does not prove `KO-DET`.
- Numerical evidence is neither used nor needed for the strict partial result.

## Artifacts

- Candidate package:
  `runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace/runs/rigorous-open-math-research/R-20260830T020000Z-g1p-live-recovery/candidate_proof.md`.
- Independent audit: sibling `independent_audit.md`, verdict `PASS`.
- Lean scaffold: `lean-proof/SL/KpOddFirstZero_Scaffold.lean`, Tier 0 only.
