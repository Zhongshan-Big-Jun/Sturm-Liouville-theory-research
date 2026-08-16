# MIN-REFL-C route ledger

Append-only record for `R-20260815T181317Z-min-reflection`.

## 2026-08-16T02:30:00+08:00

- Bound the route to context `CTX-DEFAULT`, Blueprint
  `sha256:76346e2fa9f880fd8c1c02bf4b001b38cb66f2f4688c8497c9d764ebb746c7a7`,
  and inventory
  `sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Deterministic retrieval confirmed `CLM-NGE2-MPO3A-FULL-RELAY` and
  `CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11` are trusted, while the
  general minimum uniqueness inference remains open.
- Inspected the accepted full relay evaluator, R7 physical validator, R8
  adaptive search, fixed-`mu` common-terminal scans, and the exact general
  `mu`, `n=2` interface reductions.
- Frozen `computation_contract.md` before new numerical search.  The route
  remains `active`; no prior null scan is treated as proof.

## 2026-08-16T02:43:30+08:00

- The smoke run found that a coarse sign bracket can cross an event-count
  transition while containing a strict physical root in the adjacent
  chamber.  Frozen `computation_contract_addendum_v2.md` before the full
  run; all cross-count refinements remain subject to every root-level gate.
- Corrected the implementation gate to match the frozen contract: numerical
  derivative-step stability is a conditioning diagnostic, not one of the
  premise-validity predicates requested for a witness.  Trajectory,
  transversality, energy, law, index, and independent evaluator gates remain
  mandatory.  Conditioning failures now trigger 100-digit replay.

## 2026-08-16T02:56:34+08:00

- Completed the frozen v2 full run: 1,584 complete-root starts at 33
  contrasts, 160 direct singular starts, 127 fixed-frequency problems, and
  64 held-out `n=3,4` problems.
- Found zero premise-complete asymmetric candidates and zero singular-root
  candidates.  The closest singular optimizer output had residual score
  `4.6374417243092407e-4`, outside the candidate gates.
- Replayed 12 high-contrast conditioning records at 100 decimal digits.  Four
  apparent binary multiple-root cases each collapsed to one root; the
  high-precision `h(h(q))-q` and switch-mirror defects were below `8e-69`
  and `2.4e-65`, respectively.
- Held-out search retained 11 common-terminal roots and no pair or asymmetry.
- `audit_results.py` returned `PASS`.  Route status is
  `NUMERICAL_EVIDENCE`; the null search is not promoted to a proof.  Stopped
  after the registered conditioning replay and held-out layer as directed.
