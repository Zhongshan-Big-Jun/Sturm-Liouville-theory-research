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
