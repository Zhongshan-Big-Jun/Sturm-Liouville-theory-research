# Task packet Q-20260816-leftdef-density-E5F6A7B8 (左定空间稠密性一般判据)

- **Task ID:** Q-20260816-leftdef-density-E5F6A7B8
- **Project ID:** MRP-20260731-BVE-SL
- **Created:** 2026-08-16
- **Task type:** solve
- **Portfolio problem ID:** O-2026-SL-DENS-BC-A1B2C3
- **Task state:** DRAFT
- **Mode:** PROGRAM_AND_DELEGATE
- **Upstream run (context):** `R-20260814T070000Z-densbc-3F8A2C`, `R-20260816T000000Z-densbc-o1`
- **Run root (new):** `runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/`

## Project reason for this task

The project has proved polynomial completeness in the full left-definite spaces
`H^s[-1,1]` for all integer `s >= 1`, and has developed a general abstract
criterion for density in constrained subspaces (DensBC O1: projection-density,
obstruction moment system, run/first-obstruction, reduced core `O1'`).  This
task specializes and advances that general criterion to **left-definite spaces**
with structural/boundary constraints, with the goal of closing `O1'` in this
concrete Hilbert-space class or obtaining a complete necessary-and-sufficient
criterion.

## Authoritative source wording / source locations

- DensBC O1 candidate proof: `runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`
  (Theorems 1-5, Lemma 6.1, Heuristic 6.2, reduced core O1').
- DensBC O1 audit: `.../audit_report.md`.
- Original DensBC run: `runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md`
  (Theorems A-H, Theorem E, F-densbc-01).
- Left-definite completeness proofs: `docs/SL_h2_completeness_proof.tex`,
  `docs/SL_h3_completeness_proof.tex`, `docs/SL_hs_orthogonal_systems_proof.tex`,
  `docs/SL_denseness_criteria.tex`.
- Summary open problem: `docs/SL_spectral_topics_summary.tex` section 5 item 4.

## Problem statement

Let `H` be a left-definite Hilbert space associated with a Sturm-Liouville /
Krein-type operator (e.g. `H^s[-1,1]` with the Krein inner product, `s >= 1`),
and let `V` be a closed subspace defined by boundary/structural constraints
(FORM (a): intersection of kernels of bounded linear functionals, or a
structural subspace such as the elements satisfying a boundary condition).

For the sparse polynomial family `{p_n}` (or the monomial family adapted to
`V`), give a complete necessary-and-sufficient criterion for
`closure(span Q_sp) = V`, expressed in terms of the left-definite inner product,
the constraint functionals, and the moment/run data.  In particular:

1. Determine when the DensBC O1 reduced core `O1'` (realizability/membership of
   a free run-base moment sequence) is decidable by finite data in the
   left-definite class.
2. Give the concrete first-obstruction degree / free-base characterization for
   the Krein spaces `H^s[-1,1]` with structural boundary constraints.
3. Recover the known full-space completeness results (`H^s` complete for all
   integer `s >= 1`) as the unconstrained case `V = H`.

## Known ambiguities / risks

- The left-definite inner product is not diagonal in the monomial basis for
  general `s`; the moment matrix `<x^i, x^k>_H` is nontrivial.
- Boundary constraints may be structural (elements of `H^s` automatically
  satisfy certain conditions) rather than finite-rank coordinate constraints;
  the criterion must distinguish these.
- `O1'` may remain open even in the left-definite class; an honest reduction
  is an acceptable partial result.

## User constraints / tools

- Strictness labels enforced; numerical evidence never closes an obligation.
- Python `C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe`,
  `PYTHONUTF8=1`; numpy/scipy/sympy; Lean 4 available if formalization is requested.
- Do NOT git commit or push; manager performs git sync at stage close.

## Source bundle

| Item | Version | Path | sha256 |
|---|---|---|---|
| DensBC O1 candidate proof | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md | D87BBDA0E455EE3DFC6B682AA41E1625A5BBDBBAA89D198E8CAE4692202B62EA |
| DensBC O1 audit report | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/audit_report.md | C3243608D52B6181B47691894F818FF704DB0CB4BC3BA9CD9209387E7A1C3DCB |
| DensBC O1 problem contract | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/problem_contract.md | AE43B8B9E7ACC6701FEC400670106FAF356202D5A3DA4679E2364EE8761CC6FB |
| DensBC original candidate | 2026-08-14 | runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md | C2B78E77B8F70BD1F3D67253FB813730F01D296023782F3C2FAF0865AD669B31 |
| Left-definite criteria doc | 2026-08-05 | docs/SL_denseness_criteria.tex | E869849444092C148955BE4B3530F7E9A6C27472650CDAE7DC2E29DF910E8671 |
| H^2 completeness | 2026-08-04 | docs/SL_h2_completeness_proof.tex | 419E721FF43919ED6E5C6D14547C6ABF8C52EAC54578D5946A8624E868361FBF |
| H^3 completeness | 2026-08-05 | docs/SL_h3_completeness_proof.tex | 41E3A8F4289DFA8415A1126348755536C212B3CE4DCDF13617890ED306FB23F0 |

## Novelty preflight (B0)

- **Openness verdict:** As of 2026-08-16, no published exact criterion for
  polynomial density in constrained subspaces of left-definite/Krein spaces is
  known to the project's audits; the full-space H^s completeness is proved
  in-project, and the general constrained criterion is open (DensBC O1').
- **Novelty audit path:** project KB (`tools/`, `docs/`), upstream DensBC O1
  run artifacts, then web sweep for "left-definite space polynomial density
  boundary constraints Krein orthogonal polynomials criterion" before claiming
  novelty.
- **Snapshot hash:** N/A - project `knowledge/` is pre-v2.2; bound to git head
  at dispatch.

## Required run location

runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/

## Upstream invocation

Use $rigorous-open-math-research on the concrete problem in this task packet.
Treat this packet as project context, not as a verified theorem contract.
Independently normalize and audit the exact statement. Write all standard
artifacts under RUN_ROOT. Return the upstream result status verbatim. Do not
git commit or push.

## Manager ingestion checklist

- [ ] Preserve upstream status verbatim.
- [ ] Index the run root and artifact paths/hashes.
- [ ] Do not copy or replace upstream standard artifacts.
- [ ] Update portfolio, maps, tools, budget, checkpoint, resume.
- [ ] Promote reusable knowledge only from exact source/audited artifact locations.
