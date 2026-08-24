# Obligation graph

## Root objective (OBJ)

Prove or disprove: for all `n >= 1` and `R > 1`, `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, all simple.

## Nodes and dependencies

```
OBJ
 |
 +-- O1  det(C_s)=1 and D = E C_s E^{-1} is determinant-one with explicit form
 |        status: COMPLETE
 |
 +-- O2  Q_{n,s}(x) = U_n(u) + s^{-1} U_{n-1}(u), u = alpha x^2 - beta
 |        depends on O1
 |        status: COMPLETE
 |
 +-- O3  P_n(u) = U_n(u) + lambda U_{n-1}(u), lambda=s^{-1} in (0,1],
 |        has exactly n simple zeros in (-1,1)
 |        depends on O2
 |        status: COMPLETE
 |
 +-- O4  Each P_n root gives exactly two simple x-roots in (-1,1), and
 |        no other x-roots exist; therefore G has exactly 2n simple zeros in (0,pi)
 |        depends on O2, O3
 |        status: COMPLETE
 |
 +-- O5  Special audits: n=1, y=0, y=pi, y=pi/2, R=1
 |        depends on O4
 |        status: COMPLETE
 |
 +-- O6  External-theorem hypothesis check (Cayley-Hamilton, Chebyshev identities)
 |        status: COMPLETE
```

## Edge labels

- O1 -> O2: matrix conjugation is necessary for `E C^n = D^n E`.
- O2 -> O3: the polynomial `P_n` is exactly the reduced problem in the `u` variable.
- O3 -> O4: root locations in `u` must be transferred back to `x`.
- O4 -> O5: the final root-count claim must be audited at boundaries and special points.

## Status

All obligations are closed. No open load-bearing obligations remain.
