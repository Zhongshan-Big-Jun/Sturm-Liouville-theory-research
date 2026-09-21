from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import importlib.util,json,hashlib,shutil,time
Root=Path('/mnt/f/LaTeX/BVE research');Base=Path('/mnt/f/tools/math-audit-round5-20260921');Author=Base/'lean-author';Out=Base/'lean-replay'
assert (Base/'lean-author-completion.json').exists()
Out.mkdir(exist_ok=False)
for Name in ['logs','attempts','final','build/SL']:(Out/Name).mkdir(parents=True,exist_ok=True)
Spec=importlib.util.spec_from_file_location('r5_author_runner',Author/'run_lean.py');Runner=importlib.util.module_from_spec(Spec);Spec.loader.exec_module(Runner);Runner.OUT=Out
Source=Root/'lean-proof/SL/AuditRound5.lean';Obj=Out/'build/SL/AuditRound5.olean'
assert Source.read_bytes()==(Author/'final/AuditRound5.lean').read_bytes()
assert Runner.run('01-version',[str(Runner.LEAN),'--version'])==0
assert Runner.run('02-fresh-root',[str(Runner.LEAN),'--root='+Runner.win(Runner.ROOT),'-o',Runner.win(Obj),Runner.win(Source)],[Source])==0
Probe=Out/'InspectAuditRound5.lean';Text=(Author/Probe.name).read_text();Old='F:/tools/math-audit-round5-20260921/lean-author/final/'
assert Text.count(Old)==1
Probe.write_text(Text.replace(Old,'F:/tools/math-audit-round5-20260921/lean-replay/final/'))
assert Runner.run('03-object-inspection',[str(Runner.LEAN),Runner.win(Probe)],[Probe,Source,Obj])==0
assert Runner.run('04-resolved-imports',[str(Runner.LEAN),'--deps',Runner.win(Probe)],[Probe,Source,Obj])==0
Deps=(Out/'logs/04-resolved-imports.stdout.txt').read_text();assert 'lean-replay' in Deps and 'AuditRound5.olean' in Deps
Controls=[]
for Name,Control,Expected in [('05-positive','PositiveControls',0),('06-negative','FalseHighSpanEquality',1)]:
	P=Out/(Control+'.lean');shutil.copyfile(Author/'controls'/P.name,P)
	Code=Runner.run(Name,[str(Runner.LEAN),Runner.win(P)],[P,Source,Obj]);assert Code==Expected
	Controls.append({'control':P.name,'actual_exit':Code,'expected_exit':Expected})
Contract=json.loads((Author/'positive-contract.json').read_text());P=Out/'ContractCheck.lean'
P.write_text('import SL.AuditRound5\nexample : '+Contract['expected_type']+' := SL.AuditRound5.local_algebra_root\n')
assert Runner.run('07-contract',[str(Runner.LEAN),Runner.win(P)],[P,Source,Obj])==0
Matches=[]
for Name in ['formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt','declarations.json']:
	assert (Out/'final'/Name).read_bytes()==(Author/'final'/Name).read_bytes(),Name
	Matches.append({'path':Name,'sha256':Runner.digest(Out/'final'/Name),'byte_identical_to_author':True})
A=json.loads((Author/'final/loaded-modules.json').read_text());B=json.loads((Out/'final/loaded-modules.json').read_text());assert A['module_count']==B['module_count']
Changes=[]
for X,Y in zip(A['modules'],B['modules'],strict=True):
	assert X['module']==Y['module']
	if X!=Y:
		assert X['module']=='SL.AuditRound5' and Y['olean']==X['olean'].replace('lean-author','lean-replay')
		Changes.append({'module':X['module'],'author':X['olean'],'replay':Y['olean']})
assert len(Changes)==1
Tasks=[]
for M in json.loads((Author/'final/module-artifact-hashes.json').read_text())['modules']:
	if M['module']=='SL.AuditRound5':continue
	for F in M['artifacts']:Tasks.append((Path(F['path']),F['sha256'],F['bytes'],'import'))
for F in json.loads((Author/'environment.json').read_text())['runtime_files']:Tasks.append((Path(F['path']),F['sha256'],F['bytes'],'runtime'))
def Check(Item):
	P,H,Size,Kind=Item;assert P.stat().st_size==Size and Runner.digest(P)==H,str(P)
	return {'path':str(P),'sha256':H,'bytes':Size,'kind':Kind}
Start=time.monotonic()
with ThreadPoolExecutor(max_workers=8) as Pool:Hashes=list(Pool.map(Check,Tasks))
RootObjects=[]
for P in sorted((Out/'build/SL').glob('AuditRound5.*')):RootObjects.append({'path':str(P),'sha256':Runner.digest(P),'bytes':P.stat().st_size})
(Out/'artifact-rehash.json').write_text(json.dumps({'status':'PASS','files':Hashes,'root_objects':RootObjects,'count':len(Hashes),'duration_seconds':time.monotonic()-Start},indent=2)+'\n')
Logs=[]
for P in sorted((Out/'logs').glob('*.json')):
	R=json.loads(P.read_text());assert R['source_unchanged_during_run'] and R['exit_code']==(1 if P.stem=='06-negative' else 0)
	for S in ['stdout','stderr']:assert R[S+'_sha256']==Runner.digest(P.with_suffix('.'+S+'.txt'))
	Logs.append({'path':str(P.relative_to(Out)),'exit_code':R['exit_code'],'sha256':Runner.digest(P)})
assert len(Logs)==7
Result={'status':'PASS','scope':'Coordinator fresh machine replay, not independent semantic approval. Real polynomial local algebra, no Sobolev or complex closure. New root compiled from unchanged live source; existing pinned Mathlib objects. No full Lake build.','platform':'Windows Lean4.31.0 PE invoked through WSL','source_sha256':Runner.digest(Source),'root_object_sha256':Runner.digest(Obj),'author_object_sha256':Runner.digest(Author/'build/SL/AuditRound5.olean'),'root_binary_identical_to_author':Obj.read_bytes()==(Author/'build/SL/AuditRound5.olean').read_bytes(),'declarations':len(json.loads((Out/'final/declarations.json').read_text())['declarations']),'exports':Matches,'loaded_modules':B['module_count'],'expected_path_changes':Changes,'import_artifacts_rehashed':sum(H['kind']=='import' for H in Hashes),'runtime_files_rehashed':sum(H['kind']=='runtime' for H in Hashes),'root_artifacts':RootObjects,'commands':Logs,'controls':Controls}
(Out/'RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
Folder=Root/'research/artifacts/proof-audit-round5-20260921/lean/coordinator-replay';Folder.mkdir(parents=True,exist_ok=False)
for P in sorted(Out.rglob('*')):
	if not P.is_file() or 'build' in P.relative_to(Out).parts:continue
	Q=Folder/P.relative_to(Out);Q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P,Q)
shutil.copyfile(Obj,Folder/'root-AuditRound5.olean.bin');shutil.copyfile(__file__,Folder/'replay_lean.py')
print(json.dumps({K:Result[K] for K in ['status','declarations','loaded_modules','import_artifacts_rehashed','runtime_files_rehashed','root_binary_identical_to_author']},indent=2))
