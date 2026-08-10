# BVE research (MRP-20260731-BVE-SL)

Sturm-Liouville spectral optimization: eigenvalue ratios, gaps, extremal configurations, and left-definite theory.

## Ownership (per manage-math-research-program v2026-08-05)
- Program state: `state/`, `index/`, `agenda/`, `literature/`, `knowledge/`, `reports/` (manager-owned).
- Legacy pre-skill layout preserved as-is: `docs/`, `tools/`, `papers/`, `scripts/`, `research_cache/`, `images/`, `misc/`.
- Solver runs: `runs/rigorous-open-math-research/RUN_ID/` (owned by $rigorous-open-math-research).
- Protected upstream filenames (`problem_contract.md` etc.) only under run roots.

## Research directions
1. **SL gap extremals** (active): SUP/INF of lambda_{n+1}-lambda_n over box class 1<=rho<=R. n=1 strict proof in progress (run R-20260805T000000Z-gapn1-a1b2c3).
2. **SL ratio extremals**: sup lambda_{n+1}/lambda_n = nu(R) proved (session 5); fixed-n and inf problems open.
3. **Left-definite theory / orthogonal systems**: H^2 polynomial completeness proved (session 9).

## Key files
- Overview: `docs/SL_spectral_topics_summary.tex` (open-problem list authoritative).
- Gap extremals report: `docs/SL_gap_extremals.tex`.
- Tools: `tools/` (legacy) + `knowledge/tools/` (new index).
- Recovery entry: `state/RESUME.md`.
