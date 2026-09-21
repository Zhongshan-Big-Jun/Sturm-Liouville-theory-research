# BVE research (MRP-20260731-BVE-SL)

Sturm-Liouville spectral optimization: eigenvalue ratios, gaps, extremal configurations, and left-definite theory.

## Ownership (per manage-math-research-program v2026-08-05)
- Program state: `state/`, `index/`, `agenda/`, `literature/`, `knowledge/`, `reports/` (manager-owned).
- Legacy pre-skill layout preserved as-is: `docs/`, `tools/`, `papers/`, `scripts/`, `research_cache/`, `images/`, `misc/`.
- Solver runs: `runs/rigorous-open-math-research/RUN_ID/` (owned by $rigorous-open-math-research).
- Protected upstream filenames (`problem_contract.md` etc.) only under run roots.

## Research directions
1. **SL gap extremals** (active for n>=2): SUP/INF of lambda_{n+1}-lambda_n over box class 1<=rho<=R. For n=1, both SUP and INF are STRICT/CLOSED for all R>1 (2026-08-12, session 58 continuation 3; commit 220785e). See `state/RESUME.md` for the closure record and `docs/research-guide.md` for the proof chain. The n>=2 global problem remains open; n=1 certificate-kernel formalization is a separate follow-up.
2. **SL ratio extremals**: sup lambda_{n+1}/lambda_n = nu(R) proved (session 5); fixed-n and inf problems open.
3. **Left-definite theory / orthogonal systems**: H^2 polynomial completeness proved (session 9).

## Key files
- Status/proof navigation: `docs/research-guide.md`; overview: `docs/SL_spectral_topics_summary.tex`. Resolve status differences using the relevant proof chain and dated closure/audit records.
- 2026-09-20 proof errata and validation: `reports/proof-audit-20260920/REPORT.md` (local repairs; historical full interval audits and Lean are separate).
- Gap extremals report: `docs/SL_gap_extremals.tex`.
- Tools: `tools/` (legacy) + `knowledge/tools/` (new index).
- Recovery entry: `state/RESUME.md`.
