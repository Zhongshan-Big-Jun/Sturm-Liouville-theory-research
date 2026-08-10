# Research ledger: R-20260806T140000Z-o3ac1-42F931

Chronological record (effective research; wall-clock spans are honest but not
independently audited).  All numerics in reproducibility/; Python 3.10
(numpy 2.2.6, scipy 1.15.3), xelatex at D:\texlive\2024.

## Handoff state (start of this continuation)
- problem_contract.md and repro_manifest.md already written.
- Key observation from the handoff: sigma(a,b) = (1-b, 1-a) maps Gamma_1 onto
  Gamma_2; h(a) = g1(a) - 1 + g1^{-1}(1-a); h'(a) = g1'(a) - 1/g1'(u(a)).
- Tooling issues known: verify_refl.py crashed (degenerate config), check_props
  crashed (None filtering), hp_accurate timed out, multi-sheet hazard for Gamma_2.

## R-101 (setup): re-derived the reflection identities at first principles
- R1(sigma(a,b)) = R2(a,b), R2(sigma(a,b)) = R1(a,b): verified to 1e-16 at
  generic points, R=4.  Slope-normalization subtlety: the reflected
  slope-normalized ratio is v'(x) = c_v v(1-x), c_v = y_2'(1)/y_1'(1) < 0;
  sign-consistency is preserved.  This fixes the sign question that the
  reflection map is about.

## R-102: verify_refl2/3 (reflection structure)
- Fixed trace_g2 sign bug (sign point must be b for Gamma_2, not a).
- Confirmed sigma(Gamma_1) subset Gamma_2 with max|R2| ~ 1e-9..1e-11, and
  v(b') < 0 on the image (R in {2, 4, 100, 1000, 1e4}).
- Confirmed h(a) = g1(a) - 1 + g1^{-1}(1-a) to ~1e-6 (trace-limited).
- Domain facts: Gamma_1 leaves (a0,a0) with steep slope and climbs to
  (a_max1, g1(a_max1)) with g1(a_max1) close to 1; Gamma_2 = sigma(Gamma_1)
  has a-domain [1 - g1(a_max1), b0]; b_min2 = 1 - g1(a_max1) (endpoint
  identity), verified to trace precision.

## R-103: roots2 scan-range bug (important)
- Discovered roots2 (secular root scan up to 2*pi+1e-3) MISSES eigenvalues
  pushed above 4*pi^2 by heavy barriers (e.g. s2 > 6.284 near a = b0 at
  R = 1e4).  This created phantom "gaps" in the branch.  Fix: adaptive retry
  up to 6*pi.  Patching L.roots2 at import time in all scripts.
- Lesson: eigenvalue scans must be adaptive to the heavy-weight regime; the
  "gap" in Gamma_1 at a ~ 0.58 for R = 1e4 was an artifact, not structure.

## R-104: geometric scans
- Near-diagonal R1/R2 roots (b - a ~ 4e-4 at large R) are missed by uniform
  b-scans (even numbers of sign changes within the first interval).  Fix:
  geometric grid in (b - a) near a + uniform grid far from a.  Verified all
  R1-roots with v(a)>0 for a grid at R = 1500, 1e4, 1e5, 1e6.

## R-105: branch structure (corrected picture)
- Gamma_1: single root with v(a) > 0 per a (no multi-sheet ambiguity) on the
  relevant range; leaves (a0,a0) steeply, passes the fp, ends at a_max1(R)
  with g1(a_max1) ~ 1.  a_max1 is NOT monotone in R (grows to ~0.985 at
  R=1e4, then shrinks to ~0.616 at R=1e5-1e6); beta = b0 for R >= ~4.
- Gamma_2: multi-sheet hazard near the right end at large R: at R=1e4,
  a=0.57364 there are THREE R2-roots with v(b)<0 (b = 0.5737, 0.5738, 0.5748);
  only the largest is the main sheet (component through (b0,b0)).  At R=1e4,
  a <= 0.55: unique root.  Consequence: direct g2 tracing must use the
  reflection formula (from single-sheeted g1) or main-sheet selection.
- h(a0) and h(beta) endpoint values recomputed pointwise; h(a0) ~ -0.38/sqrt(R),
  h(b0) ~ +0.38/sqrt(R) for large R (fits the prior-run asymptotics).

## R-106: shape tables (shape_v4/v5/v6, dip_study, final_shape)
- Clean tables for R in {1.02..1e7}: h(a0) < 0, h(beta) > 0, h > 0 on
  (fp, beta], h'(fp) > 0 for ALL tested R.  h'(a0) and h'(b0) both tend to 0.
- M-shape of h' confirmed: for R <= ~1350, h' > 0 on all of I (h strictly
  increasing).  For R >= ~1500, h' < 0 on an interval near the right end
  (certified at R=1500, a=0.57364 by CE-1: h' ~ -3.4e-4).  For R >= ~3000
  additionally h' < 0 on an interval left of fp (a ~ 0.43-0.46, h' ~ -0.003
  to -0.012).  Both dips shallow; h stays positive on (fp, beta].
- g1' profile (exact implicit derivatives): g1' > 1 mostly; dips below 1 to
  ~0.98 near a ~ 0.42-0.44 for R >= ~1000 (e.g. R=1500: g1'(0.42) = 0.9804;
  R=1e4: g1'(0.43) = 0.9897).  This REFUTES the naive sufficient condition
  "g1' > 1 on I" (MVT route).  g1'(fp): R=4: 2.752, R=1e4: 1.421, R=1e6:
  1.411 (limit consistent with sqrt(2)).
- Nondegeneracy: det J_res = AC + B^2 < 0 at the fp for all tested R
  (R=4: -107576.4; R=1e6: -1.4); det Hess(D) > 0, D_aa = D_bb < 0 (fp is a
  local maximum of D).  Hessian identities (R-1)A = -D_aa, (R-1)B = D_ab,
  (R-1)C = D_bb re-verified.

## R-107: reductions (this run's main mathematical output)
- Lemma R5(i): R1 = R2 = 0 with 0 < a < b < 1 forces a sign-consistent good
  root (uses O1c: v strictly decreasing, at most two zeros of f, ordered).
  C1 is equivalent to: {R1 = R2 = 0} has a unique solution (per R > 1).
- Lemma R4: h(a) = integral_{u(a)}^{a} (g1'(t) - 1) dt (exact; from the
  reflection identity + FTC).  MVT corollary shows the sign structure; the
  naive g1' > 1 route is refuted (CE-3), so the integral form is the right
  object.
- Lemma R6: C1 follows from endpoint signs + M-shape + h(fp) = 0 (proved).
  The M-shape and endpoint signs are the exact remaining gap.

## R-108: failed routes / lessons (see also approach_registry)
- Lemma A (g1' > g2' everywhere): refuted by CE-1 (interval certificate,
  prior run; values rechecked: at (1500, 0.57364) certified h' < 0).
- MVT sufficient condition (g1' > 1 on I): refuted numerically (CE-3).
- Newton continuation on the full system (c1_sys.py): sheet jumps; abandoned
  in favor of the reflection formula.
- R -> 1+ perturbation (naive IFT on branch functions): degenerate at R=1
  (branches are vertical/horizontal lines); not closed.
- Direct g2 tracing at large R: wrong-sheet hazard; use reflection formula.
- hp_accurate (high-precision direct trace): too slow (>1800s); replaced by
  pointwise partials.

## Open items for continuation
1. Prove (E1) endpoint signs analytically (h(a0) < 0 < h(beta)).
2. Prove the M-shape of h' (at most two zeros, ordered around fp, values
   h(x1) < 0 < h(x2)) for every R > 1.
3. Optional: asymptotic proof that g1'(fp) -> sqrt(2), h'(fp) -> sqrt(2) -
   1/sqrt(2) as R -> inf (numerically convincing, unproved).
4. Independent interval-arithmetic certificates for the M-shape over a
   compact R-grid (pattern: cert_ce1.py in the prior run).

