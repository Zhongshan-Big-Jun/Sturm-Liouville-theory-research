from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,shutil,time
Root=Path('/mnt/f/LaTeX/BVE research'); Base=Path('/mnt/f/tools/math-audit-round4-20260921'); Author=Base/'lean-author'; Out=Base/'lean-replay'
def digest(P):
	with Path(P).open('rb') as F: return hashlib.file_digest(F,'sha256').hexdigest()
Source=Root/'lean-proof/SL/AuditRound4.lean'; Object=Out/'final/build/SL/AuditRound4.olean'
Logs=[]
for P in sorted((Out/'logs').glob('*.json')):
	R=json.loads(P.read_text()); Expected=1 if P.stem in ['06-WrongPrintedReduction','07-PerturbedTable'] else 0
	assert R['exit_code']==Expected and R['source_unchanged_during_run']
	assert R['stdout_sha256']==digest(P.with_suffix('.stdout.txt')) and R['stderr_sha256']==digest(P.with_suffix('.stderr.txt'))
	for Q,H in R['local_objects_before'].items(): assert R['local_objects_after'][Q]==H
	Logs.append({'record':str(P.relative_to(Out)),'exit_code':R['exit_code'],'sha256':digest(P)})
assert len(Logs)==11
Matches=[]
for Name in ['formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt','declarations.json']:
	assert (Out/'final'/Name).read_bytes()==(Author/'final'/Name).read_bytes(),Name
	Matches.append({'path':Name,'sha256':digest(Out/'final'/Name),'byte_identical_to_author':True})
Original=json.loads((Author/'final/loaded-modules.json').read_text()); Actual=json.loads((Out/'final/loaded-modules.json').read_text())
assert Original['module_count']==Actual['module_count']==3217
PathChanges=[]
for A,B in zip(Original['modules'],Actual['modules'],strict=True):
	assert A['module']==B['module']
	if A!=B:
		assert B['olean']==A['olean'].replace('lean-author','lean-replay'),(A,B)
		assert A['module'].startswith('SL.')
		PathChanges.append({'module':A['module'],'author':A['olean'],'coordinator':B['olean']})
assert len(PathChanges)==5
assert digest(Object)==digest(Author/'final/build/SL/AuditRound4.olean')
Manifest=json.loads((Author/'final/module-artifact-hashes.json').read_text()); Tasks=[]
for M in Manifest['modules']:
	for A in M['artifacts']:
		P=Path(A['path'].replace('/lean-author/','/lean-replay/'))
		Tasks.append((P,A['sha256'],A['bytes']))
Env=json.loads((Author/'environment.json').read_text())
Tasks += [(Path(A['path']),A['sha256'],A['bytes']) for A in Env['runtime_files']]
def check(T):
	P,H,Size=T; assert P.stat().st_size==Size and digest(P)==H,str(P)
	return {'path':str(P),'sha256':H,'bytes':Size}
Start=time.monotonic()
with ThreadPoolExecutor(max_workers=8) as Pool: Checked=list(Pool.map(check,Tasks))
(Out/'artifact-rehash.json').write_text(json.dumps({'files':Checked,'count':len(Checked),'duration_seconds':time.monotonic()-Start,'status':'PASS'},indent=2)+'\n')
(Out/'comparison-correction.json').write_text(json.dumps({'first_finalizer_status':'FAILED_AFTER_SUCCESSFUL_EXECUTIONS','reason':'A byte-equality assertion included loaded-modules.json, whose five local object paths necessarily change in a new output directory. Root/definition/declaration bytes matched. The revised comparison checks all names, the exact five permitted path substitutions and all artifact hashes; no source or proof was changed.','path_changes':PathChanges},indent=2)+'\n')
Result={'status':'PASS','scope':'Coordinator machine replay, not independent semantic verdict. Four restricted-import dependency bodies and new root rebuilt; same compiler and hashed package binaries. No full original broad-import build.','source_sha256':digest(Source),'object_sha256':digest(Object),'exports':Matches,'loaded_modules':3217,'module_artifacts_rehashed':12853,'runtime_files_rehashed':10,'expected_local_path_changes':PathChanges,'execution_records':Logs,'negative_controls':[{'name':'WrongPrintedReduction','exit_code':1},{'name':'PerturbedTable','exit_code':1}],'positive_controls_exit_code':0,'contract_check_exit_code':0}
(Out/'RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
Folder=Root/'research/artifacts/proof-audit-round4-20260921/lean/coordinator-replay'; Folder.mkdir(parents=True,exist_ok=False)
for P in Out.rglob('*'):
	if not P.is_file() or 'build' in P.relative_to(Out).parts: continue
	Q=Folder/P.relative_to(Out); Q.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(P,Q)
shutil.copyfile(Object,Folder/'root-AuditRound4.olean.bin')
shutil.copyfile(Base/'replay_lean.py',Folder/'replay_lean.py'); shutil.copyfile(Path(__file__),Folder/'finalize_lean_replay.py')
print('PASS: 11 executions; identical root and four exports; 3217 module names; 12853 artifact hashes plus10 runtime files.')
