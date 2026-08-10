# -*- coding: utf-8 -*-
import os, io

ROOT = r"F:\LaTeX\BVE research"

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", os.path.relpath(path, ROOT))

# ---- agenda/DIRECTIONS.md ----
directions = """# Research directions (BVE SL spectral optimization)

## DIR-1 SL adjacent gap/ratio extremals, box class 1<=rho<=R (ACTIVE)
- Problems: O-2026-SL-GAP-3B7A2C (n=1 gap SUP/INF, current run),
  O-2026-SL-INF-RATIO-1C2D3E (inf of lambda_{n+1}/lambda_n), 
  O-2026-SL-FIXEDN-SUP-4E5F6A (fixed-n sup ratio conjecture),
  O-2026-SL-MW-LEMMA-0D1E2F (independent re-proof of MW periodic extension).
- Rationale: extends Keller/Mahar-Willner line to the gap functional D=lambda_2-lambda_1;
  the n=1 proof is the template for n>=2 and validates the band self-consistency picture.
- Current sub-goals: KEY LEMMA (O2 single crossing), O3a Lemmas A-C (2-param uniqueness),
  O3b boundary bounds (2-block done), O1 audit.

## DIR-2 Left-definite theory and orthogonal-system equivalence (mostly solved)
- H^2[-1,1] analytic completeness of the polynomial basis proved (session 9,
  docs/SL_h2_completeness_proof.pdf).
- Open: H^s (s>2) generalization; necessary/sufficient criteria for polynomial density
  in constraint-enforced Hilbert spaces.

## DIR-3 MDE extremal methods and singular measures (WATCH)
- Chu-Meng Math. Ann. 2024 (Camassa-Holm ratios), Zhang 2010, Meng-Zhang 2013,
  Wei-Meng-Zhang 2009. Applies to L^p balls / fixed total variation, not the box class.

## DIR-4 Nonlinear and generalized SL problems (WATCH)
- p-Laplacian (Wen-Zhou Mediterr. J. Math. 2026), singular measure potentials,
  Neumann and mixed boundary variants (Li-Ao JDE 2026).
"""
write_utf8(os.path.join(ROOT, "agenda", "DIRECTIONS.md"), directions)

# ---- agenda/PRIORITIES.md ----
priorities = """# Priorities (planning aid, not mathematical evidence)

Ranking by leverage x urgency x verification cost. Scores are management heuristics.

| Rank | Item | Leverage | Novelty risk | Verification cost | Rationale |
|---|---|---|---|---|---|
| 1 | KEY LEMMA (O2): (d/dc)log(M1/M2)<0 on (0,1/2) | closes O2 entirely | low (local lemma) | medium (transcendental estimates) | unique remaining gap for symmetric family; decomposition + corner limit + large numerical margin |
| 2 | O3a Lemmas A-C (branch uniqueness) | closes O3a | low | high (R-uniform bounds) | needed for full theorem; margins shrink with R |
| 3 | O1 draft independent audit (O4) | rigor of reduction | low | low (read + check) | reduction is foundational; must not ship unverified |
| 4 | INF R->inf limit D*R -> 24.943866 | completes asymptotics | medium | medium | explicit constant available (Agent C) |
| 5 | inf lambda_{n+1}/lambda_n = 1 ? | open ratio question | high | high | fully open; no proof bridge known yet |

Policy: keep KEY LEMMA as the single active delegation; run O3a in parallel when agents are free.
"""
write_utf8(os.path.join(ROOT, "agenda", "PRIORITIES.md"), priorities)

# ---- literature/maps/PAPER_MAP.md ----
paper_map = """# Paper map (SL spectral optimization; canonical identity + role)

Core ratio/gap line (Dirichlet string, box or bounded density classes):
- P-Keller1976: The minimum ratio of two eigenvalues, SIAM J. Appl. Math. 31 (1976),
  DOI 10.1137/0131042. Variational necessary conditions; inf ratio over box class.
- P-MW1976: Mahar-Willner, CPAM 29 (1976), DOI 10.1002/cpa.3160290505. Two-step
  extremal mechanism; lambda_2/lambda_1 max/min; periodic extension Lemmas 1-2.
- P-WM1982: Willner-Mahar, SIAM J. Math. Anal. 13 (1982), DOI 10.1137/0513040.
- P-Huang1999: Huang, eigenvalue ratio bounds, Proc. AMS / JMAA (1999).
- P-AB1993: Ashbaugh-Benguria, J. Diff. Eq. 103 (1993), DOI 10.1006/jdeq.1993.1047.
- P-Kiss2006: Kiss, Ann. Univ. Sci. Budapest (2006). Single-well/single-barrier n^2 bounds.
- P-Hedhly2021: arXiv:2111.01728 (single-well ratios); arXiv:2111.07719 (concave density).
- P-AEH2024: Ahrami-El Allali-Harrell, arXiv:2407.02459. Fundamental gap; Wronskian
  monotonicity of u_2/u_1 (Lemma 2.2 reused in O1).
- P-Cheng2010: Cheng-Kung-Law-Lian, CAMWA 60 (2010). Neumann 2nd-eigenvalue double-hole.

MDE / measure extremal line:
- P-Zhang2010: Zhang, Sci. China Math. 53 (2010); P-MZ2013: Meng-Zhang, JDE 254 (2013);
  P-WMZ2009: Wei-Meng-Zhang, JDE 247 (2009); P-CM2024: Chu-Meng, Math. Ann. 388 (2024),
  DOI 10.1007/s00208-022-02556-9.

2026 ratio/gap batch (paywalled; abstract or review level):
- P-Gan2026: Gan-Zheng-Li-Shao, MMAS 49 (2026), DOI 10.1002/mma.70611.
- P-LiAo2026: Li-Ao, JDE 476 (2026), DOI 10.1016/j.jde.2026.114478 (Neumann, MDE bridge).
- P-Xie2026: Xie-Jiang-Zhang, JDE 465 (2026), DOI 10.1016/j.jde.2026.114322 (inverse problems).

Left-definite / Krein-Sobolev line:
- P-JLQR2025: Jones-Littlejohn-Quintero Roba, Axioms 14 (2025) 115 (OA full text).
- P-LQR2025: Littlejohn-Quintero-Roba, OPSFA-16, Springer (2025), DOI 10.1007/978-3-031-90135-5_7
  (paywalled; content recovered via P-JLQR2025).

Relations: P-MW1976 extends P-Keller1976; P-WM1982 extends P-MW1976; P-Hedhly2021
specializes single-well classes; P-AEH2024 supplies the Wronskian lemma used in O1;
P-CM2024 generalizes ratio bounds to Camassa-Holm; DIR-1 results would extend all of
these to the gap functional on the box class.
"""
write_utf8(os.path.join(ROOT, "literature", "maps", "PAPER_MAP.md"), paper_map)

# ---- literature/maps/FRONTIER.md ----
frontier = """# Frontier (open problems, current as of 2026-08-06)

Active frontier (DIR-1, gap-n1 run):
- F-1 KEY LEMMA: (d/dc)log(M1/M2)<0 on q>1, c in (0,1/2); equivalent G(alpha2)>G(alpha1).
- F-2 O3a Lemmas A-C: R-uniform lower bound for g1'-g2'; endpoint signs; branch coverage.
- F-3 O1 draft independent audit (obligation O4).
- F-4 Rigorous proof of INF limit D*R -> 24.943866 as R -> inf.

Standing open problems (portfolio):
- inf_{n>=1,rho} lambda_{n+1}/lambda_n over box class: exact value (is it 1?).
- Fixed-n sup ratio Lambda_n^sup(R)=c_n(R) conjecture with band limit c_inf(R).
- n>=2 adjacent gap lambda_{n+1}-lambda_n extremals (template = n=1 proof).
- L^1/L^p potential-ball extremal bounds for adjacent gap (MDE line).
- Second/third left-definite spaces H^s (s>2): polynomial basis completeness.
- Krein operator constant c->0 degenerate limit.
- p-Laplacian and singular-measure generalizations of gap/ratio extremals.
"""
write_utf8(os.path.join(ROOT, "literature", "maps", "FRONTIER.md"), frontier)

# ---- knowledge/GLOSSARY.md ----
glossary = """# Glossary (project terms)

- Box class: densities rho measurable with 1<=rho<=R a.e.; pointwise bounds.
- Fundamental gap: D = lambda_2 - lambda_1 (first two eigenvalues).
- Barrier family: rho=R on an interior interval (a,b), 1 elsewhere.
- Well family: rho=1 on an interior interval (a,b), R elsewhere.
- Half-problem: on [0,1/2] with Neumann (even modes) or Dirichlet (odd modes) at 1/2.
- Phase variables: alpha_k = s_k u, beta_k = alpha_k c with c = qv/u; secular curves E/O.
- Feynman-Hellmann (FH): d lambda_k / d(parameter) from eigenfunction integrals.
- MDE: measure differential equation; extremal measures with atoms.
- Left-definite space: Hilbert space with inner product (K f, K g)_L2 for a Krein operator K.
- Krein-Sobolev polynomials: orthogonal in the first left-definite space of K_c.
- Bang-bang: extremizers take only boundary values {1,R}.
- KEY LEMMA: single-crossing estimate for the symmetric family (see tools/key-lemma-decomposition.md).
- M_1/M_2, F, G, W: specific functions of the phase analysis (see agentA_O2 report).
- Two-block config: rho with a single jump (a=0 or b=1 boundary of barrier/well families).
"""
write_utf8(os.path.join(ROOT, "knowledge", "GLOSSARY.md"), glossary)

# ---- knowledge/FAILURE_PATTERNS.md ----
failures = """# Failure patterns (recorded, reusable)

1. Itemwise monotonicity traps: B-D is NOT q-monotone even though A-C is (counterexample
   c=0.01, q 5000->20000). Never close a proof on grid-verified itemwise monotonicity alone.
2. Coarse-grid corner values: handoff tables (2.8086/-0.3751/2.4258) were coarse-grid;
   exact corner limits are 2.80613/-0.38773/2.41840. Always resolve corner limits analytically.
3. Secular equation sign errors: odd secular is q*tan(s2u)+tan(s2qv)=0, not tan(s2u)tan(s2qv)=-q.
4. Normalization square-root placement: zero condition is sqrt(N2)sin(alpha1)=sqrt(N1)sin(alpha2).
5. Numerical full-grid pass != theorem: every computational claim needs a proof bridge or certificate.
6. PowerShell heredoc Chinese corruption: always write UTF-8 no-BOM .py files, then execute.
7. Periodic-extension cell merging: unmerged cell-boundary blocks produce spurious jumps that
   falsely refute MW periodicity; merge same-value neighboring cells.
8. Table cross-fill: docs/SL_gap_extremals.tex tab:rscan SUP u-column was mis-filled with INF
   values; verify tables against independent solvers.
9. Oversold convergence claims: do not claim a fixed-point iteration is a global contraction
   (T has spectral radius 1.64 at R=100 with a genuine 2-cycle).
10. Itemwise product lower bounds: u_j >= (A_j/c) u_{j-1} fails; use monotonicity + ratio method.
"""
write_utf8(os.path.join(ROOT, "knowledge", "FAILURE_PATTERNS.md"), failures)

print("ALL DONE")