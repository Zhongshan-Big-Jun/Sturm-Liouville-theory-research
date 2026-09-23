from pathlib import Path
import hashlib,json,shutil,zipfile
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923';S=O/'lean-author';D=A/'lean-author'
def sha(P):
	with P.open('rb') as F:return hashlib.file_digest(F,'sha256').hexdigest()
def save(P,V):P.write_text(json.dumps(V,ensure_ascii=False,indent=2)+'\n')
H=json.loads((S/'handoff-manifest.json').read_text())
for N,V in H['files'].items():
	if sha(S/N)!=V:raise RuntimeError('Author handoff mismatch '+N)
if D.exists():raise RuntimeError('Archive already exists; inspect before resuming')
D.mkdir(parents=True)
Rows=[]
with zipfile.ZipFile(D/'raw-evidence.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as Z:
	for P in sorted(S.rglob('*')):
		if not P.is_file() or '__pycache__' in P.parts or P.suffix=='.pyc':continue
		N=P.relative_to(S).as_posix();Rows.append(dict(path=N,sha256=sha(P),size=P.stat().st_size));Z.write(P,N)
with zipfile.ZipFile(D/'raw-evidence.zip') as Z:
	if Z.testzip() is not None:raise RuntimeError('Archive CRC failure')
	for X in Rows:
		if hashlib.sha256(Z.read(X['path'])).hexdigest()!=X['sha256']:raise RuntimeError('Archive byte mismatch')
for N in ['AGENTS.md','REPORT.md','HUMAN-CONTRACT.md','handoff-manifest.json','author-result.json','candidate-freeze.json','readonly-postcheck.json','positive-contract.json','author_runner.py','replay.py','launch_replay.py','project/AuditRound9.lean','project/ConditionalRound9.lean','project/lean-toolchain','project/lake-manifest.json','project/lakefile.toml','controls/missing-target.json','controls/unproved-premise.json','controls/wrong-type.json']:
	P=D/N;P.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/N,P)
save(D/'archive-manifest.json',dict(status='EXACT_AUTHOR_ARCHIVE_NOT_INDEPENDENT_APPROVAL',archive='raw-evidence.zip',archive_sha256=sha(D/'raw-evidence.zip'),files=Rows,comment='The archive preserves all author evidence and failures byte for byte. Selected small navigation/replay files are also exposed; no original author evidence was deleted.'))
Target=R/'lean-proof/SL/AuditRound9.lean'
if Target.exists():raise RuntimeError('Existing new Lean source')
shutil.copyfile(S/'project/AuditRound9.lean',Target)
Attrs=R/'lean-proof/SL/.gitattributes';Old=Attrs.read_bytes();Line=b'AuditRound9.lean -text\n'
if Line not in Old:Attrs.write_bytes(Old+(b'\n' if Old and not Old.endswith(b'\n') else b'')+Line)
F=A/'formal-blind';F.mkdir()
for Src,Dest in [('declarations-all.json','declarations.json'),('AuditRound9.lean','AuditRound9.lean'),('environment.json','environment.json'),('lean-toolchain','lean-toolchain')]:shutil.copyfile(S/'formal-only'/Src,F/Dest)
Decl=json.loads((F/'declarations.json').read_text())
Spec=dict(kind='formal-readback',author_ids=['01a06f46-dd03-7c83-9267-32048412c359','01a0cbe7-a5ba-7be1-9170-4484e929436b'],inputs=[dict(path=str((F/N).relative_to(R)),role=Role) for N,Role in [('declarations.json','formal-statement'),('AuditRound9.lean','definitions'),('environment.json','environment'),('lean-toolchain','environment')]],claims=[dict(id=X['name'],declaration=X['name']) for X in Decl])
save(O/'formal-readback-spec.json',Spec)
save(A/'lean-integration.json',dict(source_sha256=sha(Target),old_SL_sources_count=49,new_source=str(Target.relative_to(R)),author_handoff_manifest_sha256=sha(S/'handoff-manifest.json'),author_archive_sha256=sha(D/'raw-evidence.zip'),all_archived_files=len(Rows),blind_claims=len(Decl)))
print('Lean integrated; author files',len(Rows),'archive bytes',(D/'raw-evidence.zip').stat().st_size,'blind declarations',len(Decl),flush=True)
