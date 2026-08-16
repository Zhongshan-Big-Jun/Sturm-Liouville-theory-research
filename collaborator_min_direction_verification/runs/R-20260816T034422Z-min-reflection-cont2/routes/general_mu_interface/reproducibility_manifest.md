# Reproducibility manifest

- Route: `MIN-REFL-C2-H` / `general_mu_interface`.
- Run: `R-20260816T034422Z-min-reflection-cont2`.
- Frozen snapshot: Blueprint
  `358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0`,
  inventory
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Exact runtime: `E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe`.
- Exact dependency: SymPy (version emitted by checker).
- Randomness: none.
- Inputs rederived/audited: the complete two-momentum Cramer system, its
  normalized split bridge, both left/right Schur prefactors, exact
  time-reversal reciprocity, the three-cell gamma-jump gluing, the
  positive-cell margin, and the affine contrast parameterization.  No
  historical route assertion is used without replay.
- Forbidden premise: R17 finite cover or any open R14 coefficient sign.
- Replay command:

```text
E:/ai_auto_solve/O3a_blueprint_v22_research_20260808/.venv/Scripts/python.exe runs/R-20260816T034422Z-min-reflection-cont2/routes/general_mu_interface/exact_checker.py
```

- Replay result: `PASS`, Python 3.12.13, SymPy 1.14.0, no random seed.
- Proof/report artifacts and SHA-256:

```text
problem_contract.md       e7e561b914ab1152f3811467e14ef1979faf4baf0aa3c4eb7c578e1614f470b3
computation_contract.md   0b18f4c04cbb88f636afad6cb2d9d0e63ecb9fdca2f34d7c8d226e40101cda75
report.md                 32a4aea77442b1980e5d76fbc608b0ac73b034004eef816eaa9e790b2fd262b7
exact_checker.py          2e0590c02109a1eca57382ecc5b5f5fa4f62da5a34a6fe7b9dc7dd104b256c9c
exact_checker_output.json 40ccfcdab0b8512e67eca8ff7a503246bfffbf4b2afc2e4d994ad2f821f53927
self_audit.md             274d73ae152312795a8ffc9d71b866504f9ff329b7a97e509846bd1b672aea87
```

- Discovery-only artifact:
  `discovery_scout.py`, SHA-256
  `eef23998bb3254bfbf136d08aaa3eccd4ac6f4acf9bbe2052b95afe80e11eb07`.
  Its floating-point grid is not a proof input.
