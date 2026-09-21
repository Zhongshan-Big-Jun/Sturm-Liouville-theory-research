"""Bind the current author deliverables and verify named frozen source bytes."""
from pathlib import Path
import datetime, hashlib, json

Root=Path(__file__).resolve().parent
Inputs=json.loads((Root/'input_manifest.json').read_text())
ReadSet=[]
for Item in Inputs['inputs']:
	P=Path(Item['path'])
	Now=hashlib.sha256(P.read_bytes()).hexdigest()
	ReadSet.append({'path':str(P),'read_sha256':Item['sha256'],'current_sha256':Now,'unchanged':Now==Item['sha256'],'role':'frozen mathematical source' if ('/sources/' in str(P) and P.suffix!='.md') or '/submitted/' in str(P) else 'instruction input'})
for Item in Inputs.get('additional_inputs',[]):
	P=Path(Item['frozen_copy'])
	Now=hashlib.sha256(P.read_bytes()).hexdigest()
	ReadSet.append({'path':str(P),'original_path':Item['path'],'read_sha256':Item['sha256'],'current_sha256':Now,'unchanged':Now==Item['sha256'],'role':'locally frozen coordinator candidate'})
Required=[Item for Item in ReadSet if Item['role']!='instruction input']
if not all(Item['unchanged'] for Item in Required):
	raise RuntimeError('A mathematical read-set item changed; do not seal.')
Verification={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mathematical_inputs_unchanged':True,'comparisons':ReadSet,'scope':'read-set comparison only; no claim to have audited the full repository'}
(Root/'logs/frozen_input_verification.json').write_text(json.dumps(Verification,indent=2)+'\n')
Paths=sorted({P.relative_to(Root).as_posix() for P in Root.rglob('*') if P.is_file()} | {'CHANGED_PATHS.md','output_manifest.json'})
Lines=['# Created paths in this author task','', 'All paths below are relative to `/mnt/f/tools/math-audit-round8-20260922/sliver-author/`. No pre-existing files outside that directory were modified. Build products are syntax-validation artifacts, not independent mathematical certificates.','']
Lines += ['- `'+Name+'`' for Name in Paths]
(Root/'CHANGED_PATHS.md').write_text('\n'.join(Lines)+'\n')
Records=[]
for P in sorted(Root.rglob('*')):
	if not P.is_file() or P.name=='output_manifest.json':
		continue
	Data=P.read_bytes()
	Records.append({'path':P.relative_to(Root).as_posix(),'bytes':len(Data),'sha256':hashlib.sha256(Data).hexdigest()})
Manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(Root),'role':'author candidate; independent review pending','input_manifest_sha256':hashlib.sha256((Root/'input_manifest.json').read_bytes()).hexdigest(),'self_exclusion':'This manifest does not hash itself; all other current files are listed.','files':Records}
(Root/'output_manifest.json').write_text(json.dumps(Manifest,indent=2)+'\n')
print('Bound author files:',len(Records))
print('Mathematical read-set items unchanged:',len(Required))
print('Instruction-input changes:',[Item['path'] for Item in ReadSet if Item['role']=='instruction input' and not Item['unchanged']])
print('proof.md SHA-256:',hashlib.sha256((Root/'proof.md').read_bytes()).hexdigest())
print('sliver_t1_fragment.tex SHA-256:',hashlib.sha256((Root/'sliver_t1_fragment.tex').read_bytes()).hexdigest())
