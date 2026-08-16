# Reproducibility manifest: MIN-REFL-C2-G

## Binding

```text
context: CTX-DEFAULT
blueprint:
  sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
target:
  OBL-NGE2-MPO3A-MIN-DET-H-POSITIVE-R35
  semantic-sha256:3f22913f6cf51e3d6615a1f6469744d142608c70fb6bd73422d725fedaf175fd
formalization_status: not_requested
```

## Frozen inputs

```text
runs/R-20260816T034422Z-min-reflection-cont2/problem_contract.md
runs/R-20260816T034422Z-min-reflection-cont2/routes/det_forest/report.md
  sha256:858ca18b12bda01334dad53f163e0d4fe1cfd61dc790aedff634582ad7b4e1b2
runs/R-20260816T034422Z-min-reflection-cont2/routes/det_forest/exact_forest_checker.py
  sha256:5cbe9aabbcbe53447c20f7109f44f52d78a9095cf84f185cbb862c8f22aaa614
```

## Replay

From the project root:

```text
E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe \
  runs\R-20260816T034422Z-min-reflection-cont2\routes\charge_compensation\exact_checker.py
```

Arithmetic: exact SymPy rational-function algebra.  The checker verifies
both raw momentum residuals, shared-contrast product/quadratic equivalence,
the `Xi` factorization, forced-charge/four-margin identity, block-deficit
sum, central loaded-Robin determinant, and reflected parity factorization.

No random seed, tolerance, interval enclosure, or numerical search is used
in the frozen output.  The exact certificate proves identities and the sign
criterion under the strict analytic phase/branch inequalities; it does not
prove the remaining sign of `Xi`, `D_mid`, or `det(H)`.

Tool versions and final content hashes are recorded in
`exact_checker.json` and the route handoff.

## Frozen output hashes

```text
report.md
  sha256:227c78997d9052653901f7635a899900f1db3c0beca6ea5b9e02d55ff223d03c
exact_checker.py
  sha256:6a2881a167716ac17ff2c2571c4917081e1c094292ccd37d1148f232ca9b22fc
exact_checker.json
  sha256:20d66e78588be406f2b447bb38298b41121e90d076b4cc7a3285caf2f773a9d0
route_registry.md
  sha256:768a12f1783bca78879e34aa428b898733fd456f470da62baf448d189b014bb2
research_ledger.md
  sha256:7747b4aaf92562854d1ab2b2eabca6e2f16bd73f5773e1a001e195c1ac3c79ec
```
