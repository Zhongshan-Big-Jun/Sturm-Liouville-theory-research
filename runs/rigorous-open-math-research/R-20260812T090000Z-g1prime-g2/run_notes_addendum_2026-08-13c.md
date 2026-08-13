# Run addendum: second-variation audit, corrected Kp identity, closed handoff route (2026-08-13, R-206)

Continuation of R-20260812T090000Z-g1prime-g2.  All numerics EVIDENCE unless
flagged STRICT.  This addendum audits the handoff-proposed second-order
coefficient route, records the corrected global resolvent identity for K,
and closes the proposed route with a precise obstruction.

## STRICT: second variation of a weighted Dirichlet eigenvalue

Setting: -u'' = lambda rho u on (0,1), u(0)=u(1)=0, rho bounded positive,
u_k normalized by int rho u_k^2 = 1.  Perturb rho_e = rho + e dr with dr
bounded (any L^inf perturbation, not necessarily piecewise constant).
Write u_k(e) = u_k + e v_k + (e^2/2) w_k, lambda_k(e) = lambda_k + e lam'
+ (e^2/2) lam''.  Then

    lam'  = -lambda <dr, u^2>,
    lam'' = 2 lambda <dr, u^2>^2
            - 2 lambda^2 sum_{l != k} <dr u, u_l>^2 / (lambda_l - lambda),

where all pairings are the UNWEIGHTED L^2(dx) pairing <dr, phi> = int dr phi.

Derivation (complete; fixed-space generalized eigenproblem A = -d^2/dx^2,
B = mult rho on H_0^1, constraint <u_e, B_e u_e> = 1):
  1. From the Rayleigh quotient lambda(e) = a[u_e]/<B_e u_e, u_e> with the
     exact constraint (=1, hence first AND second constraint derivatives
     vanish): lam'' = 2 int (v')^2 + 2 int u' w'  (expand a'' and use
     b'' = 0; Dirichlet BCs kill boundary terms).
  2. The first-order equation -v'' = lam' rho u + lam dr u + lam rho v
     (lambda' kept; it is the only subtle sign source) gives, pairing
     with u and using the first constraint derivative
     <rho u, v> = -(1/2)<dr, u^2>:  int u' v' = lam' + (lam/2)<dr,u^2>,
     and pairing with v:  int (v')^2 = lam'<rho u, v> + lam<dr u, v>
     + lam<rho v, v>.
  3. The second-order equation -w'' = lam'' rho u + 2 lam' dr u
     + 2 lam' rho v + 2 lam dr v + lam rho w, paired with u, together
     with the second constraint derivative <rho u, w> = -2<dr u, v>
     - <rho v, v>, eliminates w:
       int u' w' = lam'' + lam'<dr, u^2> - lam<rho v, v>.
  4. Hence -lam'' = 2[int(v')^2 - lam<rho v,v>] + 2 lam'<dr,u^2>, i.e.
       lam'' = -2<v, (A - lam B)v> - 2 lam'<dr, u^2>.
     Insert lam' = -lam<dr,u^2> and v = lam R_lam^perp[(dr - rho<dr,u^2>)u]
     (R_lam^perp = reduced resolvent of A - lam B in L^2(dx)): the
     rho<dr,u^2>u term contributes nothing to l != k because
     <rho u, u_l> = delta_{kl}, and the u_k-component of v is fixed by the
     constraint but does not enter (A - lam B)v.  This gives the stated
     lam'' formula.  QED.

Note: the operator form A(rho) = -(1/rho) d^2/dx^2 acting in the moving
space L^2(rho dx) is the WRONG frame (the inner product changes with e);
a derivation there produced a spurious 4 lam<dr^2/rho, u^2> term.  The
fixed-space Rayleigh derivation above is the correct one.

Verification (EVIDENCE):
- Constant string rho=1, dr = antisymmetric step 1_{[0,1/2]} - 1_{[1/2,1]}
  (lam' = 0 exactly): FD lambda_1'' = -4.93479937; formula (N=40 spectral
  truncation) = -4.93471230; rel 1.7e-5.
- Band-consistent config n=2 R=4 SUP, random piecewise-constant dr on the
  5-block grid: per-eigenvalue FD vs formula rel 4e-3 / 5e-2 at N=60
  truncation; Q = (1/2)(lam_{n+1}'' - lam_n'') rel 1e-3 (scripts/
  _gapn2_second_variation_probe.py, P1).

## STRICT: corrected global resolvent identity for K

At ANY band-consistent point (no symmetry), with eps_j = (-1)^{j+1}
(STRICT, R-205), s_j = rho_{j+1} - rho_j = eps_j sigma (R-1)
(sigma = +1 SUP / -1 INF), c = sqrt(lam_n/lam_{n+1}), W = u_{n+1}'u_n
- u_{n+1}u_n' < 0, d_j = sigma 2 c |W(x_j)|/(R-1), K := diag(1/s) J,
Kp := diag(eps) K diag(eps), v_j = u_n(x_j)^2:

    Kp = diag(d) + (2 lam_n D/lam_{n+1}^2) v v^T
         - (2 lam_n^2/lam_{n+1}) [u_n u_n^T o Gt_n]
         + 2 lam_n [(eps o u_n)(eps o u_n)^T o Gt_{n+1}],

D = lam_{n+1} - lam_n, Gt_k = regularized resolvent kernel of the full
problem at lam_k (pole removed), evaluated on the 2n switch points,
o = entrywise product.  This is pure algebra from the verified first-order
perturbation formulas (A1)(A2) plus the band identities w_j = lam_n
u_n(x_j)^2 = lam_{n+1} u_{n+1}(x_j)^2.  Machine check: reconstructed Kp
equals the FD Kp to rel 2.6e-4 (n=2 SUP R=4, N=2000 truncation; the
identity itself with the same Gt_n/Gt_{n+1} objects holds to 1e-15) and
rel 4e-5 (n=3 INF R=4).  Script: scripts/_gapn2_k_global_rank2.py.

Spectral expansion (substitute the spectral sums for Gt_n, Gt_{n+1}):

    Kp = diag(d) + (2 lam_n D/lam_{n+1}^2) vv^T
         - (2 lam_n^2/lam_{n+1}) sum_{l != n}   (u_n o u_l)(u_n o u_l)^T
           /(lam_l - lam_n)
         + 2 lam_n sum_{l != n+1} (eps o u_n o u_l)(eps o u_n o u_l)^T
           /(lam_l - lam_{n+1}).

Honest negative note: an earlier draft of this session cancelled the eps
factors before substituting u_{n+1} = eps c u_n and obtained a false
"positive kernel + rank-2" form (rel err 0.49 vs FD).  That draft is
RETRACTED.  The eps structure is intrinsic: the two resolvent kernels
enter under DIFFERENT entrywise masks (u_n u_n^T vs eps eps^T o u_n u_n^T),
so no sign-definite rank-2 split exists without further parity input.
This is the same parity obstruction recorded in R-205 for the sector
decomposition.

## NEGATIVE: the handoff second-order coefficient route is closed

Claim tested: the naive second-variation form Q(dr) = (1/2)(lam_{n+1}''
- lam_n'') reproduces the width-Hessian quadratic form when dr is the
bump-regularized bang-bang direction dr = -sum_i s_i dx_i bump(x - x_i).
Result (scripts/_gapn2_second_variation_probe.py, P3): sign mismatch at
every tested point (n=2 R=4 SUP: Q(Hess) = -1.35e3, -2.78e3, -8.59e3 vs
naive +2.28e2, +3.83e2, -5.31e2; same at R=10).  Reason (STRICT): the
width family rho(x; w + e dw) is NOT linear in rho; its second-order
density variation is d^2 rho = sum_i s_i dw_i^2 delta'(x - x_i)
(Heaviside-shift expansion), a boundary-layer term of leading order that
the naive formula omits.  The naive form additionally diverges as the
bump width -> 0 (diagonal of the un-regularized Green sum), so the
"naive = Hessian + controlled residual" identity proposed in the handoff
does not hold in any tested form.

## EVIDENCE: SUP tangent-space negative definiteness (new conjecture input)

At the symmetric critical point, Q(dr) restricted to the tangent space
{<dr, f> = 0}, f = lam_n u_n^2 - lam_{n+1} u_{n+1}^2:
- SUP n=2 R=4: all 8 random piecewise-constant tangent directions and all
  6 random smooth (trigonometric) tangent directions give Q < 0.
- SUP n=3 R=4: all 8 + 6 directions give Q < 0.
- SUP n=2 R=10: all directions give Q < 0.
- INF n=2 R=4: INDEFINITE (signs mixed), as expected from det K -> 0+
  (no uniform margin, R-202).  The naive tangent-space route is at best
  a SUP-only statement.
Eigenanalysis of the tangent quadratic form (n=2 SUP R=4, block-constant
basis): eigenvalues [-38.36, -3.58, -0.301, -0.223]; eigenvectors show
antisymmetric / symmetric / switch-localized modes with no immediate
identification against spectral gaps (lam_l - lam_n).  No trivial positive
representation found yet.

## Literature status (2026-08-13)

- Cox, S.J.; McLaughlin, J.R., Extremal eigenvalue problems for composite
  membranes I, II, Appl. Math. Optim. (1990).  Zbl 0709.73044 /
  Zbl 0709.73045, DOI 10.1007/BF01447325 / 10.1007/BF01447326.  Part I:
  topology of the two-density class, continuity of rho -> lambda_k,
  existence of extremizers (N-dimensional generalization of Krein's work).
  Part II: optimality conditions and level-set geometry of extremizers for
  lambda_1.  NOT applicable to the adjacent-gap second-order strictness:
  both papers concern lambda_1.  (Reviews via zbMATH Open API; fulltexts
  not obtained.)
- Osmolovskii, N.P.; Maurer, H., Applications to regular and bang-bang
  control: second-order necessary and sufficient optimality conditions...,
  SIAM J. Control Optim. (2008), Zbl 1293.49043; and the survey chapter
  Zbl 1534.49015 (Springer, DOI 10.1007/978-3-319-30785-5_6).  This is the
  general framework for second-order conditions with switching-time
  variations (trajectory derivatives w.r.t. switching times, Hessian of the
  induced Lagrangian in terms of first-order variations).  Our J/K
  structure is exactly an instance of this theory; the general theorem
  reduces to the same quadratic-form sign condition, i.e. it does not
  supply the specific inequality (G1').  Fulltexts not obtained.

## Status and reduced open core

- (G1') remains OPEN.  New precise form: Kp = diag(d) + rank-1 v v^T
  + two entrywise-masked regularized-resolvent terms (identity above),
  valid globally; the eps-masks are the intrinsic parity structure.
- The handoff's second-order coefficient identity is REFUTED (P3) with an
  exact mechanism (delta' boundary-layer term of the width path).
- New conjecture-level input (EVIDENCE): SUP tangent-space negative
  definiteness of the naive second variation; no proof yet, and the
  delta-measure regularization link to the Hessian remains open.
- INF has no uniform margin (R-202); any INF argument must use the
  boundary-layer terms or the qualitative det K -> 0+ behavior.

## Scripts

- scripts/_gapn2_second_variation_probe.py (P1/P2/P3; corrected formula;
  docstring updated with the session results).
- scripts/_gapn2_k_global_rank2.py (corrected Kp identity; the earlier
  false positive-kernel draft is RETRACTED in the docstring).
