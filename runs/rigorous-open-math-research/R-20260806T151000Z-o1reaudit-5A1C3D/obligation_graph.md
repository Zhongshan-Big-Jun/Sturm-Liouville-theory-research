# Obligation graph - independent re-audit of O1 Lemma 1 and Lemma 3

Node format: ID / statement / depends on / evidence-status / verdict.

## O1 reduction theorem (root)
- Statement: (i) sup_K D = max over the barrier family; (ii) inf_K D = min
  over the well family; both attained.  R > 1 fixed, K = {1 <= rho <= R a.e.}.
- Depends on: O1a-O1f + synthesis.
- Evidence/status: PROVED after this audit (INDEPENDENTLY_AUDITED_PROOF).
- Verifier notes: this run re-audited the two changed points from scratch;
  O1c-O1f rest on the prior independent audit (422A69) plus this run's
  consistency read.

## O1a (Lemma 1) - L^1 continuity of lambda_k on K
- Statement: |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
  <= (R/4)||rho - sigma||_1^{1/2}; hence |lambda_k(rho) - lambda_k(sigma)|
  <= (R/4)(k^2 pi^2)^2 ||rho - sigma||_1^{1/2}.
- Depends on: similarity S_rho ~ T_rho (algebra), HS kernel bound (F-001
  corrected chain), Weyl/min-max for self-adjoint compact operators,
  Rayleigh comparison bounds, Sturm simplicity (for the identity
  mu_k(S_rho) = 1/lambda_k(rho)).
- Evidence/status: PROVED (re-derived in this run; numerically verified
  11/11 HS-bound pairs, 22/22 Weyl cases).
- Verdict: PASS.
- Prior verdict (on the draft): PARTIAL (draft applied Weyl to the
  non-self-adjoint T_rho).  Repair R1 applied and verified.

## O1b (Lemma 3) - moving-jump FH derivative
- Statement: d lambda_k/d eps|_0 = lambda_k (c_+ - c_-) u_k(x_j)^2;
  dD/d eps|_0 = -(c_+ - c_-) f(x_j) (rightward), +(c_+ - c_-) f(x_j)
  (leftward distance); stationarity forces f(x_j) = 0.
- Depends on: AEH Lemma 2.1 (primary source), Lemma 1 (eigenvalue
  convergence under L^1 density convergence), uniform H^2 bounds, Dirac
  family / smoothing limit (R4), dominated convergence.
- Evidence/status: PROVED (re-derived in this run; numerically verified
  16/16 lambda derivatives and 16/16 D derivatives at eps = 1e-4; sign flip
  confirmed; smoothing limit confirmed to 0.03-0.3%).
- Verdict: PASS.
- Prior verdict (on the draft): FAILED-as-stated (sign error).  Repair R2 + R4
  applied and verified.

## F-001 repair chain (arithmetic)
- Statement: ||S_rho - S_sigma||_HS^2 <= (R/32)(||A||_2^2 + ||A||_1^2)
  <= (R^2/16)||A||_1, hence ||S_rho - S_sigma||_HS <= (R/4)||A||_1^{1/2}.
- Depends on: |sqrt(u)-sqrt(v)| <= |u-v|/2 (u,v >= 1), G <= 1/4,
  ||A||_2^2 <= (R-1)||A||_1, ||A||_1 <= R-1.
- Evidence/status: VERIFIED (derived analytically in this run; 11/11 numeric).
- Verdict: PASS (final bound unchanged by the repair; pre-correction line was
  not derivable).

## O1c (Lemma 2) - structure of f
- Statement: f = lambda_1 u_1^2 - lambda_2 u_2^2 has at most two zeros in
  (0,1) and {f > 0} = (x_-, x_+) with z_0 (zero of u_2) inside.
- Depends on: Wronskian algebra, Sturm oscillation, sign convention (R3).
- Evidence/status: PROVED (prior independent audit 422A69; consistency read
  in this run; numeric checks in the audited run's battery).
- Verdict: PASS (unchanged point; no new gap in the re-read).

## O1d (Lemma 4) - N-jump compactness and at most two effective jumps
- Depends on: O1a (continuity), O1b (stationarity), O1c (zero count).
- Evidence/status: PROVED (prior audit; consistency read here).
- Verdict: PASS (unchanged point).

## O1e (Lemma 5) - step functions are dense
- Depends on: O1a.
- Evidence/status: PROVED (prior audit; consistency read here).
- Verdict: PASS (unchanged point).

## O1f (Lemma 6) - bang-bang at a global extremizer
- Depends on: AEH Lemma 2.1, existence of the K_2 global extremizer
  (synthesis), piecewise-constant structure (F-003 presentational).
- Evidence/status: PROVED (prior audit; consistency read here).
- Verdict: PASS (unchanged point).

## Synthesis (SUP/INF, attainment)
- Depends on: O1a-O1f.
- Evidence/status: PROVED (prior audit; consistency read here).
- Verdict: PASS.

## Non-circularity
- Lemma 1 depends only on standard operator facts and the comparison bounds.
- Lemma 3 depends on AEH Lemma 2.1 and Lemma 1 (acyclic).
- Lemma 4 depends on Lemmas 1-3; Lemma 5 on Lemma 1; Lemma 6 on AEH Lemma
  2.1 and the existence result from the synthesis; the synthesis on Lemmas
  1-6.  No lemma uses the theorem under proof.

## Edge cases and degenerate cases
- rho = sigma; R -> 1+; a = b; (a,b) = (0,1); a = 0 or b = 1; jumps at 0 or 1
  (zero measure effect, absorbed).  All covered by the closed parameter domain
  and Lemma 1 continuity.