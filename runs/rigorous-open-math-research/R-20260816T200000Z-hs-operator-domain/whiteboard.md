# Run whiteboard (Planner memory)

- **Run ID:** `R-20260816T200000Z-hs-operator-domain`
- **Task packet ID:** `Q-20260816-hs-operator-domain-C0D1E2F3`
- **Upstream status (verbatim):** `RIGOROUS_PARTIAL_RESULT`
- **This-run status:** `RIGOROUS_PARTIAL_RESULT`
- **Last updated:** `2026-08-16T23:45:00Z`

## Current plan

Run is closed with `RIGOROUS_PARTIAL_RESULT`.  Load-bearing STRICT theorems MO,
SPD, ND are independently audited (REPAIRABLE_GAP with non-load-bearing gaps,
one repaired).  The auxiliary every-degree lemma Q1a(ii) is EVIDENCE/OPEN.
Lean scaffold `SL/HsOperatorDomain_Scaffold.lean` created (builds, sorry).

## Route history

- `[SUCCEEDED]` Transport-level reduction (Lemma T): membership reduces to level-1 Krein transport condition.
- `[SUCCEEDED]` Legendre deficit positivity (Lemmas DE/DO): K_c^{-1}P_n fails D(K_c) for n>=2.
- `[SUCCEEDED]` Deficit monotonicity (Lemma DM) and Krein-Sobolev positivity (A-POS a_m>0, L-KS).
- `[SUCCEEDED]` Main membership theorem (MO): Q_n^{(s)} in D(K_c^{s/2}) iff n in {0,1}, s>=4.
- `[SUCCEEDED]` Operator-domain vs abstract-completion separation (SPD).
- `[SUCCEEDED]` Non-density of span{Q_n^{(s)}} in H_op^s (ND).
- `[PARTIAL]` Degree-spectrum lemma Q1a(ii) (EVIDENCE for r<=3; general-r open).
- `[SUCCEEDED]` Independent adversarial audit: REPAIRABLE_GAP, non-load-bearing gaps repaired/recorded.

## Ideas to return to

- Close Q1a(ii) with a rigorous triangularity/leading-coefficient induction for all r.
- Reconcile the SL_hs doc's completeness claim with the operator-domain/abstract-completion distinction in a published note.
- Investigate whether a modified operator-domain family (e.g. applying boundary corrections) restores density for s>=4.

## Open obligations

- Q1a(ii): rigorous general-r description of `D(K_c^r) ∩ Pi` (degree spectrum {0,1} ∪ {d ≥ 2r+2}).
- Inherited: O1'LD, O2', O3 (fractional window).

## Key artifacts

- `runs/.../candidate_proof.md` -- STRICT MO/SPD/ND + Lemmas T/DE/DO/DM/A-POS/L-KS, Q1a.
- `runs/.../audit_report.md` -- independent audit REPAIRABLE_GAP + repairs.
- `runs/.../final_report.md` -- run final report.
- `runs/.../problem_contract.md` -- normalized contract.
- `runs/.../reproducibility/*.py` -- exact EVIDENCE scripts.
- `lean-proof/SL/HsOperatorDomain_Scaffold.lean` -- Lean scaffold (builds, sorry).
