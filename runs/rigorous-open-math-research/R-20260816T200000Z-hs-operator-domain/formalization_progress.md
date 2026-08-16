# Formalization progress — R-20260816T200000Z-hs-operator-domain

Project Lean repo: `F:\LaTeX\BVE research\lean-proof` (lean 4.31.0 / mathlib v4.31.0).

## New scaffold created (session 2026-08-16)
- File: `lean-proof/SL/HsOperatorDomain_Scaffold.lean`
- Header: `-- SCAFFOLD: hs-operator-domain 2026-08-16 R-20260816T200000Z-hs-operator-domain OPEN`
- Status: RIGOROUS_PARTIAL_RESULT; scaffold only, all proof bodies are `sorry`.
- Declarations (statement-level placeholders matching the run's STRICT theorems):
  - `mo_even_membership` / `mo_odd_membership` (Theorem MO)
  - `legendre_deficit_pos` (Lemma DE/DO)
  - `deficit_strict_increasing` (Lemma DM)
  - `aSeq_pos` (Lemma A-POS)
  - `kreinSobolev_deficit_pos` (Lemma L-KS)
  - `spd_spaces_differ` (Theorem SPD)
  - `nd_not_dense` (Theorem ND)
- `InKreinDomain` / `kreinDeficit` are scaffold-level placeholder definitions.
- The bindings use the existing `HsOrthogonalSystems` (`legendreClosed`, `qnEven`,
  `qnOdd`, `aSeq`) and `KreinDegenerateLimit` (`kS`) names; argument orders follow
  those definitions: `qnEven family c r n`, `qnOdd family c r n`, `aSeq c n`, `kS c n`.

## What is NOT yet formalized (open obligations)
- The analytic positivity core: Legendre endpoint-deficit positivity, deficit
  monotonicity, Krein-Sobolev deficit positivity (paper proof in candidate_proof.md).
- The functional-analytic statements: D(K_c^{s/2}) definition, density, transfer
  isometries, the operator-vs-abstract difference (SPD/ND) — require spectral/
  functional-analysis infrastructure.
- The degree-spectrum lemma (Q1a, "every degree >= 2r+2 present") is EVIDENCE-level
  and recorded open (`Q1a_general_degree_spectrum_open`).

## Supersession
- The upstream `LeftDefDensity_Scaffold.lean` l1doubleprime (s >= 4, sparse family)
  stands; its auxiliary claim "H^s ∩ C[x] = span{1,x}" is REFUTED by this run
  (see counterexample_log.md CE-1). No formal declaration relied on that claim.

## Verify command (once Lean workers available)
- `cd F:\LaTeX\BVE research\lean-proof && lake build SL.HsOperatorDomain_Scaffold`
- Result (2026-08-16): **Build completed successfully (8567 jobs)**, exit 0. Only
  warnings are unused-variable lints on the two placeholder defs and the expected
  `sorry` warnings on the placeholder theorem bodies (this is a scaffold, NOT a
  verified artifact). All proof bodies are `sorry` by design.
- Full `lake build` reaches the same new file (previous full-build failure was only
  a missing namespace qualification for `kS`, fixed to `KreinDegenerateLimit.kS`).
