# Audit report

Run: R-20260822T220000Z-b3-baseline

## Scope

Self-audit (no nested subagents per run instructions) of the two STRICT
results recorded in `candidate_proof.md`.

## Part A: ratio extremizer structure

Checks performed:

- Re-derived Feynman-Hellmann ratio derivative; sign matches saturation.
- Re-checked H zero-count ranges with Wronskian monotonicity (`q' < 0`).
- Re-derived ratio energy invariant and verified jump cancellation at H zeros.
- Verified endpoint identities algebraically.
- Numerical cross-check: `q0=1/c`, `q1=-1/c` on alternating maxima.

Findings: no fatal gap. The proof is self-contained modulo cited project
spectral facts (weak-* continuity, nodal/interlacing, FH).

## Part B: 2n-root count

Checks performed:

- Symbolically verified recurrence `G_n = tau G_{n-1} - G_{n-2}` for n=2..5.
- Verified closed form `P_n = U_n + delta U_{n-1}` numerically (machine precision).
- Verified matrix char poly identity `det(zI-J_n(delta)) = p_n+delta p_{n-1}` symbolically for n=2,3,4.
- Confirmed no zeros outside `(-2,2)` by hyperbolic estimates.

Findings: no fatal gap. The proof uses only standard Chebyshev/Jacobi facts.

## Known not-audited

- The full O1/O2 remain open; this is declared, not hidden.
- No independent second agent audited (prohibited by run instruction); the
  audit is self-audit and a fresh-context convergence check from files.
