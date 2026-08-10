# Research ledger - R-20260806T140000Z-o1revise-2ED02A

Timestamps approximate (UTC, local +8).  Chronological entries with concrete
evidence.  All numerics are evidence only; proofs are in candidate_proof.md.

## R-001 (2026-08-06): contract + provenance
- Read the task packet, the O1 draft, the audit report, the repair list, the
  draft obligation graph and problem contract; hashed all inputs
  (repro_manifest.md).
- Re-normalized the theorem statement in problem_contract.md: box class K
  = {1 <= rho <= R}, Dirichlet string, D = lambda_2 - lambda_1; SUP reduces to
  the 2-parameter barrier family, INF to the well family; both attained.
- Noted and recorded two recheck findings vs the audit text:
  (1) the packet/audit operator formula S_rho = rho^(1/2) T_rho rho^(1/2) is
  NOT symmetric when T_rho = T_0 M_rho; the correct symmetrization is
  S_rho = M_{sqrt(rho)} T_0 M_{sqrt(rho)} = M_{sqrt(rho)} T_rho M_{rho^{-1/2}}
  (kernel sqrt(rho(x)) G(x,t) sqrt(rho(t))); spectra coincide by similarity.
  (2) the audit's parenthetical "the two-sided derivative exists only if
  f(x_j) = 0" is imprecise: the signed map eps |-> D(jump at x_j + eps) is
  differentiable at every x_j with derivative -(c_+ - c_-) f(x_j); what
  differs is the SIGN of the derivative in the rightward/leftward DISTANCE
  parametrization.  Stationarity consequence f(x_j) = 0 unchanged.

## R-002 (2026-08-06): premise recheck (Phase 2)
- Verified AEH arXiv:2407.02459v2 (papers/fundamental_gap.txt, sha256
  2F3C90E6...) Lemma 2.1 (FH formula, hypotheses: V, w locally L1, inf V >
  -inf, C >= w >= 1/C, dw/dkappa in L1; normalization int w u^2 = 1) and
  Lemma 2.2 items (1)-(5) (monotonicity of u_2/u_1, structure of f) verbatim.
- Re-derived O1c with a GLOBAL W < 0 argument (W(0) = W(1) = 0, sign pattern
  of W' from the zeros of u_2) instead of AEH's reflection argument; valid for
  every rho in K and rho-independent.
- Verified Keller 1976 abstract (min lambda_2/lambda_1, 0 < a <= phi <= A,
  minimizer = a on (-x0,x0), A elsewhere) and MW 1976 Theorems 0-3
  (bounded-jump class, ratio): class difference confirmed, no O1 premise.
- Weyl/min-max inequality for self-adjoint compact operators: stated
  precisely (P3); draft's application to non-self-adjoint T_rho is invalid;
  the S_rho repair fixes it.

## R-003 (2026-08-06): O1b sign repair verified numerically
- verify_fh_sign.py (R=4): config [1,4,1], jumps at 0.2, 0.65.
  V1: signed derivative dD/deps = -(R-1) f(x1): numeric 30.8283210 vs
  predicted 30.8283199 (FD truncation only).
  V2: rightward delta: dD = -(R-1) f(x1) delta + o(delta); leftward: +; rel
  errors 3.6e-3 -> 3.6e-5 as delta -> 0.  The draft sign (+(R-1)f) is REFUTED.
  V3: d lambda_k/deps = lambda_k (R-1) u_k(x1)^2 to 2e-8/4e-9.
  V4: symmetric barrier identity dD/du = -2(R-1) f(u) reproduced at u in
  {0.2,0.3,0.4,0.49} to <= 1.4e-6 (FD truncation), consistent with the
  draft-run ledger R-003 and the audit cross-check.
- High-precision u*: zero of f at 0.451485468013 (bisection, f residual
  1.6e-12); D* = 32.613983617704 (contract 32.6139836177, match 4e-12).
  RECORDED DISCREPANCY: the draft-run contract/ledger values
  u* = 0.45148546584 / 0.451485465757 differ from this run's zero by ~2e-9;
  the D*/lambda values agree to 1e-11.  Conclusion: the draft-run u* digits
  are a precision artifact; no mathematical consequence (evidence-level note).

## R-004 (2026-08-06): O1a repair verified numerically
- Solver accuracy: constant cases and the two-block [1,4] exact secular
  equation match to <= 4e-13.
- verify_hs_bound.py (fixed step evaluation, see R-006): random rho,sigma in
  K (8 trials): ||S_rho - S_sigma||_HS <= (R/4)||rho-sigma||_1^{1/2} holds
  (ratios 0.06-0.17); Weyl |1/lambda_k(rho) - 1/lambda_k(sigma)| <=
  ||S_rho-S_sigma||_HS holds on all 16 cases; comparison bounds
  lambda_k in [k^2 pi^2/R, k^2 pi^2] hold; discretized symmetric-kernel
  eigenvalues match 1/lambda_k to O(1/N); eigenfunctions are O(eps)-Lipschitz
  under jump motion (maxdiff/eps -> const).

## R-005 (2026-08-06): O1c structure verified numerically
- verify_structure_f.py (fixed on-grid zero counting, see R-006): 22 hostile
  configs (alternating 1/R, random continuous values, random bang-bang, 3-8
  blocks): u1 has no interior zeros; u2 has exactly one interior zero z0; W <
  0 on (0,1); v = u2/u1 strictly decreasing; f has <= 2 interior zeros; {f>0}
  is a single interval containing z0.  All checks pass.
- Note: u2's zero sits exactly at a grid point for symmetric configs; the
  naive sign-change counter missed it (fixed in R-006).

## R-006 (2026-08-06): verification-tool bugs found and fixed (failure log)
- BUG-1 (stepvals): np.interp linearly interpolates between breakpoints,
  turning intended step functions into piecewise-linear functions.  Caused
  spurious Weyl "violations" in H2 and wrong kernel eigenvalues in H4
  (compare verify_hs_bound pre/post fix; H4 21% -> 4e-4 relative).  Fixed
  with np.searchsorted-based true step evaluation.
- BUG-2 (on-grid zeros): sign-change counting missed zeros lying exactly on
  grid points (symmetric configs, u2(0.5) = 0).  Fixed by counting
  |value| <= margin with opposite signs on both sides.
- BUG-3 (refinement penalty): infeasible-point penalty sign was flipped for
  the barrier refinement (returned -1e6, attracting Nelder-Mead to a=b=0.5);
  R=50 bar_max was wrong (29.54) until fixed (36.85).  Fixed: penalty +1e6
  for both kinds.
- BUG-4 (smoothing test): verify_smoothing_r4 first version smoothed only ONE
  of the two jumps of [1,R,1], so the family converged to the 2-block [1,R]
  config and the derivative matched the WRONG problem.  Fixed to a single-jump
  reference [1,R].
- LESSON: every numeric helper that converts (breaks, values) to a function
  must be tested against exact cases; every "sign change" counter must decide
  the boundary/on-grid policy explicitly.

## R-007 (2026-08-06): R4 smoothing convergence verified numerically
- verify_smoothing_r4.py: single-jump reference [1,R] at 0.3; smoothed
  transition of width delta; finite-difference derivative
  d lambda_k/d eps -> lambda_k (R-1) u_k(0.3)^2 as delta -> 0 (rel errors
  1.2% at delta=0.05 -> 0.8% at 0.005 -> 0.3% at 0.002; residual is block
  resolution and FD step).  Direct integral of (1/delta) H' u_k^2 matches the
  delta-limit formula to 1e-3 at delta=0.02.
- This confirms the R4 approximation argument mechanism (AEH Lemma 2.1
  applied to smoothed families + dominated convergence).

## R-008 (2026-08-06): theorem-level adversarial search (evidence)
- verify_reduction_search.py: barrier max / well min by 2-parameter scan +
  refinement for R in {2,4,10,50}: R=4 bar_max = 32.6139836177 (= contract to
  4e-12) at (0.451485462, 0.548514531) symmetric; well_min = 6.7844823391
  (= contract to 4e-13) at (0.382598256, 0.617401745) symmetric; R=2/R=10
  match draft-run ledger values (31.102264, 34.451278); R=50 bar_max 36.852185
  at (0.484069, 0.515931) symmetric.
- 300 random adversarial configs at R=4 (2-8 blocks, bang-bang and continuous
  values): max D seen 30.825 < 32.614; min D seen 6.8246 > 6.7845; zero
  violations.  Evidence only (finite search).

## R-009 (2026-08-06): O1f bang-bang verified numerically
- verify_bangbang.py: pointwise FH formula dD/dt = int delta-rho f dx holds
  (strips inside blocks, both signs; absdiff 9e-5 on the {f>0} strip, 1.4e-3
  on a wide {f<0} strip with eta=0.1 - first-order formula, sign and magnitude
  correct).  Saturation: at the global maximizer rho = R on {f>0} and rho = 1
  on {f<0}; at the global minimizer rho = 1 on {f>0} and R on {f<0}.  Both
  pass.

## R-010 (2026-08-06): synthesis + self-audit
- Wrote candidate_proof.md (revised O1 proof with R1-R4) and audit_report.md
  (per-obligation verdicts O1a-O1f, adversarial verifier pass).
- Phase 11 novelty scan (web): see status_and_literature.md and the report.
- Final status: CANDIDATE_COMPLETE_PROOF (self-audited; independent
  re-audit still required by the skill's revision policy).

## R-011 (2026-08-06 continuation): Sun 2022 novelty scan (Phase 11 completion)

- zbMATH Open API (an:1506.34110) full record retrieved (HTTP 200), saved as
  research_cache/sun2022_zbmath.json + parsed text.  Review (Erdogan Sen):
  Sun, "On the minimum eigenvalue gap for vibrating string", J. Math. Anal.
  Appl. 516 (2022) No. 1, 126513, treats the MINIMUM eigenvalue gap of the
  first two eigenvalues for rho(x) piecewise continuous with a bounded number
  of jumps, following Qi-Li-Xie, Qual. Theory Dyn. Syst. 19 (2020) No. 1,
  Paper 12 (Zbl 1456.34022).  The review does NOT define the classes S1/S2.
- ScienceDirect abstract snippet (via search index): "The eigenvalue gap
  Gamma(rho) attains its minimum on each of the classes of S1 and S2 by rho0."
  Confirms Sun's result is INF-side only, over two classes S1, S2.
- S1/S2 definition attempts (all recorded): zbMATH review (no definition);
  ScienceDirect page + r.jina.ai proxy (connection failed/closed); Peeref
  works/26609210 (login wall); Semantic Scholar Graph API (429 twice);
  OpenAlex works/doi:10.1016/j.jmaa.2022.126513 (200, no abstract, closed
  access); Crossref (200, no abstract); MaRDI portal Publication:2166449
  (200, empty metadata page); zbMATH pdf/07574902.pdf (403); web search
  (snippet only).  Verdict: S1/S2 exact definitions NOT_VERIFIABLE from public
  metadata.
- Novelty conclusion: O1 SUP side + the reduction theorem over the FULL
  measurable box class: POTENTIALLY_NEW (no source found).  O1 INF side: new
  as stated over the full measurable class; its VALUE may coincide with Sun's
  minimum over the bounded-jump subclass, but the identification with Sun's
  S1/S2 minimizers is NOT_VERIFIABLE.  Honest classification recorded in
  status_and_literature.md (N1-N5).
- AEH published version confirmed: Arch. Math. (Basel) 126 (2026), No. 2,
  187-197, DOI 10.1007/s00013-025-02213-y (search index + EBSCO records).
- Qi-Li-Xie 2020 (research_cache/qi2020.json): density-infimum/Lyapunov
  direction, not a box-class gap extremization; Sun-Yang sub-elliptic 2023
  (research_cache/sun_subelliptic.json): review license-blocked, sub-elliptic
  gap, different setting.

## R-012 (2026-08-06 continuation): self-audit of the revised proof; audit report delivered

- F-001 found and repaired: candidate Lemma 3(b) pre-correction line
  "||S-S||_HS^2 <= (R/16)||rho-sigma||_2^2" is arithmetically wrong.  Correct
  chain: |Delta| <= (sqrt(R)/2)(A_x + A_t) gives ||S-S||_HS^2 <= (R/32)
  (||A||_2^2 + ||A||_1^2) <= (R/32)(2R||A||_1) = (R^2/16)||A||_1, using
  ||A||_2^2 <= (R-1)||A||_1 and ||A||_1 <= R-1.  Final bound
  (R/4)||A||_1^{1/2} unaffected.  Corrected in the delivered candidate_proof.md
  Section 3 (b).
- Re-derived O1a-O1f line by line (Weyl chain, smoothing limit interchanges,
  Wronskian structure, compactness/2-jump reduction, L^1 density, bang-bang
  saturation, synthesis).  Verdicts: all PASS after F-001 (audit_report.md).
- Recorded F-002 (the O1 audit run's "two-sided derivative exists only where
  f(x_j) = 0" is imprecise; the two-sided derivative exists at every jump
  position, the one-sided DISTANCE derivatives flip sign unless f(x_j) = 0),
  F-003 (Lemma 6 hypothesis should read "rho~ in K_2 a global maximizer";
  piecewise-constant hypothesis supplied by the synthesis; no circularity),
  F-004 (draft-run u* digit discrepancy = precision artifact, D*/lambda agree
  to 1e-11), F-005 (R-010 falsely claimed audit_report.md was written; the
  file was lost; delivered in this session; R-010 not retro-edited).
- audit_report.md delivered (~30 KB, ASCII-only), per-obligation verdicts,
  findings log, residual-gap instructions for the independent re-audit.

## R-013 (2026-08-06 continuation): reproducibility spot re-runs

- verify_bangbang.py and verify_smoothing_r4.py re-run fresh from the
  committed state: bit-identical outputs to the recorded *out.json.  The
  heavier battery (verify_hs_bound, verify_fh_sign, verify_structure_f,
  verify_reduction_search) was run earlier in this run (R-004..R-009) with
  outputs preserved.

## R-014 (2026-08-06 continuation): run closure

- Refreshed run-manifest.json: completed_at, upstream_status_verbatim =
  CANDIDATE_COMPLETE_PROOF, artifacts with hashes,
  manager_ingestion_state = COMPLETED.
- Final status: CANDIDATE_COMPLETE_PROOF (self-audited; independent re-audit
  of the changed points Lemma 1 and Lemma 3 remains the closing step before
  the manager closes obligation O1).
- Out of scope, per packet: O2/O3; manage-math-research-program NOT called
  from inside this solver run.

## R-015 (2026-08-06 continuation): failure routes and tooling lessons

- Failure route: Sun 2022 S1/S2 exact class definitions.  All public routes
  failed or were empty: ScienceDirect page + r.jina.ai proxy (connection
  closed/failed), Peeref (login wall), Semantic Scholar Graph API (HTTP 429
  twice), OpenAlex (200, no abstract, closed), Crossref (200, no abstract),
  MaRDI portal (200, empty metadata page), zbMATH PDF (403), web search
  (snippet only).  Outcome: NOT_VERIFIABLE, honestly recorded in
  status_and_literature.md N3.  Lesson: for closed-access articles, an
  unresolved bibliographic detail must be reported as NOT_VERIFIABLE, not
  inferred.
- Tooling failure: apply_patch.bat mangles multi-line patch arguments on
  Windows (%* newline handling), repeatedly returning "Invalid patch: The
  last line of the patch must be '*** End Patch'".  Workaround that works:
  invoke codex.exe --codex-run-as-apply-patch directly from PowerShell with
  the patch as a single argument.  Lesson recorded for future runs.
- Tooling limitation: Remove-Item in shell commands was policy-blocked this
  session; scratch files were left in place and recorded as scratch in
  repro_manifest.md instead of deleted.
- Encoding lesson: Windows PowerShell -Encoding utf8 writes a UTF-8 BOM;
  several artifacts carried BOMs and were stripped at closure (all run
  hashes re-verified after stripping).  For ASCII-only artifacts, verify with
  an explicit BOM/non-ASCII scan before closing.
- Process lesson: ledger R-010 claimed audit_report.md was written while the
  file was lost; this session delivered it and recorded the correction as new
  entries (R-011..R-015) rather than retro-editing R-010.  Rule: before
  claiming an artifact is delivered, verify the file exists and hash it.
