from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research')
O=Path('/mnt/f/tools/math-audit-round8-20260922')
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_review as Review
mode,name=sys.argv[1:3]
def read(s): return json.loads((O/(name+s+'.json')).read_text())
if mode=='prepare': result=Review.create_packet(R,read('-spec'))
elif mode=='dispatch': result=Review.record_dispatch(R,read('-packet')['packet'],read('-spawn'))
elif mode=='receive': result=Review.receive_review(R,read('-dispatch')['bundle'],read('-completion')['result'])
elif mode=='verify': result=Review.verify_review_bundle(R,read('-dispatch')['bundle'])
else: raise ValueError(mode)
suffix={'prepare':'packet','dispatch':'dispatch','receive':'received','verify':'verified'}[mode]
(O/(name+'-'+suffix+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
