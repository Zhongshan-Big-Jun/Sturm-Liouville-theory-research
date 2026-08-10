# Research ledger

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)
Chronological log.  Times are wall-clock estimates; the environment clock was
ahead of the nominal run timestamp (harness artifact, recorded honestly).

## 2026-08-06 (handoff from the previous solver session)
- Read the task packet, the target run (candidate_proof, contract, audit_report),
  the parent run (candidate_proof with the reduction and bases), and the origin
  report (definitions of E, O, alpha_k, G, H, Ftilde, the KEY LEMMA).
- Verified symbolic identities with audit_symbolic.py / audit_symbolic2.py:
  E' = O' = -q/Phi, alpha' = -a Phi/(q + c Phi), the G formula, IN = G2*POS,
  M2 = dIN/du, dM2/dq, M2(1,u) = pi h(u), dG/dc transcription, Fpp identity,
  CORNER closed forms, C4 identity IN = A*K(v), C4 tail T^3K, B5, B4 (P(x)
  identity).  Results: 0 diffs except (i) the B4 closed-form transcription and
  (ii) the C4 identity left atan(tan v) unresolved (both resolved later).
- Built the interval engine (audit_iv.py) and the function library
  (audit_functions.py).  Found and fixed two engine bugs: ambient-precision
  products (unsound) and Decimal.sqrt ignoring the rounding mode
  (implemented _sqrt_directed, validated on 3000 random cases).

## 2026-08-06 (this continuation session)
- Rewrote audit_iv.py v3: exact monotone-range sin/cos over intervals (the
  Taylor-over-the-interval version had dependency blow-up: sin over the
  alpha_2 bracket [2.392, 2.4275] came out width 0.2 instead of the true ~0.023,
  making the L4/L5 re-evaluations useless).  Introduced and then fixed a
  factorial bug in _atan_series (it must divide by 2j+1, not (2j+1)!).
- Removed the negative-control sqrt check from the __main__ sanity harness
  (Python 3.10 Decimal.sqrt ignores the rounding mode; the check was testing the
  bug, not the engine).
- audit_iv sanity: point and interval checks pass; PI contains true pi (width
  1.93e-77); sin over [2.392,2.4275] now width 0.0265 (contains the true range).
- Fixed audit_certificates.py: run1d now passes Iv(a,b) to the 1-D reeval; the
  2-D tiling check uses exact Fraction arithmetic (area equality, containment,
  disjointness; no row-alignment assumption - the certificate leaves are not a
  tensor-product partition); added the exact (y1+1e-30)^2 > 41 check; added the
  C4 sliver-bridge check (max gap < 2 eps) and the certified-PI coverage checks.
- Ran audit_certificates.py: ALL FIVE CERTIFICATES INDEPENDENTLY RE-VERIFIED:
  - cert_dM2dq_boxes.json: exact tiling, worst upper -0.1902428, 0 failures.
  - cert_dM2dq_strip_boxes.json: exact tiling, worst upper -448.7453,
    (y1+1e-30)^2 > 41 exactly.
  - cert_c4_boxes.json: worst lower 2.49716 > 0, coverage and sliver bridge OK.
  - cert_L4box_boxes.json: exact tiling of [1,2]x[0.4,0.5], worst upper
    -4.8416038, 0 failures.
  - cert_L5box_boxes.json: exact tiling, worst lower +8.3793828, 0 failures.
- Verified the C4 tail constants with the audit engine: iv(2pi/5-1e-3).lo > 1.25,
  iv_tan(2pi/5-1e-3).lo > 3.06, iv_tan(2pi/5).hi < 3.08, iv_tan(2.5e-3).hi <=
  2.50002e-3; exact rational T^3K lower bound = 349333915896399959797475605401/
  1953125000000000000000000000 = 178.85896 > 0 (matches the target's constant).
- Verified B4/B5 from the primary definitions (first numeric attempt had
  inverted bisection directions in both root finders - fixed; then B4/B5 closed
  forms match direct evaluation to 1e-45; B4 worst (closest to zero) = -2.1e-5
  at q -> 1+; B5 min = 2.4184 at q -> 1+).
- Re-verified the CORNER closed form to 1e-45 and its elementary certificate;
  R1/R2 grids (G2 >= 0 on q >= 2 and on c <= 0.4); the B(q) tail bound holds
  numerically (dM2/dq <= B(q) on the q >= 20 grid, B(20) = -232.72);
  u_c(q) < sqrt(2q+1) at c = 0.4.
- Ran float64 evidence grids: 200k random points: LOG max -2.50 < 0, FP max
  -2.2e-5 < 0, G1 max -2.83 < 0, IN*G2 > 0 everywhere, M2 < 0, dM2/dq < 0;
  Region B dense grid (1,2)x(0.4,0.5): min H = 2.4185 > 0, max Fp = -0.456 < 0.
- Fresh symbolic verification: B4 closed form diff = 0 (with q = cos x/(1 - cos x));
  IN = G2*POS diff = 0; C4 identity IN = A*K(v) holds with atan(tan v) = v.
- Read the origin report in full and confirmed semantic fidelity of the contract
  (Mtilde vs the origin's M differ by the c-independent factor q(q^2-1)).
- Read the target run's verify_certificates_indep.py and confirmed the structural
  agreement of the independent re-verification approach; the target's second
  engine (mpmath.iv) and this audit's engine (Decimal, exact sin/cos ranges) both
  close all five certificates.
- Wrote the standard artifacts (problem_contract, status_and_literature,
  obligation_graph, approach_registry, counterexample_log, research_ledger,
  candidate_proof, audit_report, repro_manifest) and updated run-manifest.json.

## Decisions
- Use exact Fraction arithmetic for tiling (area equality), not Decimal area sums
  with tolerance, to remove rounding artifacts.
- Use certified-PI interval coverage for the C4 region instead of trusting the
  certificate's printed region constants (the shipped verifier used stale ones).
- Treat the interval engines as soundness-documented executables, not as
  formally verified tools; this is recorded as a reproducibility note, not an
  open proof obligation.
