# Approach registry

## Pre-scan REUSE hits

- REUSE: tools/transfer-matrix-secular.md — transfer-matrix machinery for all numerical/symbolic work.
- REUSE: tools/balanced-phase.md — n=1 closed form and balanced-phase idea; C=cos y substitution.
- REUSE: tools/keller-variational.md + tools/bang-bang.md — variational saturation framework for ratio functional.
- REUSE: docs/SL_gap_nge2_finite_reduction_proof.tex + docs/SL_gap_nge2_exact_2n_switches_proof.tex — Wronskian W<0, strict Q monotonicity, exact zero-count pattern, endpoint rigidity.
- REUSE: tools/switch-saturation-k-invariant.md — block-energy invariant template (adapted to ratio K_ratio).
- REUSE: tools/band-selfconsistency-equivariance.md — equivariance/Jacobian/topological-degree framework for later uniqueness/symmetry arguments.
- REUSE: lean-proof/ReflectionSymmetry.lean F_reflection VERIFIED — reflection symmetry support.
- REUSE: scripts/op02_secular_sym.py / op02_poly_extract.py / op02_rootcount.py — symbolic F_n and numerical root-count baseline.

## Pre-scan REUSE misses

- REUSE_MISS: no existing strict proof that the alternating secular polynomial has exactly 2n roots; only numerical evidence.
- REUSE_MISS: no existing ratio-specific exact-2n-switch theorem or ratio block-energy invariant.
- REUSE_MISS: no existing proof of alternating-family monotonicity at w_1/w_2=sqrt(R).
- REUSE_MISS: no existing self-consistency/root-solver script for the ratio functional on the alternating bang-bang family.

## Route portfolio

| ID | Route | State | Exact remaining gap |
|----|-------|-------|---------------------|
| R0 | Pre-scan / reuse audit | DONE | none |
| R1 | 2n-root count via elliptic-zone phase lemma | STRICT (this run) | none |
| R2 | Ratio finite reduction + exact 2n switches + alternating pattern | STRICT (this run) | ratio uniqueness/width optimization inside alternating family still open |
| R3 | Alternating-family self-consistency uniqueness (topology/equivariance) | IN_PROGRESS | prove (G1')/(G2) or an analogous degree invariant for ratio system |
| R4 | Alternating-family one-parameter monotonicity | PROPOSED/OPEN | prove ratio as function of width ratio has single max at sqrt(R) |
| R5 | Literature route (MW/Keller) | OPEN | no direct fixed-n ratio result found in pre-scan |

## Quick decision

R1 and R2 are new STRICT partial results, enough to upgrade the run status to
RIGOROUS_PARTIAL_RESULT. R3/R4 remain open and are candidates for deeper work.

## Mid-run REUSE update (baseline discovery)

- REUSE: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md
  — the baseline run already contains both STRICT results we independently
  derived. We cross-checked: the baseline ratio energy invariant E = b E_n - a E_{n+1}
  is equivalent to our K_ratio = E_n/a - E_{n+1}/b, scaled by 1/(ab); the
  baseline 2n-root-count proof uses a Jacobi-matrix argument, ours uses an
  elliptic-zone phase lemma; both are valid and consistent.
- REUSE: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/probe_alternating_family.py
  — EVIDENCE probe for the one-parameter alternating family; reused for O2 discussion.
- REUSE_MISS_EXISTING (protocol note): the pre-scan did not discover the baseline
  run before derivation because it was not in the required reading list at start;
  it was found later via AGENTS.md session-log update. This is recorded as a
  performance/tooling observation, not a mathematical gap.
