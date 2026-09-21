from pathlib import Path
import sys,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round6-20260921');A=R/'research/artifacts/proof-audit-round6-20260921'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
import research_corrections as C
Done=json.loads((O/'release-results.json').read_text());assert len(Done)==19
Cards=json.loads((O/'cards.json').read_text())
Notes=json.loads((O/'annotations.json').read_text())
assert set(Notes)=={'constrained-denseness-runs','spectral-domain-checks'}
Index=json.loads((O/'index-result.json').read_text())
assert Index['verdict']=='INDEXED' and Index['indexed']==78 and Index['blocked']==1
assert (R/'tools/README.md').read_text().count('## 第六轮修订 (2026-09-21)')==1
print('Resuming final query with limit=50; prior releases, annotations and index preserved.',flush=True)
Query=L.query_tools(R,' '.join([*Cards,'third-order-recurrence','third-order-minimal-K1','left-definite-orthogonal-systems']),limit=50)
(O/'final-query-result.json').write_text(json.dumps(Query,ensure_ascii=False,indent=2)+'\n')
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
