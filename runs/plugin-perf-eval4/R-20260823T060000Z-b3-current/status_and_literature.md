# Status and literature

## Current status of B3

| Obligation | Status | Evidence |
| --- | --- | --- |
| O3 (2n-root count of balanced secular F_n) | CLOSED (STRICT) | R-20260822T220000Z-b3-baseline candidate_proof Part B; audit repaired |
| Ratio extremizer structure (bang-bang [1,R,1,...,1], 2n switches) | STRICT | R-20260822T220000Z-b3-baseline candidate_proof Part A |
| O1 (equal-width optimum among 2n-switch family) | OPEN | no proof; numerical maxima match balanced |
| O2 (alternating family max at r=sqrt R) | OPEN | no proof; numerical maxima match balanced |

## Relevant project results

- B1: `sup_{n,rho} lambda_{n+1}/lambda_n = nu(R)` solved
  (`docs/SL_ratio_proof.tex`), using Mahar-Willner Lemma 2.
- B2: `inf_{n,rho} lambda_{n+1}/lambda_n = 1`, solved (`docs/SL_inf_ratio_proof.tex`).
- Reflection symmetry for balanced alternating family: STRICT
  (`docs/SL_fixed_n_supremum.tex`, `lean-proof/SL/ReflectionSymmetry.lean`).
- MW Lemma/periodic extension gives `sup_rho lambda_{2n}/lambda_n = nu(R)`
  for every n, but that does not bound `lambda_{n+1}/lambda_n` sharply.

## Literature scan (compact)

- Keller 1976 (`papers/keller1976.pdf`): min `lambda_2/lambda_1`, general `j/k` ratios in class of piecewise constant densities; not the fixed-n `lambda_{n+1}/lambda_n` problem.
- Mahar-Willner 1976 (`papers/mw1976.pdf`): max/min `lambda_2/lambda_1`; Lemma 2 gives `sup lambda_{2n}/lambda_n = nu(R)`; not fixed-n adjacent ratio.
- Qi-Li-Xie 2020 (`papers/qi2020.pdf`): Lyapunov-type inequalities for first two eigenvalues of vibrating string; not fixed-n adjacent ratio.
- Huang 1999 (`papers/huang1999.pdf`): ratio bounds for concave/symmetric single-well/single-barrier densities; first two eigenvalues only.
- No published direct proof of `Lambda_n^sup(R) = c_n(R)` was found in the initial literature pass.

## New literature/tool update

The only new mathematical artefact in this run is a strict secular representation
for the general equal-within-type alternating family (see candidate_proof Part C).
It extends the round-2 balanced-case Chebyshev/Jacobi tool to non-balanced
widths `r != sqrt(R)` and is the natural tool for O2.
