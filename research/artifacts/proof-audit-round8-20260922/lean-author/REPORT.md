# Round 8 local Lean author report

Status: **AUTHOR_MACHINE_CHECKS_PASSED** for the stated local contract. Independent verification and independent semantic review are **pending**. All work and writes are confined to `/mnt/f/tools/math-audit-round8-20260922/lean-author`. No project/library/git/global configuration was written, no agents were started, and no Mathlib download/rebuild or full Lake build was run.

## Deliverables and identity

- Standalone source: `AuditRound8.lean`.
- Source SHA-256: `3cbc7e84dab06ffdc2cc974a9d7553c47847eca4227e49024f04a1e91ccc486e`.
- Full nine-conjunct expected type: `positive-contract.json`, SHA-256 `73343f7985954ee2f88b55546d89684bef34016956ce81d8c4a4a6025065f72a`.
- Public declaration contract: `public-declaration-contract.json`.
- Author mathematical correspondence and every condition/exclusion: `README.md`.
- Actual complete elaborated type/definition readback: `PUBLIC-READBACK.md`; lossless expressions, dependency graph and transitive axioms: `author-replay-03/declarations.json`.
- Final raw execution: `author-replay-03/`; raw file manifest: `author-replay-03/receipt-manifest.json`.
- Final replay UUID: `ec5fe5fe-5513-4a27-8a73-283b42166f2d`; UTC 2026-09-21T16:50:31.148070+00:00 to 2026-09-21T16:52:44.713349+00:00.
- Fresh compiled root object: `/mnt/f/tools/math-audit-round8-20260922/lean-author/author-replay-03/lib/AuditRound8.olean`; SHA-256 `66a222f836b7b0f94b5a713202dd800af0bb2f78394ebce3663c94720949d26d`.
- Runtime: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`.
- Mathlib revision: `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.
- Frozen complete external environment identity: `9fd3c7c278bca4802689d3db40034e598740cbefa523caabf61fc86d23acedef`; imports and runtime DLLs are hashed in `external-environment.json`.
- Public declaration semantic data identity: `95c2c0f2e6870994137bc3472397ced7be0a6c844341519d0c9b0b97f35f5159`. This hashes actual declarations/definitions and their reached axioms; it is not a human review verdict.

## Actual scope and counts

The root proves the conditional small-u phase bound; the actual trigonometric I2 and S reductions; the explicit coefficient identity; stationary coefficient equality and positivity; the exact rational ratio <0.8256; and both B/D curved-coverage witnesses with actual pi bounds. In particular the trigonometric-to-S bridge **is formalized**. No desired C-equation is an input hypothesis.

15 handwritten theorems and 11 definitions produce 47 actual public namespace declarations (36 theorems, including 21 compiler-generated auxiliaries, and 11 definitions). All 47 were exported and axiom-checked. The actual type/body closure contains 16511 declarations, with no unknown or unsafe nodes or disallowed axioms. Root axioms: `['propext', 'Classical.choice', 'Quot.sound']`.

The final replay completed 10 commands: current-source compilation, complete positive contract and actual extraction passed; three genuine wrong-target Lean compilations failed as intended. It resolved the imported root to its own fresh output olean. It checked 4427 external modules (4428 modules including the root during inspection), 17708 external olean/private/server/IR artifacts, and 10 runtime binaries before/after, with exact stability. No previous author output is called independent evidence.

Across development and replay, 32 recorded processes include 25 actual Lean invocations. There are 10 nonzero process receipts, including the three intentional mathematical negative controls; nonzero outcomes were not removed or reclassified as passes. Exact command/count scope is in `command-index.json` and `author-evidence.json`.

## Conditions and nonformalized work

- Phase: lambda2 is a real parameter with `0<=lambda2<=4*pi^2`. The spectral minmax comparison is an explicit premise.
- I2/S bridge: a,u,b>0 and `sin a+b*a*cos a=0`. The trigonometric formulas are genuine definitions; identifying I2 as a normalization integral remains analytic.
- Coefficient: a>0, 0<u<1/2, b=(1/2-u)/u, and the same root equation. Stationary simplification additionally assumes S(a,u)=0. The statements prove algebra for the explicitly defined C; they do not establish that C is the coefficient of an actual eigenvalue expansion or prove the existence/location of u*.
- Scalar: the final rational combination of the supplied constants is proved. Bounds feeding those constants, such as Cz and B(t), are not established by this Lean file.
- Curves: the B/D rational witnesses and their precise curve inequalities are proved. The historical Python code and complete domain partition are not formalized. These are coverage witnesses, not density examples with G<25.

Explicitly excluded: **full spectral minmax, analytic implicit-function expansions and remainders, spectral mode/root selection, T1/deep-sliver and global coverage certification, global convergence, exchanges of infimum and limit, and global minimizing-parameter rates**.

## Preserved failures and recovery

1. `development/attempts/attempt-01` / its logs: two polynomial consequences required explicit multiplication, and b*u=ell was reversed. Exit 1, original bytes retained. The corrected core passed attempt-02.
2. `development/attempts/attempt-03`: field_simp had already closed a goal and the following ring reported no goals. Exit 1 retained. Full source/root passed attempt-04 and every later current-source compile.
3. `exporter-smoke-01` and `author-replay-01`: the reporter had an invalid match/if layout. Its standalone and full replay failures are retained. The full replay did compile the source and positive contract before failing export; it was never reported as a completed pass.
4. `replay-launches/logs/stop-author-replay-01`: the identity-checked attempted stop found the old replay had already exited; it failed with FileNotFoundError before sending any signal. This diagnostic failure is retained.
5. `exporter-smoke-02` passed. `author-replay-02` also passed compilation/positive control/export, then the Python inventory guard rejected 47 names because it expected only 26 handwritten names. Retained that rejection. The fixed contract includes all 21 compiler-generated theorem names and the final replay validates all 47.
6. `author-replay-03` is the completed fresh run. WrongPhase and WrongStationaryFactor failed with actual type mismatches; WrongScalar failed on the false rational target. All three retain source, stdout, stderr, exit and hashes.

Every recorded process below has a raw receipt plus full stdout/stderr hashes and immutable source snapshots. `freeze-history` keeps previous reporter/input versions. The preliminary read/search/edit shell calls are preserved in the task conversation; the process counts below intentionally count the recorded author execution harness only.

| Receipt | Actual run UUID | Exit |
| --- | --- | --- |
| `author-replay-01/logs/01-version.json` | `7ff37479-f5c5-46a7-93b0-f28acfcda65f` | 0 |
| `author-replay-01/logs/02-mathlib-revision.json` | `397ba28b-42dc-43c9-8c6b-b1950cf74af5` | 0 |
| `author-replay-01/logs/03-import-discovery.json` | `762a9bbb-1685-4161-a30c-0425a1ffd9e0` | 0 |
| `author-replay-01/logs/04-compile-current-source.json` | `33db00b7-8ccc-4f8e-8be7-244d1eb40a48` | 0 |
| `author-replay-01/logs/05-positive-control.json` | `e1096897-6637-4204-bdc5-ee62b92d08c4` | 0 |
| `author-replay-01/logs/06-declaration-inspection.json` | `e8218146-daf2-4c3d-860b-c282471d781a` | 1 |
| `author-replay-02/logs/01-version.json` | `52283f9e-d4f3-4548-813b-7bcee3d493ce` | 0 |
| `author-replay-02/logs/02-mathlib-revision.json` | `8a706975-5e48-4ab5-b76c-14e33efb93ae` | 0 |
| `author-replay-02/logs/03-import-discovery.json` | `a0093c93-ae6f-4118-8cf5-f28381978aad` | 0 |
| `author-replay-02/logs/04-compile-current-source.json` | `7c8c50e5-3993-4a38-97d5-0e4b29215665` | 0 |
| `author-replay-02/logs/05-positive-control.json` | `c0b21cf6-a123-4b6a-a3c4-a43f2c95f2cf` | 0 |
| `author-replay-02/logs/06-declaration-inspection.json` | `9da2aa69-7701-417a-8ea2-6ecfad6c3c8f` | 0 |
| `author-replay-03/logs/01-version.json` | `65cb8f01-8719-4034-b0ed-6fadf9160ef4` | 0 |
| `author-replay-03/logs/02-mathlib-revision.json` | `4e4c0af8-92c3-400c-8e0c-8d3ced79d1a2` | 0 |
| `author-replay-03/logs/03-import-discovery.json` | `d04c09f7-70b3-47b1-810e-09b200a04d9b` | 0 |
| `author-replay-03/logs/04-compile-current-source.json` | `4b99728a-5c78-4b89-b7a6-6bf627139519` | 0 |
| `author-replay-03/logs/05-positive-control.json` | `d9010e6b-404d-45d6-b2a6-4ff4e6f8abc1` | 0 |
| `author-replay-03/logs/06-declaration-inspection.json` | `fe8b3090-ca38-4e32-b434-56e6bbc2b703` | 0 |
| `author-replay-03/logs/07-root-resolution.json` | `c73b259f-b42b-45b8-b25f-b02a3f6e7a38` | 0 |
| `author-replay-03/logs/08-WrongPhase.json` | `78021c8f-b6b8-4119-9501-4d775df9ecf7` | 1 |
| `author-replay-03/logs/09-WrongStationaryFactor.json` | `b85c7ad0-0d81-47af-b178-f026398fa0e1` | 1 |
| `author-replay-03/logs/10-WrongScalar.json` | `b5a2690e-f709-4b55-8d13-70d10e964050` | 1 |
| `development/logs/attempt-01.json` | `fa9a8a24-d7f0-4b3a-9e76-683a3835068a` | 1 |
| `development/logs/attempt-02.json` | `407c1fb8-bf20-4248-9377-a16da547b69e` | 0 |
| `development/logs/attempt-03.json` | `f5b4fecb-7e39-4b3c-a501-8964a09bd9ef` | 1 |
| `development/logs/attempt-04.json` | `bd5b3101-1eed-4bf2-92f9-36b73c92ddce` | 0 |
| `exporter-smoke-01/logs/inspection.json` | `acc72755-55c8-4aa7-b387-ff9632daa1f8` | 1 |
| `exporter-smoke-02/logs/inspection.json` | `68935f11-d798-4520-b4f0-726c9de38f72` | 0 |
| `replay-launches/logs/author-replay-01.json` | `1355ea79-4d7a-41d2-b03d-601e6158e528` | 1 |
| `replay-launches/logs/author-replay-02.json` | `48d349c3-fcdd-4e37-a4cb-2a9c54dceb5b` | 1 |
| `replay-launches/logs/author-replay-03.json` | `ae9d452c-dd1a-40e7-9e75-c756946cb803` | 0 |
| `replay-launches/logs/stop-author-replay-01.json` | `b8abf4bc-3b88-410c-adf0-775549acd649` | 1 |

## New verifier replay

`round8-lean-frozen-inputs.zip` is the compact task-source replay package. It contains all scripts, source, exact contracts, negative controls, informal source snapshots, full environment hash bindings, attribution, and readback needed for a new verifier. Installed external Lean/Mathlib artifacts are reused; no precompiled local root is included. The durable failed/successful author logs remain separately in this directory to avoid copying a large redundant history into the input package.

Extract/copy into the verifier's own authorized directory and run `python3 -B /absolute/path/to/copied-package/replay.py /absolute/path/to/new-output`. The runner writes only to the new output and freshly compiles the copied current source. It reports execution only; the new verifier supplies its own semantic assessment and independence provenance. Check the archive hash and per-file bindings in `handoff-manifest.json`.
