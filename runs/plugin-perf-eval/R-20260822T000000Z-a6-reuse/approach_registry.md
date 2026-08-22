# Approach registry

Run: R-20260822T000000Z-a6-reuse
Variant: REUSE-GATE.

## REUSE protocol lines

For each route or lemma attempted, the following lines record whether an
existing item already covered it.

- `REUSE: docs/SL_third_order_recurrence_theory.tex` (sections 2-6, exact
  coefficients, definitions, Theorem 6.1/6.2/6.3; used as the source of all
  known facts before attempting new derivation).
- `REUSE: tools/third-order-recurrence.md` (summary of known classification,
  exact coefficient forms, and existing open gaps; used before deriving).
- `REUSE: tools/README.md` (tool index; confirms no separate high-degree tool
  exists under a different slug).
- `REUSE: research_map.md` (project node status; A6 is PARTIAL, no closure
  recorded).
- `REUSE: lean-proof/LEMMA_INDEX.md` (formalized ThirdOrder facts only cover
  beta-family, closed forms, minimal solution; no high-degree rational no-go).
- `REUSE: scripts/op13_general_product_classify.py` (general alpha/gamma
  family; supports the two-parameter family already known).
- `REUSE: scripts/op13_tail_check.py` (tail-recursion verification for the
  gamma = -1 representation; supports existing family).
- `REUSE: scripts/op13_4param_reduced.py` (degree-2 4-parameter classification;
  confirms the known degree-2 results, but does not cover degree > 2).
- `REUSE: scripts/op13_degtest.py` and `scripts/op13_degtest2.py` (attempted
  degree-3 rational solve; recorded as existing prior attempts, too heavy to
  run to completion in this bounded run).
- `REUSE: runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline/status_and_literature.md`
  (claimed a root-1 no-go result and described the asymptotic-uniqueness route;
  used as a route inspiration).
- `REUSE: runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline/reproducibility/verify_asymptotic_no_go.py`
  (exact symbolic script for the diagonal-coefficient facts; reused and
  re-run. It confirms `f1 = -2` free, `0` rigid for the chosen formulation.)
- `REUSE_MISS: runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline/candidate_proof.md`
  (the baseline's referenced proof file does not exist in the run root; the
  claimed theorem was not independently usable as a proof).
- `REUSE_MISS: runs/plugin-perf-eval/R-20260822T000000Z-a6-baseline/final_report.md`
  (no final report artifact exists; baseline status is not certified).
- `REUSE_MISS: scripts/op13_degtest.py` for a complete degree-3 solve
  (it timed out at 120s, so it does not provide an existing usable proof).
- `REUSE_MISS: an existing proof that the diagonal-coefficient formula holds for
  all m` (the baseline script checks only m = 3..8; the general formula was
  derived independently in this run).

## Route portfolio

| Route | Name | State | Exact gap / result |
| --- | --- | --- | --- |
| A | Asymptotic uniqueness + rational injection (root-1) | SUCCESS (STRICT sub-result) | Proves no reduced degree > 2 rational ratio on the root-1 branch, even and odd, all c > 0. |
| B | Petkovsek / hypergeometric-solution theory | TRIAGED, NOT PURSUED | Would independently bound degree from linear-recurrence theory; heavier and not needed for the partial result. |
| C | Direct degree comparison in the cleared polynomial identity | TRIAGED, NOT PURSUED | The cleared identity has many equations; the asymptotic route gives the same result more cleanly. |
| D | Root-0 / minimal-branch rationality exclusion | OPEN | The source has numerical fits plus formal uniqueness; no complete theorem. |
| E | Finite degree-3 symbolic solve | PARTIAL | Existing scripts time out for a general solve; finite checks would only reinforce route A, not prove the general no-go. |

## Route cards

### Route A: asymptotic uniqueness + rational injection

- Route ID and family: A (formal asymptotic/difference algebra).
- Core mechanism: prove the formal Laurent expansion is uniquely determined by
  `u` and, on the free branch, by `x_2`; then use uniqueness of a rational
  function from its expansion at infinity.
- Target obligation: root-1 high-degree no-go on both parities.
- Why easier: the diagonal coefficient is a simple first-order linear
  calculation and avoids solving the full nonlinear polynomial system.
- Required known results: Theorem 6.1 (allowed `u`), Theorem 6.2/6.3
  (known low-degree families).
- First concrete deliverable: exact diagonal-coefficient lemma.
- Fast falsification test: check m = 3..8 symbolically, both parities and all
  four allowed `u` values.
- Expected bottleneck: proving the coefficient formula for general `m`; this
  turned out to be a short exact derivative computation.
- Status: SUCCESS (STRICT sub-result).
- Exact gap: root-0 branch remains open.
- Next action: none for root-1; optionally formalize in Lean later.

### Route D: root-0/minimal branch non-rationality

- Route ID and family: D (minimal-solution asymptotic uniqueness).
- Core mechanism: show the minimal ratio's asymptotic expansion has no rational
  representation.
- Target obligation: complete exclusion of rational `e_j -> 0` ratios.
- Status: OPEN.
- Exact gap: no exact rational-injection theorem; only numerical fitting plus
  formal uniqueness evidence in the source.
