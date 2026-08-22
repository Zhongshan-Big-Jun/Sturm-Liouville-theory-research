# Research Ledger

Run: `R-20260822T000000Z-a6-baseline`
All timestamps UTC.

## 2026-08-22T13:20Z

- Read `PROBLEM-A6-RATIONAL.md`, `docs/SL_third_order_recurrence_theory.tex`,
  `tools/third-order-recurrence.md`, `research_map.md`.
- Read `scripts/op13_general_product_classify.py` and `scripts/op13_tail_check.py`.
- Established the exact even/odd `a_i` in the z-scale:
  - even a1 = `(c + 8 j^2 - 12 j + 4)/(4 j (j-1))`, a2 =
    `(-2 c j + 3 c - 4 j^3 + 12 j^2 - 11 j + 3)/(4 j (j-1)^2)`, a3 =
    `(4 c j^2 - 16 c j + 15 c)/(16 j (j-1)^2 (j-2))`.
  - odd a1 = `(c + 8 j^2 - 4 j - 4)/(4 j (j-1))`, a2 =
    `( -2 c j + c - 4 j^3 + 4 j^2 + j - 1)/(4 j (j-1)^2)`, a3 =
    `(4 c j^2 - 8 c j + 3 c)/(16 j (j-1)^2 (j-2))`.

## 2026-08-22T13:22Z

- Computed the generic asymptotic expansion of the fixed-point identity.
- Found the coefficient equations order by order.
- Key observation: for the free branch (`u = 1/2` even, `u = 3/2` odd),
  `A_2` is the only free asymptotic coefficient; `A_3, A_4, ...` are determined
  by `A_2`. For the rigid branch (`u = -1/2` even, `u = 1/2` odd), all higher
  coefficients are forced to vanish.

## 2026-08-22T13:24Z

- Derived the exact diagonal coefficient of the formal triangular system.
- Along the known exact trajectories:
  - free branch: `F_x = 1 - 2/j + O(j^{-2})`, so the coefficient of `A_{m-1}`
    in the `j^{-m}` residual is `m-3`;
  - rigid branch: `F_x = 1 + O(j^{-2})`, so the coefficient is `m-1`.
- These are nonzero for all relevant `m`, proving uniqueness of the formal
  expansion from `(u,A_2)`.

## 2026-08-22T13:26Z

- Wrote `reproducibility/verify_asymptotic_no_go.py` and ran it with sympy.
  Output:
  - parity=e, free: f1 = -2, diagonal coefficients [0,1,2,3,4,5] for m=3..8;
  - parity=e, rigid: f1 = 0, diagonal coefficients [2,3,4,5,6,7];
  - parity=o, free: f1 = -2, diagonal coefficients [0,1,2,3,4,5];
  - parity=o, rigid: f1 = 0, diagonal coefficients [2,3,4,5,6,7].
- The script output is exact symbolic, not numerical.

## 2026-08-22T13:29Z

- Composed the artifacts in the run root.
- The main theorem is: on the root-1 branch, any rational product ratio has
  degree at most 2, for both parities and all c > 0.

## Decisions

- Route A (asymptotic uniqueness + rational injection) selected.
- Route B (Petkovsek) not pursued: too heavy for a bounded run.
- Root-0 branch left open, with exact remaining gap recorded.
