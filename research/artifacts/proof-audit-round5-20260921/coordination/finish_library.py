from pathlib import Path
import sys,json,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round5-20260921');Art=Root/'research/artifacts/proof-audit-round5-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
import research_corrections as C
import research_review as R
# Card approval is analytic; final documents/publication separately require all4 reviews.
for Name in ['mathematics','dependency-v2','readback']:
	D=json.loads((Out/(Name+'-review-dispatch.json')).read_text());assert R.verify_review_bundle(Root,D['bundle'])['verdict']=='APPROVED'
Revision=json.loads((Out/'revision-result.json').read_text());Dispatch=json.loads((Out/'mathematics-review-dispatch.json').read_text())
Released=json.loads((Out/'dependency-release-result.json').read_text());assert Released['reuse_allowed'] and Released['verdict']=='RELEASED'
Card=json.loads((Out/'card-result.json').read_text())
Note=L.annotate(Root,Card['location'],Card['sha256'],author='coordinator-20260921-round5',kind='research-experience',locator='R5-TAIL-MOMENT and cofinite two-trace classification',text='Deleting finitely many low modes changes continuous interior trace constraints even when every sufficiently high recurrence remains true. Here the exact L2 obstruction is span{g0,c,g1,c}, with u=cM0*g0,c+cM1*g1,c; adding both zero initial moments restores rigidity. A closed V with cofinite actual retention must contain every high p_n; only p0 and p1 can be missing. Distinguish a chosen cofinite index set from the actual retained set of a closed V, and density in all L2 from density inside Kc(V). The analytic complex Sobolev theorem is separately reviewed; AuditRound5.lean covers only real-polynomial traces, residues, algebraic spans and correction. See reports/proof-audit-round5-20260921/REPORT.md and its actual reviews. This annotation adds research experience, not a higher-order or non-cofinite theorem.')
(Out/'annotation-result.json').write_text(json.dumps(Note,ensure_ascii=False,indent=2)+'\n')
P=Root/'tools/README.md';Raw=P.read_text();Marker='## 第四轮修订 (2026-09-21)\n';assert Raw.count(Marker)==1
Insert='## 第五轮修订 (2026-09-21)\n\n[余有限稀疏族与两条迹](leftdef-o1pld-l2-structural.md)撤回原Claim4/Theorem5/Corollary6的错误候选, 给出s=2的完整余有限闭包、两个Green障碍及实际闭子空间分类. 单项式有限删除引理的换元系数和证明同时修复. 原封存run保持不变, 当前复用以新版精确回执为准; 一般非余有限O1\'LD与s=3仍开放. [第五轮报告](../reports/proof-audit-round5-20260921/REPORT.md)区分解析证明、37个局部Lean定理及四份隔离检验.\n\n'
P.write_text(Raw.replace(Marker,Insert+Marker))
Index=L.make_index(Root);(Out/'index-result.json').write_text(json.dumps(Index,ensure_ascii=False,indent=2)+'\n')
Names=['leftdef-o1pld-l2-structural','third-order-recurrence','third-order-minimal-K1','krein-sobolev-polynomials','jump-stability','left-definite-theory','left-definite-moment-recurrence','moment-jump-completeness','denseness-criteria']
Query=L.query_tools(Root,' '.join(Names+['left-definite-orthogonal-systems']),limit=50);assert Query['verdict']=='RETRIEVAL_ONLY' and Query['changed_paths']==[]
Hits={H['location']:H for H in Query['hits']}
for Name in Names:
	Loc='tools/'+Name+'.md';assert Loc in Hits and Hits[Loc]['reuse_allowed'],Loc
	assert Hits[Loc]['sha256']==hashlib.sha256((Root/Loc).read_bytes()).hexdigest(),Loc
assert Hits[Card['location']]['sha256']==Card['sha256'] and 'tools/left-definite-orthogonal-systems.md' not in Hits
Current=json.loads((Root/'index/tools.json').read_text());assert len(Current['items'])==78 and len(Current['blocked_items'])==1
assert Current['blocked_items'][0]['location']=='tools/left-definite-orthogonal-systems.md'
Store=C.load_store(Root);Classified=[]
for Problem in Query['issues']:
	assert Problem.get('status')=='REVIEW_NO_LONGER_VALID',Problem
	Release=Store['requests'][Problem['release']]['payload'];Old=Store['requests'][Release['revision']]['payload'];Loc=Old['new']['location']
	assert Loc in Hits and Hits[Loc]['reuse_allowed']
	Latest=[E['request'] for E in Store['events'] if Store['requests'][E['request']]['kind']=='revision' and Store['requests'][E['request']]['payload']['issue']==Old['issue'] and Store['requests'][E['request']]['payload']['new']['location']==Loc][-1]
	assert Latest!=Release['revision']
	Classified.append(dict(Problem,location=Loc,classification='SUPERSEDED_HISTORICAL_RECEIPT',current_revision=Latest))
Result={'status':'PASS','available_cards':len(Current['items']),'blocked_cards':len(Current['blocked_items']),'current_card':Card,'default_query_excludes_old_hash':all(H['sha256']!='1e8977c0137179a8a5009e8de9e5c3055a0596e1454d4e3ee3f9a6c0ec80f0d5' for H in Query['hits']),'query_verdict':Query['verdict'],'historical_superseded_review_warnings':Classified,'annotation_id':Note['annotation_id'],'versions':len(Store['nodes']),'correction_events':len(Store['events']),'canonical_modified':False}
for P in [Out/'library-final.json',Art/'library-final.json']:P.write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
(Art/'default-query.json').write_text(json.dumps(Query,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:V for K,V in Result.items() if K not in ['historical_superseded_review_warnings','current_card']}));print('Historical superseded warnings',len(Classified))
