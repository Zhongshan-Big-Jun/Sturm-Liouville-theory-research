from pathlib import Path
import sys,json,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round4-20260921');Art=Root/'research/artifacts/proof-audit-round4-20260921'
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as Library
import research_corrections as Corrections
for Name in ['quotient','recurrence','unchanged','k1-dependency']: assert (Out/(Name+'-release-results.json')).exists(),Name
Card=json.loads((Out/'recurrence-card-result.json').read_text())
Note=Library.annotate(Root,Card['location'],Card['sha256'],author='coordinator-20260921-round4',kind='research-experience',locator='Exact factorial difference reduction and runtime checks',text='The factorial change of variables exposes a first-order recurrence for second differences, connecting finite reconstruction, positive infinite tails and rational-ratio obstruction for this exact coefficient family. When reusing implementations, preserve exact input conversion through wrapper functions and reject provably zero symbolic denominators. A negative test must be mathematically false: zero itself solves a homogeneous recurrence. See the fourth-round report and its preserved independent rejections; this annotation is research experience, not a new theorem or wider-family extension.')
(Out/'annotation-result.json').write_text(json.dumps(Note,ensure_ascii=False,indent=2)+'\n')
# Keep the generated pointer block intact while updating its human entry text.
P=Root/'tools/README.md';Raw=P.read_text();Marker='## 本轮修订入口\n';assert Raw.count(Marker)==1
Insert='## 第四轮修订 (2026-09-21)\n\n[三阶递推](third-order-recurrence.md)给出指定双奇偶系数族的正项尾解、一般c常数和全部有理比值分类; [K1锚点](third-order-minimal-K1.md)保留独立有限终端约定. [Krein-Sobolev](krein-sobolev-polynomials.md)区分普通函数代表与商类极限. [稳定性](jump-stability.md)及四张未改正文的卡片完成精确审计绑定续接. 原错误版本、退回记录和批注仍可溯源, 默认检索只按当前纠错状态复用. 证明、程序与局部Lean的不同范围见 [第四轮报告](../reports/proof-audit-round4-20260921/REPORT.md).\n\n'
P.write_text(Raw.replace(Marker,Insert+Marker))
Index=Library.make_index(Root); (Out/'index-result.json').write_text(json.dumps(Index,ensure_ascii=False,indent=2)+'\n')
Names=['third-order-recurrence','third-order-minimal-K1','krein-sobolev-polynomials','jump-stability','left-definite-theory','left-definite-moment-recurrence','moment-jump-completeness','denseness-criteria']
Query=Library.query_tools(Root,' '.join(Names+['left-definite-orthogonal-systems']),limit=50)
assert Query['verdict']=='RETRIEVAL_ONLY' and Query['changed_paths']==[],Query['verdict']
Hits={H['location']:H for H in Query['hits']}
for Name in Names:
	Loc='tools/'+Name+'.md';assert Loc in Hits and Hits[Loc]['reuse_allowed'],Loc
	assert Hits[Loc]['sha256']==hashlib.sha256((Root/Loc).read_bytes()).hexdigest(),Loc
assert 'tools/left-definite-orthogonal-systems.md' not in Hits
Current=json.loads((Root/'index/tools.json').read_text());assert len(Current['items'])==78 and len(Current['blocked_items'])==1
assert Current['blocked_items'][0]['location']=='tools/left-definite-orthogonal-systems.md'
# Old, superseded receipts legitimately remain invalid for current input bytes.
Store=Corrections.load_store(Root); Problems=Query['issues'];Classified=[]
for Problem in Problems:
	if Problem.get('status')!='REVIEW_NO_LONGER_VALID':
		raise AssertionError(('Unexpected query issue',Problem))
	Release=Store['requests'][Problem['release']]['payload'];Old=Store['requests'][Release['revision']]['payload']
	Loc=Old['new']['location'];assert Loc in Hits and Hits[Loc]['reuse_allowed']
	Latest=[E['request'] for E in Store['events'] if Store['requests'][E['request']]['kind']=='revision' and Store['requests'][E['request']]['payload']['issue']==Old['issue'] and Store['requests'][E['request']]['payload']['new']['location']==Loc][-1]
	assert Latest!=Release['revision']
	Classified.append(dict(Problem,location=Loc,classification='SUPERSEDED_HISTORICAL_RECEIPT',current_revision=Latest))
Result={'status':'PASS','available_cards':len(Current['items']),'blocked_cards':len(Current['blocked_items']),'checked_current_cards':Names,'query_verdict':Query['verdict'],'historical_superseded_review_warnings':Classified,'annotation_id':Note['annotation_id'],'versions':len(Store['nodes']),'correction_events':len(Store['events']),'canonical_modified':False}
(Out/'library-final.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n');(Art/'library-final.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
(Art/'default-query.json').write_text(json.dumps(Query,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:V for K,V in Result.items() if K!='historical_superseded_review_warnings'}));print('Historical superseded warnings',len(Classified))
