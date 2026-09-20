from pathlib import Path
import sys,json
Root=Path('/mnt/f/LaTeX/BVE research'); Out=Path('/mnt/f/tools/math-audit-round4-20260921')
Art='research/artifacts/proof-audit-round4-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
Rows=json.loads((Out/'recurrence-revisions.json').read_text())+json.loads((Out/'k1-revisions.json').read_text())
Inputs={}; Claims=[]; Authors={'01a06f46-dd03-7c83-9267-32048412c359','01a0bfab-5af3-7352-a134-deabd755066c'}
for Row in Rows:
	Req=Row['requirements']
	for Item in Req['inputs']:
		if Item['path'] in Inputs: assert Inputs[Item['path']]['sha256']==Item['sha256']
		Inputs[Item['path']]=Item
	Claims+=Req['claims']; Authors.update(Req['author_ids'])
for Name in ['docs/SL_third_order_recurrence_theory.tex','docs/SL_third_order_K1_proof.tex','runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md','runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/audit_report.md',Art+'/before/docs/SL_third_order_recurrence_theory.tex',Art+'/submitted/constructive_repairs.md']:
	if (Root/Name).is_file(): Inputs.setdefault(Name,{'path':Name,'role':'current-proof-or-disclosed-history'})
for P in sorted((Root/Art/'recurrence-checks').iterdir()):
	if P.is_file():
		Name=str(P.relative_to(Root)); Inputs.setdefault(Name,{'path':Name,'role':'author-checks-and-execution-scope'})
Claims += [
	{'id':'R4-recurrence-analytic','verification':'analytic','statement':'Independently audit all new analytic proofs of the exact even/odd P,Q,R recurrence for every real c>0: reversible scales and three initial data; difference factorization; full solution v=A+Bj+C Phi; finite terminal convention z_N=1,z_(N+1)=z_(N+2)=0 and positive normalized convergence; unique positive normalized minimal solution; closed K0(c),K1(c) and all-index tail/error estimates. Check infinite convergence/positivity/limit operations directly; finite tests are not a proof. Verify K0(1)=e/4 and explain the old K1 card uses a different finite unnormalized terminal convention.'},
	{'id':'R4-rational-classification','verification':'analytic','statement':'Verify the arbitrary-degree rational-ratio classification by poles and polynomial degree, and all monic quadratic numerator/denominator representations including cancellations, all exceptional tau branches, and A=0 tail representations with d!=0. Raw denominators must not vanish on a claimed recurrence domain; eventual rational identity is distinct from a normalized global solution. Check reduction and its converse require termwise nonzero E, correctly retain r0,s1,s2 and variation nonzero hypotheses. Check the homogeneous-box counterexample and ensure a rational-subclass exclusion is not generalized to all homogeneous solutions. Reconnect the existing frozen all-degree root-1 proof without modifying it or mistaking its historical repaired-gap verdict for new approval.'},
	{'id':'R4-recurrence-evidence','verification':'exact-computation','statement':'Check the supplied exact/symbolic, high precision and static checks are honestly separated, including original failed attempts and corrections. Re-execute useful disposable checks from snapshots when feasible, disclose path adaptations. Historical higher asymptotic tables and old numerical error estimates were not recertified. Current TeX/card claims must not promote finite computations, historical tables or local formal algebra into an all-project or all-Lean theorem.'}
]
Packet=Review.create_packet(Root,{'kind':'mathematics','author_ids':sorted(Authors),'inputs':list(Inputs.values()),'claims':Claims})
(Out/'recurrence-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
print(Packet['packet_sha256'])
