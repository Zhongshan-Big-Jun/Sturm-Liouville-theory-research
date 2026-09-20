from pathlib import Path
import sys,json
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round4-20260921')
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as R
Name=sys.argv[1];File={'unchanged':'unchanged-renewals.json','k1-dependency':'k1-dependency-revisions.json'}[Name]
Rows=json.loads((Out/File).read_text());Bundle=json.loads((Out/(Name+'-review-dispatch.json')).read_text())['bundle'];assert R.verify_review_bundle(Root,Bundle)['verdict']=='APPROVED'
for Row in Rows:
	Id=Row['revision']['revision_id'];Saved=Out/('release-'+Id+'.json')
	if Saved.exists():continue
	Result=C.release(Root,Id,Bundle);Saved.write_text(json.dumps(Result,indent=2)+'\n');print(Name,Id,Result['verdict'],flush=True);break
Files=[Out/('release-'+Row['revision']['revision_id']+'.json') for Row in Rows]
if all(P.exists() for P in Files):
	(Out/(Name+'-release-results.json')).write_text(json.dumps([json.loads(P.read_text()) for P in Files],indent=2)+'\n');print('GROUP COMPLETE',Name)
else:print('Remaining',sum(not P.exists() for P in Files))
