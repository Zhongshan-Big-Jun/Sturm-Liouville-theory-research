# Reproducibility manifest

- Run: R-20260823T000000Z-o1p-baseline
- Date: 2026-08-23
- Repo HEAD at start: `e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f`
- Working tree: dirty at start; no commit created during run.
- Variant: BASELINE (no additional reuse protocol).
- Python: 3.14.4; numpy 2.5.2; sympy 1.14.0.
- Scripts:
  - `reproducibility/banded_shift_verify.py` (round 1 symbolic/numeric check)
  - `reproducibility/audit_banded_shift.py` (consistency/regression checks)
- Commands:
  - `python3 reproducibility/banded_shift_verify.py`
  - `python3 reproducibility/audit_banded_shift.py`
- Lean scaffold:
  - `lean-scaffold/DensBCO1p3BandShift.lean`
  - copied to `lean-proof/SL/DensBCO1p3BandShift.lean`
  - compile attempt timed out after 120s on Mathlib warm-up; not verified.
- External search: 3 web queries (degraded, no exact source).
- No seeds needed (scripts deterministic).
