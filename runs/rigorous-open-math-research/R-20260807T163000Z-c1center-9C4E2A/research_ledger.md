# Research ledger - R-20260807T163000Z-c1center-9C4E2A

## R-001 (setup): run root created; contract/obligation/approach written.
## R-002 (center contraction probe): dXC/da+dXC/db max over grids 0.0458
  (R=1.05) .. 0.9998 (R=1e4 near diagonal), 4.31 (R=100, near-degenerate x_+);
  on the diagonal dXC/dC = 1 EXACTLY.  Strict-contraction form refuted.
## R-003 (sign conjecture probe): M = XC - C; one violation at (0.7793, 0.8032,
  R=100), M = +0.00925 with a+b > 1.
## R-004 (violation check, mpmath 60 digits): violation is REAL (x_- = 0.72671,
  x_+ = 0.87430, q = 0.056, v(1-) = -0.05828).  Center mechanism REFUTED.
## R-005 (reduction upgrade): N1 - C1 follows from (E1)+(U)+(P0) with
  Phi = g_1' * g_1'(u).
## R-006 (U verification): verified the M-shape of Phi - 1 numerically over
  (R, a) grids; Phi(a0) dips below 1 for large R -> U is FALSE as stated;
  replaced by U' (M-shape of Phi - 1).  Registered as correction R-012.
## R-007 (clean S3 tracing): tracew_*.json rows are polluted by sheet jumps for
  a > ~1/2 (e.g. W ~ 1.03 at a=0.51 instead of 0.33) and near the diagonal;
  built targeted continuation (s33_profile.py) giving clean branch data.
## R-008 (ground state law): verified s1 sqrt(q) = 1/sqrt(W a (1-a)) to 0.1%
  on the clean S3 branch at q = 1000 (a = 0.43..0.58).
## R-009 (one-sided pinning): verified s2 a ~ pi for a > 1/2 and
  s2 (1-b) ~ pi for a < 1/2 on the clean branch; delta = (pin - s2 x) q
  satisfies delta = -cot(theta) + O(1/q), theta = s2 W, on both sides.
## R-010 (right-side norm): n2 ~ a^3/(2 pi^2) for a > 1/2 (mode pinned in the
  left well; barrier and right-well pieces O(1/q)); the earlier draft norm
  (with a right-well term) is WRONG - corrected (F-014).
## R-011 (branch equations): derived and verified (P-): sin(pi W/(1-a)) =
  sqrt(2a) pi W/(1-a) (a < 1/2) and (P+): kappa^2 = 1/(2 pi^2 (1-a) W^2)
  (a > 1/2), both to ~0.1% at q = 1000 in the generic regime; (P-) degrades
  inside the transition layer (a ~ 0.49, 60% error).
## R-012 (E1-inf PROVED): u in (0, pi/2) root of sin(u) = sqrt(2 a0) u and
  x in (pi/2, pi) root of x^2 cot^2 x = 1/(2 a0); then -x cot x = u/sin u and
  the strictly increasing map Y1(t) = -t cot t give u < x, hence
  W_R(1-a0) - W_L(a0) = (1-a0)(x-u)/pi = 0.2474707 > 0.  Strict (conditional
  on the profile limits).
## R-013 (fp limit system DERIVED): on the diagonal, two-sided pin gives
  delta = 2 pi xi + kappa/2, theta = 4 pi xi; (SEC) gives
  sin(theta)(1 - delta^2) = 2 delta cos(theta); (BR) gives delta^2 =
  1/(8 pi^2 xi^2).  Combined: xi tan(2 pi xi) = 1/(2 sqrt2 pi), unique xi* =
  0.1199372; alpha*^2 = 2/xi*, kappa* = 2(tan 2 pi xi* - 2 pi xi*).
## R-014 (Phi-1 zero motion): measured (0.5 - z0) q = 4.30, 5.32, 10.47, 20.03
  at q = 70.7, 100, 316, 1000; the earlier "fixed a ~ 0.480/0.520" and
  "O(1/sqrt(q)) window" claims are wrong (F-015).  U'-layer single crossing
  is the open core of G-U'.

## R-015 (R -> 1+ structure, CORRECTED): the old A9/C8 "limit curve
  sin(2 pi b) = -sin(pi a)/2, slope 1/14" is REFUTED (F-016).  Direct
  continuation: S3 is nearly vertical for small R (db/da in (48,531) at R=1.05),
  G(a0) -> +inf, not 1/14; no S3 point lies on that curve.  Correct structure:
  S3 is the sheet a = a0 + eps phi(b) + O(eps^2), eps = R-1, with phi(b) =
  -R1_1(a0; a0, b)/f_const'(a0) from first-order perturbation theory
  (closed formulas in candidate_proof A9; verified vs finite differences to 6
  digits).  phi(a0) = 0 exactly (degenerate point (a0,a0) on S3); phi' > 0 on
  [a0, 0.98] (min 0.006, EVIDENCE); g_1(a0) = a0 exactly for R in [1.001,
  1.05]; h(a0) = 2a0-1 + phi(b0)eps + O(eps^2) = -0.160861 + 0.026021 eps
  (matches e15 to O(eps^2)); h(beta) -> b_top* - b0 > 0 (b_top ~ 0.936, margin
  0.35); Phi-1 > 0 and G > 0 on the whole domain for R <= 1000.  R -> 1+ proof
  is reduced to closed-form monotonicity of phi + b_top* > b0 + O(eps) bounds
  (Gap 1).  Also found: e15 first-row b at a0 is an off-branch artifact for
  R <= 100 (F-017); Green's function sign bug in the first cumsum integrator
  (F-018).  Script: s33_r1plus.py -> s33_r1plus.json.

## R-016 (2026-08-09, R -> 1+ strict push): closed form of phi, phi' > 0,
  b_top* > b0, and the w_k^1 division bug
  - Closed form of phi(b) = -R1_1(a0; a0, b)/f_const'(a0) derived by hand
    antiderivatives (all integrands elementary trig products), f_const'(a0) =
    15 pi^3 sqrt(15)/4.  Script: sym_phi_closedform3.py.
  - BUG found and fixed (F-019): the normalized-mode correction w_k^1 =
    y_k^1/sqrt(n_k^0) - u_k^0 n_k^1/(2 n_k^0) had been implemented with
    multiplication by sqrt(n_k^0) instead of division (sym_phi_closedform2.py);
    caught by term-by-term comparison (dbg_pieces3.py), corrected in
    sym_phi_closedform3.py.
  - phi'(b) = -N/(60 pi) with N = m u^2 + (2 pi a0 + 3 sqrt15) u + (3 sqrt15 -
    58 pi a0) + 2 sqrt15 pi (1-b)(1-4u) v, u = cos(2 pi b), v = sin(2 pi b),
    m = 56 pi a0 - 6 sqrt15 > 0.  Factored form: phi'(b) 60 pi = (1-u)(m(1+u)
    + n) + 2 sqrt15 pi (1-b)(4u-1) v with n = 2 pi a0 + 3 sqrt15 > 0.
  - phi' > 0 on [a0, 1): CERTIFIED (mpmath.iv 200-bit interval arithmetic,
    uniform 4000-cell grid on [a0, 0.999], worst enclosure lower bound
    8.896e-6, cert_phi_prime.py -> cert_phi_prime.json) + STRICT (elementary
    tail bound on (0.999, 1): for b = 1-e, e in (0, 1/1000],
    phi'(b) 60 pi >= C_tail e^2 with C_tail >= 9.651926).
  - b_top* > b0: STRICT structural lemma (implicit function theorem for
    R1(a, b-bar, eps) at (a0, 0) uniform on [a0, 7/10]; fp arc b in [a0, 7/10]
    lies in the fp-component S3, hence b_top(eps) >= 7/10 and
    b_top* >= 7/10 > b0 ~ 0.5804, margin 0.12).
  - Consequences (all reduced to Gap 1): h(a0) = -0.160861 + 0.026022 eps +
    O(eps^2) < 0 (margin 0.16); h(beta) -> b_top* - b0 >= 0.12 > 0; P0:
    G = 1/(eps phi' + O(eps^2)) > 0; U': Phi - 1 = 1/(eps^2 phi' phi'_u)
    (1 + O(eps)) - 1 > 0 for small eps (b, b_u in [a0, 1) where phi' > 0).
  - Verification re-run 2026-08-09: verify_phi_closedform2.py (vs reference
    R1_1, max diff 1.38e-6), verify_sheet_exact.py (a*(b,eps) - a0 - eps phi
    < 1e-9 at eps = 1e-4; phi' closed form vs FD to 5 digits),
    cert_phi_prime.py (all PASS).  Scripts:
    sym_phi_closedform3.py, verify_phi_closedform2.py, verify_sheet_exact.py,
    cert_phi_prime.py, analyze_dphi.py, scan_dphi_full.py, tail_bound_phi.py
    (+ JSONs verify_sheet_exact.json, cert_phi_prime.json).

## Open items (priority order)
1. Gap 1 (G-EST): explicit uniform error bounds for A4/A5 (implicit function
   theorem + Lipschitz bounds on the explicit trig formulas), converting
   E1-inf's corollary, U'-generic, and the fp limit into theorems for q >= q0.
2. U'-layer: single crossing of Phi - 1 on [a0, fp] from the layer profile
   W(xi) and the map xi -> xi_u.
3. R -> 1+ perturbation (A9): DONE this session - closed form of phi(b)
   (DERIVATION, verified), phi' > 0 on [a0, 1) (CERTIFIED + STRICT), and
   b_top* >= 7/10 > b0 (STRICT).  REMAINING (Gap 1): explicit uniform O(eps)
   error bounds for A_eps - a0 - eps phi, b_top(eps), h, G, Phi, plus an
   explicit upper bound b_top(eps) <= 1 - delta_0.  Then E1/U'/P0 hold for
   R in (1, 1+eps0).
4. Certified bulk (finite R): sign-based certification at useful cell sizes.
