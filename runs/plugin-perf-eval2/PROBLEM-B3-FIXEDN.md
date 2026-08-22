# Round 2 benchmark problem: B3 fixed-n supremum (global extremality + 2n root count)

Project: Sturm-Liouville spectral optimization (MRP-20260731-BVE-SL)
Local root: F:\LaTeX\BVE research

## Why this is a harder / larger benchmark

This is a major open problem in the project. It has a large existing tool
library, several partial STRICT results, a clear conjectured extremal
configuration, and two independent open proof obligations. It is intended to
stress the plugin much harder than the small A6 experiment in round 1.

## Problem statement

Consider the Dirichlet string equation

    -y'' = lambda rho(x) y,   y(0)=y(1)=0,   0 < a <= rho <= A,

with R = A/a. Let 0 < lambda_1 < lambda_2 < ... be the eigenvalues and define
the fixed-n adjacent ratio supremum

    Lambda_n^sup(R) = sup_rho  lambda_{n+1}(rho) / lambda_n(rho).

Conjecture (numerical, recorded in the project): the supremum is attained by
the alternating bang-bang configuration

    rho = [1, R, 1, R, ..., 1]   (2n+1 blocks),
    w_1 / w_2 = sqrt(R),
    t = 1 / ((n+1) sqrt(R) + n),

and the value is c_n(R) = ((pi - y_n)/y_n)^2 where y_n is the n-th balanced
phase root.

## Open proof obligations (from docs/SL_fixed_n_supremum.tex section 5)

1. Global extremality: prove that every fixed-n maximizer can be reduced by a
   Keller-type variational argument to the alternating bang-bang family
   [1,R,1,...,1].
2. Alternating-family monotonicity / uniqueness: prove the ratio
   lambda_{n+1}/lambda_n is maximized at the width ratio w_1/w_2 = sqrt(R)
   inside the alternating family, and that the balanced-phase root y_n gives
   the maximum.
3. General 2n-root count: prove that the alternating secular polynomial
   F_n(y) (or equivalently Q_n(cos y)) has exactly 2n roots in (0,pi) for
   every n >= 1 and R > 1. This is currently numerical evidence only.

Any rigorous partial result, new reduction, structural theorem, falsification,
or exact obstruction is a valuable outcome. Do not claim the whole problem is
solved unless every one of these obligations is closed.

## Required project context to read

- `docs/SL_fixed_n_supremum.tex`
- `docs/SL_ratio_proof.tex`
- `docs/SL_gap_nge2_finite_reduction_proof.tex`
- `docs/SL_gap_nge2_exact_2n_switches_proof.tex`
- `research_map.md`
- `tools/README.md` and relevant tools (`balanced-phase`,
  `transfer-matrix-secular`, `keller-variational`, `bang-bang`,
  `reflection-branch-reduction`, `gap-band-extremals`,
  `band-selfconsistency-equivariance`, `switch-saturation-k-invariant`)
- `lean-proof/LEMMA_INDEX.md`
- Existing scripts under `scripts/op02_*.py` (fixed-n and alternating-family
  numerical/symbolic tools)

## Output requirements

Write in the run root the standard rigorous-open-math-research artifacts:
`problem_contract.md`, `status_and_literature.md`, `approach_registry.md`,
`research_ledger.md`, `candidate_proof.md`, `escalation_ladder.md`,
`performance_log.md`, `final_report.md`, plus any reproducibility scripts.

Status labels must follow the rigorous-open-math-research output protocol.
Numerical evidence must never be presented as proof.
