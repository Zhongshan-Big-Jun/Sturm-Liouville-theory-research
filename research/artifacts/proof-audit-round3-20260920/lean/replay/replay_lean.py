from pathlib import Path
import importlib.util,json,shutil,hashlib,sys
Root=Path('/mnt/f/LaTeX/BVE research');Base=Path('/mnt/f/tools/math-audit-round3-20260920')
Author=Base/'lean-author';Out=Base/'lean-replay'
Out.mkdir(exist_ok=True);(Out/'logs').mkdir(exist_ok=True);(Out/'final/build/SL').mkdir(parents=True,exist_ok=True)
Spec=importlib.util.spec_from_file_location('round3_native_runner',Author/'run_lean.py')
Runner=importlib.util.module_from_spec(Spec);Spec.loader.exec_module(Runner);Runner.OUT=Out
Source=Root/'lean-proof/SL/AuditRound3.lean';Configs=[Root/'lean-proof'/Name for Name in ['lean-toolchain','lakefile.lean','lake-manifest.json']]
assert Source.read_bytes()==(Author/'final/AuditRound3.lean').read_bytes()
Object=Out/'final/build/SL/AuditRound3.olean'
assert Runner.run('01-fresh-build',[str(Runner.BIN/'lean.exe'),'-o',Runner.win_path(Object),'SL/AuditRound3.lean'],[Source]+Configs)==0
Inspection=(Author/'InspectAuditRound3.lean').read_text()
Old='F:/tools/math-audit-round3-20260920/lean-author/final/'
assert Inspection.count(Old)==1
(Out/'InspectAuditRound3.lean').write_text(Inspection.replace(Old,'F:/tools/math-audit-round3-20260920/lean-replay/final/'))
assert Runner.run('02-inspection',[str(Runner.BIN/'lean.exe'),Runner.win_path(Out/'InspectAuditRound3.lean')],[Out/'InspectAuditRound3.lean',Source]+Configs)==0
Controls=[]
for Name in ['OldProductEquality','OldPerturbedDifference']:
	shutil.copyfile(Author/'controls'/(Name+'.lean'),Out/(Name+'.lean'))
	Code=Runner.run('03-'+Name,[str(Runner.BIN/'lean.exe'),Runner.win_path(Out/(Name+'.lean'))],[Out/(Name+'.lean'),Source]+Configs)
	assert Code!=0, 'old false formula was accepted'
	Controls.append({'name':Name,'exit_code':Code})
Matches=[]
for Name in ['formal-statements.txt','formal-statements-fully-explicit.txt','local-definition-closure.txt','declarations.json']:
	Raw=(Out/'final'/Name).read_bytes();Same=Raw==(Author/'final'/Name).read_bytes();assert Same,Name
	Matches.append({'path':Name,'exact_author_export_match':Same,'sha256':hashlib.sha256(Raw).hexdigest()})
Result={'status':'PASS','role':'coordinator machine replay, not independent semantic verdict','source_sha256':hashlib.sha256(Source.read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(Object.read_bytes()).hexdigest(),'exports':Matches,'negative_controls':Controls}
(Out/'RESULT.json').write_text(json.dumps(Result,indent=2)+'\n')
print(json.dumps(Result,indent=2))
