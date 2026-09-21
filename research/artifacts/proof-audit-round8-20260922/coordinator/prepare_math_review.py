from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A='research/artifacts/proof-audit-round8-20260922'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as V
B=json.loads((O/'baseline.json').read_text());Cards=json.loads((O/'cards.json').read_text());Done=json.loads((O/'revisions.json').read_text()) if (O/'revisions.json').exists() else []
Coord='01a06f46-dd03-7c83-9267-32048412c359'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for name,new in Cards.items():
	if any(x['name']==name for x in Done):continue
	old=dict(location=new['location'],sha256=B['tracked'][new['location']])
	result=C.propose_revision(R,'round8-inf-limit-certificates',old,dict(location=new['location'],sha256=new['sha256']),Coord,'R8-F01-F05 and P01-P03 scoped repair: exact root image and scalar certificate; continuous global phase/sliver proof; elementary positive-margin A doubleprime; conditional branches and fixed-u 1/R rate. Historical runs remain evidence, not current certification.')
	Done.append(dict(name=name,result=result));save(O/'revisions.json',Done);print('REVISION',name,result['revision_id'],flush=True)
Inputs={};Claims=[];Authors={Coord}
for d in Done:
	req=C.review_requirements(R,d['result']['revision_id']);save(O/(d['name']+'-requirements.json'),req)
	for x in req['inputs']:
		if x['path'] in Inputs and Inputs[x['path']]['sha256']!=x['sha256']:raise RuntimeError('Conflicting binding')
		Inputs[x['path']]=x
	Claims+=req['claims'];Authors.update(req['author_ids'])
for n in ['sliver-author','certificate-author','lean-author']: Authors.add(json.loads((O/(n+'-spawn.json')).read_text())['result']['agent_id'])
extras=['docs/SL_gap_n1_inf_limit_proof.tex','docs/SL_gap_n1_proof.tex','docs/SL_spectral_topics_summary.tex',A+'/certificate/certificate.py',A+'/certificate/results.json',A+'/certificate/README.md',A+'/submitted/analytic_repairs.md',A+'/submitted/proof_audit_round8_20260922.md',A+'/direct-propagation-findings.md',A+'/literature/dlmf-equation-extract.md']
for n in extras:Inputs.setdefault(n,dict(path=n,role='current-source-or-evidence'))
Claims += [
dict(id='R8-phase',verification='analytic',statement='Verify the actual even ground and odd first-excited mode selection for the full symmetric Dirichlet string, pole-free matching equations, spatial positivity/root indexing, global domains and conditional theta2>pi/2. Verify all delta brackets, z2<pi/8 and theta2<a under R>=1500,w>=2, the R1600/u1/1600 counterexample, and arctan limit.'),
dict(id='R8-A-doubleprime',verification='analytic',statement='Independently verify the complete new continuous A-doubleprime proof, every division and strict inequality: alpha, d1>4alpha, elementary r(z)<7z/20, B(t)<2(t sin t)^2<=8 using exact sin2/cos2 Taylor bounds and concavity, retaining D0-d, d2<3alpha, and G>Dbar+ell/(Ru^3). No sampled graph may replace a universal proof.'),
dict(id='R8-continuous-sliver',verification='analytic',statement='Independently verify the continuous unwrapped phase Phi and its derivative, actual first two mode roots, k1 bound and separation, and G>=pi^2/[2epsilon(w+ell)(w+epsilon*ell)] for every R>=1,0<u<1/2. Verify it yields G>15pi^2/4>3pi^2 and >25 on the whole R>=1500,0<w<=2 domain, including arbitrarily small positive w, w=1/2,w=2, curved B/D strips and R-infinity tail. Do not assume old grid coverage or wrong global odd branch.'),
dict(id='R8-T2-T3',verification='analytic',statement='Check the retained complete T2 sign chain identities, monotonicity, unique minimizer and both endpoint limits. Check exact T3 root sign brackets, monotone u(a) image direction and Fraction enclosures in new certificate including error bounds; do not infer Dbar monotonicity across its minimizer. Distinguish old evidence from current mathematical support.'),
dict(id='R8-fixed-u-T1',verification='analytic',statement='Verify analytic continuation of pole-free equations in t=1/R, nonzero root derivatives, actual mode correspondence, fixed-interior-u expansion and compact-interior uniform remainder; C(u*) formula via actual S. Check T1 global lower/pointwise upper sandwich, nonnegative O(1/R) error and all eta>=0 with R eta->0 near-minimizer convergence. Rule out both endpoints separately. Do not infer exact optimized coefficient or parameter rate from fixed-u analysis.'),
dict(id='R8-cards-summaries',verification='analytic',statement='Verify all four cards, explicit retrieval summaries, exact upstream references, DLMF cot powers/local uniform scope, and the directly changed INF sections of two companion TeX sources agree with the current proof. Only those INF sections are in scope in the companion documents; retained unrelated historical claims are not recertified. Check scope excludes non-symmetric/all-box/n>=2 results and complete Lean formalization. Source report findings and author statements are not proof by themselves.')]
spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=Claims)
save(O/'math-review-spec.json',spec);p=V.create_packet(R,spec);save(O/'math-review-packet.json',p);print('PACKET',p['packet_sha256'],len(Inputs),len(Claims),flush=True)
