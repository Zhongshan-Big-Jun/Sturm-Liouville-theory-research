# Formalization progress (scaffold register)

This file tracks Lean scaffolds for partial/structural results.  Scaffolds are
**not** formally verified; they record declarations, open obligations, and the
intended statements.

## 2026-08-16

### DensBC O1 (run R-20260816T000000Z-densbc-o1)

- Verified cores:
  - `SL/ProjectionDensity.lean` -- Theorem 1 (projection density), machine-checked.
  - `SL/DensBCEmpty.lean` -- Lemma 6.1 (empty kept set => density fails), machine-checked.
- Scaffold:
  - `SL/DensBC_O1_Scaffold.lean` -- placeholders for Theorems 2-5 and open core O1'.
- Open: `O1'` (moment representability + membership).

### Left-definite density (run R-20260816T120000Z-leftdef-density)

- Scaffold:
  - `SL/LeftDefDensity_Scaffold.lean` -- placeholders for L1', L1'', L2, L3, L4, L5 and open core O1'LD.
- Open: `O1'LD`; additionally the membership of `{Q_n^{(s)}}` in `D(K_c^{s/2})` for `s >= 4`.

## Rule

Scaffold files contain `-- SCAFFOLD` headers and `sorry`; they are never
reported as `FORMALLY_VERIFIED`.  They must be replaced by real proofs or
superseded before a completion label is used.

### Min-direction audit (run R-20260816T174722Z-min-direction-audit)

- Scaffold: `SL/MinDirectionAudit_Scaffold.lean` -- placeholder for accepted claims.
- Status: audit accepted with caveats; no full formalization yet.

### H^s operator-domain vs completion (run R-20260816T200000Z-hs-operator-domain)

- Scaffold: `SL/HsOperatorDomain_Scaffold.lean` -- placeholders for MO/SPD/ND, deficit lemmas.
- Status: RIGOROUS_PARTIAL_RESULT; load-bearing STRICT theorems MO/SPD/ND, Q1a(ii) open.

## 2026-08-22

### A6 root-1 rational no-go (plugin performance experiment)

- Scaffold: `SL/A6Root1RationalNoGo_Scaffold.lean` -- root-1 higher-degree
  rational product exclusion (both parities, all c>0), after independent audit
  REPAIRABLE_GAP + repair.
- Status: RIGOROUS_PARTIAL_RESULT; root-0/minimal branch remains open.
- Sources: `runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md`,
  audit `runs/plugin-perf-eval/R-20260822T000000Z-a6-audit/audit_report.md`.
