# -*- coding: utf-8 -*-
import io, re
p = r"state\RESUME.md"
src = io.open(p, encoding="utf-8-sig").read()
# locate the "Read these files first" list block and rebuild it
start = src.index("## Read these files first")
end = src.index("## Last completed action")
block = src[start:end]
new_list = """## Read these files first
1. `docs/SL_gap_n1_well_rigidity_R32.pdf` (INF well-family small-R rigidity theorem, 11 pp, 2026-08-10; gaps (a)-(d) registered; evidence log `misc/_well_explore_log.md`)
2. `docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf` (O3a complete proof, 40 pages, audited 2026-08-10 incl. Audit E replay + dual-subagent audit, F-210/F-211 fixed)
3. `docs/SL_gap_nge2_finite_reduction_proof.pdf` (n>=2 finite block reduction, 15 pages, 2026-08-10)
4. `docs/SL_gap_nge2_exact_2n_switches_proof.pdf` (n>=2 exact 2n switches, 16 pages, 2026-08-10)
5. `docs/SL_gap_n1_inf_limit_proof.tex` / `.pdf` (Theorem A, 10 pages)
6. `docs/SL_gap_n1_proof.tex` (O1/O2/O3b complete; section 5 = O3a status now CLOSED)
7. `docs/SL_spectral_topics_summary.tex` (overview; open problem list updated 2026-08-10)
8. `runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/`
9. `state/checkpoints/2026-08-07T160000Z--inflimit-close.md`
10. `misc/_well_explore_log.md` (well-family EVIDENCE log, 2026-08-10)
"""
src = src[:start] + new_list + src[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(src)
print("fixed")
