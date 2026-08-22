# Final report

Status label: `RIGOROUS_PARTIAL_RESULT`

Run root: `F:\LaTeX\BVE research\runs\plugin-perf-eval2\R-20260822T220000Z-b3-baseline`

## Summary

This baseline run produced two strict mathematical results on the fixed-n
adjacent ratio supremum problem (B3):

1. **Ratio extremizer structure theorem (STRICT).**
   For every `R>1` and `n>=1`, every global maximizer of
   `lambda_{n+1}/lambda_n` over the measurable box `1<=rho<=R` is a bang-bang
   configuration with exactly `2n` effective switches and material order
   `[1,R,1,...,1]`. The proof adapts the gap exact-2n-switch theory to the
   ratio functional using the switching function `H=u_n^2-u_{n+1}^2` and a new
   ratio energy invariant `E=b(u_n'^2+a r u_n^2)-a(u_{n+1}'^2+b r u_{n+1}^2)`,
   which gives `E=0` and `q0=1/c`, `q1=-1/c`.

2. **2n-root count theorem (STRICT).**
   For the balanced alternating bang-bang configuration
   `[1,R,1,...,1]` with `w_1/w_2=sqrt(R)`, the secular polynomial `F_n(y)` has
   exactly `2n` simple roots in `(0,pi)` for every `n>=1` and `R>1`.
   The proof uses the transfer-matrix recurrence
   `G_n = tau G_{n-1} - G_{n-2}`, the square variable `x=C^2`, and the
   identification `P_n(x)=U_n(t)+(1/s)U_{n-1}(t)`, which is the characteristic
   polynomial of a finite Jacobi matrix whose spectrum lies in `(-2,2)`.

These are new strict partial results beyond the existing project state
(reflection symmetry STRICT, B1 all-n sup SOLVED, gap D_n exact 2n switches).

## Exact remaining gaps

- **O1 (global extremality to equal-width alternating family/value).** The
  structural theorem reduces global extremality to optimization over all
  `[1,R,1,...,1]` bang-bang configurations with exactly `2n` switches. The
  switch positions/block lengths are still not determined; in particular it is
  not proved that the maximizer has equal widths `w_1/w_2=sqrt(R)` or that the
  value is `c_n(R)`.
- **O2 (alternating-family monotonicity/uniqueness).** Within the restricted
  equal-within-type alternating family, the maximum appears at
  `r=sqrt(R)` numerically, but a proof is not given. The new structural theorem
  and O3 root-count proof provide tools but do not by themselves close O2.
- **O3** is now closed in this run.

## Numerical evidence (not proof)

- `q0=1/c`, `q1=-1/c` for alternating maximizers, R=2,4,10, n=1..5.
- `E` approximately constant and close to 0 on the balanced maximizer.
- Ratio as a function of `r=w_1/w_2` peaks near `r=sqrt(R)` in the restricted
  family; `H` residuals are negative for `r<sqrt(R)` and positive for
  `r>sqrt(R)`.

## Reproducibility

- Environment: WSL, Python 3.14, numpy/mpmath/sympy; scipy unavailable.
- Scripts in run root:
  - `probe_ratio_structure3.py` (robust eigen/state probe)
  - `verify_ratio_invariant.py` (E evidence)
  - `probe_alternating_family.py` (r-variation evidence)
  - `symbol_polys.py`, `symbol_polys2.py` (secular polynomial exploration)
- The strict proofs in `candidate_proof.md` are self-contained and do not rely
  on these numerical scripts.

## Handoff

No handoff was written because the run reached a natural reporting boundary
with two STRICT results and explicit remaining obligations. The run's
artifacts were written to the run root; they have not been committed to git by
this subagent (project-level AGENTS.md, research_map.md and tools/ index were
updated in the working tree as part of the standard skill behavior).

If extended, the next actions are:
- attack O2 on the equal-width alternating family using the secular recurrence;
- attack O1 by proving that among all `[1,R,1,...,1]` bang-bang maximizers the
  equal-width balanced configuration is optimal;
- consider Lean scaffolding for the 2n-root-count theorem and the ratio
  structure theorem.
