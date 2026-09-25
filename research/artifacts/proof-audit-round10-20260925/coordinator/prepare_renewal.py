from pathlib import Path
import sys,json,hashlib,difflib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_review as V
def sha(P):return hashlib.sha256(P.read_bytes()).hexdigest()
def save(P,D):P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
Cards=json.loads((O/'cards.json').read_text());Changed={X['location'] for X in Cards.values()}
Rows=[X for X in json.loads((O/'renewal-inspection.json').read_text())['new_invalid_releases'] if X['target']['location'] not in Changed]
if len(Rows)!=4:raise RuntimeError('Unexpected unchanged renewal set')
Inputs={};Claims={};Authors={'01a06f46-dd03-7c83-9267-32048412c359'};Identities=[]
for Row in Rows:
	Target=Row['target']
	if sha(R/Target['location'])!=Target['sha256']:raise RuntimeError('Unchanged card drift')
	Req=C.review_requirements(R,Row['revision'])
	for X in Req['inputs']:
		if X['path'] in Inputs and Inputs[X['path']].get('sha256')!=X['sha256']:raise RuntimeError('Conflicting binding')
		Inputs[X['path']]=X
	for X in Req['claims']:Claims[X['id']]=X
	Authors.update(Req['author_ids'])
	Identities.append(dict(target=Target,issue=Row['issue'],revision=Row['revision'],reason=Row['problem']['error']))
Extras=['docs/SL_gap_nge2_symmetry_local_proof.tex','docs/SL_fixed_n_supremum.tex','research/artifacts/proof-audit-round9-20260923/analytic-repair.md','docs/SL_gap_nge2_symmetry_recon.tex','tools/second-variation-weighted-eigenvalues.md',A.relative_to(R).as_posix()+'/before/docs/SL_gap_nge2_symmetry_recon.tex',A.relative_to(R).as_posix()+'/before/tools/second-variation-weighted-eigenvalues.md',A.relative_to(R).as_posix()+'/analytic-repair.md']
for N in Extras:Inputs.setdefault(N,dict(path=N,role='current-proof-or-changed-source-scope-comparison'))
Identity=dict(scope='Four unchanged exact cards need review because whole-packet inputs changed. No prior reviewer verdict is supplied as a premise.',unchanged=Identities,changed_inputs=['docs/SL_gap_nge2_symmetry_recon.tex','tools/second-variation-weighted-eigenvalues.md'])
save(A/'renewal-identities.json',Identity);save(O/'renewals.json',Rows)
Inputs['research/artifacts/proof-audit-round10-20260925/renewal-identities.json']=dict(path='research/artifacts/proof-audit-round10-20260925/renewal-identities.json',role='exact-identity-and-renewal-scope')
Claims['R10-unchanged-card-renewal']=dict(id='R10-unchanged-card-renewal',verification='analytic',statement='Independently reassess the four exact correction obligations on unchanged feynman-hellmann, gap-band-extremals, secular-chebyshev-jacobi-rootcount and bloch-band cards. Compare the supplied changed reconnaissance/second-variation passages with their before versions and inspect the relevant original mathematical derivations. The numerical indexing and seed corrections are not premises of the retained variational identity, structural reduction or prescribed balanced-candidate Jacobi/root/limit proofs. Verify exact assumptions and no scope expansion, without using old verdict labels or recertifying unrelated historical Green/M3/KP contents. Root count in the normalized balanced family is an analytic result, distinct from the general-purpose old grid scanner. Global O1/O2/G1 and finite-R uniqueness remain open.')
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=list(Claims.values()))
save(O/'renewal-review-spec.json',Spec);save(O/'renewal-review-packet.json',V.create_packet(R,Spec))
print('Renewal packet ready',len(Inputs),'inputs',len(Claims),'claims',flush=True)
