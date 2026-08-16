CANDIDATE_COMPLETE_PROOF

# R15 reproducibility manifest

## Canonical inputs

```text
statistics/blueprint.json
sha256:0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799

statistics/evidence_inventory.csv
sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

## Inspected candidate source

```text
routes/r13_min_n3_composition_r1/derivation.md
bytes:10202
sha256:cd4f1a387c4729e0902c64843560e5643ac03b49565b21128cf8618022965e11

routes/r13_min_n3_composition_r1/amplitude_contraction_mu2.py
bytes:6257
sha256:cb2418d63eb49d4dc68ca977e1dcf14befa8ebe342a5f3d008c1ed346c3d60e4

routes/r13_min_n3_composition_r1/independent_amplitude_audit.py
bytes:4870
sha256:b987d4c2b9302bf2bf00e53667a63f0b86541ba0780d192181a01c60fc6fdafd
```

The candidate source is not imported as a trusted theorem.  R15 repeats the
algebra needed for its result.

## Arithmetic and replay contract

- exact symbolic arithmetic only; no tolerance and no random seed;
- Python standard library plus SymPy, resolved by `uv run --with sympy`;
- checked object: rational-function identities and deterministic integer
  index/orientation tables;
- finite enumeration range: `2<=n<=12`, used only to attack indexing errors;
- proof bridge: the arbitrary-index derivation in `derivation.md`, not the
  finite enumeration;
- replay command from the project root:

```text
uv run --with sympy python runs/R-20260812T165103Z-mpo3a-cont4/routes/
  r15_min_mu2_general_n_nonexistence/general_n_exact_check.py
```

No external literature, network source, numerical solver, or floating-point
search is used.

