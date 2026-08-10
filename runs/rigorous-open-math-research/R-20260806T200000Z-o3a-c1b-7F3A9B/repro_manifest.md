# Reproduction manifest (run R-20260806T200000Z-o3a-c1b-7F3A9B)

## Task
Conjecture C1 / obligation O3a: unique zero of h = g1 - g2 in the common range
I = [a0, beta] for every R > 1 (barrier family, Dirichlet string on [0,1]).
Requested: a NEW mechanism closing C1, or a decisive rigorous sub-lemma, or an
exact counterexample.

## Environment
- OS: Windows (PowerShell); timezone Asia/Shanghai; date 2026-08-06.
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (Python 3.10).  Packages: numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1.
- LaTeX (not used for proof artifacts unless the manager compiles):
  D:\texlive\2024\bin\windows\xelatex.exe.
- Network: enabled; search tool available (literature checks only).
- Encoding: all artifact files ASCII punctuation (UTF-8); Python scripts ASCII.

## Inputs (exact source versions)
- agenda/task-packets/Q-20260806-o3a-c1b-7F3A9B.md (2026-08-06, DRAFT).
- runs/rigorous-open-math-research/R-20260806T140000Z-o3ac1-42F931/
  problem_contract.md, candidate_proof.md, audit_report.md, approach_registry.md,
  research_ledger.md, status_and_literature.md, counterexample_log.md,
  repro_manifest.md, reproducibility/c1_lib.py (+ json data).
- runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/
  candidate_proof.md, counterexample_log.md (CE-1..CE-3), reproducibility/
  (cert_ce1.py, clean_lib.py, agentB_lib.py, ...).
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentB_O3a_fixed_point.md (T1-T4).
- papers/fundamental_gap.txt = AEH arXiv:2407.02459v2 (O1c source, Lemma 2.2).
- tools/reflection-branch-reduction.md, tools/fh-hessian-branch-reduction.md,
  tools/interval-ad-certificate.md, tools/balanced-phase.md (leads only; each
  re-verified against the run artifacts it cites).

## Hashes of key inputs
Computed at run start (sha256), see reproducibility/hash_inputs.txt.

## Restrictions and constraints
- Do NOT call manage-math-research-program from inside this run.
- Computation is evidence only unless certified.
- ASCII punctuation in all files; Chinese final report.
- At least 8 hours of effective research effort before concluding; every failed
  route and lesson recorded in the research ledger.
- Do NOT modify files outside RUN_ROOT except optionally adding evidence scripts
  under scripts/.

## Unknowns
- Wall-clock duration of prior runs is not independently verifiable; only artifact
  contents are used.
- Whether C1 admits an elementary proof is unknown (target of the run).
