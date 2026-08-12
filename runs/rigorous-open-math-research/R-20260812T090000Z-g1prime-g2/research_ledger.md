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
