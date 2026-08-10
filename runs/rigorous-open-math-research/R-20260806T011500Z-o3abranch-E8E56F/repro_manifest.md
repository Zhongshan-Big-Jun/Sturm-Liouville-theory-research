# Repro manifest: run R-20260806T011500Z-o3abranch-E8E56F

## Task packet
- agenda/task-packets/Q-20260806-o3a-branch-E8E56F.md (sha256 computed at ingestion
  by manager: 7b1aeb2c61513a8ab1841b1a116914a23505c99930a6b4c1b29f62e17343c35b)

## Authoritative source (prior run)
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md
- same dir: agentB_lib.py (solver library), agentB_goodbranch*.py, agentB_crossing.py,
  agentB_fixedpoints.json, agentB_fptable.json, agentB_goodbranches.json,
  obligation_graph.md, problem_contract.md, research_ledger.md, approach_registry.md,
  agentA_O2_single_crossing.md, agentC_O3b_boundary.md

## Primary literature (local copies, rechecked in this run)
- papers/fundamental_gap.txt = AEH arXiv:2407.02459v2 (OCR text); Lemma 2.1 (FH),
  Lemma 2.2 (Wronskian / single-interval {f>0})
- papers/keller1976.txt, papers/mw1976.txt (context: ratio extremals, not used as
  premises for the branch lemmas)

## Environment
- OS: Windows, PowerShell; timezone Asia/Shanghai; date 2026-08-06
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (numpy 2.2.6, scipy 1.15.3)
- Run root: runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/

## Scripts created in this run (reproducibility/)
- agentB_lib.py (copy of prior-run solver; sha256 in index at ingestion)
- vec_lib.py (vectorized secular/residual solver over b-grids; good-root
  classification via v-sign)
- clean_lib.py (exact formulas verified vs ODE integration: sec, y_at, norm_n,
  R1_R2, roots2)
- closed_deriv.py (closed-form branch derivatives g1', g2' via implicit system;
  verified vs FD to 1e-8)
- explore_branches.py, branch_scan.py, probe.py, local_branch.py, r_scan.py,
  hprime_scan.py, hprime_detail.py, endpoints*.py, diag_probe.py (numerical
  exploration scripts)

## Key numerical outputs (evidence only)
- fp(R), common ranges, h at endpoints, min h': see research_ledger.md and
  reproducibility JSON files (branch_*.json, r_scan.json)
- All numbers recomputed in this run with the listed scripts; no seed-based
  randomness used (deterministic grids).

## Unknown fields
- model identity of this run: unknown (not recorded by the harness)
- The prior run's internal timings/agent traces: not independently verifiable;
  only files listed above were used as inputs.

## Artifacts delivered (2026-08-06)
- problem_contract.md (with Section 14 revision: Lemma A falsified)
- status_and_literature.md, obligation_graph.md, approach_registry.md,
  research_ledger.md, counterexample_log.md, candidate_proof.md,
  audit_report.md
- reproducibility/: audit_fh_t3.py, audit2.py, audit3_hessian.py,
  largeR_scan.py, largeR_scan2.py, fp_largeR.py, minhp_largeR.py,
  verify_hp.py, h_trace.py, h_trace2.py, crosscheck_hp.py, h_tail3.py,
  h_tail4.py, h_tail5.py, threshold.py, closed_check.py, ode_check.py,
  hb0_fine.py, hb0_fine2.py, hb0_cfg.py, misc_checks.py, h_recovery.py
- reproducibility JSON: largeR_scan.json, largeR_scan2.json, fp_largeR.json,
  minhp_largeR.json, h_b0.json, hb0_fine.json, hb0_fine2.json, h_tail3.json,
  h_tail4.json
- cert_ce1.py + cert_ce1_output.txt (RIGOROUS interval-arithmetic certificate
  for CE-1: h'(a*) < 0 at R = 1500 and R = 1e4, a* = 0.57364)
- amax1_scan.py, amax1_scan2.py (Gamma_1 extends beyond b0 for R in
  {1e3, 1e4, 1e5}; beta = b0)
- dbg_r2profile.py, dbg_r2profile2.py (multi-sheet R2 structure at R = 1500)
- dbg_trace_branches.py (main-sheet continuation from (a0,a0) and (b0,b0))
- dbg_ad_vs_fd.py, dbg_norm_ad.py, dbg_sec_partials.py, dbg_ad_mini.py,
  dbg_ad_terms.py, dbg_iv_r1.py, dbg_roots2robust.py, dbg_r1fine.py
  (AD-vs-FD debugging; recorded in research_ledger R-122)
