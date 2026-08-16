# Task packet Q-20260816-hs-operator-domain-C0D1E2F3 (H^s operator-domain vs completion; SL_hs system membership)

- **Task ID:** Q-20260816-hs-operator-domain-C0D1E2F3
- **Project ID:** MRP-20260731-BVE-SL
- **Created:** 2026-08-16
- **Task type:** solve
- **Portfolio problem ID:** O-2026-SL-DENS-BC-A1B2C3
- **Task state:** DRAFT
- **Mode:** PROGRAM_AND_DELEGATE
- **Upstream run (context):** `R-20260816T120000Z-leftdef-density`
- **Run root (new):** `runs/rigorous-open-math-research/R-20260816T200000Z-hs-operator-domain/`

## Project reason for this task

The left-definite density run exposed a decisive new open point: for `s >= 4`,
under the operator-domain reading `H^s = D(K_c^{s/2})`, the sparse family
`{p_n}` is not a subset of `H^s` (e.g. `p_4 ∉ H^4`), and the SL_hs orthogonal
system `{Q_n^{(s)}}` may or may not lie in `D(K_c^{s/2})`.  This task resolves
the relationship between the operator-domain and abstract-completion readings
of `H^s` and determines the membership of `{Q_n^{(s)}}` in `D(K_c^{s/2})` for
`s >= 4`.  This is a prerequisite for a complete left-definite density
criterion beyond `s = 3`.

## Authoritative source wording / source locations

- Left-definite run final report: `runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/final_report.md`
- Candidate proof: `.../candidate_proof.md` (S1a-S1d, L1'', L6)
- Audit report: `.../audit_report.md`
- SL_hs orthogonal systems doc: `docs/SL_hs_orthogonal_systems_proof.tex`
- Left-definite theory: `docs/SL_h2_completeness_proof.tex`, `docs/SL_h3_completeness_proof.tex`

## Problem statement

Let `K_c = -d^2/dx^2 + c` on `[-1,1]` with the Krein boundary condition
`f'(±1) = (f(1)-f(-1))/2`.  For integer `s >= 4`:

1. Give a precise description of `H^s = D(K_c^{s/2})` as an operator domain:
   which polynomials belong to it?  In particular, determine whether the
   SL_hs orthogonal polynomials `{Q_n^{(s)}}` (defined via `K_c^{-r}` on `L^2`
   or `H^1`) belong to `D(K_c^{s/2})`.
2. Compare the operator-domain completion `D(K_c^{s/2})` with the abstract
   completion obtained from the left-definite inner product on polynomials.
   Are they equal?  If not, give the precise difference.
3. Consequence: state whether `span{Q_n^{(s)}}` is dense in `D(K_c^{s/2})`
   under the operator-domain reading, and whether the left-definite density
   criterion can be extended to `s >= 4`.

## Known ambiguities / risks

- The distinction between the operator domain `D(K_c^{s/2})` and the abstract
  completion is subtle; boundary conditions at intermediate powers may differ.
- The SL_hs system `{Q_n^{(s)}}` is defined via the isometries
  `K_c^{-r} : L^2 -> H^{2r}` and `K_c^{-r} : H^1 -> H^{2r+1}`; their images may
  not equal `D(K_c^{s/2})` for all `s`.
- This is a project-internal technical question; no separate literature surface
  is expected, but a novelty sweep is still required.

## User constraints / tools

- Strictness labels enforced; numerical evidence never closes an obligation.
- Python `C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe`,
  `PYTHONUTF8=1`; numpy/scipy/sympy; Lean 4 available for scaffold/formalization.
- Do NOT git commit or push; manager performs git sync at stage close.

## Source bundle

| Item | Version | Path | sha256 |
|---|---|---|---|
| Leftdef final report | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/final_report.md | E737FFD8A04DE945D59641AB16885B63708D428AD1E70527B80BD777C2C4ECF5 |
| Leftdef candidate proof | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/candidate_proof.md | 159090ADDC564B5C8DC2546E4144FB4EC7FBF462D40229125C940C86FF635CBE |
| Leftdef audit report | 2026-08-16 | runs/rigorous-open-math-research/R-20260816T120000Z-leftdef-density/audit_report.md | E1EBB2E02AAB17BE5CB4A4B4B8D44B739EDA1A9945BAF37A2A1E0B1495246466 |
| SL_hs systems doc | 2026-08-05 | docs/SL_hs_orthogonal_systems_proof.tex | A1C05A0D862F7F8BF4290E4D29C4C20178F21E0CF5131501A053CC4CEFFA6181 |

## Novelty preflight (B0)

- **Openness verdict:** The operator-domain vs abstract-completion issue for
  Krein left-definite spaces `H^s`, `s >= 4`, and membership of `{Q_n^{(s)}}`
  in `D(K_c^{s/2})` is flagged open by the project's own left-definite run; no
  external source is known to settle it (2026-08-16 sweep).
- **Novelty audit path:** project KB (`tools/`, `docs/`), leftdef run
  artifacts, then web sweep for "left-definite operator domain completion
  Krein boundary conditions powers" before claiming novelty.
- **Snapshot hash:** N/A - project `knowledge/` is pre-v2.2; bound to git head
  at dispatch.

## Required run location

runs/rigorous-open-math-research/R-20260816T200000Z-hs-operator-domain/

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
