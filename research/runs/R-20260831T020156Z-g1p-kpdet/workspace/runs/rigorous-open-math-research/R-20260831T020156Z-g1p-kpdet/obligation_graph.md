# Obligation graph

## Shortest chain

```text
A-NEAR + A-CONT + KP-SCHUR
  => KP-DET
  => Kp_odd remains negative definite.
```

## Nodes

### A-NEAR

- Statement: `Kp_odd` is strictly negative definite for all sufficiently small positive `R-1`.
- Status: `PROVED`, frozen parent premise.

### A-CONT

- Statement: `Kp_odd` is a continuous symmetric matrix path on the prescribed finite-interior branch.
- Status: `PROVED` within the branch contract.

### KP22

- Statement: `(Kp_odd)22<0` at every finite-interior branch point.
- Status: `PROVED` in `direct_attempt.md`.
- Dependencies: exact last-layer phases, `b_0` formula, and Wronskian penalty formula.

### KP-SCHUR

- Statement:

```text
a_0-gamma_1+b_0^2/(gamma_2-b_0)<0
```

at every finite-interior branch point.
- Status: `OPEN`.
- Dependencies: `KP22` gives the positive denominator.
- Verifier note: equality is exactly the remaining same-sign Jacobi kernel.

### KP-DET

- Statement: `det Kp_odd>0` for every finite `R>1` on the branch.
- Status: `BLOCKED` only by `KP-SCHUR` after the endpoint anchors.
- Equivalence: since `(Kp_odd)22<0`, determinant positivity is equivalent to the strict negative Schur complement.

### ROOT

- Statement: KP-DET is decided on the prescribed branch.
- Status: `OPEN`.
- Excluded downstream nodes: KO-DET, non-symmetric roots, and global G1 prime.
