from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A='research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
import research_review as V
def save(N,D):(O/N).write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
Coord='01a06f46-dd03-7c83-9267-32048412c359';Name='second-variation-weighted-eigenvalues';Loc='tools/'+Name+'.md'
Cards=json.loads((O/'cards.json').read_text());Done=json.loads((O/'revisions.json').read_text());Old=Cards[Name]
Raw=(R/Loc).read_bytes();Front,Body,_=L.read_metadata(Raw)
OldLine='固定总变差的集中脉冲二次型因此有有限点值极限. 特别在 rho=1,'
NewLine='总变差一致有界的集中脉冲二次型因此一致有界. 还须支持集中到 a、\n带符号总质量 int h_eta dx 趋于 q, 才有极限 q^2 u_k(a)^2 Gtilde_k(a,a).\n总变差有界本身不保证带符号质量或二次型收敛. 特别在 rho=1,'
if OldLine not in Body:raise RuntimeError('Expected exact old statement absent')
Data=json.loads(json.dumps(Front,default=str));Data['content']=Body.replace(OldLine,NewLine,1)
Data['summary']=Data['summary'].replace('窄脉冲Green极限有限','Green核有界, 集中脉冲须总变差有界且有符号质量收敛才有点值极限')
New=L.save_card(R,Data,Loc,Old['sha256']);save('cards-before-f1.json',Cards);Cards[Name]=New;save('cards.json',Cards)
Result=C.propose_revision(R,'round9-variation-and-normalization',dict(location=Loc,sha256=Old['sha256']),dict(location=Loc,sha256=New['sha256']),Coord,'Respond to fresh independent mathematical review F1: bounded total variation only proves boundedness. Require support concentrating at a and signed mass tending to q for the continuous-kernel point-value limit. Preserve the rejected exact candidate and analytic proof bytes.')
save('revisions-before-f1.json',Done)
Done=[dict(name=Name,result=Result) if X['name']==Name else X for X in Done];save('revisions.json',Done)
Note='''# 独立审查 F1 的修复

首次隔离数学审查指出: 工具卡把有界总变差写成了点值极限的充分条件. 原解析证明 V3 已要求支集集中、总变差一致有界和有符号总质量收敛; 当前卡遗漏最后一项.

固定连续核 K 时, 支集集中到 a 且总变差不超过 C 给出
|∫∫K dmu_eta dmu_eta - K(a,a)(∫dmu_eta)^2| <= C² sup_support |K-K(a,a)| -> 0.
若总质量趋于 q, 极限是 q²K(a,a); 若质量不收敛, 只能保证有界.
rho=1、a=1/2 时交替取单位正脉冲和左右正负等量脉冲, 总变差均为1而质量交替为1和0; k=1的夹心核 K(a,a)=1/pi², 二次型有两个不同子列极限. 这确认审查发现.

本次仅修订二阶变分卡的该句和显式摘要. 解析证明、两份TeX/PDF、两张B3卡和软件冻结输入原字节未变. 旧卡版本和CHANGES_REQUIRED回执保留; 当前修订须经另一新会话验收.
'''
(R/A/'review-f1-repair.md').write_text(Note)
Inputs={};Claims=[];Authors={Coord}
for Row in Done:
	Req=C.review_requirements(R,Row['result']['revision_id'])
	for X in Req['inputs']:Inputs[X['path']]=X
	Claims+=Req['claims'];Authors.update(Req['author_ids'])
OldSpec=json.loads((O/'math-review-spec.json').read_text())
for X in OldSpec['inputs']:
	if not X['path'].startswith('research/library/') and not X['path'].startswith('tools/'):Inputs.setdefault(X['path'],X)
Bundle=json.loads((O/'math-review-dispatch.json').read_text())['bundle']
for N in [A+'/review-f1-repair.md',Bundle+'/report.json',Bundle+'/receipt.json']:Inputs[N]=dict(path=N,role='historical-rejection-and-response')
Claims += [X for X in OldSpec['claims'] if not X['id'].startswith('correction:')]
Claims.append(dict(id='R9-F1-response',verification='analytic',statement='Independently verify the current signed-concentration hypotheses and the two-subsequence counterexample in the F1 response. Check both current card prose and explicit summary preserve signed-mass convergence. Reassess all supplied correction claims against actual proof inputs; prior mixed approval/rejection is context, not a substitute for your judgment.'))
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=Claims)
save('math-review2-spec.json',Spec);save('math-review2-packet.json',V.create_packet(R,Spec))
print('Repaired card',New['sha256'],'revision',Result['revision_id'],'inputs',len(Inputs),'claims',len(Claims),flush=True)
