p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3\research_ledger.md"
s = open(p, encoding="utf-8").read()

add = """

## R-005 (2026-08-05): Agent C - O3b boundary bounds
- Deliverable: agentC_O3b_boundary.md (verdicts: 2-block bounds PROVED; symmetric critical values PARTIAL; direct symmetry PARTIAL).
- Proved rigorously: two-block bound 3*pi^2/R < D(t) < 3*pi^2 for both orientations,
  via phase coordinates theta(x) = arctan(mu tan x) and three regimes (c >= 1 with exact sympy
  factorization of dG/dmu; 1/3 <= c <= 1; 0 < c <= 1/3 with exact W' < 0 proof, mpmath 60 digits).
- Numerics: 4000-point bound grid over R in [1.05, 1e4], 0 violations (margins +1.25e-8 / +1.28e-6).
- Partial: R->1+ first-order constant c ~ 2.0812 > 0 proved unconditionally; all-R conditional on O2.
- R->inf limits verified: SUP D -> 4*pi^2, u* -> 1/2; INF D*R -> 24.9438661384.
- Falsified routes recorded: ratio route (lambda_2/lambda_1 > 4 for two-block, phase computation ~9.0 at mu=1e4);
  regime-A sector bound; independent bracketing of eps_k; W' < 0 for all c; crude root-finding at extreme R.

## R-006 (2026-08-05): coordinator - KEY LEMMA decomposition and independent re-verification
- Decomposition: with alpha_2 = pi - gamma, G_2 - G_1 = (A-C) + (B-D) where
  A-C (even side) and B-D (odd side, |sin cos|) are explicit; q=1 base values
  (A-C)|_{q=1} = W(alpha_1)/(1+c), (B-D)|_{q=1} = -W(alpha_2)/(1+c).
- Exact corner limit q->1+, c->1/2-: A-C -> W(pi/3)/(3/2) = 2.80613..., B-D -> -W(2pi/3)/(3/2) = -0.38773...,
  sum -> 4 pi/(3 sqrt 3) = 2.41840...  (values in the handoff table 2.8086/-0.3751/2.4258 were slightly off, now corrected.)
- INDEPENDENT RE-VERIFICATION (coordinator, scripts misc/_verify_*.py): R=4 SUP D*=32.6139836177, INF D*=6.7844823391
  reproduced to 3.9e-11; two-block bound scan (phase solver) 0 violations over R in {1.05..1e4} x 120 t-values,
  min relative margin 1.6e-9; f_sym(1/2)=2 pi^2; KEY LEMMA margin min G(a2)-G(a1) >= 2.4481 (R=1.1) .. 19.45 (R=1e4).
- FALSIFIED ROUTE (handoff claim corrected): itemwise q-monotonicity of B-D does NOT hold.
  Fine scan: c=0.01, q: 5000 -> 20000 gives B-D: 199.79 -> 193.99 (decreasing); B-D decreases in q for c <= 0.1
  and increases only for c >= 0.3.  A-C IS monotone increasing in q on all sampled (c, q).
  Hence the handoff statement "d/dq(B-D) >= 0 on the full grid (min increment ~9e-5)" is FALSE;
  the closure "decomposition + itemwise q-monotonicity" is void.  The sum G_2 - G_1 remains >= 2.41840
  numerically on the full grid (min at the corner q->1+, c->1/2-), but KEY LEMMA proof stays open.
- Document rebuilt: docs/SL_gap_n1_research_summary.tex was corrupted (all Chinese -> '?' by a PowerShell
  encoding bug); reconstructed in full from run artifacts, corrected with the findings above, compiled
  with xelatex to 8 pages, zero warnings.
"""
s = s.rstrip() + "\n" + add
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ledger appended, new length", len(s))