# Research ledger - R-20260812T090000Z-g1prime-g2 (O-1..O-5, n>=2 gap extremal Jacobian/Hessian)

Timestamps UTC+8.  Continuation sessions of the n>=2 symmetry line
(AGENTS.md session 58 continuation 4b handoff).  All numerics EVIDENCE unless
flagged STRICT.

## R-200 (2026-08-12): reduced-cost INF/SUP scan + sign-convention audit
- Ran scripts/_gapn2_hp_scan_reduced.py at N = 600 Richardson, 9-point R grid
  (INF n=2..4, SUP n=2..4), merged JSON
  scripts/_gapn2_hp_scan_inf_reduced.json with fd_* authoritative fields.
- STRICT identities established and FD-verified (details in run_notes):
  geometric convention delta rho = -s_i delta(x-x_i) dx_i; d lambda_k/dx_i =
  +lambda_k s_i u_k(x_i)^2; dD/dx_i = -s_i f(x_i) (CORRECTS the session-51 sign
  record; zero set f = 0 unchanged); Hess(D) = -lambda_{n+1} diag(s) J at
  critical points (CORRECTS the A3 docstring sign); K := diag(1/s) J symmetric;
  det J = (R-1)^(2n) (-1)^n det K, so (G1') <=> det K > 0 <=> Hess positive
  definite; first-order Jacobian formula M~ (two minus signs corrected).
- O-3 map: SUP detJ sign (+1)^n and evK > 0 on the whole reachable range
  (smallest |evK| at R=100: 0.0156/0.0185/0.0214 for n=2/3/4); INF detJ sign
  (-1)^n and evK < 0 (softest direction 0.78 at n=3 R=75; margins decay
  exponentially, no sign change found).  Analytic (truncated) Jacobian
  UNRELIABLE near degeneracy (n=3 R=75 false sign flip retracted as
  truncation artifact; FD stable).
- O-4: INF large-R near-degenerate pair (s-gap 0.0098 at n=3 R=75 vs grid
  0.0092) stops continuation beyond n=4 R~40; (G2) fails only in the R->inf
  limit, needed only on compact ranges.
- O-5: det B != 0 numerically supported; strict proof open.  Candidate route
  via constant sign of the diagonal part of K.
- Deliverables: run_notes_2026-08-12.md; scripts _gapn2_hess_verify.py /
  _gapn2_hess_sign_and_bigR.py; tools/band-selfconsistency-equivariance.md
  updated (2026-08-12 section).

## R-201 (2026-08-12 evening): closed-form M~ diagonal, sign audit, dead ends
- (I1) STRICT partial-fraction identity: lambda_{n+1} G~_{n+1}(x_j,x_j) -
  lambda_n G~_n(x_j,x_j) = Sigma'(x_j) - 2 w_j/D - w_j D/(lambda_n lambda_{n+1}),
  Sigma'(x_j) > 0 strictly (sum over l != n, n+1 of positive terms).
- (I2) STRICT closed form: M~_{jj}/s_j = 2 w_j Sigma'(x_j) - 4 w_j^2/D, hence
  K_{jj} = sigma * 2 c |W(x_j)|/(R-1) + 2 w_j Sigma'(x_j)/lambda_{n+1}
           - 4 w_j^2/(D lambda_{n+1}), sigma = +1 SUP / -1 INF.
  Verified against one-shot spectral sums at N=800 to rel 1e-13..1e-15
  (n = 2, 3; R in {1.2, 2, 4, 10}; both modes).  Two wrong intermediate forms
  rejected by the same script (missing pole-cancellation term; wrong sign of
  u_{n+1}^2 - u_n^2).  Script: scripts/_gapn2_mtilde_diag_identity.py.
- (I3) CORRECTION: f'(x_j)/s_j = +2 c |W(x_j)|/(R-1) for SUP and -2 c |W(x_j)|
  /(R-1) for INF (the run notes' uniform "< 0" held only for INF).  Verified by
  FD at n = 2, 3, R in {1.2, 2, 4, 10}: zero violations.
- (I4) STRICT bound |W(x_j)| <= D via W = -D int rho u_n u_{n+1} + C-S.
- Dead ends (EVIDENCE, registered): Gershgorin diagonal dominance of K fails
  for R >= 2..4 (margin -38 at n=3 INF R=10); H-matrix scaling (rho(B) < 1)
  fails at n=2 INF R=4 (1.31), n=3 SUP R=4 (1.05), n=3 INF R=2 (1.36).  Both
  candidate routes for O-5 are numerically refuted on the full R range.
- New EVIDENCE: Sylvester LU pivots of K have constant sign along the branch
  (SUP all > 0, INF all < 0) for n = 2, 3, R in {1.2, 2, 4, 10}; by Sylvester's
  inertia law constant pivot signs are equivalent to (G1').  Sign patterns of
  K, K+, K- printed by scripts/_gapn2_hmatrix_probe.py.  A strict proof of the
  pivot sign remains open (most promising structural handle).
- Deliverables: run_notes_addendum_2026-08-12.md; scripts _gapn2_diag_dominance.py,
  _gapn2_mtilde_diag_identity.py, _gapn2_hmatrix_probe.py, _gapn2_pivots_bigR.py;
  tools update below.
- R-201 extension: Sylvester pivots at large R (FD, LU without pivoting) -
  INF pivots all negative on the full reachable range (n=2 R<=100, n=3 R<=75,
  n=4 R<=30; detK down to 6e-17), SUP pivots all positive at n=2/n=4 R<=100;
  spurious-root warning: direct continuation fails at R>=30 (n=3 SUP R-ladder
  probe fell onto a spurious root with mixed evK; those points are covered by
  the hp_scan fd_* fields which show evK all positive/negative).  Pattern
  constant over the full reachable range, still EVIDENCE.

## Remaining gaps
- (G1') det K > 0 on the whole solution set: STRICT diagonal closed form (I2)
  + constant f'/s sign + constant Sylvester pivot signs (EVIDENCE) are the new
  ingredients; the off-diagonal Green part of K still lacks analytic control.
- (G2) boundary exclusion: unchanged (obstructions recorded in run_notes).
- O-5 det B != 0: no strict proof; diagonal-dominance and H-matrix routes
  closed by the dead-end register above.

## R-201 (2026-08-12 evening): diagonal closed forms, sign audit, dead ends
- (I1) STRICT partial-fraction identity: lambda_{n+1} G~_{n+1}(x_j,x_j)
  - lambda_n G~_n(x_j,x_j) = Sigma'(x_j) - 2 w_j/D - w_j D/(lambda_n lambda_{n+1}),
  Sigma'(x_j) > 0; (I2) M~_{jj}/s_j = 2 w_j Sigma'(x_j) - 4 w_j^2/D; (I3)
  CORRECTION f'(x_j)/s_j = +2c|W(x_j)|/(R-1) (SUP), -2c|W(x_j)|/(R-1) (INF);
  (I4) |W(x_j)| <= D.  All FD/spectral verified (1e-13..1e-15).
- Dead ends: Gershgorin diagonal dominance (fails R >= 2..4), H-matrix
  scaling (fails n=2 INF R=4, n=3 SUP R=4, n=3 INF R=2).
- Sylvester pivots of K constant sign along the branch (SUP all > 0, INF
  all < 0) on the reachable range incl. large R (detK down to 6e-17);
  spurious-root trap at n=3 SUP R>=30 (retracted, hp_scan fd_* authoritative).

## R-202 (2026-08-12 late evening): off-diagonal closed forms + mirror sectors
- (C1)/(C2) STRICT: T_ji = M~_ji/s_i closed forms (same/cross eps-parity) via
  per-mode partial fractions + band relations; verified 1e-13..1e-15
  (n=2,3; R in {1.2,2,4,10}); resolvent identity (R) verified with exact
  per-block Gram quadrature (trapezoid O(1) fails).
- eps-structure STRICT: eps_j = (-1)^{j+1} alternating; w mirror-even,
  eps odd, (eps w) odd; eps_j = sigma s_j/(R-1).
- Mirror-sector decomposition STRICT (machine 1e-15..1e-16):
  K_e = diag(d_h) + E_e + H_e, K_o = diag(d_h) + E_o + H_o with
  E_e = c_e w_h w_h^T (c_e > 0), E_o = c_o (eps_h.w_h)(eps_h.w_h)^T (c_o < 0),
  H_e/H_o parity-masked closed forms with mirrored kernels
  Sigma'(x_i,x_j) +/- p_n Sigma_+(x_i,xbar_j).  First verification attempt
  failed due to coordinate mixup (sector basis = mirror halves, mask =
  parity classes); corrected forms all pass.
- Falsified: (P1') Hankel symmetry of K~ (rel 0.6..1.2).
- Dominance scans (EVIDENCE): SUP sufficient inequalities
  lammin(H_o-E_o)+mind > 0 and lammin(H_e+E_e)+mind > 0 hold on every scan
  point (n=2 R<=100, n=3/4 R<=10); INF naive bounds FAIL at large R
  (n=3 R>=4; n=2 R=100 borderline), detK -> 0+ as R->inf: INF needs a
  qualitative argument, no uniform margin exists.
- Sherman-Morrison reduction (exact): K_o PD iff A_o = diag(d)+H_o PD and
  |c_o| (eps w)^T A_o^{-1} (eps w) < 1; same for K_e and -K (INF).
- Sector Sylvester pivots (closed-form K): SUP all +, INF all - on every
  scan point; FD direct continuation spurious-root trap reproduced (n=3 sup
  R=10, retracted).
- (G1') still OPEN: reduced to sector quadratic-form lemmas (resolvent
  Green estimates of R_k^||/R_k^bot at band-consistent points).
- Deliverables: run_notes_addendum (deep-night extension);
  scripts/_gapn2_mtilde_offdiag_identity.py, _gapn2_sector_decomposition.py,
  _gapn2_sector_scan_{2,3}_{sup,inf}.json, _gapn2_sector_scan_4_sup.json;
  tools/band-selfconsistency-equivariance.md (deep-night section);
  tools/README.md (maintenance log).

## R-203 (2026-08-13): (G2) endpoint obstruction reduction + slope-ratio evidence
(SUPERSEDED by R-204: the sqrt(lambda)-weighted q0 convention in the
evidence lines below was mixed with the framework q0 convention; see the
R-204 bug-fix register.)
- STRICT: endpoint-collapse reduction (O-4 endpoint part).  If a
  band-consistent family has first block width w1 -> 0 on a compact R-range,
  the limit is a band-matched root of the reduced 2n-block system satisfying
  the endpoint condition q0 = c, q0 = sqrt(lambda_{n+1})|u_{n+1}'(0)|
  /(sqrt(lambda_n)|u_n'(0)|), c = sqrt(lambda_n/lambda_{n+1}).  Proof via
  continuous dependence of eigenvalues/eigenfunctions, persistence of band
  matching, and the quadratic endpoint expansion f(x) = a x^2 + O(x^4) with
  a = lambda_n u_n'(0)^2 - lambda_{n+1} u_{n+1}'(0)^2 (dividing f(x1) = 0 by
  x1^2 and passing to the limit).  Band matching on a reduced root gives
  q0 < 1; the endpoint condition q0 = c needs a quantitative separation.
- EVIDENCE (branch): q0/c > 1 along both branches for n=2 (R<=100), n=3
  (R<=30), n=4 (R<=10); quadratic expansion test f(x)/(a x^2) -> 1 at
  x = 1e-4, 1e-3; R -> 1 limit reproduces the constant-density value
  q0/c -> ((n+1)/n)^3 (3.375, 2.37037, 1.953125).
- EVIDENCE (reduced roots): random and targeted seeds give no band-matched
  reduced root and every reduced root has q0 - c > 0 (min +0.322 at n=3 SUP
  R=4; degenerate roots reproduce the ((n+1)/n)^3 signature).  Consistent
  with, but not a proof of, the finite-dimensional non-existence statement.
- Bug-fix register: eigfun_slope0 block-start coefficient (final M01 vs
  starts[bi] M01) and part_a per-R pattern were wrong; all previous slope
  numbers in the handoff are RETRACTED.  After fixes, slope ratio and
  quadratic-expansion test agree with independent checks to machine precision.
- Deliverables: run_notes_addendum_2026-08-13.md;
  scripts/_gapn2_slope_ratio.py, _gapn2_reduced_endpoint_hunt.py,
  _gapn2_endpoint_targeted.py.
- Status: (G1') OPEN; (G2) endpoint part reduced to "no band-matched reduced
  root has q0 = c" (EVIDENCE supports); (G2) interior coalescence OPEN.

## R-204 (2026-08-13, continued): convention fix + (G2) fully CLOSED STRICT
- Convention correction: the previous addendum mixed two q0 conventions
  (sqrt(lambda)-weighted q0 with the conclusion q0 = c).  Correct framework
  convention q0 := u_{n+1}'(0)/u_n'(0): a = 0 iff q0 = c.  Scripts
  _gapn2_slope_ratio.py and _gapn2_reduced_endpoint_hunt.py switched to this
  convention; all earlier sqrt-weighted q0-c evidence lines RETRACTED.
- STRICT Theorem A (block-energy identity): for any piecewise-constant rho
  with f = 0 at every jump, K = (u_n'^2 + lam_n rho u_n^2) -
  (u_{n+1}'^2 + lam_{n+1} rho u_{n+1}^2) == -2D < 0; hence q0 > 1 and
  q1 < -1 at every root of any (full or reduced) system.  FD/spectral
  verification to 1e-11 (scripts/_gapn2_kidentity_audit.py).
- STRICT Theorem C (interior simplicity): f has no point in (0,1) with
  f = f' = 0 (Cauchy-data uniqueness + Sturm interlacing).  Closes the
  interior-coalescence part of (G2) (Rolle).
- STRICT Theorem D (exact zero count, arbitrary weight): #Z(f;(0,1)) =
  2n-2 + 1_{q0>c} + 1_{q1<-c} (cell analysis of |Q| = |u_{n+1}/u_n| via
  W < 0).
- STRICT Theorem E ((G2) closed): any width -> 0 along band-consistent
  solutions on a compact R-range yields a limit string whose eigenpair has
  q0* > 1, q1* < -1 (Theorem A), hence 2n interior zeros of f* (Theorem D),
  while only 2n-m-m' < 2n switch zeros survive and band matching persists
  strictly on block interiors (Theorem C): contradiction.  Parity of the
  collapsed leading/trailing count is irrelevant.
- EVIDENCE (re-run, corrected convention): full branch n=2 R=4 SUP q0 =
  2.376980, INF q0 = 1.142677 (both > 1, q0 = -q1); all reduced roots
  found have q0 > 1 and q1 < -1 with band = False; ladder scan n=2
  (R in [1.05, 100]) has 0 violations of (r > 1, a < 0), quadratic
  expansion f/(a x^2) = 1 at both probe points (see
  scripts/_out_slope_a{2,3,4}.txt).
- Status: (G2) CLOSED STRICT (endpoint + interior + cascades).  (G1')
  remains OPEN; O-5 (det B != 0) remains OPEN.  The global classification
  conjecture now depends only on (G1').

## R-205 (2026-08-13): parity claim refuted; global eps-alternation; Green inertia
- REFUTED (EVIDENCE): the handoff's "palindromic pattern => global eigenfunction
  parity u_k(1-x)=(-1)^{k-1}u_k(x), independent of symmetry" is FALSE.  Parity
  requires rho(1-x)=rho(x), i.e. symmetric WIDTHS, not just palindromic
  heights.  Random asymmetric widths give parity and f-evenness errors O(1)
  (worst 1.072 / 1.290), vs 1e-16 on the symmetric branch.  The proposed
  direct symmetry chain is invalid; the mirror-sector / bracket / Green closed
  forms are scoped to symmetric points (docstring corrected).
- STRICT global eps-alternation lemma (no symmetry): eps_j := sign(u_{n+1}/u_n)
  at the ordered simple zeros of f equals (-1)^{j+1}.  Proof via W < 0 => Q
  strictly decreasing on each cell, Q: +inf -> 0 -> -inf, so the left zero has
  Q=+c, the right Q=-c.  This is the correct global input for (C1)/(C2).
  Numerically confirmed on random asymmetric widths (#zeros = 2n, pattern
  [1,-1,...] in all draws).
- STRICT (classical Gantmacher-Krein): on the symmetric branch the half spectra
  interleave as lambda_n = mu_{n/2}^D, lambda_{n+1} = mu_{n/2+1}^N (n even),
  lambda_n = mu_{(n+1)/2}^N, lambda_{n+1} = mu_{(n+1)/2}^D (n odd); the
  odd-sector reduced resolvents R_n^bot and R_{n+1}^bot on the n left-half
  switches have negative index n/2 each (n even), or (n-1)/2 and (n+1)/2
  (n odd).
- (G1') reduction (STRICT, machine 1e-13..1e-16): K_o = diag(d) + (4 lam_n/lam_{n+1})
  diag(u) M diag(u) with M = lam_{n+1} diag(eps) R_{n+1}^bot diag(eps)
  - lam_n R_n^bot; M has mixed inertia (n=2: 1+/1-, n=3: 1+/2-), while K_o is
  PD (SUP) / ND (INF) via the non-uniform diagonal d; this comparison is the
  remaining obstacle for (G1').
- NEGATIVE (EVIDENCE): D_n as a function of the bang-bang widths has
  mixed-sign Hessian at random points; no global concavity/convexity shortcut.
- Deliverables: run_notes_addendum_2026-08-13b.md;
  scripts/_gapn2_parity_global_probe.py, _gapn2_green_inertia_probe.py;
  _gapn2_bracket_identity_audit.py (docstring scoping fix).
- Status: (G1') OPEN; (G2) CLOSED (R-204); symmetry of all band-consistent
  solutions NOT established independent of the degree argument.

## R-206 (2026-08-13): second-variation audit, corrected Kp identity, handoff route closed
- STRICT: weighted-eigenvalue second variation (fixed-space generalized
  eigenproblem A = -d^2/dx^2, B = mult rho on H_0^1, constraint
  <u_e, B_e u_e> = 1): lam' = -lam <dr, u^2>, lam'' = 2 lam <dr, u^2>^2
  - 2 lam^2 sum_{l != k} <dr u, u_l>^2/(lam_l - lam), UNWEIGHTED L^2(dx)
  pairings, denominators lam_l - lam for both sums.  FD-verified (constant
  string antisymmetric step 1.7e-5; n=2 SUP R=4 per-eigenvalue 4e-3/5e-2 at
  N=60 truncation, Q rel 1e-3).  The operator frame A(rho) = -(1/rho)d^2/dx^2
  in the moving space L^2(rho dx) is the WRONG frame (spurious
  4 lam <dr^2/rho, u^2> term).
- STRICT: corrected global resolvent identity for K at ANY band-consistent
  point: Kp := diag(eps) K diag(eps) = diag(d) + (2 lam_n D/lam_{n+1}^2) v v^T
  - (2 lam_n^2/lam_{n+1}) [u_n u_n^T o Gt_n] + 2 lam_n [(eps o u_n)(eps o u_n)^T
  o Gt_{n+1}], d_j = sigma 2 c |W(x_j)|/(R-1), v_j = u_n(x_j)^2.  Identity
  machine-verified 1e-15 with the same Gt objects; reconstructed Kp vs FD
  rel 2.6e-4 (n=2 SUP R=4, N=2000) / 4e-5 (n=3 INF R=4).  The eps-masks are
  intrinsic (two resolvent kernels enter under different entrywise masks):
  no sign-definite rank-2 split without further parity input; earlier false
  "positive kernel" draft RETRACTED.
- NEGATIVE (P3, route closed): the naive second variation applied to
  bump-regularized bang-bang dr does NOT reproduce the width-Hessian (sign
  mismatch at all tested points).  STRICT mechanism: the width path
  rho(x; w + e dw) has d^2 rho = sum_i s_i dw_i^2 delta'(x - x_i), a
  boundary-layer term of leading order the naive form omits; the naive form
  additionally diverges as bump width -> 0.  The handoff's proposed
  second-order coefficient identity is REFUTED.
- EVIDENCE (new conjecture input): SUP tangent-space negative definiteness of
  the naive Q on {<dr, f> = 0} (n=2,3 R=4; n=2 R=10; piecewise-constant and
  trigonometric directions); INF n=2 R=4 INDEFINITE, consistent with det K
  -> 0+ (no uniform margin, R-202).  Tangent quadratic form eigenvalues
  (n=2 SUP R=4, block basis): [-38.36, -3.58, -0.301, -0.223].
- Literature: Cox-McLaughlin I/II (Zbl 0709.73044/45) cover lam_1 only, not
  applicable; Osmolovskii-Maurer (Zbl 1293.49043, Zbl 1534.49015) is the
  general bang-bang second-order theory and reduces to the same quadratic-form
  sign condition, no shortcut; fulltexts not obtained.
- Deliverables: run_notes_addendum_2026-08-13c.md;
  scripts/_gapn2_second_variation_probe.py (P1/P2/P3),
  _gapn2_k_global_rank2.py (corrected identity);
  tools/second-variation-weighted-eigenvalues.md (new tool).
- Status: (G1') OPEN, now in the precise global form Kp = diag(d) + rank-1
  vv^T + two eps-masked regularized-resolvent terms; (G2) unchanged CLOSED
  (R-204).  The global classification conjecture depends only on (G1').

## R-207 (2026-08-13, session 2): corrected half-Green machinery + both 2x2
## sector closed forms; precise open core for (G1')
- RETRACTED (handoff draft): green_regularized with extra rho(y) factors in
  B and P.  STRICT replacement: Gt_k = B - u(x)P(y), B = (u(x)v(y)-v(x)u(y))
  1_{x>y} - u(x)u(y)I1(x) + v(x)u(y)I2(x), P = <rho u, B>, NO rho(y)
  factor; L_x B = delta - rho u u^T by direct differentiation; A1/A2 via
  exact per-block trig primitives (_prims_9/_fold3/_a1a2_exact).  The
  handoff diagnosis (A1/A2 quadrature accuracy) was also WRONG: exact vs
  200k-point trapz differ by 2e-8; the constant-density self-test missed the
  rho(y) bug because rho=1 there.  C2 green: Gt_D/Gt_N/G_D/G_N vs
  Richardson spectral 1.3e-6..7.7e-6 (tail O(1/N^2)); symmetry 1.4e-17;
  T_D closed vs spectral 1.8e-11.
- RETRACTED (handoff convention claim): sector_data Ko is the odd sector
  Bo^T K Bo of the RAW K, NOT the odd sector of Kp, and diag(1,-1) Ke
  diag(1,-1) = Ko is FALSE.  STRICT correct identity: eps_{2n-1-j} = -eps_j
  gives diag(eps) Bo = Be diag(beta), beta_j = -(-1)^j, hence Bo^T Kp Bo =
  diag(beta) Be^T K Be diag(beta); verified vs FD 2.3e-9 / 8.6e-10.
- STRICT (n even): both mirror sectors of the raw K at symmetric band-
  consistent points have exact half-problem closed forms:
    Kp_odd = diag(d[:n]) + 2 lam_n diag(u)[G_D o ee^T - c^2 G_N] diag(u)
      (= diag(beta) Ke diag(beta), the even sector of K up to conjugation),
    Ko = diag(d[:n]) + 2 r (eps v)(eps v)^T
      + 2 lam_n diag(u)[Gt_N - c^2 Gt_D o ee^T] diag(u),
  with all four kernels exact (Section 1).  n=2 R=4 EVIDENCE vs FD:
  Ko err 4.6e-10 (INF) / 3.7e-10 (SUP); both R-205 and collapsed assemblies
  agree 1.8e-15; INF eig Kp_odd=[-9.12,-0.63] Ko=[-2.91,-1.07], SUP
  Kp_odd=[2.32,9.05] Ko=[3.18,7.15].
- STRICT spectral splits (n=2): G_D(mu_2^N)|2 = -alpha v1v1^T + Ph,
  G_N(mu_1^D)|2 = -beta w1w1^T + Qh, Gt_N = -alphaN w1w1^T + Rh, with
  Ph, Qh, Gt_D, T_D, Rh positive definite on the 2-point grid (weights
  positive by Gantmacher-Krein interleaving; rank-2 evaluation argument).
  Exact B1/B2 decompositions recorded; the R-205 mixed-inertia statement on
  M reproduced exactly (det M < 0 at R=4 INF), so the non-uniform diagonal d
  is the only sign source for Kp_odd.
- EVIDENCE R-scan (n=2): Kp_odd and Ko negative definite (INF) / positive
  definite (SUP) for R in [1.05,100] (INF) / [1.05,10] (SUP, continuation
  limit); det J > 0 throughout, consistent with sgn det J = (-1)^n; INF
  margins decay polynomially as R -> inf (det K -> 0+, R-202).
- REDUCED OPEN CORE: (G1') at n=2 symmetric points is now equivalent to
  the explicit 2x2 inequalities (I1)(I2) (addendum Section 6) with exact
  closed-form entries; Cauchy/Binet expansion writes both determinants as
  signed double sums.  Proposed route (OPEN): (i) finite rescaled limit
  L = lim_{R->1+} (R-1)K at the constant string; (ii) monotonicity of
  det Kp_odd / det Ko in R along the symmetric branch (FH + band-system
  derivatives); (iii) R -> inf bonding-antibonding asymptotics.
- Deliverables: run_notes_addendum_2026-08-13d.md; scripts rewritten/new:
  _gapn2_half_problem_probe.py (corrected), _gapn2_half_debug2/3/4.py,
  _gapn2_odd2x2_decompose.py, _gapn2_rawko_closed.py, _gapn2_odd2x2_scan.py.
- Status: (G1') OPEN, reduced at n=2 to explicit 2x2 definiteness (I1)(I2);
  (G2) unchanged CLOSED (R-204); the parity/convention structure is now
  fully STRICT (Sections 1-4 of the addendum).

## R-208 (2026-08-13, session 3): R->1+ anchor + half-gap Hessian + monotonicity evidence
- STRICT Lemma A: at the constant string, W0(x) = (u_{n+1}^0)'u_n^0 -
  u_{n+1}^0(u_n^0)' does not vanish at any zero of f0 (n>=1).  Proof:
  f0=0 gives 1-p = c0^2(1-q), p=cos^2((n+1)t), q=cos^2(nt); W0=0 plus
  f0=0 forces q = -(n+1)^2/n^2 < 0, contradiction (sin(nt)=0 case
  excluded by gcd(n,n+1)=1).  Hence f0 has exactly 2n simple zeros,
  f0'(x_j) = -2 lam3^0 eps_j c0 W0(x_j) != 0, sgn det D_xF(1,x*) = (-1)^n.
- STRICT Theorem B (anchor): near R=1 the solution set Sigma_sigma(R) is a
  single smooth symmetric branch (each coordinate is one of the 2n simple
  zeros of the same scalar f(.;R); IFT on the symmetric submanifold).
  (R-1)K(R) -> (sigma/lam3^0) diag(|f0'(x_j)|), strictly sign-definite, so
  (G1') holds on (1,1+delta) for EVERY n (even and odd); n=2: (I1)/(I2)
  hold on (1,1+delta) via (R-1)Kp_odd, (R-1)Ko -> diag(sigma 2c0|W0(x_j)|).
  EVIDENCE: n=2 R=1.00001 continuation errors 1.2e-4 linear in (R-1),
  D->5pi^2, switches -> f0 zeros; n=3 diagonal-limit check 3.8e-4/3.1e-3.
- STRICT half-gap Hessian identity (signs corrected): dg/dx_j = -2 s_j f(x_j)
  (g = mu_2^N - mu_1^D), grad^2 g = -2(R-1)^2 K = +(2/lam3) Hess(D_n); so
  (I1)+(I2) <=> strict local min (INF) / max (SUP) of g at the symmetric
  critical point.
- FALSIFIED route (EVIDENCE): global convexity of g on the switch triangle
  (R=4 grid scan: Hessian indefinite off the critical point, 11/15 INF and
  12/15 SUP violations; eigenvalues up to +/-4800).
- EVIDENCE: det Kp_odd and det Ko strictly decreasing in R on [1.05,100]
  for BOTH modes; traces sign-correct (tr<0 INF, tr>0 SUP) but not
  monotone; chain rule d/dR M = dM/dR|x + sum (dM/dx_j)(dx_j/dR) with
  dx/dR = -J^{-1} dF/dR verified to 4-5 digits at R=1.5,2,4,10 (probe bug
  documented: Recon caches pat at init; mutating rc.R does nothing).
- REDUCED OPEN CORE: (G1') open on [1+delta,infinity); n=2 (I1)/(I2) open on
  [1+delta,infinity) with obligations (M1) d/dR det Kp_odd, det Ko < 0,
  (M2) trace signs, (M3) R->inf bonding-antibonding asymptotics.
- Deliverables: run_notes_addendum_2026-08-13e.md; scripts
  _gapn2_r1_anchor_probe.py, _gapn2_r1_monotonicity_probe.py,
  _gapn2_gap_convexity_probe.py, _gapn2_r1_det_derivative_probe.py.
