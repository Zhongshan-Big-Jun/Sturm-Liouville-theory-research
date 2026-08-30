# Plugin performance report: v1.13 formalization consumption

Date: 2026-08-30

Status: ENGINEERING_VALIDATED. This round produced no new mathematical claim.

## Outcome

Released workflow v1.13.0 with a canonical, immutable Stage C consumption
record for the cross-root Tier 0 handoff introduced in v1.12.

Published revisions:

- Codex parent and fork: `96df6def5ae3ad646cbccc4f397c1f5fd1a84ceb`.
- DSH adapter: `c371ee641933d396b747c4e5addb7ccdc95a8083`.
- Local Codex install: `math-research-workflow@math-research` v1.13.0.

The installed and source `formalization_handoff.py` hashes both equal
`EABE483B097DFADBFFAA19617AD1056E3B5A07FFC42CE7FE70EED097EACA82FF`.

## Consumption contract

After an exact-copy handoff returns `READY`, `consume` writes the one canonical
sibling `FHC-<stable-id>.json`. The caller cannot choose another output path.
The record binds:

- the immutable handoff path, hash, and ID;
- the consumer logical root and formalization status;
- the destination scaffold hash at consumption;
- one Stage C registration that exactly matches a handoff-bound registration;
- explicit `UNCHANGED` mathematical and verification effects.

`verify-consumption` returns `CONSUMED_READY` only when the receipt file,
source run, proof, source scaffold, consumer project identity, consumption-time
artifact hash, and durable Stage C anchor remain valid.

The destination scaffold may legitimately evolve after consumption. This is
the key distinction between the pre-consumption exact-copy check and the
post-consumption history check. Destination evolution does not erase history,
while receipt/source drift, project-ID change, registration removal,
relocation, duplicate consumption, unbound anchors, or a claimed
`FORMALLY_VERIFIED` promotion fails closed.

Both `seal` and `consume` use exclusive file creation. This closes the
check-then-write overwrite race present in the v1.12 sealer.

## Real-artifact drill

Input handoff:
`research/formalization-handoffs/FH-20260830-g1p-live-recovery.json`, SHA-256
`4742146D9BCF0939010986D1FDF2B0520139CEF07AE7851F03D0C8C0F751F7A5`.

Canonical consumption:
`research/formalization-handoffs/FHC-20260830-g1p-live-recovery.json`, SHA-256
`15655FD04103F565A13D8662D122DE9BDA7BA2E3C440D0937D877DC0E7351E1C`.

The installed v1.13 script returned `CONSUMED` and then `CONSUMED_READY`. It
bound the existing `v1.9 live recovery G1 prime sector run` registration in
`lean-proof/formalization_progress.md` and the scaffold snapshot SHA-256
`02D5F0FDA3598D35DFF34E50686445CB3C1F20F895E7A2A4905CD65B32384C0B`.

Ten installed-script consumption verification replays took 1665.324 ms in
total, or 166.532 ms per replay on this Windows host. The round used zero model
research calls, zero research children, zero network calls in the drill, and no
mathematical recomputation.

The mathematical status is unchanged: this remains a Tier 0 scaffold for a
`RIGOROUS_PARTIAL_RESULT`. `KP-DET`, simultaneous sector singularity, `KO-DET`,
non-symmetric roots, and global G1' remain OPEN.

## Validation

Parent plugin repository:

- `validate_all.py`: 81/81.
- Smoke tests: 13/13.
- Workflow plugin validator and UTF-8 skill validator: PASS.
- Python compile and `git diff --check`: PASS.

DSH adapter:

- `validate_all.py`: 51/51.
- Smoke tests: 17/17. The existing handoff smoke gained the new consumption
  adversarial cases, so the smoke file count did not increase.
- Bundle check, Node syntax check, sync-check, Python compile, and diff check:
  PASS.
- Upstream lock: 110 files at parent commit `96df6de`.

Adversarial coverage includes duplicate consumption, unbound registration,
receipt mutation, status promotion, append-only index evolution, anchor
removal, destination scaffold evolution after consumption, and exclusive
overwrite refusal.

## Static context cost

The always-loaded workflow SKILL entry changed from 27,619 bytes in v1.12.0 to
27,657 bytes in v1.13.0, an increase of 38 bytes, or about 0.14 percent. It
retains 5,111 bytes of headroom below the 32,768-byte gate. All consumption
mechanics live in the on-demand formalization handoff reference.

## Remaining boundary

The environment still provides no active `runtime/blueprintctl.py`. No legacy
project-local Blueprint tool was run or copied. Blueprint v2.2 gateway and
artifact-root migration remain OPEN and separate from this workflow-owned
consumption receipt.
