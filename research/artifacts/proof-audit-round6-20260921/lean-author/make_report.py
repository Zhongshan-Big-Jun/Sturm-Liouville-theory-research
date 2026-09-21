from pathlib import Path
import hashlib, json

Base = Path(__file__).resolve().parent
Result = json.loads((Base / 'RESULTS.json').read_text())
assert Result['status'] == 'passed' and Result['wrong_expected_type_rejected']
Replay = Path(Result['replay_directory'])
Bindings = json.loads((Base / 'root-object-bindings.json').read_text())
Runtime = json.loads((Base / 'runtime-config.json').read_text())
Source = Path(json.loads((Base / 'freeze.json').read_text())['original_source'])
Text = f'''# Round 6 formalization author report

The bounded local formalization is complete, with actual author execution.
This is not independent final review or approval. The coordinator's later
stateless review and independent replay remain separate.

## Exact source and target

- New source: `{Source}`.
- Source SHA-256: `{Result['source_sha256']}`.
- Exact compound target: `{Result['declaration']}`.
- Root object SHA-256: `{Result['root_object_sha256']}`.
- 15 definitions and 21 public theorems; 36 actual elaborated public records.
- 24 exported reachable local definitions, including 9 fifth-round definitions.

## Mathematical coverage

| Part | Actual proved content | Boundary |
| --- | --- | --- |
| Sparse family | Over Polynomial R, p0, p1, both families for every m >= 2, plus X^2 and X^3 span all polynomials; the sparse span excludes X^2. | Algebraic span only; no conclusion about a Hilbert-space closure follows from this alone. |
| Four traces | Actual derivative/evaluation map (B_+ p, B_- p, B_+ p'', B_- p''); its X^2 through X^5 columns, determinant 15360, explicit two-sided matrix inverse, polynomial-valued linear right inverse, and universal correction with four zero traces. | Does not extend trace maps or right inverses to a Sobolev space or establish their continuity there. |
| Cancellation | p6 - (7/2)p4 = X^6 - 5X^4 + 7X^2 has four zero traces; p4 has trace vector (0,0,24,-24), hence nonzero. | Zero traces are not identified here with a spectral operator domain. |
| Coordinate constraint | In EuclideanSpace R (Fin 2), v=(1,1), w=(1,-1), e0=(1,0), e1=(0,1): the five actual inner products are 1,1,0,1,-1. | A real two-dimensional counterexample to separate coordinate pinning; no infinite-series Hilbert counterexample is formalized. |

The augmented-span result uses all-index even and odd induction, followed by
polynomial induction. It is not a collection of degree samples. The root has
no outer binders, no assumed target, and no assumed density statement. The trace
map and its right inverse are actual LinearMaps; EuclideanSpace carries the
actual Mathlib real inner product. Author reading checked the elaborated family,
span, endpoint, second-derivative, lift and vector definitions against this
contract. That is author semantic assessment, not independent blind readback.

## Actual execution and evidence

- Windows PE Lean 4.31.0, x86_64-w64-windows-gnu, compiler commit
  68218e876d2a38b1985b8590fff244a83c321783, launched through WSL.
- Actual Mathlib Git HEAD matches its pin
  fabf563a7c95a166b8d7b6efca11c8b4dc9d911f. All nine package heads match the
  manifest. The source-only Cli package has no build directory and is not put
  into the object search path.
- Unchanged AuditRound5 source SHA-256:
  `{Bindings['AuditRound5_source_sha256']}`.
  Both local modules were rebuilt from the frozen snapshot in each maintained
  verifier output. Root resolution points to that fresh output. Old project
  objects are absent from LEAN_PATH.
- Maintained positive verifier: strict exit 0, actual expected type matched,
  `exact_root_passed=true`, root closure closed.
- Compiling positive control: exit 0.
- Maintained wrong-type control: determinant expected as 15361 instead of 15360;
  compilation/extraction succeeds, strict exit 1, root status `target_mismatch`.
- Root axiom closure: propext, Classical.choice, Quot.sound only. No unknown or
  unsafe dependencies. The 36 public declarations have separately extracted
  axiom lists and graph-recomputed closures; all comparisons pass.
- One shared public dependency graph has {Result['shared_dependency_nodes']} nodes.
  The maintained root inventory records {Result['loaded_module_count']} loaded
  modules and {Result['module_artifact_count']} hashed import artifact entries.
  There is no full environment dump per theorem.
- The maintained semantic field remains `not_reviewed`; no independent review
  was fabricated by supplying an author-written approval.
- {Result['protected_old_files_unchanged']} protected old source/config/object files
  match their before hashes. The broader 306-file baseline also included
  SL/.gitattributes, which gained exactly the new AuditRound6.lean -text rule
  and its comment during parallel coordination. Its prior bytes remain an
  exact prefix. This author did not write or revert that coordinator-owned
  Git-policy file; the individual writer was not independently identified.
  The change and both hashes are explicitly recorded in protection-check.json.
  No project AGENTS, report, library, Git delivery,
  canonical or plugin source/cache edits were performed by this author.

Runtime binaries, tools, source and pin hashes are in `freeze.json` and
`runtime-config.json`. The full command arguments, raw stdout/stderr, exit codes,
generated inspection sources, declarations and resolved objects are retained
under `{Replay.name}`. Compiler and precompiled package artifacts remain trust
inputs; no full Mathlib source rebuild or second kernel check is claimed.

## Replay and handoff

```bash
python3 -B {Base}/replay.py /mnt/f/tools/CHOOSE_A_NEW_OUTPUT_DIRECTORY
```

The directory must be new. The frozen entrypoint was actually run to completion
as author job `round6-lean-author-02`. `REPLAY.md` also gives an optional durable
launcher, which is useful when a client terminates long foreground commands.
The executor can choose a fresh directory with no source edits or prior-object
modification. No extra per-theorem verification environments are required.

`BLIND_PACKET.json` and `HANDOFF.json` select actual types and elaborated
reachable definition data only, including R5 definitions. Full R5 source,
intended-meaning comments and proof scripts are excluded from blind readback.
The semantic/execution packet includes full unchanged R5 source. The later
coordinator correction is recorded in `HANDOFF_RULES.md`, superseding the older
packet suggestion in the byte-preserved frozen CONTRACT.md.

## Preserved failures and omissions

All actual failed attempts remain in `attempts/`, `logs/` and their build
directories: the initial missing-Cli-directory runner failure, SL path shadowing,
comment parsing, matrix notation, coefficient normalization and finite-index
simplification failures. No final proof uses those failed states. Development
compile 13 completed successfully without warnings.

The first complete packaging attempt, `replay-author-01`, was interrupted with
outer session exit 143 before its final manifest. Its cause was not established;
it is not counted as success. Compiler and extraction logs remain with
`INTERRUPTED.json`. The subsequent durable job and its actual result are kept
under `.research-state/jobs/`.

The first finalization pass conservatively stopped on the concurrent
SL/.gitattributes append. Its exact traceback and script are retained under
attempts/finalize-01. The final pass checks that append separately instead of
falsely counting it as an unchanged file. No Lean source or object changed.

Not formalized: the complex analytic appendices, weighted infinite-series
counterexample, Sobolev density or graph cores, spectral asymptotics, convergence,
fractional powers or the 7/2 threshold/window. Also omitted are the optional
general Hilbert projection identity, finite-dimensional tail-obstacle injection
lemma, and sparse-span equality with the full Krein polynomial kernel. These
are scope omissions, not claimed failures or impossible targets.

## File entrypoints

- `CONTRACT.md`, `HANDOFF_RULES.md`: exact scope and current packet selection.
- `RESULTS.json`, `root-object-bindings.json`, `closure-consistency.json`:
  compact actual outcomes and bindings.
- `BLIND_PACKET.json`, `HANDOFF.json`: selected file hashes for later reviewers.
- `replay.py`, `REPLAY.md`, `launch_replay.py`: replay instructions and entrypoints.
- `snapshot/`, `candidate-inputs/`, `freeze.json`, `runtime-config.json`:
  frozen sources, candidate evidence, pins, runtime and tool identities.
- `{Replay.name}/positive/run-manifest.json` and
  `{Replay.name}/negative/run-manifest.json`: maintained positive/negative receipts.
- `{Replay.name}/public-declarations.json`, `public-types.txt`,
  `local-definitions.json`, `local-definitions.txt`,
  `shared-public-dependency-graph.json`: actual elaborated data and shared graph.
- `protection-check.json`, `WORK_LOG.md`, `FILE_LIST.txt`, `FILE_HASHES.sha256`:
  preservation, development history and complete local file inventory.
'''
(Base / 'REPORT.md').write_text(Text)
Files = sorted(p for p in Base.rglob('*') if p.is_file() and p.name not in ('FILE_LIST.txt', 'FILE_HASHES.sha256'))
(Base / 'FILE_LIST.txt').write_text(str(Source) + '\n' + '\n'.join(str(p.relative_to(Base)) for p in Files) + '\nFILE_LIST.txt\nFILE_HASHES.sha256\n')
with (Base / 'FILE_HASHES.sha256').open('w') as File:
	for PathName in [*Files, Base / 'FILE_LIST.txt']:
		with PathName.open('rb') as Stream:
			Hash = hashlib.file_digest(Stream, 'sha256').hexdigest()
		File.write(Hash + '  ' + str(PathName.relative_to(Base)) + '\n')
print('REPORT.md and file inventory written:', len(Files), 'files plus inventories')
