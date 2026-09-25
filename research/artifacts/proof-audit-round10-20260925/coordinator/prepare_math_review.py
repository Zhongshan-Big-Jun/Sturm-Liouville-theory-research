from pathlib import Path
import sys,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A='research/artifacts/proof-audit-round10-20260925'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_review as V
def save(P,D):P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
Baseline=json.loads((O/'baseline.json').read_text());Cards=json.loads((O/'cards.json').read_text());Inspection=json.loads((O/'renewal-inspection.json').read_text())
Coord='01a06f46-dd03-7c83-9267-32048412c359'
Done=json.loads((O/'revisions.json').read_text()) if (O/'revisions.json').exists() else []
for Name,New in Cards.items():
	Entry=next(X for X in Inspection['current_blocked'] if X['target']['location']==New['location'])
	for Issue in Entry['state']['issues']:
		if any(X['name']==Name and X['issue']==Issue for X in Done):continue
		Old=dict(location=New['location'],sha256=Baseline['tracked'][New['location']])
		Result=C.propose_revision(R,Issue,Old,dict(location=New['location'],sha256=New['sha256']),Coord,
			'Round10 corrects numerical-support scope and reflection labels, with retained earlier analytic repairs. Shared roots are indexed by a continuous lift before positional refinement; -J is not a projector; the old reversal-odd antigrid preserves physical symmetry. No G1/Hessian/global conclusion follows. Prior exact analytic passages and assumptions are retained, and source pointers are refreshed. Scope mathematics separately from independent actual program acceptance.')
		Done.append(dict(name=Name,issue=Issue,revision=Result['revision_id'],target=dict(location=New['location'],sha256=New['sha256']),result=Result));save(O/'revisions.json',Done);print('Revision',Name,Issue[:8],flush=True)
Inputs={};Claims={};Authors={Coord}
for X in Done:
	Req=C.review_requirements(R,X['revision']);save(O/(X['revision']+'-requirements.json'),Req)
	for Q in Req['inputs']:
		if Q['path'] in Inputs and Inputs[Q['path']].get('sha256')!=Q['sha256']:raise RuntimeError('Conflicting exact binding')
		Inputs[Q['path']]=Q
	for Q in Req['claims']:Claims[Q['id']]=Q
	Authors.update(Req['author_ids'])
Extras=[A+'/analytic-repair.md',A+'/actual-source-failure.json',A+'/submitted/analytic_notes.md',A+'/before/docs/SL_gap_nge2_symmetry_recon.tex','docs/SL_gap_nge2_symmetry_recon.tex','docs/SL_gap_nge2_symmetry_local_proof.tex','research/artifacts/proof-audit-round9-20260923/analytic-repair.md']
for Name in Cards:
	Extras.append(A+'/before/tools/'+Name+'.md')
for N in Extras:Inputs.setdefault(N,dict(path=N,role='proof-or-before-after-scope-comparison'))
ExtraClaims=[
	dict(id='R10-phase-indexing',verification='analytic',statement='Independently verify S1-S4: the four lower-root obstruction, positive piecewise constant Dirichlet problem, continuous lifted scaled phase, positive frequency derivative across fixed interfaces, zero and infinite limits, exact one-based eigenvalue identity, density comparison brackets, half-turn preserving block maps, final local endpoint coordinate and its identical indexed roots. Do not assume the principal angle alone keeps the winding. Judge the mathematical indexing algorithm and safeguarded index contract, not arbitrary-precision or interval correctness of software; program execution has a separate fresh review.'),
	dict(id='R10-geometric-sectors',verification='analytic',statement='Verify geometric R(x)=1-Jx, derivative -J, genuine preserve/break projectors, eigenspaces, complementarity and orthogonality. Check the original assignment -J is not a projector, the old explicit antisymmetric concatenation and antigrid preserve physical symmetry, and feasibility/actual coordinate round-trip requirements. Check labels refer only to initial seeds, not optimizer trajectories. Check the document corrects the column-state transfer order to P_new*M_old without inventing a historical-code diagnosis.'),
	dict(id='R10-card-and-document-scope',verification='analytic',statement='Compare all four before/current cards and the reconnaissance TeX. Confirm scoped numerical-support withdrawal and preserved independent analytic repairs, with no inference that every R4 table was wrong or that absence of an observed asymmetric root proves uniqueness. Reassess each exact correction obligation from its issue evidence and current scoped content; preexisting identities outside this repair retain their explicitly limited original scope, not a new whole-proof certification. No new left-definite/Riesz theorem, global G1 or interval enumeration certificate is claimed. Check current source hashes and actual summaries, not just titles or counts.')]
for Q in ExtraClaims:Claims[Q['id']]=Q
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=list(Claims.values()))
save(O/'math-review-spec.json',Spec);save(O/'math-review-packet.json',V.create_packet(R,Spec))
print('Math packet ready',len(Inputs),'inputs',len(Claims),'claims',flush=True)
