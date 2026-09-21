from pathlib import Path
import sys,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round6-20260921');A=R/'research/artifacts/proof-audit-round6-20260921'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
import research_corrections as C
Done=json.loads((O/'release-results.json').read_text());assert len(Done)==19
Cards=json.loads((O/'cards.json').read_text())
TextByCard={
'constrained-denseness-runs':'Finite codimension in polynomial algebra is different from codimension of the topological closure. Projection density is controlled by V intersect M-perp, not by a silently assumed sparse totality. Full-space density is sufficient but not necessary. Finite low-moment tests belong on the realized finite-dimensional tail obstacle, not the entire infinite-dimensional V; check that hypotheses have actual instances. Round6 independent review caught and corrected a sufficient-to-necessary error in the coordinator summary. See docs/SL_projection_moment_repairs.tex and reports/proof-audit-round6-20260921/REPORT.md.',
'spectral-domain-checks':'Individual named-member admissibility differs from admissibility after finite linear combination. The example p6-(7/2)p4 cancels the next boundary residual although each summand lies outside Hc4. A fixed right inverse of the four-trace map corrects polynomial approximations and gives a graph core. This provides the independent route to 0<=s<7/2 density; it does not extend deleted-family classifications or certify uniform-c/basis claims. Local Lean covers real algebra, not the spectral/Sobolev argument.'}
NotePath=O/'annotations.json';Notes=json.loads(NotePath.read_text()) if NotePath.exists() else {}
for Name,Text in TextByCard.items():
	if Name in Notes:continue
	Card=Cards[Name];Notes[Name]=L.annotate(R,Card['location'],Card['sha256'],author='coordinator-20260921-round6',kind='research-experience',locator='Sixth-round repaired proof and independent findings',text=Text);NotePath.write_text(json.dumps(Notes,ensure_ascii=False,indent=2)+'\n')
P=R/'tools/README.md';T=P.read_text();Marker='## 第五轮修订 (2026-09-21)';assert Marker in T and '## 第六轮修订 (2026-09-21)' not in T
T=T.replace(Marker,'## 第六轮修订 (2026-09-21)\n\n[投影与有限矩准则](constrained-denseness-runs.md)修复三项问题, 采用实际尾部正交障碍上的有限检验; 原F的假设无实例, 一个表示元的非零检测不等于两个矩分别为零. [谱域工具](spectral-domain-checks.md)给出原完整命名族的精确非负稠密范围0<=s<7/2, 由四迹图核心补证. 九张相关卡和继承义务均按当前版本审查并释放; 旧源和批注保留. 第五轮s=2删除分类范围不扩大. [第六轮报告](../reports/proof-audit-round6-20260921/REPORT.md)区分解析验收、局部Lean和首次摘要退回.\n\n'+Marker,1)
T=T.replace('原稀疏族在 `s>=7/2` 时不全属于相应幂域; `3<s<7/2` 的同族稠密性仍开放.','原稀疏族在 `s>=7/2` 时不全属于相应幂域; 第二轮当时保留的 `3<s<7/2` 问题已由第六轮四迹图核心补证关闭, 当前原完整族范围为 `0<=s<7/2`.')
P.write_text(T)
Index=L.make_index(R);(O/'index-result.json').write_text(json.dumps(Index,ensure_ascii=False,indent=2)+'\n')
Query=L.query_tools(R,' '.join([*Cards,'third-order-recurrence','third-order-minimal-K1','left-definite-orthogonal-systems']),limit=60)
Hits={H['location']:H for H in Query['hits']}
for Card in Cards.values():
	assert Card['location'] in Hits and Hits[Card['location']]['reuse_allowed'] and Hits[Card['location']]['sha256']==Card['sha256'],Card
Current=json.loads((R/'index/tools.json').read_text());assert len(Current['items'])==78 and len(Current['blocked_items'])==1
assert Current['blocked_items'][0]['location']=='tools/left-definite-orthogonal-systems.md'
Active={X['location']:X for X in Current['items']}
Store=C.load_store(R);Classified=[]
for Problem in Query['issues']:
	assert Problem.get('status')=='REVIEW_NO_LONGER_VALID',Problem
	Release=Store['requests'][Problem['release']]['payload'];Rev=Store['requests'][Release['revision']]['payload'];Loc=Rev['new']['location']
	assert Loc in Active and Active[Loc]['reuse_allowed'],('unresolved historical issue',Loc,Problem)
	Latest=[E['request'] for E in Store['events'] if Store['requests'][E['request']]['kind']=='revision' and Store['requests'][E['request']]['payload']['issue']==Rev['issue'] and Store['requests'][E['request']]['payload']['new']['location']==Loc][-1]
	assert Latest!=Release['revision'];Classified.append(dict(Problem,location=Loc,classification='SUPERSEDED_HISTORICAL_RECEIPT',current_revision=Latest))
Result={'status':'PASS','available_cards':78,'blocked_cards':1,'cards':Cards,'versions':len(Store['nodes']),'correction_events':len(Store['events']),'current_reviewed_obligations':len(Done),'historical_superseded_review_warnings':Classified,'annotations':Notes,'canonical_modified':False,'default_query_verdict':Query['verdict']}
for P in [O/'library-final.json',A/'library-final.json']:P.write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
(A/'default-query.json').write_text(json.dumps(Query,ensure_ascii=False,indent=2)+'\n')
print('Final library PASS:78 available/1 blocked;',len(Store['nodes']),'versions;',len(Store['events']),'events.',flush=True)
