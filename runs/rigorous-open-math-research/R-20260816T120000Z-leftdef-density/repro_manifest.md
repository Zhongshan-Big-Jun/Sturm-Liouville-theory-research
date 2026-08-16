# Repro Manifest — R-20260816T120000Z-leftdef-density

Run root: runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/

## Inputs

- Task packet: agenda/task-packets/Q-20260816-leftdef-density-E5F6A7B8.md
  (treated as project context; NOT a verified theorem contract).
- Upstream DensBC O1: runs/.../R-20260816T000000Z-densbc-o1/{problem_contract,
  candidate_proof, audit_report}.md
- Upstream DensBC original: runs/.../R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md
- Left-definite docs: docs/SL_h2_completeness_proof.tex, SL_h3_completeness_proof.tex,
  SL_hs_orthogonal_systems_proof.tex, SL_denseness_criteria.tex,
  SL_spectral_topics_summary.tex.

## Environment / tools

- OS: Windows; Python:
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe,
  PYTHONUTF8=1.
- Libraries used (EVIDENCE only): sympy (exact rational), numpy/scipy not used
  for STRICT claims.  No Lean formalization was requested/completed this run.
- Git: NOT committed/pushed per user instruction (manager syncs at stage close).
  Repo state at start: clean working tree.  Git head at dispatch: 6b54849.

## Commands (EVIDENCE scripts)

Run from the run root:
  PYTHONUTF8=1 python reproducibility/ld_struct_facts.py
  PYTHONUTF8=1 python reproducibility/ld_counterexample.py

Both use sympy exact (Fraction-like) arithmetic; c kept symbolic (positive) where
possible; boundary/integral checks are exact rational/expressions, not floating point.

## Restrictions

- No git commit or push.
- No call to manage-math-research-program from inside this solver run.
- Numerical/exact checks are EVIDENCE only; they never close a proof obligation.
- Web search: 4 queries run 2026-08-16 (see status_and_literature.md); all target
  hits abstract/title-level; none fetched-and-verified as settling the target.

## Unknown fields

- Exact commit hash of `knowledge/` snapshot at dispatch: server note says N/A
  (project knowledge/ pre-v2.2); bound to git head 6b54849 at dispatch.
- Whether any external source settles the target: UNKNOWN (not surfaced by sweep;
  recorded as POTENTIALLY_NEW, not claimed open as a fact).

## Outputs (this run)

- problem_contract.md, status_and_literature.md, obligation_graph.md,
  approach_registry.md, research_ledger.md, counterexample_log.md,
  candidate_proof.md, audit_report.md, final_report.md,
  reproducibility/{ld_struct_facts.py, ld_counterexample.py, run-manifest.json}.
