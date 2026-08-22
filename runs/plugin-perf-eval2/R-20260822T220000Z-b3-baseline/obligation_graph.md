# Obligation graph

Run: R-20260822T220000Z-b3-baseline

## Claims

| ID | Statement | Depends on | Status |
|---|---|---|---|
| T1 | Every global fixed-n ratio maximizer is bang-bang `[1,R,1,...,1]` with exactly 2n switches | A1,A2,A3 | PROVED (STRICT, candidate_proof Part A) |
| T2 | `F_n` has exactly 2n roots in (0,pi) for the balanced alternating family | B1,B2,B3 | PROVED (STRICT, candidate_proof Part B) |
| O1 | `Lambda_n^sup(R) = c_n(R)` attained by balanced alternating config | T1 + equal-width optimum O2 | OPEN |
| O2 | In the equal-within-type alternating family, ratio max at `w1/w2=sqrt(R)` | O3/root-count + monotonicity | OPEN |
| O3 | 2n-root count for alternating secular | T2 | CLOSED (via T2) |

## Detailed dependencies

- A1: weak-star compactness + spectral continuity (project docs).
- A2: Feynman-Hellmann ratio derivative and box saturation (derived).
- A3: Wronskian strictness + H zero-count + ratio energy invariant (derived).
- B1: transfer-matrix recurrence `G_n=tau G_{n-1}-G_{n-2}` (derived).
- B2: square-variable Chebyshev/Jacobi identification (derived).
- B3: no zeros outside (-2,2) via hyperbolic estimates (derived).

## Not proved

- Equal-width optimum in the `[1,R,1,...,1]` family.
- Global value `c_n(R)`.
