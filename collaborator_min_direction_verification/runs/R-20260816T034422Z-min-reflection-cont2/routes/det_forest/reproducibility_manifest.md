# Reproducibility manifest: MIN-REFL-C2-A

## Environment

```text
project_root:
  E:\ai_auto_solve\SL_gap_nge2_blueprint_v22_research_20260809
python:
  E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe
arithmetic:
  SymPy exact integers/rationals and symbolic polynomial algebra
floating_point_used_as_proof:
  false
```

## Replay

From the project root:

```text
E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe \
  runs\R-20260816T034422Z-min-reflection-cont2\routes\det_forest\exact_forest_checker.py
```

Expected terminal lines:

```text
FOREST_IDENTITY_N_1_TO_4=PASS
ALTERNATING_W_IDENTITY_N_1_TO_4=PASS
SCALED_CHARGE_IDENTITY_N_1_TO_4=PASS
REFLECTION_COVARIANCE_N_1_TO_4=PASS
REDUCED_WITNESS_DET=-2
SHARED_CONTRAST_MISMATCH=PASS
```

The finite symbolic dimensions check the implementation; the universal
forest theorem is proved combinatorially in `report.md` and is not inferred
from these checks.

## Provenance

```text
human contribution:
  selected the minimum reflection target and requested continued research
model contribution:
  path-ground decomposition, signed forest theorem, forced-charge scaling,
  obstruction analysis, and restart condition
tool contribution:
  deterministic canonical retrieval and exact SymPy identity checking
```

Final SHA-256 digests are computed after freezing the artifacts and reported
to the parent run coordinator.
