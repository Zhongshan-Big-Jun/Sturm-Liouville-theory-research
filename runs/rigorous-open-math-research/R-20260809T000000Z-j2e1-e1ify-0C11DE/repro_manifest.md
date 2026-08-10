# Reproducibility manifest - R-20260809T000000Z-j2e1-e1ify-0C11DE

## Certificate chain (input -> ledger -> tables -> document)
| file | sha256 |
|---|---|
| misc/e1_certgen.py (L10, generator) | 375209e2574aea15e3966b442316e2326070d75d4b9445d4bdb9ccf74dfec57c |
| misc/e1_cert_ledger.json (L11, ledger) | ec9ce5ff7af7d9684bdd2097368e789e6f0b1dae798a04e62aef3d073fd68d30 |
| misc/e1_cert_tables.py (L12, table generator) | 9268b4cce7ab56bf66e5b651a8f36bf8269cf096efcbfdd740ae30676e9b38d3 |
| misc/e1_cert_tables.tex (generated fragment) | a5057c02cab697e154e21acc63526b73a0ae31d15c362888f5b5d044010e5742 |
| misc/rigid1d.py (exact rational interval kernel) | 1dec97d9c59185fa38a94058c5ca94b0573e3ed36c268826b61ce537e1095ddc |
| docs/SL_gap_n1_O3a_phase_rigidity_proof.tex | 2c3312579218f204cfd381146c1eeb57a0af62c376dd1f4c1150c63d96a7ebb0 |
| docs/build/SL_gap_n1_O3a_phase_rigidity_proof.pdf | ecc7ef62393dc3ef5f014613a25d63fd75fdf05adfc3ec1e26f33f9a4ca65f8d |
| misc/_audit_symbolic_a.py (session 45 audit, 21 checks) | 2fef4039e0e601a052a1599198fdc48fe97acb301c75e889a6925a029ca26d83 |
| misc/_audit_symbolic_b.py (session 45 audit, 67 checks) | b7f7b3cb3b8461ade7132d5b2a562ff95b58be8708b4887646b1ca49d28a99a0 |
| misc/_audit_symbolic_c.py (session 45 audit C, 70 checks) | b0f3b644e5fd264c0617cad84febd22955213e03fbc8e074fb142e3560fa5a47 |
| misc/_verify_identity.py (fixed modulo-relations report) | 7bae4b3b40f2c89810dd26e132b35b83eb092a41dcd1a80f8ef44436706db25b |
| misc/audit_o3a_cert_replay.py (independent Decimal replay engine) | 3a8672f4a30525ab8e0bd4fe56a54d07ed10e2bb55ce7fd967631d43c65085a7 |
| misc/audit_o3a_cert_replay.json (replay results, 71/71) | c239092dfc79f938929d6604d011b75cace8537e102dc2c9bfeeb32755c3b1bb |
| audit_report.md (sessions 45/47-49, audits A-E + F-210/F-211 + script fixes) | 0868eacf4b7c0052639de8837ccbb899ba9aa0137a4b7e13ffb51ca423db1ddc |
| scripts/audit_o3a_pdf_part2b.py (completeness audit E3, grid top 3*pi, R list w/o 1e6) | f4f223be3bc13bbe6249320d58b5b35207a5bc56bd2b357101957946aab6fabb |
| scripts/audit_o3a_pdf_part2c.py (completeness audit E3, xi scan to 0.4999995, mpmath xi* as mpf) | 2623ba804ac9c223426922a254a84b584304f7f52ec8ec3d88028d7d90f466ea |
| docs/build/SL_gap_n1_O3a_phase_rigidity_proof.log | c9be856046c73dca6f493e62e338895321c490baa0e7ff2c1f3a39ec8c614b1b |

## Reproduce
1. `py -X utf8 misc\e1_certgen.py` -> must print 57/57 PASS and regenerate
   misc/e1_cert_ledger.json (needs `sys.set_int_max_str_digits(1000000)`; ~266 s).
2. `py -X utf8 misc\e1_cert_tables.py` -> regenerates misc/e1_cert_tables.tex.
3. Splice fragment into the tex between the marker line and `\section{符号速查}`
   (already done in this session; the tex embeds the fragment inline).
4. `cd docs; xelatex -interaction=nonstopmode -output-directory=build
   SL_gap_n1_O3a_phase_rigidity_proof.tex` twice -> zero warnings/errors, 40 pages.

## Verification results
- e1_certgen: 57 facts certified, 57 PASS (54 main + 3 h-concavity reductions).
- Ledger meta: GLO=131/200, GHI=1309/1250, m=791/2500; method: alternating-series
  envelopes (sin/cos/arctan, Machin pi) + exact Fraction interval arithmetic +
  2nd-order Taylor model.
- E3 spot checks (cross-check only, NOT proof): tightest margins ~2.6e-5
  (h(0.655) >= m), ~6.3e-5 (Qlo(1.0014) <= -1/10000), ~2.2e-4
  (TA_B2(0.86) >= 47/25); interval lower bounds TA_B2 >= 27/10 on [0.723,0.724]
  margin ~2.4e-3, TC >= 19/10 on [0.82,0.83] margin ~0.06; all monotonicity
  Taylor-model margins strictly positive (min ~3.9e-2).

## Historical (retired, no longer supports any conclusion)
- L5 old (LOG) 128-leaf certificate script: 132e998f...
- L6 J1 E1 cross-check script: 64e24ace...
- L7-L9 old decimal interval validator trio (rigid_dec.py, zz_verify_e1_dec.py,
  e1_facts_ledger.json): dd81278e..., cad6c5ef..., cc74fc50...
- Old 16/67/200 leaf-box families: retired with thm:j1e1 / thm:j2e1 / lem:corner.

## Session 45 audit (2026-08-09)
- Full independent symbolic audit: 21 + 67 checks PASS (see audit_report.md).
- Fixed tex line 344 sign typo and line 1437 sin(17/10) >= cos(13/100).
- Fixed misc/_verify_identity.py (raw identity False is expected; modulo-relations
  identity True, matching the doc's claim).
- e1_certgen replay: 57/57 PASS, 241.6 s, L10/L11/L12 hashes unchanged.
- Independent J2 = 2 A^2 cg W / Delta^4 verification modulo circle relations
  (Groebner reduction -> 0; numeric cross-check 1e-49 at 50 digits).

- Audit C (misc/_audit_symbolic_c.py): 70/70 PASS, groups I-V (lem:B1 tail, lem:boundary
  rational bounds, lem:M2 (a)(d)(e) incl. the dM2/dq <= B(q) chain and B(20) envelope,
  lem:corner/C4 full elementary proof, lem:inclusion endpoint bounds and gamma_* chain).
- F-206 (tex line 1106): d_q F1 corrected to tan x/(1+q^2 tan^2 x) (spurious q factor removed).
- F-207 (tex lines 672-679): Leibniz partial-sum labels corrected (values are S_5 and S_6,
  not S_6 and S_7); numerical chain unchanged.
- xelatex twice: 38 pages, zero warnings/errors.

## Audit D (2026-08-09, continuation): appendix certificate-method prose
- F-208: sin alternating-series sandwich direction corrected in lem:envseries
  (S_{2m} >= sin x >= S_{2m+1}; cos direction was already correct).
- F-209: arctan term-count/remainder and envelope-width claims corrected
  (22-term direct series only for v <= 1, remainder <= v^45/45; worst
  tab:envprims certified width is tau(131/200) ~ 1.8e-10 = 2 v^45/45 with
  v ~ 0.651; all other primitives <= 10^-23; min margin 2.6e-5).
- No certificate data changed: e1_certgen.py / e1_cert_ledger.json hashes
  unchanged (375209e2... / ec9ce5ff...); regenerated fragment differs only
  in the caption line.
- Recompiled: 39 pages, zero warnings/errors.


## Audit E (2026-08-10): independent third-party replay + dual-subagent audit
- Independent replay engine misc/audit_o3a_cert_replay.py (decimal.Decimal 80 digits,
  directed rounding, alternating-series sin/cos/atan + Machin pi) re-certified
  71/71 rows: 57/57 ledger facts + 11/11 tab:envprims primitive rows + 3 structural
  checks; margins agree with the ledger to <= 2.7e-11 (min certified margin 2.56e-5).
- Dual-subagent adversarial audit (Curie lines 1-559, Linnaeus lines 559-2396):
  Curie found the single gap F-210 (phase-branch selection, eq:phaseeq); Linnaeus
  PASS on the rest with two harmless remarks. See audit_report.md.
- F-210 fixed: new lemma lem:phasebranch proves alpha1 in (0,pi/2), alpha2 in (0,pi),
  E(alpha1) = c alpha1, O(alpha2) = c alpha2 via the Prufer phase and explicit
  mid-region solutions (pure E1).
- F-211 fixed: thm:j1e1 step (iv) monotonicity of f extended to [pi/3, 1122/1000]
  with exact rational envelopes at x0 = 1122/1000 (lem:envseries):
  sin x0 in (9009/10000, 9010/10000), cos x0 in (4338/10000, 4340/10000);
  3 + 3x cot x - x^2 csc^2 x >= 765791/250000 > 0 on [5pi/14, 1122/1000].
- xelatex twice: 40 pages, zero warnings/errors. New hashes in the table above
  (tex 2c331257..., pdf ecc7ef62..., log c9be8560...). Certificate data unchanged
  (e1_certgen/ledger/rigid1d hashes identical).

## Session 49 (2026-08-10): completeness-audit script fixes (E3)
- Re-ran all 8 completeness-audit scripts (E3 cross-checks; no E1 premise).
- part2b fix: eigvals grid upper bound 2*pi - 1e-7 -> 3*pi (the second zero near
  2*pi was truncated at R=1.1); R list now [1.1,1.5,2.0,4.0,10.0,100.0,1000.0]
  (1e6 is handled by the high-precision scripts part2c/_audit_cstar/_tmp_verify_r1e6).
  PASS: single sign change per R.
- part2c fix: xi scan extended to 0.4999995; mpmath refinement keeps xi* as mpf
  throughout (float64 only brackets xi0 via 30 bisection steps inside a 1e-9 window).
  PASS: R=1000 xi*=0.49626089548007825 R1=-5.44e-44; R=1e6 xi*=0.499880117059947152
  R1=-2.76e-46.
- All 8 scripts PASS (part1, part2, part2b, part2c, part3, part4, _audit_cstar,
  _tmp_verify_r1e6). Certificate data unchanged; the document was recompiled
  (40 pages, zero warnings) after the sec:certs audit-script list was completed
  with part2b plus a one-line note on the 2026-08-10 re-run (new tex/pdf/log
  hashes in the table above).