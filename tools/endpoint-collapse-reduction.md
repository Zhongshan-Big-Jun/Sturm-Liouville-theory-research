---
canonical_key: endpoint-collapse-reduction (G2 endpoint obstruction, n>=2 gap extremals)
title: endpoint-collapse reduction: w1 -> 0 forces a band-matched reduced root with q0 = c
tags: [mathtool, self-developed, gap-extremals, boundary-exclusion, n-ge-2]
source: self-developed (session 58 continuation 8, 2026-08-13; run R-20260812T090000Z-g1prime-g2, obligation O-4)
status: reduction STRICT (proved); (G2) is now CLOSED STRICT by the block-energy identity + exact zero count (see [[switch-saturation-k-invariant]]); the non-existence of the reduced root is STRICT, not evidence
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
$c = \sqrt{\lambda_n / \lambda_{n+1}}$, and the endpoint slope ratios
$q_0 := u_{n+1}'(0)/u_n'(0) > 0$, $q_1 := u_{n+1}'(1)/u_n'(1) < 0$
(framework convention).

If a sequence of band-consistent solutions ($f = 0$ at every switch) has
$w_1 \to 0$ on a compact $R$-range $[R_0, R_1]$ with $R_0 > 1$, while
$w_2, \dots, w_{2n+1}$ stay bounded below, then (passing to a subsequence)
the limiting configuration is a band-matched root of the reduced $2n$-block
system, and it satisfies $q_0 = c$.

This reduction is now superseded by the direct closure: the block-energy
identity (see [[switch-saturation-k-invariant]]) gives $q_0 > 1 > c$ at every root of
the reduced system, while band matching on the reduced first block gives
$q_0 \le c$; hence no band-matched reduced root exists and no band-consistent
family has $w_1 \to 0$ on a compact $R$-range.  The reduction remains valid as
a consistency statement ($q_0 = c$ and $q_0 > 1$ cannot both hold).

## Proof sketch (full proof in run_notes_addendum_2026-08-13.md, Theorem B)

1. Widths $w_2, \dots, w_{2n+1}$ converge along a subsequence to positive
   widths summing to 1, giving the reduced string on $[0,1]$.
2. Eigenvalues and normalized eigenfunctions converge in $C^1$ (continuous
   dependence for piecewise-constant coefficients with a bounded number of
   discontinuities), so $\lambda_n, \lambda_{n+1}$ tend to the corresponding
   eigenvalues of the reduced string and $f$ tends to $f^*$ in $C^1$.
3. Band matching persists because $f^*$ has only simple interior zeros and
   is not identically zero on any block.
4. From $f(x_1) = 0$ with $x_1 = w_1 \to 0$ and the endpoint expansion
   $f(x) = \lambda_n u_n'(0)^2 (1 - q_0^2/c^2) x^2 + O(x^4)$, dividing by
   $x_1^2$ and taking the limit gives $q_0^* = c$.

Sign remark: band matching on the reduced first block (height $h_2$, opposite
of $h_1$) demands $f^* > 0$ near $x = 0$, i.e. $q_0^* \le c$; the endpoint
condition $q_0 = c$ is the boundary value of that range and is not excluded by
sign alone.

## Scope

- Applicable: boundary (endpoint) accumulation of block widths for the
  alternating bang-bang family, SUP and INF, any $n \ge 2$; the reduction is
  fully rigorous.
- Boundary cases: simultaneous collapse of both endpoints reduces the pattern
  by two blocks and imposes both $q_0 = c$ and $q_1 = -c$ (handled by the same
  reduction with end = both); interior coalescence $x_j \to x_{j+1}$ is
  excluded independently by the simplicity of interior zeros of $f$
  (Theorem C of the addendum).
- Superseded: the closure of (G2) now follows from
  [[switch-saturation-k-invariant]] + the exact zero count + interior simplicity
  (Theorem E of the addendum); this reduction is kept for reference.

## Verification status

- Reduction: STRICT (proved; see the run addendum for the complete argument).
- Closure of the obstruction: STRICT via [[switch-saturation-k-invariant]]
  ($q_0 > 1$ at every root) versus band matching ($q_0 \le c < 1$).
- Supporting numerics (EVIDENCE, not a proof): every reduced root found has
  $q_0 > 1$ and $q_1 < -1$ with band = False (n = 2, R = 4 random seeds;
  scripts/_gapn2_kidentity_audit.py); the degenerate (zero-width) roots
  reproduce the constant-density signature $q_0 = (n+1)/n$.

## Notes

- Convention bug fixed on 2026-08-13: the first version mixed the
  sqrt(lambda)-weighted ratio with the framework $q_0$; in the framework
  convention $a = 0$ is exactly $q_0 = c$ (in the sqrt-weighted convention
  it is $q_0 = 1$).  All earlier sqrt-weighted evidence lines are retracted.
- Related tools: [[switch-saturation-k-invariant]] (block-energy identity and
  exact zero count, the closing premises),
  [[band-selfconsistency-equivariance]] (the (G1')/(G2) framework),
  [[gap-band-extremals]] (band self-consistency),
  [[feynman-hellmann]] (the band-matching sign convention).
