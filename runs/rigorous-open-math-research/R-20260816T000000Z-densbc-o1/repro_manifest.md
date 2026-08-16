# Reproducibility Manifest

Run root: runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/
Task: Q-20260816-densbc-o1-A1B2C3D4

## Inputs

- Task packet: agenda/task-packets/Q-20260816-densbc-o1-A1B2C3D4.md
- Upstream run: runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/
  - candidate_proof.md (Theorems A-H, Theorem E, open core O1-O3)
  - audit_report.md (coordinator audit; F-densbc-01 correction)
  - problem_contract.md, status_and_literature.md, research_ledger.md,
    obligation_graph.md, whiteboard.md, run-manifest.json
- Project tools: tools/denseness-criteria.md, tools/constrained-denseness-runs.md

## Source hashes (upstream, from upstream run-manifest.json)

- (upstream bundle hashes recorded there; this run did NOT modify upstream files)

## Upstream result status (VERBATIM, to be returned)

RIGOROUS_PARTIAL_RESULT

## Git state (project root: F:\LaTeX\BVE research)

- HEAD: c0ba1d9e5022d2e028d7c3204b81e1aba1ae74fa (recorded via WSL bash)
- Working tree: HIGHLY DIRTY (pre-existing modified/untracked files across the
  repo, including state/current.json and many docs/scripts/tools).  This run
  created files ONLY under its own run root; it did NOT commit and did NOT push
  (per user instruction).  Upstream run root files were left untouched.
- Note: skill Phase 12 nominally says "commit before stopping"; the USER
  instruction "Do NOT git commit or push" takes precedence.  Uncommitted state
  is recorded here as required by the skill's reproducibility rules.

## Environment

- OS: Windows (WSL2 Ubuntu available for git; Git Bash not installed).
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (PYTHONUTF8=1).  numpy 2.2.6, scipy 1.15.3, sympy 1.13.1.
- No Lean/formalization performed (out of scope for this run).

## Reproducibility scripts (reproducibility/)

- o1_projection_density.py  — H=L^2([-1,1]), V={f: <e^x,f>=0, <1,f>=0}:
  kept set N (empty), projection-density rank check (EVIDENCE).
  Run: python o1_projection_density.py
- o1_poly_rep_example.py — H=L^2([-1,1]), V={f: <x - 1/2 x^2, f>=0} (polynomial
  representer): kept set N (empty for this single constraint), run structure
  (all isolated).  Run: python o1_poly_rep_example.py

## Labels

- All numerical/symbolic computation is EVIDENCE only; strict claims live in
  candidate_proof.md and are labeled STRICT.
