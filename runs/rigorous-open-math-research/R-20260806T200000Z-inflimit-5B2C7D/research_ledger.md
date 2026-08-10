# Research ledger

Run: R-20260806T200000Z-inflimit-5B2C7D
Task: Q-20260806-inflimit-5B2C7D (INF R->infinity limit for D = lambda_2 - lambda_1
over the symmetric well family [R,1,R]).
All files ASCII punctuation, UTF-8 without BOM.

## Timeline and entries

### R-001 [2026-08-06, handoff checkpoint]
- State inherited: problem_contract.md complete and audited; T2 (uniqueness and
  minimality of u*) complete via exact sympy chain (07_part1_symbolic.py); T3
  (verified value) complete via mpmath.iv (05_interval_value.py, margin vs 3pi^2
  >= 4.664947); certified mid-left/right-sliver bounds complete (08_certified_part2.py)
  EXCEPT M4 (deep sliver) which is VACUOUS because the underlying Lemma 9 is FALSE.
- False Lemma 9 recorded: claimed Rayleigh-comparison bound gap >= 3pi^2 R / (...)
  with c = (R-1)u^2/2; refuted at (R=1e6, u=1e-3): claimed ~2.41e5, true gap
  (mu2-mu1) = 6276.97. Do NOT reuse the c-based bound.
- Missing artifacts: candidate_proof.md (0 bytes), status_and_literature.md,
  obligation_graph.md, approach_registry.md, counterexample_log.md, audit_report.md,
  reproducibility/README.md, reproducibility/exploratory/.

### R-002 [2026-08-06, probe tooling audit]
- Bug found in earlier probe scripts: secular-equation bisection without pole
  detection converges to tan-poles (light-block phase z = sqrt(mu/R)(1/2-u) crosses
  pi/2, pi, 3pi/2, 2pi for small w = u sqrt(R)); several earlier probe values were
  invalid branch artifacts. Robust method: transfer-matrix root scan (y1(mu) = 0
  with M[0][1] component), validated against the uniform string (mu_k = (k pi)^2 R).
- Deep-sliver landscape at R=1500 (transfer matrix, all parity-verified):
  w=0.02: gap=44412.6; w=0.5: 2573.3; w=1.0: 238.56; w=2.0: 91.73. Gap decreases
  in w (= increases in u) at fixed R; minimum at the corner (R0=1500, w=2) with
  gap 91.7263 >= 25.
- Gap at fixed w increases in R: w=2: 91.7 (1500), 127.2 (3000), 227.4 (1e4),
  2226.5 (1e6); w=1: 238.6 (1500) to 6277 (1e6); w=0.5: 2573 (1500) to 383905 (1e6).

### R-003 [2026-08-06, FH paradox resolved - IMPORTANT]
- Apparent contradiction: standard FH formula dlambda/du = -lambda*int(rho_dot y^2)
  seemed to give 0 for the symmetric well (mode symmetric => y(u)^2 = y(1-u)^2),
  while exact secular-IFT and transfer-matrix FD gave dlambda1/du = -181.25522 at
  (R=1500, u=1/sqrt(R)). Resolved: SIGN ERROR in rho_dot. As u increases, BOTH
  heavy blocks grow: rho_{u+du} - rho_u = (R-1)*1_{[u,u+du) union (1-u-du,1-u]}
  (positive everywhere), NOT the previously assumed difference of two opposite
  signs. Hence
      dlambda_k/du = -lambda_k*(R-1)*(y_k(u)^2 + y_k(1-u)^2) < 0,
  i.e. rho is pointwise increasing in u, lambda_k decreasing in u, mu_k = R*lambda_k
  decreasing in u. Verified numerically: FH value -181.25522 matches IFT exactly.
- Consequences: (a) mu_k(R,u) is provably decreasing in u (monotone-corner scheme
  has the u-half rigorously); (b) gap(u) monotonicity in u needs y2(u)^2 > y1(u)^2
  at the interface (FH for the difference); (c) the parity of the mode no longer
  kills the FH derivative.
- Verification of eigenfunction identity Q = lambda*B for the exact piecewise
  solution: PASS to 1e-28 (probe_exact2). y(u) = y(1-u) exactly, y'(1/2) = 0
  (even mode), as expected.

### R-004 [2026-08-06, in progress]
- Checking mu_k monotonicity in R (pointwise rho increase in R gives lambda
  decrease; mu_k = R*lambda_k needs numerical/proof verification) to complete the
  monotone-corner scheme; if mu_k is not monotone in R, fall back to a 1D
  certified scan (deep sliver reduces to the w=2 boundary via gap-monotonicity in
  u, plus gap increasing in R at fixed w) or certified 2D cells with explicit
  Lipschitz corrections.
- Open sub-question: prove gap(R,u) decreasing in u on the deep sliver (FH:
  d gap/du = 2R(R-1)*(y1_n(u)^2 - y2_n(u)^2); need y2_n(u)^2 > y1_n(u)^2, to be
  verified and proved) and gap increasing in R at fixed w.
### R-005 [2026-08-06, fixed-u monotonicity in R - CORRECTION to earlier handoff]
- Re-verified with fresh high-precision transfer-matrix runs at FIXED u = 2/sqrt(1500):
  R=1500: mu1=914.2045 mu2=1005.9308 gap=91.7263; R=1600: 914.9180/1006.1662/91.2481;
  R=2000: 917.0410/1006.8710/89.8300; R=3000: 919.8310/1007.8082/87.9772; R=1e4: 923.6608/1009.1152/85.4544.
- CONCLUSION: mu_k is INCREASING in R at fixed u (matches FH dmu/dR = lambda * L_light > 0, verified
  to 1e-6 against finite differences). The earlier handoff claim "dmu1/dR|u ~ -0.378" is REFUTED;
  it came from probe_fhR3 whose dmu/dR formula was wrong (recorded as lesson). Correct FH:
  dmu_k/dR|u = lambda_k * int_light y_k^2 dx (L2(rho)-normalized), always > 0.
- IMPORTANT CONSEQUENCE: the GAP at fixed u DECREASES in R (91.7263 -> 85.4544). So a corner scheme
  in (R,u) coordinates must not assume gap-monotonicity in R; only mu_k monotone (separately) and
  gap-monotonicity in u (see R-006) hold.

### R-006 [2026-08-06, deep-sliver monotonicity directions - verified]
- w-monotonicity: dG/du|R < 0 everywhere on the deep sliver (R=1500: -1950.20 at w=2, -16948.9 at
  w=1, -1193985 at w=0.5). Sign condition H = mu2*y2(u)^2 - mu1*y1(u)^2 > 0 holds on the whole scan
  grid (R in {1500,2000,1e4,1e5}, w in {0.5,1.0,1.5,1.8,2.0}); min H = 0.65050 at (1500,2.0),
  relative margin 5.55%. H grows fast away from the corner (w=0.5, R=1500: rel margin 114%).
- R-monotonicity at fixed w: dG/dR|w > 0 everywhere: +0.02845 at (1500,2), +0.08066 at (1500,1),
  +1.34790 at (1500,0.5). (Handoff value +0.086 at (1500,2) is inaccurate; correct is +0.0285.)
  Decomposition: dG/dR|w = [lam2*L2light - lam1*L1light] + u(R-1)*H/R; first term negative
  (-0.00512 at corner), second positive (+0.0336), net positive.
- G(R,2) along w=2 curve: 91.7263 (1500), 127.1702 (3000), 227.4387 (1e4), 707.6150 (1e5),
  2226.5252 (1e6). Monotone increasing in R, consistent with dG/dR|w > 0.

### R-007 [2026-08-06, NEW: exact two-term asymptotics at fixed w - key for the tail]
- With w = u*sqrt(R) fixed and R -> infinity: both scaled eigenvalues satisfy
  mu_k = R*nu_k with nu_k -> nu0 = pi^2/(4w^2) (heavy-block phase sqrt(nu_k)*w -> pi/2),
  and G(R,w)/sqrt(R) -> g_inf(w) = 2*pi/(w^2 * sin(pi/(2w))) for w in (1/2, 2].
- Derivation: first-order expansion of the even/odd secular equations
  cot(sqrt(nu1)*w) = R^{-1/2}*tan(z1), tan(sqrt(nu2)*w) = -sqrt(R)*tan(z2),
  z_k = sqrt(nu_k)*(1/2 - w/sqrt(R)); gives delta_1 = -(pi/w^2)*tan(pi/(4w)),
  delta_2 = (pi/w^2)*cot(pi/(4w)), g_inf = delta_2 - delta_1.
- Numerical verification (mpmath findroot from asymptotic initial guesses):
  w=2: g_inf=2.221441469; G/sqrt(R) = 2.22652522 (1e6), 2.22304415 (1e7), 2.22194779 (1e8).
  w=1: g_inf=6.283185307; G/sqrt(R) = 6.27696535 (1e6), 6.28120473 (1e7), 6.28255762 (1e8).
  w=1.5: g_inf=3.224532203; G/sqrt(R) = 3.22800576 (1e6), 3.22562577 (1e7), 3.22487753 (1e8).
- Consequence: g_inf(w) is minimized at w=2 with value pi/sqrt(2) = 2.22144; the tail bound
  G >= g_inf(w)*sqrt(R) - C >= 2.22144*sqrt(1500) - C = 86.03 - C >= 25 requires C <= 61.
  Numerically the remainder |G - g_inf*sqrt(R)| is O(1), <= ~10 at R=1500 across w. So a rigorous
  O(1) remainder bound C < 61 on [1/2,2] x [1500,inf) closes the tail.

### R-008 [2026-08-06, exact eigenfunction data + perturbation sanity check]
- Exact formulas (L2(rho)-normalized), corrected factor-2 bug in earlier probe:
  A_k^2 = 1/(2*(R*I_k + ratio_k^2*J_k)); y_k(u)^2 = A_k^2*sin^2(theta_k);
  L_{k,light} = ratio_k^2*J_k/(R*I_k + ratio_k^2*J_k);
  I_k = u/2 - sin(2*theta_k)/(4*kh); J_1 = (1/2-u)/2 + sin(2*z1)/(4*kl) (even),
  J_2 = (1/2-u)/2 - sin(2*z2)/(4*kl) (odd); theta_k = sqrt(mu_k)*u, z_k = sqrt(mu_k/R)*(1/2-u).
  Verified: FH dG/dR|u = lam2*L2light - lam1*L1light matches finite differences to 1e-6.
- Sanity check that killed a naive route: regular perturbation of the flat string is INVALID on
  the deep sliver. At (R=1e6, w=1): lambda_1 = 2.464 vs flat pi^2 = 9.87; the first mode is
  concentrated on the heavy blocks (singular limit, light-block phase -> 0 but mass matters).
  Do not use first-order perturbation in (R-1)*u^3 for lambda_k on the deep sliver.
- Deep-sliver lemma route (chosen): Lemma D1 = rigorous two-term expansion
  G(R,w) = g_inf(w)*sqrt(R) + O(1) with explicit uniform remainder < 61 on [1/2,2] x [1500,inf);
  Lemma D2 = w <= 1/2 regime bound G >= 25; corner/intermediate values certified by interval
  arithmetic. Alternative: certified 2D cells + Lipschitz on [1500,R_tail] x [w_min,2] plus the
  D1/D2 analytic regimes. Monotonicity proofs (R-006) remain the fallback if D1 remainder is hard.

### R-009 [2026-08-06, w <= 1/2 branch structure - resolved apparent contradiction]
- Verified by fine scans (4 roots, N=600k) at w=0.4: nu1=mu1/R -> 9.84690 (R=1e6), 9.86732 (R=1e8),
  approaching pi^2 = 9.86960 from below (SLOW, error ~ c/sqrt(R), c ~ 23); nu2 -> 15.41317 (1e6),
  15.42044 (1e8), approaching pi^2/(4w^2) = 15.42134 from below. Earlier apparent contradiction
  (predicted nu1 -> pi^2/(4w^2) = 15.43) was a slow-convergence artifact; the subleading balance
  is: z1 -> pi/2 - c/sqrt(R), cot(theta1) -> 1/c > 0, theta1 = sqrt(nu1)*w -> arccot(1/c), so
  nu1 -> pi^2 exactly (not 15.43), consistently with the scan.
- Branch structure for fixed w, R -> infinity (deep sliver):
  * w in (0, 1/4]: nu1 -> pi^2, nu2 -> 4*pi^2 (flat-string regime), G ~ 3*pi^2*R.
  * w in (1/4, 1/2): nu1 -> pi^2, nu2 -> pi^2/(4w^2), G ~ c(w)*R with c(w) = pi^2*(1/(4w^2)-1),
    decreasing from 3*pi^2 (w=1/4) to 0 (w=1/2). Third eigenvalue also -> pi^2/(4w^2) (near
    degenerate pair from above: 15.46850 (1e6) -> 15.42600 (1e8)).
  * w = 1/2: degenerate/resonance case, G ~ 0.384*R (c(1/2) = 0.384 from data, NOT given by the
    (1/4,1/2) formula which gives 0; needs its own expansion).
  * w in (1/2, 2]: G ~ g_inf(w)*sqrt(R) + q(w), g_inf = 2*pi/(w^2*sin(pi/(2w))) (R-007), q from
    R-008 (eta_2 - eta_1 closed forms, verified to 1e-3 at R=1e8).
- Implication for the deep-sliver lemma: the R >= R_tail tail needs ONLY the SIGNS of
  dG/dw < 0 (H > 0) and dG/dR|w > 0 on the tail, plus the certified values at R = R_tail:
  G(R,w) >= G(R_tail, w) >= G(R_tail, 1/2) or G(R_tail, 2/sqrt(R_tail)) depending on w-regime.
  The near-1/2 degenerate value c(1/2) = 0.384 is NOT needed, only signs.

### R-010 [2026-08-06, corrected two-term coefficients - THE technical core]
- Hand-derived (sympy expansion had a sign error; hand calculation verified numerically):
  with eps = 1/sqrt(R), nu_k = nu0 + delta_k*eps + eta_k*eps^2, nu0 = pi^2/(4w^2),
  delta_1 = -(pi/w^2)*tan(pi/(4w)), delta_2 = (pi/w^2)*cot(pi/(4w)), g_inf = delta_2 - delta_1.
  eta_k = delta_k^2*w^2/pi^2 + beta_k*pi/w^2, where for k=1 (even):
  beta_1 = -p_1*sec^2(pi/(4w)), p_1 = delta_1*w/(2*pi) - pi/2;
  for k=2 (odd): beta_2 = -alpha_2^2*p_2*sec^2(pi/(4w)), alpha_2 = 1/tan(pi/(4w)),
  p_2 = delta_2*w/(2*pi) - pi/2.
  G(R,w) = g_inf(w)*sqrt(R) + q(w) + O(R^{-1/2}), q(w) = eta_2 - eta_1.
- Verification (R=1e8): w=0.8: eta1=43.3566 vs num 43.3280; eta2=8.8856 vs 8.8862; q=-34.471 vs
  -34.442. w=1.0: q=-6.28319 vs -6.27684 (limit -2*pi). w=1.2: q=0.26821 vs 0.27138.
  w=1.5: q=3.45103 vs 3.45328. w=1.8: q=4.63881 vs 4.64100. w=2.0: q=5.06092 vs 5.06319.
- Tail slack at w=2 (the worst case): g_inf(2)*sqrt(R) + q(2) = 2.22144*sqrt(R) + 5.06; for
  R >= 1500 this is >= 91.06 and for R >= 1e5 >= 707.5. So the curve g(R) = G(R,2/sqrt(R))
  needs only an O(1) remainder bound C < 61 on [1500,inf) (or C < 680 on [1e5,inf)) to certify
  g(R) >= 25. Numerically the remainder after two terms is <= ~11 across R >= 1500 at w=2.

### R-011 [2026-08-06, manager check-in 3 - status snapshot]
- Status: T2 (unique minimizer of Dbar) COMPLETE via 07_part1_symbolic.py exact chain; T3
  (verified value) COMPLETE via 05_interval_value.py (u* width 2e-20, Dbar(u*) in
  [24.9438661384324768968, 24.9438661384324769084], margin >= 4.664947); T1 OPEN.
- T1 sole blockers: (i) deep-sliver lemma G >= 25 on R >= 1500, u <= 2/sqrt(R); (ii) certified
  uniform-K on middle band [0.1, 0.475] (numeric M6 grid max <= 1273 << 5e4, needs certification
  or analytic K).
- candidate_proof.md: still 0 bytes, not started (planned after deep-sliver + uniform-K close).
- Current route: (a) P1-only corner scheme for bounded deep sliver [1500, RTAIL]; (b) analytic
  proof of H > 0 (the crux) for dG/du < 0 and dG/dR|w > 0; (c) tail via monotonicity; (d)
  uniform-K certification.
- This check-in: record status; no new findings beyond R-005..R-010 yet; continue research.
### R-012 [2026-08-06, deep-sliver reduction to a single analytic lemma - key progress]
- NEW REDUCTION (verified numerically, structure for the proof): the deep sliver reduces to the
  1D certified curve at R0 = 1500 plus ONE analytic lemma (dG/dR|w > 0):
    * G(R,u) with w = u*sqrt(R): if dG/dR|w > 0 on R >= 1500, w in (0,2], then
      G(R,u) >= G(1500, w/sqrt(1500)) = G(1500, u*sqrt(R/1500)).
    * Since u*sqrt(R/1500) <= 2/sqrt(1500), the 1D curve G(1500, .) on (0, 2/sqrt(1500)]
      suffices; its min is at the corner u = 2/sqrt(1500): G = 91.7263 >= 25.
- The 1D curve can be certified WITHOUT H>0: P1-only cells (mu_k exactly decreasing in u by FH,
  R-003) give G(u) >= mu2_lo(u_{i+1}) - mu1_hi(u_i) on cells; the first cell [0,u_1] uses the
  flat-string bound mu2 >= 4*pi^2 (comparison lambda2 >= 4*pi^2/R) and mu1 <= R0*pi^2. So the
  curve certification is fully rigorous (computational).
- THETA FORMULATION (verified to 12 digits): with eps = 1/sqrt(R), u = w*eps,
  c = 1/(2w) - eps, theta_k solve
    even: cot(theta1) = eps*tan(c*theta1);  odd: tan(theta2) = -tan(c*theta2)/eps,
  and G = (theta2^2 - theta1^2)/(w^2*eps^2) =: A/(w^2*eps^2). Then
    dG/dR|w > 0  <=>  dG/deps < 0  <=>  eps*dA/deps < 2*A.
- VERIFIED (40-digit numerics): eps*dA/deps - 2A < 0 on the full grid
  w in (0,2], R in {1500,1e4,1e5,1e6,1e8} with worst slack 0.93 at (w=2, R=1500)
  (slack = 2 - eps*dA/deps/A: 0.93 at w=2; >= 1.5 for w <= 0.5; >= 1.0 for w >= 0.75).
  This is THE remaining analytic crux for the deep sliver.
- ELEMENTARY BOUND for w in (1/2, 2], eps <= 1/sqrt(1500) (hand-derived, numerically validated,
  min 81.61 >= 25 at the corner):
    G >= [tan x + cot(x + B2/(2w))]*(1 - eps^2*M^2/3)*(pi - eps*tan x)/(w^2*eps),
    x = pi/(4w), B2 = eps*cot(x - eps*pi), M = cot(x - eps*pi),
  valid where x - eps*pi > 0 and x + B2/(2w) < pi/2 (holds on w in (0.5, 2], eps <= eps0;
  the w=1/2 endpoint needs the degenerate branch). Derivation: two-sided bounds on
  delta_k = theta_k - pi/2 from the secular equations (delta1 >= -eps*tan x;
  delta2 >= arctan(eps*cot(x + B2/(2w)))), giving A >= (delta2-delta1)*(pi - eps*tan x).
- CRITICAL CORRECTION (seed bug found this session): the "certified corner" diagnostics for
  w <= 1/2 used seed max(pi^2/(4w^2), 4*pi^2)*R*0.9999 for mu2, which converges to the FOURTH
  eigenvalue branch (4*pi^2*R) at w <= 1/2, NOT the second. Correct second eigenvalue at
  (R=1e6, w=0.5): mu2 = 9.8696e6 (nu2 -> pi^2), G/R -> 0.384 (R-009 correct; the "G ~ 3*pi^2*R"
  numbers printed earlier for w=0.5 at large R were the 4th-eigenvalue branch). At
  (R=1e6, w=0.4): mu1 = 9.8469e6, mu2 = 1.5413e7 (nu2 -> pi^2/(4w^2) = 15.42), G/R -> 5.553.
  Transfer-matrix scan confirms: roots at nu ~ 15.413 and 15.421 (near-degenerate pair nu2, nu3).
- Corrected A-limit: A = w^2*eps^2*G -> A_inf(w): pi^2*(1/4 - w^2) for w in (1/4, 1/2),
  3*pi^2*w^2 for w in (0, 1/4], and A_inf(1/2) = 0.096 (degenerate, c(1/2) = 0.384).
- H values from this session (bisect-based, cross-checked vs transfer matrix and FH identity
  dG/du = -2(R-1)H to 1e-5): H > 0 on R >= 1500, w <= 2, min at corner (1500,2) = 0.65050
  (rel margin 5.55%); H at w=0.5: 398 (1500), 1021 (1e4), 3192 (1e5), 10008 (1e6) - grows.
  NOTE: the w<=1/2 H values at R>=1e5 in R-006-style grids are UNRELIABLE (the bisect bracket
  for the odd mode is branch-sensitive); do not cite them. H > 0 is NOT needed for the new
  deep-sliver architecture (only for the optional dG/du < 0 route).
- Corner scheme diagnosis: passes on [1500, 1e5] with ratio 1.01 (worst margin 57.5 at the
  first cell) but FAILS near R ~ 1e6 because d(mu1)/dR along the w=2 curve (~0.617) exceeds
  G/DeltaR (G ~ 2.22*sqrt(R)); the 2D P1-only scheme also fails near u -> 0 (mu1(R2,0) = R2*pi^2
  is too crude). Hence the 1D-curve + dG/dR|w>0 architecture is the right one.
### R-013 [2026-08-06, manager check-in 4 - status + MAJOR deep-sliver progress]
- Status: T2 COMPLETE (07_part1_symbolic.py), T3 COMPLETE (05_interval_value.py),
  T1 OPEN but the deep-sliver lemma now closes by PURELY ELEMENTARY bounds
  (no dG/dR|w>0, no H>0, no certified 1D curve needed). candidate_proof.md
  still 0 bytes (planned after deep-sliver + uniform-K close).
- CORRECTION of R-012 elementary bound: the R-012 formula for w in (1/2,2]
  [tan x + cot(x+B2/(2w))]*(1-eps^2 M^2/3)*(pi - eps tan x)/(w^2 eps) is BOGUS:
  it uses delta2 - delta1 >= delta2 + eps tan x, but delta1 >= -eps tan x gives
  delta2 - delta1 <= delta2 + eps tan x (wrong direction). Verified: at
  (R=1500, w=0.50375) the formula gives 12186 > true G = 2460 (overestimate);
  min of the formula on (0.5,2] is NEGATIVE near w=0.5. DO NOT reuse R-012 B5.
  Correct bound: A = theta2^2 - theta1^2 >= delta2^- * (pi - eps tan x),
  delta2^- = arctan(eps cot(x - eps pi/2 + c delta2^+)), delta2^+ = arctan(eps cot(x-eps pi/2)).
- NEW ELEMENTARY DEEP-SLIVER COVER (scripts 11-14, all verified <= G with 0
  violations on grids R in {1500,1e4,1e6,1e8}, ~1000 w-points each):
  * w in (0, 0.19]: G >= 3 pi^2 R - 32 pi^4 R eps w^2 / c >= 42744, c = 1/(2w)-eps.
    Chain: theta1 < pi*w (fixed-point, eps tan(pi w) > tan(pi eps w));
    theta2 = 2 pi w - eta with eta <= (eps/c)(tan(2 pi w) - 2 pi w) <= (eps/c)(2 pi w)^3
    (valid for 2 pi w <= 1.194, tan x - x <= x^3 by series); mu1 < pi^2 R, mu2 >= ...
  * w in [0.19, w_c]: G >= pi^2 R ((1-2 eps w)^-2 - 1) >= 294 (theta2 > pi/(2c) branch).
  * w in (w_c, wcap]: G >= pi^2 R (1/(4w^2) - 1) >= 25 exactly at wcap = 0.5 (1+25/(pi^2 R))^-1/2
    (theta2 >= pi/2, mu1 < pi^2 R; B3 decreasing in w, min = 25 at wcap).
  * w in (wcap, 2]: G >= max(THB, D2B); THB = (pi/2 - theta1+)(pi/2 + theta1-)/(w^2 eps^2),
    theta1- = arctan(cot(c pi/2)/eps), theta1+ = pi/2 - arctan(eps tan(c theta1-));
    D2B = delta2- (pi - eps tan x)/(w^2 eps^2) (valid where pi - eps tan x > 0).
    min max(THB,D2B) = 78.544 at (R=1500, w=1.9998); THB alone dips to 11.1 at w=2
    (needs D2B), D2B alone dips to 2.88 at w=0.503 (needs THB).
  * Tail: THB >= (3pi/4) tan(c pi/4)/(w^2 eps) (1-o(1)) >= 0.117 sqrt(R) on (0.5,2],
    so THB >= 25 for R >= 45600 analytically (theta1- >= pi/4 for w >= 1/2: proved
    via cot(c pi/2) >= tan(eps pi/2) >= eps).
- Auxiliaries verified on grids (script 13): theta1 < pi*w (w<=1/2); theta2 >= pi/2
  (w >= w_c); theta1 in [theta1-, theta1+]; delta2 in [delta2-, delta2+];
  delta1 >= -eps tan x (w>1/2). All PASS.
- Check-in answers: (1) T1/T2/T3: T2/T3 closed; T1 open, blockers now reduced to
  (a) rigorous certification of max(THB,D2B) >= 25 on [1500,45600] x (0.5,2] by
  interval cells + the analytic tail THB >= 0.117 sqrt(R), (b) uniform-K on
  [0.1,0.475]. (2) candidate_proof.md 0 B, not started; deep-sliver lemma will be
  its first written part. (3) route: certify the elementary bounds with mpmath.iv
  interval cells (script 15 planned), then uniform-K, then write candidate_proof.md.
- Ledger continuation: proceed to script 15 (interval certification) next.