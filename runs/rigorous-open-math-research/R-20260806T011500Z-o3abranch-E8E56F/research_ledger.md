# Research ledger: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

Timestamps are approximate (UTC, 2026-08-06).  Entries record concrete
experiments, findings, and failures.  Computational claims are evidence only
unless marked PROVED with a reference to candidate_proof.md.

## Phase 0: setup and contract (inherited from the checkpoint, completed here)
- R-001: read task packet Q-20260806-o3a-branch-E8E56F and the authoritative
  source runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md
  (T1-T4, Lemma A/B/C); read prior-run ledger, obligation graph, approach
  registry, and papers/fundamental_gap.txt (AEH v2).  Re-verified AEH Lemmas
  2.1/2.2 (FH; Wronskian monotonicity of v and single-interval {f > 0}).
- R-002: wrote problem_contract.md and repro_manifest.md; set up
  reproducibility/ (agentB_lib.py copy, vec_lib.py, clean_lib.py,
  closed_deriv.py, exploration scripts).  Contract corrections: packet's
  "R-uniform lower bound" flagged as likely false (numerically min h' -> 0);
  source typo y_k(0)=1 -> y_k'(0)=1 (normalization-invariant objects
  unaffected); Lemma B endpoints sharpened to a0/b0 diagonal structure.

## Phase 1: audit of the FH formula and T3 (this continuation)
- R-101: audit_fh_t3.py at (a,b,R) = (0.42, 0.56, 4).  First attempt at the
  FH derivative using the naive formula d lambda/d eps = -int rho_eps u^2 dx
  (without the eigenvalue factor) FAILED to match finite differences
  (predicted dD/da = -1.69 vs actual +38.89).  Root cause: the correct
  formula for -y'' = lambda rho y with int rho u^2 = 1 is
  d lambda/d eps = -lambda int rho_eps u^2 dx (the eigenvalue factor lambda
  is present; re-derived by differentiating the Rayleigh quotient).
  With the factor, d lambda_1/da = 3*5.2448*1.0639 = 16.739 matches FD
  16.739241; d lambda_2/da = 55.627 matches FD 55.626551; hence
  dD/da = -(R-1) R1 = +38.88731049 exactly as in the source (tool file
  residual-exactness.md).  CONCLUSION: the source's FH formula is CORRECT;
  my initial doubt was my own error (dropped lambda factor).  Recorded as
  P1 (candidate_proof.md).
- R-102: audit3_hessian.py: T3 re-verified at 4 points (sum dR1/db + dR2/da
  ~ 1e-8, including the R=4 fp).  Hessian-of-D negative-definiteness test on
  coarse grids over the triangle: MANY violations (e.g. D_bb > 0 for
  a ~ 0.08), so a global Hessian argument is FALSE; only branch-restricted
  signs can be expected.  Recorded the correct reduction (P3): on the
  branches, g1' = -D_aa/D_ab, g2' = -D_ab/D_bb; at the fp these are the
  branch formulas; h' > 0 at the fp iff the Hessian is negative definite at
  the fp (verified: det Jres = -107576 at R=4 fp).

## Phase 2: large-R fixed-point scan (good-root checked)
- R-103: largeR_scan.py (2-parameter least squares over many seeds, absolute
  residual tolerance 1e-6).  Produced CLEAN results for R in {50..1e4}:
  unique good root each; delta = 1/2 - a_fp: 0.0159 (50), 0.0115 (100),
  0.0082 (200), 0.00526 (500), 0.00374 (1000), 0.00169 (5000),
  0.00119 (1e4).  delta*sqrt(R) ~ 0.112..0.119 -> ~0.12.  h'(fp): 0.977 (50)
  .. 0.717 (1e4).  FAILURE: at R = 1e5 and 1e6 the scan returned SPURIOUS
  "fixed points" ((0.4, 0.6) at 1e5, (0.48, 0.52) at 1e6) with residual
  ~2.6e-7 (not zero at the right scale) and v(a) ~ +1 (no sign pattern:
  f < 0 everywhere, no zeros).  These are least-squares minima of the
  residual, not roots.  LESSON: absolute residual tolerance is scale-
  dependent; use relative checks and verify zeros of f via v.
- R-104: fp_largeR.py (1-parameter solve on the symmetric line
  R1(u, 1-u) = 0, exploiting T2: the fixed point, if unique, is symmetric).
  Clean results for R up to 1e7: a_fp(1e7) = 0.499962077951,
  delta*sqrt(R) -> 0.1199; lambda_1 -> 0 (0.00527 at 1e7), lambda_2 -> 4 pi^2
  (39.477 at 1e7), D -> 4 pi^2 (39.4717); g1'(fp) -> ~1.410, g2'(fp) ->
  ~0.709, h'(fp) -> ~0.701; A = -C exactly at the fp (reflection symmetry),
  so g1'(fp)*g2'(fp) = -A/C = 1 (verified to ~1e-12).  A, B, C at the fp
  scale like ~1/sqrt(R).
- R-105: minhp_largeR.py: min h' over the common range [a0, b0]:
  R=100: min 0.2933 at a = 0.5402; R=1000: min 0.01594 at a = 0.5736;
  R=1e4: min -0.00320 at a = 0.5736 (NEGATIVE!).  FIRST SIGN that Lemma A
  fails for large R.

## Phase 3: verification of the Lemma A falsification (CE-1)
- R-106: verify_hp.py: high-precision check at R = 1e4, a = 0.57364.
  Branch points g1 = 0.577383792, g2 = 0.574785110 (residuals ~1e-14,
  v-signs correct).  h' via FD with h in {1e-6, 3e-6, 1e-5, 3e-5, 1e-4}:
  h' = -0.003203 in all cases (stable).  Direct h values at a = 0.5730..0.5744
  decrease monotonically (2.600720e-3 -> 2.596231e-3), confirming h' < 0.
- R-107: crosscheck_hp.py with the PRIOR-RUN solver (agentB_lib, different
  implementation): R=1000: h' = +0.015927 > 0; R=1e4: h' = -0.003203 < 0;
  R=1e5: h' = -0.001190 < 0 at a = 0.57364.  Agreement with clean_lib.
- R-108: closed_check.py: closed-form implicit derivatives (no branch FD) at
  R = 1500, a = 0.57364: g1' = +1.020553, g2' = +1.020897, h' = -0.000344.
  Third independent method confirms h' < 0.
- R-109: threshold.py: h'(0.57364) as a function of R:
  R=1200: +0.00466; 1500: -0.00034; 2000: -0.00286; 3000: -0.00392;
  5000: -0.00389; 7000: -0.00359.  Threshold R* in (1200, 1500), ~1350-1400.
  |h'| peaks around R ~ 3000-4000 then decays.
- R-110: ode_check.py: fully independent ODE-shooting check (solve_ivp, no
  secular equation) at R = 1e4, a = 0.57364: R1(a, b) crosses zero near
  b ~ 0.5774-0.5778 with v(a) > 0 (good branch 1); R2(a, b) crosses zero
  near b ~ 0.5752 with v(b) < 0; h > 0.  The ODE grid resolution (~2.5e-4 in
  x) is too coarse to resolve h' = -0.0032 at the needed precision, so the
  ODE check confirms the branch structure qualitatively but not the sign of
  h'.  CONCLUSION (R-106..R-110): Lemma A (pointwise, all R) is FALSE for
  R >= ~1400; the falsification is robust to solver, FD step, and method.
- R-111: h_trace2.py: h over the common range at R in {1000, 3000, 1e4, 3e4,
  1e5}: EXACTLY ONE zero of h for each R, located at a_fp(R) (0.496261,
  0.497828, 0.498806, 0.499309, 0.499621).  h(a0) < 0 < h(b0).  So O3a
  (unique fixed point) is NOT refuted, despite Lemma A failing.

## Phase 4: right-end structure (dip and recovery)
- R-112: h_tail3.py: R = 1e4, tail [0.52, b0]: h increases to peak
  h = 2.6415e-3 at a ~ 0.5517, then decreases to h(b0-) = 2.5760e-3
  (dip 6.6e-5); h' < 0 on [0.5532, 0.5789] (width ~0.026); min h' = -3.45e-3.
  h stays positive; h(b0) = 3.795e-3 (fine scan).
- R-113: h_tail5.py: R = 1e5 and 1e6, tail [0.55, b0-]: h decreasing over
  [0.55, ~0.5743] with h' ~ -1.19e-3 (1e5) and -0.0004 (1e6); h > 0
  throughout (2.5e-4 .. 8.3e-4).  Continuation-based branch solving failed
  beyond a ~ 0.5743 at R = 1e5 (bracket issue; resolved conceptually: near
  b0 the good branches lie within ~1.5e-3 of a, below the coarse scan
  resolution).
- R-114: h_recovery.py: attempted the recovery region [0.5745, b0] at
  R = 1e5 with the fast solver; coarse scans MISS the narrow roots (branches
  within ~1e-3 of a); a fine scan near b0 found a SPURIOUS root of
  R1(b0, .) at h ~ 1.15e-5 with v(a) < 0 (excluded by the good-root check).
  LESSON: near b0 the good branch-1 root is at b = b0 + h(b0) with
  h(b0) ~ 0.38/sqrt(R); only fine scans with v-checks find it.
- R-115: hb0_fine.py / hb0_fine2.py / hb0_cfg.py: h(b0) = g1(b0) - b0:
  R=1000: 1.196e-2; 3000: 6.919e-3; 1e4: 3.795e-3; 3e4: 2.193e-3;
  1e5: 1.2017e-3; 3e5: 6.940e-4; 1e6: 3.801e-4; 1e7: 1.2015e-4.
  h(b0)*sqrt(R) = 0.3795..0.3801 (converging to ~0.38).  h(b0) > 0 to 1e7.
- R-116: misc_checks.py: R = 1e4 fine scan near the peak: h' crosses zero
  between a = 0.552 (h' = +5.5e-5) and a = 0.553 (h' = -2.2e-4): peak at
  a ~ 0.5523.

## Phase 5: summary of proof attempts (all recorded)
- Attempted proof of Lemma A via Hessian negative definiteness: FAILED
  (Hessian not negative definite globally; branch-restricted signs unproved).
- Attempted proof of Lemma A via second-order spectral sums: NOT CLOSED
  (same obstruction as the prior run; no clean closed form; the Green
  function representation was identified as a possible route but not
  completed).
- Attempted proof of Lemma B via R -> 1+ perturbation: base facts proved
  (P4), boundary-layer analysis not completed.
- Attempted proof of Lemma C: no new idea beyond single-component branch
  scans; not completed.
- No attempt produced a full proof of the (corrected) uniqueness claim.

## Phase 6: artifact writing
- R-117: wrote status_and_literature.md, obligation_graph.md,
  approach_registry.md, research_ledger.md, counterexample_log.md,
  candidate_proof.md, audit_report.md; updated problem_contract.md
  (revision section) and repro_manifest.md; created run-manifest.json.

## Phase 7 (continuation, 2026-08-06): rigorous certificate and structure audit
- R-118: re-ran closed_check.py and threshold.py; reproduced CE-1
  numbers exactly (g1=0.58327448, g2=0.57600536, h=+7.269117e-03,
  h'(1500,0.57364)=-3.44e-4; threshold R* in (1200,1500)).
- R-119: amax1_scan.py / amax1_scan2.py: Gamma_1 extends beyond b0 for
  R in {1e3, 1e4, 1e5} (good branch-1 roots exist at a = b0 + 0.02;
  a_max1 > b0).  h(b0) values reproduced: 1.1962e-2 (1e3), 3.7951e-3
  (1e4), 1.2018e-3 (1e5).  Common-range right end beta = b0 for large R.
- R-120: dbg_r2profile.py / dbg_r2profile2.py: DISCOVERY - at
  (R, a) = (1500, 0.57364) the equation R2(a,b) = 0 with v(b) < 0 has
  THREE solutions (b ~ 0.5737868, 0.5743718, 0.5760054), all satisfying
  b = x_+ of their own config.  Only the third is the main-sheet branch
  value (component through (b0, b0)); the extra sheets have v(a) < 0
  (a != x_-, R1 != 0), hence are not sign-consistent fixed points.
  Consequence: Lemma C's informal "only branch components" phrasing must
  be read as fixed-point-relevant components; O3a unaffected.
- R-121: dbg_trace_branches.py: continuation from the R=1 endpoints
  confirms g1(0.57364) = 0.58327448 (main sheet through (a0,a0),
  v(a) > 0) and g2(0.57364) = 0.57600536 (main sheet through (b0,b0),
  v(b) < 0).  CE-1's branch points are on the main sheets.
- R-122: cert_ce1.py development.  FAILURES along the way (all
  recorded): (a) mpmath.iv has no acos -> range check via cos
  monotonicity; (b) root brackets must lie above a (b > a) and must
  enclose the main-sheet root only (R2 has 3 roots in (0.574, 0.58) at
  R=1500); (c) AD bug 1: IAD arithmetic crashed on `iv_interval * IAD`
  patterns (mpmath.iv raises NotImplementedError instead of
  NotImplemented) -> rewrote all AD expressions with IAD on the LEFT;
  (d) AD bug 2: ad_sec/_norm_ad used Rm = R (1500) as the barrier
  wavenumber m = sqrt(R) -> sec partials off by factor ~m; (e) AD bug 3:
  _norm_ad's final line used I2 * Rm (m) instead of I2 * Rd (density R)
  -> norm value wrong by factor ~R/sqrt(R); (f) initial ir1/ir2 dropped
  the s^2 factors (sin^2(s a)/n vs sin^2(s a)/(s^2 n)).  Each bug was
  caught by comparing AD partials against finite differences
  (dbg_ad_vs_fd.py, dbg_norm_ad.py, dbg_sec_partials.py).
- R-123: FINAL CERTIFICATE PASSES.  cert_ce1.py at R=1500 and R=1e4,
  a* = 0.57364: root enclosures width ~5e-28; g1' in [1.0205529, ...],
  g2' in [1.0208959, ...], h' in [-3.4298e-4, -3.4298e-4] < 0 (R=1500);
  h' in [-3.2030e-3, -3.2030e-3] < 0 (R=1e4).  All sign checks
  (sec_s1, sec_s2, den1, den2, dR1/db, dR2/db) sign-definite; good-root
  checks certified (v(a*) > 0 at b1, v(b2*) < 0).  Output saved to
  cert_ce1_output.txt.  CE-1 is now a RIGOROUS refutation of Lemma A
  (upgraded from float64 evidence).
- R-124: updated problem_contract.md, counterexample_log.md,
  audit_report.md, status_and_literature.md, obligation_graph.md,
  repro_manifest.md, run-manifest.json with the certificate and the
  multi-sheet structural finding.  G1 (exact certificate for CE-1) is
  CLOSED; remaining gaps G2-G4 unchanged.

## Phase 8 (continuation handoff, 2026-08-06): finalization and consistency repairs

- R-125: finalization of this run (handoff continuation).  Actions:
  (a) re-ran cert_ce1.py end-to-end: CERTIFICATE PASS at R = 1500 and
  R = 1e4 (root enclosures width ~5e-28, h' < 0 with identical intervals);
  (b) fixed a cosmetic label bug in cert_ce1.py ({R:.0e} printed the R =
  1500 case as "2e+03"; the computed parameters were always correct) and
  regenerated cert_ce1_output.txt (values unchanged);
  (c) repaired dbg_ad_vs_fd.py (ad_r1/ad_r2 now get the Rd argument; y_at
  called with its correct signature; added the r2 AD-vs-FD cross-check):
  AD partials agree with finite differences to ~1e-8;
  (d) fixed a stale G1 entry in status_and_literature.md Section 5 (now
  reads CLOSED, consistent with audit_report.md);
  (e) normalized cert_ce1_output.txt to UTF-8 no BOM (was UTF-16LE from
  PowerShell redirection);
  (f) tidied AGENTS.md: removed the duplicate nested "## 工作日志" header
  left at the end of the file by the earlier append (session 23 log entry
  now sits at the end of the single 工作日志 section);
  (g) regenerated run-manifest.json (71 entries) and verified every
  sha256/bytes pair matches the files on disk;
  (h) encoding audit of all touched files: UTF-8 no BOM, 0 ASCII '?'
  (the two '?' bytes in AGENTS.md are pre-existing quoted references to
  earlier encoding corruption in sessions 16/18, not corruption).
  No change to any mathematical claim; G1 remains CLOSED, G2-G4 open.
