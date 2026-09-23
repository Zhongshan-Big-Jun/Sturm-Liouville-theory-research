from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_library as L
import research_review as V
bundle=json.loads((O/'renewal-review-dispatch.json').read_text())['bundle']
if V.verify_review_bundle(R,bundle)['verdict']!='APPROVED':raise RuntimeError('Renewal review not approved')
rows=json.loads((O/'renewals.json').read_text());groups={}
for x in rows:groups.setdefault(x['target']['location'],[]).append(x)
if len(rows)!=22 or len(groups)!=12:raise RuntimeError('Unexpected renewal scope')
dependencies={}
for loc,group in groups.items():
 raw=(R/loc).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=group[0]['target']['sha256']:raise RuntimeError('Unchanged card drift '+loc)
 front,_,_=L.read_metadata(raw)
 dependencies[loc]={d['location'] for d in C.card_dependencies(front) if d['location'] in groups}
order=[];pending=set(groups)
while pending:
 ready=sorted(loc for loc in pending if not (dependencies[loc]&pending))
 if not ready:raise RuntimeError('Renewal dependency cycle')
 order.extend(ready);pending.difference_update(ready)
output=O/'renewal-release-results.json';done=json.loads(output.read_text()) if output.exists() else []
for loc in order:
 for x in groups[loc]:
  if any(d['revision']==x['revision'] for d in done):continue
  result=C.release(R,x['revision'],bundle)
  done.append(dict(x,bundle=bundle,result=result))
  output.write_text(json.dumps(done,ensure_ascii=False,indent=2)+'\n')
  print(loc,x['issue'][:8],result['verdict'],flush=True)
  if result['verdict'] not in ['RELEASED','STILL_BLOCKED']:raise RuntimeError('Unexpected release outcome')
 # A card with multiple historical issues stays blocked until all its obligations are renewed.
 store=C.load_store(R);states,_=C.impact_states(R,store)
 if not states[C.key(groups[loc][0]['target'])]['reuse_allowed']:raise RuntimeError('Card remains blocked after all obligations '+loc)
print('Renewed twenty-two exact obligations on twelve unchanged cards.',flush=True)
