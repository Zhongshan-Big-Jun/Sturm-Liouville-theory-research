# Reproducibility manifest

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)

## Environment

- OS: Windows (PowerShell shell)
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
- Python version: 3.10
- Libraries used: mpmath 1.3.0, sympy 1.13.1, numpy 2.2.6 (float64 evidence grids)
- xelatex: D:\texlive\2024\bin\windows\xelatex.exe (not used in this run)
- Skill: rigorous-open-math-research (v2026-08-05 changelog)
- Model: not recorded (unknown field; no model-specific behavior is load-bearing)

## Inputs (SHA-256)

| File | SHA-256 |
|---|---|
| agenda/task-packets/Q-20260806-keylemma-audit-2F83B1.md | 5B2AC421FA4E5AF61743E3EF2C19E14AA28751141B08C0CA378486B0A3AF13C2 |
| runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/candidate_proof.md | DFA78BB54FCF72F46C6E47CDCF02CAB5B68C2E4219952F89340BA9E747C871DF |
| runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/audit_report.md | 6091FA3248C9BD99E93D51037967D49EED7DEF9EFD2ACB277AC98DA3928E1F9F |
| runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/problem_contract.md | 17643B7E6DB57D7CDE621040C421DF29FA82DB2127D492A7D11CB7BFB95E4E4A |
| runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/repro_manifest.md | DA1BF243731D74C600FA902766B4ACAE09C59E7EF60383159424971B6F299DCA |
| runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/cert_dM2dq_boxes.json | 10CCDA56FCD15349E4013737E62787E9FEA706E43C08A9ED515F98A42DFE7808 |
| runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/cert_c4_boxes.json | AAA767EA9B0450BEA3434E52E5F22E616F38C4F2B6C8F449D009AC2A56B64054 |
| runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/cert_L4box_boxes.json | 2081B5761FD5A4AA033BB211E1781456FBF52526D983EBE76A50B3A343345D2B |
| runs/.../R-20260806T050000Z-keylemma2-5A35E5/reproducibility/cert_L5box_boxes.json | 5E2C3BB0F1893D1366E3686C1B8FBE584F52598EA2CD4FFDF77093CB9F92C8C6 |
| runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/cert_dM2dq_strip_boxes.json | 4141DB89E288B08F12DE6E288D4E7DE5507EA1C32A38E07227A348DB396B1A64 |
| runs/.../R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md | 07C72D4BB111251E022E209A61703E8E965BFEDB2B1D669AA373EABC8F22DA56 |
| runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | DC88D7A750A3ACEF37FE5A0ED97DCAD19CFF9554EAC95FFB4024EA1B14DCFC14 |

(paths abbreviated as runs/...; full paths are under
F:\LaTeX\BVE research\runs\rigorous-open-math-research\)

## Audit code (this run, all under reproducibility/)

- audit_iv.py -- Decimal interval engine v3 (directed rounding at PREC = 80;
  Machin pi; own atan with explicit remainder; directed sqrt with 1-ulp outward
  inflation; exact monotone-range sin/cos).  Self-test: point and interval checks
  against mpmath at 120 digits; PI containment.
- audit_functions.py -- interval evaluations of Phi, W, Mtilde, G, dGdc, J,
  Hp, Fpp, dM2dq, K, IN, M2; sound two-phase bracketing of the secular roots;
  monotone alpha_1/alpha_2 bracketing over boxes.
- audit_symbolic.py, audit_symbolic2.py -- sympy verification of the identities.
- audit_certificates.py -- exact Fraction tiling, interval sign conditions,
  stored-enclosure overlap, 80-digit point cross-checks, certified-PI coverage,
  sliver-bridge check for all five certificates.
- dbg_iv.py, dbg_iv2.py -- engine debugging and the 3000-case sqrt validation.

## Commands

  python reproducibility/audit_iv.py            -> output/audit_iv_sanity_v3c.txt
  python reproducibility/audit_functions.py     -> output/audit_functions_sanity_v3.txt
  python reproducibility/audit_symbolic.py      -> output/audit_symbolic.txt
  python reproducibility/audit_symbolic2.py     -> output/audit_symbolic2.txt
  python reproducibility/audit_certificates.py  -> output/audit_certificates_v3.txt
  (plus inline scripts for the fresh B4/C4/POS symbolic checks, the C4 tail
  constants, the B4/B5 numeric checks, and the float64 evidence grids; each is
  recorded in research_ledger.md)

## Key outputs

- output/audit_certificates_v3.txt: ALL FIVE CERTIFICATES INDEPENDENTLY
  RE-VERIFIED.  Exact tiling; sign conditions hold; worst bounds: dM2dq main
  -0.1902428, strip -448.7453, C4 +2.49716, L4 -4.8416038, L5 +8.3793828;
  (y1+1e-30)^2 > 41 exact; C4 coverage and sliver bridge OK; 0 failures each.
- output/audit_symbolic.txt / audit_symbolic2.txt: all identity diffs = 0
  (the two documented exceptions were resolved in the fresh checks).
- output/audit_iv_sanity_v3c.txt: ALL SANITY OK; PI contains true pi (width
  1.93e-77).

## Expected runtime

audit_certificates.py: about 4 minutes (L4/L5 dominate); audit_iv.py: about 35 s
at PREC = 80 with the 20k-point sanity sampling.  Float64 evidence grids: a few
minutes (200k random + 8M Region B points).

## Unknown fields

- Model identity (not recorded by the harness).
- task_packet_sha256 in the run manifest (computed here for the packet file).
- Exact wall-clock history of the earlier solver session (honestly marked as
  handoff context in research_ledger.md).

## Restrictions

- No manage-math-research-program calls were made from inside this solver run.
- The audited candidate proof and certificates were not modified.
