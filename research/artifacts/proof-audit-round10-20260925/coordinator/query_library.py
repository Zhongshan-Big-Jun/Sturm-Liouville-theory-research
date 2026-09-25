from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Cards=list(json.loads((O/'cards.json').read_text()).values())
Renew=[X['target'] for X in json.loads((O/'renewals.json').read_text())]
Q=L.query_tools(R,' '.join([X['location'].removeprefix('tools/').removesuffix('.md') for X in Cards+Renew]),limit=50)
(O/'retrieval-result.json').write_text(json.dumps(Q,ensure_ascii=False,indent=2)+'\n')
Hits={X['location']:X for X in Q['hits']}
for Card in Cards+Renew:
 H=Hits.get(Card['location'])
 if not H or H['sha256']!=Card['sha256'] or not H['reuse_allowed']:raise RuntimeError('Current approved card missing '+Card['location'])
 Raw=(R/Card['location']).read_bytes();Front,Body,_=L.read_metadata(Raw)
 if hashlib.sha256(Raw).hexdigest()!=H['sha256']:raise RuntimeError('Actual hash drift')
 if Front.get('summary') and H['summary']!=Front['summary']:raise RuntimeError('Inherited stale summary')
 for Typ in ['sources','evidence']:
  for Ref in H[Typ]:
   if (Ref.get('path') or Ref.get('source_id')) and Ref['binding_state']!='CURRENT':raise RuntimeError('Stale source/evidence '+str(Ref))
for Card in Cards:
 if not any(N['state']=='CURRENT' for N in Hits[Card['location']]['annotations']):raise RuntimeError('New annotation missing')
Notes=json.loads((O/'annotations.json').read_text())
if len(Notes)!=5:raise RuntimeError('Expected five current correction annotations')
for Note in Notes:
 Location='research/library/annotations/'+Note['annotation_id']+'.json'
 Raw=(R/Location).read_bytes()
 Expected={K:V for K,V in Note.items() if K!='annotation_id'}
 if json.loads(Raw)!=Expected:raise RuntimeError('Annotation content differs '+Location)
 Matches=[N for N in Hits[Note['tool_path']]['annotations'] if N['path']==Location]
 if len(Matches)!=1 or Matches[0]['state']!='CURRENT' or Matches[0]['sha256']!=hashlib.sha256(Raw).hexdigest() or Matches[0]['tool_sha256']!=Note['tool_sha256']:raise RuntimeError('Exact new annotation not retrievable '+Location)
if Q['verdict']!='RETRIEVAL_ONLY' or Q['changed_paths'] or Q['blocked']!=1:raise RuntimeError('Query state invalid')
I=json.loads((R/'index/tools.json').read_text())
if len(I['items'])!=89 or len(I['blocked_items'])!=1:raise RuntimeError('Index count mismatch')
if I['blocked_items'][0]['location']!='tools/left-definite-orthogonal-systems.md':raise RuntimeError('Unexpected blocked current card')
Releases=json.loads((O/'current-release-results.json').read_text())
for Name,Expected in [('renewal-review',json.loads((O/'renewals.json').read_text())),('math-review',json.loads((O/'current-revisions.json').read_text()))]:
 Bundle=json.loads((O/(Name+'-dispatch.json')).read_text())['bundle']
 for Row in Expected:
  if not any(D['revision']==Row['revision'] and D['bundle']==Bundle and D['target']==Row['target'] for D in Releases):raise RuntimeError('Current review release missing '+Row['revision'])
Summary={'status':'PASS','available':89,'original_withdrawn':1,'verified_current_obligations':15,'verified_current_cards':8,'historical_warnings':len(I.get('issues',[])),'query':Q['verdict'],'returned_hits':len(Hits),'targets':[{'location':X['location'],'sha256':X['sha256'],'summary':Hits[X['location']]['summary'],'dependencies':Hits[X['location']]['dependencies']} for X in Cards+Renew]}
Summary['verified_new_annotations']=[{'annotation_id':N['annotation_id'],'tool_path':N['tool_path'],'tool_sha256':N['tool_sha256'],'status':N['status']} for N in Notes]
(O/'library-verification.json').write_text(json.dumps(Summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:V for K,V in Summary.items() if K!='targets'}),flush=True)
