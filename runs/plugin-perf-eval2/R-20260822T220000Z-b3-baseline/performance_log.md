# Performance log

Run: R-20260822T220000Z-b3-baseline
Mode: BASELINE (no mandatory reuse-gate protocol)

## Timeline (UTC approximate)

| Time | Action | Category | Result |
|---|---|---|---|
| 22:20 | Read problem statement, docs, tools, research map, Lean index, op02 scripts | READ | Registered existing B1 SOLVED, B3 PARTIAL, gap exact-2n-switch STRICT |
| 22:25 | First probe script (scipy missing; adapted to numpy) | COMPUTE | Discovered correct transfer-matrix order and fixed alt_config bug |
| 22:30 | Ran ratio structure probes | COMPUTE | EVIDENCE ratio/H/q0/q1 on alternating family |
| 22:35 | Derived ratio energy invariant and structural theorem | DERIVATION | STRICT: every ratio max is bang-bang [1,R,...,1] with exactly 2n switches |
| 22:40 | Wrote candidate_proof Part A; updated registry/ledger | WRITE | Artifact updated |
| 22:45 | Explored symbolic secular polynomials | COMPUTE | Found messy expressions; led to recurrence search |
| 22:50 | Found transfer-matrix recurrence `G_n=tau G_{n-1}-G_{n-2}` | DERIVATION | Key for O3 |
| 22:55 | Found Chebyshev/Jacobi closed form `P_n=U_n+1/s U_{n-1}` | DERIVATION | O3 proof structure |
| 23:00 | Verified recurrence and closed form symbolically/numerically | VERIFY | PASS (n=2..5 recurrence; s=3,n=1..6 closed form) |
| 23:05 | Wrote Part B proof of 2n-root count; updated artifacts | WRITE | O3 STRICT PROVED |
| 23:10 | Probe alternating family r-variation | COMPUTE | EVIDENCE: max near r=sqrt(R); H residual sign negative/positive on either side |

## Major reads/writes/derivations

- Reads: 4 main docs + research_map + tools + Lean index + op02 scripts.
- Writes: problem_contract, status_and_literature, approach_registry, research_ledger, escalation_ladder, candidate_proof, probe scripts.
- Derivations:
  1. Ratio derivative `d(b/a) = (b/a) int h (u_n^2-u_{n+1}^2)`.
  2. Ratio energy invariant `E=bE_n-aE_{n+1}` yielding `q0=1/c`, `q1=-1/c`.
  3. Secular recurrence `G_n=tau G_{n-1}-G_{n-2}`.
  4. Chebyshev/Jacobi identity for `Q_n`.

## Reuse or re-derivation notes

- Reused from project: weak-star compactness/spectral continuity argument, Prufer nodal/interlacing, Wronskian strict negativity, Feynman-Hellmann formula, and the gap exact-2n-switch strategy.
- Re-derived: ratio-specific switching function and energy invariant (not present in project).
- O3 proof is new: it reuses the transfer-matrix setup but derives a new recurrence and Chebyshev/Jacobi argument.
- No external web search was needed for the two STRICT results; the project's local docs were sufficient.

## Tool usage summary

- `bash` (jobs/probes), `read`, `write`, `edit`.
- Python 3.14 with numpy/mpmath/sympy; scipy unavailable (documented).
- Did not use web search or subagents, respecting the no-nested-subagent instruction.
