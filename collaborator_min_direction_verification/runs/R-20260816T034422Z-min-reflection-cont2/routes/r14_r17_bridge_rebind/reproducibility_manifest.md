# Reproducibility manifest

- Route: `MIN-REFL-C2-J` / `r14_r17_bridge_rebind`.
- Run: `R-20260816T034422Z-min-reflection-cont2`.
- Frozen snapshot: Blueprint
  `b93b42029f95d55489c71e344af329220c3182ff07c2d0b57b9e170b7d4f7056`,
  inventory
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Exact runtime:
  `E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe`.
- Randomness: none.
- Historical R11/R14/R17 artifacts are comparison targets only; every used
  identity is restated and checked in the new route.
- Hash-bound C2-H physical/gluing replay:

```text
report.md        32a4aea77442b1980e5d76fbc608b0ac73b034004eef816eaa9e790b2fd262b7
exact_checker.py 2e0590c02109a1eca57382ecc5b5f5fa4f62da5a34a6fe7b9dc7dd104b256c9c
```

- Replay command:

```text
E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe runs/R-20260816T034422Z-min-reflection-cont2/routes/r14_r17_bridge_rebind/exact_checker.py
```

- Replay result: `PASS`, Python 3.12.13, SymPy 1.14.0.
- Frozen proof artifacts and SHA-256:

```text
problem_contract.md       d01df9413199392ba8e637380e971dc82799eef5c25cf1500c39d9996866da76
computation_contract.md   e8987fb0852033aefe942cfe7fafe5eb8fd5d217e5a2242a65b9234c8a35d5b1
bridge_proof.md           e0c4b6f857e0f7dcbe6e3389ff1d7e061f7353a21db8e42c5b4708ee5475b06e
exact_checker.py          a6b1eec9af90e167d2f2f59889d1de4222a1f7c9469fcc01175007d94d72b3fb
exact_checker_output.json 29348073ba5a29201e3216db2824f23796aff38828c6ef7310cbebeeac8b11e3
self_audit.md             c73ef55715ea2bce2e4f87e75cca4c0034fbfbe01ff5f5192cf5ab42078269d1
```

- C2-I cover binding: pending until a complete immutable full-cube artifact
  and hash are supplied.  This is the only open premise of the conditional
  bridge.
