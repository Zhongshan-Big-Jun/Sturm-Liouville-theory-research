from pathlib import Path
import importlib.util,json,shutil,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Base=Path('/mnt/f/tools/math-audit-round3-20260920');Out=Base/'lean-replay';Author=Base/'lean-author'
Spec=importlib.util.spec_from_file_location('native_bound_runner',Author/'run_lean.py');Runner=importlib.util.module_from_spec(Spec);Spec.loader.exec_module(Runner);Runner.OUT=Out
Source=Root/'lean-proof/SL/AuditRound3.lean';Object=Out/'final/build/SL/AuditRound3.olean';Configs=[Root/'lean-proof'/N for N in ['lean-toolchain','lakefile.lean','lake-manifest.json']]
Exports=Out/'bound-exports';Exports.mkdir(exist_ok=False)
Old='F:/tools/math-audit-round3-20260920/lean-author/final/'
Probe=Out/'InspectBound.lean';Text=(Author/'InspectAuditRound3.lean').read_text();assert Text.count(Old)==1
Probe.write_text(Text.replace(Old,'F:/tools/math-audit-round3-20260920/lean-replay/bound-exports/'))
assert Runner.run('04-bound-export',[str(Runner.BIN/'lean.exe'),Runner.win_path(Probe)],[Probe,Source,Object]+Configs)==0
assert Runner.run('05-bound-deps',[str(Runner.BIN/'lean.exe'),'--deps',Runner.win_path(Probe)],[Probe,Source,Object]+Configs)==0
Deps=(Out/'logs/05-bound-deps.stdout.txt').read_text()
assert 'AuditRound3.olean' in Deps and 'lean-replay' in Deps
for Number,Name in [(6,'OldProductEquality'),(7,'OldPerturbedDifference')]:
	Control=Out/(Name+'.lean')
	assert Runner.run(f'{Number:02d}-bound-'+Name,[str(Runner.BIN/'lean.exe'),Runner.win_path(Control)],[Control,Source,Object]+Configs)==1
Final={}
for Name in ['declarations.json','formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt','loaded-modules.json']:
	Raw=(Exports/Name).read_bytes();assert Raw==(Author/'final'/Name).read_bytes(),Name
	Final[Name]=hashlib.sha256(Raw).hexdigest()
Result={'status':'PASS','scope':'Supplemental executions bind the consumed root object before/after export and both negative controls. --deps independently records its resolved import path. Dependency binaries were not rebuilt.','root_object':{'path':str(Object),'sha256':Runner.digest(Object)},'source_sha256':Runner.digest(Source),'exports':Final,'export_record':'logs/04-bound-export.json','resolved_import_record':'logs/05-bound-deps.json','negative_control_records':['logs/06-bound-OldProductEquality.json','logs/07-bound-OldPerturbedDifference.json']}
(Out/'BOUND-RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
Art=Root/'research/artifacts/proof-audit-round3-20260920/lean';Folder=Art/'bound-replay';Folder.mkdir(exist_ok=True)
for Name in ['InspectBound.lean','OldProductEquality.lean','OldPerturbedDifference.lean','BOUND-RESULT.json']:
	shutil.copyfile(Out/Name,Folder/Name)
shutil.copyfile(Object,Folder/'root-AuditRound3.olean.bin')
for P in (Out/'logs').glob('*'):
	if P.name[:2] in ['04','05','06','07']:
		Q=Folder/'logs'/P.name;Q.parent.mkdir(exist_ok=True);shutil.copyfile(P,Q)
shutil.copyfile(Author/'InspectAuditRound3.lean',Art/'InspectAuditRound3.lean')
print('Bound replay export, import resolution, compiled object and both negative controls archived.')
