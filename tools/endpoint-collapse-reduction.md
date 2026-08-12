---
canonical_key: endpoint-collapse-reduction (G2 endpoint obstruction, n>=2 gap extremals)
title: endpoint-collapse reduction: w1 -> 0 forces a band-matched reduced root with q0 = c
tags: [mathtool, self-developed, gap-extremals, boundary-exclusion, n-ge-2]
source: self-developed (session 58 continuation 7, 2026-08-13; run R-20260812T090000Z-g1prime-g2, obligation O-4)
status: reduction STRICT (proved); non-existence of the reduced root is EVIDENCE (not proved)
created: 2026-08-13
updated: 2026-08-13
---

# Endpoint-collapse reduction for the n>=2 gap extremal problem

## Statement (reduction, STRICT)

For the Dirichlet weighted string $-u'' = \lambda \rho u$, $u(0) = u(1) = 0$,
let $\rho$ be the alternating bang-bang density with $2n+1$ blocks of heights
in $\{1, R\}$ and widths $w_j > 0$ summing to 1, switch points
$x_j = w_1 + \dots + w_j$.  Let $D_n = \lambda_{n+1} - \lambda_n$,
$f = \lambda_n u_n^2 - \lambda_{n+1} u_{n+1}^2$,
$c = \sqrt{\lambda_n / \lambda_{n+1}}$, and the endpoint slope ratio
$q_0 = \sqrt{\lambda_{n+1}} |u_{n+1}'(0)| / (\sqrt{\lambda_n} |u_n'(0)|)$.

If a sequence of band-consistent solutions ($f = 0$ at every switch) has
$w_1 \to 0$ on a compact $R$-range $[R_0, R_1]$ with $R_0 > 1$, while
$w_2, \dots, w_{2n+1}$ stay bounded below, then (passing to a subsequence)
the limiting configuration is a band-matched root of the reduced $2n$-block
system, and it satisfies $q_0 = c$.

Hence the endpoint part of condition (G2) is equivalent to the
finite-dimensional statement: no band-matched reduced root has $q_0 = c$.

## Proof sketch (full proof in run_notes_addendum_2026-08-13.md)

1. Widths $w_2, \dots, w_{2n+1}$ converge along a subsequence to positive
   widths summing to 1, giving the reduced string on $[0,1]$.
2. Eigenvalues and normalized eigenfunctions converge uniformly (continuous
   dependence for piecewise-constant coefficients with a bounded number of
   discontinuities), so $\lambda_n, \lambda_{n+1}$ tend to the corresponding
   eigenvalues of the reduced string and $f$ tends to $f^*$.
3. Band matching persists because $f^*$ has only finitely many zeros and is
   not identically zero on any block interior.
4. From $f(x_1) = 0$ with $x_1 = w_1 \to 0$ and the endpoint expansion
   $f(x) = [\lambda_n u_n'(0)^2 - \lambda_{n+1} u_{n+1}'(0)^2] x^2 + O(x^4)$,
   dividing by $x_1^2$ and taking the limit gives
   $\lambda_n u_n'(0)^2 = \lambda_{n+1} u_{n+1}'(0)^2$, that is $q_0 = c$.

Sign remark: at a band-matched reduced root $q_0 < 1$ in both modes (the
reduced first block carries $f > 0$ near $x = 0$ and
$\operatorname{sign} f(x) = \operatorname{sign}(1 - q_0^2)$ for small $x$).
Since $c < 1$, the endpoint condition $q_0 = c$ is not excluded by sign alone;
a quantitative separation $q_0 \neq c$ on the band-matched reduced solution
set is what remains open.

## Scope

- Applicable: boundary (endpoint) accumulation of block widths for the
  alternating bang-bang family, SUP and INF, any $n \ge 2$; the reduction is
  fully rigorous and lowers the (G2) endpoint obstruction to a
  finite-dimensional existence/non-existence question.
- Boundary cases: simultaneous collapse of both endpoints reduces the pattern
  by two blocks and imposes both $q_0 = c$ and $q_1 = c$ (handled by the same
  reduction with end = both); interior coalescence $x_j \to x_{j+1}$ is the
  separate, harder case (a double zero of $f$ at the collapsed point).
- Not applicable: it does not prove non-existence of the reduced root; it
  only transfers the obstruction to that finite-dimensional statement.

## Verification status

- Reduction: STRICT (proved; see the run addendum for the complete argument).
- Supporting numerics (EVIDENCE, not a proof):
  - On the full symmetric branch, $q_0 / c > 1$ at every checked point
    (n = 2 for R <= 100; n = 3 for R <= 30; n = 4 for R <= 10, SUP and INF),
    with the quadratic-expansion test $f(x)/(a x^2) \to 1$ at $x = 10^{-4},
    10^{-3}$ and the $R \to 1$ limit reproducing the constant-density value
    $q_0 / c \to ((n+1)/n)^3$.
  - Reduced-root hunts (random and branch-seeded) found no band-matched
    reduced root, and every reduced root found has $q_0 - c > 0$ (n = 2, 3, 4,
    SUP/INF, R up to 100); degenerate roots reproduce the
    $((n+1)/n)^3$ signature.
- Scripts: scripts/_gapn2_slope_ratio.py,
  scripts/_gapn2_reduced_endpoint_hunt.py,
  scripts/_gapn2_endpoint_targeted.py.

## Notes

- Two slope-computation bugs in the first draft of _gapn2_slope_ratio.py
  (block-start transfer-matrix coefficient, and per-R pattern used in the
  report loop) were fixed; all earlier slope numbers in the handoff are
  retracted.
- Related tools: [[band-selfconsistency-equivariance]] (the (G1')/(G2)
  framework this feeds), [[gap-band-extremals]] (band self-consistency),
  [[feynman-hellmann]] (the band-matching sign convention).
