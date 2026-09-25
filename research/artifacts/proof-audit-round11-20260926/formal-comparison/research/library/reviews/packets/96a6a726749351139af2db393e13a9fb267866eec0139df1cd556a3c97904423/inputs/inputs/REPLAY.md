# Reproduction and review routing

The author's actual commands, working directories, start/end times, process IDs, input copies, SHA-256 identities, exit codes and complete stdout/stderr are under `commands/<label>/`. The driver logs are convenience summaries; the command records and native verifier runs are the authoritative execution records. Existing command labels are immutable and the adapter refuses to overwrite them.

`run.py` was adapted from the read-only round10 adapter. It launches the specified Windows Lean 4.31.0 executable with a Windows `LEAN_PATH` containing the existing package build libraries. Every compilation output and temporary directory is inside this author workspace. No Lake build or download is invoked. `environment-baseline.json` records all nine declared dependency revisions and actual Git heads, and hashes the runtime binaries and unchanged installed verifier files. The exact-root manifest additionally inventories the modules actually loaded; the environment baseline alone is not a full loaded-module receipt.

Author direct compilation, with a NEW unused command label:

```bash
python3 -B /mnt/f/tools/math-audit-round11-20260926/formal-author/run.py compile NEW_COMPILE_LABEL
```

Author exact-root verification, with a NEW unused command label:

```bash
python3 -B /mnt/f/tools/math-audit-round11-20260926/formal-author/run.py verify NEW_ROOT_LABEL contract.json
```

These commands write new evidence inside this author directory. A later reviewer should instead use their own authorized workspace, copy `project/AuditRound11.lean`, `project/lean-toolchain`, and `contract.json`, reuse the read-only package search paths from `environment-baseline.json`, and invoke the unchanged installed `verify_lean_project.py` with `--direct`, `--strict-exit`, the explicit Windows `--lean` and `--lake` executables, and a new reviewer output directory. The package artifacts are external dependencies; do not copy the entire `.lake` directory.

Use `formal-only/packet.json` and only its listed files for independent blind mathematical readback. This contains no intended prose contract, external report, author explanation or author verdict. It includes a comment-free, separately compiled source with the original identifiers, definitions and proofs, and actual explicit declaration/axiom exports. Generated Lean equation theorems are included in the namespace export and are identified separately from the 14 authored theorem names.

A separate comparison reviewer should then receive that readback plus `contract.md`, `contract.json`, `summary.json`, the two original report snapshots under `inputs/`, and the machine evidence. The reviewer should check the pairing convention, real scalar domain, conditional Jacobian premise, empty dimension, zero direction, all-natural `L≥4` scope, explicit boundary entries, and the absent bridges to differentiation/complex analysis/Sobolev closure. This author has not supplied either independent review.

The positive/negative mathematical controls are in `project/*Controls.lean` and `project/Negative*.lean`. Their logs distinguish an intended rejection from a development failure. The separate `closure-control-project` intentionally contains an extra axiom; its positive target does not depend on that axiom, whereas its contaminated target does. It is never imported by `AuditRound11.lean`.

The remaining linter messages on the conjunction root say that named premise binders are not referenced in later parts of the proposition. Those premises are still present in the exported types. No `sorry`, `admit`, user axiom or unsafe declaration occurs in the main source.
