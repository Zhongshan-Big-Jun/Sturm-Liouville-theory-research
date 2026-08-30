# Plugin performance report: v1.12 formalization handoff

Date: 2026-08-30

Status: ENGINEERING_VALIDATED. This round produced no new mathematical claim.

## Outcome

Released workflow v1.12.0 with a deterministic cross-root Tier 0
formalization handoff. An immutable receipt now binds an isolated Stage B
logical project to the exact scaffold consumed by the parent Stage C Lean
project.

Published revisions:

- Codex parent and fork: `299111dda6689766cebca0d5b2497f91ed75e98a`.
- DSH adapter: `aed0d4acf129d13dedc9450d7d6863f3563b8021`.
- Local Codex install: `math-research-workflow@math-research` v1.12.0.

The installed and source `formalization_handoff.py` hashes both equal
`CAE5178A7A066546A086AE3143D2564B4EF44C922343F1B66449188E33ACEBC8`.

## Receipt contract

`formalization_handoff.py seal/verify` accepts only
`formalization=scaffold` and `copy_mode=exact`. The receipt binds:

- source and destination logical-root markers, project IDs, and marker hashes;
- source run ID, run manifest, proof, and Tier 0 scaffold;
- an identical destination scaffold;
- durable destination registration anchors and their seal-time hashes;
- the repository HEAD when git metadata is available.

Absolute paths, root escapes, nested git roots, missing or duplicate manifest
artifacts, hash drift, missing registration anchors, and receipt overwrite all
fail closed.

Full `formalization=requested` packages are deliberately unsupported. Such a
package needs its own bindings for Lean environment, build evidence,
`verification.json`, obligation map, and fidelity audit. This receipt never
promotes a scaffold to `FORMALLY_VERIFIED`.

## Real-artifact drill

Source logical root:
`runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace`.

Source run:
`R-20260830T020000Z-g1p-live-recovery`.

The receipt at
`research/formalization-handoffs/FH-20260830-g1p-live-recovery.json` verified
`READY` with SHA-256
`4742146D9BCF0939010986D1FDF2B0520139CEF07AE7851F03D0C8C0F751F7A5`.
It binds:

- the audited partial proof;
- source and parent `lean-proof/SL/KpOddFirstZero_Scaffold.lean`, both with
  SHA-256
  `02D5F0FDA3598D35DFF34E50686445CB3C1F20F895E7A2A4905CD65B32384C0B`;
- parent registrations in `lean-proof/STATUS.md`, `lean-proof/README.md`, and
  `lean-proof/formalization_progress.md`.

Ten installed-script verification replays took 1594.692 ms in total, or
159.469 ms per replay on this Windows host. The drill used zero model calls,
zero research children, zero network calls, and no mathematical recomputation.

The mathematical status is unchanged: the artifact remains a Tier 0 scaffold
for a `RIGOROUS_PARTIAL_RESULT`; `KP-DET`, simultaneous sector singularity,
`KO-DET`, non-symmetric roots, and global G1' remain OPEN.

## Validation

Parent plugin repository:

- `validate_all.py`: 81/81.
- Smoke tests: 13/13.
- Workflow plugin validator and UTF-8 skill validator: PASS.
- Python compile and `git diff --check`: PASS.

DSH adapter:

- `validate_all.py`: 51/51.
- Smoke tests: 17/17.
- Bundle check, Node syntax check, sync-check, Python compile, and diff check:
  PASS.
- Upstream lock: 110 files at parent commit `299111d`.

On this host, `python.exe` first resolves to the WindowsApps placeholder and
returns 9009. Release checks therefore used `py -3`; the skill quick validator
also used `-X utf8` to avoid the Windows GBK default.

## Static context cost

The always-loaded workflow SKILL entry decreased from 31,931 bytes in v1.11.0
to 27,619 bytes in v1.12.0, a reduction of 4,312 bytes, or about 13.5 percent.
It now has 5,149 bytes of headroom below the 32,768-byte gate.

The complete Stage C decision states, verification tiers, dual-track audit,
lemma reuse, supersession, escalation, and repair loop moved into the 5,465
byte on-demand `references/stage-c-formalization.md`. The entrypoint retains
the hard boundary and an explicit read-before-Stage-C route, so the reduction
does not relax verification semantics.

## Blueprint v2.2 boundary

The current installed Codex skills and plugin caches still provide no active
`runtime/blueprintctl.py`. No project-local legacy Blueprint tool was run or
copied. The authoritative Blueprint gateway and artifact-root migration remain
OPEN. This does not affect the workflow-owned handoff receipt under
`research/`, but it prevents any claim that the separate Blueprint migration
has been completed.

## Next bounded optimization candidates

1. Obtain or implement the authoritative Blueprint v2.2 runtime gateway, then
   exercise `ensure` and artifact-root resolution without local tool copies.
2. Design a separate full verification-package handoff only after a real
   cross-root Tier 2 artifact exposes its minimum reproducibility contract.
3. Add a consumer-side Stage C command that records receipt consumption without
   mutating the immutable receipt.
