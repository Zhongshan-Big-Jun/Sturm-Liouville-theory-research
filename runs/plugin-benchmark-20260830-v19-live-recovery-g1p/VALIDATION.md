# Final validation

Date: 2026-08-30.

## Scoped program gate

Command:

```powershell
py -3.10 C:\Users\HuangZY\.codex\skills\manage-math-research-program\scripts\validate_project.py .
```

Working directory:
`runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace`.

Result: `PASS`. The project is `VALID`, with no integrity or boundary issues.

## Scoped pipeline gate

Command:

```powershell
py -3.10 C:\Users\HuangZY\.codex\plugins\cache\math-research\math-research-workflow\1.9.0\scripts\validate_pipeline.py --project .
```

Working directory:
`runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace`.

Result: `PASS`, with 0 problems and 2 expected warnings.

1. `RIGOROUS_PARTIAL_RESULT` is outside the formalization completion gate.
2. The isolated workspace has no canonical `lean-proof/run-manifest.json`.

The first warning is the honest mathematical status. The second reflects the
declared Tier 0 scaffold handoff to the parent Lean project.

## Manifest hash audit

Result: `PASS`.

All eight artifacts listed in the scoped `run-manifest.json` match their
declared SHA256 values. The parent and scoped Lean scaffold copies are
byte-identical, with SHA256
`02d5f0fda3598d35dff34e50686445cb3c1f20f895e7a2a4905cd65b32384c0b`.

## Lean scaffold

Command:

```powershell
lake env lean SL/KpOddFirstZero_Scaffold.lean
```

Working directory: `lean-proof`.

Result: `PASS`, exit code 0. Lean reports exactly two expected `sorry`
warnings, at lines 26 and 42. This is a compiling Tier 0 scaffold and is not a
formal verification result.

## Files-only convergence check

Result: `PASS`.

`CONVERGENCE_CHECK.md` reconstructs the honest partial status, exact open
obligations, nonduplicated W2 recovery lineage, and fresh audit bindings from
files alone. Its SHA256 is
`ef9b5ffa6ce6b2cf892380267cf18a7b0e36563e3c34b999801ac2f9d4ca6294`.

## Repository diff gate

`git diff --check` passed. Unrelated existing LaTeX build outputs and scratch
scripts were excluded from the result transaction.
