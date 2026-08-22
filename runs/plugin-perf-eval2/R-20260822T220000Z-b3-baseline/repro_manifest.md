# Reproduction manifest

Run: R-20260822T220000Z-b3-baseline

## Inputs

- Problem statement: `runs/plugin-perf-eval2/PROBLEM-B3-FIXEDN.md`
- Project root: `F:\LaTeX\BVE research` / `/mnt/f/LaTeX/BVE research`
- Required context read: docs/SL_fixed_n_supremum.tex, SL_ratio_proof.tex,
  SL_gap_nge2_finite_reduction_proof.tex, SL_gap_nge2_exact_2n_switches_proof.tex,
  research_map.md, tools/README.md, lean-proof/LEMMA_INDEX.md, scripts/op02_*.

## Environment

- WSL bash; python3 3.14.4.
- Python packages: numpy, mpmath, sympy. scipy not installed.
- Tool calls: read/write/edit/bash only; no subagents, no web search used.

## Exact commands

- `python3 scripts/op02_poly_extract.py`, `python3 scripts/op02_secular_sym.py`,
  `python3 scripts/op02_cn_verify.py` (project scripts, for context).
- Run-root probes:
  - `python3 probe_ratio_structure3.py`
  - `python3 verify_ratio_invariant.py`
  - `python3 probe_alternating_family.py`
  - `python3 symbol_polys2.py`

## Unknowns

- Exact git commit for run start not recorded; working tree had many pre-existing
  modifications. No commit was made by this subagent.
- scipy availability in other environments may affect scripts import (probe scripts avoid scipy).
