from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A='research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_review as V
B=json.loads((O/'baseline.json').read_text());Cards=json.loads((O/'cards.json').read_text());Coord='01a06f46-dd03-7c83-9267-32048412c359'
Done=json.loads((O/'revisions.json').read_text()) if (O/'revisions.json').exists() else []
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for Name,New in Cards.items():
	if any(x['name']==Name for x in Done):continue
	Old=dict(location=New['location'],sha256=B['tracked'][New['location']])
	Result=C.propose_revision(R,'round9-variation-and-normalization',Old,dict(location=New['location'],sha256=New['sha256']),Coord,'Correct block tangency, normalized derivative kernel and Green pulse limits; separate finite interface acceleration. Normalize physical secular reflection, preserve root count and prove monotonicity/limit only for prescribed balanced candidate sequence. Historical proofs remain immutable; no G1/O1/O2 completion claim.')
	Done.append(dict(name=Name,result=Result));save(O/'revisions.json',Done);print('Revision',Name,Result['revision_id'],flush=True)
Inputs={};Claims=[];Authors={Coord}
for Row in Done:
	Req=C.review_requirements(R,Row['result']['revision_id']);save(O/(Row['name']+'-requirements.json'),Req)
	for X in Req['inputs']:
		if X['path'] in Inputs and Inputs[X['path']].get('sha256')!=X['sha256']:raise RuntimeError('Conflicting exact input')
		Inputs[X['path']]=X
	Claims+=Req['claims'];Authors.update(Req['author_ids'])
Extra=[A+'/analytic-repair.md',A+'/submitted/analytic_repairs.md',A+'/submitted/checks.py',A+'/submitted-replay/normal.json',A+'/submitted-replay/optimized.json',A+'/submitted-replay/normal-execution.json',A+'/submitted-replay/optimized-execution.json','docs/SL_fixed_n_supremum.tex','docs/SL_spectral_topics_summary.tex',A+'/before/docs/SL_fixed_n_supremum.tex',A+'/before/docs/SL_spectral_topics_summary.tex','scripts/_gapn2_k_global_rank2.py','runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13c.md','runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md']
for N in Extra:Inputs.setdefault(N,dict(path=N,role='current-proof-or-explicit-historical-comparison'))
Claims.extend([
	dict(id='R9-V1',verification='analytic',statement='Check the positive bounded real Dirichlet contract, Volterra analytic-branch justification, normalized eigenfunction derivative including its kernel component, distinction between ordinary L2 reduced inverse and weighted spectral finite part, square-summable coefficient argument and the retained lambda second derivative formula. Check h=rho as a real counterexample to the old displayed equality. Do not assume an optimization stationary point.'),
	dict(id='R9-V2',verification='analytic',statement='Check actual block integral normal A, Euclidean and weighted coefficient metrics, zero-normal case and the exact constant-density unequal-width counterexample. Check the repaired card withdraws old block P2 tangency and never upgrades random signs, truncated spectra or saturated-box directions to an infinite-dimensional definiteness result. Execution of the new numerical implementation has a separate review; this claim covers its mathematical contract and the card scope only.'),
	dict(id='R9-V3-V4',verification='analytic',statement='Check the complete one-dimensional regular Green finite-part continuity argument including simple pole/residue normalization and uniformity, the unit-total-variation concentration scope, the infinite-series dominated convergence midpoint example with lambda1 second derivative 6pi^2, lambda2 0 and half gap -3pi^2. Check the moving-interface distributional acceleration sign and factor 1/2 for Q. Ensure no arbitrary distribution-path differentiability, universal Hessian equality, all-density feasibility or G1 sign is claimed. The old divergence and route-closure rationale is withdrawn but immutable old records are not rewritten.'),
	dict(id='R9-B1-B2',verification='analytic',statement='Independently check actual physical-to-normalized transfer matrices and omega(y), arbitrary-n J conjugation, reflection scaling, exact n1/R4 counterexample and zero/endpoint scope. Check Cayley-Hamilton recurrence, Jacobi characteristic polynomial, both endpoint quadratic-form identities including n=1, simplicity, mapping to the first 2n physical eigenvalues, nested-matrix strict minimum monotonicity and squeeze to -2. Verify c_n strictly decreases to the stated limit for all fixed R>1 and n>=1, without identifying it with the unknown global optimum.'),
	dict(id='R9-current-presentation',verification='analytic',statement='Check all three current cards and explicit retrieval summaries against the analytic repair and fixed-n TeX. Compare only the changed B3 passages of the comprehensive summary against the supplied before version; other summary mathematics is inherited and not recertified. Inspect the modified explanatory paragraph of the K script only; its retained implementation/global identity is not re-audited. Ensure historical B3 normalized proof and root count are not incorrectly retracted, old R206 errors are clearly superseded, and global O1/O2 and complete formalization remain open.')])
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=Claims)
save(O/'math-review-spec.json',Spec);Result=V.create_packet(R,Spec);save(O/'math-review-packet.json',Result);print('Math packet',len(Inputs),'inputs',len(Claims),'claims',flush=True)
