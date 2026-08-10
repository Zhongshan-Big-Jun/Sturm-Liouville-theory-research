# Reproduction manifest (run R-20260806T140000Z-o3ac1-42F931)

## Task
Prove Conjecture C1 (unique zero of h = g1 - g2; O3a) for the n=1 adjacent-gap
extremal theorem, barrier family rho_(a,b) = R on (a,b), 1 elsewhere,
0 < a < b < 1, R > 1, Dirichlet on [0,1].

## Environment
- OS: Windows (PowerShell); timezone Asia/Shanghai; date 2026-08-06.
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (Python 3.10).  Packages: numpy 2.2.6, scipy 1.15.3, mpmath (present;
  interval arithmetic mpmath.iv with iv.prec adjustable).
- LaTeX (not used for proof artifacts unless the manager compiles):
  D:\texlive\2024\bin\windows\xelatex.exe.
- Network: enabled; search tool available (used only for literature checks).

## Inputs (exact source versions)
- agenda/task-packets/Q-20260806-o3a-c1-42F931.md (2026-08-06, DRAFT).
- runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/
  candidate_proof.md (P1-P4, C1), counterexample_log.md (CE-1, CE-2),
  audit_report.md (gaps G2-G4), research_ledger.md, approach_registry.md,
  status_and_literature.md, problem_contract.md, obligation_graph.md,
  reproducibility/{clean_lib.py, agentB_lib.py, cert_ce1.py, closed_deriv.py}.
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentB_O3a_fixed_point.md (T1-T4, Lemma A/B/C), agentB_lib.py.
- tools/fh-hessian-branch-reduction.md, tools/interval-ad-certificate.md,
  tools/residual-exactness.md (tool-library leads; NOT treated as premises,
  re-verified from the run artifacts they cite).
- papers/fundamental_gap.txt (AEH arXiv:2407.02459v2) for O1c (Wronskian).

## Hashes of key inputs (sha256, computed 2026-08-06)
(computed in reproducibility/hash_inputs.py; see hash_inputs.txt)

## Restrictions and constraints
- Do NOT call manage-math-research-program from inside this run.
- Computation is evidence only unless certified.
- ASCII punctuation in all files; Chinese final report.
- Work for a long time before concluding; record all failures in the ledger.

## Unknowns
- Exact upstream provenance of some prior-run numbers (wall-clock time
  claimed "8+ hours" in older sessions) is not independently verifiable;
  only the artifact contents are used.
- Whether C1 is provable by elementary means is unknown (target of the run).
