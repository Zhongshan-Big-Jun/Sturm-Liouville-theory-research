from pathlib import Path
import sys
import json

Root=Path('/mnt/f/LaTeX/BVE research')
Out=Path('/mnt/f/tools/math-audit-round4-20260921')
Art='research/artifacts/proof-audit-round4-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
Rows=json.loads((Out/'quotient-revisions.json').read_text())
Inputs={};Claims=[];Authors={'01a06f46-dd03-7c83-9267-32048412c359','01a0bfab-01ac-7dd2-b9e3-15edb3ffd3f3'}
for Row in Rows:
	Req=Row['requirements']
	for Item in Req['inputs']:
		if Item['path'] in Inputs:
			assert Inputs[Item['path']]['sha256']==Item['sha256']
		Inputs[Item['path']]=Item
	Claims+=Req['claims'];Authors.update(Req['author_ids'])
for Name,Role in [('docs/SL_krein_c0_limit.tex','repaired-proof'),(Art+'/before/docs/SL_krein_c0_limit.tex','original-proof'),('docs/SL_fractional_left_definite.tex','unchanged-previous-scope-reference'),('tools/krein-power-domain-polynomial-obstruction.md','unchanged-operator-domain-scope-reference'),('tools/left-definite-orthogonal-systems.md','withdrawn-all-order-interpretation'),('research/artifacts/proof-audit-round3-20260920/quotient-checks/primary-excerpt.txt','primary-source-setting')]:
	Inputs.setdefault(Name,{'path':Name,'role':Role})
for P in sorted((Root/Art/'quotient-checks').iterdir()):
	if P.is_file():
		Name=str(P.relative_to(Root));Inputs.setdefault(Name,{'path':Name,'role':'author-exact-check-or-manifest'})
Claims += [
	{'id':'R4-F01-F05-analytic','verification':'analytic','statement':'Independently verify the fixed-index ordinary Sobolev representative limits versus quotient limits, explicit Legendre derivative and Gram identities, positive parity induction with controlled O_n(a_n) remainder, coefficient/norm leading constants, and O_n(c) rate in the repaired thm:unit for every fixed n. In particular n=2,3 must retain affine discrepancies and n=0,1 have zero quotient classes. Check all-index proofs instead of inferring them from finite symbolic tests. No uniform-in-n or joint-limit claim is allowed. Check adjacent corrected numerical-section formulas (n=4 norm, n=5 exponent, actual projection coefficient).'},
	{'id':'R4-quotient-card-propagation','verification':'analytic','statement':'Check the exact repaired Krein-Sobolev card resolves both original issue and new issue: first-derivative boundary, removal of stale H2-open/all-order polynomial-transfer claims, and new ordinary-versus-quotient c->0 limit paragraph/source bindings. Other retained literature summaries are explicitly not reaudited. The third-round setting/radical/isometry/completeness block is unchanged; check preservation and applicability rather than claim a new full-project audit.'},
	{'id':'R4-quotient-execution-scope','verification':'exact-computation','statement':'Check the 274 author checks are accurately described as260 exact mathematical finite checks plus14 preservation/structure checks. Re-execute in disposable space if possible using copied snapshots (do not write into frozen inputs); report any unavailable part or required path adaptation honestly. Finite checks and TeX structure checks are not universal mathematical proof, independent review or PDF verification. Inspect actual first-run preservation failures and final hashes without relabeling failed attempts.'}
]
Packet=Review.create_packet(Root,{'kind':'mathematics','author_ids':sorted(Authors),'inputs':list(Inputs.values()),'claims':Claims})
(Out/'quotient-review-packet.json').write_text(json.dumps(Packet,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(Packet,ensure_ascii=False))
