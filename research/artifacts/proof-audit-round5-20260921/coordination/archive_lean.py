from pathlib import Path
import sys,json,shutil,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round5-20260921');Author=Out/'lean-author';Art='research/artifacts/proof-audit-round5-20260921/lean';Folder=Root/Art
assert (Out/'lean-author-completion.json').exists()
assert json.loads((Author/'FINAL_CHECKS.json').read_text())['status']=='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW'
Manifest=[]
for P in sorted(Author.rglob('*')):
	if not P.is_file():continue
	Rel=P.relative_to(Author)
	if any(N in Rel.parts for N in ['__pycache__','build']) or P.suffix in ['.olean','.ilean','.ir','.pyc','.private','.server']:continue
	Q=Folder/Rel;Q.parent.mkdir(parents=True,exist_ok=True)
	assert not Q.exists() or Q.read_bytes()==P.read_bytes(),Q
	shutil.copyfile(P,Q);Manifest.append({'path':str(Rel),'sha256':hashlib.sha256(Q.read_bytes()).hexdigest(),'bytes':Q.stat().st_size})
(Folder/'archive-manifest.json').write_text(json.dumps(Manifest,indent=2)+'\n')
Pins=Folder/'pins';Pins.mkdir(exist_ok=True)
for Name in ['lean-toolchain','lakefile.lean','lake-manifest.json']:shutil.copyfile(Root/'lean-proof'/Name,Pins/Name)
shutil.copyfile(Author/'build/SL/AuditRound5.olean',Folder/'root-AuditRound5.olean.bin')
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as R
Declarations=json.loads((Folder/'final/declarations.json').read_text())['declarations']
Packet=R.create_packet(Root,{'kind':'formal-readback','author_ids':['01a06f46-dd03-7c83-9267-32048412c359','01a0c22b-dabe-7f30-a5bd-08b48dae6ae3'],'inputs':[{'path':Art+'/final/'+Name,'role':Role} for Name,Role in [('formal-statements.txt','formal-statement'),('formal-statements-fully-explicit.txt','formal-statement'),('local-definition-closure.txt','definitions')]]+[{'path':Art+'/pins/'+Name,'role':'environment'} for Name in ['lean-toolchain','lakefile.lean','lake-manifest.json']],'claims':[{'id':D['declaration'],'declaration':D['declaration']} for D in Declarations]})
(Out/'readback-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
print('Archived',len(Manifest),'files,',sum(M['bytes'] for M in Manifest),'bytes; readback',len(Declarations),'declarations;',Packet['packet_sha256'])
