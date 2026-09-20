from pathlib import Path
import importlib.util,json,hashlib,shutil
Root=Path('/mnt/f/LaTeX/BVE research'); Base=Path('/mnt/f/tools/math-audit-round4-20260921'); Author=Base/'lean-author'; Out=Base/'lean-replay'
Out.mkdir(exist_ok=False); (Out/'logs').mkdir(); (Out/'final/build/SL').mkdir(parents=True)
Spec=importlib.util.spec_from_file_location('round4_native_runner',Author/'run_lean.py'); Runner=importlib.util.module_from_spec(Spec); Spec.loader.exec_module(Runner); Runner.OUT=Out
Source=Root/'lean-proof/SL/AuditRound4.lean'; Configs=[Root/'lean-proof'/N for N in ['lean-toolchain','lakefile.lean','lake-manifest.json']]
assert Source.read_bytes()==(Author/'final/AuditRound4.lean').read_bytes()
Adapt=json.loads((Author/'DEPENDENCY_ADAPTATION.json').read_text())
for Row in Adapt['files']:
	Original=Path(Row['original']); Copy=Path(Row['copy'])
	assert Runner.digest(Original)==Row['original_sha256'] and Runner.digest(Copy)==Row['copy_sha256']
	assert Original.read_text().split('\n',1)[1]==Copy.read_text().split(Adapt['replacement_header']+'\n',1)[1]
	Target=Out/'dependency-src/SL'/Copy.name; Target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(Copy,Target)
	Object=Out/'final/build/SL'/(Copy.stem+'.olean')
	assert Runner.run('01-dependency-'+Copy.stem,[str(Runner.BIN/'lean.exe'),'--root='+Runner.win_path(Out/'dependency-src'),'-o',Runner.win_path(Object),Runner.win_path(Target)],[Target,Original]+Configs)==0
Object=Out/'final/build/SL/AuditRound4.olean'
assert Runner.run('02-fresh-root',[str(Runner.BIN/'lean.exe'),'-o',Runner.win_path(Object),'SL/AuditRound4.lean'],[Source]+Configs)==0
Inspection=(Author/'InspectAuditRound4.lean').read_text(); Old='F:/tools/math-audit-round4-20260921/lean-author/final/'
assert Inspection.count(Old)==1
Probe=Out/'InspectAuditRound4.lean'; Probe.write_text(Inspection.replace(Old,'F:/tools/math-audit-round4-20260921/lean-replay/final/'))
assert Runner.run('03-object-inspection',[str(Runner.BIN/'lean.exe'),Runner.win_path(Probe)],[Probe,Source,Object]+Configs)==0
assert Runner.run('04-resolved-imports',[str(Runner.BIN/'lean.exe'),'--deps',Runner.win_path(Probe)],[Probe,Source,Object]+Configs)==0
Deps=(Out/'logs/04-resolved-imports.stdout.txt').read_text(); assert 'lean-replay' in Deps and 'AuditRound4.olean' in Deps
Controls=[]
for N,Name,Expected in [(5,'PositiveControls',0),(6,'WrongPrintedReduction',1),(7,'PerturbedTable',1)]:
	Target=Out/(Name+'.lean'); shutil.copyfile(Author/'controls'/(Name+'.lean'),Target)
	Code=Runner.run(f'{N:02d}-'+Name,[str(Runner.BIN/'lean.exe'),Runner.win_path(Target)],[Target,Source,Object]+Configs)
	assert Code==Expected
	Controls.append({'name':Name,'exit_code':Code,'expected_exit':Expected})
Contract=Out/'ContractChecks.lean'; shutil.copyfile(Author/'ContractChecks.lean',Contract)
assert Runner.run('08-contract',[str(Runner.BIN/'lean.exe'),Runner.win_path(Contract)],[Contract,Source,Object]+Configs)==0
Matches=[]
for Name in ['formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt','declarations.json','loaded-modules.json']:
	Raw=(Out/'final'/Name).read_bytes(); assert Raw==(Author/'final'/Name).read_bytes(),Name
	Matches.append({'path':Name,'sha256':hashlib.sha256(Raw).hexdigest(),'byte_identical_to_author':True})
assert Object.read_bytes()==(Author/'final/build/SL/AuditRound4.olean').read_bytes()
Result={'status':'PASS','scope':'Coordinator machine replay, not independent semantic review. Four restricted-import dependencies and new root rebuilt from exact source bodies; same compiler, existing pinned package binaries. No full original broad-import build.','source_sha256':Runner.digest(Source),'object_sha256':Runner.digest(Object),'exports':Matches,'controls':Controls}
(Out/'RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
Folder=Root/'research/artifacts/proof-audit-round4-20260921/lean/coordinator-replay'; Folder.mkdir(parents=True,exist_ok=False)
for P in Out.rglob('*'):
	if not P.is_file() or 'build' in P.relative_to(Out).parts: continue
	Q=Folder/P.relative_to(Out); Q.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(P,Q)
shutil.copyfile(Object,Folder/'root-AuditRound4.olean.bin')
shutil.copyfile(Path(__file__),Folder/'replay_lean.py')
print(json.dumps(Result,indent=2))
