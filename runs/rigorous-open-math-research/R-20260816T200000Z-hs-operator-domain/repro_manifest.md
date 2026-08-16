# Reproducibility manifest — R-20260816T200000Z-hs-operator-domain

## Environment
- OS: Windows (host); Python 3.10 at
  `C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe`, `PYTHONUTF8=1`.
- Libraries: sympy (exact rational arithmetic), numpy (only for one floating-point
  density check in reproducibility/wdensity_check.py, labeled EVIDENCE).
- Skill: rigorous-open-math-research (DSH bundle).

## Inputs (task packet + source artifacts)
- Task packet: agenda/task-packets/Q-20260816-hs-operator-domain-C0D1E2F3.md (DRAFT).
- Source: runs/.../R-20260816T120000Z-leftdef-density/{final_report.md,
  candidate_proof.md, audit_report.md}.
- Source: docs/SL_hs_orthogonal_systems_proof.tex (2026-08-05).
- These are project context, not verified facts; the contract was normalized and
  independently audited.

## Artifacts produced (this run root)
- problem_contract.md, obligation_graph.md, approach_registry.md,
  research_ledger.md, counterexample_log.md, candidate_proof.md (to be followed by
  audit_report.md, status_and_literature.md, formalization_progress.md, final_report.md).
- reproducibility/*.py (exact sympy EVIDENCE; see below).
- evidence/evidence_log.txt (consolidated EVIDENCE output).

## Exact-arithmetic EVIDENCE scripts (all exact unless noted)
| Script | What it checks (exact) |
|---|---|
| boundary_facts.py | K_c^{-1}P_n in D(K_c) only n in {0,1}; Q_n in D(K_c^r) r=1,2,3 only n in {0,1}; monomials in D(K_c), D(K_c^2) |
| domain_poly_span.py | explicit basis of D(K_c^r) ∩ Pi for r=1,2,3 (degree structure) |
| degree_structure.py | degree presence in D(K_c^r) ∩ Pi |
| genericity_check.py | degree structure c-independent (c in {1,3,10}) |
| krein_sobolev_membership.py | K_c^{-1}K_n in D(K_c) only n in {0,1}; even cross-check |
| krein_sobolev_deficit_fixed.py | deficits of K_c^{-1}K_n (authoritative version; the
  earlier krein_sobolev_deficit.py had a P_{-1} handling bug and was removed) |
| validate_krein_sobolev.py | K_n match SL_hs doc closed forms (K_0..K_4, clean build);
  deficits positive |
| odd_proof_data.py | D_m and L(K_n) via a-combination; a_m positive |
| monotonicity_data.py | D_m monotonicity, differences positive |
| wdensity_check.py | (numpy, float) W_r density probe; EVIDENCE only |

Replay: `python run_all_evidence.py` (runs boundary_facts, domain_poly_span,
degree_structure, genericity_check, krein_sobolev_membership, krein_sobolev_deficit_fixed,
odd_proof_data, monotonicity_data; validate_krein_sobolev.py and wdensity_check.py are
separate; wdensity_check.py is numpy float, EVIDENCE only).

## Lean scaffold
- `lean-proof/SL/HsOperatorDomain_Scaffold.lean` — statement placeholders for
  MO/DE/DO/DM/A-POS/L-KS/SPD/ND/Q1a. Build: `cd F:\LaTeX\BVE research\lean-proof;
  lake build SL.HsOperatorDomain_Scaffold` → 8567 jobs, exit 0, all bodies `sorry`
  (scaffold, not verified). Toolchain leanprover/lean4:v4.31.0, mathlib v4.31.0.

## Reproducibility of the STRICT proof
The strict theorems (MO, DE/DO, DM, A-POS, L-KS, SPD, ND) are derived analytically in
candidate_proof.md and do NOT depend on the EVIDENCE scripts. The EVIDENCE scripts are:
- finite exact corroboration (n <= ~12, c in {1,3,10});
- the W_r density numerical probe (float) is EVIDENCE only and is NOT load-bearing
  (SPD does not use it);
- the "every degree >= 2r+2 present" lemma (Q1a/EMB) is EVIDENCE-supported for
  r <= 3 and is explicitly non-load-bearing.

## Unknowns / constraints
- No git commit/push performed (manager syncs at stage close).
- Repo working tree at dispatch: clean except the new untracked run root directory.
- No human numerical claims; all EVIDENCE is exact arithmetic except the explicitly
  labeled float probe.
