# Status and Literature

## Current status

- Problem node A6: `PARTIAL`.
- This run proves a new STRICT sub-result: **no higher-degree (degree > 2)
  rational product ratio exists on the root-1 branch (`e_j -> 1`)**, for both
  even and odd recurrences and all `c > 0`.
- The complete problem remains `PARTIAL` because the root-0/minimal branch
  (`e_j -> 0`) has only a numerical + uniqueness exclusion, not a full theorem.

## Exact known theorems before this run

Source: `docs/SL_third_order_recurrence_theory.tex`, sections 3-6, and
`tools/third-order-recurrence.md`.

| Result | Statement | Status |
| --- | --- | --- |
| Lemma 3.1 | `E_j = prod e_k` solves the z-recurrence iff `e_j = F_j(e_{j-1}, e_{j-2})` for `j >= 3` | STRICT |
| Theorem 3.2 | `1 + beta/(2k)` family: even `beta in {1,-1}`, odd `beta in {1,3}` | STRICT |
| Theorem 4.1 | Exact reduction of order | STRICT |
| Theorem 6.1 | Asymptotic classification: if `e_j -> 1` and `j(e_j-1) -> u`, then even `u in {-1/2,1/2}`, odd `u in {1/2,3/2}` | STRICT |
| Theorem 6.2 | Rigid branch: even `u=-1/2`, odd `u=1/2` forces `e_j = E^-` | STRICT |
| Theorem 6.3 | 4-parameter degree `<= 2` rational family: `E^(tau)` plus `E^-` | STRICT |
| Section 6.4 | Higher-degree rational exclusion | OPEN (before this run) |
| Section 6.4 | Minimal branch non-rational | NUMERICAL + uniqueness, not full theorem |

## New result in this run

**Theorem (Root-1 high-degree no-go).** Let `p in {e,o}` and `c > 0`. Suppose
`E_j = prod_{k=1}^j e_k` is a product solution of the z-scaled recurrence, with
`e_j` a rational function of `j` and `e_j -> 1`. Then `e_j` has degree at most 2;
it is exactly one of the known rational ratios of Theorem 6.3. Consequently no
high-degree (degree > 2) rational product ratio exists on the root-1 branch.

Proof: see `candidate_proof.md`. The essential new mechanism is an exact
asymptotic triangularity lemma:

- Along a **free** exact trajectory, `F_x = -a_2/e^2 - a_3/(e^2 e)`
  satisfies `F_x = 1 - 2/j + O(j^{-2})`.
- Along a **rigid** exact trajectory, `F_x = 1 + O(j^{-2})`.
- In the residual `F - e`, the coefficient of the first not-yet-determined
  coefficient `A_{m-1}` at order `j^{-m}` is `(m-1) + f_1` with `f_1 = -2`
  (free) or `f_1 = 0` (rigid). This is nonzero for every `m >= 4` (free) and
  `m >= 3` (rigid), so the formal expansion is uniquely determined by the
  first one or two coefficients.

## Literature

- The project document is the primary source; no external result was needed.
- Relevant classical background: Poincare (1885), Perron (1909) for
  Poincare-type recurrence; the source document cites both.
- The Petkovsek/Gosper hypergeometric-solution theory was considered as an
  alternative route (route B) but not needed. It may offer an independent
  cross-check; no implementation was performed in this run.
- No novelty claim beyond the project: the degree `<= 2` classification was
  already known. The novelty of this run is the closure of the root-1
  higher-degree gap.
