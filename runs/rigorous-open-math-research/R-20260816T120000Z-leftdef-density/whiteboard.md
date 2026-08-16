# Run whiteboard (Planner memory)

- **Run ID:** `R-20260816T120000Z-leftdef-density`
- **Task packet ID:** `Q-20260816-leftdef-density-E5F6A7B8`
- **Upstream status (verbatim):** `RIGOROUS_PARTIAL_RESULT`
- **This-run status:** `RIGOROUS_PARTIAL_RESULT`
- **Last updated:** `2026-08-16T18:30:00Z`

## Current plan

Run closed with `RIGOROUS_PARTIAL_RESULT`.  STRICT structural theorems are scoped
to `s ∈ {1,2,3}` (L1' whole-space sparse density; L2; L4; L3 transfer descent; L5
counterexample), plus a decisive negative finding for `s >= 4` (L1''/S1d: under
the operator-domain reading `H^s = D(K_c^{s/2})`, the sparse family `{p_n}` is
NOT a subset of `H^s`, `H^s ∩ C[x] = span{1,x}`, so whole-space density via the
sparse family FAILS for s >= 4, correcting the packet's Q3 premise).  The reduced
open core is `O1'LD`.  Audit trail: REPAIRABLE_GAP (original L1) -> FATAL (first
s>=4 repair) -> corrected scoping + exact re-derivation.

## Route history

- `[SUCCEEDED]` Whole-space recovery (V=H^s): L1' for s in {1,2,3}; L1'' negative for s>=4.
- `[SUCCEEDED]` Structural projection density: L2 for s in {1,2,3}.
- `[SUCCEEDED]` Transfer descent: L3 core; remark corrected (r=1 only).
- `[SUCCEEDED]` Proper V characterization: L4 for s in {1,2,3}.
- `[SUCCEEDED]` Concrete non-density instance: L5 (V=ker Δ in H^2).
- `[PARTIAL]` O1' status: L6 decided for V=H^s (L1'/L1'') and L5; open for general proper V (O1'LD).
- `[SUCCEEDED]` Decisive structural finding: S1d/L1'' (sparse family not in H^s for s>=4; p_4 notin H^4, exact).
- `[SUCCEEDED]` Audits: REPAIRABLE_GAP then FATAL on first repair; final correction exact-re-derived.

## Ideas to return to

- Fresh verification of the FINAL corrected artifact (L1'/L1'', S1d, L6) before
  canonical promotion.
- Reconcile operator-domain vs abstract-completion reading of `H^s` for `s >= 4`;
  membership of `{Q_n^{(s)}}` in `D(K_c^{s/2})` is open.
- Attack `O1'LD` via H^1/L^2 moment-matrix structure.
- Investigate whether the parity/boundary obstruction mechanism (L5) extends to
  other natural functionals.

## Open obligations

- `O1'LD`: decide whether a free jump-base moment sequence is realized by a
  nonzero element of the descended constraint `K_c^r V` in `H^{s'}` (`s' ∈ {0,1}`).
- NEW: membership of the SL_hs system `{Q_n^{(s)}}` (s >= 4) in `D(K_c^{s/2})`;
  operator-domain vs abstract-completion reading of H^s.
- `O2'` (inherited): constraints guaranteeing density for all c.
- `O3` (inherited): fractional window `3/2 ≤ s < 2`.

## Key artifacts

- `runs/.../candidate_proof.md` -- L1'/L1''/L2/L3/L4/L5/L6 + S1a-S1d (corrected).
- `runs/.../audit_report.md` -- audit trail (REPAIRABLE_GAP -> FATAL -> corrected).
- `runs/.../final_report.md` -- run final report (corrected scope).
- `runs/.../problem_contract.md` -- normalized contract (corrected).
- `runs/.../repro_manifest.md` -- input/env/hash manifest.
- `runs/.../reproducibility/ld_struct_facts.py` -- EVIDENCE incl. S1d.
- `runs/.../reproducibility/ld_counterexample.py` -- EVIDENCE L5 counterexample.
