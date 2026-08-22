# Approach registry

Run: R-20260822T220000Z-b3-baseline

## Route cards

### R1: Ratio finite bang-bang reduction (STRICT partial result achieved)

- Route ID: R1
- Family: variational / saturation
- Core mechanism: Feynman-Hellmann for the ratio functional, exact zero-count of `H = u_n^2 - u_{n+1}^2` via Wronskian monotonicity, ratio energy invariant `E = b E_n - a E_{n+1}` forcing `q0 = 1/c`, `q1 = -1/c`.
- Target obligation: O1 partial.
- Status: `PROVED` as a structural theorem; full O1 still `BLOCKED` on the finite optimization.
- Exact gap: switch positions/block lengths not determined; global maximum value not closed.

### R2: Exact 2n-root count for alternating secular polynomial (STRICT PROVED)

- Route ID: R2
- Family: transfer-matrix recurrence / Chebyshev-Jacobi matrix
- Core mechanism: `F_n` satisfies `G_n = tau G_{n-1} - G_{n-2}`; in the square variable `x=C^2`, `P_n(x)=U_n(t)+1/s U_{n-1}(t)`; this is the characteristic polynomial of a finite Jacobi matrix whose eigenvalues all lie in `(-2,2)`, giving `n` roots in `(0,1)` and hence `2n` roots in `(0,pi)`.
- Target obligation: O3.
- Status: `PROVED` (STRICT).
- Exact gap: none for O3.
- Next action: write formalization scaffold (not required by this run); use result in O2/O4.

### R3: Alternating-family one-dimensional monotonicity

- Route ID: R3
- Status: UNEXPLORED
- Exact gap: open.
- Next action: use R1/R2 tools.

### R4: Direct Keller-type reduction to value

- Route ID: R4
- Status: PARTIAL (after R1); exact global extremality still open.
- Exact gap: prove that the optimized `[1,R,1,...,1]` bang-bang configuration has equal block widths and value `c_n(R)`.

### R5: Disprove/find counterexample

- Status: EVIDENCE supporting conjecture; no counterexample found.
