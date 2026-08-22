# Counterexample log

Run: R-20260822T220000Z-b3-baseline

## Tested claims

1. Ratio maximizer structure theorem: no counterexample found.
   - Tested numerically on alternating maximizers `n=1..5`, `R=2,4,10`;
     all had `q0=1/c`, `q1=-1/c`, `2n` H zeros.
2. 2n-root count: no counterexample found.
   - Recurrence and closed form match machine precision for `n=1..6`;
     matrix eigen check confirms Jacobi spectrum in `(-2,2)` for `delta<=1`.
3. Alternating-family monotonicity (O2): no counterexample found.
   - Probed `n=2,3`, `R=4,10`, `r` values on both sides of `sqrt(R)`;
     peak near `sqrt(R)`, H residuals negative below and positive above.

## Tested edge cases

- `R=1` excluded by contract; recurrence still would work with `delta=1` but
  `B/2=1`, the affine interval degenerates and the root count would need
  endpoint handling.
- `n=1` checked; formulas reduce correctly.
- `n=5` high index checked numerically (not part of proof).
