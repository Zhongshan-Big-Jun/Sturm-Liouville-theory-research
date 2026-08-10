# Approach registry - O1 revision (R-20260806T140000Z-o1revise-2ED02A)

Route families by mechanism.  Statuses: UNEXPLORED | ACTIVE | PROMISING |
PARTIAL | BLOCKED | REFUTED | MERGED | PROVED.

## R1 - Operator repair (O1a): symmetric Hilbert-Schmidt operator

Core mechanism: replace the non-self-adjoint T_rho = T_0 M_rho by the
symmetric HS operator S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} (kernel
sqrt(rho(x)) G(x,t) sqrt(rho(t))); S_rho is similar to T_rho, mu_k(S_rho)
= 1/lambda_k(rho); ||S_rho - S_sigma||_HS <= (R/4)||rho-sigma||_1^{1/2};
Weyl inequality gives continuity.
Target obligation: O1a.
Why easier: reduces to standard operator perturbation theory; no analysis
beyond HS norms and the Rayleigh comparison bounds.
Required known results: P3, P4, P5.
First concrete deliverable: explicit HS bound derivation + numeric check.
Fast falsification tests: random rho,sigma in K; compare predicted vs
actual eigenvalue differences; check the kernel is symmetric.
Expected bottleneck: none (clean).
Status: PROVED (after the operator-formula correction).
Exact gap: closed.

## R2 - Sign repair (O1b): moving-jump derivative

Core mechanism: distributional FH with the correct parametrization
(rho_eps = rho - (c_+ - c_-) chi_{(x_j,x_j+eps)} for rightward eps > 0);
sign of dD/deps = -(c_+ - c_-) f(x_j) (signed displacement).
Target obligation: O1b.
Why easier: one-line sign bookkeeping once the parametrization is fixed.
Required known results: P1, P6.
First concrete deliverable: corrected lemma + numeric verification of both
one-sided derivatives and the signed derivative.
Fast falsification tests: numeric finite differences on [1,R,1] configs;
check against the verified identity dD/du = -2(R-1)f(u).
Expected bottleneck: none.
Status: PROVED (after R4 supplies the rigorous justification).
Exact gap: closed.

## R3 - Presentation repair: u_2 sign convention (O1c)

Core mechanism: adopt AEH's convention (u_1 > 0 on (0,1); u_2 > 0 on
(0,z_0), < 0 on (z_0,1)); restate the Wronskian proof of O1c with a global
W < 0 argument.
Target obligation: O1c.
Status: PROVED (presentation only).

## R4 - Approximation justification (O1b): moving-jump FH via smoothing

Core mechanism: rho_eps^delta = c_- + (c_+-c_-) H_delta(x - x_j - eps) with
H_delta a smoothed Heaviside; apply AEH Lemma 2.1 to the delta-family;
pass delta -> 0 using uniform convergence of eigenfunctions (H^2 bounds +
Arzela-Ascoli) and dominated convergence; then eps -> 0.
Target obligation: O1b hypothesis; makes R2 rigorous.
Why easier: reduces the distributional case to the L1 case covered by the
primary source.
Required known results: P1, P5, H^2 a priori bounds for eigenfunctions.
First concrete deliverable: written argument (candidate_proof.md Lemma 3).
Fast falsification tests: numeric check that the smoothed-family derivative
converges to the delta limit as delta -> 0.
Expected bottleneck: interchange of limits (handled by bounded integrand +
dominated convergence).
Status: PROVED.
Exact gap: closed.

## V1 - Numeric verification of the full reduction (evidence)

Core mechanism: transfer-matrix solver for piecewise constant rho; compute
max over barrier family and min over well family (2-parameter scan), compare
against random configs with many blocks and values in [1,R].
Target obligation: THEOREM_SUP_RED / THEOREM_INF_RED (evidence only).
First concrete deliverable: verify_reduction_search.py + out json.
Fast falsification tests: adversarial configs (alternating 1/R, random
values, random jump counts 2-8).
Expected bottleneck: none (finite search is evidence only).
Status: ACTIVE -> PARTIAL (completed, no counterexample).

## V2 - Boundary and degenerate cases (evidence)

Core mechanism: evaluate D at rho = 1, rho = R, 2-block configs, a = b,
coalesced jumps; check O1c structure on hostile configs (f zero count,
W < 0, v strictly decreasing).
Target obligation: edge cases in the contract.
Status: ACTIVE -> PARTIAL (completed).

## V3 - Premise verification (evidence)

Core mechanism: numeric checks of P4 (comparison bounds), P5 (HS bound),
P7 (Sturm zero counts), and continuity of eigenfunctions.
Target obligation: premise recheck obligations of the packet.
Status: ACTIVE -> PARTIAL (completed).

## D1 - Disproof route (adversarial)

Core mechanism: deliberately attempt to falsify each O1x claim: (a) a density
with D above the barrier-family max or below the well-family min; (b) an
O1c violation (f with 3+ zeros or {f>0} disconnected); (c) a jump-moving
derivative with the wrong sign; (d) discontinuity of lambda_k in L^1.
Status: PARTIAL (no counterexample found; the only falsified statement is
the DRAFT's O1b sign, already repaired).

## Route allocation notes

- Single-agent run: routes executed sequentially as reviser, then verifier
  pass (adversarial, fresh context per role).
- The revised candidate_proof.md merges R1-R4 + unchanged O1c-O1f into the
  final proof (synthesis only after each route produced a closed obligation).
