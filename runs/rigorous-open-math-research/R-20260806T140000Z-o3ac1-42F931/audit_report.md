# Audit report (run R-20260806T140000Z-o3ac1-42F931)

Independent verification pass (single-agent fallback: verifier role executed
after the explorer/synthesizer passes, with an adversarial checklist).
Scope: the candidate proof (candidate_proof.md), the contract
(problem_contract.md), and the rechecked premises P1-P4, O1c, T1-T3.

## Verdict

REPAIRABLE_GAP (for the overall goal C1).  The reduction R6 is sound; the
remaining obligations (E1) endpoint signs and (M) M-shape of h' are
numerically verified but analytically open.  No fatal gap, circular
reduction, or wrong-problem issue was found in the proved part.  The claim
"C1 is proved" is NOT made; any such claim would be blocked by G-E1 and G-M.

## Audit of the proved lemmas (this run)

R1 (reflection of residuals).  PASS.  The map y(x) -> y(1-x) is a bijection
between eigenpairs of the reflected problems with equal L^2(rho)-norms;
f'(x) = f(1-x) follows; R1(sigma) = R2 and R2(sigma) = R1 are immediate.
Numerics at 1e-16 confirm.  Edge cases: a' = 1 - b > 0, b' = 1 - a < 1
preserved for 0 < a < b < 1.  No issue.

R2 (sigma(Gamma_1) = Gamma_2).  PASS with one flagged dependency: the
sign-tracking (c_v = y_2'(1)/y_1'(1) < 0, so sign-consistency a = x_-,
b = x_+ is preserved under reflection) is complete and verified
(max|R2| on the image ~1e-9..1e-11, v(b') < 0 preserved).  The step
"the image is the main-sheet component" uses the single-component structure
of the main sheets (H2, part of Lemma C), which remains OPEN.  Under H2 the
lemma is correct; without H2 the statement must be read as "sigma maps
Gamma_1 into the Gamma_2 branch set with the correct sign-consistency".
Impact on C1: H2 is an explicit hypothesis in the contract (section 2), so
the reduction is honest.

R3 (h-reflection formulas).  PASS.  Requires g1' > 0 on I (branch slope
positivity, part of H2/Lemma C; numerically verified).  u'(a) = -1/g1'(u(a))
by the inverse function theorem; algebra checked.

R4 (integral identity).  PASS.  Pure FTC from R3.1; the MVT corollary is
correct as stated (sign(h) = sign(a - u(a)) * sign(g1'(xi) - 1)).

R5 (good roots = zeros of h).  PASS.  (i) uses O1c (v strictly decreasing ->
f has at most two zeros, x_- < x_+; R1 = R2 = 0 forces a = x_-, b = x_+).
(ii)-(iii) are algebraic given H2's coverage of I.  The equivalence
"C1 iff {R1 = R2 = 0} has a unique solution" is correct.

R6 (C1-reduction).  PASS (elementary monotonicity).  Verified the sign
arithmetic: with h' pattern - + - and h(x1) < 0 < h(x2), h crosses zero
exactly once on (x1, x2) and nowhere else.

## Audit of the rechecked premises

P1 (FH with eigenvalue factor).  PASS.  The derivation in the source run
carries the lambda factor; the naive version without it contradicts FD and
is rejected.  Re-verified: (0.42, 0.56, 4) FD dD/da = 38.887 = -(R-1) R1
with R1 = -12.9624.

P2 (= T3).  PASS.  P1 + real-analyticity + Schwarz; no circularity.

P3 (branch-slope identities).  PASS.  At the symmetric fp, A = -C by
reflection invariance of D, so g1' g2' = 1; h' = g1' - 1/g1' at fp.
Numerics to 1e-12.

P4 (R = 1 base).  PASS.  Direct computation of v, q, f_0; a0, b0 exact.

O1c (v strictly decreasing).  PASS.  Wronskian argument; matches AEH
arXiv:2407.02459v2 Lemma 2.2 (v2 checked); numerics consistent.  Flag:
O1c is used as a premise in R5(i); its source (prior run + AEH v2) is
acceptable, and the current run independently re-derived the Wronskian sign.

T1, T2.  PASS (rechecked from the 2026-08-05 run agentB_O3a_fixed_point.md:
T1 good root <=> fixed point of T; T2 T sigma = sigma T).  These are
standard and were not re-derived from scratch this run; they enter only
through the equivalence chain and are consistent with R5.

T4 (conditional uniqueness).  NOT USABLE: hypothesis (b) refuted (CE-1).
No reliance on T4 anywhere in the current candidate.

## Audit of the numerical evidence for E1 and M

- Method: two independent eigenvalue paths (secular roots via c1_lib
  adaptive scan; reflection formula for g2), closed-form implicit branch
  derivatives (partials in c1_lib), finite differences (h = 1e-6..1e-4
  stable).  Agreement to ~1e-6 or better.
- Solver bug audit: the earlier roots2 scan cap (2 pi + 1e-3) was found to
  miss eigenvalues above 4 pi^2 for heavy barriers (ledger R-103); all
  evidence tables in shape_v6/dip_study/final_shape were regenerated with
  the adaptive cap (6 pi).  The phantom "branch gaps" were artifacts.
- Coverage: R in {1.02, 1.05, 1.1, 1.2, 2, 4, 10, 100, 1000, 1350, 1500,
  2000, 3000, 1e4, 1e5, 1e6, 1e7}; a-grids of 100-300 points per R.
- Limitation: all of this is finite numerical evidence; it does NOT close
  the "for every R > 1" quantifier.  Stated honestly in the status.

## Exact remaining gaps

- G-E1: endpoint signs h(a0) < 0 < h(beta) for every R > 1.  Numerically
  verified; asymptotics partial (h ~ +/- 0.38/sqrt(R) at large R); the
  R -> 1+ limit is degenerate and not closed.
- G-M: M-shape of h' for every R > 1.  Numerically verified (transition
  R ~ 1350-1500 for the right dip, ~3000 for the left dip; |h'| <= 0.012);
  no analytic proof.
- G-C (H2): single-graph branch structure and coverage of good roots by I.
  Hypothesis; multi-sheet hazards documented (CE-4).
- G-Z: h(fp) = 0 depends on O2 (existence of the symmetric fixed point),
  assumed from the portfolio chain.
- G-N: nondegeneracy det J_res away from fp (needed for any continuation
  argument) is not established.

## Confidence by axis

- Semantic fidelity: HIGH (contract audited against the packet and source;
  no quantifier silently changed; main-sheet convention H3 made explicit).
- Mathematical correctness (proved part): HIGH (elementary proofs, each
  re-checked; numerics confirm).
- Completeness (C1): LOW (G-E1, G-M open).
- Novelty: not claimed for C1; R1-R6 are new elementary lemmas of this run.
- Reproducibility: HIGH (all scripts and JSON data under reproducibility/;
  commands recorded in research_ledger.md).

## Residual risks

- The multi-sheet structure (CE-4) means any future proof must either prove
  H2/Lemma C or avoid the sheet-selection question; the reflection route
  (R2) already avoids direct sheet tracing.
- The interval certificate CE-1 has the standard mpmath.iv trust model
  (outward rounding), not a formal proof-assistant certificate.
- All asymptotic constants (~0.38, ~0.118, sqrt(2)) are numerically
  inferred, not proved.