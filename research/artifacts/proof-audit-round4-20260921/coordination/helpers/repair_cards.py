from pathlib import Path
import sys
import json
import hashlib

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round4-20260921')
sys.path.insert(0, str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as Library
import research_corrections as Corrections

Author = '01a06f46-dd03-7c83-9267-32048412c359'
Mode = sys.argv[1]
Intake = json.loads((Out/'card-intake.json').read_text())
Names = {'recurrence':'tools/third-order-recurrence.md', 'k1':'tools/third-order-minimal-K1.md', 'quotient':'tools/krein-sobolev-polynomials.md', 'stability':'tools/jump-stability.md'}
Location = Names[Mode]
Old = next(Row['old'] for Row in Intake if Row['old']['location']==Location)
Raw = (Root/Location).read_bytes()
assert hashlib.sha256(Raw).hexdigest()==Old['sha256'], 'Expected original current version'
Front, Body, _ = Library.read_metadata(Raw)
Metadata = {'created':str(Front['created']),'author_ids':sorted(set(Front.get('author_ids',[])+[Author]))}
if Mode=='recurrence':
	Body = (Out/'third-order-card-content.md').read_text()
	Metadata.update(title='固定系数三阶递推: 差分分解、最小解与有理比值', status='第四轮解析修订; 精确适用范围与复用状态见纠错记录', evidence_status='ANALYTIC_PROOF_SCOPED', scope='Specified even and odd P,Q,R only; c>0; finite/normalized terminal conventions and eventual nonzero ratio domains are explicit.', sources=[{'path':'docs/SL_third_order_recurrence_theory.tex','locator':'Fourth-round exact-coefficient recurrence, all-index proofs and scope'}, {'path':'runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md','locator':'Existing frozen all-degree root-1 proof'}])
	Metadata['author_ids'].append('01a0bfab-5af3-7352-a134-deabd755066c')
elif Mode=='k1':
	OldText='- `OPEN`: the corresponding closed form and constant `K(c)` for general c,\n  source-term control in the box induction, and classification of all general\n  coefficient families remain unresolved.'
	NewText='- For the same explicit even/odd coefficient family, the fourth-round proof now gives the normalized general-c positive-tail formula and constants. See `tools/third-order-recurrence.md` and `docs/SL_third_order_recurrence_theory.tex`. This card retains the original even c=1 terminal convention above; its finite unnormalized sequence must not be confused with the other convention.\n- `OPEN`: source-term control in the box induction and classification of arbitrary coefficient families remain outside those exact-coefficient results.'
	assert OldText in Body
	Body=Body.replace(OldText,NewText)
	Body += '\n2026-09-21 scope update: the c=1 proof and all displayed anchor formulas are unchanged. The new general-c proof specializes to the same e/4 constant; this status update and its exact dependency receive new independent review.\n'
	Third = json.loads((Out/'recurrence-card-result.json').read_text())
	Metadata.update(status='STRICT even c=1 anchor; exact-family general-c extension linked separately', evidence_status='SCOPED_STATUS_AND_DEPENDENCY_UPDATE', dependencies=[{'location':Third['location'],'sha256':Third['sha256']}], sources=[{'path':'docs/SL_third_order_K1_proof.tex','locator':'Existing c=1 finite terminal convention and normalized limit'},{'path':'docs/SL_third_order_recurrence_theory.tex','locator':'Fourth-round explicit family general-c extension'}])
	Metadata['author_ids'].append('01a0bfab-5af3-7352-a134-deabd755066c')
elif Mode=='quotient':
	Body += r'''

## 2026-09-21: c下降到0时的函数代表与商类

令S_n=P_n-P_(n-2), W=span{1,x}. 零参数配对满足(S_n,S_m)_(1,0)=2(2n-1)delta_nm, 因而标准Gram-Schmidt的正首项代表为Q_n=S_n/sqrt(2(2n-1)). 对每个固定n>=2, 单位归一化Krein-Sobolev多项式的商类收敛到[Q_n]. 普通Sobolev H1中的函数极限则是P2/sqrt(6)、P3/sqrt(10) (n=2,3), 以及Q_n (n>=4). 低阶仿射差在商空间中消失, 在普通H1中并不消失. 不声称关于n一致的收敛.

高阶系数按奇偶归纳使用主项(4n^2-1)a_n/c与O(a_n)余项. a6-(63/c)a4=1+42/c, 不能把余项写成O(1). 这修正证明而不撤回固定高模态的发散结论. 完整解析证明见`docs/SL_krein_c0_limit.tex`的thm:high及thm:unit; 本轮未重新审计本卡其它既有文献摘要.
'''
	Metadata.update(evidence_status='SCOPED_QUOTIENT_LIMIT_CORRECTION; OTHER_LITERATURE_SUMMARY_NOT_REAUDITED', sources=[{'path':'docs/SL_krein_c0_limit.tex','locator':'Setting and thm:high/unit; ordinary representatives versus quotient classes'}, {'path':'docs/SL_fractional_left_definite.tex','locator':'Previously proved 0<=s<=3 spectral transfer'}, {'path':'tools/krein-power-domain-polynomial-obstruction.md','locator':'Operator inverse versus algebraic polynomial inverse'}])
	Metadata['author_ids'].append('01a0bfab-01ac-7dd2-b9e3-15edb3ffd3f3')
else:
	Body += '\n2026-09-21 review-binding renewal: the stability mathematics and its proof source are unchanged. The previous shared verification packet also bound the quotient paper, whose separate unit-limit section is now repaired. This card is rechecked in its own precise scope; the fourth-round quotient correction is not a new counterexample to this card.\n'
	Metadata.update(evidence_status='ANALYTIC_PROOF_SCOPED; REVIEW_BINDING_RENEWED', sources=[{'path':'docs/SL_stability_moment_jump.tex','locator':'Unchanged third-round general recurrence, exact model and perturbation proof'}])
Metadata['content'] = Body
New = Library.save_card(Root,Metadata,Location,Old['sha256'])
(Out/(Mode+'-card-result.json')).write_text(json.dumps(New,ensure_ascii=False,indent=2)+'\n')

# Each earlier issue affects every new version in this card family. Renew all
# issue obligations, not just the newest quarantine. Old issue target snapshots
# are retained and remain affected even if an earlier replacement was released.
Issues=[]
for P in sorted((Root/'research/library/corrections/requests').glob('*.json')):
	Request=json.loads(P.read_text())
	if Request['kind']=='issue':
		for Ref in Request['payload']['targets']:
			if Ref['location']==Location:
				Issues.append((Request['payload']['issue_id'],Ref))
Rows=[]
for IssueId,IssueOld in Issues:
	Revision=Corrections.propose_revision(Root,IssueId,IssueOld,New,Author,'Fourth-round exact-version repair and evidence renewal. Check the full prior correction plus the new scoped statements; preserve all old snapshots and distinguish unchanged accepted dependencies from newly proved explicit-family claims.')
	Req=Corrections.review_requirements(Root,Revision['revision_id'])
	Row={'issue_id':IssueId,'revision':Revision,'requirements':Req}
	Rows.append(Row)
	(Out/(Mode+'-'+IssueId+'-revision.json')).write_text(json.dumps(Row,ensure_ascii=False,indent=2)+'\n')
	print(Mode,IssueId,Revision['revision_id'],flush=True)
(Out/(Mode+'-revisions.json')).write_text(json.dumps(Rows,ensure_ascii=False,indent=2)+'\n')
