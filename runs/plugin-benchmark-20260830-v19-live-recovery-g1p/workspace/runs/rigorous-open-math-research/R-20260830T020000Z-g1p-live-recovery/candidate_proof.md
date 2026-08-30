RIGOROUS_PARTIAL_RESULT

# Candidate partial proof package

This synthesis is pending fresh independent audit. It claims only the strict
partial statements below, not `KP-DET`, `KO-DET`, or global G1 prime.

## Contract

Work on the prescribed finite-interior n=2 symmetric INF branch. The target is
negative definiteness of the normalized two-by-two matrices `Kp_odd(R)` and
`Ko(R)` for every finite `R>1`.

## P1. Inertia reduction

Near `R=1`, each sector matrix is strictly negative definite. Along a connected
continuous branch, a positive determinant prevents either eigenvalue from
crossing zero. Therefore determinant positivity for a sector preserves its
negative inertia and makes its trace inequality automatic. Evidence:
`direct_attempt.md`.

## P2. Exact semiseparable reduction for the odd sector

With the notation fixed in `route-01-spectral-coercivity/derivation.md`, the
two-point Green difference satisfies the exact congruence-normalized identity

```text
U^(-1) H U^(-1) = [[a,b],[b,b]],
```

and `b>0`. After the diagonal penalty congruence, `Kp_odd<0` is equivalent to
negative definiteness of

```text
M = [[a-gamma_1,b],[b,b-gamma_2]].
```

At a first singularity, double zero is impossible and the only remaining
scalar alternative is

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b).
```

Evidence: the W1 route report and derivation.

## P3. Exact Jacobi and transfer realization

For a reflection-transverse switch displacement `y`, the half-string Jacobi
fields satisfy the exact residual derivative

```text
dot(F)_trans = -tau Kp_odd y.
```

Equivalently, `Kp_odd y=0` is a parity-crossing half-string Jacobi field with
the two moving-level boundary conditions written in the W2 derivation. In
reflection-adapted transfer coordinates,

```text
D_(p,q) A = -tau Kp_odd E,
det D_(p,q) A = -tau^2 det Kp_odd.
```

The odd-sector off-diagonal entry is strictly positive at every finite
interior branch point. Hence a first loss cannot be the zero matrix; it is
corank one with strictly negative diagonals and a same-sign kernel vector.

If `Ko` is nonsingular at that point, the symmetric branch remains analytic
through the odd-sector singularity because

```text
D_(a,b) S = -tau E Ko.
```

This chart does not invert the singular full Jacobian. Evidence: the W2 route
report and derivation.

## Exact open obligations

1. Exclude the one-dimensional same-sign Jacobi kernel, equivalently prove the
   forbidden crossing-form sign or rule out the W1 scalar branch equality.
2. Treat the exceptional possibility that `Kp_odd` and `Ko` are singular at
   the same finite-interior point.
3. Prove or refute `KO-DET` on the all-finite-R branch.

No numerical result appears in this package. The full target remains open.
