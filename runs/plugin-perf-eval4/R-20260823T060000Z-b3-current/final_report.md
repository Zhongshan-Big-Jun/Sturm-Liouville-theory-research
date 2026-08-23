# Final report

Status label: `RIGOROUS_PARTIAL_RESULT`

Run root: `F:\LaTeX\BVE research\runs\plugin-perf-eval4\R-20260823T060000Z-b3-current`

## Summary

This run attacked the remaining B3 open obligations O1 (equal-width optimal
among `[1,R,1,...,1]` bang-bang maximizers) and O2 (alternating-family ratio
maximized at `w_1/w_2 = sqrt(R)`).

It **does not close O1 or O2**. It produced:

1. **New STRICT tool: general alternating Chebyshev secular representation.**
   For every `R>1`, `n>=1`, and every equal-within-type alternating family
   `r = w_1/w_2`, the secular function is
   `sin(p) [ U_n(m) + delta U_{n-1}(m) ]`,
   with `m = tr(C)/2`, `delta = sin(q)/(s sin(p))`, `p = rx`, `q = sx`.
   This extends the round-2 balanced-case Jacobi/Chebyshev tool to non-balanced
   `r` and is the natural starting point for O2.

2. **New STRICT corollary.** Any global maximizer has equal amplitudes of
   `u_n` and `u_{n+1}` on each constant block (from `E=0`).

3. **O2 route reduction.** In the elliptic region (`|m|<1`), secular roots
   satisfy `sin((n+1)theta) + delta(x) sin(n theta) = 0`.
   The exact gap is that `delta` is x-dependent, so fixed-delta Chebyshev
   monotonicity is not directly applicable.

## Remaining open obligations

- **O1 open.** No proof that among all `[1,R,1,...,1]` with 2n switches the
  equal-width balanced configuration is optimal or that its value is `c_n(R)`.
- **O2 open.** No proof that inside the equal-within-type family the ratio
  peaks at `r = sqrt(R)`.

## STRICT results

- Baseline result (reused, not new): global maximizers are bang-bang
  `[1,R,1,...,1]` with 2n switches; balanced secular has 2n simple roots.
- New strict result: Chebyshev secular representation for general equal-width
  alternating family; amplitude equality corollary.

## Evidence (not proof)

- O2 numerical scans: `R=4,n=2` peak at `r=2`; `R=2,n=1` peak at `r=sqrt(2)`.
- O1 width-simplex random optimization for `n=2,R=4` recovered balanced widths.
- Lemma C1 numerical verification to machine precision.

## Artifacts count

12 files written in this run root (including this report and the evidence script):
- problem_contract, status_and_literature, approach_registry, research_ledger,
  obligation_graph, candidate_proof, escalation_ladder, audit_report,
  performance_log, reuse_summary, final_report,
- probe_general_alternating_chebyshev.py
Plus project-level additions: Lean scaffold and `tools/`/`research_map.md` update.

## Lean scaffold

A new Lean scaffold is added at
`lean-proof/SL/B3GeneralAlternatingChebyshev_Scaffold.lean` (scaffold, not
verified). It records the new Chebyshev representation as a placeholder
statement.

## Handoff

No interrupted handoff was written because the run reached a natural reporting
boundary at a partial-result status.
