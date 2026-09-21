from pathlib import Path
import sys,json,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round5-20260921');Art='research/artifacts/proof-audit-round5-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as R
Authors=['01a06f46-dd03-7c83-9267-32048412c359','01a0c22b-f107-7520-9d75-33258752765c']
New=json.loads((Out/'card-result.json').read_text())
State=json.loads((Out/'interrupted-library-state.json').read_text());assert not State['pending']
Store=C.load_store(Root);Issue,_=C.find_issue(Store,'round5-o1pld')
Rows=[E['request'] for E in Store['events'] if Store['requests'][E['request']]['kind']=='revision' and Store['requests'][E['request']]['payload']['issue']==Issue]
assert len(Rows)==1 and not Store['pending']
Payload=Store['requests'][Rows[0]]['payload'];assert Payload['new']=={K:New[K] for K in ['location','sha256']}
assert hashlib.sha256((Root/New['location']).read_bytes()).hexdigest()==New['sha256']
Revision={'revision_id':Rows[0],'request_id':Rows[0],'recovery':'Read existing verified committed journal, not a successful return claimed from the interrupted mutation. No second revision created.','original_exec_exit':143,'index_refresh':'Interrupted; final release will regenerate and query the index.','payload':Payload}
(Out/'revision-result.json').write_text(json.dumps(Revision,ensure_ascii=False,indent=2)+'\n')
Req=C.review_requirements(Root,Revision['revision_id']);(Out/'review-requirements.json').write_text(json.dumps(Req,ensure_ascii=False,indent=2)+'\n')
Inputs={X['path']:X for X in Req['inputs']}
Extras=[('docs/SL_cofinite_left_definite.tex','analytic-proof'),('docs/SL_h2_completeness_proof.tex','unchanged-operator-setting'),(Art+'/submitted/cofinite_replacement_proof.md','external-proposed-proof-not-approval'),(Art+'/submitted/proof_audit_round5_20260921.md','external-findings'),(Art+'/coordinator-checks/check_counterexamples.py','coordinator-check-source'),(Art+'/coordinator-checks/results.json','scoped-symbolic-results'),(Art+'/coordinator-checks/execution.json','actual-execution'),(Art+'/coordinator-checks/test-repair.json','preserved-test-representation-correction')]
for Name,Role in Extras:Inputs.setdefault(Name,{'path':Name,'role':Role})
Claims=Req['claims']+[
{'id':'R5-F01-refutations','verification':'analytic','statement':'Independently verify the explicit nonzero g0,c, its Green identity for all complex functions in the precise Krein Hc2 domain, M0=1/c and all-tail recurrence consequence. Check V=ker evaluation is proper closed and excludes exactly p0. These refute old NOT-YET-STRICT Claim4/Theorem5/Corollary6, without refuting accepted full H2/H3 completeness or confusing a plausible candidate with a previously certified theorem.'},
{'id':'R5-cofinite-closure','verification':'analytic','statement':'Verify the all-cofinite theorem, not merely samples: self-adjoint positive Kc and onto isometry assumptions, equivalence to ordinary Sobolev H2 norm on its domain, continuity of both central traces, algebraic tail span by leading-term elimination for every even L>=2, the zero-trace cutoff estimates with local L2 norms and uniform-in-delta constants, polynomial approximation and exact endpoint residual correction. Check complex scalars, first-linear inner product, all c>0, cofinite N, both missing-low-index cases, and no s=3 or non-cofinite generalization.'},
{'id':'R5-Green-and-actual-subspace','verification':'analytic','statement':'Check g1,c normalization, positivity of its denominator, endpoint/interface signs and its L2-only domain. Verify the exact orthogonal complement, two-dimensional tail-moment obstruction (if stated) and initial-moment normalization. For closed V with actual cofinite retained set, check V contains V*, V=Gamma^-1(S), retained closure corresponds exactly to included coordinate axes, and the oblique 1+x example. Verify any stated full classification of such S.'},
{'id':'R5-F02-monomial-repair','verification':'analytic','statement':'Verify the odd norm coefficient is1 rather than1/2 and the direct finite-deletion monomial density proof via x^M f for arbitrary complex L2 f. Check the bounded multiplication, polynomial orthogonality, density premise and almost-everywhere zero conclusion, including an empty deleted set. This true monomial result cannot be transferred to q_n merely by analogy.'},
{'id':'R5-checks-and-boundaries','verification':'exact-computation','statement':'Inspect and, in disposable external space if possible, rerun the24 coordinator checks. Treat symbolic identities and exact counterexamples separately from Sobolev/closure proofs. Inspect the preserved CAS removable-singularity test repair rather than treating it as a mathematical defect. Check the new card states its sources and the limits of old parity/mu4 branches and local Lean honestly; this packet makes no full Lean or global repository certification.'}]
Packet=R.create_packet(Root,{'kind':'mathematics','author_ids':sorted(set(Authors+Req['author_ids'])),'inputs':list(Inputs.values()),'claims':Claims})
(Out/'mathematics-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_card':New,'revision':Revision['revision_id'],'packet':Packet.get('packet'),'claims':len(Claims)},ensure_ascii=False))
