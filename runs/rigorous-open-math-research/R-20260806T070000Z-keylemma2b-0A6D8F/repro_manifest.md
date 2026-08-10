# Reproducibility manifest

Run: R-20260806T070000Z-keylemma2b-0A6D8F
Task: Q-20260806-keylemma2b-0A6D8F (resume of R-20260806T050000Z-keylemma2-5A35E5)

## Purpose

Record every input, version, tool, restriction, and unknown field used in this
run, so that every claim in candidate_proof.md and audit_report.md is replayable.

## Inputs

- Task packet: agenda/task-packets/Q-20260806-keylemma2b-0A6D8F.md (project
  context only; NOT a verified theorem contract).
- Interrupted predecessor run (authoritative state):
  - runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/
    problem_contract.md, research_ledger.md, obligation_graph.md,
    run-manifest.json.
  - reproducibility/: riarith.py, rigorous.py, sound_bracket.py,
    verify_certificates.py, and the four certificate JSONs:
    cert_dM2dq_boxes.json (84 leaves), cert_c4_boxes.json (200 leaves),
    cert_L4box_boxes.json (128 leaves), cert_L5box_boxes.json (128 leaves).
- Parent run: runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/
  candidate_proof.md, audit_report.md, problem_contract.md (reduction and bases
  L1, L2, B4, B5, B7).
- Origin run: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentA_O2_single_crossing.md (definitions, T1-T4, KEY LEMMA, secular equations).
- Tool library leads (context only, not premises): tools/key-lemma-decomposition.md,
  tools/interval-ad-certificate.md.

## Environment

- OS: Windows, PowerShell shell.
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (Python 3.10).  Bare `python` is not reliable on this machine.
- Libraries: mpmath 1.3.0, numpy 2.2.6, sympy 1.13.1 (sympy used for symbolic
  checks in verify_algebra_sym.py, verify_corner_sym.py, verify_corner_sym2.py).
- Decimal interval engine: riarith.py (outward-rounded Decimal arithmetic,
  ROUND_FLOOR / ROUND_CEILING, Taylor series with explicit remainders, Machin pi).
- Independent interval engine: mpmath.iv (libmp outward-rounded interval
  arithmetic) at 50 dps with an own rigorous atan (alternating Taylor series with
  explicit remainder plus reduction for x > 1) and own sign-safe bisection.
- No formal proof assistant (Lean/Coq/Isabelle/HOL) was used.

## Certificate verification runs (this run, fresh captures)

Shipped verifier (predecessor verify_certificates.py, region constants as
declared):
- cert_dM2dq_boxes.json: PASS (worst upper bound -0.19024277945171448312...).
- cert_c4_boxes.json: FAIL on tiling only (leaf 199 outside region) because the
  shipped verifier's declared region constants were STALE (x0 = 2pi/7 rounded up
  at 20 digits, x1 = 2pi/5 - 1e-3 - 4.44e-5); the leaf re-evaluations themselves
  passed (worst lower bound 2.42176456..., 0 sign failures).
- cert_L4box_boxes.json: PASS (worst upper bound -4.656924407794...).
- cert_L5box_boxes.json: PASS (worst lower bound 6.242855270012...).
Capture: reproducibility/cert_reeval_output/verify_certificates_shipped_rerun.txt

Fixed-constants verifier (corrected C4 region constants = certificate's own
leaf endpoints):
- ALL FOUR CERTIFICATES PASS.  Capture:
  reproducibility/cert_reeval_output/verify_certificates_fixed_constants_rerun.txt

Independent from-scratch engine (verify_certificates_indep.py):
- ALL FOUR CERTIFICATES PASS: dM2/dq worst -0.19024..., C4 worst 2.49716...,
  L4 worst -4.84160..., L5 worst 8.37938..., 0 sign/overlap/point failures.
  Capture: reproducibility/cert_reeval_output/verify_certificates_indep_rerun.txt

New strip certificate (closes the dM2/dq region gap, see audit_report.md Sec 4):
- cert_dM2dq_strip.py: PASS (worst upper bound -448.745..., exact squaring shows
  (y1 + 1e-30)^2 > 41).  Boxes written to cert_dM2dq_strip_boxes.json.
- Independent re-verification verify_dM2dq_strip_indep.py (mpmath.iv): PASS
  (worst upper bound -448.745..., 0 sign failures).
  Captures: reproducibility/cert_reeval_output/cert_dM2dq_strip.txt,
  reproducibility/cert_reeval_output/verify_dM2dq_strip_indep.txt

Analytic-part verification scripts (all re-run fresh in this run, all PASS):
- verify_formulas.py (300 points; sections 1-8: sign identity, c=1/2 corner,
  M2/dM2dq formulas vs central FD, M2(1,u) = pi h(u), B(q) tail, CORNER, C4).
- verify_analytic_parts.py (dM2/dq <= B(q) worst gap 394.095; M2/q^2 direct
  bound -7.018; T^3 K lower bound 178.8589649; CORNER closed forms).
- verify_c4_tail.py (C4 tail identity and constants, 500 points, 0 bad).
- verify_parent_bases.py (L1, B4, B5, B7 grid checks, 0 violations).
- verify_algebra_sym.py (symbolic: IN = G2*POS, M2, dM2/dq, M2(1,u); the C4
  curve identity leaves atan(tan(...)) terms unresolved symbolically - the C4
  identity is verified numerically and by the certified re-evaluations, NOT by
  symbolic reduction).
- verify_corner_sym.py, verify_corner_sym2.py (symbolic CORNER closed forms,
  diff = 0).
- verify_c4_details.py (coverage: cert covers [2pi/7, 2pi/5-1e-3]).
- cert_tail_constants.py (Machin pi at 90 digits; coverage iv(2pi/7).lo >=
  cert_v_lo, iv(2pi/5-1e-3).hi <= cert_v_hi; sliver bridge with eps = 1e-58,
  worst inflated lower bound 2.42176456...; tail constants 1.25, 3.06, 3.08,
  2.50002e-3; exact rational LB(T^3 K) = 349333915896399959797475605401 /
  1953125000000000000000000000 = 178.85896 > 0).
- audit_semantics_fresh.py / audit_semantics_fresh2.py (fresh adversarial
  semantic audit, written from scratch in this run; the v1 of the fresh audit
  had an alpha2 bisection bound bug (hi = 3.14 < pi) which produced two false
  failures; v2 solves gamma = pi - alpha2 on (0, pi/3) and passes all checks).
All captures in reproducibility/cert_reeval_output/ (*.txt).

## Scripts in this run's reproducibility/

- cert_tail_constants.py, cert_dM2dq_strip.py, verify_dM2dq_strip_indep.py,
  verify_analytic_parts.py, verify_c4_details.py, verify_c4_tail.py,
  verify_certificates_fixed_constants.py, verify_certificates_indep.py,
  verify_corner_sym.py, verify_corner_sym2.py, verify_formulas.py,
  verify_parent_bases.py, verify_algebra_sym.py, audit_semantics_fresh.py,
  audit_semantics_fresh2.py.
- cert_reeval_output/: fresh capture of every run (shipped/fixed/independent/
  strip/tail/analytic/formula/parent-bases/symbolic).

## Exact commands (replay)

python reproducibility\cert_dM2dq_strip.py          (writes strip boxes + checks)
python reproducibility\verify_certificates_indep.py (independent engine, ~10 min)
python reproducibility\cert_tail_constants.py       (tail + coverage + slivers)
python reproducibility\verify_formulas.py           (formula checks)
python reproducibility\verify_analytic_parts.py     (analytic parts)
python reproducibility\verify_c4_tail.py            (C4 tail)
python reproducibility\verify_parent_bases.py       (bases L1, B4, B5, B7)
python reproducibility\verify_algebra_sym.py        (symbolic identities)
python reproducibility\verify_corner_sym.py         (CORNER symbolic)
python reproducibility\verify_corner_sym2.py        (CORNER symbolic 2)
python reproducibility\verify_c4_details.py         (C4 coverage details)
python reproducibility\verify_certificates_fixed_constants.py  (shipped engine, ~6 min)
python reproducibility\verify_dM2dq_strip_indep.py  (strip independent)
The predecessor's shipped verifier is run from the predecessor directory:
python <R-20260806T050000Z-keylemma2-5A35E5>\reproducibility\verify_certificates.py

## Known caveats

- riarith.iv_sqrt is NOT strictly outward-rounded (Decimal.sqrt uses nearest
  rounding; the lower bound can exceed the true value by ~1e-60; documented in
  audit_report.md Section 4).  This affects the certificate-GENERATION engine and
  the SHIPPED re-verification engine only.  Every sign conclusion is independently
  re-derived by the sound mpmath.iv engine, so the defect is not load-bearing for
  the final proof.
- The C4 curve identity IN = A*K(v) was NOT reduced to 0 symbolically by sympy
  (leftover atan(tan(...)) terms).  It is verified numerically on 300+ points, on
  the certificate re-evaluations, and in the fresh audit (audit_semantics_fresh2).
- Wall-clock research effort in this run: the run was resumed from an interrupted
  predecessor; the total effective effort across both runs is several hours.  The
  time spent in this continuation session is recorded in research_ledger.md.
- Model/unknown fields: the model identifier is not recorded (unknown).

## Hashes / identifiers

- Run IDs: R-20260806T050000Z-keylemma2-5A35E5 (predecessor),
  R-20260806T070000Z-keylemma2b-0A6D8F (this run).
- Task ID: Q-20260806-keylemma2b-0A6D8F.  Portfolio problem: O-2026-SL-GAP-3B7A2C.
- No external DOIs or arXiv ids are used as premises (project-derived statement).
