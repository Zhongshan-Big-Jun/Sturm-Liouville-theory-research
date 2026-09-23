from pathlib import Path
import sys,json,hashlib,difflib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_review as V
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
Rows=json.loads((O/'renewal-inspection.json').read_text())['new_invalid_releases']
if len(Rows)!=22 or any('docs/SL_spectral_topics_summary.tex' not in r['problem']['error'] for r in Rows):raise RuntimeError('Unexpected renewal set')
Store=C.load_store(R);Inputs={};Claims={};Authors={'01a06f46-dd03-7c83-9267-32048412c359'};Packets={};Same=[]
for Row in Rows:
	Target=Row['target']
	if sha(R/Target['location'])!=Target['sha256']:raise RuntimeError('Renewal card changed')
	Req=C.review_requirements(R,Row['revision'])
	for X in Req['inputs']:
		if X['path'] in Inputs and Inputs[X['path']].get('sha256')!=X['sha256']:raise RuntimeError('Conflicting binding')
		Inputs[X['path']]=X
	for X in Req['claims']:Claims[X['id']]=X
	Authors.update(Req['author_ids'])
	Bundle=Row['old_bundle'];PacketPath=json.loads((R/Bundle/'dispatch.json').read_text())['packet'];Packets[PacketPath]=Bundle
for PacketPath,Bundle in Packets.items():
	Packet=json.loads((R/PacketPath).read_text());Authors.update(Packet['author_ids']);Changes=[]
	for Name,Info in Packet['inputs'].items():
		Frozen=(R/PacketPath).parent/Info['snapshot'];Current=sha(R/Name)
		if sha(Frozen)!=Info['sha256']:raise RuntimeError('Old snapshot changed '+Name)
		if Current!=Info['sha256']:Changes.append(Name)
		else:Same.append(dict(path=Name,sha256=Current,prior_packet=PacketPath))
		Inputs.setdefault(Name,dict(path=Name,role='unchanged-prior-proof-or-evidence'))
	if Changes!=['docs/SL_spectral_topics_summary.tex']:raise RuntimeError('Unexpected changed prior input '+str(Changes))
	for Name in [PacketPath,Bundle+'/report.json',Bundle+'/dispatch.json',Bundle+'/spawn.json',Bundle+'/receipt.json']:Inputs.setdefault(Name,dict(path=Name,role='historical-review-provenance-not-current-approval'))
Old=A/'before/docs/SL_spectral_topics_summary.tex';New=R/'docs/SL_spectral_topics_summary.tex'
Delta=''.join(difflib.unified_diff(Old.read_text().splitlines(True),New.read_text().splitlines(True),fromfile='round9 baseline summary',tofile='round9 corrected summary'))
(A/'renewal-summary.diff').write_text(Delta)
Identity=dict(cause='Only B3 physical secular normalization and balanced candidate status passages changed in the whole summary. Twelve existing cards retain exactly their prior bytes and proof premises. Twenty-two review obligations need fresh renewal because prior packets bound the entire summary.',unchanged_bindings=Same,prior_packets=list(Packets),old_summary_sha256=sha(Old),new_summary_sha256=sha(New),renewals=Rows)
save(A/'renewal-identities.json',Identity);save(O/'renewals.json',Rows)
for P in [Old,New,A/'renewal-summary.diff',A/'renewal-identities.json']:Inputs.setdefault(P.relative_to(R).as_posix(),dict(path=P.relative_to(R).as_posix(),role='section-diff-and-identity-evidence'))
Claims['R9-unchanged-card-renewal']=dict(id='R9-unchanged-card-renewal',verification='analytic',statement='Independently reassess the 22 listed correction obligations on 12 unchanged cards (eight left-definite and four INF-limit). Inspect their exact statements, dependency scope and supplied original mathematical proofs, not verdict labels alone. All card and proof bytes remain as in the prior approved packets; their sole changed input is the B3 passages in the whole summary. Verify by source comparison and mathematical reading that these passages are not premises of the retained results and introduce no scope expansion. Renewal is limited to continued applicability of these unchanged scoped repairs, not full recertification of all historical results or new Lean status. The withdrawn original left-definite family stays withdrawn. New B3 normalization and candidate results undergo a separate review; do not use their correctness as a premise of these unrelated old claims.')
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=list(Claims.values()))
save(O/'renewal-review-spec.json',Spec);Result=V.create_packet(R,Spec);save(O/'renewal-review-packet.json',Result)
print('Prepared',len(Inputs),'inputs',len(Claims),'obligations',len(Packets),'prior packets',flush=True)
