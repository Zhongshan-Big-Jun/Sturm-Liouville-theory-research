from pathlib import Path
import sys, json, shutil
Root=Path('/mnt/f/LaTeX/BVE research'); Out=Path('/mnt/f/tools/math-audit-round5-20260921')
sys.path.insert(0,str(Root/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
Mode,Name=sys.argv[1:3]
Packet=json.loads((Out/(Name+'-review-packet.json')).read_text())
if Mode=='dispatch':
	Result=Review.record_dispatch(Root,Packet['packet'],json.loads((Out/(Name+'-review-spawn.json')).read_text()))
	Suffix='dispatch'
else:
	Dispatch=json.loads((Out/(Name+'-review-dispatch.json')).read_text())
	Result=Review.receive_review(Root,Dispatch['bundle'],json.loads((Out/(Name+'-review-completion.json')).read_text()))
	Review.verify_review_bundle(Root,Dispatch['bundle'])
	Suffix='receipt'
(Out/(Name+'-review-'+Suffix+'.json')).write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(Name,Result.get('verdict',Result.get('state')),Result.get('bundle',''))
