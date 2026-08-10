# Research ledger

Run: R-20260806T070000Z-keylemma2b-0A6D8F
Problem: resume R-20260806T050000Z-keylemma2-5A35E5; independently verify the
four interval certificates, complete the analytic proofs (M2, CORNER, C4,
L4box, L5box), assemble candidate_proof.md + audit_report.md and the standard
artifacts.

All timestamps are wall-clock local (Asia/Shanghai), 2026-08-06.  ASCII
punctuation only.  The predecessor run's ledger (entries 1-6) is the prior state.

## Entry 1 (resume): state inventory and first verification pass

- Read the task packet, the predecessor ledger/contract/obligation graph, the
  parent run candidate/audit, and the origin report (semantic chain T1-T4).
- Read the four certificate JSONs and the three engine files (riarith, rigorous,
  sound_bracket) and the shipped verifier.
- Ran the shipped verifier on the four certificates (fresh capture).  Results:
  dM2dq PASS (-0.19024277945171448312...), C4 FAIL on tiling only (stale region
  constants in the shipped verifier; the leaf re-evaluations passed, worst lower
  bound 2.42176456..., 0 sign failures), L4box PASS (-4.65692440779...),
  L5box PASS (+6.24285527001...).
- Verified at 90-digit precision that the C4 leaves actually cover
  [2pi/7, 2pi/5 - 1e-3]: first leaf starts 2.637e-62 below 2pi/7, last leaf ends
  2.163e-60 above 2pi/5 - 1e-3, and the interior gaps between the 60-digit
  printed leaves total 6.25e-58 (max 1e-59).  This matches the stale-constant
  diagnosis.

## Entry 2: fixed-constants and independent verification (ALL PASS)

- Ran the fixed-constants verifier (C4 region constants corrected to the
  certificate's own leaf endpoints): ALL FOUR CERTIFICATES VERIFIED.
- Ran the independent from-scratch engine (mpmath.iv 50 dps + own rigorous atan
  + own bisection): ALL FOUR CERTIFICATES VERIFIED; worst bounds dM2/dq
  -0.19024, C4 2.49716, L4 -4.84160, L5 +8.37938; 0 sign / 0 overlap / 0 point
  failures; atan sanity PASS.  (~10 min runtime.)

## Entry 3: critical finding - the dM2/dq certificate does NOT cover up to sqrt(41)

- cert_dM2dq_boxes.json declares region u in [0, y1] with
  y1 = 6.403124237432848686488217674621813264520, which is a 40-digit
  truncation of sqrt(41) = 6.403124237432848686488217674621813264520420..., i.e.
  y1 is 4.2e-40 BELOW sqrt(41).  The M2 proof requires dM2/dq < 0 on
  [1,20] x [0, sqrt(41)] (superset of D intersect {q <= 20}); the strip
  [1,20] x [y1, sqrt(41)] was uncovered.
- Numeric scan: dM2/dq in [-1114.7, -514.9] on the strip.
- Wrote cert_dM2dq_strip.py certifying dM2/dq < 0 on [1,20] x [y1, y1 + 1e-30]
  (exact squaring: (y1 + 1e-30)^2 = 41.000...0000128 > 41, so the strip contains
  [y1, sqrt(41)]).  Ran it: PASS, worst upper bound -448.7453035065...
  Wrote cert_dM2dq_strip_boxes.json (10 boxes).

## Entry 4: independent strip verification and fresh semantic audit

- Wrote verify_dM2dq_strip_indep.py (mpmath.iv engine, no riarith dependency):
  PASS, worst upper bound -448.7453035065..., tiling and exact coverage of
  sqrt(41) confirmed.
- Wrote a fresh adversarial semantic audit (audit_semantics_fresh.py, then v2
  audit_semantics_fresh2.py): re-derives alpha_1, alpha_2, G, Mtilde from first
  principles and checks sign(G2) = sign(IN), u = tan(c A), the CORNER closed
  form, the C4 curve identity, region signs (R1, R2, Box), and H / F~' signs on
  the box; 0 failures on random and edge samples.
- BUG FOUND IN MY OWN FIRST AUDIT SCRIPT: alpha2 bisection used hi = 3.14 < pi,
  which missed roots closer than 1e-3 to pi (e.g. q = 70.8, c = 0.0294 has
  alpha2 = pi - 0.00130 > 3.14).  Fixed by solving gamma = pi - alpha2 on
  (0, pi/3) with hi = 1.05 (f strictly increasing).  Lesson: always solve the
  odd equation in the gamma coordinate (as the shipped sound_bracket does), and
  never clamp a bisection bound below pi.

## Entry 5: tail and analytic parts re-verification (ALL PASS)

- Re-ran cert_tail_constants.py: Machin pi at 90 digits; coverage iv(2pi/7).lo
  >= cert_v_lo and iv(2pi/5-1e-3).hi <= cert_v_hi; sliver bridge with eps = 1e-58
  (worst inflated lower bound 2.42176456... > 0); tail constants 1.25 / 3.06 /
  3.08 / 2.50002e-3; exact rational LB(T^3 K) = 349333915896399959797475605401 /
  1953125000000000000000000000 = 178.8589649... > 0.  ALL PASS.
- Re-ran verify_formulas.py (300 points, sections 1-8), verify_analytic_parts.py,
  verify_c4_tail.py (500 points), verify_parent_bases.py, verify_algebra_sym.py,
  verify_corner_sym.py, verify_corner_sym2.py, verify_c4_details.py: ALL PASS.
  The exact T^3 K rational lower bound is 178.8589649... (not 180.62 as an early
  estimate in the predecessor had suggested; the u_min constant 3.07 was
  corrected to 3.06 in verify_analytic_parts.py).

## Entry 6: manual re-derivations (audit of the analytic proofs)

- M2 tail bound B(q): re-derived term by term (4A^2u <= 4 pi^2 sqrt(2q+1);
  8Au^2q/S <= 8 pi (2q+1)/q; -7Aq^2 bounded by 0; -14Aq <= -14 pi q + 14 sqrt(2q+1)
  via A >= pi - sqrt(2q+1)/q; 2u/(1+u^2) <= 1; 4Aq/(1+u^2) <= 4 pi q;
  t(4u^2/S - 5 - 9u^2) <= 2 pi (2q+1)/q^2).  B(20) < -232 < 0 with elementary
  bounds; B'(q) < 0 for q >= 20 ( (4 pi^2+14)/sqrt(41) < 8.39 < 31.4 = 10 pi ).
  VERIFIED.
- M2/q^2 bound for u > sqrt(41): t <= t_max = sqrt(41)/20 < 0.33; 4At - 5 < 0;
  bound <= 4 pi^2 t_max - 7(pi - arctan t_max) + 2 pi (1+t_max^2)/42 < 0
  (numerically -7.018).  VERIFIED.
- h(u) < 0: h'' < 0, h'(1/2) > 0, h'(0.53) < 0 (elementary bounds), max value
  < 13(0.53)^2 - 5 = -1.3483 < 0.  VERIFIED.
- CORNER: q >= 2 iff x <= arccos(2/3); x -> pi - x - 3 sin x strictly decreasing;
  min at q = 2; pi > arccos(2/3) + sqrt(5) via y = pi - sqrt(5) in (0.9, 1) and
  cos(y) <= 1 - y^2/2 + y^4/24 < 0.6223375 < 2/3.  VERIFIED.
- C4 tail: T^3 K = 5vu^3(1+T^2) - 3u^3T(1+T^2) + 2vu^2T(1+T^2) - 1.2u^2(1+u^2)T^2
  >= 5(5/4)(153/50)^3 - 3(77/25)^3 T_max(1+T_max^2) - (6/5)(77/25)^2(1+(77/25)^2)
  T_max^2 = 178.85896 > 0 with T_max = 125001/50000000.  VERIFIED.
- L1 re-derivation: G_1 < 0 reduces to W_1 > 2 c alpha_1 (q^2-1) sin cos /(q+c Phi_1)
  using (q^2-1) sin cos <= Phi_1 cot alpha_1 (equivalent to 0 <= 1); cleanest form:
  numerator = Phi_1 * N with N < -2 alpha_1 cot alpha_1 * q < 0.  VERIFIED.
- iv_dGdc (rigorous.py) checked term by term against the total derivative
  dG/dc = Ga * (-a Phi/D) + Gc; matches the formula re-derived from scratch.
- Monotonicity of alpha_1 (decreasing in c, q) and alpha_2 (decreasing in c,
  increasing in q) re-derived from the implicit equations (O_q sign analysis on
  the branch (pi/2, pi)).  VERIFIED.

## Entry 7: soundness audit of the engines

- riarith: found iv_sqrt is NOT strictly outward-rounded (Decimal.sqrt uses the
  ambient ROUND_HALF_EVEN; lower bound can exceed the true sqrt by ~1e-60,
  verified on sqrt(2) = 1.41421356237309504880168872420969807856967187537694807317668
  vs the true value ...6673799).  Documented in audit_report.md Section 4.
  Consequence: the certificate-generation engine and the shipped re-verification
  engine have this defect; it does not affect the final proof because every sign
  conclusion was re-derived by the sound mpmath.iv engine (which does not use
  iv_sqrt) with 0 failures and large margins.
- mpmath.iv independent engine: atan series remainder R = x^(2n+3)/(2n+3) on
  [0,1] with reduction atan(x) = pi/2 - atan(1/x) for x > 1; monotone endpoint
  evaluation; sign-safe bisection with precision doubling.  Assessed sound.
- sound_bracket: bisection shrinks only on sign-definite evaluations; the
  initial bracket signs f1e(0) = -c pi/2 < 0, f1e(pi/2-) = pi/2 > 0,
  fO(0) = -c pi < 0, fO(gamma_hi) > 0 hold; safe.

## Entry 8: proof write-up and audit report

- Updated candidate_proof.md: integrated the strip certificate (Section 4.4),
  fixed two cosmetic numeric slips (Section 4.2: arctan(1/2) bound value and the
  h'(0.53) numeric), updated Sections 8.3 and 10 (five certificates, new strip
  row).
- Wrote problem_contract.md, repro_manifest.md, status_and_literature.md,
  obligation_graph.md, approach_registry.md, counterexample_log.md.
- Wrote audit_report.md with verdict PASS (modulo documented caveats), Section 4
  documenting the stale C4 constants and the riarith iv_sqrt defect.
- Updated run-manifest.json (upstream_status_verbatim, completed_at, artifacts).

## Honest effort note

The predecessor run (R-20260806T050000Z) and this continuation together span
many hours of effective research.  This continuation session performed the
verification runs (shipped/fixed/independent), found and closed the strip gap,
wrote and ran the fresh semantic audit, re-derived every analytic proof step by
hand, and assembled the artifacts.  No claim is made about wall-clock hours of
the predecessor beyond its ledger; this session's real work is recorded above.
