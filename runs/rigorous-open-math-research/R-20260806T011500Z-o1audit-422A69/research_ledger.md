# Research ledger (audit run R-20260806T011500Z-o1audit-422A69)

Timestamps approximate (UTC), date 2026-08-06.

## A-001: packet and target normalization
- Read the task packet, O1_reduction_draft.md, obligation_graph.md,
  problem_contract.md, research_ledger.md, status_and_literature.md of the
  draft run; agenda/problems/O-2026-SL-GAP-3B7A2C.md.
- Normalized the audit contract (problem_contract.md) and repro manifest.
- Decisions: audit only O1 (per packet); verdicts PROVED / PARTIAL / FAILED /
  OPEN per obligation; do not repair the draft.

## A-002: primary-source recheck (AEH)
- papers/fundamental_gap.txt = arXiv:2407.02459v2 (header "3 Jul 2024").
- Lemma 2.1 quoted in full (FH formula, V and w families, dw/dkappa in L^1,
  normalization int w u_n^2 = 1).
- Lemma 2.2 quoted in full (items (1)-(5), Wronskian proof, sign convention
  u_{1,2} > 0 near 0).
- Finding: draft Lemma 2 = correct re-derivation of (1),(4),(5); the moving
  jump derivative is NOT literally covered by Lemma 2.1 (dw/dkappa is a
  delta); the draft's Lemma 3 sign is inconsistent with its own verified
  identity dD/du = -2(R-1) f(u).

## A-003: solver development and bug fixes (important audit-internal history)
- v1 of verify_o1_audit.py had three bugs found by adversarial checking:
  1. find_roots bracket missed eigenvalues at bracket endpoints (constant
     density rho=1: lambda_1 = pi^2 exactly at the k=2 lower endpoint);
     fixed by a robust wide-bracket k-th-root search.
  2. eigpair returned the first root of the k=2 bracket, which equals
     lambda_1 in degenerate cases; fixed by scanning [pi^2/(2R), 9 pi^2] and
     taking the two smallest roots.
  3. analytic per-block normalization integral had cos^2/sin^2 signs swapped,
     making nrm wrong by up to a factor ~2 and shifting f and u*; fixed to
     I = A^2(L/2 + sin(2 wL)/(4w)) + B^2(L/2 - sin(2 wL)/(4w)) + AB(1-cos(2 wL))/(2w).
- After fixes: int rho u_1^2 = 1.0000065 (grid), u* = 0.45148546576,
  D* = 32.61398361770, lambda = (6.10928, 38.72326) - all match the contract.
- Lesson recorded: a "small" normalization error invalidates f values while
  leaving the SIGN STRUCTURE (zeros/interval) intact; structure checks alone
  cannot catch normalization bugs.  This mirrors the draft-run lesson about
  kc_apply (session 9 in AGENTS.md).

## A-004: O1b sign determination
- Derivation: moving jump right by eps -> rho_eps = rho - (c_+ - c_-) chi,
  partial rho/partial eps = -(c_+ - c_-) delta, FH gives
  dlambda_k/deps = +lambda_k (c_+ - c_-) u_k(x_j)^2,
  dD/deps = -(c_+ - c_-) f(x_j).
- Numerics (u = 0.2, b = 0.65, [1,4,1]): right difference 30.828430 vs
  corrected prediction 30.828320 (match ~1e-4); draft prediction -30.828320
  (sign fails).  Left difference: -30.828209 vs +30.828320 (again match after
  accounting for the orientation).
- Symmetric family: dD/du matches -2(R-1) f(u) at u in {0.2, 0.3, 0.4, 0.49}
  to ~1e-7 and at u* to ~1e-8.  Confirms the contract identity and falsifies
  the draft Lemma 3 sign.
- The zero-condition consequence f_N(x_j) = 0 is unchanged (both one-sided
  derivatives must be nonpositive at a max).

## A-005: O1c structural verification
- 10 random 3-block configs (values {1,4} and uniform in [1,4]) and 4 random
  5-block configs: nzeros_u2 = 1, nzeros_f = 2 (at most 2), single positive
  interval containing z_0, W < 0 on (0,1), v strictly decreasing.  All hold.

## A-006: O1a / O1e / O1f / boundary checks
- L1 continuity: moving a jump by eps in {1e-3, 1e-4, 1e-5} gives
  |dlambda_k| ~ O(eps); consistent with continuity (evidence).
- Operator defect identified: T_rho not self-adjoint on L^2; repair via
  S_rho = rho^{1/2} T_rho rho^{1/2} (Hilbert-Schmidt, symmetric) with
  ||S_rho - S_sigma||_HS -> 0; or weighted space L^2(rho); or direct
  Rayleigh-quotient estimate (|lambda_k(rho) - lambda_k(sigma)| bounded by
  C * ||rho - sigma||_1 * lambda_k-type terms).
- O1f direction: increasing rho on {f > 0} increases D (dD ~ w f > 0),
  increasing on {f < 0} decreases D (dD ~ w f < 0) - matches corrected sign.
- Boundary: D(rho=1) = 3 pi^2, D(rho=R) = 3 pi^2/R; 2-block and a=b configs
  inside closed families.
- Global search evidence: 1200 random configs (2-6 blocks), best D =
  32.3416 < 32.61398, worst D = 6.8828 > 6.78448; no counterexample found
  (evidence only).

## A-007: hash and provenance recording
- Packet sha256 verified against manager run-manifest.json.
- Input file hashes recorded in repro_manifest.md.

## Decisions
- Verdicts: O1a PARTIAL, O1b FAILED (as stated), O1c PROVED, O1d PROVED,
  O1e PROVED, O1f PROVED.  Overall draft verdict REPAIRABLE_GAP.
- Artifacts finalized in this run root; draft files untouched.
