# Status and literature

## Current status

- Problem node A6: `PARTIAL`.
- This run closes the root-1 higher-degree rational-ratio gap: **no reduced
  rational ratio of degree > 2 exists on the root-1 branch**, for both even and
  odd recurrences and all `c > 0`.
- The complete A6 problem remains `PARTIAL` because the root-0 / minimal-solution
  branch is not excluded by a complete theorem (the existing source evidence is
  numerical plus a formal uniqueness argument, not a full rational-injection
  proof).

## Exact known theorems before this run

Source: `docs/SL_third_order_recurrence_theory.tex`, sections 3-6, and
`tools/third-order-recurrence.md`.

| Result | Statement | Status |
| --- | --- | --- |
| Lemma 3.1 | `E_j = prod e_k` solves the z-recurrence iff `e_j = F_j(e_{j-1}, e_{j-2})` for `j >= 3` | STRICT |
| Theorem 3.2 | `1 + beta/(2k)` family: even `beta in {1,-1}`, odd `beta in {1,3}` | STRICT |
| Theorem 4.1 | Exact reduction of order (from a known product solution) | STRICT |
| Theorem 6.1 | Asymptotic classification: if `e_j -> 1` and `j(e_j-1) -> u`, then even `u in {-1/2,1/2}`, odd `u in {1/2,3/2}` | STRICT |
| Theorem 6.2 | Rigid branch: even `u=-1/2`, odd `u=1/2` forces `e_j = E^-` | STRICT |
| Theorem 6.3 | 4-parameter degree `<= 2` rational family: `E^(tau)` plus `E^-` | STRICT |
| Section 6.4 / open item | Higher-degree rational exclusion on root-1 branch | OPEN before this run |
| Section 6.4 | Minimal (root-0) branch non-rational | NUMERICAL + uniqueness, not a full theorem |

## New result in this run

**Theorem (Root-1 high-degree no-go).**
Let `p in {e,o}`, `c > 0`. Suppose `E_j = prod_{k=1}^j e_k` is a product
solution of the z-scaled recurrence, `e_j` is a rational function of `j`, and
`e_j -> 1`.  Then the reduced numerator and denominator degrees of `e_j` are
at most 2.  In fact `e_j` is exactly one of the known rational ratios from
Theorem 6.3.

The proof is in `candidate_proof.md`.  The new mechanism is the exact
diagonal-coefficient lemma for the formal fixed-point identity:

- Write `e_j = 1 + u/j + x_2/j^2 + x_3/j^3 + ...`.
- In the residual of the fixed-point identity, the coefficient of `x_m` at
  order `1/j^{m+1}` equals
  - even: `2u - (m-1)`;
  - odd:  `2u - (m+1)`.
- For the allowed `u` values this is nonzero for every `m >= 3` (and also for
  `m = 2` on the rigid branches).  Hence, once `u` and `x_2` are known, all
  higher `x_m` are uniquely determined.
- The free branches (`u = 1/2` even, `u = 3/2` odd) have `x_2` as the single
  free parameter; the known `E^(tau)` family realizes all these expansions.
- The rigid branches (`u = -1/2` even, `u = 1/2` odd) force `x_2 = x_3 = ... = 0`.

Since a rational function is uniquely determined by its Laurent expansion at
infinity, any rational solution must coincide with the known degree-`<= 2`
family.

## Literature

- The project document is the primary source; no external result was needed.
- Classical background: Poincare (1885), Perron (1909) for Poincare-type
  recurrence; the source document cites both.
- Petkovsek/Gosper hypergeometric-solution theory is a possible alternate route
  but was not needed.  It could provide an independent cross-check.
- No novelty claim beyond the project: the degree-`<= 2` classification was
  already known.  This run closes the root-1 higher-degree gap in the
  project's own A6 problem.
