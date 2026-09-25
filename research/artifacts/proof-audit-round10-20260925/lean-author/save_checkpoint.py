from run import *
import re

CHECKPOINT = BASE / 'handoff-checkpoint'
CHECKPOINT.mkdir(exist_ok=False)
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
JOB_PATH = BASE / '.research-state/jobs/exact-root-02-durable.json'
JOB = json.loads(JOB_PATH.read_text())
shutil.copyfile(JOB_PATH, CHECKPOINT / 'exact-root-02-job.json')
shutil.copyfile(BASE / 'commands/exact-root-02/command.json', CHECKPOINT / 'exact-root-02-command.json')
SOURCE = PROJECT / 'AuditRound10.lean'
FROZEN = BASE / 'root-project/AuditRound10.lean'
assert SOURCE.read_bytes() == FROZEN.read_bytes()
CORE_RECORD = json.loads((BASE / 'commands/final-source-01/command.json').read_text())
assert CORE_RECORD['exit_code'] == 0 and CORE_RECORD['inputs_unchanged']
assert CORE_RECORD['inputs_after'][str(SOURCE)] == digest(SOURCE)
DECL_PATH = next((BASE / 'evidence/exact-root-02/lean-verification-runs').glob('*/declaration.json'))
DECL = json.loads(DECL_PATH.read_text())
assert DECL['comparison']['status'] == 'matched'
assert set(DECL['axioms']) <= {'propext','Classical.choice','Quot.sound'}
SUMMARY = []
for Label in ['runtime-version','development-01','development-02','development-03','final-source-01',
	'positive-refutations-01','positive-refutations-02','negative-flip-01','negative-reflection-01','negative-index-01',
	'print-main-01','print-controls-01','explicit-export-01','explicit-export-full-01','blind-source-01','exact-root-01']:
	RecordPath = BASE / 'commands' / Label / 'command.json'
	Record = json.loads(RecordPath.read_text())
	SUMMARY.append({'label':Label,'exit_code':Record['exit_code'],'seconds':Record['seconds'],
		'command_record':str(RecordPath.relative_to(BASE)),'record_sha256':digest(RecordPath)})
write_json(CHECKPOINT / 'completed-executions.json', SUMMARY)
NAMES = json.loads((BASE / 'declaration-names.json').read_text())
AXIOMS = {}
for Label in ['print-main-01','print-controls-01']:
	for Match in re.finditer(r"^'([^']+)' depends on axioms: (\[[^\n]*\])$", (BASE / 'commands' / Label / 'stdout.log').read_text(), re.M):
		AXIOMS[Match[1]] = {'raw':Match[0],'log':'commands/'+Label+'/stdout.log'}
assert set(AXIOMS) == set(NAMES['main']+NAMES['controls'])
write_json(CHECKPOINT / 'per-target-axioms.json', AXIOMS)
FULL = json.loads((BASE / 'formal-declarations-full.json').read_text())
for Entry in FULL:
	assert '⋯' not in Entry['type_explicit'] and '...' not in Entry['type_explicit']
PathList = [SOURCE,FROZEN,BASE/'root-contract.json',BASE/'root-exact-type.lean.txt',BASE/'root-clauses.json',
	BASE/'HUMAN-CONTRACT.md',BASE/'REPLAY.md',BASE/'formal-declarations-full.json',BASE/'declaration-names.json',
	BASE/'run.py',BASE/'verify_frozen.py',BASE/'launch_frozen.py',BASE/'frozen-root-inputs.json',BASE/'blind-transform.json',
	BASE/'first-root-failure-summary.json',BASE/'external-input-identities.json']
PathList += [P for P in (BASE/'formal-only').iterdir() if P.is_file()]
PathList += [PROJECT/Name for Name in ['lean-toolchain','lakefile.toml','lake-manifest.json','Counterexamples.lean',
	'NegativeFlip.lean','NegativeReflection.lean','NegativeIndex.lean','PrintAuditRound10.lean','PrintCounterexamples.lean',
	'ReadbackExportFull.lean']]
for Item in SUMMARY:
	Directory = BASE/'commands'/Item['label']
	PathList += [P for P in Directory.rglob('*') if P.is_file()]
CHECK = {
	'created_utc':NOW,'role':'author','scope':'frozen local formal interfaces; no proof expansion',
	'root_declaration':'AuditRound10.root','root_source':str(SOURCE), 'root_source_sha256':digest(SOURCE),
	'root_exact_type':'root-exact-type.lean.txt','root_contract':'root-contract.json',
	'direct_final_compile_exit':0,'blind_source_compile_exit':0,
	'negative_compile_exits':{'NegativeFlip.lean':1,'NegativeReflection.lean':1,'NegativeIndex.lean':1},
	'exact_opposite_counterexample_compile_exit':0,
	'declaration_extraction':{'path':str(DECL_PATH.relative_to(BASE)),'sha256':digest(DECL_PATH),
		'comparison_status':DECL['comparison']['status'],'axioms':DECL['axioms'],
		'overall_verifier_result':'pending final manifest at checkpoint time' if JOB['state']=='RUNNING' else JOB['state']},
	'long_job':{'id':JOB['job_id'],'state_at_checkpoint':JOB['state'],
		'child_pid':JOB.get('child_pid'),'child_identity':JOB.get('child_identity'),
		'supervisor_pid':JOB.get('supervisor_pid'),'supervisor_identity':JOB.get('supervisor_identity'),
		'live_record':str(JOB_PATH.relative_to(BASE)),
		'live_command':'commands/exact-root-02/command.json',
		'final_manifest':'evidence/exact-root-02/run-manifest.json'},
	'first_root_run':{'exit_code':1,'evidence_status':'stale','changed_inputs':['Counterexamples.lean','ReadbackExportFull.lean'],
		'interpretation':'not a pass; unchanged core compiled and exact type matched, but development project snapshot changed'},
	'blind_packet':'formal-only/packet.json','semantic_review':'coordinator to dispatch fresh readback and separate recompile/semantic check',
	'files':{str(P.relative_to(BASE)):{'sha256':digest(P),'bytes':P.stat().st_size} for P in sorted(set(PathList))}}
write_json(CHECKPOINT / 'checkpoint.json', CHECK)
ROWS = '\n'.join('| '+I['label']+' | '+str(I['exit_code'])+' |' for I in SUMMARY)
TEXT = f'''# Round10 author handoff checkpoint

Snapshot time: {NOW}. Author delivery only. No independent readback, independent recompilation/semantic review, or full-project build is claimed. The coordinator requested handoff within the existing scope while a long machine check may still be running; no proof was expanded in response.

## Direct blind packet

Send only `formal-only/packet.json` and its listed files to the fresh blind reader. Its main source is `formal-only/AuditRound10.lean`, retaining the actual imports, definitions, theorem names, declarations and proofs, with the single generation-marker comment removed. It has been separately compiled with exit 0. `formal-only/declarations-full.json` has the complete fully explicit declaration types and definition bodies; the ordinary readable variant can suppress proof terms. `formal-only/print-and-axioms.log` is the actual per-named-declaration #print and #print axioms output. `formal-only/environment.json` records the real pinned Lean executable, package versions and search path. Do not give the blind reader HUMAN-CONTRACT.md or this author explanation.

## Current precise target

`AuditRound10.root` in `project/AuditRound10.lean`, byte-identical to frozen `root-project/AuditRound10.lean`. Source SHA-256: `{digest(SOURCE)}`. The full literal conjunction type is in `root-exact-type.lean.txt` and `root-contract.json`; individual clauses are in `root-clauses.json`. The separate natural-language per-target contract is `HUMAN-CONTRACT.md` for the later comparison reviewer. This conjunction covers actual coordinate reversal, derived linear projection/reflection/Euclidean dot-product laws and the explicitly conditional IVT phase/index interface. It does not assert a formalized Sturm theory or a verified executable enumerator.

## Actual completed execution

The final core source compiled with exit 0; the comment-stripped blind source compiled with exit 0. All three false mathematical controls were actually rejected with exit 1 and False remaining. Counterexamples.lean proves their exact negations and compiled with exit 0. All requested named #print/#print axioms commands and the full structured exporter completed. The extracted root type matches the literal contract; transitive axioms are propext, Classical.choice, Quot.sound. Compiler evidence and a root-extraction match are separate from the unfinished overall fresh-evidence receipt.

| Command | Actual exit |
| --- | --- |
{ROWS}

Development-01, development-03 and positive-refutations-01 are retained author errors; their snapshots and full logs show the exact fixes. Exact-root-01 returned 1 with stale evidence because Counterexamples.lean changed and ReadbackExportFull.lean was added during its project-wide snapshot. That first run is not a pass. The ongoing successor uses a separate frozen minimal project; its source must remain unchanged.

## Long machine job and continuation

- Job: `{JOB['job_id']}`. State at this timestamp: `{JOB['state']}`.
- Supervisor PID/identity: `{JOB.get('supervisor_pid')}` / `{JOB.get('supervisor_identity')}`.
- Child PID/identity: `{JOB.get('child_pid')}` / `{JOB.get('child_identity')}`.
- Live state: `.research-state/jobs/exact-root-02-durable.json`.
- Actual command, input snapshot and exit: `commands/exact-root-02/command.json`; complete stdout/stderr alongside it.
- Final original-verifier result, once materialized: `evidence/exact-root-02/run-manifest.json`. Do not infer pass from dispatch, zero Lean subcommand exits or file existence alone; read final flags, evidence status and terminal process state.
- At this checkpoint, all Lean subprocesses in the second run had returned 0, declaration comparison was matched, and the original verifier was finishing its environment/freshness evidence. No second overall pass is asserted here.
- An already-running local completion waiter may write REPORT.md, author-result.json and handoff-manifest.json after exact-root-02 actually ends successfully. Those are later author-side observations; this checkpoint and its frozen source/contract files remain the timestamped handoff. If the verifier fails, it leaves the failed run intact and withholds that success report.

`REPLAY.md` contains exact non-overwriting author-side entry points. To start a new root replay against the frozen inputs use `python3 -B launch_frozen.py NEW_LABEL`, or `python3 -B verify_frozen.py NEW_LABEL` in the foreground, from this directory. Do not restart the running job simply because its final report is not yet present. The coordinator's fresh second compilation and semantic check should use their own output directory and preserve these author artifacts.

## Remaining scope

Independent blind readback and the second independent compilation/semantic comparison are assigned to the coordinator. Phase continuity, strict increase and valid per-index brackets remain explicit assumptions. Indices can skip levels; no coverage of every natural level follows unless the caller chooses consecutive indices and supplies those brackets. No phase ODE/lift, Sturm operator, spectral identification, interval arithmetic, numerical solver termination/correctness, interface feasibility after clipping or global symmetry theorem is claimed. All author writes are under formal-author; no project, old evidence, plugin or commit was changed.
'''
(BASE/'HANDOFF.md').write_text(TEXT)
write_json(CHECKPOINT/'handoff-document.json',{'path':'HANDOFF.md','sha256':digest(BASE/'HANDOFF.md')})
with (BASE/'AGENTS.md').open('a') as File:
	File.write('\n- 2026-09-25. User steering: main software implementation/CLI recalculation is complete and isolated software review is running; complete the existing formal handoff without expanding proofs, leaving independent blind/readback and second recompile/semantic review to the coordinator. Saved HANDOFF.md and handoff-checkpoint with byte-frozen source/definitions/declarations/contracts, completed real compiler/negative-control outcomes, exact root and live durable job identity. The second overall verifier status is recorded as observed, not promoted before completion.\n')
print(json.dumps({K:CHECK[K] for K in ['created_utc','root_declaration','root_source_sha256','long_job']},ensure_ascii=False,indent=2))
