from pathlib import Path
import sys,json
Root=Path('/mnt/f/LaTeX/BVE research'); Out=Path('/mnt/f/tools/math-audit-round4-20260921')
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as Corrections
import research_review as Review
Name=sys.argv[1]
Rows=json.loads((Out/({'quotient':'quotient-revisions.json','recurrence':'recurrence-revisions.json','unchanged':'unchanged-renewals.json'}[Name])).read_text())
if Name=='recurrence': Rows+=json.loads((Out/'k1-revisions.json').read_text())
Bundle=json.loads((Out/(Name+'-review-dispatch.json')).read_text())['bundle']
Verdict=Review.verify_review_bundle(Root,Bundle)
assert Verdict['verdict']=='APPROVED'
Results=[]
for Row in Rows:
	Id=Row['revision']['revision_id'];Saved=Out/('release-'+Id+'.json')
	if Saved.exists(): Result=json.loads(Saved.read_text())
	else:
		Result=Corrections.release(Root,Id,Bundle)
		Saved.write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
	Results.append(Result)
	print(Name,Id,Result['verdict'],flush=True)
(Out/(Name+'-release-results.json')).write_text(json.dumps(Results,ensure_ascii=False,indent=2)+'\n')
