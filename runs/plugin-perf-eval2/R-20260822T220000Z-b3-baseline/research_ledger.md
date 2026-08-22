# Research ledger

Run: R-20260822T220000Z-b3-baseline

## Conventions

- Each entry: UTC time, action, result, evidence status, next.
- Numerical evidence is labeled `EVIDENCE`; STRICT results are labeled `STRICT`.

## 2026-08-22T22:20Z

- Read problem statement, required docs, tools, and op02 scripts.
- Recorded existing status: B1 SOLVED, B3 PARTIAL, gap-side exact 2n-switch theorem STRICT.
- Key observation: gap-side switching function is `F_gap = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2`; ratio derivative yields `H = u_n^2 - u_{n+1}^2`.
- This suggests a new ratio-side finite bang-bang reduction distinct from the existing gap theorem.

## 2026-08-22T22:35Z

- Derived and wrote STRICT structural theorem for ratio maximizers:
  - Every global ratio maximizer is bang-bang `[1,R,1,...,1]` with exactly `2n` switches.
  - Proof uses FH derivative `d(b/a) = (b/a) int h H`, saturation, Wronskian zero-count, and a ratio energy invariant `E = b E_n - a E_{n+1}` giving `E=0` and `q0=1/c`, `q1=-1/c`.
- Registered in `candidate_proof.md`.
- Numeric EVIDENCE: `q0=1/c`, `q1=-1/c` on alternating maximizers for R=2,4,10, n=1..5; E approximately constant; H has `2n` interior zeros when endpoint artifacts excluded.
- Follow-up: The full problem is reduced to optimizing over `[1,R,1,...,1]` bang-bang with `2n` switch positions.

## 2026-08-22T23:00Z

- Found a transfer-matrix recurrence `G_n = tau G_{n-1} - G_{n-2}` for the alternating secular function.
- In the square variable `x=C^2`, the polynomials satisfy a Chebyshev-like recurrence.
- Proved STRICT:
  - `P_n(x) = U_n(t) + (1/s) U_{n-1}(t)`, `t = (A x - B)/2`;
  - this is the characteristic polynomial of a finite Jacobi matrix with one negative boundary diagonal;
  - all its roots are real and lie in `(-1,1)` in the t variable;
  - therefore `Q_n(C)` has exactly `2n` roots in `(-1,1)`, and `F_n(y)` has exactly `2n` roots in `(0,pi)`.
- This closes O3. Registered in `candidate_proof.md`.
- Symbolic verification of the recurrence `G_n = tau G_{n-1}-G_{n-2}` for n=2..5: PASS.
- Numeric verification of the closed form `P_n=U_n+1/s U_{n-1}` for s=3, n=1..6: machine precision.
- Remaining: O1 full (equal widths/value), O2 monotonicity.
