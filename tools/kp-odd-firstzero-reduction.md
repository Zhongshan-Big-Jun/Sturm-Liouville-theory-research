---
title: n=2 symmetric INF odd-sector first-zero reduction
status: STRICT partial, independently audited PASS
source_run: R-20260831T020156Z-g1p-kpdet
predecessor_run: R-20260830T020000Z-g1p-live-recovery
---

# n=2 symmetric INF odd-sector first-zero reduction

## Status

`RIGOROUS_PARTIAL_RESULT`. The structural statements below and the 2026-08-31
pivot and phase refinement passed fresh independent audits. `KP-DET`,
`KO-DET`, and global `G1'` remain open.

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

## Global pivot and Schur frontier

The final-layer phases give a strict sign at every finite-interior branch
point, without first assuming a singularity. Put

```text
k_j=sqrt(lambda_j R),
theta_j=k_j(L-b),
c=k_2/k_3,
tau=R-1.
```

Then `0<theta_3<pi/2`, `theta_2=c theta_3`, and the exact Green quotient
calculation gives

```text
gamma_2-b_0=2/[v(b)^2 k_3]
  {R/tau[tan(theta_3)+c cot(theta_2)]
   -[sin(theta_3)cos(theta_3)
     +c sin(theta_2)cos(theta_2)]}>0.
```

The strict inequality follows from `R/tau>1` and the two elementary positive
gaps

```text
tan(t)-sin(t)cos(t)=sin(t)^3/cos(t),
cot(t)-sin(t)cos(t)=cos(t)^3/sin(t).
```

Consequently the lower-right pivot is globally negative and

```text
det Kp_odd>0
  iff S_KP=a_0-gamma_1+b_0^2/(gamma_2-b_0)<0.
```

This is a lossless all-finite-interior reduction, not a proof that the final
inequality holds.

## Exact phase frontier

The transfer route eliminates every Green kernel, Wronskian, and eigenfunction
amplitude. On its exact five-phase spectral, band, mass, and mode-index system,

```text
S_KP<0 iff Phi<0,
S_KP=0 iff Phi=0,

Phi=Dtheta[X(D-c s N/C)-Dalpha]+X^2 Ttheta^2/C^2.
```

All cleared denominators are strictly positive and the phase equations
reconstruct the normalized branch point. The exact definitions of
`Dtheta,X,D,s,N,C,Dalpha,Ttheta` are frozen in the W1 derivation named below.

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

For a hypothetical same-sign kernel, the quotient fields satisfy the common
projective-flux law

```text
v^2(phi/v)'=w^2(psi/w)'=P.
```

The flux is constant on each of the three layers and the difference
`h=v psi-w phi` has exactly one simple downward zero before the unique zero of
`w`. Its locking integral increases from zero to infinity, so pure Sturm
quotient monotonicity always realizes one locking point and cannot exclude the
kernel. This closes that route as a reusable negative result. The endpoint
impulse ratio is exactly

```text
y_1 v(a)^2/[y_2 v(b)^2]=(gamma_2-b_0)/b_0>0.
```

## Applicability

- Exact n=2 symmetric INF branch with finite interior switches.
- Compact-middle first-zero analysis between the strict near-one and accepted
  large-R anchors.
- Useful for combining spectral Green estimates with branch transversality.

## Non-applicability and open obligations

- Does not treat non-symmetric roots or global branch construction.
- Does not exclude the remaining one-dimensional same-sign Jacobi kernel.
- The exact remaining scalar obligation is `Phi<0` on the complete five-phase
  constraint set, or an admissible exact tuple with `Phi=0`.
- Does not treat simultaneous singularity of `Kp_odd` and `Ko`.
- Does not prove `KO-DET`.
- Numerical evidence is neither used nor needed for the strict partial result.

## Artifacts

- Candidate package:
  `runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace/runs/rigorous-open-math-research/R-20260830T020000Z-g1p-live-recovery/candidate_proof.md`.
- Independent audit: sibling `independent_audit.md`, verdict `PASS`.
- Lean scaffold: `lean-proof/SL/KpOddFirstZero_Scaffold.lean`, Tier 0 only.
- 2026-08-31 candidate and audit:
  `research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/`.
- Exact phase derivation: sibling `route-01-transfer-schur/derivation.md`.
- Exact Jacobi derivation: sibling `route-02-jacobi-falsifier/derivation.md`.
- New Lean scaffold:
  `research/runs/R-20260831T020156Z-g1p-kpdet/workspace/lean-proof/SL/KpDetPhaseReduction_Scaffold.lean`, Tier 0 only.
