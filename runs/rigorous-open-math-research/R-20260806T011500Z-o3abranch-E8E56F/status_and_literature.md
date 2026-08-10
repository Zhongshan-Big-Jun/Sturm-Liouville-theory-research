# Status and literature: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

## 1. Problem and current status

Task Q-20260806-o3a-branch-E8E56F asks for proofs of Lemma A, Lemma B, Lemma C
of the prior run R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md,
which close obligation O3a: any sign-consistent interior critical point of the
gap D = lambda_2 - lambda_1 over the 3-block barrier family
rho_(a,b) = R on (a,b), 1 elsewhere, satisfies b = 1 - a.

Status (2026-08-06, end of this run):

- T1, T2, T3, T4 (prior run) audited.  Logic of T1, T2, T4 sound.  T3's proof
  is valid once the Feynman-Hellmann formula is stated with the eigenvalue
  factor (Proposition P1, candidate_proof.md); the identity
  dR1/db = -dR2/da was re-verified numerically to ~1e-8 at several points.
- Lemma A (pointwise g1' > g2' on the whole common range, all R > 1):
  REFUTED rigorously for R >= ~1400.  Three independent float methods agree
  (see counterexample_log.md, CE-1) and an interval-arithmetic certificate
  (reproducibility/cert_ce1.py) proves h'(a*) < 0 at (R, a*) = (1500,
  0.57364) and (1e4, 0.57364).  The R-uniform lower-bound claim in the task
  packet is false for two reasons: min h' -> 0 as R -> infinity, and h'
  becomes negative on a subinterval near the right end for R >= R* in
  (1200, 1500).
- Lemma B (endpoint signs h(a0) < 0 < h(beta)): verified numerically for
  R in {1.02, 1.05, 1.2, 1.5, 2, 3, 4, 10, 50, 100, 200, 500, 1000, 3000,
  1e4, 1e5, 1e6, 1e7}; not proved.
- Lemma C (single-graph branches, coverage of all good roots): verified
  numerically for the fixed-point-relevant components; not proved.  This run
  found extra Gamma_2 sheets (R2 = 0 with v(b) < 0 but v(a) < 0) at
  R = 1500, a = 0.57364; they are not sign-consistent fixed points, so the
  theorem-relevant content of Lemma C is unaffected, but the informal "only
  branch components" phrasing must be read accordingly (see
  counterexample_log.md).
- O3a itself (unique fixed point, hence symmetric by T2): numerically
  supported for R in {1.02, ..., 1e6}; h = g1 - g2 has exactly one zero in
  the common range for every tested R, located at the symmetric fixed point
  a_fp(R).  NOT refuted; proof remains open.  The T4 reduction is invalid for
  large R because T4(b) fails; a corrected structural conjecture (C1) is the
  replacement target.

Result label (skill output protocol): RIGOROUS_PARTIAL_RESULT, with the
rigorous (interval-arithmetic) counterexample to Lemma A and the corrected
conjecture documented precisely.

## 2. Premises rechecked against original sources

All premises used in this run were re-derived or re-verified; nothing was
assumed from the packet without checking.

1. AEH (Ahrami-El Allali-Harrell), "The fundamental gap of the vibrating
   string", arXiv:2407.02459v2, local copy papers/fundamental_gap.txt.
   - Lemma 2.1 (Feynman-Hellmann formula) re-derived; the exact form needed
     here is d lambda_k/d eps = -lambda_k int (d rho/d eps) u_k^2 dx, with u_k
     normalized by int rho u_k^2 = 1.  Verified numerically (e.g. at
     (a,b,R) = (0.42, 0.56, 4): d lambda_1/da = 16.739241 vs
     (R-1) lambda_1 u_1(a)^2 = 16.739; d lambda_2/da = 55.626551 vs
     3*37.098*0.4998166 = 55.627; dD/da = 38.88731049 = -(R-1) R1 exactly).
   - Lemma 2.2 (Wronskian: v = y_2/y_1 strictly decreasing; f has at most two
     zeros; {f > 0} is a single interval) re-derived in the prior run (O1c)
     and re-checked here (the Wronskian argument is elementary and correct).
2. Prior-run source agentB_O3a_fixed_point.md:
   - T1 (sign-consistent critical point <=> fixed point <=> good root):
     logic sound; depends only on O1c and the sign pattern.
   - T2 (sigma-equivariance; uniqueness implies b = 1 - a): sound.
   - T3 (dR1/db = -dR2/da): proof valid with the corrected FH formula
     (P1).  Numerically re-verified (sum of residuals ~1e-8 at four points,
     including the R = 4 fixed point and R = 10).
   - T4 (conditional uniqueness): sound as a conditional; hypothesis (b)
     (g1' > g2') fails for large R, so T4 no longer applies there.
   - The numerical tables of the prior run (R in {1.02..1000}) are consistent
     with this run's recomputations; the falsification of Lemma A occurs just
     outside that range (R* ~ 1350).
3. Standard SL theory: simplicity of Dirichlet eigenvalues of positive bounded
   weights, Sturm oscillation (one interior zero for y_2), real-analyticity of
   eigenvalues in (a,b) on the open set (secular function is real-analytic;
   simple roots; implicit function theorem).  Used without issue.

## 3. Literature and novelty

This is internal research-program work (portfolio MRP-20260731-BVE-SL).  The
immediate background is the prior run (R-20260805T000000Z-gapn1-a1b2c3) and
the project documents docs/SL_gap_extremals.* and the tool-library files
tools/residual-exactness.md, tools/gap-n1-reduction.md.  No new external
literature was required for the findings of this run.  The falsification of
the monotonicity lemma for large R is a new negative result for the internal
reduction; it does not contradict any published theorem known to this run.

Relevant local references:
- papers/fundamental_gap.txt (AEH arXiv:2407.02459v2)
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentB_O3a_fixed_point.md, agentB_lib.py, obligation_graph.md
- tools/residual-exactness.md, tools/gap-n1-reduction.md

## 4. Key numerical facts established (evidence; scripts in reproducibility/)

- Fixed point fp(R) = (a_fp, 1-a_fp) with a_fp(R): R=4 -> 0.451485465757;
  R=1000 -> 0.496260895480; R=1e4 -> 0.498806036580; R=1e6 -> 0.499880117060;
  R=1e7 -> 0.499962077951.  delta = 1/2 - a_fp ~ 0.118/sqrt(R) for large R
  (delta*sqrt(R): 0.1126 (50) ... 0.1199 (1e7)).
- Eigenvalues at fp: lambda_1 -> 0 (point-mass asymptotics: lambda_1 ~ 4/M,
  M = R*(1-2*a_fp) ~ 0.24*sqrt(R)); lambda_2 -> 4 pi^2 (from below);
  D -> 4 pi^2.  Matches session 13's R->inf limit for the SUP family.
- Branch gap h = g1 - g2 on the common range:
  - h(a0) < 0, h(b0) > 0 for all R tested; h(b0) ~ 0.38/sqrt(R) (verified to
    1e7: h(b0)*sqrt(R) = 0.3795 (1e4), 0.3800 (1e5), 0.3801 (1e6, 1e7)).
  - h' at the fixed point: 2.3887 (4), 0.97698 (50), 0.88593 (100),
    0.75452 (1000), 0.71737 (1e4), 0.70603 (1e5), 0.70244 (1e6),
    0.70097 (1e7); h'(fp) -> ~0.70.  g1'(fp) -> ~1.41, g2'(fp) -> ~0.71,
    and g1'(fp)*g2'(fp) = 1 identically at the symmetric fp (A = -C by
    reflection symmetry).
  - h' < 0 on a subinterval near the right end for R >= R* in (1200, 1500):
    e.g. R = 1500, a = 0.57364: h' = -0.000344; R = 1e4: min h' ~ -0.00345
    on [0.5532, 0.5789]; R = 1e5: h' ~ -0.00119 on [0.55, 0.5743] then h' > 0
    again near b0; R = 1e6: h' ~ -0.0004 over the tail.  h stays positive in
    the tail (h(b0) > 0), so h has exactly one zero.
- Branch derivative identities at the fp: A = -C (reflection), B > 0,
  g1' = A/B = -D_aa/D_ab, g2' = -B/C = -D_ab/D_bb, h' = g1' - g2'; at the
  R = 4 fp, A = 352.05, B = 127.92, C = -352.05, det Jres = -107576 < 0.

## 5. Remaining gaps (exact)

- G1: CLOSED (2026-08-06).  The falsification of Lemma A is now certified:
  reproducibility/cert_ce1.py (mpmath.iv, outward-directed rounding,
  iv.prec = 220) proves h'(a*) < 0 at (R, a*) = (1500, 0.57364) and
  (1e4, 0.57364), with verified root enclosures (width ~5e-28),
  sign-definite partials and denominators, and certified good-root checks.
  Trust model: standard verified computation (mpmath.iv outward rounding),
  not a machine-checked formal proof; see counterexample_log.md CE-1 and
  audit_report.md Section 5.
- G2: prove the corrected structure: h has exactly one zero in the common
  range for every R > 1 (equivalently O3a).  Numerically supported for
  R <= 1e6.
- G3: Lemma B and Lemma C as stated: still open (numerically supported).
- G4: asymptotic question: whether h(b0) - dip margin stays positive for all
  large R; the available scaling (h(b0) ~ 0.38/sqrt(R), |min h'| bounded by
  ~4e-3 with shrinking support) suggests yes, but no proof.
