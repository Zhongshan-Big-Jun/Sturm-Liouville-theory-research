# Research ledger: R-20260806T200000Z-o3a-c1b-7F3A9B

Chronological record of effective research.  All numerics in reproducibility/.
Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1).
Wall-clock spans are honest but not independently audited.

## R-001 (setup): contract and manifest written; inputs hashed
- problem_contract.md and repro_manifest.md written (ASCII).
- Input hashes in reproducibility/hash_inputs.txt (task packet, prior-run
  candidate/contract/audit, branch-run candidate, T1-T4 chain, AEH txt, c1_lib).
- Copied c1_lib.py from the C1 run into this run's reproducibility/.

## R-002 (foundation re-verification): P1, P2/T3
- explore_1.py: P1 (FH with eigenvalue factor) verified to 1e-8 at four configs,
  R=4 (matches prior values 16.739/55.627).  T3 (dR1/db = -dR2/da) verified to
  1e-8..1e-11.  PASS.

## R-003 (NEW mechanism probe: convexity of D in (w,t) coords)
- explore_2/3.py: D_ww = (Daa-2Dab+Dbb)/4 and D_tt = (Daa+2Dab+Dbb)/4 computed
  over the triangle and on the axis b = 1-a.
- FINDING (falsifies the naive convexity route): for R >= ~1000, on the axis
  LEFT of the fp (a in (0.40, ~0.492)), BOTH D_ww > 0 and D_tt > 0 (e.g. R=1e4,
  a=0.49: D_ww ~ +3.7e4, D_tt ~ +4.1e-2); D_ww/D_tt < 0 only in a neighborhood
  of the fp (a in (0.492, 0.5)) and at small a.  At the fp itself D_ww < 0 and
  D_tt < 0 for every tested R (negative-definite Hessian, consistent with fp a
  local max).  CONSEQUENCE: "D_ww < 0 on the whole axis" and "D_tt < 0 on the
  whole triangle" are FALSE.  The convexity sufficient condition for C1 is void.
  Lesson: the axis gap d(a) = D(a,1-a) is NOT concave on (0,1/2): d'' changes
  sign near a ~ 0.492 (R=1e4); the fp is a local max of d but d has an
  inflection.  R1_sym(a) = -d'(a)/(2(R-1)) is therefore NOT monotone on the
  axis; uniqueness of its zero must come from elsewhere.

## R-004 (branch structure re-mapping; corner analysis)
- Found the main-sheet branch Gamma_1 leaves the corner (a0, a0) with slope
  db/da = -R1_a/R1_b (one-sided limits) given by: 484 (R=1.05), 122 (1.2),
  25 (2), 9.0 (4), 3.68 (10), 1.24 (100), 1.024 (1000), 1.0024 (1e4),
  1.0003 (1e5), 1.0002 (1e6).  Steep for R near 1; nearly the diagonal for
  large R.
- NOTE (correction to my earlier invalid corner scan): configs with a > b are
  INVALID; R1R2(a,b) with a > b returns garbage.  All valid corner limits are
  one-sided from inside the triangle.
- explore_10.py traced the full main sheet for R in {1.02..1e4}:
  a_max1(R): 0.4222 (1.02), 0.4260 (1.05), 0.4438 (1.2), 0.4735 (1.5),
  0.5117 (2), 0.5646 (3), 0.6008 (4), 0.7060 (10), 0.8814 (100); for R=1000/1e4
  the tracer terminated early (a_max1 ~ 0.5804 artifact) due to corrector
  failure near the right end (multi-sheet hazard, documented in prior runs);
  R=1e5/1e6 traces failed (same cause).
- h(a0) < 0 for ALL tested R (values: -0.1603 (1.02) .. -0.0038 (1e4)); the
  R -> 1+ limit is h(a0) -> a0 - b0 = -0.1608 (NOT 0; consistent with g1^{-1}(b0)
  -> a0).  h(beta) > 0 wherever computed.

## R-005 (E1 reduction, independent of prior runs)
- Verified the reflection identities: h(a0) = g1^{-1}(b0) - b0 and
  h(b0) = g1(b0) - b0 (using g2 = 1 - g1^{-1}(1-a), g1(a0) = a0, g2(b0) = b0).
- Hence, for beta = b0: E1 (h(a0) < 0 < h(b0)) is EQUIVALENT to the single
  inequality g1(b0) > b0 (g1 increasing).  For beta = a_max1 < b0 (R <= ~3):
  h(a_max1) = g1(a_max1) - g2(a_max1) ~ 1 - g2(a_max1) = g1^{-1}(1-a_max1) > 0
  AUTOMATICALLY (g1^{-1} of a value in (a0, b0) is positive) PROVIDED the branch
  reaches b = 1 at a_max1 (numerically g1(a_max1) ~ 0.97..0.998 for R <= 3).
- g1(b0) values: R=4: 0.8469 (h = +0.2665); R=10: 0.7101 (h = +0.1297);
  R=100: 0.6182 (h = +0.0378).  Matches the manager's evidence and ~0.38/sqrt(R).
- Structural finding on R1(b0, .): for R >= ~4, R1(b0, b) = 0 has TWO
  sign-consistent roots: the x_+ root (v(b0) = -q, e.g. 0.6009 at R=4) and the
  x_- root g1(b0) (v(b0) = +q, e.g. 0.8469 at R=4).  R1(b0, b0+) < 0.  For
  R <= 3, R1(b0, .) has only the x_+ root (0.6036 at R=2, 0.6021 at R=3): the
  branch does not reach a = b0 (a_max1 < b0).  The manager's lead (4)
  ("g1(b0) > b0 iff b0 in the band on (b0, g1(b0))") is INCORRECT as stated:
  R1(b0,b) < 0 on (b0, x_+root), i.e., b0 is OUTSIDE the band there; the x_+
  root is the FIRST crossing to positive; g1(b0) is the SECOND root (x_- type).
  Corrected understanding recorded.
- E1 is therefore tied to the coverage part of H2 (branch extends past b0 for
  R >= ~3.7) plus the ordering of the two roots.  Both numerically verified.

## R-006 (band-endpoint monotonicity probe, manager lead B)
- x_- and x_+ (zeros of f, i.e. level crossings of v) computed by bisection.
  R=4 data at 4 configs: dx+/da > 0 (~+0.40), dx+/db < 0 (~-0.13);
  dx-/db > 0 (~+0.40), dx-/da < 0 (~-0.13, sign varies near the corner).
- FINDING: x_- and x_+ are NOT jointly increasing in both arguments (dx+/db < 0,
  dx-/da < 0).  The manager lead B monotonicity ("x_- and x_+ strictly
  increasing in a and in b") is FALSE in general.  However there is a striking
  near-exact structure: dx-/da ~ -dx+/db and dx+/da ~ -dx-/db (twist/decoupled
  structure: x_- depends mostly on b, x_+ mostly on a).  At (0.45,0.55):
  dx-/da = -0.133, dx+/db = -0.132; dx-/db = +0.414, dx+/da = +0.414.
  Candidate structural identity: dx_+/db = -dx_-/da and dx_+/da = -dx_-/db
  (exact?) -- TO VERIFY.  If exact, the fixed-point system decouples in a
  "twist" form; T(a,b) = (x_-(a,b), x_+(a,b)) with Jacobian [[-J, +K],[+K', ...]]
  structure worth pursuing.

## R-007 (literature probe)
- Web search: no published statement of O3a-type two-parameter branch uniqueness
  found; the literature on the minimum gap (Qi-Li-Xie QTDS 2020; JMA 2022) treats
  the INF side over piecewise-constant/bounded-jump classes, not the SUP-side
  interior critical point uniqueness of the 3-block family.  Consistent with the
  prior audits' novelty assessment.

## Open items
1. E1 (g1(b0) > b0) -- clean target; tied to branch coverage + root ordering.
2. M-shape of h' (G-M) -- main bottleneck.
3. Verify/exploit the exact twist identities dx_+/db = -dx_-/da, dx_+/da = -dx_-/db.
4. Independent counterexample search over the full (a,b,R) domain.

## R-008 (twist identity verified; reflection is exact)
- x_-(sigma(a,b)) = 1 - x_+(a,b), x_+(sigma(a,b)) = 1 - x_-(a,b) verified to 1e-16 at
  generic points (R in {2,4,100,1e4}).  PROOF: reflected problem's ratio v'(x) = c_v v(1-x)
  with c_v = y1'(1)/y2'(1) < 0 and q' = -c_v q, so x_+'(sigma) = 1 - x_-.  Derivative
  consequences at symmetric points (a+b=1): dx_+/db = dx_-/da and dx_+/da = dx_-/db
  (chain rule; NOT a decoupling, just the involution).  The "twist" is real but yields no
  new information beyond the reflection symmetry (T2).

## R-009 (NEW: multi-sheet structure near the corners for large R; H2 needs revision)
- For R >= ~600-1000, the R1 = 0 branch set has THREE x_- type sheets near a = a0
  (e.g. R=1e4, a=a0+1e-5: b-a = 2.4e-8, 1.19e-4, 1.21e-3) and three sheets near b = b0
  (two x_+ plus the main x_-).  The sheet through (a0,a0) (S1, b ~ a) merges with S2 at a
  saddle-node a* ~ 0.429 (R=1e4); the fp-containing branch (S3, largest b-a near a0) is a
  SEPARATE connected component that does NOT pass through (a0,a0) for large R.
- CONSEQUENCE: hypothesis H2 (Gamma_1 a single graph over I_1 through (a0,a0)) is FALSE
  for large R; the main-sheet convention must be "the fp-containing component", and the
  endpoint identity g1(a0) = a0 fails there (R=1e4: g1(a0) = 0.420775 on S3).  E1 must be
  stated on the fp-component; the manager's "E1 iff g1(b0) > b0" is exact only in the
  non-split regime (R <= ~600) where g1^{-1}(a0) = a0.
- Verified on auxiliary sheets: R2 ~ 0.01..0.02 (bounded away from 0), so no good roots
  hide there.  Secular equation confirmed correct by ODE shooting (scipy solve_ivp);
  the finite-difference matrix discretization is UNRELIABLE when the barrier is narrower
  than the grid (barrier width 1.2e-4 at N=6000-8000), which caused a red herring.

## R-010 (h/h' profile on the TRUE fp-branch S3)
- Sampled S3 from the fp outward (a in [~a0, b0]) for R in {4,100,1000,1e4,1e5}:
  - h(a0) < 0 and h(b0) > 0 for every tested R (E1 holds on the fp-branch).
  - h has exactly ONE zero, at the fp.
  - h' > 0 on all of I for R <= 1000; for R >= 1e4, h' has EXACTLY TWO zeros
    (R=1e4: 0.4467, 0.5521) with sign pattern - + - (h'(a0+) < 0, h'(b0) < 0).
    This is the M-shape, confirmed on the correct branch.
  - g1' - 1 on S3: exactly ONE zero for large R (R=1e4: at 0.4648; sign - then +),
    strictly positive for small R; g1' max at the fp (g1'(fp) -> sqrt(2) ~ 1.42).

## R-011 (contraction route REFUTED)
- Spectral radius of J_T = d(x_-,x_+)/d(a,b) over the triangle: max 0.49 (R=2), but
  1.042 at (0.80,0.95) (R=4).  T is NOT a contraction on the whole triangle; the
  Banach fixed-point route fails.  (Eigenvalues at (0.8,0.95): -1.042, +0.152.)

## R-012 (good-root hunt; no extra good roots)
- Cell sign-change hunt + least_squares refine over the full triangle for R in
  {2,4,100,1000,1e4,1e5}: no good roots beyond the symmetric fp (the fp itself was not
  resolved by the coarse grid - expected; prior runs resolved it).  Auxiliary sheets have
  |R2| >= ~1e-2 away from the fp.  Consistent with C1.

## R-013 (E1 asymptotics, partial)
- h(b0)*sqrt(R) -> ~0.379..0.382 (R=100..1e5); h(a0)*sqrt(R) -> -0.38 (same).
- a_fp: 1/2 - a_fp ~ 0.118/sqrt(R) (confirmed R=100..1e7 range).
- Point-mass limit derived for the symmetric heavy barrier: odd modes s = 2*pi*k exactly;
  even fundamental solves cot(s/2) = s*mu/2 with mu = point mass; s ~ 2/sqrt(mu), lambda_1
  ~ 4/mu -> 0.  Constants 0.38/0.118 not yet derived from the finite-width expansion.
