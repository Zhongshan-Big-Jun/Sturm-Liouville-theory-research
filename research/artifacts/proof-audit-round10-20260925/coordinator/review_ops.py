from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
Mode,Name=sys.argv[1:3]
RootRecord=O/(Name+'-root.json')
if RootRecord.exists():R=Path(json.loads(RootRecord.read_text())['project'])
def read(s):return json.loads((O/(Name+s+'.json')).read_text())
if Mode=='prepare':Result=V.create_packet(R,read('-spec'))
elif Mode=='dispatch':Result=V.record_dispatch(R,read('-packet')['packet'],read('-spawn'))
elif Mode=='receive':Result=V.receive_review(R,read('-dispatch')['bundle'],read('-completion')['result'])
elif Mode=='verify':Result=V.verify_review_bundle(R,read('-dispatch')['bundle'])
else:raise ValueError(Mode)
Suffix={'prepare':'packet','dispatch':'dispatch','receive':'received','verify':'verified'}[Mode]
(O/(Name+'-'+Suffix+'.json')).write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in Result.items() if k in ('verdict','packet_sha256','reviewer_id','bundle','state','trust')},ensure_ascii=False),flush=True)
