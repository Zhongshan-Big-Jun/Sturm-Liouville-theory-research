from pathlib import Path
import json,hashlib,shutil,subprocess
Root=Path('/mnt/f/LaTeX/BVE research');Base=Path('/mnt/f/tools/math-audit-round3-20260920');Out=Base/'lean-replay';Author=Base/'lean-author';Exports=Out/'bound-exports'
def sha(P): return hashlib.sha256(P.read_bytes()).hexdigest()
Object=Out/'final/build/SL/AuditRound3.olean';Source=Root/'lean-proof/SL/AuditRound3.lean'
for Name,Code in [('04-bound-export',0),('05-bound-deps',0),('06-bound-OldProductEquality',1),('07-bound-OldPerturbedDifference',1)]:
	Record=json.loads((Out/'logs'/(Name+'.json')).read_text());assert Record['exit_code']==Code and Record['source_unchanged_during_run']
	for When in ['before','after']: assert Record['source_sha256_'+When][str(Object)]==sha(Object)
	for Stream in ['stdout','stderr']: assert Record[Stream+'_sha256']==sha(Out/'logs'/(Name+'.'+Stream+'.txt'))
Final={}
for Name in ['declarations.json','formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt']:
	Raw=(Exports/Name).read_bytes();assert Raw==(Author/'final'/Name).read_bytes();Final[Name]=sha(Exports/Name)
Loaded=json.loads((Exports/'loaded-modules.json').read_text());Original=json.loads((Author/'final/loaded-modules.json').read_text())
Actual={R['module']:R['olean'] for R in Loaded['modules']};Expected={R['module']:R['olean'] for R in Original['modules']}
assert Actual.keys()==Expected.keys()
ObjectWin=subprocess.check_output(['wslpath','-w',str(Object)],text=True).strip()
assert Actual['SL.AuditRound3'].replace('\\','/').casefold()==ObjectWin.replace('\\','/').casefold()
assert all(Actual[K]==Expected[K] for K in Actual if K!='SL.AuditRound3')
Final['loaded-modules.json']=sha(Exports/'loaded-modules.json')
Result={'status':'PASS','scope':'The declaration/type/definition exports match original bytes. Loaded-module paths intentionally identify the separate replay root: only the SL.AuditRound3 path differs; all dependency paths agree. Supplemental runs bind root-object hashes before/after export and controls. Native --deps corroborates resolution. Dependency binaries were not rebuilt.','root_object':{'path':str(Object),'sha256':sha(Object)},'source_sha256':sha(Source),'exports':Final,'export_record':'logs/04-bound-export.json','resolved_import_record':'logs/05-bound-deps.json','negative_control_records':['logs/06-bound-OldProductEquality.json','logs/07-bound-OldPerturbedDifference.json'],'orchestration_correction':'The initial outer comparison demanded equality of loaded-module path inventories despite the separate output roots. It failed after the four successful native executions. The comparison here checks the distinct root path explicitly; no compiler success/failure was relabeled.'}
(Out/'BOUND-RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
Art=Root/'research/artifacts/proof-audit-round3-20260920/lean';Folder=Art/'bound-replay';Folder.mkdir(exist_ok=True)
for Name in ['InspectBound.lean','OldProductEquality.lean','OldPerturbedDifference.lean','BOUND-RESULT.json']:
	shutil.copyfile(Out/Name,Folder/Name)
shutil.copyfile(Object,Folder/'root-AuditRound3.olean.bin');shutil.copyfile(Exports/'loaded-modules.json',Folder/'loaded-modules.json')
for P in (Out/'logs').glob('*'):
	if P.name[:2] in ['04','05','06','07']:
		Q=Folder/'logs'/P.name;Q.parent.mkdir(exist_ok=True);shutil.copyfile(P,Q)
for Name in ['bind_lean_replay.py','finalize_bound_replay.py']: shutil.copyfile(Base/Name,Folder/Name)
print('PASS: current root object, true import resolution, exports and controls bound.')
