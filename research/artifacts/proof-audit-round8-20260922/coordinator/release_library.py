from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922')
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as V
for n in ['math-review','certificate-review']:
	d=json.loads((O/(n+'-dispatch.json')).read_text())
	if V.verify_review_bundle(R,d['bundle'])['verdict']!='APPROVED':raise RuntimeError('Missing current approval '+n)
bundle=json.loads((O/'math-review-dispatch.json').read_text())['bundle']
rows=json.loads((O/'revisions.json').read_text())
if len(rows)!=4:raise RuntimeError('Expected four card revisions')
p=O/'release-results.json';done=json.loads(p.read_text()) if p.exists() else []
for x in rows:
	if any(d['revision']==x['result']['revision_id'] for d in done):continue
	print('Releasing',x['name'],flush=True)
	result=C.release(R,x['result']['revision_id'],bundle)
	done.append(dict(name=x['name'],revision=x['result']['revision_id'],bundle=bundle,result=result));p.write_text(json.dumps(done,ensure_ascii=False,indent=2)+'\n')
	print(x['name'],result['verdict'],flush=True)
	if result['verdict']!='RELEASED':raise RuntimeError('Still unresolved: '+x['name'])
print('Four exact issue releases completed; actual query still required.',flush=True)
