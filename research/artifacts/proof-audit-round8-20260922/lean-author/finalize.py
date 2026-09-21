"""Assemble author handoff only after the actual complete replay passes."""
from pathlib import Path
import hashlib,json,re,zipfile,collections
from run_lean import BASE,digest,write_json

runroot=BASE/'author-replay-03'
e=json.loads((runroot/'evidence.json').read_text())
if e['status']!='AUTHOR_MACHINE_CHECKS_PASSED': raise RuntimeError('No completed success')
freeze=json.loads((BASE/'freeze.json').read_text())
if not all(digest(BASE/n)==h for n,h in freeze['files'].items()): raise RuntimeError('Frozen input changed')
manifest=json.loads((runroot/'receipt-manifest.json').read_text())
if not all(digest(runroot/n)==h for n,h in manifest['files'].items()): raise RuntimeError('Final raw receipt changed')
d=json.loads((runroot/'declarations.json').read_text())
contract=json.loads((BASE/'public-declaration-contract.json').read_text())
origin={p['declaration']:p['origin'] for p in contract['entries']}
lines=['# Actual Lean declaration and definition readback','',
 'Generated from the completed author replay declarations.json. This is machine readback, not an independent mathematical review. Every namespace declaration, including compiler-generated auxiliaries, is retained. Explicit elaborated expressions and the complete type/body dependency graph remain in the raw JSON.','',
 '| Source SHA-256 | '+e['source_sha256']+' |',
 '| --- | --- |','| Replay run UUID | '+e['run_id']+' |','']
for p in d['public_declarations']:
 lines += ['## '+p['declaration'],'',f"Kind: {p['kind']}; origin: {origin[p['declaration']]}; universes: {p['universes']}; transitive axioms: {p['axioms']}.",'','```lean',p['display_type'],'```','']
 if p['kind']=='definition': lines += ['Actual body:','','```lean',p['value_readback'],'```','']
(BASE/'PUBLIC-READBACK.md').write_text('\n'.join(lines))
receipts=[]
for p in sorted(BASE.rglob('logs/*.json')):
 r=json.loads(p.read_text())
 if 'argv' not in r: continue
 if 'exit_code' not in r: raise RuntimeError('Still-running/incomplete command '+str(p))
 for stream in ('stdout','stderr'):
  q=p.with_suffix('.'+stream+'.txt')
  if digest(q)!=r[stream+'_sha256']: raise RuntimeError('Changed raw log '+str(q))
 receipts.append({'path':str(p.relative_to(BASE)),'sha256':digest(p),'run_id':r['run_id'],'exit_code':r['exit_code'],
  'executable':r['argv'][0],'label':r['label'],'duration_seconds':r['duration_seconds'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']})
if len({r['run_id'] for r in receipts})!=len(receipts): raise RuntimeError('Duplicate run UUID')
write_json(BASE/'command-index.json',{'all_recorded_processes':len(receipts),'commands':receipts})
lean=[r for r in receipts if r['executable'].lower().endswith('/lean.exe')]
failed=[r for r in receipts if r['exit_code']!=0]
byexit=dict(collections.Counter(r['exit_code'] for r in receipts))
write_json(BASE/'author-evidence.json',{'role':'local_lean_author','independent_verification':'pending','final_replay':e,
 'source_sha256':digest(BASE/'AuditRound8.lean'),'freeze_sha256':digest(BASE/'freeze.json'),
 'receipt_manifest_sha256':digest(runroot/'receipt-manifest.json'),'command_index_sha256':digest(BASE/'command-index.json'),
 'all_recorded_processes':len(receipts),'all_lean_processes':len(lean),'process_exit_counts':byexit,
 'nonzero_processes':failed,'raw_receipts_scope':'All Lean, exporter, replay, git-revision and attempted-stop processes launched through the recorded author helpers; preliminary file reads/edits are in the task conversation, not counted as compiler receipts.'})
rows=['| Receipt | Actual run UUID | Exit |','| --- | --- | --- |']
for r in receipts: rows.append(f"| `{r['path']}` | `{r['run_id']}` | {r['exit_code']} |")
text=f'''# Round 8 local Lean author report

Status: **AUTHOR_MACHINE_CHECKS_PASSED** for the stated local contract. Independent verification and independent semantic review are **pending**. All work and writes are confined to `{BASE}`. No project/library/git/global configuration was written, no agents were started, and no Mathlib download/rebuild or full Lake build was run.

## Deliverables and identity

- Standalone source: `AuditRound8.lean`.
- Source SHA-256: `{e['source_sha256']}`.
- Full nine-conjunct expected type: `positive-contract.json`, SHA-256 `{e['contract_sha256']}`.
- Public declaration contract: `public-declaration-contract.json`.
- Author mathematical correspondence and every condition/exclusion: `README.md`.
- Actual complete elaborated type/definition readback: `PUBLIC-READBACK.md`; lossless expressions, dependency graph and transitive axioms: `author-replay-03/declarations.json`.
- Final raw execution: `author-replay-03/`; raw file manifest: `author-replay-03/receipt-manifest.json`.
- Final replay UUID: `{e['run_id']}`; UTC {e['utc_start']} to {e['utc_end']}.
- Fresh compiled root object: `{e['olean_path']}`; SHA-256 `{e['olean_sha256']}`.
- Runtime: `{e['lean_version']}`.
- Mathlib revision: `{e['mathlib_commit']}`.
- Frozen complete external environment identity: `{e['environment_sha256']}`; imports and runtime DLLs are hashed in `external-environment.json`.
- Public declaration semantic data identity: `{e['public_semantic_sha256']}`. This hashes actual declarations/definitions and their reached axioms; it is not a human review verdict.

## Actual scope and counts

The root proves the conditional small-u phase bound; the actual trigonometric I2 and S reductions; the explicit coefficient identity; stationary coefficient equality and positivity; the exact rational ratio <0.8256; and both B/D curved-coverage witnesses with actual pi bounds. In particular the trigonometric-to-S bridge **is formalized**. No desired C-equation is an input hypothesis.

{e['authored_theorems']} handwritten theorems and {e['authored_definitions']} definitions produce {e['public_declarations']} actual public namespace declarations ({e['public_theorems']} theorems, including {e['compiler_generated_theorems']} compiler-generated auxiliaries, and {e['public_definitions']} definitions). All {e['public_declarations']} were exported and axiom-checked. The actual type/body closure contains {e['closure_declarations']} declarations, with no unknown or unsafe nodes or disallowed axioms. Root axioms: `{e['root_axioms']}`.

The final replay completed {e['commands']} commands: current-source compilation, complete positive contract and actual extraction passed; three genuine wrong-target Lean compilations failed as intended. It resolved the imported root to its own fresh output olean. It checked {e['external_loaded_modules']} external modules ({e['inspected_loaded_modules']} modules including the root during inspection), {e['external_import_artifacts']} external olean/private/server/IR artifacts, and {e['runtime_binaries']} runtime binaries before/after, with exact stability. No previous author output is called independent evidence.

Across development and replay, {len(receipts)} recorded processes include {len(lean)} actual Lean invocations. There are {len(failed)} nonzero process receipts, including the three intentional mathematical negative controls; nonzero outcomes were not removed or reclassified as passes. Exact command/count scope is in `command-index.json` and `author-evidence.json`.

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

'''+ '\n'.join(rows)+'''

## New verifier replay

`round8-lean-frozen-inputs.zip` is the compact task-source replay package. It contains all scripts, source, exact contracts, negative controls, informal source snapshots, full environment hash bindings, attribution, and readback needed for a new verifier. Installed external Lean/Mathlib artifacts are reused; no precompiled local root is included. The durable failed/successful author logs remain separately in this directory to avoid copying a large redundant history into the input package.

Extract/copy into the verifier's own authorized directory and run `python3 -B /absolute/path/to/copied-package/replay.py /absolute/path/to/new-output`. The runner writes only to the new output and freshly compiles the copied current source. It reports execution only; the new verifier supplies its own semantic assessment and independence provenance. Check the archive hash and per-file bindings in `handoff-manifest.json`.
'''
(BASE/'REPORT.md').write_text(text)
with (BASE/'AGENTS.md').open('a') as f:
 f.write(f'- 2026-09-22: Final fresh replay {e["run_id"]} passed current-source compilation, exact nine-conjunct type, 47 actual declarations/axioms, 16,511-node closure, three genuine wrong-target failures and before/after import identity. Added full actual readback, author report and complete process index; maintained explicit exclusions and pending independent verification. Packaging only frozen inputs and compact final summaries; all raw failures remain here.\n')
# Package only replay inputs and explanatory handoff, without author olean/cache or repeated raw history.
names=list(freeze['files'])+['freeze.json','README.md','PUBLIC-READBACK.md','REPORT.md','author-evidence.json','command-index.json']
archive=BASE/'round8-lean-frozen-inputs.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:z.write(BASE/n,n)
with zipfile.ZipFile(archive) as z:
 if z.testzip() is not None:raise RuntimeError('Bad ZIP CRC')
 for n in names:
  if hashlib.sha256(z.read(n)).hexdigest()!=digest(BASE/n):raise RuntimeError('Packaged bytes differ '+n)
package_files={n:digest(BASE/n) for n in names}
# Bind all raw receipts and retained failed sources without making a huge archive.
raw={str(p.relative_to(BASE)):digest(p) for p in sorted(BASE.rglob('*')) if p.is_file() and
 any(str(p.relative_to(BASE)).startswith(pre) for pre in ['development/','exporter-smoke-','author-replay-','replay-launches/','freeze-history/'])}
write_json(BASE/'handoff-manifest.json',{'role':'author_handoff','independent_verification':'pending','source_sha256':e['source_sha256'],
 'archive':{'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'crc_and_member_hashes_checked':True},
 'package_files':package_files,'raw_evidence_files':raw,'final_run_id':e['run_id'],'task_agents_sha256':digest(BASE/'AGENTS.md')})
print(json.dumps({'source_sha256':e['source_sha256'],'final_run_id':e['run_id'],'processes':len(receipts),'lean_invocations':len(lean),'nonzero_processes':len(failed),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive),'raw_files':len(raw)},indent=2))
