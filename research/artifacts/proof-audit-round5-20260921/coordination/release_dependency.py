from pathlib import Path
import sys,json,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round5-20260921')
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_corrections as C
import research_review as V
D=json.loads((O/'dependency-v2-review-dispatch.json').read_text());assert V.verify_review_bundle(R,D['bundle'])['verdict']=='APPROVED'
Rev=json.loads((O/'dependency-revision-result.json').read_text());assert not (O/'dependency-release-result.json').exists()
print('Releasing inherited obligation',Rev['revision_id'],datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
Result=C.release(R,Rev['revision_id'],D['bundle'])
(O/'dependency-release-result.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
assert Result['reuse_allowed'] and Result['verdict']=='RELEASED',Result
print(Result['verdict'],datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
