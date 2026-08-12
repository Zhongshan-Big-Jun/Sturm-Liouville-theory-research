# Run notes addendum: closed-form M~ diagonal, sign audit, dead ends (2026-08-12 evening)

Continuation of R-20260812T090000Z-g1prime-g2 (O-1..O-5).  All numerics EVIDENCE
unless flagged STRICT.

## New STRICT identities (verified to 1e-13..1e-15)

Let G~_k(x,y) = sum_{l != k} u_l(x) u_l(y)/(lambda_l - lambda_k) (regularized
resolvent kernel), w_j = lambda_n u_n(x_j)^2 = lambda_{n+1} u_{n+1}(x_j)^2
(band-consistent point), D = lambda_{n+1} - lambda_n.

(I1) Partial-fraction identity (exact, termwise):
  lambda_{n+1} G~_{n+1}(x,x) - lambda_n G~_n(x,x)
      = Sigma'(x) - 2 w_j/D - w_j D/(lambda_n lambda_{n+1})   at x = x_j,
  Sigma'(x_j) = sum_{l != n, n+1} lambda_l u_l(x_j)^2 D
                / ((lambda_l - lambda_{n+1})(lambda_l - lambda_n)) > 0 strictly.
  Proof: lambda/(lambda_l - lambda) = lambda_l/(lambda_l - lambda) - 1; the
  l = n pole term is -lambda_n u_n^2/D = -w_j/D, the l = n+1 term is
  -lambda_{n+1} u_{n+1}^2/D = -w_j/D, and u_{n+1}^2 - u_n^2 =
  -w_j D/(lambda_n lambda_{n+1}) (all exact; truncation leaves the identity
  unchanged, only Sigma' itself is truncated).

(I2) Closed form for the diagonal of M~ (consequence of (I1)):
  M~_{jj}/s_j = 2 w_j Sigma'(x_j) - 4 w_j^2 / D.
  Hence the diagonal of K = diag(1/s) J reads
  K_{jj} = sigma * 2 c |W(x_j)|/(R-1) + 2 w_j Sigma'(x_j)/lambda_{n+1}
           - 4 w_j^2/(D lambda_{n+1}),
  sigma = +1 (SUP), -1 (INF), c = sqrt(lambda_n/lambda_{n+1}).

(I3) Sign of f'(x_j)/s_j (CORRECTION to this run's earlier notes): using
  f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j) with W < 0 (structure theorem),
  eps_j = s_j/(R-1) for SUP and eps_j = -s_j/(R-1) for INF, we get
  f'(x_j)/s_j = +2 c |W(x_j)|/(R-1) > 0 for SUP and
                -2 c |W(x_j)|/(R-1) < 0 for INF.
  The run notes' earlier "f'(x_j)/s_j < 0 by A2" holds ONLY for INF; the
  constant sign per mode is what matters, and it is verified by FD at
  n = 2, 3, R in {1.2, 2, 4, 10}: SUP r/s in [+3.7e2, +2.6e4], INF in
  [-1.9e4, -3.2e0], zero violations.

(I4) |W(x_j)| <= D (Cauchy-Schwarz): W(x) = -D int_0^x rho u_n u_{n+1} dt,
  so |W(x)| <= D (int rho u_n^2)^{1/2} (int rho u_{n+1}^2)^{1/2} = D.
  Useful for ordering the terms of (I2) near degeneracy.

## Dead ends (falsified sub-claims, EVIDENCE)

- Gershgorin diagonal dominance of K: |K_jj| > sum_{i != j} |K_ji| holds only
  for small R (n=2 SUP up to ~R=2, INF up to ~R=2; n=3 SUP only ~R<=1.2).
  At n=3 INF R=10 the row-dominance margin/min|diag| is -38.1.  The O-5
  candidate route "diagonal part of K dominates" is numerically REFUTED for
  R >= 2..4; it cannot close (G1') globally.
- H-matrix scaling (Perron-Frobenius criterion rho(B) < 1,
  B = diag(|K_jj|)^{-1} |K_off|): holds for n=2 SUP R<=10 (rho 0.15..0.89),
  n=2 INF R<=2 (0.17..0.70), n=3 SUP R<=2 (0.25..0.71); FAILS at n=2 INF R=4
  (rho=1.31), n=3 SUP R=4 (1.05), n=3 INF R=2 (1.36).  So K is NOT globally an
  H-matrix; the H-matrix route is closed for large R.
- Positive scaling vector d (I-B) d = 1 > 0: matches the rho(B) verdict.

## New EVIDENCE: Sylvester pivots of K

LU-without-pivoting pivots of K along the symmetric branch:
- SUP: all pivots > 0 for n = 2, 3, R in {1.2, 2, 4, 10} (det K > 0,
  consistent with Hess < 0).
- INF: all pivots < 0 for the same grid (det K > 0 since 2n even, consistent
  with Hess > 0).
Sign pattern of K (n=2 SUP, R=4): diag +, off-diagonal - except the central
2x2 block (rows/cols 2-3) is [[+,+],[+,+]]-pattern; K+ and K- both
[[+,-],[-,+]]-pattern.  n=3 patterns printed by scripts/_gapn2_hmatrix_probe.py.
A strict proof of the pivot sign is still open; the pattern is stable over the
whole reachable R range and is the most promising structural handle found so
far (Sylvester's inertia law turns constant pivot signs into (G1')).

## Scripts added this session

- scripts/_gapn2_diag_dominance.py: f'/s sign, K diagonal ratios, Gershgorin,
  block spectra, det K vs prod(diag) along the branch.
- scripts/_gapn2_mtilde_diag_identity.py: verification of (I1)-(I2) via
  one-shot spectral sums (N=800, rel err 1e-13..1e-15), Sylvester pivots.
  NOTE: two wrong closed forms were tried first (missing +w_j D/(lambda_n
  lambda_{n+1}) term and then wrong sign of u_{n+1}^2 - u_n^2); both rejected
  by the same script.  Final form (I1)/(I2) verified.
- scripts/_gapn2_hmatrix_probe.py: H-matrix / Perron-Frobenius probe, sign
  patterns of K, K+, K-.

## Honest register

- Nothing here closes (G1') or (G2).  The diagonal closed form (I2) is new
  and STRICT; it reduces the diagonal part of K to explicit positive/negative
  terms but the off-diagonal Green part still needs control.
- The run notes' earlier "f'(x_j)/s_j < 0" statement is corrected by (I3).
- The O-5 candidate route (diagonal dominance) and the H-matrix route are
  both numerically refuted on the full R range (dead-end registration).
- Sylvester pivot sign pattern is EVIDENCE only; no proof yet.

## Extension: Sylvester pivots at large R (EVIDENCE, 2026-08-12 evening)

- scripts/_gapn2_pivots_bigR.py (FD Jacobian, LU without pivoting):
  - INF: pivots ALL NEGATIVE on the full reachable range - n=2 R in {30, 75, 100}
    (detK 1.3e-6 .. 8.2e-11), n=3 R in {30, 60, 75} (detK down to 6.2e-17),
    n=4 R in {20, 30} (detK 4.7e-14 .. 2.9e-18).  No sign change.
  - SUP: pivots ALL POSITIVE at n=2 R in {30, 50, 75, 100} (detK 3.6e-3 .. 3.6e-6)
    and n=4 R in {30, 50, 75, 100} (detK 1.2e-3 .. 1.3e-9).
  - Spurious-root warning: direct continuation R=4 -> R>=30 fails; even the
    R-ladder in this probe fell onto a spurious root for n=3 SUP at R>=30
    (res ~1e-12, detK ~1e-40, evK mixed signs, alternating pivots) and could
    not reach n=4 INF R=40.  These points are covered by the hp_scan JSON
    FD-authoritative fields (n=3 SUP R=100: evKp = [0.0185, 0.0246, 0.219],
    evKm = [0.0219, 0.116, 0.188], all positive; n=4 INF R=40:
    evKp = [-1294, -0.0033, -0.00021, -4.0e-5], all negative).  The alternating-
    pivot rows of the first (direct-jump) probe run are RETRACTED as spurious.
- Conclusion: the constant pivot-sign pattern (SUP +, INF -) holds on the full
  reachable range with no exception; it remains EVIDENCE (no proof yet).