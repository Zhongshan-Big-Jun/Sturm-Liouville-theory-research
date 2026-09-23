from pathlib import Path
import json,sys,hashlib,re
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
import research_review as V
def save(P,D):P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
def require(X,M):
	if not X:raise RuntimeError(M)
Bundle=json.loads((O/'math-review2-dispatch.json').read_text())['bundle']
require(V.verify_review_bundle(R,Bundle)['verdict']=='APPROVED','Final mathematics review not approved')
SP=Path(json.loads((O/'software-review2-root.json').read_text())['project']);SB=json.loads((O/'software-isolated-review2-dispatch.json').read_text())['bundle']
require(V.verify_review_bundle(SP,SB)['verdict']=='APPROVED','Final software review not approved')
require((R/'scripts/_gapn2_second_variation_probe.py').read_bytes()==(SP/'inputs/candidate/_gapn2_second_variation_probe.py').read_bytes(),'Accepted program not integrated')
Rows=json.loads((O/'revisions.json').read_text());require(len(Rows)==3,'Expected three revised cards')
Out=O/'release-results.json';Done=json.loads(Out.read_text()) if Out.exists() else []
for X in Rows:
	Revision=X['result']['revision_id']
	if any(Y['revision']==Revision for Y in Done):continue
	Result=C.release(R,Revision,Bundle);Done.append(dict(name=X['name'],revision=Revision,bundle=Bundle,result=Result));save(Out,Done)
	print(X['name'],Result['verdict'],flush=True);require(Result['verdict']=='RELEASED','Card still blocked '+X['name'])
Cards=json.loads((O/'cards.json').read_text());Notes={
	'second-variation-weighted-eigenvalues':('V2-V4 and independent review F1','2026-09-23: 先核对真实积分泛函与投影度量, 再独立积分残差. 总变差有界仅给有界性, 集中极限另需有符号质量收敛. 旧一维Green发散解释被反证; 有限核与界面加速度组合仍是可重访的待检验路线, 不是G1结论. 数值脉冲还必须先检查坐标/求积节点可分辨, 有限宽度结果不等于极限证明.'),
	'secular-chebyshev-jacobi-rootcount':('Normalized reflection and root-count scope','2026-09-23: 非零频率缩放保留零集但不保留函数值反射律. 先明确物理F和归一化Fhat, 再传播Jacobi根计数; y=0的归一化零不能当作物理特征值. 已有归一化历史证明保持原有范围.'),
	'bloch-band':('Nested Jacobi candidate argument and future use','2026-09-23: 把异常对角放在固定首端得到真正嵌套的主子矩阵, 末行递推排除Rayleigh等号, 显式试探向量给极限. 此方法闭合规定平衡候选序列, 不证明全局极大子具有对应块宽. 迁移到其它模型前须重新证明嵌套性及根到谱指标的桥接.')}
NoteFile=O/'annotations.json';NoteDone=json.loads(NoteFile.read_text()) if NoteFile.exists() else {}
for N,(Locator,Text) in Notes.items():
	if N in NoteDone:continue
	NoteDone[N]=L.annotate(R,Cards[N]['location'],Cards[N]['sha256'],author='01a06f46-dd03-7c83-9267-32048412c359',kind='correction',locator=Locator,text=Text);save(NoteFile,NoteDone)
IndexResult=L.make_index(R,ReadmePath='tools/README.md');save(O/'index-result.json',IndexResult)
Index=json.loads((R/'index/tools.json').read_text());require(len(Index['items'])==78 and len(Index['blocked_items'])==1,'Unexpected final card counts')
Renewals=json.loads((O/'renewals.json').read_text());Targets={X['target']['location']:X['target']['sha256'] for X in Renewals};Targets.update({X['location']:X['sha256'] for X in Cards.values()})
Query=L.query_tools(R,' '.join(Path(N).stem for N in Targets),limit=50);save(A/'current-tool-query.json',Query)
require(Query['verdict']=='RETRIEVAL_ONLY' and Query['blocked']==1 and not Query['changed_paths'],'Actual query failed current gate')
Hits={X['location']:X for X in Query['hits']};IndexRows={X['location']:X for X in Index['items']};Checks=[]
for N,H in Targets.items():
	Hit=Hits.get(N);require(Hit is not None and Hit['reuse_allowed'] and Hit['sha256']==H,'Required current card missing '+N)
	Raw=(R/N).read_bytes();require(hashlib.sha256(Raw).hexdigest()==H,'Card byte identity '+N)
	Front,Body,_=L.read_metadata(Raw);Expected=Front.get('summary') or re.sub(r'\s+',' ',Body).strip()[:500]
	require(Hit['summary']==Expected,'Current summary is stale '+N)
	require(Hit['dependencies']==C.card_dependencies(Front),'Current dependency summary mismatch '+N)
	for Key in ['sources','resources','evidence']:
		for Source in Hit.get(Key,[]):
			require(Source.get('binding_state')!='INVALID','Invalid source in query '+N)
			if Source.get('sha256'):require(Source.get('binding_state')=='CURRENT','Stale hash-bound source in query '+N)
	Checks.append(dict(path=N,sha256=H,summary=Hit['summary'],dependencies=Hit['dependencies'],reuse_allowed=True))
require(len(Checks)==15,'Expected fifteen changed or renewed current cards')
Warnings=Index['issues'];require(len(Warnings)==57 and all(X.get('status')=='REVIEW_NO_LONGER_VALID' for X in Warnings),'Unexpected historical warning set')
Store=C.load_store(R);Classes=[]
for W in Warnings:
	Release=Store['requests'][W['release']]['payload'];Rev=Store['requests'][Release['revision']]['payload'];Target=Rev['new'];Current={X['location']:X for X in Index['items']+Index['blocked_items']}.get(Target['location'])
	Category=('same-current-version-reviewed-again' if Current['reuse_allowed'] else 'retained-withdrawn-current-version') if Current and Current['sha256']==Target['sha256'] else 'superseded-card-version'
	Classes.append(dict(release=W['release'],revision=Release['revision'],target=Target,classification=Category))
Result=dict(status='PASS',available=78,blocked=1,blocked_paths=[X['location'] for X in Index['blocked_items']],new_card_releases=len(Done),unchanged_card_renewals=len(Renewals),unchanged_cards=len(set(X['target']['location'] for X in Renewals)),historical_invalid_releases=len(Warnings),historical_classifications=Classes,checked_current_cards=Checks,actual_query='current-tool-query.json',note='Releases are scoped mathematical approvals; the original withdrawn card and all historical failures remain preserved.')
save(A/'library-final-check.json',Result);save(O/'library-final-check.json',Result)
print('Actual library gate PASS: 78 available, 1 original blocked; 15 current summaries/dependencies checked.',flush=True)
