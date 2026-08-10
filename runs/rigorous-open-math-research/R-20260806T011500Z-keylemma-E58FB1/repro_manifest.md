# Repro manifest

Run: R-20260806T011500Z-keylemma-E58FB1
Task: Q-20260806-keylemma-E58FB1 (KEY LEMMA of the n=1 adjacent-gap program, obligation O2)
Date: 2026-08-06 (Asia/Shanghai; run id timestamp 2026-08-06T01:15:00Z)

## Inputs and hashes

| Item | Role | Path | sha256 (first 16 hex) |
|---|---|---|---|
| Task packet | problem statement + context | agenda/task-packets/Q-20260806-keylemma-E58FB1.md | 608d3e7dba9a0126 (full: 608d3e7dba9a012650a7e8a3c9db6c13ae04850ea11d8846d7d300a2d7964b78) |
| Agent A report (authoritative derivation) | KEY LEMMA statement + reduction T1-T4 | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | see run R-20260805T000000Z manifest; file size 428298 bytes |
| Agent A verify script | floating-point evidence | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentA_verify.py | see prior run |
| KEY LEMMA decomposition tool | untrusted context (not a premise) | tools/key-lemma-decomposition.md | 20171ab5 (reported by prior handoff) |
| Research summary | status/gap context | docs/SL_gap_n1_research_summary.pdf | see project index |
| Background literature | rechecked context only | papers/keller1976.pdf/.txt, papers/mw1976.pdf/.txt, papers/aeh2407.02459 (or equivalent) | see project archive |

Note: hashes of the R-20260805 run artifacts were not recomputed in this run (the files were
read-only inputs); the only hash freshly verified here is the task packet full sha256, which
matches the packet content on disk.

## Environment

- OS: Windows (PowerShell host).
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  - mpmath 1.3.0 (keylemma_lib.py core, 30-60 digit computations)
  - numpy 2.2.6, scipy 1.15.3 (float64 exploratory scripts)
  - sympy 1.13.1 (exact symbolic derivations)
- LaTeX: D:\texlive\2024\bin\windows\xelatex.exe (not used for the solver run; proof document
  is produced as Markdown per the solver output protocol).
- Random seeds: none needed (all computations are deterministic; no Monte Carlo).

## Key scripts (reproducibility/)

All under: runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/reproducibility/

| Script | Purpose | Status |
|---|---|---|
| keylemma_lib.py | independent mpmath core (Phi, Wfun, E/O curves, alpha1/alpha2, M, G, bisection) | PASS (used by everything) |
| verify_premises.py | premise audit P1-P10 at 50-60 digits | PASS except one finite-difference tolerance flag (see notes) |
| q1_analysis.py | q=1 closed forms (F~', H, N1) | PASS |
| verify_q1_forms2.py | J1/J2/H' q=1 closed forms vs direct | PASS |
| verify_Fp12.py | closed form F~'(q,1/2) vs numeric | PASS (1e-13) |
| derive_Fp12.py, derive_Fp12b.py | sympy derivation of F~'(1/2) | PASS |
| derive_J.py, derive_J2.py, derive_J_curve.py, Gprime_J.py | sympy derivations of G', J | PASS |
| regionB.py | Region B characterization + margins | PASS (q* bisection print has an inverted update bug; values printed are correct, q* ~ 1.855) |
| regionB2.py, regionB3.py, fast_regionB.py, ratio_route.py | Region B margins cross-checks | PASS |
| qmono_box.py | R4-R6 margins (now superseded by L4box/L5box) | PASS (4.87 / -2.69 / -9.55) |
| G2_largeq.py | R1 margin structure for q >= 2 | PASS |
| G2_cmono.py, G2_decreasing.py, G2_dc_04.py, G2_min_at_half.py, G2_profile.py | G2 structure probes | PASS |
| global_min_Fp.py | global min of -F~' (0.42534 at q~3.12, c~0.5) | PASS |
| check_Fpp.py | second-difference check of Fpp | FAILS as written (second difference unreliable; identity verified by first difference in debug_Fpp.py) |
| debug_Fpp.py | trace of Fpp identity | PASS (dFp/dc = M1J1-M2J2 to 2e-9) |
| debug_N2.py, map_J_boundaries.py, map_J_boundaries2.py, map_structure.py | exploratory | recorded |
| direct_bounds.py, boundary12.py, explore2.py, explore3.py, explore_H.py, Gp_mono.py, profile_Gp.py, qderiv.py, qderiv2.py, qmono.py, tight_spots.py, wide_mono.py | exploratory / route probes | recorded |
| (new in this continuation) global_scan.py, r1r2_margins.py, Bmono.py, G2qmono.py, Bqmono_true.py, G2c_struct.py, corner_envelope.py, sym_R1.py, sym_dG2dq.py, r1_tail.py, asym_corner.py, corner_exact.py, corner_Fp12.py, corner_Fp12b.py, n12_check.py, dG2dq_stress.py, r456_mpmath.py, box_Hp_Fpp.py, box2.py, box_margins2.py, final_margins.py | continuation-run probes and margin tables (ad hoc; kept for provenance) | recorded |

Exact commands used for the main reproducibility runs (from the run root):
  python reproducibility\verify_premises.py   (131 s, 60-digit)
  python reproducibility\q1_analysis.py
  python reproducibility\verify_q1_forms2.py
  python reproducibility\verify_Fp12.py
  python reproducibility\regionB.py
  python reproducibility\qmono_box.py
  python reproducibility\global_min_Fp.py
  python reproducibility\debug_Fpp.py

## Numeric margin tables (evidence, not proofs)

- G2 - G1 >= 2.4184 on (1, inf) x (0, 1/2); min approached at (q -> 1+, c -> 1/2-)
  (exact corner limit = 4*pi/(3*sqrt(3)) = 2.418399...).
- -F~' >= 0.4253 on the bounded sampled range (q <= 100); min 0.425342 at (q ~ 3.120, c ~ 0.4999).  For large q, -F~' shrinks toward 0 (M~ ~ 1/q^3); the inequality F~' < 0 there follows from region A (R1 + L1 + L2), not from the margin.
- R1: G2 >= 0 for q >= 2, c in (0, 1/2); grid min 0.070593 at (2, 0.4999).
- R2: G2 >= 0 for q > 1, c <= 0.4; grid min 0.415004 at (q -> 1+, 0.4).
- L4box: H' <= -7.7317 on (1, 2] x [0.4, 0.5].
- L5box: F~'' >= 14.167 on (1, 2] x [0.4, 0.5].
- Region B (G2 < 0) is contained in (1, 2) x (0.44, 0.5) on the sampled grid; boundary
  values c_G2(1) = 0.44465, c_G2(1.2) = 0.46335, c_G2(1.5) = 0.48345, c_G2(1.8) = 0.49765;
  q* (G2(q,1/2) = 0) ~ 1.855.
- dG2/dq >= 0 on the whole sampled domain (min ~5.0e-4 at (q=100, small c); grid min
  5.0e-12 at (q=1e6, c=0.0125) up to finite-difference noise).
- |G1|/|G2| >= 7.42, M~2/M~1 <= 6.94, |G1|-|G2| >= 2.418 on Region B.

## Verification notes and caveats

1. P9a tolerance flag: at (q=10, c=0.05), the central finite difference of F' differs from
   M1G1-M2G2 by 2.7e-7 on a quantity of magnitude ~1386. This is a finite-difference
   truncation artifact, not a formula failure; the identity F~' = M~1G1 - M~2G2 was verified
   independently to 1e-12 (debug_Fpp.py and P9a at other points).
2. check_Fpp.py's second-difference column is numerically unreliable (root-solving noise in
   Fp evaluations amplifies in (F(c+h)-2F(c)+F(c-h))/h^2). The correct check is the first
   difference dFp/dc = M1J1 - M2J2 (debug_Fpp.py), which passes to 2e-9 at h=1e-6.
3. regionB.py prints "q* = 2.0" from a bisection whose update direction is inverted
   (lo := mid when G2(mid) > 0). The printed G2 values are correct and give the true root
   q* ~ 1.855 (between 1.85 and 1.9). Cosmetic script bug; does not affect other outputs.
4. mpmath.iv (interval arithmetic) was NOT used for certificates. No claim in this run
   relies on interval-arithmetic soundness. Numerical claims are labeled as evidence only.
5. All "new" continuation-run scripts under reproducibility/ are ad hoc probes; the curated
   reproducibility set is the 8 commands listed above plus keylemma_lib.py.

## Unknown fields

- Model identity and internal settings: unknown (not recorded by the harness).
- Exact CPU hours of the full run: not tracked; the continuation executed on 2026-08-06.
- Hashes of the prior-run inputs (agentA report, agentA_verify.py, tools): carried from the
  prior handoff, not recomputed.
