---
title: Krein power-domain polynomial obstruction
tags: [mathtool, self-developed, left-definite, operator-domain, krein-boundary]
source: Pilot v6 Arm A, independently audited blind proof
status: STRICT
created: 2026-08-28
---

# Krein power-domain polynomial obstruction

## Strict theorem

Let `K_c=-D^2+c`, where `c>0`, on `[-1,1]` with Krein boundary conditions

```text
f'(1)=f'(-1)=(f(1)-f(-1))/2.
```

Put `L=c-D^2`. For the algebraic polynomial inverse `L_poly^(-1)`, define

```text
Q_n^(2r)=L_poly^(-r) P_n,
Q_n^(2r+1)=L_poly^(-r) R_n,
```

where `P_n` is the degree `n` `L^2` orthogonal polynomial and `R_n` is the degree `n`
Krein-form orthogonal polynomial. Then, for every integer `s>=4`,

```text
Q_n^(s) in D(K_c^(s/2)) if and only if n in {0,1}.
```

This is a strict, independently audited theorem. It distinguishes the algebraic inverse of the
differential expression on polynomials from the genuine self-adjoint operator inverse.

## Proof mechanism

Define

```text
B(f)=(f'(1)-Delta(f)/2, f'(-1)-Delta(f)/2).
```

The Krein form satisfies

```text
a_0(f,f)=integral |f'|^2-|Delta(f)|^2/2 >= 0,
ker(a_0)=span{1,x}.
```

For a polynomial `p`, exact power-domain recursion gives

```text
p in D(K_c^(s/2))
if and only if
B(L^j p)=0 for 0<=j<floor(s/2).
```

If `v=L_poly^(-1)P_n` and `v in D(K_c)`, then `K_cv=P_n`. Orthogonality of `P_n`
to `P_n-cv=-v''` yields

```text
0=||K_0v||^2+c a_0(v,v).
```

Thus `v` is affine, which contradicts degree preservation when `n>=2`. In the odd case,
Krein-form orthogonality of `R_n` gives `a_0(R_n,R_n)=0`, again forcing `n<=1`.
The indices 0 and 1 are affine eigenfunctions and belong to every positive power domain.

## Completion and density interface

- The abstract polynomial completion is not canonically identical to `D(K_c^(s/2))` under the
  identity on polynomial representatives. The polynomial `x^2` is an exact witness because it
  violates both endpoint equations.
- The abstract completion and operator domain are naturally unitarily equivalent after a
  boundary-correcting map.
- The literal algebraic-polynomial span contains non-domain elements, so it is not a subspace of
  the operator domain. Its individually admissible named elements span only `span{1,x}`.
- For the genuine operator inverse `K_c^(-r)`, every transported function lies in the appropriate
  power domain and the transported span is dense. These functions are generally not polynomials.

For example,

```text
L_poly^(-1)x^2=x^2/c+2/c^2,
K_c^(-1)x^2=x^2/c+2/c^2-2 cosh(sqrt(c)x)/(c sqrt(c) sinh(sqrt(c))).
```

The hyperbolic correction is exactly what enforces the operator boundary condition.

## Scope and provenance

- Applies to every real `c>0`, every integer `s>=4`, both parities, and every `n>=0`.
- The polynomial degree spectrum remains `deg Q_n^(s)=n` under the algebraic reading.
- It does not classify `span{Q_n} intersect D(K_c^(s/2))`, and it makes no novelty claim.
- Full proof and audits are in
  `runs/three-arm-pilot-v2/pilot-v6-hs-domain/arms/a-plugin/`.

This theorem supersedes the operator-domain interpretation in
`left-definite-orthogonal-systems.md`. The earlier polynomial formulas remain valid only for the
algebraic inverse `L_poly^(-r)` and the corresponding abstract completion.
