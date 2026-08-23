# Research ledger

## 2026-08-23 (this run)

- **Contract/context read.** Baseline candidate_proof, final reports,
  docs/SL_fixed_n_supremum.tex, docs/SL_ratio_proof.tex, research_map,
  tools README + relevant tools, LEMMA_INDEX. Notable: round-2 reuse run
  `runs/plugin-perf-eval2/R-20260822T220000Z-b3-reuse/reuse_summary.md` was
  not present; only final_report there. No per-route REUSE/MISS tags per
  v1.5.0 protocol.

- **Symbolic derivation of general alternating cell matrix.**
  Discovered that with the correct product order `C = T_1(p) T_R(q)` and
  `M_n = C^n T_1(p)`, the Dirichlet secular element satisfies a Chebyshev
  combination with `delta = sin(q)/(s sin(p))`, simplifying the balanced-case
  recurrence. Verified symbolically/numerically for `s=2`,`r in {1,1.5,2,2.5,3}`,
  `n=1..5`, max error ~1e-14. This is STRICT.

- **Corollary.** In any global maximizer, `E=0` implies equal amplitudes of
  `u_n` and `u_{n+1}` on each constant block. STRICT.

- **O2 attempt.** Rewrote secular roots as
  `sin((n+1)theta)+delta(x)sin(n theta)=0` in the elliptic region.
  Proved fixed-delta Chebyshev root-location lemma for `0<delta<1` (STRICT; no monotonicity claimed).
  Could not close O2 because `delta` varies with `x`.

- **Numerical evidence.** For `R=4`, `n=2`, central pair ratio peaks near
  `r=2`; for `R=2` peaks near `1.414`; central pair delta values remain mostly
  below 1 away from extreme r. This is EVIDENCE, not proof.

- **Attempt O1 evidence.** Random Nelder-Mead on the 5-block simplex for
  `n=2,R=4` repeatedly approached the balanced widths; this is EVIDENCE.

## Failure mechanisms / gaps

- R6 literature route: no published fixed-n theorem found; degraded.
- R3 fixed-delta monotonicity cannot be applied directly because the curve
  `(m(x), delta(x))` has nonconstant delta.
- R5 cannot be converted to proof without a rigorous inequality.
