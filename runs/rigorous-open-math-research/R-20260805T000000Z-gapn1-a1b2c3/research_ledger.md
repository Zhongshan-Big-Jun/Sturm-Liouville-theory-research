# Research ledger

Timestamps are approximate (UTC).  Every entry names concrete evidence.

## R-001 (2026-08-05): contract + literature grounding
- Read AEH arXiv:2407.02459v2 (papers/fundamental_gap.txt): Lemma 2.1
  (FH), Lemma 2.2 (monotonicity of u_2/u_1 and single-interval {f>0}),
  Theorem 3.1 (single-barrier class minimizes the gap; different class).
- Re-derived the Wronskian argument: for ANY positive bounded rho,
  W = u_1 u_2' - u_1' u_2 satisfies W' = (lambda_1 - lambda_2) rho u_1 u_2,
  W(0) = W(1) = 0, W < 0 on (0,1); hence v = u_2/u_1 strictly decreasing
  on (0,1); f = lambda_1 u_1^2 - lambda_2 u_2^2 has at most two zeros and
  {f > 0} is a single interval.  This is O1c (PROVED).
- Established O1 (reduction): N-jump compactness argument reduces
  S(R) to the max over the barrier family and I(R) to the min over the
  well family; see obligation_graph.md.  Written as a draft proof.
- Wrote problem_contract.md, repro_manifest.md, status_and_literature.md,
  obligation_graph.md, approach_registry.md.

## R-002 (2026-08-05): first-order placement analysis (Route D theory)
- For rho = 1 + eps chi_(a,b), dD/deps(0) = 2 pi^2 int_a^b g(x) dx with
  g(x) = 4 sin^2(2 pi x) - sin^2(pi x).  g has global max at x ~ 0.2400
  and 0.7600 (roots of 16 cos(2 pi x) = 1), min at x = 1/2 (g = -1).
- CONSEQUENCE: for fixed small barrier width, the optimal placement is
  OFF-CENTER (near the quarter points), NOT symmetric.  So any proof
  must NOT rely on "centered placement is best at fixed width".
  This kills the naive symmetrization and motivates Route D numerics for
  small R (phase-transition check).

## R-003 (2026-08-05): Agent A O2 - single zero-crossing of f_sym (symmetric barrier)
- Deliverable: agentA_O2_single_crossing.md (22 KB) + agentA_verify.py. Verdict PARTIAL.
- Proved rigorously (T1-T4, Section 2): half-problem reduction with corrected odd secular
  equation q tan(s2 u) + tan(s2 q v) = 0; normalization u_k(u,u)^2 = tan^2(alpha_k)/(1/2 + w tan^2(alpha_k));
  corrected zero condition sqrt(N2) sin(alpha1) = sqrt(N1) sin(alpha2); corrected endpoint f_sym(1/2) = 2 pi^2;
  c-parametrization u = q/(2(c+q)) with beta = c alpha shared line; phi_c strictly increasing on (0,pi/2)
  (Lemma 1, full proof); F(c) = M1 - M2 sign: F < 0 on [1/2, inf), F(0+) > 0, F(1) < 0;
  D'(c) = (8/q^2)(c+q) F(c); f_sym and F same sign; dD/du = -2(R-1) f_sym verified to 1e-6.
- Exact gap: KEY LEMMA - (d/dc) log(M1/M2) < 0 for all q > 1, c in (0,1/2); equivalent to F'(c) < 0 on
  (0,1/2) and to G(alpha_2) > G(alpha_1) with explicit G (Section 2.9). Numeric margin min >= 2.45 (R=1.1)
  up to 19.45 (R=1e4); verified R in [1.0005, 1e6]. Closing it upgrades verdict to PROVED.
- Numerics: u* and D* for R in {1.1, 2, 4, 10}: (0.420835, 29.7107), (0.436696, 31.1023),
  (0.451485466, 32.613983617), (0.466931, 34.4513); matches contract u*=0.45148546584, D=32.6139836177 at R=4.
  Sign pattern - then + verified; zero condition vanishes to ~1e-9 at u*.
- Failed candidates recorded (Section 5): F not monotone on (0,1), F not convex, M1/M2 not globally
  decreasing, G(alpha;c) not monotone in alpha, sign dichotomy G(a1)<0<G(a2) false for R<4,
  D not concave/unimodal in any standard variable, Wronskian argument inapplicable to moving junction.
- Flagged discrepancy: docs/SL_gap_extremals.tex tab:rscan SUP u-column (u=0.382598 at R=4) contradicts
  the contract and all recomputations; contract numbers are correct.

## R-004 (2026-08-05): Agent B - O3a uniqueness of the 3-block self-consistent fixed point (barrier family)
- Deliverable: agentB_O3a_fixed_point.md (verdict PARTIAL). Claim NOT refuted at any R in
  {1.02, 1.05, 1.2, 1.5, 2, 3, 4, 5, 10, 20, 50, 100, 1000}; exactly one sign-consistent fixed point each.
- Proved rigorously: T1 (fixed points of T = sign-consistent critical points = good roots of (R1,R2)=0);
  T2 (T o sigma = sigma o T, uniqueness implies b = 1 - a); T3 (exactness identity dR1/db = -dR2/da,
  from O1b FH formulas dD/da = -(R-1)R1, dD/db = +(R-1)R2 plus Schwarz; FH verified to 1e-6, identity to ~1e-7);
  T4 (uniqueness reduces to three branch lemmas A/B/C).
- Branch structure verified for R in {1.05, 1.5, 2, 4, 10, 100}: good branches Gamma_1 (a=x_-),
  Gamma_2 (b=x_+) are single monotone increasing graphs g1, g2; h = g1 - g2 strictly increasing with
  exactly one zero at the fp; min h' = 42.78 (1.05), 5.93 (1.5), 3.53 (2), 1.77 (4), 1.02 (10), 0.287 (100).
- T is NOT a global contraction: R=100 fp is a repeller (rho(J_T)=1.642), genuine 2-cycle
  (0.4657,0.5343) <-> (0.4970,0.5030); R=50 rho(J_T)=1.478; R=4 max grid pair ratio 1.59 (task-stated 2.3 not reproduced).
- Exact remaining gap: Lemma A (g1' > g2' on the common range, R-uniform), Lemma B (h endpoint signs), Lemma C (coverage).
- Falsification extras: R=1.02 (good root (0.420084, 0.579916)) and R=1000 (good root (0.496261, 0.503739),
  h' = 0.755 at fp) added this session; fptable R=50/100 rows (a~0.002, b~0.997) identified as spurious
  residual roots (zeros of f at (0.4196, 0.5804), not sign-consistent) and excluded.
- Key numbers reproduced: R=4 fp (0.451485465757, 0.548514534243), lambda = (6.10928, 38.72326),
  D = 32.613983618, J_T = [[-0.14504, 0.41606],[0.41606, -0.14504]], rho = 0.5611.


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
